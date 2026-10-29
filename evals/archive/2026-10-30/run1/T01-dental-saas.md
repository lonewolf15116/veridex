# T01-dental-saas

**Stage:** building

## Input

We're building AI-powered scheduling software for independent US dental clinics. We believe a no-show prediction model could reduce missed appointments by 30%, and plan to charge $299 per location per month. Our initial acquisition strategy is a two-person outbound team, targeting 50 paying clinics within six months.

**Reviewer expectation:** asks for validation of the 30% figure, data access, pricing and acquisition without claiming pilots occurred; after refinement acknowledges 30% is a target and does not treat three conversations as proof of demand.

## First critique

### pre_mortem

The plan hinges on several unvalidated assumptions that, if false, make the product unbuildable or unloved. The most dangerous gap is data access — without historical, labelled appointment/no-show data the ML model cannot be trained. Other high-risk assumptions are the claimed 30% reduction from prediction alone, willingness to pay $299/location/month, and that a two-person outbound team can acquire 50 paying clinics in six months. Additionally, it's unclear why clinics would adopt an add-on prediction layer over existing reminders and who the actual buyer/user is inside the clinic.

- **No evidence you can get the training data you need** [CRITICAL] (assumptions)
  The strategy assumes you can collect sufficient, clean historical appointment and no-show labels from independent dental clinics, but the document says nothing about data access, integrations, consent, or variation in record-keeping. If you cannot legally or practically access that data, the core ML feature cannot be developed as promised. This dependency is a hard blocker rather than a tuning problem.
  -> Do you have signed agreements or technically feasible integrations with clinics (or vendors) that will provide the historical, labeled appointment data needed to train and validate the no-show model?

- **Assumes prediction alone will cut missed appointments by 30%** [HIGH] (assumptions)
  The claim that a no-show prediction model will reduce missed appointments by 30% is presented without evidence about prediction accuracy, what interventions will follow predictions, or whether clinics will use those interventions reliably. Prediction does not equal outcome change: clinics must act on the signal and those actions must be effective. No pilot data, A/B test plan, or causal evidence is provided to support the 30% figure.
  -> What empirical evidence (pilot, randomized test, or validated proxy) shows that providing a no-show prediction plus the intended clinic intervention reliably reduces missed appointments by ~30%?

- **Pricing assumption ($299/location/month) is unvalidated** [HIGH] (pricing)
  Charging $299 per location per month is asserted with no buyer validation, willingness-to-pay testing, or linkage to measured value delivered. Independent dental clinics vary widely in size and margins; without evidence, this price could be too high (blocking adoption) or misaligned with buyer willingness. The document lacks price-sensitivity tests or a plan to justify ROI to purchasers.
  -> Have you tested willingness to pay and perceived ROI with target clinic decision-makers to validate $299/location/month is acceptable and competitive?

- **Acquisition plan (two-person outbound -> 50 paid in 6 months) is unproven** [HIGH] (acquisition)
  The funnel metrics, conversion assumptions, sales cycle length, and average deal complexity for independent dental clinics are not provided. A two-person outbound team may lack capacity or channels to reach decision-makers, especially if clinical stakeholders require pilots or integrations. There is no evidence the targeted outreach will translate into 50 paying locations within the timeline.
  -> What are the assumed outreach/contact, demo-to-trial, and trial-to-paid conversion rates and time-to-close that make 50 paying clinics in six months achievable with two outbound reps, and on what evidence are those assumptions based?

- **Unclear differentiation vs existing reminders and scheduling workflows** [MEDIUM] (differentiation)
  The document doesn't explain why clinics would adopt an extra prediction layer instead of using existing automated reminders, confirmations, or simple scheduling policy changes. If clinics perceive the feature as incremental to tools they already have (or as adding workflow friction), adoption will stall. No user research is cited that shows prediction-based interventions are preferred over current approaches.
  -> Why will clinics choose your prediction product over (or in addition to) their current reminder/scheduling workflows — what exact pain does it solve that they cannot solve today?

