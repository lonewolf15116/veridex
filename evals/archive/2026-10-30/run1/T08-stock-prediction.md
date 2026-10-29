# T08-stock-prediction

**Stage:** idea

## Input

We're developing an AI model that predicts stock-market movements with 95% accuracy. We plan to sell access to retail traders for $49 monthly. The model is still conceptual, and we have not collected data or run experiments.

**Reviewer expectation:** challenges metric definition, leakage, transaction costs, validation; no invented backtest outcomes; does not declare it demonstrably impossible.

## First critique

### pre_mortem

The plan rests on an extraordinary, untested technical claim (95% predictive accuracy) and multiple unstated assumptions about data, model generalization, and customer willingness to pay. If any of those central assumptions fail, the product has no foundation. The highest-risk items are the accuracy claim itself, the availability of usable data that generalizes, and the unvalidated assumption that retail traders will subscribe without a vetted track record or trust signals.

- **Core claim of 95% predictive accuracy is unsubstantiated and implausible** [CRITICAL] (assumptions)
  The strategy's single foundational claim is that an AI model can predict stock-market movements with 95% accuracy; the document provides no data, experiments, or definition of the metric. This claim must be true for the business to exist as stated; if it is false or never demonstrated on realistic, out-of-sample data, the entire plan collapses. No alternative business model is described if this turns out to be unattainable.
  -> What empirical, out-of-sample evidence (with a precise prediction horizon and label definition) demonstrates >=95% accuracy under realistic testing conditions?

- **No evidence retail traders will pay $49/month for this product** [HIGH] (demand_evidence)
  The $49/month price and the buyer (retail traders) are asserted without any demand validation. Retail traders typically require verifiable performance history, trust, integrations, or different packaging; assuming they'll subscribe to an unproven black-box model is a large leap. The plan lacks any stated experiments to validate willingness-to-pay or product-market fit.
  -> Can you show validated willingness-to-pay (e.g., pre-sales, paid pilot commitments, or conversion on a landing page) from retail traders at $49/mo?

- **Assumes access to clean, exhaustive data and that models will generalize despite market non‑stationarity** [HIGH] (assumptions)
  No data collection plan or discussion of look-ahead bias, survivorship bias, regime shifts, or covariate shift is provided. The idea assumes training data exists and will produce a model that generalizes to live markets—an assumption that often fails for financial prediction problems. If suitable, unbiased historical data or a protocol to avoid overfitting does not materialize, the claimed performance is unachievable.
  -> What exact datasets and validation protocols will you use to train and test the model, and do walk-forward/backtest results survive tests for look-ahead and regime-change biases?

- **Accuracy metric (95%) is not connected to real trader value or profitability** [MEDIUM] (assumptions)
  Even if direction predictions are 95% accurate by some definition, that metric may not translate into profitable, usable signals after accounting for timing, position sizing, slippage, and transaction costs. The founder hasn't specified prediction granularity (next tick, day, week) or how accuracy maps to net P&L for retail traders. This mismatch could mean the marketed metric is irrelevant to customers.
  -> How does your chosen accuracy metric (horizon, label, frequency) convert into net trader P&L after realistic costs and execution constraints?

- **Misread of trust/ differentiation: retail traders may require audited track record or explainability** [MEDIUM] (differentiation)
  The plan assumes retail traders will adopt and pay for access to a predictive AI model without articulating trust-building features (verified track record, audited performance, explainability, or integration with broker platforms). It also does not state why traders would choose this offering over existing signal providers, copy-trading, or broker tools. This is a gap in understanding the buyer's selection criteria.
  -> What evidence or product features (e.g., audited returns, explainability, broker integrations) will differentiate your product and convince retail traders to trust and buy it?

