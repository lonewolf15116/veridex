"""
Critique streaming endpoint.

POST /api/v1/critique/stream
Body: {"strategy_doc": "<the user's strategy text>"}

Returns Server-Sent Events. Event types:
  - pass_started   {"lens": "<lens>"}
  - pass_completed {"lens": "<lens>", "result": <CriticPassResult>}
  - error          {"lens": "<lens>", "reason": "<string>"}
  - done           {}                                       plain critique (unchanged)
                   {"questions": [...], "refine_token": "..."}  idea mode (stage set)
                   {"refinement": {lenses, gaps_filled, gaps_skipped}}  idea-mode refinement

Idea builder (Revision 2): `stage` switches on idea-stage calibration and gap tags; `refine`
re-runs only the lenses the founder's answers inform, free once per critique via refine_token
(refused with 409, never charged, if the token is used or expired). Answering a gap never marks a
flaw resolved; the new critique is the verdict.

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

from app.services import builder
from app.services.critics import (
    Stage,
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

class RefineRequest(BaseModel):
    """The one free refinement of an idea-mode critique (idea builder, Revision 2)."""
    token: str = Field(..., min_length=10, max_length=600)
    answers: list[builder.Answer] = Field(..., min_length=1, max_length=len(builder.QUESTION_BANK))


class CritiqueRequest(BaseModel):
    strategy_doc: str = Field(
        ...,
        min_length=20,
        max_length=10_000,
        description="The strategy document to critique, or in idea mode the founder's idea. Max 10,000 characters.",
    )
    lenses: list[str] | None = Field(
        default=None,
        description="Evaluation only: run just these lenses. Ignored without a valid X-Eval-Token.",
    )
    stage: Stage | None = Field(
        default=None,
        description="Idea builder: the founder-declared stage. Omit for a plain paste-a-plan critique.",
    )
    answers: list[builder.Answer] | None = Field(
        default=None,
        description="Idea builder full form: answers given up front. Requires stage.",
    )
    refine: RefineRequest | None = Field(
        default=None,
        description="Idea builder: re-run only the lenses these answers inform. Requires stage and an unused refine token.",
    )


def _is_eval(token: str | None) -> bool:
    """True when the request carries the EVAL_TOKEN configured on the server."""
    expected = os.getenv("EVAL_TOKEN", "")
    return bool(expected) and bool(token) and secrets.compare_digest(token, expected)


# ── SSE helpers ───────────────────────────────────────────────────────────────

def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _run_one(lens: str, strategy_doc: str, queue: asyncio.Queue, stage: str | None, results: dict) -> None:
    await queue.put(_sse("pass_started", {"lens": lens}))
    try:
        result = await asyncio.to_thread(run_critic_pass, lens, strategy_doc, stage=stage)
        results[lens] = result
        await queue.put(
            _sse("pass_completed", {"lens": lens, "result": result.model_dump(exclude_none=stage is None)})
        )
    except CriticValidationError as e:
        await queue.put(_sse("error", {"lens": lens, "reason": f"validation: {e.reason}"}))
    except Exception as e:  # noqa: BLE001
        await queue.put(_sse("error", {"lens": lens, "reason": f"{type(e).__name__}: {e}"}))


async def _stream(
    strategy_doc: str,
    lenses: list[str] = LENSES,
    stage: str | None = None,
    refinement: dict | None = None,
) -> AsyncIterator[str]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    results: dict = {}
    tasks = [asyncio.create_task(_run_one(lens, strategy_doc, queue, stage, results)) for lens in lenses]

    total_events = len(tasks) * 2  # each task: pass_started + pass_completed/error
    for _ in range(total_events):
        yield await queue.get()

    await asyncio.gather(*tasks, return_exceptions=True)

    done: dict = {}
    if refinement is not None:
        # A record of what the founder supplied. It does NOT say any flaw is resolved: the new
        # critique above is the verdict.
        done["refinement"] = refinement
    elif stage is not None:
        done["questions"] = [q.model_dump() for q in builder.select_questions(results)]
        done["refine_token"] = builder.issue_refine_token(stage)
    yield _sse("done", done)


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/critique/stream")
async def critique_stream(
    request: Request,
    body: CritiqueRequest,
    x_eval_token: str | None = Header(default=None),
):
    is_eval = _is_eval(x_eval_token)
    stage = body.stage
    if (body.answers or body.refine) and stage is None:
        raise HTTPException(status_code=422, detail={"message": "answers and refine need a stage."})
    if body.answers and body.refine:
        raise HTTPException(status_code=422, detail={"message": "Send answers either up front or as a refinement, not both."})

    # Refinement: only the informed lenses, free with an unused token, otherwise refused (never charged).
    if body.refine is not None:
        lenses = builder.lenses_for_answers(body.refine.answers)
        if not lenses:
            raise HTTPException(status_code=422, detail={"message": "Answer at least one question to refine."})
        if not is_eval and not builder.redeem_refine_token(body.refine.token):
            raise HTTPException(
                status_code=409,
                detail={"message": "This critique's free refinement has already been used or has expired. Start a new critique to refine again.",
                        "code_status": "refine_unavailable"},
            )
        doc = builder.compose_brief(body.strategy_doc, stage, body.refine.answers)
        answered = [a for a in body.refine.answers if not a.skipped and (a.text.strip() or a.numbers)]
        refinement = {
            "lenses": lenses,
            "gaps_filled": [a.gap for a in answered],
            "gaps_skipped": [a.gap for a in body.refine.answers if a not in answered],
        }
        return _response(_stream(doc, lenses, stage, refinement))

    lenses = LENSES
    if is_eval:
        # Evaluation runs skip the free limit and may select lenses.
        if body.lenses:
            unknown = [l for l in body.lenses if l not in LENSES]
            if unknown:
                raise HTTPException(status_code=422, detail={"message": f"Unknown lenses: {unknown}"})
            lenses = body.lenses
    else:
        ip = request.client.host if request.client else "unknown"
        _check_rate_limit(ip)

    doc = body.strategy_doc if stage is None else builder.compose_brief(body.strategy_doc, stage, body.answers or [])
    return _response(_stream(doc, lenses, stage))


def _response(stream: AsyncIterator[str]) -> StreamingResponse:
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
