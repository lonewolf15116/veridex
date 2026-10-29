# T01-dental-saas

**Stage:** building

## Input

We're building AI-powered scheduling software for independent US dental clinics. We believe a no-show prediction model could reduce missed appointments by 30%, and plan to charge $299 per location per month. Our initial acquisition strategy is a two-person outbound team, targeting 50 paying clinics within six months.

**Reviewer expectation:** asks for validation of the 30% figure, data access, pricing and acquisition without claiming pilots occurred; after refinement acknowledges 30% is a target and does not treat three conversations as proof of demand.

## First critique

### pre_mortem

The plan rests on multiple interdependent assumptions that are unstated and untested: that clinics will legally and operationally provide the data needed to build the model; that a no-show risk score by itself (or with simple clinic actions) will cut missed appointments ~30%; and that clinics will pay $299/location/month and can be acquired via two-person outbound within six months. If any one of these core assumptions fails, the product either cannot be built, cannot produce the promised impact, or cannot find customers.

- **No proof clinics will allow HIPAA-compliant access to the patient/appointment data needed** [CRITICAL] (assumptions)
  The strategy assumes access to appointment and patient-level data to train and run an AI model but does not state how that data will be obtained, whether clinics will sign Business Associate Agreements (BAAs), or whether practice management vendors will permit integrations. If clinics cannot legally or operationally provide the required data streams, the core model cannot be trained or deployed as described. This is a hard stop: without compliant data access there is no AI product.
  -> Can target clinics and their vendors legally and operationally provide the necessary appointment/patient data under HIPAA-compliant BAAs and integrations to train and run the model?

- **Conflating prediction with impact: 30% reduction in missed appointments is unproven** [HIGH] (assumptions)
  The thesis claims a no-show prediction model will reduce missed appointments by 30%, but no evidence or mechanism is provided for how predictions translate into effective actions (e.g., targeted reminders, overbooking policies) that achieve that magnitude of reduction. Prediction accuracy alone does not guarantee behavioral change by patients or operational change by clinics. If high-quality risk scores do not lead to scalable, clinic-implementable interventions that materially change behavior, the product fails to deliver its primary value proposition.
  -> When risk scores are delivered to clinics along with realistic interventions, do real clinics achieve ~30% fewer missed appointments in a controlled pilot?

- **Pricing is assumed, not validated: $299/month per location may not match willingness to pay** [HIGH] (pricing)
  Charging $299 per location per month is asserted without evidence that independent dental clinics value this feature at that price or prefer this pricing model to alternatives (one-off fees, per-appointment fees, bundled PMS features). Independent clinics often have tight budgets and prefer low-friction, low-cost solutions; without willingness-to-pay data the revenue plan is speculative. If clinics balk at the price, landing even a small pilot will be difficult.
  -> Will a representative sample of independent dental clinics commit to paying $299/month per location for this service versus existing reminder/manual processes or cheaper alternatives?

- **Acquisition channel assumption: two-person outbound can hit 50 paying clinics in six months** [HIGH] (acquisition)
  The plan assumes a two-person outbound team can reach decision-makers, communicate the product's value, and convert 50 paying clinics in six months, but provides no evidence of sales cycle length, response rates, or conversion rates for this market. Independent clinics may have decentralized purchasing, slow decision-making, or require trials and references, making outbound less effective than assumed. If outbound falls short, customer acquisition stalls and the strategy cannot validate product-market fit.
  -> Can a two-person outbound team reliably contact decision-makers and convert enough clinics to reach 50 paying customers within six months based on pilot outreach metrics?

- **Model generalizability across diverse independent clinics is assumed** [MEDIUM] (assumptions)
  The document implicitly assumes a model trained on some data will generalize to other independent dental clinics, but clinics vary in patient demographics, scheduling rules, reminder practices, and software systems. If the model needs per-clinic training or adaptation, the product complexity and data requirements grow and the value proposition changes. The plan does not state whether a single model or per-clinic models are envisioned.
  -> Will a single no-show prediction model trained on pooled data meet accuracy thresholds across diverse clinics, or will each clinic require bespoke training/adaptation?

