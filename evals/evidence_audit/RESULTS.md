# Evidence Audit — eval log

Scored against `ANSWER_KEY.md`. Runs are single samples from `gpt-5-mini` on the live backend, so treat
individual cells as noisy. Note that v2–v3.1 were tuned on these same six documents, so this is no longer a
blind test: a fresh hold-out set is needed to measure generalisation.

Shape = severities of the lens's flaws in order (C critical, H high, M medium, L low).

## v1 (scored by hand from the live site)

| # | Core flag | Math catch | Backtest jargon on a non-backtest doc | Lane |
|---|---|---|---|---|
| 01 Dental | yes (critical) | no | yes ("leakage is plausible", "best-of-many") | ok |
| 02 Coffee | yes | half | yes ("multiple testing", rated high) | drift (margins) |
| 03 Handyman | yes | half | mild ("walk-forward") | ok |
| 04 EU payroll | yes | no | yes ("out-of-sample", survivorship) | drift (team size) |
| 05 Ghost kitchen | not run | | | |

Calibration on 04: fail (same 1C/2H/3M shape as weak plans).

## v2 — classify claims, do the arithmetic, gate backtest checks

| # | Shape | Core flag | Math catch | Jargon | Lane |
|---|---|---|---|---|---|
| 01 | CHHHMM | yes | **$60k ÷ 50 = $1,200 vs $800** | none | ok |
| 02 | CHHHMM | yes (churn critical) | **10,000 / 1.15^11 ≈ 2,150** | none | drift (box margin) |
| 03 | CHHHM | yes | **200 × 3 = 600 jobs/week** | none | ok |
| 04 | CHHML | half (compliance timeline missed) | **$1M / 40 = $25k** | none | drift (sales capacity) |
| 05 | CHHMML | **n=1 (critical)** | 20 × $40K × 20% = $160K/mo | none | drift (budget, pipeline) |

Calibration on 04: fail. Rated Weak, flagged "profitable" as undocumented, called an ambiguity
($4M / 40 = $100k, dividing total ARR by a subset) a critical "contradiction".

## v3 — Strong/Mixed/Weak bands with severity caps, out-of-scope list, build timelines as forecasts

| # | Shape | Change vs v2 |
|---|---|---|
| 01 | CHHMML | **regressed: CAC arithmetic gone** (out-of-scope list suppressed it) |
| 02 | CHHMM | 2,150 is now the top critical; margin drift gone |
| 04 | CHHMM | facts credited, **compliance timeline now flagged high**; still Mixed with a critical; subset division repeated |
| 05 | CHHMM | rated Mixed (correct); still raises burn/CAC/team capacity |
| 06 Cascade | CHHMM | look-ahead still critical |

## v3.1 — restore CAC arithmetic, same-population rule for division, firmer Strong definition

| # | Shape | Core flag | Math catch | Jargon | Calibration / lane |
|---|---|---|---|---|---|
| 01 | CHHHMM | yes | **$1,200 vs $800 restored** | none | ok |
| 03 | CHHMM | yes | **600 jobs/week** | none | ok |
| 04 | **HHHMM** | yes, incl. **6-month compliance (high)** | **$25k** | none | **no critical, no subset division**; still labelled Mixed with 3 highs; one drift flag (cost of the 3-person team) |
| 05 | HHHMM | n=1 ranked first but **high, not critical** | $160K/mo | none | drift (pipeline, budget) |
| 06 Cascade | CHHHM | **regressed:** critical went to a genuine arithmetic inconsistency (−15% then +60% compounds to +36%, not the reported +16.3%); the timestamp look-ahead dropped to high | — | (expected) | — |

02 was not re-run on v3.1 (hourly rate limit).
