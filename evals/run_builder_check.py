#!/usr/bin/env python3
"""Functional check for the idea builder (Revision 2) against a live backend.

For each idea in a folder: run an idea-stage critique, answer the first two selected questions
with canned founder answers (skip the third), refine, then try to refine again with the same token.

Checks printed per idea:
  - every flaw has a valid gap tag
  - critical flaws listed (should be genuine blockers, not "X not stated")
  - questions selected
  - the refinement ran exactly the lenses the answered gaps inform
  - the refinement reports gaps filled/skipped and nothing about flaws being resolved
  - re-using the token is refused with 409 (never charged)

    export VERIDEX_EVAL_TOKEN=...   (the first critique uses it to skip the free limit;
                                     the refinement deliberately does NOT, to test the free path)
    python3 evals/run_builder_check.py evals/ideas
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = os.getenv("VERIDEX_API", "https://veridex-backend-n0nf.onrender.com")
ORDER = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]
GAPS = {"buyer", "demand_evidence", "pricing", "acquisition", "key_numbers", "assumptions", "alternatives", "differentiation"}
INFORMS = {
    "buyer": ["pre_mortem", "unit_economics", "evidence_audit"], "demand_evidence": ["pre_mortem", "evidence_audit"],
    "pricing": ["unit_economics", "evidence_audit"], "acquisition": ["unit_economics", "execution_risk"],
    "key_numbers": ["unit_economics", "evidence_audit"], "assumptions": ["pre_mortem", "evidence_audit"],
    "alternatives": ["adversarial_competitor", "pre_mortem"], "differentiation": ["adversarial_competitor"],
}
# Canned founder answers (test data standing in for a real founder).
ANSWERS = {
    "buyer": "Small-business owners and their staff who currently do this by hand.",
    "demand_evidence": "I interviewed 8 potential customers; 5 said they would try it; nobody has paid yet.",
    "pricing": "The business pays a monthly subscription, roughly 30 per month.",
    "acquisition": "Direct outreach through two industry associations I belong to.",
    "assumptions": "Customers will trust it enough to use it without checking every result.",
    "alternatives": "Doing it by hand, spreadsheets, or general-purpose freelancer sites.",
    "differentiation": "It is built for this one job, so setup takes minutes rather than days.",
}
NUMBERS = [{"label": "People interviewed", "value": "8", "evidence": "measured"},
           {"label": "Monthly price", "value": "30", "evidence": "estimate"}]


def post(body: dict, eval_token: str | None) -> tuple[int, list | str]:
    headers = {"Content-Type": "application/json"}
    if eval_token:
        headers["X-Eval-Token"] = eval_token
    req = urllib.request.Request(f"{API}/api/v1/critique/stream", data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            text = r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    events = []
    for block in text.strip().split("\n\n"):
        f = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
        events.append((f.get("event"), json.loads(f.get("data", "{}"))))
    return 200, events


def check(path: Path, eval_token: str) -> dict:
    idea = path.read_text().strip()
    out: dict = {"doc": path.name}
    status, ev = post({"strategy_doc": idea, "stage": "idea"}, eval_token)
    if status != 200:
        return {**out, "error": f"first critique HTTP {status}: {ev}"}
    flaws = [(d["lens"], f) for e, d in ev if e == "pass_completed" for f in d["result"]["flaws"]]
    done = next(d for e, d in ev if e == "done")
    out["gap_tags"] = f"{sum(f.get('gap') in GAPS for _, f in flaws)}/{len(flaws)} valid"
    out["criticals"] = [f"{l}: {f['title']}" for l, f in flaws if f["severity"] == "critical"]
    qs = done.get("questions", [])
    out["questions"] = [q["gap"] for q in qs]
    if not qs or not done.get("refine_token"):
        return {**out, "error": "no questions or no refine token"}

    answers = []
    for i, q in enumerate(qs[:3]):
        if i == 2:
            answers.append({"gap": q["gap"], "skipped": True})
        elif q["kind"] == "numbers":
            answers.append({"gap": q["gap"], "numbers": NUMBERS})
        else:
            answers.append({"gap": q["gap"], "text": ANSWERS[q["gap"]]})
    expected = [l for l in ORDER if any(l in INFORMS[a["gap"]] for a in answers if not a.get("skipped"))]

    body = {"strategy_doc": idea, "stage": "idea", "refine": {"token": done["refine_token"], "answers": answers}}
    status, ev = post(body, None)  # free path: no eval token
    if status != 200:
        return {**out, "error": f"refinement HTTP {status}: {ev}"}
    ran = [d["lens"] for e, d in ev if e == "pass_completed"]
    rdone = next(d for e, d in ev if e == "done")
    ref = rdone.get("refinement", {})
    out["refine_lenses_ok"] = sorted(ran) == sorted(expected) and ref.get("lenses") == expected
    out["refine_ran"] = ran
    out["gaps_filled"], out["gaps_skipped"] = ref.get("gaps_filled"), ref.get("gaps_skipped")
    out["no_resolved_claims"] = not any(k in json.dumps(rdone).lower() for k in ("resolved", "fixed", "addressed"))
    out["no_new_token"] = "refine_token" not in rdone
    status, _ = post(body, None)
    out["reuse_refused_409"] = status == 409
    return out


def main() -> int:
    token = os.getenv("VERIDEX_EVAL_TOKEN")
    if not token:
        print("Set VERIDEX_EVAL_TOKEN first.", file=sys.stderr)
        return 2
    docs = sorted(p for p in Path(sys.argv[1] if len(sys.argv) > 1 else "evals/ideas").glob("*.md") if p.name != "RESULTS.md")
    urllib.request.urlopen(f"{API}/health", timeout=90).read()  # wake the backend
    with ThreadPoolExecutor(3) as ex:
        results = list(ex.map(lambda p: check(p, token), docs))
    out = Path(__file__).resolve().parent / "results" / f"builder-check-{time.strftime('%Y%m%d-%H%M%S')}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2))
    for r in results:
        print(f"\n== {r['doc']}")
        for k, v in r.items():
            if k != "doc":
                print(f"   {k}: {v}")
    print(f"\nSaved {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