- **Regulatory/operational assumption: ability to sell market predictions without advice/licensing constraints** [MEDIUM] (assumptions)
  The document assumes the product can be sold directly to retail traders as a subscription without addressing whether providing predictive signals constitutes regulated investment advice in target jurisdictions. If the offering requires licensing or adherence to disclosure rules, that will materially change go-to-market and trust requirements. No legal/regulatory validation is described.
  -> Have you validated the legal/regulatory classification of selling market predictions in your initial target markets and what restrictions or disclosures will be required?

### unit_economics

The document provides a headline price ($49/mo) and an untested product claim (95% accuracy) but contains no unit-economic inputs. Key drivers — per-user cost to serve, validated willingness-to-pay, CAC and channels, gross margin and payback math, and hidden operational/compliance costs — are entirely absent, so the economics cannot be assessed. Before building, the founder must produce a minimal set of experimentally-backed numbers or run quick tests to populate LTV, CAC, cost-to-serve and refund/chargeback assumptions.

- **No estimate of cost-to-serve a user (compute, storage, support, payments)** [HIGH] (key_numbers)
  The plan gives a $49/mo price but lists no per-user cost assumptions: inference CPU/GPU time, model hosting, storage of signals/logs, customer support staffing, or payment processing fees are unspecified. Without per-user cost you cannot compute gross margin, scale costs (e.g., model inference at scale), or whether $49 covers variable costs. This is a fundamental missing input for any unit-economics model.
  -> What is your expected per-user monthly cost broken down by inference compute, storage, support, and payment processing (with assumptions about model size, inference frequency, and support load)?

- **Price given ($49/mo) has no evidence of willingness-to-pay** [HIGH] (pricing)
  The $49 monthly price is asserted with no user research, price testing, or analogous market data. For subscription products aimed at retail traders, willingness-to-pay can vary widely with demonstrated signal quality; absent experiments the revenue per user is speculative. This undermines any LTV or payback calculations.
  -> How did you validate $49/month as a real willingness-to-pay — show conversion or pricing-test data, or state how you will run the cheapest test to validate it?

- **No CAC or acquisition channels specified (so payback infeasible to model)** [HIGH] (acquisition)
  The strategy implies selling to retail traders but lists no acquisition channels, expected conversion rates, or CAC. At $49/mo you need realistic channel unit economics (e.g., performance ads, affiliates, content) to know if CAC < first-month gross margin or LTV. Without this you cannot compute payback period or judge scalability.
  -> Which acquisition channels will you use and what are the expected CAC and conversion rates for each channel (or how will you cheaply measure them)?

- **Gross margin and payback period not modeled at all** [MEDIUM] (key_numbers)
  There is no LTV, churn, gross margin, or payback calculation presented — no current vs. scale margin analysis. Investors and operators need an explicit model showing ARPU, variable cost, contribution margin, churn and resulting payback months. Without these, unit economics are unknowable.
  -> Provide a simple LTV/CAC table: ARPU, monthly churn, gross margin per user, CAC, and resulting payback months (or state current estimates and sources).

- **Hidden/omitted costs (compliance, refunds, chargebacks, fraud, moderation, retraining)** [MEDIUM] (assumptions)
  The doc assumes a clean $49 subscription revenue stream but omits common and potentially large hidden costs: legal/compliance for financial advice to retail traders, chargebacks/refunds, fraud prevention, costs to retrain/label models, and content moderation for user communications. These can materially reduce margins or add fixed costs.
  -> How will you account for regulatory/compliance costs, refund/chargeback rates, fraud prevention, and ongoing model retraining in your unit-economics model (include expected % of revenue or fixed costs)?

### adversarial_competitor

This is an untested, extraordinary claim (95% accuracy) with no data, no definition of the prediction task, no customer validation, and no go-to-market plan — a high-fragility idea that is easy to neutralize. Cheapest kill: incumbents (brokers, trading apps, or a well-funded signal vendor) can ship a transparent, lower‑risk signal product or free trial, bundle it into existing accounts, and use brand trust + distribution to swamp this newcomer. The single incumbent feature that kills it is a broker-integrated predictive signal/alert with public backtests and a free tier; combine that with loss-leading pricing, owned user lists, SEO/app-store placement, and partner channels to make this product redundant before it launches.

