# T02-restaurant-inventory

**Stage:** idea

## Input

I want to build an AI tool that predicts food waste for independent restaurants using historical sales and inventory data. Restaurants would pay £79 per month, and I plan to acquire early customers through direct outreach to restaurant owners.

**Reviewer expectation:** identifies data availability, willingness to pay, existing inventory systems, integration complexity; no invented trials or waste-reduction percentages.

## First critique

### pre_mortem

The plan rests on unvalidated assumptions about data availability, willingness to pay, and easy customer access. The most likely killing blow is that independent restaurants either do not have usable historical sales + inventory data in a machine-readable form or will not share it—without that, the predictive product cannot operate. Other high-risk assumptions include the £79/mo price being acceptable, direct outreach being an effective acquisition channel, and waste prediction being a high priority versus simpler operational fixes.

- **Target restaurants lack usable historical sales & inventory data** [CRITICAL] (assumptions)
  The strategy assumes independent restaurants have historical sales and inventory data in a form the AI can consume; the founder provided no evidence. If shops use paper logs, ad-hoc spreadsheets, or no inventory tracking, the model cannot be trained or deployed at scale. Cheap first test: call or visit 15–30 local independents and ask for a recent week's exports/screenshots or offer to ingest one sample manually to see what real data looks like.
  -> Do independent target restaurants reliably have machine-readable historical sales and inventory data (or will they export/share it) so the product can function at all?

- **The £79/month price is unsupported by willingness-to-pay evidence** [HIGH] (pricing)
  A fixed subscription price was declared without evidence that independent restaurants will pay recurring fees for predictive analytics. Restaurants may prefer free/basic tools, one-off consultancy, or integrated POS features rather than a separate £79 subscription. Cheap test: run a landing page/preorder offer or pilot sale to 20 owners at £79 and measure signups or use short phone interviews with direct willingness-to-pay questions.
  -> Will a sufficient number of independent restaurants commit to paying £79/month for predictive food-waste analytics?

- **Direct outreach to owners is assumed to be an effective acquisition channel** [HIGH] (acquisition)
  The plan relies solely on direct outreach without evidence that owners are reachable, receptive, or willing to trial new analytics tools. Independent owners often have gatekeepers, limited time, and many competing priorities, so direct outreach may yield low conversion. Cheap test: attempt targeted outreach (calls/visits/emails) to 50 restaurants and record contact rate, demo interest, and trial commitments to validate conversion assumptions.
  -> Can direct outreach to independent restaurant owners convert enough early customers at a rate/cost that validates the go-to-market approach?

- **Assumed priority: waste prediction is a top pain worth paying to solve** [HIGH] (demand_evidence)
  The founder assumes waste prediction is a high-priority, actionable problem for independents, but no user research is cited. Owners may prioritize labor, menu pricing, suppliers, or cash flow over predictive waste analytics, making adoption unlikely even if the product works. Cheap test: qualitative interviews and a simple ranking exercise with 20 owners to see where waste forecasting sits among their top pain points and what value they'd assign to a solution.
  -> Is predictive food-waste forecasting a priority problem for independent restaurant owners compared to other operational issues, and would they pay for it?

- **Data quality and integration complexity underestimated** [MEDIUM] (assumptions)
  Even if data exists, its format, completeness, and linkage (sales to inventory to recipes) are unspecified and may be inconsistent across restaurants, making modeling and integration costly. The founder did not describe expected schemas, POS systems, or fallbacks for missing fields. Cheap test: request raw exports from three different POS/inventory setups and attempt a quick normalization and baseline model to surface real integration issues.
  -> Can we reliably ingest, normalize, and use exports from the common POS/inventory systems used by target restaurants without prohibitive manual work?

- **Unclear alternatives and differentiation from current workflows** [MEDIUM] (alternatives)
  The document doesn't state what restaurants currently do to manage waste or why they'd replace those workflows with this tool. If owners use simple heuristics, suppliers' forecasts, or prefer POS vendor features, a separate predictive product may be redundant. Cheap test: map current workflows by interviewing owners and list existing tools/shortcuts they use so you can define a clear differentiation or integration path.
  -> What do restaurants use today to manage waste and inventory, and why would they choose this standalone predictive product instead?

