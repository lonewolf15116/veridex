"""Idea builder (Revision 2) tests. No network: model calls are stubbed.

Run from backend/:  OPENAI_API_KEY=x python -m pytest -q tests/test_builder.py
"""

import json
import os

os.environ.setdefault("OPENAI_API_KEY", "x")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.api.v1 import routes_critique  # noqa: E402
from app.main import app  # noqa: E402
from app.services import builder, critics  # noqa: E402
from app.services.critics import GAPS, CriticPassResult, Flaw  # noqa: E402

IDEA = "An app that matches retired engineers with small manufacturers needing short consulting jobs."

# gap tags each stubbed lens returns in idea mode (two flaws per lens)
STUB_GAPS = {
    "pre_mortem": [("critical", "demand_evidence"), ("medium", "assumptions")],
    "unit_economics": [("high", "pricing"), ("medium", "key_numbers")],
    "adversarial_competitor": [("high", "alternatives"), ("low", "differentiation")],
    "execution_risk": [("medium", "acquisition"), ("low", None)],
    "evidence_audit": [("high", "demand_evidence"), ("medium", "key_numbers")],
}


def _stub(calls):
    def fake(model_id, prompt):
        calls.append(prompt)
        if prompt.startswith("You are the CHECKER"):  # evidence_audit checker: keep everything
            n = prompt.count("\nQuestion: ")
            return json.dumps({"strength": "Weak", "summary": "Evidence base: Weak. x",
                               "decisions": [{"index": i, "action": "keep"} for i in range(n)]})
        lens = prompt.split('"lens": "')[1].split('"')[0]
        idea_mode = '"gap" field' in prompt
        flaws = []
        for i, (sev, gap) in enumerate(STUB_GAPS[lens]):
            f = {"title": f"{lens}-{i}", "severity": sev, "description": "d", "question": "q"}
            if idea_mode:
                f["gap"] = gap
            flaws.append(f)
        return json.dumps({"lens": lens, "summary": "s", "flaws": flaws})
    return fake


@pytest.fixture
def calls(monkeypatch):
    out = []
    monkeypatch.setattr(critics, "_call_openai", _stub(out))
    routes_critique._ip_buckets.clear()
    return out


def _events(text):
    evs = []
    for block in text.strip().split("\n\n"):
        f = dict(line.split(": ", 1) for line in block.split("\n"))
        evs.append((f["event"], json.loads(f["data"])))
    return evs


def _done(r):
    return [d for e, d in _events(r.text) if e == "done"][0]


def _lens_prompts(calls):
    return [p for p in calls if not p.startswith("You are the CHECKER")]


# ── Compatibility: paste-a-plan unchanged ─────────────────────────────────────

def test_plain_prompt_has_no_idea_mode_text():
    for lens in builder.LENS_ORDER:
        p = critics._build_prompt(lens, "doc")
        assert '"gap"' not in p and "IDEA-STAGE" not in p and "STAGE NOTE" not in p


def test_plain_critique_unchanged(calls):
    r = TestClient(app).post("/api/v1/critique/stream", json={"strategy_doc": IDEA})
    evs = _events(r.text)
    assert r.status_code == 200
    assert evs[-1] == ("done", {})  # no questions, no token
    flaws = [f for e, d in evs if e == "pass_completed" for f in d["result"]["flaws"]]
    assert flaws and all("gap" not in f for f in flaws)
    assert sum(1 for e, _ in evs if e == "pass_completed") == 5


# ── Idea mode ─────────────────────────────────────────────────────────────────

def test_stage_prompts():
    early = critics._build_prompt("pre_mortem", "doc", stage="idea")
    late = critics._build_prompt("pre_mortem", "doc", stage="established")
    assert "IDEA-STAGE MODE" in early and '"gap" field' in early and "Do NOT invent specifics" in early
    assert "STAGE NOTE" in late and '"gap" field' in late
    with pytest.raises(ValueError):
        critics._build_prompt("pre_mortem", "doc", stage="seed")


def test_invalid_gap_tag_rejected():
    with pytest.raises(Exception):
        Flaw(title="t", severity="low", description="d", question="q", gap="vibes")


def test_idea_critique_returns_questions_and_token(calls):
    r = TestClient(app).post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea"})
    done = _done(r)
    assert done["refine_token"]
    gaps = [q["gap"] for q in done["questions"]]
    # demand_evidence: critical(4)+high(3)=7 · key_numbers: 2+2=4 · pricing 3 · alternatives 3 (pricing first by GAPS order)
    assert gaps == ["demand_evidence", "key_numbers", "pricing", "alternatives"]
    q0 = done["questions"][0]
    assert {p["lens"] for p in q0["prompted_by"]} == {"pre_mortem", "evidence_audit"}
    assert all(q["gap"] in GAPS for q in done["questions"])
    # the brief carries the declared stage
    assert all("Stage: Idea (declared by the founder)" in p for p in _lens_prompts(calls))


def test_question_selection_deterministic_and_order_independent():
    def res(lens, pairs):
        return CriticPassResult(lens=lens, summary="s", flaws=[
            Flaw(title=f"{lens}{i}", severity=s, description="d", question="q", gap=g) for i, (s, g) in enumerate(pairs)])
    results = {l: res(l, STUB_GAPS[l]) for l in builder.LENS_ORDER}
    a = builder.select_questions(results)
    b = builder.select_questions(dict(reversed(list(results.items()))))
    assert [q.model_dump() for q in a] == [q.model_dump() for q in b]
    assert len(builder.select_questions(results, max_questions=2)) == 2
    assert builder.select_questions({}) == []


