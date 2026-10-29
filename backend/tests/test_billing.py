"""Billing + critique credit tests. OpenAI and Stripe are stubbed; the credit store is in memory.

Run from backend/:  OPENAI_API_KEY=x python -m pytest -q
"""

import json
import os
import types

import pytest

os.environ.setdefault("OPENAI_API_KEY", "x")

from fastapi.testclient import TestClient  # noqa: E402

from app.api.v1 import routes_critique  # noqa: E402
from app.main import app  # noqa: E402
from app.services import billing, critics  # noqa: E402

DOC = {"strategy_doc": "x" * 40}


def _fake_openai(fail_lens=None):
    def call(model_id, prompt):
        lens = prompt.split('"lens": "')[1].split('"')[0]
        if lens == fail_lens:
            raise RuntimeError("boom")
        return json.dumps({"lens": lens, "summary": "s",
                           "flaws": [{"title": "t", "severity": "low", "description": "d", "question": "q"}]})
    return call


class FakeSession(dict):
    @property
    def url(self):
        return self["url"]


class FakeStripe:
    def __init__(self):
        self.sessions = {}
        self.checkout = types.SimpleNamespace(Session=types.SimpleNamespace(
            create=self._create, retrieve=self._retrieve))

    def _create(self, **kw):
        sid = f"cs_test_{len(self.sessions) + 1:04d}abcdef"
        s = FakeSession(id=sid, url=f"https://checkout.stripe.test/{sid}", metadata=kw["metadata"],
                        payment_status="unpaid", customer_details={"email": "buyer@example.com"})
        self.sessions[sid] = s
        self.last_kwargs = kw
        return s

    def _retrieve(self, sid):
        if sid not in self.sessions:
            raise LookupError(sid)
        return self.sessions[sid]


@pytest.fixture
def env(monkeypatch):
    for k in ("PAYMENTS_ENABLED", "STRIPE_SECRET_KEY", "ALLOW_LIVE_PAYMENTS", "DATABASE_URL", "PUBLIC_SITE_URL"):
        monkeypatch.delenv(k, raising=False)
    routes_critique._ip_buckets.clear()
    billing.set_store(billing.MemoryCreditStore())
    monkeypatch.setattr(critics, "_call_openai", _fake_openai())
    return monkeypatch


@pytest.fixture
def paid_env(env):
    env.setenv("PAYMENTS_ENABLED", "true")
    env.setenv("STRIPE_SECRET_KEY", "sk_test_123")
    env.setenv("DATABASE_URL", "postgres://unused")  # store is overridden with the memory store
    fake = FakeStripe()
    from app.api.v1 import routes_billing
    env.setattr(routes_billing, "_stripe", lambda settings: fake)
    return fake


def _events(text):
    out = []
    for block in text.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.split("\n"))
        out.append((lines["event"], json.loads(lines["data"])))
    return out


def _buy(client, fake):
    url = client.post("/api/v1/billing/checkout").json()["url"]
    sid = url.rsplit("/", 1)[1]
    fake.sessions[sid]["payment_status"] = "paid"
    return sid


# ── Settings / safety ─────────────────────────────────────────────────────────

def test_payments_off_by_default(env):
    c = TestClient(app)
    cfg = c.get("/api/v1/billing/config").json()
    assert cfg["payments_enabled"] is False
    assert cfg["pack"] == {"credits": 25, "price_cents": 900, "currency": "usd"}
    assert c.post("/api/v1/billing/checkout").status_code == 503


def test_live_key_refused_without_unlock(env):
    env.setenv("PAYMENTS_ENABLED", "true")
    env.setenv("STRIPE_SECRET_KEY", "sk_live_abc")
    env.setenv("DATABASE_URL", "postgres://x")
    s = billing.load_settings()
    assert not s.payments_enabled and "live Stripe key refused" in s.disabled_reason
    env.setenv("ALLOW_LIVE_PAYMENTS", "true")
    assert billing.load_settings().payments_enabled


def test_config_reports_test_mode(paid_env):
    cfg = TestClient(app).get("/api/v1/billing/config").json()
    assert cfg["payments_enabled"] is True and cfg["test_mode"] is True


# ── Checkout + claim ──────────────────────────────────────────────────────────

