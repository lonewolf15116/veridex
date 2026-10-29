# Suite run 1 — 2026-10-30 (suite-20261030-042958)

Live backend at main `c7a5fc7` (no prompt changes since Revision 2 shipped). Idea route, one critique plus one
refinement per case. Each case answered one question and skipped the rest. Scoring: Opus read the full JSON.
Regex flags were checked by hand.

## Mechanics (Revision 2 plumbing)

| Check | Result |
| --- | --- |
| Gap tags valid | 275/275 |
| Questions per critique | 4 in every case, each with its "why we're asking" sources |
| Refinement re-ran exactly the informed lenses | 10/10 |
| Token reuse refused (409) | 10/10 |
| Answered gap labelled "resolved" | 0/10 |

## Rubric

| Dimension | Result | Notes |
| --- | --- | --- |
| Factuality | 9/10 | T04 Pre-Mortem writes invented history: "In the market outcome, the major systems … had no public APIs", "clinics and some insurers refused to share…". |
| Evidence provenance | **Fail (new bug)** | In 8/10 refined critiques, skipped questions are read as founder admissions. T01: "$299 … but the founder skipped 'Who pays' … an internal inconsistency". T04: "elsewhere admits 'who pays' is unknown", rated **critical** "internal contradiction". T05: "founder admits they haven't determined who pays" (never said). Cause: `compose_brief` adds "## Still unknown (the founder skipped these)". |
| Numeric fidelity | Mostly | T09: "$800/yr" in Adversarial Competitor and Execution Risk (first critique). Evidence Audit and Unit Economics kept "800 (units)" and asked for the currency. T01 again assumes a $5k/month rep cost ("bounding"). T03 introduces labelled example prices. |
| Severity | **Fail** | 27 criticals in idea/building cases. About 7 are defensible: T06 arithmetic ×4, T10 15 enterprise deals with no sales staff ×3. About 20 are "not shown yet" (data access, compliance plan, demand evidence, price unvalidated). The idea-stage "never critical for merely unstated" rule is not holding. |
| Question relevance | Pass | key_numbers selected in 8/10 cases. |
| Gap traceability | Pass | |
| Refinement correctness | Pass (10/10) | |
| Refinement honesty | Partial | No "resolved" claims, but see the skipped-question bug. |

## Controls

- **T06 (real contradiction):** pass. 4 lenses rate the £40 cost vs £5 price as critical, with correct arithmetic. The Pre-Mortem critical (unvalidated 20 videos/month) is the only weak one.
- **T07 (traction):** mostly pass. Evidence Audit: "Evidence base: Mixed … real early traction (24 paying studios, £2,136 MRR)". It never says "verified". However there are 4 criticals for missing things (moat, COGS, channel). The refined Execution Risk adds a speculative "Regulatory blockade: GDPR / PCI / VAT not addressed" critical.

## Other observations

- T01 refinement: correctly treats 30% as "an unverified target", and n=3 conversations as "far too small". The Pre-Mortem calls the claim "likely false", which is stronger than the evidence.
- T08: "either meaningless or impossible", "implausible". It edges into declaring the model impossible.
- T09: 20/day → CAC 24 is computed but framed as conditional and flagged as suspicious. Acceptable.

## Proposed fixes (not applied)

1. **Bug (code, deterministic):** drop or reword the "Still unknown" section of the refinement brief, so that a skipped question carries no information.
2. **Severity (enforcement):** in stage mode, code-cap criticals that rest only on missing information, as the checker caps Evidence Audit. Prompt wording alone has failed.
3. **Pre-Mortem factuality:** label each failure as a scenario. Never assert events, pilots or conversations the input does not contain.

## Applied after run 1
- Fix 1 (skipped-question bug): `compose_brief` no longer lists skipped questions. Verify with
  `run_suite.py --only T01,T04,T05`: no refined finding should cite a skip or a founder "admission" the answer did not make.