- **Buyer and user within the clinic are not specified** [MEDIUM] (buyer)
  ‘Independent US dental clinics’ is a broad category and the document does not identify the economic buyer or daily user (owner, office manager, front-desk staff, etc.). Different personas have different incentives and procurement processes; not specifying who will buy and who will act on predictions obscures validation needs. This increases the risk of building features for the wrong person.
  -> Who is the exact buyer and day-to-day user in the clinic (title and incentives), and what evidence do you have that this persona will adopt and rely on the product?

### unit_economics

The plan states a $299/month price and a target of 50 paying clinics in six months but provides no unit-costs, CAC, conversion or margin calculations. Without per-location cost-to-serve, validated willingness-to-pay, or an acquisition funnel/CAC estimate, you cannot compute gross margin, payback period, or viability at scale. First tests to run: validate $299 with paid pilot/price tests and run a small outbound experiment to measure lead->paid conversion and per-lead cost before building further.

- **No per-location cost-to-serve (compute, storage, support, payments) provided** [HIGH] (key_numbers)
  The document gives a $299/month price but lists no estimates for the recurring costs to serve a single clinic (cloud inference, model training amortization, data storage, backups, customer support staffing, payment processing fees). Without these inputs you cannot calculate gross margin or determine whether $299 covers ongoing costs at scale.
  -> What is your detailed monthly per-location cost breakdown (compute/inference, storage, backups, support FTE allocation, payment fees, and model retraining amortization)?

- **Willingness-to-pay not validated — $299 is unsupported** [HIGH] (pricing)
  Founder declares a $299/month price but provides no evidence (interviews, price experiments, pilots) that independent US dental clinics will pay that amount or that it’s the right pricing metric (per-location vs per-provider). The 30% no-show reduction claim is not tied to a demonstrated ROI that would justify $299.
  -> How did you validate clinics would pay $299/month — show the evidence (surveys with price sensitivity, signed pilots, or paid trials) tying $299 to realized ROI for clinics?

- **CAC and acquisition funnel are undefined and inconsistent with two-person outbound plan** [HIGH] (acquisition)
  The acquisition plan is 'two-person outbound targeting 50 paying clinics in six months' but contains no activity, conversion, or cost metrics (emails/calls per rep, response rate, demo-to-trial, trial-to-paid conversion). Without CAC and funnel metrics you cannot compute payback period or assess whether a two-person team can scale acquisition at this price point.
  -> What are your expected funnel conversion rates and resulting CAC (cost per paid clinic) based on outbound activity targets and channel benchmarks — and how many leads per rep per month must be sourced to hit 50 paying clinics?

- **Gross margin at scale vs today is unspecified** [MEDIUM] (key_numbers)
  No projections for gross margin today or at scale are given, so it's impossible to evaluate sustainability as you add locations. Key drivers (model inference cost per appointment, marginal support cost per new clinic, SaaS overhead) are missing, so margin compression or improvement scenarios are untested.
  -> Provide projected gross margin today and at 1k/10k locations with assumptions for variable and fixed costs that drive those margins.

- **Payback period and sensitivity to failure modes not calculated** [MEDIUM] (key_numbers)
  There is no payback analysis showing months to recover CAC from $299 MRR, nor sensitivity testing for lower conversion, higher churn, or higher support costs. Without this, you can't know how long capital is tied up or what breaks the economics.
  -> What is the calculated payback period on a new customer at your estimated CAC and LTV assumptions, and which parameter (CAC, churn, cost-to-serve) makes payback exceed 12 months?

- **Hidden operational costs (fraud, refunds, compliance, moderation, support) are not acknowledged** [LOW] (assumptions)
  No mention of likely recurring non-technical costs such as dispute/chargeback rates, refunds for missed predictions, HIPAA compliance costs for dental data, or higher-than-expected support needs as clinics onboard. These can materially alter unit economics if assumed negligible.
  -> Which operational and compliance costs have you estimated (HIPAA/legal, chargebacks/refunds, escalation/triage support) and how are they included in per-location margins?

### adversarial_competitor

