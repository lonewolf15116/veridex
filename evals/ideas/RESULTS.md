# Idea builder (Revision 2) — live checks

## Gap-tag check, 29 Oct 2026 (backend `2b5fd72`, all five lenses, stage = idea)

- **Gap tags:** 83/83 flaws tagged with a valid gap (I1 27/27, I2 25/25, I3 30/30 + checker). Pre-frontend gate: pass.
- **No invented specifics:** zero money or percentage figures in any flaw; the ideas contain none.
- **Question ranking (fixed after this check, `builder.select_questions`):** summing severity let the catch-all
  `assumptions` (22/83 flaws) top every idea and hid single-lens criticals. Now: specific gaps first, then worst
  severity, then total, then fixed order. Replayed on the same results:

| Idea | Before | After |
|---|---|---|
| I1 consumer app | assumptions, acquisition, key_numbers, demand_evidence | acquisition, key_numbers, differentiation, demand_evidence |
| I2 B2B tool | assumptions, acquisition, demand_evidence, key_numbers | pricing, acquisition, demand_evidence, key_numbers |
| I3 marketplace | assumptions, demand_evidence, pricing, key_numbers | demand_evidence, pricing, differentiation, key_numbers |

- **Idea-stage criticals:** 12 criticals across 15 lens runs, most of them "X is not stated" (no price, no numbers,
  no acquisition plan). Added one idea-mode rule: a flaw that is only "not stated yet" is at most high; genuine
  blockers (e.g. legal access to receipts, on-site liability) stay critical. To be confirmed in the functional test.
