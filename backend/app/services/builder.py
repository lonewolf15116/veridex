"""
Idea builder, Revision 2 — critique first.

Flow
  1. The founder sends a short idea + a declared stage. All five lenses run in idea-stage mode and
     tag each flaw with a gap from critics.GAPS.
  2. select_questions() maps gap tags to questions from a fixed bank. Pure function: same critique
     in, same questions out. No model call.
  3. The founder answers (or skips). compose_brief() builds the document for the re-run from a fixed
     template: the founder's idea, their answers (numbers tagged as founder-reported), and what is
     still unknown. Critique text is never copied into it, so it can't be mistaken for evidence.
  4. lenses_for_answers() picks only the lenses the answered gaps inform. That re-run is the one
     free refinement, authorised by a single-use token issued with the first critique.

Answering a gap does NOT mean a flaw is resolved. The new critique is the only verdict; "gaps
filled" is just a record of what the founder supplied.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import threading
import time
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.services.critics import GAPS, CriticPassResult

LENS_ORDER = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]

# ── Question bank ─────────────────────────────────────────────────────────────
# One question per gap. `informs` = the lenses whose critique depends on that answer; it decides
# which lenses a refinement re-runs. `kind` = "numbers" for the label/value/evidence-tag rows.

class BankQuestion(BaseModel):
    gap: str
    text: str
    kind: Literal["text", "numbers"] = "text"
    informs: list[str]


QUESTION_BANK: dict[str, BankQuestion] = {
    "buyer": BankQuestion(gap="buyer", text="Who has this problem? Be specific.",
                          informs=["pre_mortem", "unit_economics", "evidence_audit"]),
    "demand_evidence": BankQuestion(gap="demand_evidence",
                                    text="How do you know people want this? (people you've talked to, data, your own experience)",
                                    informs=["pre_mortem", "evidence_audit"]),
    "pricing": BankQuestion(gap="pricing", text="Who pays, and roughly how much?",
                            informs=["unit_economics", "evidence_audit"]),
    "acquisition": BankQuestion(gap="acquisition", text="How will your first customers find you?",
                                informs=["unit_economics", "execution_risk"]),
    "key_numbers": BankQuestion(gap="key_numbers",
                                text="Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.",
                                kind="numbers", informs=["unit_economics", "evidence_audit"]),
    "assumptions": BankQuestion(gap="assumptions", text="What has to be true for this to work?",
                                informs=["pre_mortem", "evidence_audit"]),
    "alternatives": BankQuestion(gap="alternatives", text="What do people use instead today?",
                                 informs=["adversarial_competitor", "pre_mortem"]),
    "differentiation": BankQuestion(gap="differentiation",
                                    text="Why would customers choose this over the alternatives?",
                                    informs=["adversarial_competitor"]),
}
assert set(QUESTION_BANK) == set(GAPS), "every gap needs exactly one bank question"

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}
MAX_QUESTIONS = 4


# ── Question selection (deterministic) ────────────────────────────────────────

class PromptedBy(BaseModel):
    lens: str
    title: str
    severity: str


class SelectedQuestion(BaseModel):
    gap: str
    text: str
    kind: str
    informs: list[str]
    prompted_by: list[PromptedBy]


def select_questions(results: dict[str, CriticPassResult], max_questions: int = MAX_QUESTIONS) -> list[SelectedQuestion]:
    """Rank gaps by the total severity of the flaws that point at them; return up to max_questions.

    Deterministic: ties break by severity of the worst flaw, then by the fixed GAPS order. Flaws
    with no gap tag are ignored. Lenses are read in LENS_ORDER so the result never depends on the
    order results arrived in.
    """
    score: dict[str, int] = {}
    worst: dict[str, int] = {}
    sources: dict[str, list[PromptedBy]] = {}
    for lens in LENS_ORDER:
        res = results.get(lens)
        if res is None:
            continue
        for flaw in res.flaws:
            if flaw.gap is None:
                continue
            w = SEVERITY_WEIGHT[flaw.severity]
            score[flaw.gap] = score.get(flaw.gap, 0) + w
            worst[flaw.gap] = max(worst.get(flaw.gap, 0), w)
            sources.setdefault(flaw.gap, []).append(PromptedBy(lens=lens, title=flaw.title, severity=flaw.severity))

    ranked = sorted(score, key=lambda g: (-score[g], -worst[g], GAPS.index(g)))
    out = []
    for gap in ranked[:max_questions]:
        q = QUESTION_BANK[gap]
        out.append(SelectedQuestion(gap=gap, text=q.text, kind=q.kind, informs=list(q.informs),
                                    prompted_by=sources[gap]))
    return out


# ── Founder answers and the brief ─────────────────────────────────────────────

STAGE_LABEL = {"idea": "Idea", "building": "Building (pre-launch)",
               "traction": "Early traction", "established": "Established business"}
EVIDENCE_LABEL = {"measured": "Measured (founder-reported, not verified)", "estimate": "Estimate", "unknown": "Don't know"}


class NumberRow(BaseModel):
    label: str = Field(..., min_length=1, max_length=80)
    value: str = Field("", max_length=80)
    evidence: Literal["measured", "estimate", "unknown"]


class Answer(BaseModel):
    gap: str
    skipped: bool = False
    text: str = Field("", max_length=1500)
    numbers: list[NumberRow] = Field(default_factory=list, max_length=12)

    @field_validator("gap")
    @classmethod
    def _known_gap(cls, v: str) -> str:
        if v not in QUESTION_BANK:
            raise ValueError(f"unknown gap: {v}")
        return v


def _clean(s: str) -> str:
    # Founder text goes into a markdown brief: keep it on its own lines and strip table pipes.
    return " ".join(s.replace("|", "/").split())


def compose_brief(idea: str, stage: str, answers: list[Answer]) -> str:
    """Build the re-run document from a fixed template. Only founder-supplied text goes in."""
    lines = [f"Stage: {STAGE_LABEL[stage]} (declared by the founder)", "", "## The idea (founder's words)", idea.strip()]
    answered = [a for a in answers if not a.skipped and (a.text.strip() or a.numbers)]
    unknown = [a for a in answers if a not in answered]

    if answered:
        lines += ["", "## Founder's answers to follow-up questions"]
        for a in answered:
            q = QUESTION_BANK[a.gap]
            lines += ["", f"### {q.text}"]
            if a.text.strip():
                lines.append(_clean(a.text))
            if a.numbers:
                lines += ["", "| Number | Value | Evidence |", "| --- | --- | --- |"]
                for n in a.numbers:
                    lines.append(f"| {_clean(n.label)} | {_clean(n.value) or 'not given'} | {EVIDENCE_LABEL[n.evidence]} |")

    if unknown:
        lines += ["", "## Still unknown (the founder skipped these)"]
        lines += [f"- {QUESTION_BANK[a.gap].text}" for a in unknown]
    return "\n".join(lines)


def lenses_for_answers(answers: list[Answer]) -> list[str]:
    """Lenses informed by the answered (not skipped) gaps, in fixed order. Empty if nothing answered."""
    informed = set()
    for a in answers:
        if not a.skipped and (a.text.strip() or a.numbers):
            informed.update(QUESTION_BANK[a.gap].informs)
    return [lens for lens in LENS_ORDER if lens in informed]


# ── One free refinement per critique ──────────────────────────────────────────
# A signed, single-use token issued with each idea-mode critique. The signing key must survive
# restarts (Render's free plan sleeps after ~15 idle minutes, mid-questionnaire), so it is
# REFINE_SECRET if set, else derived from the server's OpenAI key, else random per process.
# Used token ids are remembered in memory until they expire; a restart forgets them, which at worst
# allows one extra free refinement of the same critique.

REFINE_TTL_SECS = 24 * 3600


def _signing_key() -> bytes:
    explicit = os.getenv("REFINE_SECRET", "")
    if explicit:
        return explicit.encode()
    base = os.getenv("OPENAI_API_KEY", "")
    if base:
        return hmac.new(base.encode(), b"veridex-refine-token-v1", hashlib.sha256).digest()
    return secrets.token_bytes(32)


_secret = _signing_key()
_used: dict[str, float] = {}
_used_lock = threading.Lock()


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def issue_refine_token(stage: str, now: Optional[float] = None) -> str:
    body = json.dumps({"id": secrets.token_hex(8), "stage": stage, "exp": int((now or time.time()) + REFINE_TTL_SECS)},
                      separators=(",", ":")).encode()
    sig = hmac.new(_secret, body, hashlib.sha256).digest()
    return f"{_b64(body)}.{_b64(sig)}"


def redeem_refine_token(token: Optional[str], now: Optional[float] = None) -> bool:
    """True exactly once per valid, unexpired token. Anything else returns False."""
    if not token or token.count(".") != 1:
        return False
    try:
        body_b64, sig_b64 = token.split(".")
        body = _unb64(body_b64)
        if not hmac.compare_digest(hmac.new(_secret, body, hashlib.sha256).digest(), _unb64(sig_b64)):
            return False
        claims = json.loads(body)
    except Exception:  # noqa: BLE001 — malformed token
        return False
    now = now or time.time()
    if claims.get("exp", 0) < now:
        return False
    with _used_lock:
        for k in [k for k, exp in _used.items() if exp < now]:
            del _used[k]
        if claims["id"] in _used:
            return False
        _used[claims["id"]] = claims["exp"]
    return True
