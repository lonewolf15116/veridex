"""Checker pass tests. No network: the model call is a stub.

Run from backend/:  OPENAI_API_KEY=x python -m pytest -q tests/test_checker.py
"""

import json
import os

os.environ.setdefault("OPENAI_API_KEY", "x")

from app.services import checker, critics  # noqa: E402
from app.services.critics import CriticPassResult, Flaw  # noqa: E402


def _draft(*sevs):
    return CriticPassResult(
        lens="evidence_audit",
        summary="draft summary",
        flaws=[Flaw(title=f"f{i}", severity=s, description="d", question="q") for i, s in enumerate(sevs)],
    )


def _verdict(strength, decisions):
    return json.dumps({"strength": strength, "summary": f"Evidence base: {strength}. x", "decisions": decisions})


def _run(draft, raw):
    return checker.check_pass("evidence_audit", "focus", "doc", draft, lambda prompt: raw)


def test_strong_band_caps_at_medium():
    d = _draft("critical", "high", "high", "low")
    out = _run(d, _verdict("Strong", [{"index": i, "action": "keep"} for i in range(4)]))
    assert [f.severity for f in out.flaws] == ["medium", "medium", "medium", "low"]
    assert out.summary.startswith("Evidence base: Strong")


def test_mixed_band_caps_at_high_weak_uncapped():
    d = _draft("critical", "critical", "medium")
    keep = [{"index": i, "action": "keep"} for i in range(3)]
    assert [f.severity for f in _run(d, _verdict("Mixed", keep)).flaws] == ["high", "high", "medium"]
    assert [f.severity for f in _run(d, _verdict("Weak", keep)).flaws] == ["critical", "critical", "medium"]


def test_drop_and_regrade_and_resort():
    d = _draft("critical", "high", "medium")
    out = _run(d, _verdict("Weak", [
        {"index": 0, "action": "drop"},
        {"index": 1, "action": "keep", "severity": "medium"},
        {"index": 2, "action": "keep", "severity": "critical"},
    ]))
    assert [(f.title, f.severity) for f in out.flaws] == [("f2", "critical"), ("f1", "medium")]


def test_cannot_add_flaws_and_ignores_bad_indices():
    d = _draft("high", "medium")
    out = _run(d, _verdict("Weak", [
        {"index": 0, "action": "keep"}, {"index": 1, "action": "keep"}, {"index": 7, "action": "keep"},
    ]))
    assert [f.title for f in out.flaws] == ["f0", "f1"]


def test_missing_decision_keeps_flaw():
    out = _run(_draft("high", "medium"), _verdict("Weak", [{"index": 0, "action": "drop"}]))
    assert [f.title for f in out.flaws] == ["f1"]


def test_never_empty():
    out = _run(_draft("high", "medium"), _verdict("Strong", [{"index": 0, "action": "drop"}, {"index": 1, "action": "drop"}]))
    assert [(f.title, f.severity) for f in out.flaws] == [("f0", "low")]


def test_falls_back_to_draft_on_bad_output_or_error():
    d = _draft("critical", "high")
    assert _run(d, "not json") == d
    assert _run(d, json.dumps({"strength": "Huge", "summary": "s", "decisions": []})) == d

    def boom(prompt):
        raise RuntimeError("provider down")
    assert checker.check_pass("evidence_audit", "f", "doc", d, boom) == d


def test_code_fenced_json_accepted():
    raw = "```json\n" + _verdict("Weak", [{"index": 0, "action": "keep"}]) + "\n```"
    assert _run(_draft("high"), raw).summary.startswith("Evidence base: Weak")


def test_only_checked_lenses_get_checked(monkeypatch):
    calls = []

    def fake(model_id, prompt):
        calls.append(prompt)
        if prompt.startswith("You are the CHECKER"):
            return _verdict("Strong", [{"index": 0, "action": "keep"}])
        lens = prompt.split('"lens": "')[1].split('"')[0]
        return json.dumps({"lens": lens, "summary": "s",
                           "flaws": [{"title": "t", "severity": "critical", "description": "d", "question": "q"}]})

    monkeypatch.setattr(critics, "_call_openai", fake)
    ea = critics.run_critic_pass("evidence_audit", "a plan with numbers")
    assert ea.flaws[0].severity == "medium" and len(calls) == 2  # draft + checker; Strong caps at medium
    calls.clear()
    pm = critics.run_critic_pass("pre_mortem", "a plan with numbers")
    assert pm.flaws[0].severity == "critical" and len(calls) == 1  # no checker
