# T04-medical-assistant

**Stage:** building

## Input

We're developing an AI assistant that helps small private clinics manage appointment requests and patient queries. We plan to integrate with existing booking systems, charge £149 per clinic per month and begin with clinics in the UK.

**Reviewer expectation:** distinguishes admin from clinical advice, flags privacy/data-processing risk, does not declare regulatory violations that have not occurred.

## First critique

### pre_mortem

The plan relied on several untested, interlocking assumptions: that technical integrations with clinics' booking systems would be straightforward, that UK private clinics would accept an AI handling patient queries, and that they would pay £149/month. The single most likely killing blow was a failure to achieve reliable, authorized integrations with the booking systems clinics actually use. Other dependencies—regulatory acceptance, a clear buyer within clinics, and an acquisition channel—also did not materialize because they lacked early validation.

- **Integration dependency collapsed — booking systems weren't open or consistent** [CRITICAL] (assumptions)
  The strategy assumed you could integrate with 'existing booking systems' as a matter of engineering work. In the market outcome, the major systems used by target clinics either had no public APIs, required commercial partnerships, or had highly bespoke data models, making reliable two-way sync infeasible within the planned timeline and budget. Without those integrations the assistant couldn't own appointment state or reliably confirm/modify bookings, which is central to the product's value proposition and effectively killed adoption. The immediate test you missed was proving at least one real, authorized integration with representative systems before assuming broad technical feasibility.
  -> Can you demonstrate working, authorized integrations with the specific booking systems used by representative UK private clinics (not just theoretical APIs)?

- **Demand unvalidated — clinics didn't want AI to handle patient queries** [HIGH] (demand_evidence)
  You assumed clinics actively want an AI to manage appointment requests and patient queries, but you never validated whether clinics view that as acceptable for patient-facing communication. In reality many clinics prioritized human touch, feared patient dissatisfaction, or had low volumes that didn't justify automation. The cheapest validation should have been a small paid pilot or simulated concierge test to measure willingness to hand queries to an automated assistant.
  -> Can you show direct evidence (paid pilots, signed LOIs, or measured behavioral trials) that target clinics want an AI to handle patient queries instead of current human processes?

- **Pricing assumption failed — £149/month didn't match willingness to pay** [HIGH] (pricing)
  The fixed price of £149/month was asserted without evidence that clinics valued the feature set enough to pay that amount. After launch, many clinics rejected the price as too high relative to their appointment volume or preferred one-off fees per booking, or they prioritized hiring reception staff. You should have tested price sensitivity with pre-sell offers or A/B price experiments in pilot clinics before locking the price.
  -> Can you secure paid commitments from representative clinics at £149/month (or demonstrate willingness via refundable prepayments) before building the full product?

- **Regulatory/privacy acceptance was assumed but didn't materialize** [HIGH] (assumptions)
  The plan assumed clinics would be comfortable routing patient queries and booking data through your AI service, but you didn't validate legal, insurer or data protection constraints. Over 18 months, clinics and some insurers refused to share identifiable patient data with a third-party AI without extensive audits, contracts, or on-prem solutions, blocking deployments. A minimal test would have been a regulatory review and a security questionnaire completed by a pilot clinic before scaling.
  -> Have you validated with compliance officers/insurers/regulatory advisors that clinics can lawfully and contractually route patient queries and booking data to your service, and can you pass their security assessments?

- **Buyer is vague — who signs the contract and pays is unclear** [MEDIUM] (buyer)
  Labeling the customer as 'small private clinics' hides who actually decides and pays: owners, practice managers, chains, or franchise owners. In practice the sales cycle stretched because decisions required multi-stakeholder approval (clinical lead, owner, IT), which you had not accounted for. You needed to identify and validate the economic buyer and decision process through interviews and pilot negotiations early on.
  -> Who within the clinic will be the economic buyer and decision-maker, and have you validated their authority and buying criteria in real clinics?

- **No credible acquisition channel — clinics were hard to reach at scale** [MEDIUM] (acquisition)
  The strategy had no tested plan to reach and convince clinics; you implicitly assumed outreach would be straightforward. Over 18 months, low response rates, gatekeeping by receptionists, and expensive trade channels meant you couldn't acquire pilot customers at the necessary rate. The immediate, low-cost tests missing were targeted outreach campaigns and partnerships to measure real conversion from outreach to pilot signup.
  -> What repeatable, low-cost channel will acquire clinics, and can you demonstrate initial customer acquisition through that channel?

