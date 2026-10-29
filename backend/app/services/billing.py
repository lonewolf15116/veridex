"""
Billing: Founder Pack credit codes sold through Stripe Checkout.

Model
  - One critique (all five lenses) costs one credit.
  - A Founder Pack is FOUNDER_PACK_CREDITS credits for FOUNDER_PACK_PRICE_CENTS, never expiring.
  - A paid buyer gets a code (e.g. VDX-7K3M-Q9TD-X2HF). The frontend sends it in the
    X-Veridex-Code header; no accounts.
  - If any lens fails during a paid critique, the credit is refunded.

Safety
  - Payments are OFF unless PAYMENTS_ENABLED=true and Stripe + database settings are present.
  - Live Stripe keys (sk_live_...) are refused unless ALLOW_LIVE_PAYMENTS=true, so the site
    cannot start taking real money by accident.

Environment
  PAYMENTS_ENABLED       "true" to turn the feature on
  STRIPE_SECRET_KEY      sk_test_... (or sk_live_... with ALLOW_LIVE_PAYMENTS=true)
  ALLOW_LIVE_PAYMENTS    "true" only when you are allowed to take real payments
  DATABASE_URL           Postgres connection string (e.g. Supabase pooler URL)
  PUBLIC_SITE_URL        where Stripe sends buyers back (default https://www.veridex.fyi)
"""

from __future__ import annotations

import os
import secrets
import threading
from dataclasses import dataclass
from typing import Optional, Protocol

FOUNDER_PACK_CREDITS = 25
FOUNDER_PACK_PRICE_CENTS = 900
FOUNDER_PACK_CURRENCY = "usd"
FOUNDER_PACK_PRODUCT = "founder_pack"

_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I


def new_code() -> str:
    groups = ["".join(secrets.choice(_CODE_ALPHABET) for _ in range(4)) for _ in range(3)]
    return "VDX-" + "-".join(groups)