- **Extraordinary 95% accuracy claim with no evidence** [CRITICAL] (assumptions)
  The founder asserts '95% accuracy' but provides no definition of what is being predicted (time horizon, instrument, up/down vs. magnitude), no data, no out-of-sample backtest, and no evaluation protocol. Without a reproducible metric and independent validation this claim is either meaningless or impossible, and it undermines the entire product proposition. Competitors and regulators could quickly expose or replicate any weak proof, destroying trust.
  -> Show a reproducible, out-of-sample backtest (with clearly defined prediction task and time horizon) that achieves 95% and explain how you avoid lookahead/data-snooping.

- **No evidence retail traders will pay $49/month** [HIGH] (demand_evidence)
  A price is stated but there is no validation that retail traders see enough value to subscribe, nor evidence on conversion rates, trial behavior, or churn for this category. Willingness-to-pay for trading signals varies widely and is tightly coupled to perceived credibility, track record, and integration with trading flow — none of which are addressed. Without early demand tests the price and revenue model are speculative.
  -> What validated demand signals (preorders, landing-page conversions, paid pilots) show retail traders will pay $49/month for this service?

- **No go-to-market or distribution plan — easy for incumbents to out-distribute** [HIGH] (acquisition)
  There is no acquisition strategy, customer funnel, or channel described; retail traders are reachable cheaply via brokers, fintech apps, newsletters, and app stores, all channels incumbents already own. A well-funded competitor can bundle a signal into an existing brokerage app, push it to millions of active accounts, and undercut or bury an independent startup in acquisition and retention metrics. This product lacks defensible placement.
  -> Which specific channels, partnerships, and CAC targets will you use to acquire retail traders, and why would you win those channels versus brokers and signal vendors?

- **Undifferentiated vs existing signals and research products** [MEDIUM] (differentiation)
  The document gives no unique data source, proprietary model architecture, IP, or integration that would prevent incumbents from replicating the feature quickly. Predictive signals are a crowded space (newsletters, quant services, broker algorithms), so without clear differentiation this offering is a commodity that established players can reproduce and rebrand. Differentiation is the primary lever for charging subscription fees.
  -> What unique data, model, or integration (not currently replicable by incumbents) gives you sustained advantage over brokers and signal vendors?

- **Key operational and financial numbers are missing** [MEDIUM] (key_numbers)
  There are no estimates for data requirements, model training compute, labeling costs, expected latency, CAC, LTV, or unit economics for a $49/month product. Without these inputs you cannot assess feasibility, pricing, or runway; a competitor with scale can absorb these costs and offer a loss-leading product that this startup cannot match. Missing numbers also hide how defensible the product is to replication.
  -> Provide estimated data volume, training/serving costs, CAC, expected churn, and LTV to justify the $49/month price and show you can scale profitably.

### execution_risk

The plan asserts a near-perfect predictive model and a paid retail subscription with no data, team, compliance or go-to-market details. The biggest shipping risks are regulatory blocking (selling trading predictions to retail can be regulated), lack of any data/validation for the 95% accuracy claim, and a severe underestimation of engineering, ML and compliance effort. Smaller but real risks are wrong sequencing (selling before validating), no customer acquisition plan, and an untested price point.

- **Regulatory/financial-advice blocker — selling predictions may be regulated as investment advice** [CRITICAL] (assumptions)
  Offering a model that predicts stock movements to retail users likely falls into financial advice / investment product territory in many jurisdictions. Without a compliance plan the project can trigger cease-and-desist orders, fines, or mandatory registration as an advisor or broker—any of which would block or dramatically change the business model. The document contains no legal or jurisdictional analysis or plan for licensed distribution.
  -> Which jurisdictions and regulators (e.g., SEC, FCA or equivalent) have you reviewed, and what licenses, registrations, or compliance processes are required to sell predictive stock signals to retail users there?

