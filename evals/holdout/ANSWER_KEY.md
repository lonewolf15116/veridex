# Veridex holdout set: answer key

This is a blind holdout set of ten synthetic strategy documents (H01-H10) for scoring the Veridex critic lenses, Evidence Audit in particular. It was written without reading the Veridex source or the existing eval files. Three plans are weak (H01-H03), three mixed (H04-H06), two strong (H07-H08), one is a backtest (H09) and one an A/B test (H10). Six plans carry one or two planted arithmetic inconsistencies (H01, H02, H04, H05, H08, H09). Four contain none (H03, H06, H07, H10) and test for false alarms. All figures were checked in Python. Every company, person and figure is invented. "Max reasonable severity" is the ceiling a well-calibrated reviewer should reach for the plan's worst evidence problem. A lens that goes above it is over-flagging.

---

## H01 - Solar cold-storage pods (Kenya)
- **Evidence strength**: Weak
- **Core flags**:
  1. Demand is unproven: no production unit, no sales, and "eleven cooperatives said they would want one" is interview interest, not purchase. The year-one figure of 300 pods has no basis.
  2. The $75/month saving is asserted, not measured. It rests on a regional post-harvest-loss midpoint from sector reports, and the plan assumes the pods remove all of the loss.
  3. The 95% on-time instalment assumption and the zero-paid-marketing referral assumption are untested.
- **Math catch**: 300 pods x $2,400 = $720,000, not the stated "$1.2M". Payback: $2,400 / $75 per month = 32 months, not "roughly 14 months".
- **Must NOT flag**: (a) "a third" spoilage versus "30 to 40 percent" is consistent. (b) The 6 m3 / 8-10 degrees / 5 days specs are not arithmetic. (c) Any data leakage, look-ahead or multiple-testing concern.
- **Max reasonable severity**: critical

## H02 - School bus routing software
- **Evidence strength**: Weak
- **Core flags**:
  1. The 12% bus reduction comes from simulations against two districts' last-year data, not a live deployment. There is no paying customer and no measured outcome.
  2. The growth plan is implausible: 6 to 120 districts in 12 months through public procurement, with three non-binding LOIs as the only market signal.
  3. Two solutions engineers cannot implement 120 districts. Cooperative purchasing is asserted to remove bid cycles with no evidence.
- **Math catch**: 6 x 1.25^12 = 87.3 (6 x 1.25^11 = 69.8), not 120. Reaching 120 from 6 in 12 months needs about 28.4% a month (about 140 districts at 30%).
- **Must NOT flag**: (a) 85 buses x $70,000 = $5.95M a year, and 12% of that (about $714k) against an $18,000 price is correct. (b) Ignore the 12% savings figure's source as an arithmetic problem; only its evidence is a concern. (c) Any data leakage or multiple-testing concern.
- **Max reasonable severity**: critical

## H03 - Prefab ADU factory (Texas)
- **Evidence strength**: Weak
- **Core flags**:
  1. Demand is unvalidated: 14 refundable $1,000 deposits ($14,000) from a single social post, against a 120-unit-a-year capacity plan.
  2. The 22% gross margin comes from a bottom-up cost budget with no supplier quotes or build data, and nobody on the team has run a factory (the ops lead has run a modular classroom plant).
  3. Lead-generation channels (paid search, builder partnerships) are untested. The 14-week build time and the permitting claim are unmeasured.
- **Math catch**: None - numbers are consistent. 120 x $98,000 = $11,760,000. $98,000 - $76,440 = $21,560 = 22.0% margin. 22% x $11.76M = $2,587,200. 14 x $1,000 = $14,000.
- **Must NOT flag**: (a) Revenue, margin and deposit totals are all correct. (b) The $4.5M start-up capital is a budget, not a derived figure. (c) Any data leakage or look-ahead concern.
- **Max reasonable severity**: critical