def normalise_code(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    code = raw.strip().upper()
    if not code.startswith("VDX-") or len(code) != 18:
        return None
    return code


# ── Settings ──────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class BillingSettings:
    enabled_flag: bool
    stripe_key: str
    allow_live: bool
    database_url: str
    site_url: str

    @property
    def is_live_key(self) -> bool:
        return self.stripe_key.startswith(("sk_live_", "rk_live_"))

    @property
    def test_mode(self) -> bool:
        return not self.is_live_key

    @property
    def disabled_reason(self) -> Optional[str]:
        if not self.enabled_flag:
            return "PAYMENTS_ENABLED is not true"
        if not self.stripe_key:
            return "STRIPE_SECRET_KEY is missing"
        if not self.database_url:
            return "DATABASE_URL is missing"
        if self.is_live_key and not self.allow_live:
            return "live Stripe key refused (set ALLOW_LIVE_PAYMENTS=true to allow real payments)"
        return None

    @property
    def payments_enabled(self) -> bool:
        return self.disabled_reason is None


def load_settings() -> BillingSettings:
    return BillingSettings(
        enabled_flag=os.getenv("PAYMENTS_ENABLED", "").strip().lower() == "true",
        stripe_key=os.getenv("STRIPE_SECRET_KEY", "").strip(),
        allow_live=os.getenv("ALLOW_LIVE_PAYMENTS", "").strip().lower() == "true",
        database_url=os.getenv("DATABASE_URL", "").strip(),
        site_url=os.getenv("PUBLIC_SITE_URL", "https://www.veridex.fyi").strip().rstrip("/"),
    )


# ── Credit store ──────────────────────────────────────────────────────────────

class CreditStore(Protocol):
    def mint_for_session(self, session_id: str, email: Optional[str], credits: int) -> tuple[str, int]: ...
    def consume(self, code: str) -> Optional[int]: ...
    def refund(self, code: str) -> None: ...
    def balance(self, code: str) -> Optional[int]: ...


class MemoryCreditStore:
    """In-process store for tests and local development. Not persistent."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._codes: dict[str, dict] = {}
        self._by_session: dict[str, str] = {}

    def mint_for_session(self, session_id, email, credits):
        with self._lock:
            if session_id in self._by_session:
                code = self._by_session[session_id]
            else:
                code = new_code()
                self._codes[code] = {"total": credits, "used": 0, "email": email}
                self._by_session[session_id] = code
            row = self._codes[code]
            return code, row["total"] - row["used"]

    def consume(self, code):
        with self._lock:
            row = self._codes.get(code)
            if not row or row["used"] >= row["total"]:
                return None
            row["used"] += 1
            return row["total"] - row["used"]

    def refund(self, code):
        with self._lock:
            row = self._codes.get(code)
            if row and row["used"] > 0:
                row["used"] -= 1

    def balance(self, code):
        with self._lock:
            row = self._codes.get(code)
            return None if row is None else row["total"] - row["used"]


class PostgresCreditStore:
    """Postgres-backed store. One short connection per call (fine at this volume)."""

    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS credit_codes (
        code              TEXT PRIMARY KEY,
        stripe_session_id TEXT UNIQUE NOT NULL,
        email             TEXT,
        credits_total     INTEGER NOT NULL,
        credits_used      INTEGER NOT NULL DEFAULT 0 CHECK (credits_used >= 0),
        created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """

    def __init__(self, database_url: str) -> None:
        self._url = database_url
        self._schema_ready = False
        self._lock = threading.Lock()

    def _connect(self):
        import psycopg  # imported lazily so the app runs without it when payments are off
        # prepare_threshold=None: Supabase's transaction pooler does not support prepared statements.
        return psycopg.connect(self._url, autocommit=True, prepare_threshold=None, connect_timeout=10)

    def _ensure_schema(self, conn) -> None:
        if self._schema_ready:
            return
        with self._lock:
            if not self._schema_ready:
                conn.execute(self._SCHEMA)
                self._schema_ready = True

    def mint_for_session(self, session_id, email, credits):
        with self._connect() as conn:
            self._ensure_schema(conn)
            # Retry on the (astronomically unlikely) code collision.
            for _ in range(5):
                code = new_code()
                cur = conn.execute(
                    """
                    INSERT INTO credit_codes (code, stripe_session_id, email, credits_total)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (code, session_id, email, credits),
                )
                row = conn.execute(
                    "SELECT code, credits_total - credits_used FROM credit_codes WHERE stripe_session_id = %s",
                    (session_id,),
                ).fetchone()
                if row:
                    return row[0], row[1]
                if cur.rowcount == 0:
                    continue  # code collided with another session's code; try a new one
            raise RuntimeError("could not mint a credit code")

    def consume(self, code):
        with self._connect() as conn:
            self._ensure_schema(conn)
            row = conn.execute(
                """
                UPDATE credit_codes SET credits_used = credits_used + 1
                WHERE code = %s AND credits_used < credits_total
                RETURNING credits_total - credits_used
                """,
                (code,),
            ).fetchone()
            return None if row is None else row[0]

    def refund(self, code):
        with self._connect() as conn:
            self._ensure_schema(conn)
            conn.execute(
                "UPDATE credit_codes SET credits_used = credits_used - 1 WHERE code = %s AND credits_used > 0",
                (code,),
            )

    def balance(self, code):
        with self._connect() as conn:
            self._ensure_schema(conn)
            row = conn.execute(
                "SELECT credits_total - credits_used FROM credit_codes WHERE code = %s", (code,)
            ).fetchone()
            return None if row is None else row[0]


_store: Optional[CreditStore] = None
_store_lock = threading.Lock()


def get_store() -> CreditStore:
    global _store
    if _store is None:
        with _store_lock:
            if _store is None:
                url = load_settings().database_url
                _store = PostgresCreditStore(url) if url else MemoryCreditStore()
    return _store


def set_store(store: CreditStore) -> None:
    """Override the store (tests)."""
    global _store
    _store = store