### unit_economics

The document gives a single price (£79/mo) and an acquisition channel (direct outreach) but provides no unit-costs, CAC estimates, conversion assumptions, or evidence of willingness-to-pay. Key inputs required to validate unit economics — cost to serve per user (compute, storage, onboarding/support, payment fees), realistic CAC by channel, gross margin at scale, and payback period — are all missing. First tests should be cheap customer conversations and a priced landing page or paid pilot to validate willingness-to-pay and to collect initial CAC/conversion data, and a simple cost model (cloud + onboarding + support + payments) to estimate per-user unit cost.

- **Listed price (£79/mo) has no evidence of willingness-to-pay** [HIGH] (pricing)
  You state restaurants would pay £79/month but provide no evidence for that price: no customer interviews, no pilot, no reference to how much value (waste reduction) translates to willingness-to-pay. Without demand evidence the revenue per user is an untested assumption and could be far lower. If restaurants only value it at a fraction of that price the whole unit economics break.
  -> What direct evidence (surveys, paid pilots, LOIs, or pre-signups) shows restaurant owners will pay £79/month instead of a lower price or a one-time/commission model?

- **No estimate of cost to serve one restaurant (compute, storage, support, payments)** [HIGH] (key_numbers)
  The plan contains no breakdown of per-customer costs such as cloud compute for ML predictions, data storage, connectors/ETL, onboarding time, ongoing customer support, or payment processing fees. These are necessary to compute gross margin and scalable unit economics; without them you cannot know whether £79/mo covers operating costs. Heavy data-cleaning and integrations for restaurants often make per-customer costs material, but you present no numbers.
  -> Provide a per-customer cost model (estimates for compute, storage, ETL/integration labor amortized per customer, onboarding hours, ongoing support cost, and payment processing fees) so we can calculate gross margin at £79/month.

- **CAC and channel economics are undefined for direct outreach** [HIGH] (acquisition)
  You plan to acquire early customers via direct outreach but give no CAC estimate, expected conversion rates, salesperson time per closed deal, or whether outreach is owner-level or manager-level. Direct outreach can be expensive and slow for low-priced B2B products; without CAC and funnel conversion numbers it's unknown if payback is feasible at £79/mo. Additionally, channel scalability (how many restaurants can be reached per SDR) is unstated.
  -> What is your expected CAC (broken down by labor, tools, and outreach expenses) and expected conversion rate from outreach to paid customer, based on any prior experiments or comparable benchmarks?

- **Gross margin at scale vs. today is unspecified** [MEDIUM] (key_numbers)
  No current or projected gross margin is shown. You need to know per-user gross margin today (with onboarding and manual steps) and how it improves when processes or automation scale. Without this you can't assess sustainability or required price/CAC targets. The lack of a margin projection obscures capital needs and profitability timelines.
  -> What is the projected gross margin per customer today (including manual onboarding and support) and at target scale after automation, expressed as £/month and % of revenue?

- **No payback period or unit economics sensitivity analysis** [MEDIUM] (key_numbers)
  You don't show payback period (months to recoup CAC from gross margin), nor which variables (CAC, churn, price, integration time) would break payback. For subscription businesses this is critical to understand capital needs and viability. Without churn and CAC inputs there is no way to know if growth is self-funding or requires sustained investment.
  -> What is the expected customer lifetime (or churn rate) and the resulting payback period on CAC given your price and projected gross margin?

- **Hidden onboarding, data-integration and operating costs are unaddressed** [MEDIUM] (assumptions)
  Key operational costs that often dominate early-stage unit economics — time to normalize restaurant data, connector maintenance, per-customer customizations, fraud/chargeback handling, refunds and legal/compliance — are not mentioned. These can materially increase per-customer costs and lengthen payback. Treating the product as 'low-cost' without quantifying these risks is an unstated assumption.
  -> How much time and cost do you expect for initial data integration and ongoing maintenance per restaurant, and what assumptions ensure these costs remain low enough for profitability at £79/mo?