- **Misread of alternative solutions and revealed preferences** [MEDIUM] (alternatives)
  There is no evidence of what clinics currently use to reduce no-shows (automated reminders, phone calls, deposits, overbooking) or why they would replace those methods with an AI-driven scheduler. The founding statement risks confusing expressed interest in reducing no-shows with actual willingness to adopt an AI tool that changes workflows. If current, cheaper, or simpler remedies are 'good enough' in revealed behavior, adoption will be low.
  -> What do target clinics actually do today to reduce no-shows, and why would they switch to an AI-driven scheduling solution instead of sticking with those practices?

- **Implicit integration dependency with practice management systems is unstated** [LOW] (assumptions)
  The strategy does not state whether the product requires deep integration with practice management systems to read schedules and send interventions, or if it can operate via manual uploads/CSV exports. If integrations are required but harder than assumed, deployment and adoption become frictioned. This gap affects speed of pilots but is not necessarily fatal if addressed early.
  -> Can the product access scheduling data and send reminders through the major practice management systems used by target clinics with acceptable technical effort and permission?

### unit_economics

The document states price ($299/location/mo), a 30% no-show reduction claim, and a two-person outbound plan to land 50 clinics, but provides no unit-costs, CAC math, compliance plan, or evidence of willingness-to-pay. Key inputs for LTV, payback, and gross margin are missing, so the revenue and margin claims are unsupported. Before launch the team must (1) validate willingness-to-pay with price tests, (2) model CAC using realistic outbound conversion metrics, and (3) itemize per-location serving costs including HIPAA/compliance.

- **No plan for HIPAA / PHI compliance — a potential blocker and material cost** [CRITICAL] (assumptions)
  Scheduling and no-show prediction will almost certainly require handling protected health information (PHI). The doc contains no HIPAA/BAA, security, or legal compliance plan; those are non‑optional and add measurable engineering, hosting, legal, and insurance costs. Ignoring this changes unit economics (higher fixed and per-customer costs) and may prevent selling to clinics until solved.
  -> How will you handle PHI and HIPAA (BAA, encryption, logging, audits, breach liability) and what is the expected incremental monthly cost per location to meet compliance?

- **Price ($299/mo) is unsupported by any willingness-to-pay evidence** [HIGH] (pricing)
  The $299/month per-location price is asserted without cited customer interviews, pilots, or price tests. There is no breakdown of what $299 buys the clinic vs alternatives, so LTV and margin projections are baseless. If clinics won’t pay this price, CAC and payback calculations (which are absent) will fail.
  -> What evidence (surveys, paid pilots, signed LOIs, price‑sensitivity tests) shows clinics will pay $299/location/month rather than a lower price or a per-appointment fee?

- **CAC and go-to-market channels are unspecified and likely underestimated** [HIGH] (acquisition)
  A two-person outbound team is the only acquisition plan; no conversion rates, outreach volume, time-per-sale, or expected CAC are given. Selling to independent dental clinics can involve slow sales cycles and significant outreach time per closed deal, so CAC could be many months of revenue per customer unless proven otherwise.
  -> What is the detailed outbound funnel (outreach per rep per week, expected response and demo rates, demo→close %), and the implied CAC and sales cycle in months?

- **Per-location cost-to-serve (compute, storage, support, payments) is missing** [HIGH] (key_numbers)
  There is no breakdown of marginal costs: model inference cost (real-time predictions), data storage and backups, retraining, monitoring, customer support/onboarding, and payment processing fees. Without per-customer unit costs you cannot compute gross margin or test price viability.
  -> Provide a per-location/month estimate for model inference, storage, backups, support time, onboarding amortization, and payment processing fees (or explain why these are negligible).

