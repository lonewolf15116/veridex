# Cascade Spider: a squeeze-fade crypto bot

## Thesis
Crypto perpetual futures are full of forced flow. When shorts get liquidated, price spikes for a few minutes and open interest drops as positions are closed by the exchange. That buying is forced, not informed, so price tends to give some of it back. Cascade Spider sells into these short squeezes using resting limit orders and buys back on the retrace.

The bot never predicts direction and never pushes price. It only provides liquidity to traders who are being forced out.

## How it trades
- Watches 10 Binance USD-M perpetuals: BTC, ETH, SOL, XRP, DOGE, BNB, LINK, AVAX, ADA, SUI.
- Every 5 minutes it computes a "panic meter" per coin: price move against 24h volatility, change in open interest over the same 5 minutes (from Binance's 5-minute open-interest history), and volume against its 24h median.
- Trigger: a 5-minute up-move of at least 3 standard deviations, open interest falling at least 1%, and volume at least 3x normal.
- On a trigger it places three resting sell limit orders slightly above the trigger price (5%, 10% and 15% of the spike's size above it), live for 60 minutes.
- Take profit when price retraces 80% of the spike. Hard stop beyond the top rung. Maximum hold 12 hours.

## Risk rules
- 0.5% of equity at risk per trade, sized as if all three orders fill and the stop is hit.
- Max 3x leverage per position, 6x per account, at most 4 positions open and one per coin.
- Daily kill switch at -2%. Position size shrinks automatically during drawdowns and regrows on recovery.

## Backtest
- Data: Binance public historical data, January 2023 to August 2026, 1-minute candles, 5-minute open interest, funding rates.
- Costs modelled: 0.02% maker, 0.05% taker, 0.10% extra slippage on stops, funding paid or received.
- Fills are conservative: limit orders only fill if price trades through them, and stops are assumed to hit before take-profits within the same minute.
- Parameters were chosen on 2023-2024 data from a sweep of 6,768 combinations (signal thresholds, order spacing, stop, take-profit, holding time), picking the highest Sharpe among setups with at least 80 trades and under 20% drawdown.
- Then tested once on January 2025 to August 2026.

| Period | Return | Sharpe | Max drawdown | Trades | Win rate |
|---|---|---|---|---|---|
| Train 2023-2024 | +16.3% | 1.46 | 15.7% | 399 | 58% |
| Test Jan 2025 - Aug 2026 | +52.9% | 3.18 | 4.4% | 321 | 69% |

- In the test period all 10 coins were profitable. Removing any single coin still leaves +43% or more.
- The same orders placed at random times lose money (-6.6% in test), so the signal matters.
- 2023 alone lost 15%; 2024 made +60%.

## Plan
1. Month 1-2: run live with $10,000 of my own money on Binance, same rules.
2. Month 3-6: scale to $50,000 if live results track the backtest within 30%.
3. Month 6+: sell the signals as a Telegram subscription at $49/month and target 500 subscribers ($24,500 MRR). Later, offer a managed account product.

## Why now
Open-interest data is public and free, the infrastructure costs under $20/month (one small cloud server), and the edge comes from forced flow, which should persist as long as leverage exists in crypto.