### unit_economics

The document states a price (£149/month per clinic) and target (UK small private clinics) but contains no unit-costs, CAC, conversion or evidence of willingness-to-pay. That makes it impossible to evaluate gross margin, payback, or whether the stated price is realistic relative to customer acquisition costs and hidden operational/regulatory expenses. Before launch the team must provide a minimal unit-economics model and simple validation experiments for price and acquisition.

- **No fully-burdened cost-to-serve per clinic** [HIGH] (key_numbers)
  The plan lists a price but provides no breakdown of the monthly cost to serve one clinic (compute, storage, backups, monitoring, third‑party APIs, SMS/voice, payment fees, customer support time, onboarding). Without these numbers you cannot calculate gross margin or know whether £149/mo covers ongoing costs at any scale. This is a foundational missing input for unit economics.
  -> What is your fully-burdened monthly cost to serve one clinic (itemized: compute, storage, third‑party API usage, payment fees, and per‑clinic support/onboarding costs)?

- **Pricing is unsupported by evidence of willingness-to-pay** [HIGH] (pricing)
  The document fixes a price of £149/mo but provides no evidence (pilot signups, contracts, survey or A/B price tests) that clinics will actually pay that amount. Stating a price without validation risks a mismatch between assumed ARPU and real revenue. Willingness-to-pay is a core revenue assumption that needs at least a few validated commitments before scaling.
  -> How did you validate the £149/month price — do you have pilot commitments, paid trials, signed LOIs, or price‑sensitivity test results from target clinics?

- **Customer acquisition channels and CAC are unspecified** [HIGH] (acquisition)
  There is no acquisition plan or channel mix described, so expected CAC is unknown. At a £149/mo price point different channels (self‑serve, inbound content, outbound sales, partnerships) imply very different CAC and sales cycles; without channel assumptions you cannot estimate payback or scalability. The feasibility of the model depends heavily on realistic CAC relative to LTV.
  -> Which specific acquisition channels will you use, what is your expected CAC per clinic on each, and what experiments will you run to validate those CAC assumptions?

- **Gross margin and payback period not modeled** [MEDIUM] (key_numbers)
  No unit-economics model is presented (gross margin per clinic, churn, LTV, months to payback). Without combining cost-to-serve, CAC and churn you cannot say whether the business reaches positive gross margins at scale or how long customer acquisition investment takes to recover. This prevents any sensible planning for hiring, marketing spend, or fundraising.
  -> Provide a simple model showing gross margin per clinic, expected monthly churn, LTV, CAC, and months to payback under your base and pessimistic scenarios.

- **Operational and regulatory costs (moderation, compliance, refunds) are unaccounted** [MEDIUM] (assumptions)
  Healthcare/clinic-facing products commonly incur additional costs: data‑protection/GDPR compliance, secure data handling, legal review, clinical content moderation, incident response, refunds/chargebacks and fraud prevention. None of these are mentioned, yet they can materially increase per‑clinic costs and compliance overhead as you scale.
  -> How will you budget for healthcare data compliance, content moderation/clinical oversight, refunds/chargebacks and fraud prevention, and what monthly cost per clinic do you assume for these functions?

### adversarial_competitor

This AI assistant is an obvious bolt-on to existing clinic booking/EHR products and can be neutralized cheaply by incumbents. The plan lacks a defensible differentiator, clear go-to-market detail, and justification for a £149/month charge — all things a well-funded competitor can weaponize quickly. The cheapest kill: ship a simple auto-responder/triage feature bundled into an existing product or offered free to existing customers while leaning on trust and integration partnerships.

- **Incumbent feature parity makes you redundant** [HIGH] (differentiation)
  The product is a classic 'feature' (auto-respond/triage for appointment requests) that can be built into any booking/EHR system. A vendor with existing clinic customers can ship a basic AI responder or templates within weeks and mark it as an included capability, removing your primary differentiation. With no claimed unique IP or exclusive data, there's nothing preventing incumbents from replicating core functionality.
  -> What unique capability or data do you have that booking/EHR vendors cannot replicate and ship within 3 months?

- **We can out-distribute you via existing partnerships and integrations** [HIGH] (acquisition)
  You plan to integrate with booking systems, but incumbents already own those relationships and integration contracts. A competitor can push the assistant as an add-on or built-in feature across thousands of clinics overnight via existing channels, crushing your GTM. Your document doesn't say which systems or partners you have access to, so you are vulnerable to rapid incumbent rollouts.
  -> Which booking systems are you targeting first and do you have partnership or API access commitments from them?