### adversarial_competitor

This idea-stage product rests on a narrow technical pitch (AI predicts food waste) but offers no defensible moat, no demand proof, and a fragile GTM. A well-funded incumbent (or a large POS/inventory vendor) can neutralize it cheaply by adding a forecasting feature, bundling it into existing products, or giving a free/light tier to their users while using their distribution and brand to win trust. The founder must prove willingness-to-pay, a clear beachhead customer, and a defensible data/tech advantage before this becomes strategically valuable.

- **No defensible differentiation — trivial for incumbents to replicate** [CRITICAL] (differentiation)
  The plan offers a generic ML forecast for waste without describing proprietary data, unique models, integrations, or network effects that competitors can't copy. Large POS, inventory, or accounting vendors can add a similar forecasting widget or report and push it to all their customers, making a standalone £79/month tool redundant. The founder hasn't articulated any lock-in (e.g., exclusive data, hardware tie-in, or contractual relationships) that would prevent rapid replication.
  -> What concrete technical, data, contractual, or distribution barrier prevents major POS/inventory providers or well-funded rivals from shipping the same waste-forecasting feature and bundling it into their product?

- **No evidence restaurants will pay £79/mo** [HIGH] (demand_evidence)
  The price point is stated but there's no validation that independent restaurants perceive £79/month as worth paying or that the ROI is obvious and realizable. Independent restaurants are price-sensitive and often accept free spreadsheets or low-cost add-ons; without WTP tests you risk building a product nobody buys. The founder hasn't proposed experiments to validate retention or LTV assumptions.
  -> What is your cheapest experiment to validate willingness-to-pay and monthly retention (e.g., paid pilot, convertible pre-order, or landing page with pricing) and what conversion threshold would make £79 viable?

- **GTM relies on one expensive channel (direct outreach) that won't scale** [HIGH] (acquisition)
  Cold outreach to restaurant owners can work for initial pilots but is labor-intensive and expensive to scale; meanwhile incumbents can exploit SEO, POS marketplaces, referral partnerships, and app stores to flood the market. The plan has no acquisition funnel, CAC estimate, or channel prioritization that would survive competition from players with large installed bases and channel partnerships.
  -> How will you acquire restaurants at scale (specific channels and projected CAC), and what channel gives you an edge versus being out-competed by incumbents with existing distribution?

- **Pricing is fragile — larger players can undercut or bundle cheaply** [HIGH] (pricing)
  A well-funded competitor can undercut by offering a free/basic forecasting tier, including the feature in existing subscriptions, or subsidizing pilots to capture users. Independent restaurants often favor integrated, low-cost solutions; without unique value or scale the startup will be forced into price competition they can't win. The founder hasn't justified why customers would pay a standalone premium rather than accept a bundled or cheaper alternative.
  -> How do you defend a £79/month standalone pricing model if larger vendors bundle the same capability for free or at a lower price as a retention tool?

- **Unclear what restaurants do today (alternatives and switching costs)** [MEDIUM] (alternatives)
  No description of current workflows: spreadsheets, manual ordering, POS reports, or existing inventory apps could already solve most of the problem. If current alternatives are 'good enough' or integrated into POS workflows, convincing restaurants to switch to a new tool is costly. The founder needs to map incumbent workflows and quantify the incremental value of their AI.
  -> What are the specific current alternatives your target customers use to forecast or avoid food waste, and why are they insufficient?

- **Buyer is too broadly defined — no beachhead segment** [MEDIUM] (buyer)
  'Independent restaurants' is a broad category with huge variance in size, tech-savviness, and buying power; the sales and product requirements for a single chef-run cafe vs. a multi-unit indie group differ dramatically. Without a clear initial customer profile you can't optimize onboarding, pricing, or channel. This increases the risk you'll build the wrong product features or target the wrong acquisition channels.
  -> Which precise buyer persona and subsegment (size, tech stack, POS, cuisine, monthly order volume) is your initial beachhead and why will they adopt first?

### execution_risk