- **No gross-margin or scale economics — unclear if price covers costs at scale** [MEDIUM] (key_numbers)
  The doc claims benefit but provides no gross-margin projections today vs at scale (50, 500, 5,000 locations). Economies of scale for model serving or support could help, but without numbers it's unknown whether margins are healthy or will flip negative as you add compliance and support.
  -> What is your projected gross margin per location at 50, 500, and 5,000 paying locations (including compliance and support costs)?

- **No LTV, churn, payback-period, or hidden operational costs modeled** [MEDIUM] (assumptions)
  There are no assumptions for retention/churn, refunds/chargebacks, fraud, or customer support escalations; LTV and payback period are therefore undefined. These inputs determine whether a likely CAC can be recovered and whether the business is financially viable.
  -> What are your assumed monthly churn, average contract length, refund/chargeback rate, and resulting LTV and CAC payback period?

### adversarial_competitor

This product is an undifferentiated ML layer on top of dental scheduling with an unproven 30% impact claim and a high per-location price. A well-funded incumbent can neutralize it cheaply by shipping a basic risk-score + reminder bundle, bundling it into existing products, and exploiting deeper distribution, partnerships, and trust to undercut adoption.

- **No defensible moat — the "predictive" bit is easy to replicate** [HIGH] (differentiation)
  Founder leans entirely on a no-show prediction model as the unique value. That model is not described as proprietary, nor is any exclusive data source or technical barrier claimed. An incumbent with access to appointment logs can reproduce a usable risk score or simple heuristics within weeks and ship the same feature to existing customers.
  -> What proprietary data, integration, or technical advantage prevents an incumbent from reproducing your predictive score in 30–90 days?

- **Pricing exposed — $299/location/mo is easy to undercut or bundle away** [HIGH] (pricing)
  Charging $299 per location per month for a single feature creates a large arbitrage opportunity: incumbents can include a similar risk score and reminder automation as a free or low-cost add-on for their installed base or wholesale-bundle it into payments/insurance channels. The plan gives no evidence that independent clinics will pay a standalone $299 premium.
  -> How did you validate willingness to pay $299/location/mo given incumbents can bundle the same capability into their existing offerings?

- **Key integration / data access assumption unstated and fragile** [HIGH] (assumptions)
  A predictive scheduling product requires reliable, real-time access to appointment and patient-history data from practice management systems. The document states no integrations, pilot partners, or permissions; incumbents or EHR vendors control those channels and can block or replicate integrations. Without confirmed API access, the core product cannot function.
  -> Which practice-management systems have you confirmed API access with (or signed partnerships for), and can they provide the historical and live appointment data your model needs?

- **Impact claim (30% reduction) has no supporting evidence or pilot plan** [MEDIUM] (demand_evidence)
  The assertion that a no-show model will reduce missed appointments by 30% is stated as a belief with no pilot, retrospective evaluation, or baseline no-show rates. That gap is killable: incumbents can run quick A/B pilots with existing customers to show equal or better impact and beat the startup to market.
  -> Can you produce a retrospective validation or a one-month pilot with 5–10 clinics demonstrating the claimed 30% reduction on real appointment data?

- **Go-to-market plan is tiny and easy to out-distribute** [MEDIUM] (acquisition)
  A two-person outbound team targeting 50 clinics is insufficient against competitors who can push features to thousands of existing customers, leverage SEO content, app stores/marketplaces for practice-management systems, and partner with dental associations or insurers. Distribution, not the model, is the lever that wins here.
  -> Beyond the two-person outbound effort, which channels (integrations, marketplaces, associations, SEO or partner pipelines) are validated to scale acquisition to hundreds of clinics?

### execution_risk