- **Price is easily undercut or bundled away** [HIGH] (pricing)
  At £149/clinic/month you are attackable: incumbents can include an equivalent feature for free or at a nominal add-on cost, or a deep-pocketed competitor can underprice with freemium to win share. Because clinics are price-sensitive and incumbents can cross-subsidize, your standalone subscription is unlikely to withstand competitive pricing pressure.
  -> Why will clinics pay £149/mo for this instead of getting the same capability bundled by their current vendor or a cheaper alternative?

- **Brand, trust and patient data concerns favor incumbents** [MEDIUM] (assumptions)
  Clinics handle protected health information and will prefer vendors with established compliance, accreditations, and clinical references. A new startup asking to handle patient queries faces a steep trust hurdle; incumbents and NHS-endorsed partners can exploit that to block third-party entrants. Your plan doesn't address compliance, certifications, or clinical endorsements.
  -> How will you overcome clinics' trust and compliance concerns to get them to hand patient queries to a new vendor?

- **No evidence clinics will pay or adopt — pilot plan missing** [MEDIUM] (demand_evidence)
  There is no demand evidence, pilot commitments, or early adopter pipeline presented. Before launch this should be validated with pay-or-pilot clinics; without that the product is a speculative feature. The cheapest test (not described) would be a concierge pilot with a small number of clinics to prove value and willingness to pay.
  -> How many clinics have agreed to a paid pilot and what metrics will you use to prove value quickly?

- **Unclear what clinics currently use and how you'll displace them** [MEDIUM] (alternatives)
  You haven't specified the incumbent workflows (reception staff, phone systems, automated booking, outsourced triage) you are displacing or augmenting. Without mapping current alternatives, you can't target messaging or product hooks that overcome inertia. That leaves you open to incumbents who already own those workflows.
  -> What are the current workflows and stop-gap solutions clinics use today for appointment requests and patient queries, and which segment will you displace first?

### execution_risk

The plan glosses over the hardest parts of shipping: handling regulated patient data, integrating with many heterogeneous booking systems, and actually finding paying clinics. Missing detail on team capability, sequencing (validate demand before heavy engineering), and go-to-market execution are the most likely causes of multi-month delays or a product that never reaches customers.

- **No plan for regulated patient data (GDPR/medical liability)** [CRITICAL] (assumptions)
  The doc says the assistant will handle patient queries and appointment requests but says nothing about legal or compliance work. Processing identifiable health-related data in the UK triggers GDPR, Data Protection Impact Assessments, data processing agreements with clinics, potential registration with ICO, and clinical/legal liability for automated responses — any of which can block deployment or require a full redesign. This is a fatal operational blocker if not resolved before piloting with real clinics.
  -> What specific legal/compliance steps, DPIAs, DPAs, clinical oversight and insurance are in place to process health data and serve patient-facing AI responses in UK clinics?

- **Integration hell: supporting many booking systems is under-scoped** [HIGH] (assumptions)
  You plan to integrate with 'existing booking systems' but provide no list, prioritization, or fallback plan. Each vendor may have different APIs, authentication, webhook behaviors, rate limits, or no API at all — building and maintaining connectors is often months of work per system and a continuous maintenance burden. Underestimating this will push launch timelines and consume engineering resources.
  -> Which booking systems will you support in month 1–6 and what is the concrete engineering plan (including fallback/manual flows) for systems without stable APIs?

- **No team, roles, or capacity stated versus the scope of work** [HIGH] (assumptions)
  The document names a product and price but no founders, engineers, or compliance/legal resources. Building secure, integrated, and compliant healthcare automation typically requires multiple engineers, a security/DevOps person, and legal/compliance or clinical input; without that stated, the plan is likely under-resourced and will slip. The implicit failure mode is a one- or two-person team trying to do months of specialized work and burning out or shipping unsafe tech.
  -> Who is on the team today (roles and relevant experience) and how many engineer-months are budgeted for integrations, security, and compliance work?

