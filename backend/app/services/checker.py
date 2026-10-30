"""
Checker pass — a second, cheap review of a lens's draft critique.

The checker can only KEEP, DOWNGRADE or DROP the draft's flaws. It cannot add flaws or rewrite
them, because it returns decisions by index and the code applies them. It also rates the
document's evidence strength, and the code enforces severity caps for that band:

    Strong -> no critical, at most 1 high
    Mixed  -> at most 1 critical
    Weak   -> no cap

If the checker call fails or returns something unusable, the draft is returned unchanged.
"""

from __future__ import annotations

import json
import logging
from typing import Callable, Literal

from pydantic import BaseModel, Field, ValidationError

from app.services.critics import CriticPassResult, Flaw

log = logging.getLogger("veridex.checker")

Strength = Literal["Strong", "Mixed", "Weak"]
_SEV_ORDER = ["critical", "high", "medium", "low"]


class _Decision(BaseModel):
    index: int = Field(..., ge=0)
    action: Literal["keep", "drop"]
    severity: Literal["critical", "high", "medium", "low"] | None = None
    reason: str = ""


class CheckerVerdict(BaseModel):
    strength: Strength
    summary: str = Field(..., min_length=1)
    decisions: list[_Decision]


_CHECKER_PROMPT = """You are the CHECKER for a draft critique produced by the "{lens}" lens of Veridex, a tool that critiques strategy documents.
The lens's scope: {focus}

Your job is quality control, not new criticism. You will see the document and the draft flaws (numbered from 0).
Do NOT invent new flaws. For each draft flaw decide keep or drop, and the right severity.

STEP 1 — RATE THE EVIDENCE STRENGTH of the document, using these definitions literally:
  - Strong: an established business with real revenue, customers or profitability that are directly relevant to the plan's central claim (e.g. an operating company extending what it already does, or selling to its own existing customers). Being unproven about the extension itself does NOT make it Mixed.
  - Mixed: some real measured traction (a pilot, early revenue, one site, one channel), but the central claim extrapolates well beyond it.
  - Weak: pre-launch or pre-revenue, OR the central claim rests on a single study/backtest/experiment whose method is questionable, OR on assumptions only.

STEP 2 — FOR EACH FLAW, DROP it if any of these is true:
  a) It questions a number or fact the document states plainly and that is consistent with the document's other numbers. (Check the arithmetic yourself before calling anything inconsistent.)
  b) It calls something a "contradiction", "inconsistent" or "impossible" when the figures can in fact both be true (e.g. a figure that is merely not derived, or a subset compared to a total). Real contradictions — figures that cannot both be true — must be KEPT.
  c) It criticises a test, pilot or experiment design that the document already describes as staged, small by intention, or exploratory, without identifying a concrete error in it.
  d) It is outside the lens's scope (see above).
  e) It duplicates another kept flaw (keep the better one).
Otherwise KEEP it.

STEP 3 — SET SEVERITY for each kept flaw:
  - critical: the plan's central claim is likely wrong because of this flaw by itself.
  - high: a load-bearing number or claim is unsupported or genuinely inconsistent.
  - medium/low: secondary gaps.
  Leave severity unchanged unless it is clearly over- or under-stated.

Respond with ONLY this JSON object:
{{
  "strength": "Strong" | "Mixed" | "Weak",
  "summary": "<2-4 sentences. Start with 'Evidence base: <Strong|Mixed|Weak>.' then 'Weakest number: <the claim> — because <reason>. Prove it by: <one concrete check>.' stated plainly, then what is proven>",
  "decisions": [
    {{"index": 0, "action": "keep" | "drop", "severity": "critical" | "high" | "medium" | "low", "reason": "<under 15 words>"}}
  ]
}}
Include exactly one decision for every draft flaw index.

---- STRATEGY DOCUMENT ----
{document}
---- END DOCUMENT ----

---- DRAFT FLAWS ----
{flaws}
---- END DRAFT FLAWS ----"""


def build_checker_prompt(lens: str, focus: str, document: str, draft: CriticPassResult) -> str:
    flaws = "\n\n".join(
        f"[{i}] ({f.severity}) {f.title}\n{f.description}\nQuestion: {f.question}"
        for i, f in enumerate(draft.flaws)
    )
    return _CHECKER_PROMPT.format(lens=lens, focus=focus, document=document.strip(), flaws=flaws)


def parse_verdict(raw: str) -> CheckerVerdict:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`").split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return CheckerVerdict(**json.loads(text))


def _cap(flaws: list[Flaw], strength: Strength) -> list[Flaw]:
    """Enforce severity caps per strength band; flaws must already be sorted most severe first."""
    max_critical, max_high = {"Strong": (0, 1), "Mixed": (1, 99), "Weak": (99, 99)}[strength]
    out, n_crit, n_high = [], 0, 0
    for f in flaws:
        sev = f.severity
        if sev == "critical" and n_crit >= max_critical:
            sev = "high"
        if sev == "high" and n_high >= max_high:
            sev = "medium"
        n_crit += sev == "critical"
        n_high += sev == "high"
        out.append(f.model_copy(update={"severity": sev}))
    return out


def apply_verdict(draft: CriticPassResult, verdict: CheckerVerdict) -> CriticPassResult:
    by_index = {d.index: d for d in verdict.decisions if d.index < len(draft.flaws)}
    kept: list[Flaw] = []
    for i, flaw in enumerate(draft.flaws):
        d = by_index.get(i)
        if d is None:  # no decision: keep as drafted
            kept.append(flaw)
        elif d.action == "keep":
            kept.append(flaw.model_copy(update={"severity": d.severity or flaw.severity}))
    if not kept:  # never return an empty critique; keep the draft's top flaw, mildly
        kept = [draft.flaws[0].model_copy(update={"severity": "low"})]
    kept.sort(key=lambda f: _SEV_ORDER.index(f.severity))
    kept = _cap(kept, verdict.strength)
    kept.sort(key=lambda f: _SEV_ORDER.index(f.severity))
    return draft.model_copy(update={"summary": verdict.summary, "flaws": kept})


def check_pass(
    lens: str,
    focus: str,
    document: str,
    draft: CriticPassResult,
    call: Callable[[str], str],
) -> CriticPassResult:
    """Run the checker; on any failure return the draft unchanged."""
    try:
        verdict = parse_verdict(call(build_checker_prompt(lens, focus, document, draft)))
    except (ValidationError, ValueError, KeyError, TypeError) as e:
        log.warning("checker output unusable for %s: %s", lens, e)
        return draft
    except Exception as e:  # noqa: BLE001 — provider errors must not fail the lens
        log.warning("checker call failed for %s: %s", lens, e)
        return draft
    return apply_verdict(draft, verdict)