The plan underestimates the legal, data and integration work required to build a production-ready no-show predictor for US dental clinics and overestimates a two-person outbound team's ability to both acquire and onboard 50 clinics in six months. The biggest shipping risks are regulatory/compliance blockade around PHI, per-clinic integration and data scarcity/cold-start for the model. Several sequencing and GTM assumptions (pilot data, connector effort, pricing validation, support capacity) are unstated and likely to derail timelines and conversion.

- **HIPAA / PHI compliance is unaddressed and can legally block sales** [CRITICAL] (assumptions)
  Predicting no-shows requires appointment and likely patient-level data that is PHI under US law. The document contains no plan for HIPAA compliance, BAA signings, secure hosting, encryption, audits, or legal sign-offs — clinics will not hand over data (or allow you to process it) without these in place. Failing to solve this before outbound sales will prevent pilots and paid deployments and could create legal exposure.
  -> How will you legally and operationally obtain, store, and process appointment/patient data from US dental clinics (BAA, HIPAA controls, encryption, audit timeline) before you start selling or deploying?

- **Per-clinic integration burden will explode engineering and onboarding time** [HIGH] (assumptions)
  Dental clinics use multiple practice-management systems (Dentrix, Eaglesoft, Open Dental, others) and often require custom connectors or manual CSV exports; the doc assumes a generic integration without listing systems or connector plans. Each new connector can take weeks of engineering, testing, and legal review (BAA), making rapid onboarding of 50 clinics infeasible with current staffing. Underrating this work will create a long tail of slow deployments and angry early customers.
  -> Which practice-management systems are you integrating with first, and what is your engineering/time/cost estimate per connector and per clinic onboarding?

- **Model needs historical labeled data (cold-start) — risk of poor accuracy at launch** [HIGH] (assumptions)
  The promised 30% no-show reduction is model-dependent but there's no plan showing access to historical appointment/no-show labels. Individual clinics may not have enough labeled history for reliable per-location models, and a centralized model may not generalize across clinics. Without an explicit pilot dataset and accuracy milestones, you risk shipping a product whose predictions don't meaningfully reduce no-shows.
  -> Can you secure historical appointment/no-show data from at least one clinic to validate model accuracy and the 30% reduction claim before broad development?

- **Two-person outbound GTM won't scale to acquire and onboard 50 paying clinics in 6 months** [HIGH] (acquisition)
  The acquisition plan is a two-person outbound team targeting 50 paying clinics in six months but gives no funnel metrics, conversion assumptions, demo/onboarding capacity, or implementation bandwidth. Even if leads convert, each closed customer will need onboarding, integration, BAA execution, and support — work that will overwhelm two people. This will delay revenue and create poor customer experiences.
  -> What are your assumed outreach->demo->pilot->paid conversion rates, and how many full-time sales and technical onboarding staff do you need to realistically close and deploy 50 clinics in six months?

- **Sequencing: building product before securing pilot data/connectors wastes engineering effort** [MEDIUM] (acquisition)
  The plan implies building the AI-powered product now but does not require a pilot clinic or exported historical data before development. If you build connectors and a model before proving data availability and predictability, you'll likely rework code and integrations. A cheap pilot with CSV exports or one clinic can validate feasibility much faster than full engineering.
  -> Will you run a short pilot (CSV exports from one clinic) to validate predictability before building production connectors and UX?

- **Price point and post-sale support expectations are unvalidated** [MEDIUM] (pricing)
  You state $299/location/month but provide no evidence that clinics will accept that price or that onboarding/support costs per location are sustainable. High onboarding and integration costs per clinic can kill conversions and margins if the price isn't validated. Without at least an LOI or paid pilot at the target price, revenue forecasts and staffing plans are guesses.
  -> Have you validated willingness to pay $299/month (e.g., LOI or paid pilot) and estimated the real onboarding/support hours and cost per location at that price?

### evidence_audit

Evidence base: Weak. The plan is pre-launch with no measured pilots or customer revenue; core effectiveness and pricing assumptions are unsupported. The most important gap is the unsupported 30% no-show reduction and the absent buyer-backed ROI/pricing justification.

