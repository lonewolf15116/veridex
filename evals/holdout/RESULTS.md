# Holdout results — Evidence Audit

Scored against `ANSWER_KEY.md`. One run per plan (gpt-5-mini), so treat single cells as noisy.

## v3.1 baseline (29 Oct 2026) — `results/v3.1-baseline-evidence_audit-20261029-184712.json`

| Plan | Strength key→lens | Max severity key→lens | Main core flag | Math catch | False alarm | Jargon |
|---|---|---|---|---|---|---|
| H01 solar pods | Weak→Mixed | critical→critical | Yes (3/3) | Yes ($720k; 32 mo) | No | No |
| H02 bus routing | Weak→Mixed | critical→critical | Yes (3/3) | Yes (≈87) | No | No |
| H03 prefab ADU | Weak→Mixed | critical→high | Yes (2/3) | n/a (clean) | No | No |
| H04 physio | Mixed→**Strong** | high→**critical** | Yes (3/3) | Yes ($120 vs $85) | **Yes** — top critical is a false contradiction ($900 lifetime GP) | No |
| H05 irrigation | Mixed→Mixed | high→**critical** | Yes (3/3) | Yes (105%; 7.2 mo) | Yes ($2,500 margin) | No |
| H06 nurse prep | Mixed→Mixed | medium→**critical** | Partial | n/a (clean) | Yes (calls staged $20k test underpowered) | No |
| H07 roofing | Strong→**Mixed** | medium→**high** | Yes (2/2) | n/a (clean) | Borderline (renewal-rate selection bias) | No |
| H08 vet clinic | Strong→**Mixed** | medium→**high** | Yes (2/2) | Yes (growth-rate gap) | Yes (cash runway) | No |
| H09 backtest | Weak→Mixed | critical→critical | Yes (2/3) | Yes (≈15.9% CAGR needed) | Yes ("look-ahead"; 10 bp costs) | n/a |
| H10 A/B test | Weak→Mixed | critical→critical | Yes (2/3) | n/a (clean) | Yes (randomisation balance) | n/a |

**Totals:** main core flag 9/10 (+1 partial) · planted math errors computed 6/6 · backtest jargon on non-backtest plans 0/8 ·
false alarms on 7/10 plans · severity over-rated on 5/10 · strength label matched on 2/10 (8 pulled to "Mixed", H04 called "Strong").

**Patterns:** strength labels collapse to Mixed and don't drive severity; severity is inflated on milder plans (H04–H08);
numbers the key marks as fine get flagged; secondary statistical concerns (H10 interval width, H09 benchmark and
single 2008–09 episode) are missed.

## Checker pass (v4) — two rounds, then stop

Stop rule set before testing: ship if main flag ≥9, math ≥5/6, false alarms ≤3, severity over ≤2, strength ≥6, Cascade leak still flagged; otherwise one adjustment, one more round, ship the better round.

| | v3.1 baseline | v4 round 1 (`1bf1d09`) | v4.1 round 2 (`ca0f0c0`) |
|---|---|---|---|
| Main core flag | 9/10 | 8/10 | 8/10 (+1 partial) |
| Planted math computed | 6/6 | 6/6 | 5/6 (+1 partial) |
| False-alarm plans | 7/10 | 6/10 | 7/10 |
| Severity over key ceiling | 5/10 | 4/10 | 3/10 |
| Strength label matches key | 2/10 | 6/10 | 6/10 |
| Backtest jargon (8 plans) | 0 | 0 | 1 |

Round 2 tightened ceilings (Strong ≤ medium, Mixed ≤ high) and the Strong definition; it then labelled both genuinely Strong plans Mixed and capped the Cascade Spider leak at high (still flagged, rank 2).

**Decision: ship round 1.** Neither round met every target. The checker's clear win is strength labelling (2 → 6). False alarms are not fixed by a keep/drop checker — they originate in the draft and most survive review — so they stay an open issue for later, ideally guided by real user ratings rather than more prompt tuning on this set. Single runs; differences of ±1 are within noise.
