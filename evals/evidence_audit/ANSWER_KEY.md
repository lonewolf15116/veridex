# Evidence Audit — answer key

None of 01–05 contains a backtest or describes trying multiple variants. Any mention of look-ahead,
leakage, parameter sweeps, multiple testing, walk-forward or "test beats train" is a false positive.
06 (demos/04-cascade-spider.md) is the regression case: it MUST flag the open-interest look-ahead as critical.

| # | Core flag | Math catch | Calibration |
|---|---|---|---|
| 01 Dental | 30% no-show cut unsourced; 18-month lifetime can't have been observed (no customers) | 2 reps × 6 mo ≥ ~$60k at $5k/mo each; $60k ÷ 50 ≈ $1,200 CAC vs $800 target | — |
| 02 Coffee | Churn ignored; $40 CAC asserted | 1.15^11 ≈ 4.65×, so 10,000 at m12 needs ≈ 2,150 at m1 | — |
| 03 Handyman | $25 CAC unsupported; 4-month liquidity unsupported | 200 × 3 = ~600 jobs/week needed by month 4 | — |
| 04 EU payroll | $1M ARR has no deal math; DE/FR compliance in 6 months asserted | $1M ÷ 40 = $25k per customer even at 100% conversion | Strongest plan: fewest/mildest flags, credit $4M ARR / profitable / 40 customers |
| 05 Ghost kitchen | $40K/mo in 90 days generalised from n=1 (own kitchen, founders' attention) | 20 × $40K × 20% = $160K/mo royalties at full ramp | — |

Out of lane for this lens: team size/staffing, pricing levels, shipping/margins, competition, GTM channel choice.