## H04 - Paediatric home physiotherapy (Denver)
- **Evidence strength**: Mixed
- **Core flags**:
  1. The 25-city extrapolation rests on one city where about 60% of new families come from a single paediatric group. Anchor-group dependence is not shown to be replicable, and the "same per-capita numbers within 18 months" claim is unevidenced.
  2. The CAC is wrong, so unit economics look better than they are.
  3. Therapist supply and sign-on costs in new cities are untested, and the "$900 lifetime gross profit" is stated without derivation.
- **Math catch**: $31,200 / 260 = $120 CAC, not $85. (Ratio to $900 falls from about 10.6x to 7.5x; still positive.)
- **Must NOT flag**: (a) $612,000 / $149 = about 4,107 sessions a quarter over 410 families and 19 therapists is plausible. (b) 81% retention is not contradicted anywhere. (c) Any data leakage or multiple-testing concern.
- **Max reasonable severity**: high

## H05 - Orchard irrigation sensors (California)
- **Evidence strength**: Mixed
- **Core flags**:
  1. The 18% water saving is a before/after comparison across a wet and a dry year, three sites, one season, and the plan then applies it to every acre of four crop types. The claim "real saving is higher" is unfalsifiable.
  2. Customer concentration: three customers, and the revenue shares do not add up.
  3. The 40,000-acre plan is a roughly 36x scale-up from 1,100 acres across crops never tested.
- **Math catch**: 52% + 31% + 22% = 105%, not 100%. Payback: $18,000 / $2,500 per month = 7.2 months, not "under six months".
- **Must NOT flag**: (a) 1,100 acres x $150 + $47,000 hardware leases = $212,000, which is correct. (b) $150 per acre x about 367 acres per grower supports a $2,500 monthly margin; do not call the margin inconsistent. (c) Any data leakage or look-ahead concern.
- **Max reasonable severity**: high

## H06 - Nurse English exam prep (Philippines)
- **Evidence strength**: Mixed
- **Core flags**:
  1. The result is one channel (Facebook/Instagram) in one country. The Nigeria/India expansion extrapolates that economics, though the plan gates it behind explicit cost and pass-rate thresholds.
  2. The 71% pass rate is self-reported by roughly half of the students who sat the exam, which creates response bias.
  3. "Contribution-level profitable" is unaudited and the saturation risk is only acknowledged.
- **Math catch**: None - numbers are consistent. 1,900 x $140 = $266,000. $58,000 / 1,900 = $30.53, stated as "about $30.50". Tests are 2 x $20,000 = $40,000.
- **Must NOT flag**: (a) The $30.50 CAC is correct. (b) The staged $20,000-per-market test with kill criteria is a sensible design, not a weakness. (c) Any data leakage or multiple-testing concern.
- **Max reasonable severity**: medium

## H07 - Commercial roofing maintenance program (Ohio)
- **Evidence strength**: Strong
- **Core flags**:
  1. The 45% margin assumption is plausible but untested at scale. The pilot is 140 informally billed buildings.
  2. Reaching 400 buildings means selling beyond contracts that already renew; the incremental 260 are unsold. The plan itself names this and sets a 250-building review gate.
- **Math catch**: None - numbers are consistent and this is the genuinely clean plan. $14.2M x 31% = $4.40M. 736 / 1,150 = 64.0%. 127 / 140 = 90.7% (91%). 400 x $2,100 = $840,000. 3 x $68,000 = $204,000.
- **Must NOT flag**: (a) The 91% renewal rate, which is correct. (b) The 45% margin being higher than the 31% company margin, which the plan explains. (c) Any data leakage or look-ahead concern; no backtest exists.
- **Max reasonable severity**: medium

## H08 - Veterinary group, fifth clinic (Minnesota)
- **Evidence strength**: Strong
- **Core flags**:
  1. The stated growth rate is slightly inconsistent with the stated revenue endpoints (mild).
  2. The new clinic's year-three revenue and margin come from two previous openings, a small sample, and new clinics run below group margin early. Veterinary recruitment and competition are acknowledged but not quantified.