- **Core claim of 30% no-show reduction is unsupported** [HIGH] (assumptions)
  You state a 30% reduction in missed appointments but provide no pilot, backtest, or source for that effect size. That number is load-bearing: expected customer ROI and willingness-to-pay depend directly on it. Without evidence from real clinics (n and context), we cannot know if a model can reach 30% in the noisy operational environment of independent dental practices.
  -> Provide the empirical evidence (pilot results, A/B test, backtest or published source) showing a 30% reduction in no-shows for clinics like your target customers, including sample size, baseline no-show rate, and how reduction was measured.

- **Price $299/mo has no buyer-backed justification** [HIGH] (pricing)
  The plan sets $299 per location per month but gives no ROI calculation or willingness-to-pay data from dentists. Whether clinics will pay $299 depends on the monetary value of avoided no-shows per clinic (baseline no-show rate, average appointment revenue, and elasticity). Without that, the price is an unsupported assumption.
  -> Show a per-clinic ROI model that converts a 30% reduction in no-shows into dollars saved (with baseline no-show rate and average appointment value) and demonstrate that the net benefit justifies $299/mo for a typical independent US dental clinic.

- **Acquisition plan missing CAC and conversion math; implied CAC example** [HIGH] (key_numbers)
  You target 50 paying clinics in six months with a two-person outbound team but give no spend or conversion assumptions. Conservatively, at $5k fully loaded per rep per month: 2 reps × 6 months × $5,000 = $60,000; implied CAC = $60,000 / 50 = $1,200. First-year revenue per customer = 299 × 12 = $3,588, so payback could be ~4 months only if churn is low — you haven't provided churn or close-rate assumptions.
  -> Specify planned fully-loaded rep cost, expected outbound conversion rate (leads → paying), and resulting CAC; if you use different spend assumptions, show the math that yields CAC and the expected payback period versus LTV.

- **No evidence that target buyers will buy or who the decision-maker is** [MEDIUM] (buyer)
  ‘Independent US dental clinics’ is a broad buyer label; you haven't stated which subset (solo owners, multi-location independents) or who signs the check (practice owner, office manager). Buyer role and procurement process affect sales cycle and conversion rates — critical for a two-person outbound plan targeting 50 clinics in six months.
  -> Identify the specific buyer persona(s) (title, clinic size, baseline no-show rate) you will target and provide evidence (surveys, interviews or pilot commitments) that these personas have the authority and willingness to purchase at your price point.

- **No funnel/conversion assumptions for outbound required to hit 50 customers** [MEDIUM] (acquisition)
  You name team size and a customer target but provide no funnel metrics (outreach → booked demo → trial → paid). Without conversion rates or required outreach volume, the sales effort is unquantified and risk of not hitting 50 customers is unknown. This gap prevents validating whether two reps in six months is realistic.
  -> Provide the assumed outbound funnel conversion rates (e.g., outreach → response, response → demo, demo → trial, trial → paid) and compute the number of outbound touches required per rep per month to reach 50 customers in six months.


## Selected questions

- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Acquisition channel assumption: two-person outbound can hit 50 paying clinics in six months [high]
  - why we're asking: unit_economics / CAC and go-to-market channels are unspecified and likely underestimated [high]
  - why we're asking: adversarial_competitor / Go-to-market plan is tiny and easy to out-distribute [medium]
  - why we're asking: execution_risk / Two-person outbound GTM won't scale to acquire and onboard 50 paying clinics in 6 months [high]
  - why we're asking: execution_risk / Sequencing: building product before securing pilot data/connectors wastes engineering effort [medium]
  - why we're asking: evidence_audit / No funnel/conversion assumptions for outbound required to hit 50 customers [medium]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Pricing is assumed, not validated: $299/month per location may not match willingness to pay [high]
  - why we're asking: unit_economics / Price ($299/mo) is unsupported by any willingness-to-pay evidence [high]
  - why we're asking: adversarial_competitor / Pricing exposed — $299/location/mo is easy to undercut or bundle away [high]
  - why we're asking: execution_risk / Price point and post-sale support expectations are unvalidated [medium]
  - why we're asking: evidence_audit / Price $299/mo has no buyer-backed justification [high]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / Per-location cost-to-serve (compute, storage, support, payments) is missing [high]
  - why we're asking: unit_economics / No gross-margin or scale economics — unclear if price covers costs at scale [medium]
  - why we're asking: evidence_audit / Acquisition plan missing CAC and conversion math; implied CAC example [high]
