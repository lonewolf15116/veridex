"""
Critique streaming endpoint.

POST /api/v1/critique/stream
Body: {"strategy_doc": "<the user's strategy text>"}

Returns Server-Sent Events. Event types:
  - pass_started   {"lens": "<lens>"}
  - pass_completed {"lens": "<lens>", "result": <CriticPassResult>}
  - error          {"lens": "<lens>", "reason": "<string>"}
  - done           {}

All four lenses run in parallel. Each pass emits `pass_started` as soon as it begins
and `pass_completed` (or `error`) as soon as it finishes.

Rate limiting: 5 critiques per IP per hour, in-memory, resets on process restart.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections import defaultdict
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.critics import (
    CriticValidationError,
    run_critic_pass,
)


router = APIRouter()

LENSES = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk"]

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
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} critiques per hour per IP.",
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


async def _stream(strategy_doc: str) -> AsyncIterator[str]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    tasks = [asyncio.create_task(_run_one(lens, strategy_doc, queue)) for lens in LENSES]

    total_events = len(tasks) * 2  # each task: pass_started + pass_completed/error
    for _ in range(total_events):
        yield await queue.get()

    await asyncio.gather(*tasks, return_exceptions=True)
    yield _sse("done", {})


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/critique/stream")
async def critique_stream(request: Request, body: CritiqueRequest):
    ip = request.client.host if request.client else "unknown"
    _check_rate_limit(ip)

    return StreamingResponse(
        _stream(body.strategy_doc),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
