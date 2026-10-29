"""Round 2 tests: prompt wording and stage-mode severity cap. No network.

Run from backend/:  OPENAI_API_KEY=x python -m pytest -q tests/test_round2.py
"""

import json
import os

os.environ.setdefault("OPENAI_API_KEY", "x")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.api.v1 import routes_critique  # noqa: E402
from app.main import app  # noqa: E402
from app.services import builder, critics  # noqa: E402
from app.services.critics import CriticPassResult, Flaw, cap_missing_criticals  # noqa: E402

IDEA = "An app that matches retired engineers with small manufacturers needing short consulting jobs."


def test_plain_prompts_have_no_basis_or_stage_text():
    for lens in builder.LENS_ORDER:
        p = critics._build_prompt(lens, "doc")
        assert '"basis"' not in p and "basis" not in p.lower().replace("on the basis", "")
        assert ("FACTUALITY" in p) == (lens == "pre_mortem")


def test_stage_prompt_has_basis_contract():
    for stage in ("idea", "established"):
        assert '"basis" field' in critics._build_prompt("unit_economics", "doc", stage=stage)


def test_pre_mortem_wording():
    p = critics._build_prompt("pre_mortem", "doc")
    assert "the most likely reasons it would fail" in p
    assert "Assumptions most likely to prove wrong" in p
    assert p.index("FACTUALITY") < p.index("Focus ONLY on assumption failures")


def test_evidence_audit_labels_assumptions():
    p = critics._build_prompt("evidence_audit", "doc")
    assert "even at $5k" not in p and "not from the document" in p
    assert "at most HIGH" in p


def test_currency_rule_in_stage_prompts():
    for stage in ("idea", "building", "traction", "established"):
        p = critics._build_prompt("pre_mortem", "doc", stage=stage)
        assert "Never attach a currency or unit the founder did not write" in p
    assert "Never attach a currency" not in critics._build_prompt("pre_mortem", "doc")


def _flaw(title, sev, basis):
    return Flaw(title=title, severity=sev, description="d", question="q", basis=basis)


def test_cap_missing_criticals():
    res = CriticPassResult(lens="pre_mortem", summary="s", flaws=[
        _flaw("a", "critical", "missing"),
        _flaw("b", "critical", "contradiction"),
        _flaw("c", "critical", "stated_fact"),
        _flaw("d", "critical", None),
        _flaw("e", "high", "missing"),
        _flaw("f", "medium", "missing"),
    ])
    out = cap_missing_criticals(res)
    sev = {f.title: f.severity for f in out.flaws}
    assert sev == {"a": "high", "b": "critical", "c": "critical", "d": "critical", "e": "high", "f": "medium"}
    assert [f.title for f in out.flaws] == ["b", "c", "d", "a", "e", "f"]  # re-sorted, stable
    assert res.flaws[0].severity == "critical"  # input untouched


@pytest.fixture
def stub(monkeypatch):
    routes_critique._ip_buckets.clear()

    def fake(model_id, prompt):
        if prompt.startswith("You are the CHECKER"):
            n = prompt.count("\nQuestion: ")
            return json.dumps({"strength": "Weak", "summary": "Evidence base: Weak. x",
                               "decisions": [{"index": i, "action": "keep"} for i in range(n)]})
        lens = prompt.split('"lens": "')[1].split('"')[0]
        flaws = [
            {"title": "t0", "severity": "high", "description": "d", "question": "q"},
            {"title": "t1", "severity": "critical", "description": "d", "question": "q"},
        ]
        if '"basis" field' in prompt:
            flaws[0]["basis"] = "stated_fact"
            flaws[1]["basis"] = "missing"
            flaws[0]["gap"] = flaws[1]["gap"] = "buyer"
        return json.dumps({"lens": lens, "summary": "s", "flaws": flaws})

    monkeypatch.setattr(critics, "_call_openai", fake)


def _completed(text):
    out = []
    for block in text.strip().split("\n\n"):
        f = dict(line.split(": ", 1) for line in block.split("\n"))
        if f["event"] == "pass_completed":
            out.append(json.loads(f["data"])["result"])
    return out


def test_idea_mode_caps_missing_critical_end_to_end(stub):
    r = TestClient(app).post("/api/v1/critique/stream", json={"strategy_doc": IDEA, "stage": "idea"})
    results = _completed(r.text)
    assert len(results) == 5
    for res in results:  # includes evidence_audit (checked lens)
        assert [f["severity"] for f in res["flaws"]] == ["high", "high"]
        assert {f["title"] for f in res["flaws"]} == {"t0", "t1"}


def test_plain_mode_keeps_critical(stub):
    r = TestClient(app).post("/api/v1/critique/stream", json={"strategy_doc": IDEA})
    for res in _completed(r.text):
        assert any(f["severity"] == "critical" for f in res["flaws"])
        assert all("basis" not in f for f in res["flaws"])
