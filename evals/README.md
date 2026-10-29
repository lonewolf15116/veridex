# Evals

- `evidence_audit/` — first test set (5 business plans + Cascade Spider). Used for tuning v2–v3.1, so no longer blind.
- `holdout/` — 10 blind plans (H01–H10) and `ANSWER_KEY.md`, written without access to the lens prompts. Use for scoring, not tuning.
- `run_eval.py` — runs one or more lenses over a folder and saves JSON to `results/`.

## Running a round

1. On Render, set `EVAL_TOKEN` to a long random string (once).
2. On your machine:

```
export VERIDEX_EVAL_TOKEN=<same string>
python3 evals/run_eval.py evals/holdout --lens evidence_audit --label v3.1
```

Eval requests skip the free limit and can run a single lens, so a 10-plan round of one lens costs about two full critiques.