- **Math catch**: $7.9M x 1.065^4 = $10.16M, not $10.4M. The implied rate is (10.4/7.9)^(1/4) - 1 = 7.1% a year, not "about 6.5 percent". All other figures check: $10.4M / 4 = $2.6M, 18% x $10.4M = $1.87M, 85% x $2.6M = $2.21M, 18% x $2.21M = $398k.
- **Must NOT flag**: (a) The 85%-of-mature, $2.2M and about $400k figures, which are consistent. (b) $1.1M build-out funded from $1.5M cash. (c) Any data leakage or multiple-testing concern.
- **Max reasonable severity**: medium

## H09 - Dividend-growth stock screen backtest
- **Evidence strength**: Weak
- **Core flags**:
  1. Survivorship bias: the universe is the 480 stocks in today's S&P 500 with complete histories from 2005. Companies that cut dividends, shrank or were dropped from the index are excluded, and a dividend-growth screen is especially exposed to this.
  2. The headline growth figure is wrong (see below), and the comparison is against an equal-weighted version of the same survivor universe, so the benchmark carries the same bias.
  3. Robustness is checked only over payout cut-offs on that same sample. There is no out-of-sample period, and the 2008-09 drawdown is a single episode.
- **Math catch**: $100,000 x 1.142^20 = $1,423,000, not "just under $1.9 million". The benchmark is consistent: 1.098^20 x $100,000 = $648,700 (about $650,000). Reaching $1.9M would need about 15.9% a year.
- **Must NOT flag**: (a) Look-ahead bias, timestamp leakage or walk-forward concerns. The plan has no feature or date leakage, and the intended flaw is survivorship. (b) The 10 bp trading cost, which is stated and plausible. (c) The benchmark return itself, which is consistent with its $650k figure.
- **Max reasonable severity**: critical

## H10 - Checkout redesign A/B test
- **Evidence strength**: Weak
- **Core flags**:
  1. Optional stopping: the test was planned for 28 days, checked daily, and stopped on day 9 once it looked good. That inflates false positives, and the p = 0.02 does not account for peeking.
  2. Small counts (86 vs 117 conversions) mean a wide interval around the 37% lift. A promotional email on day 6 sits inside a window that is only 9 days long, with no segmentation.
  3. The $691k annual gain extrapolates a 9-day result to a year with no follow-up test, and the team has already acted on it (approved a product-page redesign, bonus credit).
- **Math catch**: None - numbers are consistent. 86 / 2,150 = 4.0%. 117 / 2,130 = 5.49% (5.5%). Relative lift 37.3%. Two-proportion z = 2.30, two-sided p = 0.022. 60,000 x 4.0% = 2,400 orders x $64 = $153,600. 60,000 x 5.5% = 3,300 x $64 = $211,200. Difference $57,600 x 12 = $691,200.
- **Must NOT flag**: (a) The p-value, the 37% lift and the revenue projections, all of which are arithmetically correct. (b) Data leakage or look-ahead; the flaw is early stopping, not leakage. (c) Randomisation or the 50/50 split as such; these are not described as faulty.
- **Max reasonable severity**: critical

---

## Summary

| Plan | Strength | Planted math error (Y/N) | Backtest/experiment (Y/N) |
|---|---|---|---|
| H01 solar cold pods | Weak | Y (2) | N |
| H02 school bus routing | Weak | Y (1) | N |
| H03 prefab ADU | Weak | N | N |
| H04 paediatric physio | Mixed | Y (1) | N |
| H05 orchard sensors | Mixed | Y (2) | N |
| H06 nurse English prep | Mixed | N | N |
| H07 roofing maintenance | Strong | N (fully clean) | N |
| H08 vet fifth clinic | Strong | Y (1, mild) | N |
| H09 dividend screen | Weak | Y (1) | Y (backtest) |
| H10 checkout A/B test | Weak | N | Y (experiment) |