This pre-launch AI scheduling product rests on an unproven 30% no-show reduction and a premium $299/month per location price, sold via a two-person outbound team. It is straightforward for a well-funded incumbent to neutralize by shipping a basic no-show risk score + automated reminders integrated into an existing practice-management or communication product, undercutting price and using existing distribution (users, SEO, app ecosystem, channel partners) to scale quickly. The founder has not shown demand, competitive alternatives, or a credible go-to-market — those gaps are the fastest levers to exploit.

- **No defensible differentiation vs existing reminders/PM systems** [HIGH] (differentiation)
  The document claims an AI no-show prediction model but gives no specifics on how this meaningfully outperforms simpler, widely-used approaches (e.g., automated SMS/email reminders, deposit requirements, double-booking heuristics, or basic rule-based scoring). Incumbent practice-management vendors or communication platforms can add a simple risk score + smarter reminder cadence and present it as the same benefit. Without a clear, hard-to-replicate technical or data moat, the product is easy to copy into established offerings.
  -> What specific predictive accuracy, feature set, or exclusive data will prevent established dental PM/communications vendors from replicating your value within weeks?

- **No evidence people will pay for a $299/location product** [HIGH] (pricing)
  Charging $299 per location per month is asserted without any evidence of willingness-to-pay, ROI calculations, or pilot results. Independent dental clinics vary in size and budgets; the founder offers no proof that a 30% reduction in no-shows will reliably translate to an economic case clinics will pay that price for. This makes the commercial thesis fragile and easy for competitors to exploit via trial offers or lower-priced alternatives.
  -> Can you show pilot data or a simple ROI model proving clinics will pay $299/month based on reduced cancellations and incremental revenue?

- **Unproven core claim: 30% no-show reduction** [HIGH] (demand_evidence)
  The central technical/delivery claim (30% fewer missed appointments) is presented as a belief with no pilot data, A/B tests, or citations. If the model cannot achieve materially better outcomes than existing reminder strategies, the product has no advantage. This is the single technical/business hypothesis the whole plan depends on and it is currently unsupported.
  -> What minimal pilot will you run (sample size, metric, duration) to validate the 30% no-show reduction claim before launch?

- **Weak customer acquisition plan that incumbents can outmuscle** [MEDIUM] (acquisition)
  A two-person outbound team targeting 50 paying clinics in six months is fragile and slow. Well-funded competitors can leverage existing sales teams, embedded channels (current customers), SEO, app stores, and partnerships (DSO vendors, suppliers, insurance networks) to reach thousands of clinics fast. The founder provides no channel strategy, conversion estimates, or low-cost pilots to validate their go-to-market.
  -> Which exact channels and conversion metrics will you test first to prove you can hit 50 paying clinics, and why can't incumbents use their existing channels to drown you out?

- **Unclear who within clinics is the buyer and decision process** [MEDIUM] (buyer)
  The target is 'independent US dental clinics' but there is no clarity on the buyer persona (owner, office manager, DSO admin) or purchase cadence (monthly subscriptions vs enterprise contracts). Without this, pricing, sales cycle, and messaging are guesses, making the startup vulnerable to incumbents who already know procurement workflows and influence decision-makers.
  -> Who is the specific buyer persona (title and decision-making power) and what is their typical procurement cadence for software at the price point you propose?

### execution_risk

The plan underestimates the work to legally and technically deploy an AI scheduling product for US dental clinics. Key shipping risks are unaddressed HIPAA/compliance requirements, fragile data and model assumptions (including the 30% no-show reduction claim), and substantial integration work across dental practice management systems — all before a credible customer acquisition and pricing validation plan is proven. A two-person outbound team looks insufficient to both close pilots and feed the training data pipeline required to reach production results.

