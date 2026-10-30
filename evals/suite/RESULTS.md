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
- Verified (suite-20261030-044354, T01/T04/T05 after deploy of 7d907ea): 0 refined findings cite a skipped
  question (was 8/10). Remaining "founder admits" lines quote what the founder actually answered. T04's
  "internal contradiction" critical is gone. Routing 3/3, reuse 409 3/3. Still open: T05 Pre-Mortem
  "trials showed low conversion" (invented history, fix 3); T01 $5k rep-cost assumption.

# Round 2 — 2026-10-30 (main 35dd855; suite-20261030-052942 + holdout r2-20261030-053209)

Changes: Pre-Mortem writes failures as scenarios and may not assert unreported events; Evidence Audit's $5k example
is labelled as an assumption; stage mode labels introduced figures and never adds a currency; stage-mode flaws carry
a `basis` (contradiction / stated_fact / missing) and code caps critical+missing at high.

| Required outcome | Result |
| --- | --- |
| Pre-Mortem fabrication | **Pass.** 0 asserted events in 93 suite Pre-Mortem flaws and 10 holdout plans (was confirmed in 3 earlier runs). 92/93 use scenario/conditional wording. (The runner's past-tense regex matched "revealed preference"; all false positives.) |
| Model-supplied figures labelled | **Pass.** T01 no longer introduces $5k/$60k/$1,200; "assum…" appears 26 times in T01. |
| Conditional scenarios still allowed | **Pass.** T10 $360,000 (15 × $24,000), T06 £40 vs £5. |
| T09 currency | **Pass.** 0 currency symbols attached to 800 or 20. |
| Severity | **Improved, partial.** First-critique criticals 31 → 16. In T01–T05 and T09: 13 → 2. Controls hold: T06 5 criticals (all contradiction/stated_fact), T10 4 (target vs resources). T07 4 → 1, and it still credits "real early traction". Caveat: the cap relies on the model's own `basis` label. T08 "95% accuracy contradicts conceptual status" and T09 "graduates won't buy 800/year" (stated_fact) are speculation labelled to stay critical. |
| Rev 2 mechanics | 275→285 gap tags valid; routing 9/10; reuse 409 10/10. **T07 refinement returned HTTP 200 with an empty body in 0.2 s, yet the token was consumed** (reuse got 409). Not reproduced yet. |
| Paste-a-plan route (holdout EA) | Main flag 10/10, planted math 6/6, false-alarm plans 5/10 firm (7 with borderlines), severity over 4/10, strength 5/10, jargon 1/8 (H02: "look-ahead" on a simulation). Same as shipped round 1 within noise, except the one jargon hit. |

Open after round 2 (backlog): basis mislabelling can bypass the cap; T07 empty refinement + token consumed;
H02 jargon; Evidence Audit false alarms (unchanged, long-standing).

# Round 3 (tone) — 2026-10-30 (main eac3b20; suite-20261030-060024, T05/T06/T07)
Every lens summary opens with a plain verdict (Most likely killer / Where the math breaks / How I would kill this /
What breaks first / Weakest number) plus a concrete test; hedging filler banned. Facts and severity rules unchanged.
- Verdicts present in 15/15 lens summaries, specific and grounded in the input (e.g. T05 competitor: "ship a free
  'Beginner Mode' toggle…"; T06: "20 × £2 = £40 … you lose £35 per subscriber per month").
- Banned phrases 0; invented-event verbs 0. T06 keeps 5 criticals (contradiction/stated_fact); critical+missing 0.
- T07 refinement ran normally (2/2 lenses); the round-2 empty-response anomaly did not recur.
- Minor over-correction: a few lines drop the founder's own currency ("price 5 vs cost 2", "12 per month").
- Some verdicts still name a missing figure as the "killer" (T07 Unit Economics: no CAC data) rather than a mechanism.