- **No data or validation plan — the 95% accuracy claim is ungrounded** [HIGH] (assumptions)
  You have neither collected data nor run experiments yet claim 95% accuracy. Failure mode: spending months building product and infra only to find no accessible data, label quality problems, or that the model cannot reach anywhere near that accuracy on out-of-sample tests. There is no minimal dataset, backtest plan, or falsification metric documented.
  -> What minimum historical and live data will you need, how will you access it, and what exact backtest/out-of-sample metric would falsify the '95% accuracy' claim?

- **Underestimated engineering, ML and ops scope — team/timeline mismatch** [HIGH] (assumptions)
  Delivering a production-grade financial ML product requires data ingestion pipelines, feature engineering, label generation, backtesting framework, model monitoring, latency-sensitive infra, security, billing and UX. The idea-stage plan implies rapid execution but contains no team, roles or timeline; failure mode: a tiny team spends months and still ships a brittle MVP with no monitoring or reproducibility.
  -> Who is on the team (engineers, ML researchers, quant traders, ops), and what is a realistic timeline and milestone plan for data pipelines, model validation, production infra, and monitoring?

- **Sequencing error — building subscriptions before proving predictive value** [MEDIUM] (assumptions)
  You plan to sell subscriptions at $49/month without first validating the core hypothesis that the model produces reliable, tradeable signals. Failure mode: customers sign up briefly then churn when predictions fail, or legal/ethical issues arise from wrong signals. The cheapest missing step (backtests, simulated/paper trading) is not described.
  -> What is the minimum validation experiment (backtest, paper-trade period, or pilot) you will run and what pass/fail criteria will you require before opening paid subscriptions?

- **No acquisition or trust-building plan for retail traders** [MEDIUM] (acquisition)
  There is no go-to-market plan: no channels, partners, influencer strategy, trials, or trust mechanisms (proof-of-performance, third-party audits). Failure mode: a built product with near-zero traction because retail traders distrust black-box claims and acquisition costs are far higher than assumed.
  -> Which specific acquisition channels and trust-building tactics (e.g., audits, paper-trade demos, partnerships with brokers) will you use, and what are your CAC/lead assumptions to reach initial users?

- **Pricing untested — $49/mo is arbitrary** [LOW] (pricing)
  $49/month is asserted without evidence of willingness-to-pay, trial structure, or competitive benchmarking. Failure mode: price too high to attract skeptical retail traders or too low to cover compliance and infra, causing poor retention or unprofitable unit economics.
  -> How will you test willingness-to-pay (pilot pricing, trials, freemium) and what conversion or retention thresholds will validate the $49/mo price?

### evidence_audit

Evidence base: Weak. The plan is purely conceptual with no data, experiments, or customers. The most important gap is the complete absence of any out-of-sample evaluation or data-backed evidence for the 95% accuracy claim.

- **95% accuracy claim is entirely unsupported** [CRITICAL] (key_numbers)
  You state the model will achieve 95% accuracy but have no data, backtest, pilot or experiment. This single number is the core technical claim and cannot be accepted without an out-of-sample evaluation showing how accuracy was measured, what data and period were used, and how results generalise. Without that evidence the central technical premise of the plan is unproven and could be false.
  -> Provide a concrete out-of-sample evaluation (dataset, time period, train/test split method, exact prediction task, and resulting confusion matrix or equivalent) that demonstrates 95% accuracy under realistic conditions.

- **Prediction target and metric are undefined (makes 95% meaningless)** [HIGH] (assumptions)
  You don't define what 'predicts stock-market movements' or '95% accuracy' mean: direction vs magnitude, time horizon (next tick, day, month), the unit of prediction, class balance, or whether accuracy is compared to a baseline. These definitions determine whether 95% is trivial (e.g. always predict the majority class) or genuinely predictive.
  -> Specify the exact prediction target (asset universe, forecasting horizon, frequency), the positive class definition, the metric(s) you will report (accuracy, precision/recall, Sharpe, P&L after costs), and the baseline accuracy to beat.

