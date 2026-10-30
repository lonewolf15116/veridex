# Holdout r2 (2026-10-30) - results/r2-evidence_audit+pre_mortem-20261030-053209.json

| Plan | Strength key->lens | Max severity key->lens | Main core flag | Math catch | False alarm | Jargon |
|---|---|---|---|---|---|---|
| H01 solar pods | Weak->Weak | critical->critical | Yes (3/3) | Yes ($720k; 32 mo) | No | No |
| H02 bus routing | Weak->Weak | critical->critical | Yes (2/3) | Yes (≈87; 28.3%) | Yes - "Possible look-ahead ... (b) exact timestamp for each input field ... no future/after-the-fact information was used" (key: no leakage concerns) | Yes - "Backtest details and possible look-ahead or omitted constraints"; "stratified holdout set" (misapplied to a simulation) |
| H03 prefab ADU | Weak->Weak | critical->critical | Yes (3/3) | n/a (clean) | Yes - "Capacity math inconsistent with 14-week build time" (3.72 units/slot, ~33 slots) invents a contradiction; "$4.5M start-up capital status and sufficiency unclear" rated high (key: budget, not derived) | No |
| H04 physio | Mixed->Strong | high->high | Yes (3/3) | Yes ($120 vs $85) | Borderline - "Active base vs new signups vs retention ... churn must be large" (key: 81% retention not contradicted) | No |
| H05 irrigation | Mixed->Mixed | high->critical | Yes (3/3) | Yes (105%; 7.2 mo) | No | No |
| H06 nurse prep | Mixed->Strong | medium->high | Yes (3/3) | n/a (clean) | Yes - "$20k at $60 CAC yields too few survey responses ... may not produce a precise enough estimate" (calls staged test underpowered) | No |
| H07 roofing | Strong->Mixed | medium->critical | Yes (2/2) | n/a (clean) | Borderline - 91% renewal "generalized without evidence" / "Ambiguous 12-month review trigger" | No |
| H08 vet clinic | Strong->Strong | medium->high | Yes (2/2) | Yes (7.15% vs 6.5%) | Yes - "Post-build cash cushion not shown: $1.5M - $1.1M = $400k remaining" (key must-not) | No |
| H09 backtest | Weak->Mixed | critical->critical | Yes (2/3; benchmark bias and out-of-sample/single episode missed) | Yes ($1.42M; 15.86%) | Yes - "Possible look-ahead or timing error" (high); "Unspecified turnover and trading-cost methodology behind the 10 bps" (high) | n/a |
| H10 A/B test | Weak->Mixed | critical->critical | Yes (3/3) | n/a (clean) | No | n/a |

**Totals:** main core flag 10/10 · planted math computed 6/6 · false-alarm plans 5/10 firm (7/10 incl. 2 borderline, H04 H07) · severity over 4/10 (H05 H06 H07 H08) · strength match 5/10 · jargon 1/8 (H02)

Severity-over evidence: H05 "critical | 18% water saving is overgeneralized" (key high); H06 "high | Pass rate used as go/no-go is survey self-report" (key medium); H07 "critical | Unsupported 45% gross-margin claim" (key medium); H08 "high | Revenue ramp (85% by year 3) rests on only two prior openings" (key medium).

## Pre-mortem fabricated-event sentences
H01-H10: 0 each. All failure scenarios are hypothetical ("Failure scenario: ... may/could"). Borderline, not counted: H10 low flag "declaring the test a win, shipping immediately, and crediting the project in the bonus pool created incentives" (bonus is only planned in the plan); H05 "based on a small, founder-led sales process" ("founder-led" not in plan; a characterisation, not an event); H08 says plan "relies on price-driven growth" (mischaracterisation, not an event).