- **No HIPAA / patient-data compliance plan — likely legal blocker** [CRITICAL] (assumptions)
  The document is silent on HIPAA, business associate agreements (BAAs), data minimization, encryption, audit logging, and breach procedures. If the product will ingest appointment or patient data to predict no-shows, you cannot legally or commercially deploy to US clinics without HIPAA-ready controls and contracts, which materially change cost, timeline, and engineering scope. Treating compliance as optional will halt pilots and sales once clinics request BAAs or security evidence.
  -> Have you validated that your system design, hosting, and contracts meet HIPAA requirements and can you sign BAAs with clinics and/or their EHR vendors within your planned timeline?

- **Integration complexity with dental PMS/EHRs underestimated** [HIGH] (assumptions)
  Dental clinics use a variety of practice management systems (Dentrix, Eaglesoft, OpenDental, etc.) with different APIs, export formats, and security models. The strategy assumes you can collect the historical scheduling data you need without listing which systems you support, what level of access is required, or how long each integration will take. Each new connector can take weeks-to-months and requires engineering, testing, and compliance work, creating a multi-quarter gating risk to onboarding even a handful of clinics.
  -> Which specific PMS/EHRs will you integrate first, how long will each connector take to build and certify, and what fallback exists if a target clinic's system cannot be integrated quickly?

- **Model performance and data access claim (30% reduction) lacks basis and a data pipeline** [HIGH] (assumptions)
  The 30% no-show reduction claim assumes access to sufficiently large, labeled historical appointment datasets and that a generalizable model can be trained or adapted per clinic. There's no plan for collecting training data, handling cold-starts for new clinics, or measuring model drift. Without a pilot dataset and repeatable retraining pipeline, deployment will either fail to achieve promised results or require per-clinic model work that scales poorly.
  -> Can you show a representative dataset or pilot results proving you can predict no-shows at the clinic level, and what is your minimum data requirement per clinic to reach production accuracy?

- **Sequencing: building full product before securing pilot clinics and integration pilots** [MEDIUM] (acquisition)
  The plan implies building the product broadly while aiming to acquire 50 clinics in six months, but it does not prioritize a narrow pilot (one PMS, 3–5 clinics) to validate integrations, compliance controls, and model efficacy. Building general features and UX ahead of a validated integration and model risks wasting engineering time on functionality clinics won't adopt. Pilots are the real blocker to product-market fit and production readiness here.
  -> Which single PMS and 3–5 clinics will you pilot with first, and can you sequence development to deliver a minimal integration+model proof in 8–12 weeks before broader feature work?

- **Two-person outbound team to hit 50 paying clinics in six months is unrealistic** [MEDIUM] (acquisition)
  Acquiring 50 clinics that require integrations, BAAs, and clinical pilots is sales- and operations-intensive; a two-person outbound team will struggle to qualify, negotiate BAAs/technical access, and support onboarding. Each sale will likely need technical pre-sales, legal negotiation, and integration coordination that the stated team doesn't cover. This creates a bottleneck where product readiness outpaces the ability to sign and onboard customers.
  -> What is the expected sales cycle per clinic (qualification → BAA → integration → go-live), and how many of those steps will your two-person team handle concurrently without additional hires or partners?

- **Pricing ($299/location/mo) is unvalidated against clinic willingness given integration effort** [MEDIUM] (pricing)
  The fixed price assumes clinics will pay $299 per location despite potential setup/integration costs, compliance requirements, and per-clinic model tuning. If onboarding requires heavy engineering or multi-week integrations, clinics may balk at the monthly fee or demand implementation discounts/one-time fees. Without pricing tests or an LTV/CAC-informed model, you risk mispricing relative to the true cost of onboarding and supporting each customer.
  -> Have you run willingness-to-pay tests or pilot contracts showing clinics accept $299/month once you include the expected integration timeline and any setup fees?

### evidence_audit

Evidence base: Weak. This is a pre-launch plan with no measured pilots or customer billing; key claims (30% no-show reduction, $299 price, and acquisition economics) are unproven. The most important remaining issue is the missing empirical evidence that the model delivers the claimed uplift and that customers will pay the stated price, because those drive revenue and CAC/LTV viability.