- **No data acquisition / dataset plan described** [MEDIUM] (assumptions)
  You haven't stated which historical market data, features, labels, or alternative datasets you'll use, nor their availability, cost, latency or licensing. Success depends on having suitable, high-quality data for training and realistic backtesting; without it the modelling claim is hollow.
  -> Provide the specific data sources you will use (vendors/APIs, fields, time span, sample size), their costs/licensing terms, and a plan for obtaining cleaned, timestamped data suitable for backtesting.


## Selected questions

- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No estimate of cost-to-serve a user (compute, storage, support, payments) [high]
  - why we're asking: unit_economics / Gross margin and payback period not modeled at all [medium]
  - why we're asking: adversarial_competitor / Key operational and financial numbers are missing [medium]
  - why we're asking: evidence_audit / 95% accuracy claim is entirely unsupported [critical]
- **acquisition**: How will your first customers find you?
  - why we're asking: unit_economics / No CAC or acquisition channels specified (so payback infeasible to model) [high]
  - why we're asking: adversarial_competitor / No go-to-market or distribution plan — easy for incumbents to out-distribute [high]
  - why we're asking: execution_risk / No acquisition or trust-building plan for retail traders [medium]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / No evidence retail traders will pay $49/month for this product [high]
  - why we're asking: adversarial_competitor / No evidence retail traders will pay $49/month [high]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: unit_economics / Price given ($49/mo) has no evidence of willingness-to-pay [high]
  - why we're asking: execution_risk / Pricing untested — $49/mo is arbitrary [low]

## Answer given

**demand_evidence**: We haven't spoken to any retail traders yet, and the 95% accuracy is a target, not a result.

Skipped: key_numbers, acquisition, pricing

## Refined critique

### pre_mortem

The plan rests on a single extraordinary technical claim (95% predictive accuracy) with no supporting evidence and no customer discovery. Key assumptions about who will pay, what metric matters to users, and access to suitable data were unstated and thus likely false. The most probable failure is that the model never achieves robust, out-of-sample predictive performance that actually matters to retail traders.

- **Core technical claim (95% accuracy) is unsupported and likely unattainable in real markets** [CRITICAL] (assumptions)
  The founder states a 95% accuracy target but has no data, experiments, or definition of the metric. Financial markets are noisy and non-stationary; without out-of-sample live-forward evidence, the 95% figure is a hypothesis, not a capability. If the model cannot deliver predictive performance prospectively, the product value disappears instantly.
  -> What live, out-of-sample evidence can you produce (forward test, not backtest) that your model achieves the claimed accuracy on future market data?

- **No customer discovery — buyer persona is unknown** [HIGH] (buyer)
  The founder has not spoken to any retail traders and therefore has not validated who the customer actually is, what their workflow is, or whether they would accept a $49/mo subscription. Without identifying specific paying personas (active day traders, swing traders, novices), the product could be misaligned with actual needs and distribution channels.
  -> Which specific retail trader persona is the first paying customer and what primary evidence (interviews, commitments, paid trials) shows they want this product?

- **Pricing and willingness-to-pay are assumed, not tested** [HIGH] (pricing)
  The $49/month price is asserted with no validation of willingness to pay, elasticity, or alternative commercial models. Different segments of retail traders have very different value perceptions and budgets; treating $49 as a given risks building a product no one will convert to pay for.
  -> What direct evidence (pre-sales, pricing experiments, competitor pricing comparisons with conversion data) shows retail traders will pay $49/month for your offering?