The idea is directionally sensible but several concrete execution risks threaten the ability to build a shippable product. The most urgent technical blocker is that restaurants rarely record labelled waste outcomes, so an ML model trained only on sales/inventory may be impossible to validate. Beyond that, integrating heterogeneous POS/inventory systems, an underspecified go-to-market plan, an unsupported price point, unclear team capacity, and unaddressed data-compliance requirements are likely to delay or block shipping.

- **No ground-truth waste labels — model may be untrainable or un-validated** [CRITICAL] (assumptions)
  You plan to predict food waste from historical sales and inventory, but you do not state where labelled outcomes (actual waste quantities by item/day) will come from. Independent restaurants rarely track waste precisely, so there may be no target variable to train or evaluate a predictive model. Without a plan to collect or approximate ground truth, the core modeling effort is likely to fail or produce meaningless metrics.
  -> Where will you get reliable, item-level waste labels for training and validation, and what is the cheapest way to collect an initial labeled dataset from real restaurants?

- **Integration hell: extracting usable data from diverse POS/inventory systems** [HIGH] (assumptions)
  Independent restaurants use many different POS, inventory, and bookkeeping systems (or none), export formats vary, and some data is manual/paper. Building and maintaining dozens of connectors plus handling dirty/missing data is a large engineering and ops burden that is not acknowledged. Expect long development time per integration and ongoing break-fix support unless you limit scope or use a manual data-onboarding approach early.
  -> Which POS/inventory systems will you support first, and how will you ingest data from restaurants that don't have consistent digital exports without building many custom connectors?

- **Direct outreach plan is underspecified and will not scale without sales/onboarding ops** [HIGH] (acquisition)
  Saying you'll acquire customers via direct outreach to restaurant owners omits conversion mechanics: who conducts demos, handles technical onboarding, or addresses data extraction issues. Independent restaurants are time-poor and skeptical of new tools; converting them will require hands-on support or partnerships, which means more people/time than implied. Relying solely on founder outreach risks very slow, high-cost customer acquisition and stalled pilots.
  -> What is your concrete outreach playbook (channels, messaging, expected conversion and onboarding steps) and who will handle demos, technical onboarding, and support for pilot customers?

- **Team size and capabilities vs. scope are unspecified — likely underestimated work** [MEDIUM] (assumptions)
  The doc lists no team or roles but expects an ML product plus integrations, UI, and customer acquisition. Building an end-to-end, reliable product (connectors, model, dashboard, onboarding) is typically >6 months for a small team; a solo founder will struggle to do all engineering, data wrangling, and sales. This mismatch will delay shipping or force scope cuts that change the product fundamentally.
  -> Who is on the team today (engineering, data, product, sales) and what is a realistic MVP scope and timeline given that headcount?

- **Price point (£79/mo) is asserted with no evidence or value metric** [MEDIUM] (pricing)
  You propose £79/month but provide no evidence that independent restaurants will pay that for waste predictions or that the product delivers measurable savings that justify the fee. Without tests of willingness-to-pay, you risk building features that don't match perceived value. The pricing also affects acquisition strategy and churn but is not tied to any metric (waste reduction percentage or ROI).
  -> How did you arrive at £79/month and what inexpensive experiment will you run to validate that restaurants will pay that price for the promised value?

- **Data privacy and security / regulatory handling is not addressed and could block pilots** [MEDIUM] (assumptions)
  Sales and inventory data can include personal data and sensitive commercial information; GDPR and data-security expectations will influence whether restaurants will share raw data. There is no plan for consent, data minimization, hosting location, or security controls. Absent a simple, compliant data-handling policy, potential pilot customers or partners may refuse access or legal teams may block integrations.
  -> What specific data will you ingest, where will it be stored/processed, and how will you ensure GDPR-compliant, secure handling for early customers?

### evidence_audit

Evidence base: Weak. This is an idea-stage plan with a stated product and price but no pilots, customers, or unit-economics. The most important remaining issue is the lack of measured demand and supporting unit economics (pricing validation, CAC/churn/LTV) to justify revenue assumptions.

