#!/usr/bin/env python3
"""Expanded 10-case idea-route suite runner (stdlib only).

    export VERIDEX_EVAL_TOKEN=...
    python3 evals/run_suite.py evals/suite [--only T01,T06] [--workers 3]

Per test: first critique (with eval token) -> answer exactly ONE selected question, skip the rest ->
refinement (no eval token, free path) -> reuse the same refinement body (expect HTTP 409).
Mechanical checks are printed; regex hits are flags for human review, not verdicts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = os.getenv("VERIDEX_API", "https://veridex-backend-n0nf.onrender.com")
LENS_ORDER = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]
GAPS = {"buyer", "demand_evidence", "pricing", "acquisition", "key_numbers", "assumptions", "alternatives", "differentiation"}
INFORMS = {
    "buyer": ["pre_mortem", "unit_economics", "evidence_audit"], "demand_evidence": ["pre_mortem", "evidence_audit"],
    "pricing": ["unit_economics", "evidence_audit"], "acquisition": ["unit_economics", "execution_risk"],
    "key_numbers": ["unit_economics", "evidence_audit"], "assumptions": ["pre_mortem", "evidence_audit"],
    "alternatives": ["adversarial_competitor", "pre_mortem"], "differentiation": ["adversarial_competitor"],
}
SEV = {"critical": "C", "high": "H", "medium": "M", "low": "L"}
PILOT_RE = re.compile(r"\b(pilots? (showed|found|revealed|produced)|in (the )?pilot|clinics told|customers told|trial(s)? (showed|found))\b", re.I)
MONEY_RE = re.compile(r"[£$]\s?\d[\d,]*(?:\.\d+)?")


# ---------- parsing / selection ----------

def parse_case(path: Path) -> dict:
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise ValueError(f"{path.name}: missing header")
    head, text = m.group(1), m.group(2).strip()
    case: dict = {"fallback_answers": {}}
    in_fb = False
    for line in head.splitlines():
        if not line.strip():
            continue
        if in_fb and line.startswith((" ", "\t")):
            k, v = line.strip().split(":", 1)
            case["fallback_answers"][k.strip()] = v.strip()
            continue
        in_fb = False
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if k == "fallback_answers":
            in_fb = True
        else:
            case[k] = v
    case["text"] = text
    case["id"] = path.stem.split("-")[0]
    case["name"] = path.stem
    return case


def pick_answer(case: dict, questions: list[dict]) -> tuple[dict | None, list[dict]]:
    """Return (answer or None, full answers list). Answers ONE question; skips every other."""
    gaps = [q["gap"] for q in questions]
    chosen = None
    if case.get("answer_gap") in gaps and case["answer_gap"] != "key_numbers":
        chosen = (case["answer_gap"], case["answer"])
    else:
        for g in gaps:
            if g != "key_numbers" and g in case["fallback_answers"]:
                chosen = (g, case["fallback_answers"][g])
                break
    answers = []
    for g in gaps:
        if chosen and g == chosen[0]:
            answers.append({"gap": g, "text": chosen[1]})
        else:
            answers.append({"gap": g, "skipped": True})
    return (({"gap": chosen[0], "text": chosen[1]} if chosen else None), answers)


# ---------- HTTP ----------

def post(body: dict, eval_token: str | None) -> tuple[int, list | str]:
    headers = {"Content-Type": "application/json"}
    if eval_token:
        headers["X-Eval-Token"] = eval_token
    req = urllib.request.Request(f"{API}/api/v1/critique/stream", data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            text = r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]
    events = []
    for block in text.strip().split("\n\n"):
        f = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
        events.append((f.get("event"), json.loads(f.get("data", "{}"))))
    return 200, events


def collect(events: list) -> tuple[dict, list, dict]:
    lenses, errors, done = {}, [], {}
    for e, d in events:
        if e == "pass_completed":
            lenses[d["lens"]] = d["result"]
        elif e == "error":
            errors.append(d)
        elif e == "done":
            done = d
    return lenses, errors, done


# ---------- checks ----------

def shape(lenses: dict) -> dict:
    return {l: "".join(SEV.get(f["severity"], "?") for f in r["flaws"]) for l, r in lenses.items()}


def all_text(*lens_dicts: dict) -> str:
    parts = []
    for ld in lens_dicts:
        for r in ld.values():
            parts.append(r.get("summary", ""))
            for f in r["flaws"]:
                parts += [f["title"], f["description"], f["question"]]
    return "\n".join(parts)


def watch(case: dict, first: dict, refined: dict) -> list[str]:
    text = all_text(first, refined)
    flags = []
    input_money = set(MONEY_RE.findall(case["text"]))
    if case["id"] == "T09":
        for pat in (r"£\s?800", r"\$\s?800", r"£\s?20\b", r"\$\s?20\b"):
            for m in re.finditer(pat, text):
                flags.append(f"T09 currency attached: {m.group(0)!r}")
    else:
        for m in sorted(set(MONEY_RE.findall(text)) - input_money):
            flags.append(f"money not in input: {m!r}")
    for m in PILOT_RE.finditer(text):
        flags.append(f"pilot/trial phrase: {m.group(0)!r}")
    return flags


# ---------- markdown ----------

def md_critique(lenses: dict) -> str:
    out = []
    for l in LENS_ORDER:
        if l not in lenses:
            continue
        r = lenses[l]
        out.append(f"### {l}\n\n{r['summary']}\n")
        for f in r["flaws"]:
            out.append(f"- **{f['title']}** [{f['severity'].upper()}] ({f.get('gap')})\n  {f['description']}\n  -> {f['question']}\n")
    return "\n".join(out)


def to_markdown(rec: dict, case: dict) -> str:
    L = [f"# {rec['name']}", "", f"**Stage:** {rec['stage']}", "", "## Input", "", case["text"], "",
         f"**Reviewer expectation:** {case.get('expect', '')}", ""]
    if rec.get("errors"):
        L += ["## Errors", ""] + [f"- {e}" for e in rec["errors"]] + [""]
    L += ["## First critique", "", md_critique(rec.get("first", {})), ""]
    if rec.get("lens_errors"):
        L += ["Lens errors: " + json.dumps(rec["lens_errors"]), ""]
    if rec.get("questions"):
        L += ["## Selected questions", ""]
        for q in rec["questions"]:
            L.append(f"- **{q['gap']}**: {q['text']}")
            for p in q.get("prompted_by", []):
                L.append(f"  - why we're asking: {p.get('lens')} / {p.get('title')} [{p.get('severity')}]")
        L.append("")
    if rec.get("answered"):
        L += ["## Answer given", "", f"**{rec['answered']['gap']}**: {rec['answered']['text']}", "",
              "Skipped: " + (", ".join(rec["skipped_gaps"]) or "none"), ""]
    if rec.get("refined"):
        L += ["## Refined critique", "", md_critique(rec["refined"]), ""]
        meta = rec.get("refinement_meta", {})
        ran = meta.get("lenses", [])
        L += ["## Refinement meta", "", f"- Lenses re-run: {', '.join(ran)}",
              f"- Lenses not re-run: {', '.join(l for l in LENS_ORDER if l not in ran)}",
              f"- Gaps filled: {meta.get('gaps_filled')}", f"- Gaps skipped: {meta.get('gaps_skipped')}", ""]
    if "reuse_refused_409" in rec:
        L += ["## Reuse check", "", f"Re-sending the same refinement token refused with 409: {'yes' if rec['reuse_refused_409'] else 'NO'}", ""]
    return "\n".join(L)


# ---------- per-test run ----------

def run_case(case: dict, token: str) -> dict:
    rec: dict = {"id": case["id"], "name": case["name"], "stage": case["stage"], "errors": [], "timings": {}}
    doc, stage = case["text"], case["stage"]
    try:
        t = time.time()
        status, ev = post({"strategy_doc": doc, "stage": stage}, token)
        rec["timings"]["first_s"] = round(time.time() - t, 1)
        if status != 200:
            rec["errors"].append(f"first critique HTTP {status}: {ev}")
            return rec
        first, lens_errors, done = collect(ev)
        rec.update(first=first, lens_errors=lens_errors, first_shape=shape(first))
        qs = done.get("questions", [])
        rec["questions"] = qs
        flaws = [f for r in first.values() for f in r["flaws"]]
        rec["gap_tags_valid"] = f"{sum(f.get('gap') in GAPS for f in flaws)}/{len(flaws)}"
        rec["criticals"] = sum(f["severity"] == "critical" for f in flaws)
        answered, answers = pick_answer(case, qs)
        rec["answered"] = answered
        rec["skipped_gaps"] = [a["gap"] for a in answers if a.get("skipped")]
        token_r = done.get("refine_token")
        if not qs or not token_r or not answered:
            rec["errors"].append("no refinement: no questions, no refine token, or nothing answerable")
            return rec
        body = {"strategy_doc": doc, "stage": stage, "refine": {"token": token_r, "answers": answers}}
        t = time.time()
        status, ev = post(body, None)  # free path: no eval token
        rec["timings"]["refine_s"] = round(time.time() - t, 1)
        if status != 200:
            rec["errors"].append(f"refinement HTTP {status}: {ev}")
            return rec
        refined, rerrs, rdone = collect(ev)
        meta = rdone.get("refinement", {})
        expected = [l for l in LENS_ORDER if l in INFORMS[answered["gap"]]]
        rec.update(refined=refined, refine_lens_errors=rerrs, refinement_meta=meta, refined_shape=shape(refined),
                   expected_lenses=expected, refine_ran=list(refined),
                   refine_lenses_ok=sorted(refined) == sorted(expected) and meta.get("lenses") == expected)
        status2, _ = post(body, None)
        rec["reuse_refused_409"] = status2 == 409
        rec["reuse_status"] = status2
        rec["watch"] = watch(case, first, refined)
    except Exception as e:  # keep the run going
        rec["errors"].append(f"{type(e).__name__}: {e}")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    token = os.getenv("VERIDEX_EVAL_TOKEN")
    if not token:
        print("Set VERIDEX_EVAL_TOKEN first.", file=sys.stderr)
        return 2
    cases = [parse_case(p) for p in sorted(Path(a.folder).glob("T*.md"))]
    if a.only:
        want = {s.strip().upper() for s in a.only.split(",")}
        cases = [c for c in cases if c["id"] in want]
    urllib.request.urlopen(f"{API}/health", timeout=90).read()  # wake the backend
    with ThreadPoolExecutor(a.workers) as ex:
        recs = list(ex.map(lambda c: run_case(c, token), cases))

    stamp = time.strftime("%Y%m%d-%H%M%S")
    res = Path(__file__).resolve().parent / "results"
    md_dir = res / f"suite-{stamp}"
    md_dir.mkdir(parents=True, exist_ok=True)
    (res / f"suite-{stamp}.json").write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    for rec, case in zip(recs, cases):
        (md_dir / f"{rec['name']}.md").write_text(to_markdown(rec, case))

    for r in recs:
        print(f"\n== {r['name']} ({r['stage']})")
        print(f"   first shape: {r.get('first_shape')}  criticals: {r.get('criticals')}  gap tags valid: {r.get('gap_tags_valid')}")
        print(f"   questions: {[q['gap'] for q in r.get('questions', [])]}  answered: {(r.get('answered') or {}).get('gap')}")
        if "refine_lenses_ok" in r:
            print(f"   refined shape: {r.get('refined_shape')}")
            print(f"   refined lenses {r['refine_ran']} vs expected {r['expected_lenses']}: {'OK' if r['refine_lenses_ok'] else 'MISMATCH'}")
            print(f"   reuse 409: {'yes' if r['reuse_refused_409'] else 'NO (status %s)' % r['reuse_status']}")
            print("   flags for human review: " + ("; ".join(r["watch"]) if r["watch"] else "none"))
        for e in r["errors"] + [f"lens error: {x}" for x in r.get("lens_errors", [])]:
            print(f"   ERROR: {e}")
    print(f"\nSaved {res / f'suite-{stamp}.json'}\nMarkdown exports in {md_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
