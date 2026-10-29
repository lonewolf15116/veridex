"""
Critique streaming endpoint.

POST /api/v1/critique/stream
Body: {"strategy_doc": "<the user's strategy text>"}

Returns Server-Sent Events. Event types:
  - pass_started   {"lens": "<lens>"}
  - pass_completed {"lens": "<lens>", "result": <CriticPassResult>}
  - error          {"lens": "<lens>", "reason": "<string>"}
  - done           {}

All five lenses run in parallel. Each pass emits `pass_started` as soon as it begins
and `pass_completed` (or `error`) as soon as it finishes.

Rate limiting: 5 critiques per IP per hour, in-memory, resets on process restart.
"""

from __future__ import annotations

import asyncio
import json
import os
import secrets
import time
from collections import defaultdict
from typing import AsyncIterator

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.critics import (
    CriticValidationError,
    run_critic_pass,
)


router = APIRouter()

LENSES = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]

# ── Rate limiter ──────────────────────────────────────────────────────────────
# Simple in-memory per-IP bucket. Each entry is a list of timestamps (floats).
# We keep only timestamps within the last WINDOW_SECONDS on each check.

RATE_LIMIT   = 5          # max requests per window
WINDOW_SECS  = 3600       # 1 hour

_ip_buckets: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(ip: str) -> None:
    """Raise HTTP 429 if the IP has exceeded RATE_LIMIT requests in the last hour."""
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
                "message": f"Rate limit exceeded. Max {RATE_LIMIT} critiques per hour per IP.",
                "limit": RATE_LIMIT,
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
    lenses: list[str] | None = Field(
        default=None,
        description="Evaluation only: run just these lenses. Ignored without a valid X-Eval-Token.",
    )


def _is_eval(token: str | None) -> bool:
    """True when the request carries the EVAL_TOKEN configured on the server."""
    expected = os.getenv("EVAL_TOKEN", "")
    return bool(expected) and bool(token) and secrets.compare_digest(token, expected)


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


async def _stream(strategy_doc: str, lenses: list[str] = LENSES) -> AsyncIterator[str]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    tasks = [asyncio.create_task(_run_one(lens, strategy_doc, queue)) for lens in lenses]

    total_events = len(tasks) * 2  # each task: pass_started + pass_completed/error
    for _ in range(total_events):
        yield await queue.get()

    await asyncio.gather(*tasks, return_exceptions=True)
    yield _sse("done", {})


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/critique/stream")
async def critique_stream(
    request: Request,
    body: CritiqueRequest,
    x_eval_token: str | None = Header(default=None),
):
    lenses = LENSES
    if _is_eval(x_eval_token):
        # Evaluation runs skip the free limit and may select lenses.
        if body.lenses:
            unknown = [l for l in body.lenses if l not in LENSES]
            if unknown:
                raise HTTPException(status_code=422, detail={"message": f"Unknown lenses: {unknown}"})
            lenses = body.lenses
    else:
        ip = request.client.host if request.client else "unknown"
        _check_rate_limit(ip)

    return StreamingResponse(
        _stream(body.strategy_doc, lenses),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