- **Metric mismatch: accuracy ≠ trader value (profitability/utility not defined)** [HIGH] (key_numbers)
  The plan focuses on a single accuracy number without specifying what 'accuracy' means (directional, magnitude, time horizon) or showing that that metric correlates with trader outcomes (profit, risk-adjusted return, reduced drawdown). High nominal accuracy can coincide with no economic benefit to users if it's concentrated on low-impact signals.
  -> Which specific, business-relevant performance metric (e.g., risk-adjusted return per trade, hit rate on high-conviction signals) will you optimize, and how do you prove it improves traders' outcomes in realistic tests?

- **Unstated dependency on access to suitable, high-quality market data** [MEDIUM] (assumptions)
  No datasets, frequency, time horizon, or labeling approach are specified; the founder has not tested that the necessary historical and live data are obtainable or fit for training a production-grade predictive model. If the data needed are expensive, restricted, or insufficiently rich, model development will stall or overfit.
  -> What exact datasets (symbols, time resolution, history length) will you use for training and validation, and can you practically obtain them under realistic cost and licensing constraints?

### evidence_audit

Evidence base: Weak. The plan is pre-launch with no measured model performance, experiments or customer discovery. The most important outstanding issue is the lack of any measured accuracy or willingness-to-pay / acquisition evidence to support the 95% accuracy claim and $49/month revenue model.

- **95% prediction accuracy is a load‑bearing unsourced number** [HIGH] (key_numbers)
  The central technical claim — a model that predicts stock-market movements with 95% accuracy — is stated as a target with no data, backtest, experiment or method. This number is the foundation for pricing and demand but currently has no provenance (dataset, time period, out-of-sample performance or evaluation metric). Without measured results the plan has no bridge from concept to product-market fit.
  -> Provide measured performance: a reproducible evaluation (dataset description, time range, sample size, train/holdout split and the model's out-of-sample accuracy and relevant metrics) showing performance close to 95%; if unavailable, state the largest empirical accuracy achieved and on what data.

- **No evidence retail traders want or will use this** [HIGH] (demand_evidence)
  Founder admits to zero conversations with retail traders and gives no market discovery data. Demand for a high‑accuracy trading predictor is not self-evident; willingness to pay, use patterns, and trust thresholds among retail traders are unknown. This makes revenue and growth projections (implicit in selling subscriptions) unsupported.
  -> Share customer discovery evidence: results from structured interviews or surveys with a specified number of retail traders (n) showing the fraction who would pay for this product, how they would use it, and the stated maximum monthly price.

- **Price point ($49/mo) is asserted without willingness‑to‑pay evidence** [MEDIUM] (pricing)
  The $49 monthly price is presented as the revenue model but has no supporting data showing retail traders will pay that amount for this type of signal or service. Price interacts with conversion, churn and LTV; without tests the revenue model is speculative.
  -> Provide evidence that $49/month is acceptable: results from pricing experiments, surveys with explicit price choice, or conversion estimates from a landing‑page test at that price and the sample size used.

- **No customer acquisition plan or CAC / funnel assumptions** [MEDIUM] (acquisition)
  The document contains no channels, experiments or cost assumptions for acquiring retail subscribers. Without at least an initial measured CAC or validated channel, you cannot project how many signups $X spend will produce or whether the unit economics support the price point.
  -> Specify initial acquisition channel(s) and provide measured or conservatively bounded CAC (with source) and an expected conversion funnel (impressions → leads → paid) for each channel.

- **Buyer segment is underspecified — who exactly is the paying customer?** [LOW] (buyer)
  The target is loosely described as 'retail traders' but there is no segmentation (day traders vs. long-term retail, geographic or regulatory constraints, platform preferences). Different retail segments will have different price sensitivity and use cases, which affects demand and acquisition strategy.
  -> Define the paying customer precisely: which retail trader segment(s) you target first, with rationale and any evidence that this segment would value a predictive signal enough to subscribe.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['key_numbers', 'acquisition', 'pricing']

## Reuse check

Re-sending the same refinement token refused with 409: yes