def test_checkout_params(paid_env):
    TestClient(app).post("/api/v1/billing/checkout")
    kw = paid_env.last_kwargs
    assert kw["mode"] == "payment"
    assert kw["line_items"][0]["price_data"]["unit_amount"] == 900
    assert kw["metadata"]["product"] == "founder_pack"
    assert "{CHECKOUT_SESSION_ID}" in kw["success_url"]


def test_claim_requires_payment_and_is_idempotent(paid_env):
    c = TestClient(app)
    url = c.post("/api/v1/billing/checkout").json()["url"]
    sid = url.rsplit("/", 1)[1]
    assert c.post("/api/v1/billing/claim", json={"session_id": sid}).status_code == 402
    paid_env.sessions[sid]["payment_status"] = "paid"
    r1 = c.post("/api/v1/billing/claim", json={"session_id": sid}).json()
    r2 = c.post("/api/v1/billing/claim", json={"session_id": sid}).json()
    assert r1 == r2 and r1["credits_remaining"] == 25 and r1["code"].startswith("VDX-")


def test_claim_rejects_unknown_and_foreign_sessions(paid_env):
    c = TestClient(app)
    assert c.post("/api/v1/billing/claim", json={"session_id": "cs_test_nope000000"}).status_code == 404
    sid = _buy(c, paid_env)
    paid_env.sessions[sid]["metadata"] = {"product": "something_else"}
    assert c.post("/api/v1/billing/claim", json={"session_id": sid}).status_code == 400


# ── Spending credits ──────────────────────────────────────────────────────────

def test_paid_critique_spends_one_credit_and_skips_free_limit(paid_env):
    c = TestClient(app)
    code = c.post("/api/v1/billing/claim", json={"session_id": _buy(c, paid_env)}).json()["code"]
    for expected in (24, 23, 22, 21):  # more than the 3 free per day
        r = c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": code.lower()})
        assert r.status_code == 200
        assert _events(r.text)[-1] == ("done", {"credits_remaining": expected})
    assert c.post("/api/v1/billing/balance", json={"code": code}).json()["credits_remaining"] == 21


def test_credit_refunded_when_a_lens_fails(paid_env):
    c = TestClient(app)
    code = c.post("/api/v1/billing/claim", json={"session_id": _buy(c, paid_env)}).json()["code"]
    paid_env_patch = pytest.MonkeyPatch()
    paid_env_patch.setattr(critics, "_call_openai", _fake_openai(fail_lens="evidence_audit"))
    try:
        r = c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": code})
    finally:
        paid_env_patch.undo()
    done = _events(r.text)[-1]
    assert done == ("done", {"credit_refunded": True, "credits_remaining": 25})


def test_empty_or_bad_code_gets_402(paid_env):
    c = TestClient(app)
    assert c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": "VDX-AAAA-BBBB-CCCC"}).status_code == 402
    assert c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": "garbage"}).status_code == 402
    store = billing.MemoryCreditStore()
    billing.set_store(store)
    code, _ = store.mint_for_session("cs_test_x", None, 1)
    assert c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": code}).status_code == 200
    assert c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": code}).status_code == 402


def test_code_ignored_when_payments_off(env):
    c = TestClient(app)
    for _ in range(3):
        assert c.post("/api/v1/critique/stream", json=DOC, headers={"X-Veridex-Code": "VDX-AAAA-BBBB-CCCC"}).status_code == 200
    assert c.post("/api/v1/critique/stream", json=DOC).status_code == 429


# ── Free tier ─────────────────────────────────────────────────────────────────

def test_free_limit_is_three_per_day_per_visitor(env):
    c = TestClient(app)
    a = {"X-Forwarded-For": "203.0.113.5, 10.0.0.1"}
    b = {"X-Forwarded-For": "198.51.100.7, 10.0.0.1"}
    assert [c.post("/api/v1/critique/stream", json=DOC, headers=a).status_code for _ in range(4)] == [200, 200, 200, 429]
    r = c.post("/api/v1/critique/stream", json=DOC, headers=a)
    assert r.json()["detail"]["window"] == "day" and r.json()["detail"]["retry_after_seconds"] > 80_000
    # A different visitor behind the same proxy is not affected.
    assert c.post("/api/v1/critique/stream", json=DOC, headers=b).status_code == 200
