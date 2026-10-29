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