- **No measured evidence that the model achieves a 30% reduction in missed appointments** [HIGH] (demand_evidence)
  The central product claim — a no-show prediction model will reduce missed appointments by 30% — is presented as belief with no pilot, backtest, or customer data. This is load-bearing: product value and customer willingness to pay depend on the achieved uplift and baseline no-show rate. Without a measured effect size and sample context (n, clinic type, baseline no-show), the 30% figure is unsupported.
  -> Provide the empirical result (pilot or backtest) that shows a 30% reduction: sample size, baseline no-show rate, how reduction was measured, and whether the same data sources/configuration will be available in target clinics.

- **Pricing ($299/location/mo) has no willingness-to-pay or competitive evidence** [HIGH] (pricing)
  The $299/month price is stated with no customer research, pilot billing, or comparable market reference. At $299 the implied ARR per customer is $3,588, which may or may not be acceptable to independent dental clinics depending on realized savings; willingness-to-pay is therefore unknown and load-bearing for revenue forecasts.
  -> Share evidence that clinics will pay $299/month (e.g., paid pilot commitments, survey with revealed preference, or comparable product pricing and uptake), or report conversion rates from a pricing experiment.

- **No CAC/LTV/churn inputs — implied economics may not support the sales plan** [HIGH] (key_numbers)
  The plan lists a two-person outbound team and a 50-clinic target but gives no CAC, churn, or lifetime assumptions. Bounding the spend at $5k/month per rep for 6 months implies acquisition spend = 2×6×$5k = $60k → implied CAC ≈ $1,200 (60k/50). With annual revenue per clinic = $299×12 = $3,588, payback and profitability hinge on unknown churn/LTV. Those missing numbers determine whether the acquisition plan is viable.
  -> Provide the assumed customer lifetime (or churn rate) and a justified CAC; if none yet, run the sensitivity: with CAC=$1,200 (as calculated from 2 reps × $5k ×6 months), what maximum churn/lifetime allows payback within X months?

- **Acquisition plan lacks conversion rates and required rep productivity** [MEDIUM] (acquisition)
  Targeting 50 paying clinics in six months implies signing ~8.33 clinics/month total, i.e. ~4.17 closures/month per rep (50/6/2). No conversion rates, contact volumes, or outbound cadence are provided to justify that quota. Without those, the headcount-to-customers arithmetic is unverified and the timeline is unsupported.
  -> Provide the assumed conversion funnel (leads → qualified → demos → closes) and the per-rep monthly activity needed to hit ~4.2 closes/month, or show a pilot that achieved similar per-rep close rates.

- **Undefined buyer and decision process inside independent dental clinics** [MEDIUM] (buyer)
  The plan targets 'independent US dental clinics' but does not specify the buyer (practice owner, office manager, corporate chain) or purchasing constraints. Who signs and who pays affects sales cycle length, willingness-to-pay, and required proof; without this the acquisition and pricing assumptions may not map to reality.
  -> Specify the target buyer persona(s) (role, clinic size, single-location vs multi-location owners) and provide evidence (interviews, commitments, or pilot contacts) that these buyers can and will make the purchasing decision at the proposed price and timeline.


## Selected questions

- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Pricing assumption ($299/location/month) is unvalidated [high]
  - why we're asking: unit_economics / Willingness-to-pay not validated — $299 is unsupported [high]
  - why we're asking: adversarial_competitor / No evidence people will pay for a $299/location product [high]
  - why we're asking: execution_risk / Pricing ($299/location/mo) is unvalidated against clinic willingness given integration effort [medium]
  - why we're asking: evidence_audit / Pricing ($299/location/mo) has no willingness-to-pay or competitive evidence [high]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Acquisition plan (two-person outbound -> 50 paid in 6 months) is unproven [high]
  - why we're asking: unit_economics / CAC and acquisition funnel are undefined and inconsistent with two-person outbound plan [high]
  - why we're asking: adversarial_competitor / Weak customer acquisition plan that incumbents can outmuscle [medium]
  - why we're asking: execution_risk / Sequencing: building full product before securing pilot clinics and integration pilots [medium]
  - why we're asking: execution_risk / Two-person outbound team to hit 50 paying clinics in six months is unrealistic [medium]
  - why we're asking: evidence_audit / Acquisition plan lacks conversion rates and required rep productivity [medium]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No per-location cost-to-serve (compute, storage, support, payments) provided [high]
  - why we're asking: unit_economics / Gross margin at scale vs today is unspecified [medium]
  - why we're asking: unit_economics / Payback period and sensitivity to failure modes not calculated [medium]
  - why we're asking: evidence_audit / No CAC/LTV/churn inputs — implied economics may not support the sales plan [high]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: adversarial_competitor / Unproven core claim: 30% no-show reduction [high]
  - why we're asking: evidence_audit / No measured evidence that the model achieves a 30% reduction in missed appointments [high]