- **No evidence restaurants will buy this (no pilot or purchase commitments)** [HIGH] (demand_evidence)
  The document gives no measured demand: no pilot, no trial results, no signed letters of intent or paying customers. At idea stage this is the primary load-bearing gap — without demonstrating even a few customers, the whole revenue model is hypothetical. The founder should show real conversion numbers (contact → trial → paid) from independent restaurants before scaling assumptions are used.
  -> Provide results from a pilot or commercial test (e.g., at least 3–5 independent restaurants with documented trials or paid subscriptions) showing actual uptake or signed commitments at any price.

- **Price point (£79/mo) is unsupported and may not reflect value to restaurants** [HIGH] (pricing)
  The plan states customers pay £79/month but cites no willingness-to-pay evidence or ROI calculation. £79/mo equals £948 per customer per year; the author must show that predicted or measured waste reduction delivers >£948/year in value (or other justification). Without an ROI link, the price is an unsupported assumption and a load-bearing input.
  -> Show the quantitative basis for £79/mo: either (a) pilot/survey data indicating willingness to pay that amount, or (b) a calculation from measured waste-reduction per restaurant (in £/year) demonstrating the service returns >£948/year net benefit.

- **Key financials (CAC, churn, LTV) are missing so unit economics are unknowable** [HIGH] (key_numbers)
  With only a price point, we can compute revenue per customer = £79×12 = £948/year, but profitability depends on CAC and churn/LTV which are not stated. These are load-bearing numbers: without them you cannot assess marketing spend tolerance, payback period, or scale feasibility. The plan cannot be evaluated financially until these are provided or bounded.
  -> Provide target and evidence-backed figures for customer acquisition cost (CAC), expected annual churn (or retention), and resulting lifetime value (LTV), or explain the acceptable LTV:CAC ratio you are targeting and why.

- **Acquisition approach 'direct outreach' has no funnel metrics or conversion assumptions** [MEDIUM] (acquisition)
  The channel is stated but there are no unit economics or conversion rates for outreach → demo → trial → paid. For outreach-heavy early sales, concrete funnel metrics (contacts needed per paying customer, time to close) are essential to estimate effort and CAC. At idea stage this is a testable gap that should be resolved before committing to growth targets.
  -> Provide a tested outreach funnel showing: number contacted → meetings booked → trials started → conversions to paid, or at minimum reasonable benchmark conversion rates and how you'll validate them in a pilot.

- **No comparison to current alternatives or clear differentiation** [MEDIUM] (alternatives)
  The document does not state what restaurants currently use to manage waste (manual counts, POS reports, existing SaaS) nor why they would switch to this AI predictor. Without identifying alternatives and the measurable advantage (cost saved, time saved, accuracy), it's unclear why customers would adopt and pay for the product.
  -> List the current alternatives independent restaurants use to predict/manage waste and provide one concrete metric showing how your solution improves on them (e.g., % reduction in over-ordering, £ saved per week) or how you'll test this in pilot trials.


## Selected questions

- **differentiation**: Why would customers choose this over the alternatives?
  - why we're asking: adversarial_competitor / No defensible differentiation — trivial for incumbents to replicate [critical]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / The £79/month price is unsupported by willingness-to-pay evidence [high]
  - why we're asking: unit_economics / Listed price (£79/mo) has no evidence of willingness-to-pay [high]
  - why we're asking: adversarial_competitor / Pricing is fragile — larger players can undercut or bundle cheaply [high]
  - why we're asking: execution_risk / Price point (£79/mo) is asserted with no evidence or value metric [medium]
  - why we're asking: evidence_audit / Price point (£79/mo) is unsupported and may not reflect value to restaurants [high]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Direct outreach to owners is assumed to be an effective acquisition channel [high]
  - why we're asking: unit_economics / CAC and channel economics are undefined for direct outreach [high]
  - why we're asking: adversarial_competitor / GTM relies on one expensive channel (direct outreach) that won't scale [high]
  - why we're asking: execution_risk / Direct outreach plan is underspecified and will not scale without sales/onboarding ops [high]
  - why we're asking: evidence_audit / Acquisition approach 'direct outreach' has no funnel metrics or conversion assumptions [medium]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No estimate of cost to serve one restaurant (compute, storage, support, payments) [high]
  - why we're asking: unit_economics / Gross margin at scale vs. today is unspecified [medium]
  - why we're asking: unit_economics / No payback period or unit economics sensitivity analysis [medium]
  - why we're asking: evidence_audit / Key financials (CAC, churn, LTV) are missing so unit economics are unknowable [high]