def test_every_gap_maps_to_exactly_one_question():
    assert set(builder.QUESTION_BANK) == set(GAPS)
    for gap, q in builder.QUESTION_BANK.items():
        assert q.gap == gap and q.informs and set(q.informs) <= set(builder.LENS_ORDER)


# ── Brief and provenance ──────────────────────────────────────────────────────

def test_brief_contains_only_founder_text():
    answers = [
        builder.Answer(gap="demand_evidence", text="Spoke to 12 | factory owners; 3 asked for a pilot."),
        builder.Answer(gap="key_numbers", numbers=[builder.NumberRow(label="Hourly rate", value="$90", evidence="measured"),
                                                    builder.NumberRow(label="Jobs per month", value="", evidence="unknown")]),
        builder.Answer(gap="pricing", skipped=True),
    ]
    brief = builder.compose_brief(IDEA, "idea", answers)
    assert brief.startswith("Stage: Idea (declared by the founder)")
    assert IDEA in brief and "Spoke to 12 / factory owners" in brief  # pipes neutralised
    assert "| Hourly rate | $90 | Measured (founder-reported, not verified) |" in brief
    assert "| Jobs per month | not given | Don't know |" in brief
    assert "## Still unknown" in brief and builder.QUESTION_BANK["pricing"].text in brief
    assert "pre_mortem" not in brief and "prompted" not in brief  # no critique text


def test_lenses_for_answers():
    a = [builder.Answer(gap="alternatives", text="Upwork"), builder.Answer(gap="pricing", skipped=True)]
    assert builder.lenses_for_answers(a) == ["pre_mortem", "adversarial_competitor"]
    assert builder.lenses_for_answers([builder.Answer(gap="pricing", text="   ")]) == []


# ── Refinement: selective, free once, never charged ───────────────────────────

def _first(c, calls):
    done = _done(c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea"}))
    calls.clear()
    return done


def test_refinement_runs_only_informed_lenses(calls):
    c = TestClient(app)
    done = _first(c, calls)
    r = c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea", "refine": {
        "token": done["refine_token"],
        "answers": [{"gap": "alternatives", "text": "Upwork and word of mouth"}, {"gap": "pricing", "skipped": True}]}})
    evs = _events(r.text)
    ran = [d["lens"] for e, d in evs if e == "pass_completed"]
    assert sorted(ran) == ["adversarial_competitor", "pre_mortem"]
    assert evs[-1] == ("done", {"refinement": {"lenses": ["pre_mortem", "adversarial_competitor"],
                                               "gaps_filled": ["alternatives"], "gaps_skipped": ["pricing"]}})
    assert "refine_token" not in evs[-1][1] and "questions" not in evs[-1][1]  # one refinement per critique
    assert all("Upwork and word of mouth" in p for p in _lens_prompts(calls))


def test_refinement_is_single_use_and_refused_not_charged(calls):
    c = TestClient(app)
    tok = _first(c, calls)["refine_token"]
    body = {"strategy_doc": IDEA, "stage": "idea", "refine": {"token": tok, "answers": [{"gap": "buyer", "text": "Plant managers"}]}}
    assert c.post("/api/v1/critique/stream", json=body).status_code == 200
    again = c.post("/api/v1/critique/stream", json=body)
    assert again.status_code == 409 and again.json()["detail"]["code_status"] == "refine_unavailable"
    forged = dict(body, refine={"token": tok[:-2] + "xx", "answers": body["refine"]["answers"]})
    assert c.post("/api/v1/critique/stream", json=forged).status_code == 409
    # the free allowance was touched only by the one first critique
    assert len(next(iter(routes_critique._ip_buckets.values()))) == 1


def test_refinement_does_not_consume_daily_allowance(calls):
    c = TestClient(app)
    tokens = [_first(c, calls)["refine_token"] for _ in range(routes_critique.RATE_LIMIT)]  # use the whole allowance
    assert c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA}).status_code == 429
    for tok in tokens:  # every refinement still runs
        r = c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea",
                                                   "refine": {"token": tok, "answers": [{"gap": "buyer", "text": "Plant managers"}]}})
        assert r.status_code == 200


def test_expired_token_refused():
    tok = builder.issue_refine_token("idea", now=1_000)
    assert builder.redeem_refine_token(tok, now=1_000 + builder.REFINE_TTL_SECS + 1) is False
    assert builder.redeem_refine_token(builder.issue_refine_token("idea")) is True


def test_request_validation(calls):
    c = TestClient(app)
    assert c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "answers": [{"gap": "buyer", "text": "x"}]}).status_code == 422
    assert c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea",
                                                   "refine": {"token": "x" * 20, "answers": [{"gap": "nonsense", "text": "x"}]}}).status_code == 422
    r = c.post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea",
                                                "refine": {"token": "x" * 20, "answers": [{"gap": "buyer", "skipped": True}]}})
    assert r.status_code == 422  # nothing answered, nothing to re-run


def test_full_form_answers_up_front_runs_all_five(calls):
    r = TestClient(app).post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "building",
                                                               "answers": [{"gap": "buyer", "text": "Plant managers"}]})
    assert sum(1 for e, _ in _events(r.text) if e == "pass_completed") == 5
    assert all("Plant managers" in p for p in _lens_prompts(calls))