## Answer given

**demand_evidence**: We have not conducted any paid pilots or live tests. The 30% reduction is an unverified target, not an observed result. We have spoken with three dental office managers, but none has committed to purchasing.

Skipped: pricing, acquisition, key_numbers

## Refined critique

### pre_mortem

The plan rests on three unvalidated pillars: that a predictive model will materially reduce no-shows (30%), that clinics will pay $299/location/month, and that two outbound reps can land 50 paying clinics in six months. Early qualitative signals are weak (3 conversations, no commitments) and critical dependencies—access to historical scheduling data and live integration partners—are unstated. If the core efficacy or willingness-to-pay assumptions fail, the product loses its raison d'être quickly.

- **Core efficacy claim (30% no-show reduction) is untested and likely false** [CRITICAL] (assumptions)
  The claimed 30% reduction is an unverified target rather than an observed outcome. This assumes (a) a predictive model can identify no-shows with sufficient precision, and (b) clinics will take the necessary actions based on predictions to realize that reduction—neither of which has been demonstrated. If predictions do not enable concrete, actionable interventions that materially reduce missed appointments, the product's primary value proposition collapses.
  -> Can you demonstrate, on real historical scheduling data or a short paid pilot, that a model+intervention workflow produces anywhere near a 30% reduction in missed appointments under realistic clinic behavior?

- **Willingness-to-pay and buyer identity are unvalidated** [HIGH] (pricing)
  You propose $299 per location per month but have not identified who actually pays (owner, office manager, corporate buyer) or tested whether that price maps to perceived value. Without a validated buyer and price point, you risk building a product clinics will not purchase or will only buy at a much lower price. The founder explicitly skipped 'who pays' and 'how much' in follow-ups.
  -> Which specific buyer (role/title) will sign and pay $299/location/month, and can you get commitments or paid pilots at that price from multiple representative clinics?

- **Outbound acquisition target is assumed, not demonstrated** [HIGH] (acquisition)
  The plan relies on a two-person outbound team to convert cold outreach into 50 paying clinics in six months, yet there is no funnel, conversion-rate assumptions, or evidence this channel works for this product. 'How will your first customers find you?' was left unanswered, so the go-to-market channel is an unstated, high-leverage dependency. If outbound conversion is lower than assumed, growth stalls before launch.
  -> Can you document a repeatable funnel showing outreach → demo → pilot → paid conversion rates that prove a two-person outbound team can acquire 50 paying clinics in six months, or can you secure signed pilot commitments now?

- **No plan for obtaining labeled scheduling data or integrations** [MEDIUM] (assumptions)
  Building a predictive model requires historical appointment, cancellation/no-show labels, and production integration into clinic schedulers—none of which are described. The model cannot be developed or validated without access to representative data and integration partners. This dependency, if unmet, prevents both model training and live utility.
  -> Which clinics or integration partners will provide the historical scheduling data and allow production integration, and can you secure access agreements or export samples within weeks?

- **Early demand signal is weak and misinterpreted** [MEDIUM] (demand_evidence)
  You spoke to three office managers and have no paid pilots or commitments; treating that as evidence of demand conflates polite interest with purchase intent. There is no revealed-preference data (paid pilots, signed LOIs, or deposits) to support the product-market fit claim. Relying on this sample risked overestimating true demand.
  -> Can you obtain multiple signed, time-boxed paid pilots or deposits from representative independent dental clinics within an immediate timeframe to validate real purchase intent?