## Answer given

**differentiation**: I haven't worked out a clear difference from existing inventory tools yet.

Skipped: pricing, acquisition, key_numbers

## Refined critique

### adversarial_competitor

This idea is under-specified and easy to neuter with a few pragmatic moves. The founder admits no differentiation, no tested demand, and no go-to-market plan — which means a well-funded incumbent can replicate the core promise (simple waste forecasting) as a feature, bury it in an existing product, and use distribution and pricing to make the standalone product irrelevant. The fastest kill: ship a basic predictive-waste dashboard as a free or low-cost add-on inside an existing inventory/POS channel and use existing customer relationships, SEO/content, and channel partners to steal early adopters.

- **No differentiation — core promise is copyable in a day or two** [HIGH] (differentiation)
  Founder concedes they haven't worked out how this differs from existing inventory tools. Predicting waste from sales/inventory is a narrow technical claim that any incumbent inventory or POS vendor can implement as an incremental feature or plug‑in. The cheapest neutralizer: ship a simple per-item forecast + suggested par levels as an add‑on or free feature in an existing suite and communicate immediate ROI with a few case studies.
  -> What specific algorithmic, data, or workflow advantage prevents a large incumbent from shipping an equivalent predictive-waste feature as an add-on?

- **No evidence customers want or will pay for this** [HIGH] (demand_evidence)
  There is no demand testing, pilot customers, or user interviews described — only a price assumption. Without evidence that independent restaurants will change behavior for a subscription, incumbents can preempt by running quick pilots with their existing customers to validate the same claim. A few 10–20 pilot installs by a larger player will produce case studies that crush a pre-product entrant's credibility.
  -> Who has validated that independent restaurants will pay £79/month for a predictive-waste tool, and what conversion/retention did those pilots show?

- **Go-to-market is undefined and easy to outmuscle** [HIGH] (acquisition)
  Founder plans 'direct outreach' but gives no acquisition funnel, channels, or CAC estimates. A well-funded competitor can weaponize existing distribution (installed base, reseller channels, app marketplaces, SEO/blog content, and sales teams) to reach restaurants at far lower marginal cost and bundle the feature into an existing product. That distribution advantage makes the founder's direct outreach a nonstarter unless they prove an early channel fit.
  -> Which specific channels and quantified outreach plan will reach a defensible cohort of paying restaurants faster than an incumbent's existing channels?

- **Unclear who actually pays and why £79 is the right price** [MEDIUM] (pricing)
  The doc lists £79/month but also says 'who pays' is unknown. Is the buyer the owner, head chef, or the franchise operator? Without the buyer persona and willingness-to-pay, price positioning is arbitrary. Incumbents can undercut or bundle the feature into existing products making £79 untenable for a standalone product aimed at cash‑tight independents.
  -> Who is the paying buyer (owner/operator, chef, corporate) and what evidence supports £79/month as acceptable relative to their margin sensitivity?

- **Missing the key numbers that govern viability** [MEDIUM] (key_numbers)
  No unit economics, TAM, conversion, retention, or CAC are provided. These load-bearing numbers determine whether a standalone SaaS makes sense versus being a feature. A competitor with these numbers can model profitable promo pricing or bundling tactics to make a standalone offer uncompetitive.
  -> List the core metrics the plan relies on (CAC, conversion from outreach, LTV, churn, pilot reduction in waste) and whether each is measured, estimated, or unknown.


## Refinement meta

- Lenses re-run: adversarial_competitor
- Lenses not re-run: pre_mortem, unit_economics, execution_risk, evidence_audit
- Gaps filled: ['differentiation']
- Gaps skipped: ['pricing', 'acquisition', 'key_numbers']

## Reuse check

Re-sending the same refinement token refused with 409: yes
