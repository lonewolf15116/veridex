"""
Critique streaming endpoint.

POST /api/v1/critique/stream
Body: {"strategy_doc": "<the user's strategy text>"}

Returns Server-Sent Events. Event types:
  - pass_started   {"lens": "<lens>"}
  - pass_completed {"lens": "<lens>", "result": <CriticPassResult>}
  - error          {"lens": "<lens>", "reason": "<string>"}
  - done           {"credits_remaining": <int>}   (credits_remaining only for paid critiques)

All five lenses run in parallel. Each pass emits `pass_started` as soon as it begins
and `pass_completed` (or `error`) as soon as it finishes.

Free tier: FREE_LIMIT critiques per client IP per rolling 24 hours, in-memory (resets on restart).
Paid: send a Founder Pack code in the X-Veridex-Code header. One critique spends one credit and
skips the free limit; the credit is refunded if any lens fails.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections import defaultdict
from typing import AsyncIterator

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services import billing
from app.services.critics import (
    CriticValidationError,
    run_critic_pass,
)


router = APIRouter()

LENSES = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]

# ── Free-tier limiter ─────────────────────────────────────────────────────────
# Simple in-memory per-IP bucket. Each entry is a list of timestamps (floats).
# We keep only timestamps within the last WINDOW_SECS on each check.

RATE_LIMIT   = 3          # free critiques per window
WINDOW_SECS  = 86_400     # rolling 24 hours

_ip_buckets: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(ip: str) -> None:
    """Raise HTTP 429 if the IP has used RATE_LIMIT free critiques in the last 24 hours."""
    now  = time.monotonic()
    cutoff = now - WINDOW_SECS
    bucket = [t for t in _ip_buckets[ip] if t > cutoff]
    if len(bucket) >= RATE_LIMIT:
        # The oldest request in the window is the next one to expire.
        retry_after = max(1, int(bucket[0] + WINDOW_SECS - now) + 1)
        _ip_buckets[ip] = bucket
        raise HTTPException(
            status_code=429,
            detail={
                "message": f"Free limit reached. Max {RATE_LIMIT} free critiques per day.",
                "limit": RATE_LIMIT,
                "window": "day",
                "retry_after_seconds": retry_after,
            },
            headers={"Retry-After": str(retry_after)},
        )
    bucket.append(now)
    _ip_buckets[ip] = bucket


# ── Request model ─────────────────────────────────────────────────────────────

class CritiqueRequest(BaseModel):
    strategy_doc: str = Field(
        ...,
        min_length=20,
        max_length=10_000,
        description="The strategy document to critique. Max 10,000 characters.",
    )


# ── SSE helpers ───────────────────────────────────────────────────────────────

def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _run_one(lens: str, strategy_doc: str, queue: asyncio.Queue) -> None:
    await queue.put(_sse("pass_started", {"lens": lens}))
    try:
        result = await asyncio.to_thread(run_critic_pass, lens, strategy_doc)
        await queue.put(
            _sse("pass_completed", {"lens": lens, "result": result.model_dump()})
        )
    except CriticValidationError as e:
        await queue.put(_sse("error", {"lens": lens, "reason": f"validation: {e.reason}"}))
    except Exception as e:  # noqa: BLE001
        await queue.put(_sse("error", {"lens": lens, "reason": f"{type(e).__name__}: {e}"}))


def client_ip(request: Request) -> str:
    """Best guess at the visitor's IP behind Render's proxy.

    request.client.host is the proxy's address on Render, which would put every visitor in
    one shared bucket. Prefer the proxy-supplied headers, falling back to the socket peer.
    """
    for header in ("cf-connecting-ip", "true-client-ip"):
        value = request.headers.get(header)
        if value:
            return value.strip()
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        first = forwarded.split(",")[0].strip()
        if first:
            return first
    return request.client.host if request.client else "unknown"


async def _stream(strategy_doc: str, paid_code: str | None = None) -> AsyncIterator[str]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    tasks = [asyncio.create_task(_run_one(lens, strategy_doc, queue)) for lens in LENSES]

    any_error = False
    total_events = len(tasks) * 2  # each task: pass_started + pass_completed/error
    for _ in range(total_events):
        event = await queue.get()
        if event.startswith("event: error"):
            any_error = True
        yield event

    await asyncio.gather(*tasks, return_exceptions=True)

    done: dict = {}
    if paid_code:
        store = billing.get_store()
        if any_error:
            await asyncio.to_thread(store.refund, paid_code)
            done["credit_refunded"] = True
        done["credits_remaining"] = await asyncio.to_thread(store.balance, paid_code)
    yield _sse("done", done)


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/critique/stream")
async def critique_stream(
    request: Request,
    body: CritiqueRequest,
    x_veridex_code: str | None = Header(default=None),
):
    paid_code = None
    if x_veridex_code and billing.load_settings().payments_enabled:
        code = billing.normalise_code(x_veridex_code)
        remaining = None if code is None else await asyncio.to_thread(billing.get_store().consume, code)
        if remaining is None:
            raise HTTPException(
                status_code=402,
                detail={"message": "That code isn't valid or has no critiques left.", "code_status": "invalid_or_empty"},
            )
        paid_code = code
    else:
        _check_rate_limit(client_ip(request))

    return StreamingResponse(
        _stream(body.strategy_doc, paid_code),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