### evidence_audit

Evidence base: Weak. The document is pre-launch with no paid pilots; only three informal customer conversations and an unverified 30% no-show claim. Pricing and an outbound acquisition plan are stated but lack measured conversion, CAC, churn or onboarding evidence. The most important gap is absence of any pilot data proving impact and willingness-to-pay.

- **No measured evidence that the product reduces no-shows or that clinics will pay** [CRITICAL] (demand_evidence)
  The central technical and commercial claims are untested: the 30% no-show reduction is explicitly unverified and there have been no paid pilots or live tests. The only customer contact is conversations with three office managers (n=3), which is far too small to evidence either effectiveness or willingness-to-pay. Without measured pilot results (baseline no-show rate, post-intervention no-show rate, sample size and statistical method) the core value proposition is unsupported.
  -> Provide results from a paid or at-minimum-instrumented pilot: baseline no-show rate, post-deployment no-show rate, sample size (number of clinics and appointments) and follow-up duration that demonstrate the claimed ~30% reduction.

- **Outbound plan implies an unsupported, costly CAC** [HIGH] (acquisition)
  Targeting 50 paying clinics in six months with a two-person outbound team implies 25 closed clinics per rep over six months (≈4.2 closures per rep per month). If we bound rep cost conservatively at $5k/month fully loaded, 2 reps × 6 months = $60,000 acquisition spend; $60,000 ÷ 50 = $1,200 implied CAC. At $299/mo revenue per clinic that is ~4.0 months of gross revenue to recoup CAC (1,200/299≈4.01), before accounting for churn, hosting/ops, or gross margin. No conversion rates, pipeline velocity or CAC estimates were provided to validate this plan.
  -> Show measured or historically justified outbound conversion rates (outreach → demo → paid) and/or an actual CAC estimate from a pilot so we can validate that 2 reps can realistically close 50 paying clinics in 6 months.

- **Pricing / buyer statement is inconsistent and unsupported** [HIGH] (pricing)
  The doc states 'charge $299 per location per month' but in the 'still unknown' section the founder skipped 'Who pays, and roughly how much?', creating an internal inconsistency. There is no evidence that the paying party (independent clinic owner vs. group manager) accepts $299, nor any willingness-to-pay data or signed letters of intent. Pricing is load-bearing for revenue math and for CAC payback calculations but is unsourced.
  -> Confirm who will actually sign/pay the $299/month (clinic owner, practice manager, or corporate owner) and supply evidence of willingness-to-pay at that price (e.g., pilot invoices, paid commitments, or pricing test results).

- **Key commercial metrics (churn, LTV, conversion) are missing** [MEDIUM] (key_numbers)
  Revenue per clinic is stated (299/mo) but other load-bearing numbers are absent: expected churn rate, customer lifetime, conversion from trial/demo to paid, and resulting LTV. Without these, you cannot assess payback, unit economics or whether the $1,200 implied CAC (see flaw above) is acceptable. The plan cannot be modeled or stressed without these inputs.
  -> Provide your assumed or measured values for conversion rate (demo→paid), monthly churn or expected customer lifetime, and resulting LTV per customer, and state whether each is measured or an estimate.

- **Timeline and product readiness to acquire 50 paying clinics in 6 months is unsupported** [MEDIUM] (assumptions)
  You forecast acquiring 50 paying clinics in six months but the product is still being built and no timeline, deployment complexity or onboarding time per clinic is provided. That outreach-to-paid timeline is a forecast that depends on product readiness (integration with clinic appointment systems), onboarding friction, and operational capacity to run pilots and deploy the model — none of which are evidenced.
  -> Provide a documented product roadmap with expected dates for a deployable beta, average onboarding hours per clinic, and evidence (or assumptions) that onboarding + validation can be completed quickly enough to reach 50 paying clinics within six months.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['pricing', 'acquisition', 'key_numbers']

## Reuse check

Re-sending the same refinement token refused with 409: yes