- **differentiation**: Why would customers choose this over the alternatives?
  - why we're asking: adversarial_competitor / No defensible moat — the "predictive" bit is easy to replicate [high]

## Answer given

**acquisition**: Our plan is outbound outreach by the two of us; we have not yet tested whether it works.

Skipped: pricing, key_numbers, differentiation

## Refined critique

### unit_economics

The document states price ($299/location/month) and an outbound plan but contains almost no unit economics. Key inputs needed to judge viability — cost to serve per clinic, validated willingness-to-pay, CAC and conversion assumptions, gross margin, and payback — are missing. Before launch, the founder must quantify these or run cheap tests to measure WTP and outbound conversion rates.

- **No cost-to-serve (compute, storage, support, payments) provided** [HIGH] (key_numbers)
  The plan gives a list price but no breakdown of the per-location monthly operating costs (model inference, data storage, backups, monitoring, customer support, payment fees). Without these you cannot calculate gross margin or determine whether $299 covers ongoing costs at scale.
  -> What is your detailed estimated monthly cost to serve one clinic (compute, storage, backups, monitoring, support headcount allocation, and payment processing fees)?

- **Price ($299/mo) is unvalidated — willingness-to-pay unsupported** [HIGH] (pricing)
  You state a $299/month price and a 30% no-show reduction claim but provide no evidence clinics will pay that amount or how $299 maps to value delivered (cost savings from reduced no-shows). Willingness-to-pay is asserted, not demonstrated.
  -> What evidence (surveys, paid pilots, pilot revenue, customer interviews quantifying savings) supports clinics paying $299 per location per month?

- **CAC and outbound channel economics are unspecified** [HIGH] (acquisition)
  The acquisition plan is 'two-person outbound' targeting 50 clinics in six months but there are no assumptions about outreach volume, conversion rate, salaries/commissions, tooling, or per-account CAC. At this price point CAC could easily exceed acceptable payback without quantification.
  -> What is your projected CAC per paying clinic (including recruiter/sales salaries, tools, outreach volume and conversion rate) and the timeline to close a lead?

- **Gross margin, LTV and payback period are not modeled** [MEDIUM] (key_numbers)
  There is no unit-economics model showing gross margin at scale, customer lifetime (churn), LTV, or months-to-payback of CAC. Without those, you cannot assess whether the business achieves acceptable payback or whether the model scales profitably.
  -> Please provide a simple unit-economics table: expected churn, LTV, gross margin, CAC, and months to recover CAC under a baseline scenario.

- **Hidden operational/compliance costs (HIPAA, refunds, fraud) not considered** [MEDIUM] (assumptions)
  Dental appointment data may be PHI triggering HIPAA-like obligations; monitoring, security, legal, and audit costs (and potential insurance) can be material. Also absent are assumptions about refunds, chargebacks, false positives from prediction models, or fraud which affect support and cost-to-serve.
  -> Do you plan to handle PHI and have you estimated compliance/security/insurance and extra support costs (and potential refund/chargeback rates) in your unit economics?

### execution_risk