- **No go-to-market or clinic acquisition plan** [HIGH] (acquisition)
  You’ve set a price (£149/mo) but have not described how you will reach or convince clinics to sign up. Small private clinics are time-poor and risk-averse; without a channel (B2B sales, partnerships with booking vendors, reseller, or targeted outreach) you can ship a working product and have zero customers. The specific failure mode is product completion followed by months of zero traction because acquisition wasn't built in parallel.
  -> What are the initial acquisition channels and sales process to acquire the first 10–50 UK clinics, and who will run that outreach?

- **Pricing is unsupported and may not match clinic willingness to pay** [MEDIUM] (pricing)
  Charging £149/month is stated with no evidence of willingness to pay, cost savings to clinics, or comparable benchmarks. If clinics view this as too expensive relative to their margin or existing staff time, conversion will be low. The plausible failure is a technically working product with churn or zero new signups because the price point is wrong.
  -> What evidence or tests support £149/mo as an acceptable price for target clinics (pilot commitments, surveys, or competitor pricing)?

- **Sequencing: building AI and integrations before validating demand** [MEDIUM] (demand_evidence)
  The strategy assumes clinics want an automated assistant and will pay upfront; there’s no plan to validate demand with a concierge or manual prototype. If clinics prefer a human triage or a simpler integration, you’ll waste months developing complex automation. Failure mode: wasted engineering on features customers don't need.
  -> What is the cheapest way you will validate clinic demand and willingness to pay before building production integrations (e.g., manual handling, landing page, paid pilots)?

- **Unspecified data model and security controls for patient data** [MEDIUM] (assumptions)
  There is no mention of what patient data is stored, how long it is retained, whether conversations are logged, or how keys/encryption are managed. This omission risks later rework if regulators or customers demand stricter controls, or a security incident forces a pause. The concrete failure is having to redesign storage/architecture mid-development, delaying launch.
  -> What data will you store, where will it reside, and what technical controls (encryption, access controls, audit logs) will you implement from day one?

### evidence_audit

Evidence base: Weak. The plan is pre-launch with no pilots, customers, or revenue; core claims (demand, pricing, integrations) are asserted but untested. The most important remaining issue is missing measured demand and pricing validation that underpin revenue forecasts.

- **No evidence clinics want this (demand)** [HIGH] (demand_evidence)
  The document asserts the AI will 'help small private clinics manage appointment requests and patient queries' but provides no measured evidence (pilot, interviews, survey, or signed LOI) that clinics face this problem at scale or will adopt an AI assistant. For an idea-stage product this is load-bearing: without basic demand validation the pricing and go-to-market plans are meaningless. Simple discovery (n = 20–50 clinics) or a paid pilot would be the minimal test.
  -> Provide concrete demand evidence: how many UK small private clinics have you interviewed or piloted with, and what fraction expressed willingness to pay or trial the service?

- **Pricing (£149/mo) is unsourced and unvalidated** [HIGH] (pricing)
  The stated price of £149/clinic/month is presented with no supporting data on willingness-to-pay, price sensitivity, or competitor pricing. That price implies £149 × 12 = £1,788 revenue per clinic per year; whether that yields viable unit economics depends entirely on CAC, churn and marginal costs which are unstated. Charging a price with no validation is a load-bearing assumption for revenue forecasts.
  -> Show pricing validation: results of willingness-to-pay tests, competitive price points, or at least pilot conversion at £149/mo (or explain how you chose £149)?

- **Customer definition ('small private clinics') is too vague** [MEDIUM] (buyer)
  Targeting 'small private clinics in the UK' lacks segmentation (size, specialty, booking volume, tech stack) needed to size the market and design acquisition. Different clinic types will have different needs and budgets; without a clear buyer persona you cannot estimate addressable market, onboarding complexity, or product fit.
  -> Define the target clinic persona(s): clinic size in practitioners, specialties, monthly appointment volume, and current booking systems used for your initial go-to-market cohort.

- **No customer acquisition plan or CAC assumptions** [MEDIUM] (acquisition)
  The doc says 'begin with clinics in the UK' but gives no acquisition channel, conversion rates, or CAC. That prevents any revenue or unit-economics projections. Even a conservative bound — e.g. one outbound rep at £5k/month fully loaded acquiring X clinics — would allow checking feasibility, but no such numbers are provided.
  -> How will you acquire clinics initially and what are your assumed conversion rate and CAC (provide channel-level estimates or pilot conversion data)?

