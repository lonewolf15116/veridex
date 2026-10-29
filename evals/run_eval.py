#!/usr/bin/env python3
"""Run a Veridex lens over a folder of strategy docs and save the results.

Uses only the standard library. Needs the server's eval token, so runs skip the free
limit and can call a single lens (about a fifth of the cost of a full critique).

    export VERIDEX_EVAL_TOKEN=...            # same value as EVAL_TOKEN on Render
    python3 evals/run_eval.py evals/holdout --lens evidence_audit --label v3.1

Writes evals/results/<label>-<lens>-<timestamp>.json and prints one line per doc:
severity shape (C/H/M/L), number of flaws, and whether backtest jargon appeared.
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

DEFAULT_API = "https://veridex-backend-n0nf.onrender.com"
LENSES = ["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]
JARGON = re.compile(r"leak|look-?ahead|walk-forward|out-of-sample|train/test|parameter sweep|multiple.testing", re.I)


def run_doc(api: str, token: str, lenses: list[str], path: Path, timeout: int, stage: str | None = None) -> dict:
    payload = {"strategy_doc": path.read_text(), "lenses": lenses}
    if stage:
        payload["stage"] = stage
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{api}/api/v1/critique/stream",
        data=body,
        headers={"Content-Type": "application/json", "X-Eval-Token": token},
        method="POST",
    )
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode()
    except urllib.error.HTTPError as e:
        return {"doc": path.name, "error": f"HTTP {e.code}: {e.read().decode()[:300]}"}
    except Exception as e:  # noqa: BLE001
        return {"doc": path.name, "error": f"{type(e).__name__}: {e}"}

    results, errors, done = {}, {}, {}
    for block in text.strip().split("\n\n"):
        fields = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
        event, data = fields.get("event"), json.loads(fields.get("data", "{}"))
        if event == "pass_completed":
            results[data["lens"]] = data["result"]
        elif event == "error":
            errors[data["lens"]] = data["reason"]
        elif event == "done":
            done = data
    return {"doc": path.name, "seconds": round(time.time() - started, 1), "results": results, "errors": errors, "done": done}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="folder of .md docs (ANSWER_KEY.md, README.md and RESULTS.md are skipped)")
    ap.add_argument("--lens", action="append", choices=LENSES, help="lens to run (repeatable; default evidence_audit)")
    ap.add_argument("--label", default="run", help="version label for the output file, e.g. v3.1")
    ap.add_argument("--api", default=os.getenv("VERIDEX_API", DEFAULT_API))
    ap.add_argument("--stage", choices=["idea", "building", "traction", "established"], help="idea builder mode")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    token = os.getenv("VERIDEX_EVAL_TOKEN")
    if not token:
        print("Set VERIDEX_EVAL_TOKEN to the EVAL_TOKEN configured on the server.", file=sys.stderr)
        return 2
    # Idea mode needs every lens to pick questions; plain evals default to Evidence Audit.
    lenses = args.lens or (LENSES if args.stage else ["evidence_audit"])
    docs = sorted(p for p in Path(args.folder).glob("*.md") if p.name not in {"ANSWER_KEY.md", "README.md", "RESULTS.md"})
    if not docs:
        print(f"No .md docs in {args.folder}", file=sys.stderr)
        return 2

    # Wake a sleeping free-tier backend before firing the batch.
    try:
        urllib.request.urlopen(f"{args.api}/health", timeout=90).read()
    except Exception as e:  # noqa: BLE001
        print(f"Backend not reachable: {e}", file=sys.stderr)
        return 1

    with ThreadPoolExecutor(args.workers) as ex:
        runs = list(ex.map(lambda p: run_doc(args.api, token, lenses, p, args.timeout, args.stage), docs))

    out_dir = Path(__file__).resolve().parent / "results"
    out_dir.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"{args.label}-{'+'.join(lenses)}-{stamp}.json"
    out.write_text(json.dumps({"label": args.label, "lenses": lenses, "stage": args.stage, "api": args.api, "runs": runs}, indent=2))

    for r in runs:
        if "error" in r:
            print(f"{r['doc']:<34} ERROR {r['error']}")
            continue
        for lens in lenses:
            res = r["results"].get(lens)
            if res is None:
                print(f"{r['doc']:<34} {lens:<14} FAILED {r['errors'].get(lens, '')[:80]}")
                continue
            shape = "".join(f["severity"][0].upper() for f in res["flaws"])
            jargon = "jargon" if JARGON.search(json.dumps(res)) else ""
            gaps = ""
            if args.stage:
                tags = [f.get("gap") for f in res["flaws"]]
                gaps = f"gaps {sum(t is not None for t in tags)}/{len(tags)}"
            print(f"{r['doc']:<34} {lens:<14} {shape:<8} {len(res['flaws'])} flaws {r['seconds']:>5}s {jargon} {gaps}")
        if args.stage and r.get("done"):
            qs = [q["gap"] for q in r["done"].get("questions", [])]
            print(f"{'':<34} questions: {', '.join(qs) or 'none'}   refine token: {'yes' if r['done'].get('refine_token') else 'no'}")
    print(f"\nSaved {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
