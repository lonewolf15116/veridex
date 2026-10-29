# Expanded idea-route suite (10 cases)

Ten founder inputs supplied by an external reviewer (T01-T10). Each case runs through the idea route
once: one critique, then one refinement in which exactly one question is answered with a short,
honest, non-evidential canned answer and every other selected question is skipped. No prompt or
code changes happen between cases. The input text in each file is verbatim from the reviewer.

## File format

A small header, then the founder text:

```
---
stage: building            # idea | building | traction
answer_gap: demand_evidence
answer: <canned founder answer for that gap>
fallback_answers:
  pricing: <used if answer_gap was not selected>
  buyer: ...
expect: <what the reviewer expects>
---
<founder text>
```

`key_numbers` is a numbers-type question and is never answered; if selected it is skipped.

## Rubric (8 dimensions, judged by a human reviewer)

1. Factuality: no invented facts about the business, market or competitors.
2. Evidence provenance: founder claims are labelled as claims; nothing is called verified without a source.
3. Numeric fidelity: numbers, currencies and units are used exactly as given; none are added or converted.
4. Severity: missing evidence is not automatically critical; critical is for defensible blockers.
5. Question relevance: 2-4 questions, each relevant to the input.
6. Gap traceability: each flaw's gap tag is valid and each question traces to the flaws that prompted it.
7. Refinement correctness: only the lenses informed by the answered gap are re-run.
8. Refinement honesty: answered gaps are not labelled "resolved"; the new critique is the only verdict.

## Controls

- T06 (video economics): the input contains a real arithmetic problem (20 videos x GBP 2 = GBP 40 cost vs GBP 5 revenue). At least one defensible critical is expected, clearly distinguished from merely missing evidence.
- T07 (fitness SaaS, traction): reported revenue and customers should be credited as founder-reported, with requests for cohort, acquisition and retention detail; never called independently verified.

## Running

```
export VERIDEX_EVAL_TOKEN=...
python3 evals/run_suite.py evals/suite [--only T01,T06] [--workers 3]
```

Writes `evals/results/suite-<stamp>.json` (everything) and one markdown export per test in
`evals/results/suite-<stamp>/`, ready to forward to the reviewer. The mechanical checks printed
(severity shape, gap tags, refined lenses, 409 on reuse, regex "flags for human review") are not verdicts.