- **Integration with 'existing booking systems' is asserted but unproven** [MEDIUM] (assumptions)
  The plan to integrate with existing booking systems is central but unspecified: which systems, whether they have public APIs, data access, multi-tenant embedding, or commercial terms. Integration complexity and variability across clinic systems could materially affect time-to-launch and deliverability, yet no feasibility or technical constraints are provided.
  -> List the booking systems you plan to integrate with first and provide evidence (API docs, pilot integrations, or partner agreements) that these integrations are technically and contractually feasible within your timeline.


## Selected questions

- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Pricing assumption failed — £149/month didn't match willingness to pay [high]
  - why we're asking: unit_economics / Pricing is unsupported by evidence of willingness-to-pay [high]
  - why we're asking: adversarial_competitor / Price is easily undercut or bundled away [high]
  - why we're asking: execution_risk / Pricing is unsupported and may not match clinic willingness to pay [medium]
  - why we're asking: evidence_audit / Pricing (£149/mo) is unsourced and unvalidated [high]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / No credible acquisition channel — clinics were hard to reach at scale [medium]
  - why we're asking: unit_economics / Customer acquisition channels and CAC are unspecified [high]
  - why we're asking: adversarial_competitor / We can out-distribute you via existing partnerships and integrations [high]
  - why we're asking: execution_risk / No go-to-market or clinic acquisition plan [high]
  - why we're asking: evidence_audit / No customer acquisition plan or CAC assumptions [medium]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / Demand unvalidated — clinics didn't want AI to handle patient queries [high]
  - why we're asking: adversarial_competitor / No evidence clinics will pay or adopt — pilot plan missing [medium]
  - why we're asking: execution_risk / Sequencing: building AI and integrations before validating demand [medium]
  - why we're asking: evidence_audit / No evidence clinics want this (demand) [high]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No fully-burdened cost-to-serve per clinic [high]
  - why we're asking: unit_economics / Gross margin and payback period not modeled [medium]

## Answer given

**demand_evidence**: We have not run any pilots and no clinic has committed to using or paying for it yet.

Skipped: pricing, acquisition, key_numbers

## Refined critique

### pre_mortem

The plan rests on several unvalidated core assumptions: that small private clinics will buy an AI assistant at £149/month, that integration with existing booking systems is straightforward, and that clinics (and their patients) will accept automated handling of appointment requests and patient queries. The founder has no pilot customers, no evidence of demand, and an internal contradiction about pricing/who pays — any of which could stop progress before launch. The single most likely fatal event is clinics refusing to allow AI to handle patient-facing communications (for trust, liability or privacy reasons) or refusing to pay the stated price.

- **Price declared but buyer and willingness-to-pay unvalidated (internal contradiction)** [CRITICAL] (pricing)
  The document sets a price of £149/clinic/month but elsewhere admits 'who pays, and roughly how much' is unknown and no clinics have committed. That contradiction means the product’s basic monetization assumption is untested and may be false — if the decision-maker won't pay that price, the model collapses. There is no evidence the buyer (owner, manager, or receptionist) bears the cost or perceives £149 of recurring value.
  -> Which specific person or entity in a clinic will decide and commit to paying £149/month, and will they sign up before the product ships?

- **No demand evidence: zero pilots, zero commitments** [HIGH] (demand_evidence)
  Founder admits no pilots and no clinic commitments. The plan assumes clinics both need and will adopt this assistant, but there is no qualitative or quantitative evidence of the problem's severity, prioritization, or willingness to change workflow. Without early customer validation, the entire go-to-market assumption is speculative.
  -> Do clinic managers experience this pain strongly enough to switch to and pay for a new AI assistant (evidence: signed pre-orders or pilot agreements)?

- **Integration with booking systems assumed feasible but untested** [HIGH] (assumptions)
  The strategy depends on integrating with existing booking systems, yet there is no inventory of which systems target clinics use, whether those systems expose APIs, or whether terms permit third-party automation of patient communications. If key booking systems are closed, inconsistent, or charge prohibitive fees, the product cannot function as designed.
  -> Which specific booking systems must be integrated first, do they provide the required APIs/permissions, and can you technically and contractually integrate with them?

- **Unclear who the actual buyer/decision-maker is inside clinics** [HIGH] (buyer)
  The plan labels 'small private clinics' as customers but does not identify who signs software contracts or who budgets for admin tools. Clinics often delegate purchases across owners, managers, or group administrators; targeting the wrong persona will prevent sales despite genuine demand. This unknown undermines pricing, acquisition, and messaging assumptions.
  -> Who in a target clinic has the budget authority and pain alignment to sign and pay for this service?