The plan misses several concrete execution blockers that will stop shipping: patient-data/HIPAA compliance is unaddressed (a legal blocker), there's no route to collect the historical, standardized appointment data needed to train a predictive model, and integrating with many dental practice management systems is treated as trivial. Operationally, two founders running outbound and building integrations/models is under-resourced, and pricing/sequence assumptions (build model before pilots) are unvalidated and likely to delay or derail launches.

- **No HIPAA / PHI compliance plan — legal blocker to onboarding clinics** [CRITICAL] (assumptions)
  You plan to ingest appointment and patient data but the doc has no HIPAA strategy: no Business Associate Agreement (BAA) plan, no specification of secure hosting, encryption, access controls, or breach processes. Clinics will refuse to share data or legal teams will block pilots without a signed BAA and audited controls, creating a hard stop before any data collection or deployment. This is not a future enhancement — it's a precondition to get data and paying customers.
  -> How will you achieve HIPAA-compliant data handling (BAAs, hosting, audits, breach plan) before any clinic integration or data ingestion?

- **No source or plan for the labeled historical data required to train the model** [HIGH] (assumptions)
  The 30% no-show reduction claim depends on a predictive model but there's no plan for acquiring sufficient, standardized historical appointment records (no-shows, cancellations, reminders, patient attributes). Dental practices hold fragmented data with inconsistent fields; without secured datasets you can't train or validate the model and will likely waste effort training models that don't generalize. This will delay an MVP or produce an unusable product.
  -> Where exactly will you obtain the standardized, labeled appointment datasets (fields and minimum record counts) needed to train and validate a no-show model prior to launch?

- **Integration with many practice management systems is underestimated** [HIGH] (assumptions)
  You assume you can plug into clinics to get appointment data, but US dental clinics use many PMS vendors with differing APIs, exports, or none at all. Building and maintaining per-vendor connectors (or resorting to screen-scraping) requires substantial engineering and legal work for each integration, adding months per vendor and blocking onboarding. Overlooking this creates a bottleneck: product exists but can't connect to customers' systems.
  -> Which PMS vendors will you target first and what are the concrete technical and legal integration steps and estimated engineering hours per vendor?

- **Two-person outbound + build team is under-resourced to hit 50 paying clinics in 6 months** [HIGH] (acquisition)
  You plan a two-person outbound team to land 50 paying clinics while also building integrations and the model. Each clinic will need outreach, legal/contract work (BAAs), demos, pilot setup, and often custom integration—work that typically takes weeks per clinic. The founders will be a bottleneck; hiring or delegating is not accounted for, making the 6-month target unrealistic.
  -> What is your assumed onboarding throughput per founder per month (sales, legal, onboarding, integration) and how will you scale if it proves insufficient?

- **Sequencing: building the model before running live pilots** [MEDIUM] (assumptions)
  The plan implies significant model development up front rather than validating the effect with lightweight pilots or rule-based approaches. Without a small number of live pilots to confirm data access, feature quality, and impact, you risk engineering a sophisticated model that can't be deployed or doesn't outperform simple heuristics. That wastes months and raises costs before you know the product works in real clinics.
  -> Can you run a 2–4 clinic pilot using simple rules or offline experiments to validate impact and data availability before training a production model?

- **Price ($299/location/mo) is asserted with no validation and may block sales** [MEDIUM] (pricing)
  Charging $299/location/month is stated but there's no evidence clinics will pay that, especially if onboarding requires integration fees or operational changes. If price is wrong, conversion will be low and lengthy negotiations will slow acquisition; this is an execution risk because sales cycles are longer and more hands-on than assumed.
  -> What evidence supports $299/month per location as an acceptable price to dentists (willingness-to-pay tests, comparable products, or pilot feedback)?


## Refinement meta

- Lenses re-run: unit_economics, execution_risk
- Lenses not re-run: pre_mortem, adversarial_competitor, evidence_audit
- Gaps filled: ['acquisition']
- Gaps skipped: ['pricing', 'key_numbers', 'differentiation']

## Reuse check

Re-sending the same refinement token refused with 409: yes