- **Assumes patients will accept AI handling sensitive queries** [MEDIUM] (assumptions)
  The product presumes it's acceptable for an AI to manage patient queries, yet no evidence shows patients are comfortable discussing health matters with automated assistants or that clinics are willing to expose patient interactions to an AI. Patient trust or regulatory concerns could sharply limit usable scope (e.g., triage vs. scheduling).
  -> Which categories of patient queries will clinics allow automated handling for, and do patients accept those automated interactions in real settings?

- **Unclear differentiation vs existing booking systems or human staff** [MEDIUM] (differentiation)
  The document does not explain why clinics would adopt this assistant instead of using features in current booking software or continuing with reception staff. Without a clearly articulated and tested unique value (time saved, fewer no-shows, revenue lift), clinics have little incentive to change entrenched workflows.
  -> What measurable outcome will clinics get from this assistant that they cannot get from their current booking system or hiring existing staff?

### evidence_audit

Evidence base: Weak. The plan is pre‑launch with no pilots, revenue, or paid commitments. What is proven is only the stated concept and price; the most important remaining issue is the lack of measured demand and core financial metrics needed to judge feasibility.

- **No demand evidence or paid commitments** [HIGH] (demand_evidence)
  You state you have not run pilots and no clinic has committed to pay. That removes any empirical basis for believing clinics will adopt or pay £149/mo. Without measured trials or signed letters of intent, the central commercial claim (that clinics will be customers) is unsupported and load-bearing for the whole plan.
  -> Provide measured demand: how many clinics have you trialed or interviewed, how many committed to a paid trial or LOI, and what were the trial-to-paid conversion and willingness-to-pay results (numbers and %)?

- **Core financial inputs (CAC, churn, conversion, LTV) are missing** [HIGH] (key_numbers)
  The plan contains no CAC, churn, conversion rate (trial→paid), LTV, or ARR target — all key numbers needed to judge viability. These are load-bearing: e.g., revenue per clinic is £149×12 = £1,788/year, so any ARR target implies a required clinic count (100,000/1,788 ≈ 56 clinics). Without those inputs you cannot estimate required sales volume, payback period, or hiring/marketing needs.
  -> Supply the measured or assumed values for CAC, monthly churn, trial→paid conversion %, target ARR (or number of clinics) at 12 months, and the LTV calculation that uses these numbers?

- **Price point (£149/mo) is unsupported** [HIGH] (pricing)
  You list £149/month per clinic but provide no evidence this price is acceptable to target clinics. That single price implies £1,788/year per clinic; to reach £100k ARR you would need ~100,000/1,788 ≈ 56 clinics. Whether that price yields enough demand or unit economics is unknown and critical.
  -> How did you choose £149/month — provide willingness-to-pay data (surveys, pilot pricing, or LOIs) showing number of clinics and % that accept this exact price or a tested price curve?

- **Buyer (who pays / decision-maker) is unspecified** [MEDIUM] (buyer)
  The document doesn't say who in a clinic will decide and pay (owner, practice manager, corporate admin of a chain), yet that determines sales cycle, objections and pricing sensitivity. Different buyers change conversion rates and required evidence or compliance.
  -> Identify the specific buyer persona(s) (title, clinic size, single site vs chain) and report how many such decision‑makers you have interviewed and what each said about buying authority and purchase criteria.

- **Acquisition channel and implied CAC are undefined** [MEDIUM] (acquisition)
  You skipped how first customers will find you. Without an acquisition channel and rough CAC estimate you cannot assess the scalability or cost to reach the clinic counts implied by your pricing. This is a required input to convert revenue-per-clinic into a go-to-market plan.
  -> State the planned initial acquisition channel(s) (e.g., direct sales, partnerships, paid ads), provide an expected CAC per clinic (or a bound), and a simple test plan to measure it in the first 90 days.

- **Integration targets and technical feasibility are not specified** [LOW] (assumptions)
  You plan to integrate with existing booking systems but list no target systems, APIs, or proof that integration is feasible. Integration complexity affects time-to-first-customer and cost but is left as an unstated assumption.
  -> List the specific booking systems you plan to support first, state whether they have public APIs or partner programs, and provide a one-system pilot plan including an estimated integration time (days) and acceptance criteria.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['pricing', 'acquisition', 'key_numbers']

## Reuse check

Re-sending the same refinement token refused with 409: yes
