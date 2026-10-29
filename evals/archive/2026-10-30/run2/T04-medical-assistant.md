# T04-medical-assistant

**Stage:** building

## Input

We're developing an AI assistant that helps small private clinics manage appointment requests and patient queries. We plan to integrate with existing booking systems, charge £149 per clinic per month and begin with clinics in the UK.

**Reviewer expectation:** distinguishes admin from clinical advice, flags privacy/data-processing risk, does not declare regulatory violations that have not occurred.

## First critique

### pre_mortem

The plan rests on multiple unvalidated assumptions about legal/regulatory permission to process patient data, clinics' willingness to let an AI handle patient-facing communications, and seamless access to booking-system APIs. The declared price and buyer are unsupported, and the product's claimed fit (integrating with existing systems) hides a major technical and commercial dependency. Any one of these could stop the project; the most likely fatal failure is inability to legally and safely process patient data for UK clinics without onerous controls or certification.

- **Unstated GDPR / health-data compliance assumption — potential legal showstopper** [CRITICAL] (assumptions)
  You assume you can process appointment requests and patient queries with an AI for UK clinics but the strategy says nothing about GDPR, DPA contracts, patient consent, or clinical safety oversight. Handling personal health information in the UK commonly requires specific contracts, data residency, and documented safeguards. If regulators, insurers, or clinics refuse to sign on without those controls, you cannot operate as described.
  -> Exactly what legal/regulatory approvals, data processing agreements, and controls do you need to process patient queries for UK clinics, and can you obtain them within the timeline and budget?

- **No evidence clinics will route live patient communications to an AI** [HIGH] (demand_evidence)
  The plan assumes clinics will let an automated assistant handle appointment requests and patient queries, but there is no evidence clinics trust AI to interact with patients about appointments and potentially sensitive health issues. Clinics may prefer human gatekeepers for liability, triage judgments, or patient experience reasons, and stated interest in automation may not translate into actual usage. A cheap first test is direct interviews plus a paid pilot where the AI handles a subset of non-clinical messages to observe revealed preference.
  -> Will target clinics actually route real patient-facing communications to an AI in production, and under what constraints (types of queries, oversight, opt-in/opt-out)?

- **Assumption that booking systems expose usable integrations** [HIGH] (assumptions)
  You plan to integrate with existing booking systems but provide no evidence those systems offer APIs or webhooks that allow an AI to read/write appointments and query state in real time. Many vendors limit third-party access or impose commercial/technical gates. If the major booking platforms used by target clinics don't permit the necessary integration, the product cannot function as described.
  -> Which booking platforms do your target clinics use and do those platforms provide the APIs and contract terms required for two-way automated appointment management?

- **£149/month price is asserted with no willingness-to-pay evidence** [HIGH] (pricing)
  You present a single price point but provide no evidence that small private clinics will accept £149/month for this assistant or that they are the payer. Price sensitivity, perceived value, and internal budget holders are unstated. Without tests (surveys, pricing experiments, or paid pilots) this assumption may be wrong and will affect adoption decisions.
  -> Will target clinics pay £149 per month for this service, and who in the clinic controls that budget?

- **Buyer and decision-maker are unspecified** [MEDIUM] (buyer)
  The document says 'clinics' but doesn't identify who signs the contract — owner, practice manager, chain IT, or external management company — nor whether the user and buyer are the same. Different buyers have different risk tolerances, procurement cycles, and legal requirements. This ambiguity makes acquisition and pricing assumptions fragile.
  -> Who will be the purchaser and contract signer in a typical target clinic, and what approvals will they require to buy an AI assistant handling patient data?

- **Unclear differentiation versus existing booking features and human staff** [MEDIUM] (differentiation)
  You claim to integrate with booking systems but don't explain why clinics would choose your AI over built-in booking features, add-ons from booking vendors, or simply hiring/reallocating reception staff. If your value is incremental (efficiency) rather than transformational (capability they don't have), adoption will be harder than assumed. You need to prove a clear advantage that matters to the buyer.
  -> What exact capability or outcome will make clinics choose this assistant instead of their current booking features or human reception staff?

### unit_economics

The document gives a headline price (£149/clinic/month) but no supporting unit-costs, CAC, churn/LTV or evidence of willingness-to-pay. Key cost drivers (integration engineering, compute/storage, support, payment fees, compliance) and customer acquisition channels are unstated, so you cannot validate margins, payback or scalability. At this stage the highest-priority gaps are validating the price with buyers, estimating per-clinic cost-to-serve (including one-time integration) and modelling realistic CAC/payback for B2B clinics.

- **Asserting £149/mo without any willingness-to-pay evidence** [HIGH] (pricing)
  The plan states a price but provides no evidence that clinics will pay £149/month, who the buyer/decision maker is, or whether that price beats existing alternatives (staff time, other software). Without validated WTP you cannot compute realistic revenue, conversion rates or LTV. Treating the price as fixed today is unsafe for any unit-economic projection.
  -> How did you validate that UK small clinics will pay £149/month and who signs the purchase order?

- **No per-clinic cost-to-serve or integration cost model** [HIGH] (key_numbers)
  There are no numbers for compute, storage, monitoring, third‑party API costs, onboarding engineering, or ongoing support per clinic. Integrations with booking systems typically require one-off engineering or per-customer configuration/maintenance, which can dominate early unit costs. Without these line-item costs you cannot estimate gross margin or break-even.
  -> What is your modeled per-clinic cost (monthly compute/storage + amortized integration/onboarding + support + payment processing) once you integrate with target booking systems?

- **Customer acquisition channels and realistic CAC are unspecified** [HIGH] (acquisition)
  The doc says 'begin with clinics in the UK' but gives no acquisition channels, funnel, or expected CAC. At a B2B price point of £149/month, channels (direct sales, partnerships, reseller, paid digital) and their costs matter hugely for payback. Assuming 'low-cost' or viral growth without a channel plan will understate CAC and overstate scalability.
  -> Which specific acquisition channels will you use for clinics and what CAC do you expect from each (esp. first 100 customers)?

- **No LTV, churn, payback period or sensitivity analysis** [MEDIUM] (key_numbers)
  There is no churn or retention assumption, no LTV, and no payback calculation on CAC. That makes it impossible to judge whether a given CAC is acceptable or how long cash is tied up. Early-stage B2B products often have meaningful onboarding churn and slow sales cycles which materially affect payback.
  -> What are your assumed monthly churn and resulting LTV, and how many months to pay back a typical CAC under those assumptions?

- **Healthcare-specific compliance, liability and hidden operational costs are unaccounted** [MEDIUM] (assumptions)
  Patient data handling triggers GDPR, data security, potential clinical governance and legal/liability costs (audit, insurance, incident response), plus moderation of conversation logs. These can be significant fixed and per-customer costs and may require third-party certification or skilled staff. The plan includes none of these line items.
  -> Which compliance, security and liability costs (one‑time and recurring) have you budgeted per clinic and company-wide?

- **No plan or cheap test to validate demand and price before building** [LOW] (demand_evidence)
  At idea stage you should run low-cost experiments to validate both demand and price (e.g., discovery calls, paid pilot, landing page with signups, concierge onboarding). The document contains no immediate test plan to confirm clinics' willingness to buy at the proposed price.
  -> What is the cheapest experiment you will run this week to validate at least a handful of clinics would pay £149/month?

### adversarial_competitor

This product is a single-feature AI assistant for appointment requests and patient queries priced at £149/month per clinic and targeting UK small private clinics. It's highly attackable: the core feature is trivial for incumbents to replicate and weaponize through existing distribution, pricing bundles, and brand trust — so the founder must show a defensible differentiation, clear acquisition channel, and validated willingness-to-pay quickly or it will be commoditized or killed by larger players.

- **No defensible differentiation — trivial to replicate** [HIGH] (differentiation)
  An AI that answers appointment requests and patient queries is a narrowly scoped feature that incumbent booking/EHR vendors or large telehealth platforms can add as a toggle or app. A single shipped feature (automated messaging + booking integration) from a well-funded incumbent makes a standalone assistant redundant almost immediately. The document provides no unique model, data moat, regulatory certification, or exclusive integrations that would prevent quick copy by others.
  -> What specific, non-replicable capability (proprietary data, exclusive integrations, regulated certification, or stickiness) prevents large incumbents from copying this in weeks?

- **Pricing is exposed to bundling and undercutting** [HIGH] (pricing)
  Charging £149 per clinic per month is presented with no evidence of willingness-to-pay; a larger vendor can bundle an equivalent feature into existing subscriptions or offer freemium/discounted trials to their installed base, making the standalone price impossible to sustain. The plan lacks price testing, tiers, or a defensible reason why clinics would pay that amount versus a cheaper bundled alternative.
  -> Why will clinics pay £149/mo for a single assistant rather than accept an equivalent as a free/bundled add-on from their existing booking/EHR supplier?

- **Go-to-market and acquisition plan is missing and easily blocked** [HIGH] (acquisition)
  No customer acquisition strategy is provided. Incumbents and platform owners control the channels to clinics (marketplaces, resellers, billing relationships, app stores) and can prioritize or preinstall a competing assistant, starving you of reach. Without a distribution edge or channel partnerships, you will struggle to scale and are vulnerable to being cut off by platform gatekeepers.
  -> What's the specific, testable acquisition channel (partnership, marketplace, installed-base sales, or direct channel) you will use and how will you get initial clinics without platform owners blocking or bundling the feature?

- **Trust, compliance and clinical risk are unaddressed — incumbents have advantage** [MEDIUM] (demand_evidence)
  Patient communication and appointment handling involve data protection and clinical safety risk; clinics are likely risk-averse and prefer trusted vendors with certifications and long-standing support. Large established vendors can leverage existing trust, contracts, and compliance certifications to displace a new entrant unless you can prove safe handling and liability coverage.
  -> How will you validate clinics' trust in your assistant and demonstrate compliance (data protection, liability, clinical safety) before launch to overcome incumbents' trust advantage?

- **Integration effort and switching cost glossed over** [MEDIUM] (assumptions)
  You state you will integrate with existing booking systems, but don't specify which ones or how deep the integration is. Incumbents controlling booking software can add the feature with minimal friction; for you, engineering, partnership negotiations, and maintenance across multiple vendors create friction and cost that slow adoption. This makes the product vulnerable to faster, simpler incumbent rollouts.
  -> Which booking systems will you integrate first, and what's the cheapest experiment to validate both technical feasibility and clinics' willingness to switch or add another vendor?

### execution_risk

The plan has directionally sensible goals but skips several execution blockers that will stop shipping: clinical-data compliance, fragile multi-vendor integrations, and no acquisition path for busy private clinics. The document also assumes a price and a delivery timeline/team capacity without evidence, and risks building hard ML work before validating core clinic workflows.

- **GDPR / clinical data compliance is unaddressed and will block pilots** [HIGH] (assumptions)
  You plan to handle patient queries and appointment data but state nothing about lawful bases, Data Processing Agreements, patient consent flows, UK data residency, or clinical-data handling controls. Concrete failure mode: clinics will refuse to connect real patient data without a DPA, indemnities, or evidence of secure hosting and processes; regulators could require changes that force a rewrite or prevent live testing. This is a pre-launch blocker for any paid pilot with real patients.
  -> Before onboarding a single clinic, what precise legal/compliance artifacts (DPA, DPIA, data residency, security certifications, logging/audit controls, and patient consent flow) will you have in place?

- **Integration hell: unspecified booking systems and connector work** [HIGH] (assumptions)
  You say 'integrate with existing booking systems' but list no target providers or integration approaches. Concrete failure mode: each clinic uses different, sometimes closed or legacy booking platforms (or bespoke systems), forcing per-clinic connector builds, screen-scraping, or manual processes that can take weeks–months each. That will blow time and budget and prevent a scalable pilot.
  -> Which specific booking systems will you support for the first 10 clinics and what is your plan (API, webhook, partner, or automated UI) and estimated engineering effort per system?

- **No acquisition / onboarding plan for B2B clinics** [HIGH] (acquisition)
  You target small private clinics but provide no channel, sales motion, or onboarding process. Concrete failure mode: product gets built but you can't get clinics to trial (busy owners, risk-averse, need references), leaving the product unused. Also onboarding requirements (training, consent, SLA) are unstated and likely to require human support, increasing costs and slowing adoption.
  -> What is the concrete first scalable acquisition channel (e.g., partnerships, local reps, referral pilots) and how many outreach/conversations/week will you need to sign your first 10 paying clinics?

- **Price (£149/mo) is asserted with no evidence of willingness-to-pay** [MEDIUM] (pricing)
  You set a single price but provide no validation that small private clinics will pay £149/month for messaging/booking automation. Concrete failure mode: clinics decline or request trial periods, leading to low conversion and poor early revenue. Without testing, you risk iterating on product-market fit at the wrong price point.
  -> Who is the economic buyer that will sign a £149/mo contract and what evidence (pilot commitments, letters of intent, pre-sales) do you have that they will pay that amount?

- **Team size / timeline not specified — likely underestimates work** [MEDIUM] (assumptions)
  No team composition, hiring plan, or timelines are stated despite integration, ML, security, and B2B onboarding work. Concrete failure mode: founders assume a short build window and find integrations, compliance, and support require months and additional hires, causing missed deadlines and funding burn. The scope (connectors + ML assistant + support) is often 6+ months for a small team.
  -> Who is on the execution team today (engineers, security, ops, sales) and what is your realistic timeline and milestones for the first integrated pilot?

- **Sequencing risk: building full ML assistant before validating clinic workflows** [MEDIUM] (assumptions)
  You plan an AI assistant but don't describe validating the target workflows, common query types, or whether automation can safely handle them. Concrete failure mode: you invest heavily in NLP and integration work only to find queries are rare, highly variable, or require clinical judgment, forcing major rework. A simpler manual or rules-based pilot could reveal real patterns before ML development.
  -> What is your minimal viable experiment to validate the exact messages and appointment workflows (e.g., a concierge/manual handling pilot) before building ML or connectors?

### evidence_audit

Evidence base: Weak. The plan is pre-launch with only a stated product, price (£149/mo) and UK focus. The most important gap is lack of measured demand, buyer definition and acquisition/CAC evidence to support revenue assumptions.

- **No evidence clinics want or will pay for this (demand untested)** [HIGH] (demand_evidence)
  The document gives no measured demand signals (no pilot, interviews, surveys or letters of intent). Without at least one real clinic committing or a small pilot showing willingness to pay £149/month, revenue assumptions are unsupported. At £149/mo a single clinic yields £1,788/year; that per-unit revenue is only useful if adoption is real.
  -> Show one of: (a) results of X customer interviews with explicit willingness-to-pay at £149, (b) a signed pilot agreement from a UK private clinic, or (c) results of a pricing test (conversion and uptake) with at least N clinics — which of these can you provide and what are the results?

- **Target buyer and clinic segment are undefined** [HIGH] (buyer)
  The plan says 'small private clinics' but doesn't define clinic size, specialty, payer type, or the decision-maker who would pay £149/mo (owner, manager, chain). Different segments have very different budgets and purchase processes; the absence of a defined buyer prevents estimating conversion or sales cycle. This is load-bearing because the acquisition approach and willingness-to-pay depend on it.
  -> Specify the target clinic profile (e.g., # of clinicians, revenue band, specialties, independent vs. multi-site) and the paying buyer role, and provide an estimate of how many such clinics exist in the UK or one measured example matching that profile.

- **No customer acquisition plan or CAC inputs (funnels missing)** [HIGH] (acquisition)
  There is no acquisition funnel, expected conversion rates, or CAC. Without CAC and expected sign-up rates, you cannot translate a per-clinic price into a business model. For context: each clinic = £149/mo = £1,788/year, so signing 100 clinics is £178,800/year; whether that is reachable depends entirely on CAC and conversion which are unstated.
  -> Provide a concrete acquisition funnel: channels, conversion rates at each step, and an expected CAC (or historical CAC from pilots) — if unknown, run a 4-week outreach pilot and report leads → trials → paid conversions so we can compute CAC.

- **Price given but no evidence/pricing rationale** [MEDIUM] (pricing)
  Price is stated as £149/month but there is no justification or comparison to alternatives, total clinic economics, or willingness-to-pay tests. Stating a price without evidence is an assumption that could be load-bearing: if clinics won't pay £149, unit economics collapse. The only implied arithmetic available is £149×12 = £1,788 ARR per clinic.
  -> Provide evidence supporting £149/mo (e.g., results of pricing experiments, quoted competitor pricing and position, or documented willingness-to-pay from at least 10 target clinics).

- **No market sizing or revenue targets (key numbers missing)** [MEDIUM] (key_numbers)
  The doc lacks UK market size (number of target small private clinics), revenue or customer targets, and a timeline. Using the stated price: one clinic = £1,788/year, therefore reaching £1M ARR would require ~560 clinics (1,000,000/1,788 ≈ 559.6). Without stated targets, scale and feasibility can't be judged.
  -> State the target ARR and timeline and provide your estimate of the count of target clinics in the UK (with source) so we can check feasibility (e.g., to reach X ARR you need Y clinics = X/1,788).


## Selected questions

- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / £149/month price is asserted with no willingness-to-pay evidence [high]
  - why we're asking: unit_economics / Asserting £149/mo without any willingness-to-pay evidence [high]
  - why we're asking: adversarial_competitor / Pricing is exposed to bundling and undercutting [high]
  - why we're asking: execution_risk / Price (£149/mo) is asserted with no evidence of willingness-to-pay [medium]
  - why we're asking: evidence_audit / Price given but no evidence/pricing rationale [medium]
- **acquisition**: How will your first customers find you?
  - why we're asking: unit_economics / Customer acquisition channels and realistic CAC are unspecified [high]
  - why we're asking: adversarial_competitor / Go-to-market and acquisition plan is missing and easily blocked [high]
  - why we're asking: execution_risk / No acquisition / onboarding plan for B2B clinics [high]
  - why we're asking: evidence_audit / No customer acquisition plan or CAC inputs (funnels missing) [high]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / No evidence clinics will route live patient communications to an AI [high]
  - why we're asking: unit_economics / No plan or cheap test to validate demand and price before building [low]
  - why we're asking: adversarial_competitor / Trust, compliance and clinical risk are unaddressed — incumbents have advantage [medium]
  - why we're asking: evidence_audit / No evidence clinics want or will pay for this (demand untested) [high]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No per-clinic cost-to-serve or integration cost model [high]
  - why we're asking: unit_economics / No LTV, churn, payback period or sensitivity analysis [medium]
  - why we're asking: evidence_audit / No market sizing or revenue targets (key numbers missing) [medium]

## Answer given

**demand_evidence**: We have not run any pilots and no clinic has committed to using or paying for it yet.

Skipped: pricing, acquisition, key_numbers

## Refined critique

### pre_mortem

The plan rests on untested core assumptions: that the product can reliably integrate with the booking systems clinics actually use, that clinics will pay £149/month, and that there is real demand among UK private clinics. The most likely single killing-blow is an integration blocker (no APIs, fragmented/legacy systems or restricted access) that makes automatic appointment/query handling impossible. Several other key gaps (who the buyer is, how to acquire clinics, and whether clinics/patients accept AI handling) are unstated and unvalidated.

- **Integration with clinic booking systems assumed feasible** [CRITICAL] (assumptions)
  The strategy assumes you can 'integrate with existing booking systems' but names no vendors or evidence about API availability, data access, or contractual permissions. If target clinics use a wide variety of legacy or closed systems, or if vendors restrict automated access, the assistant cannot perform its core function. This is a practical blocker: without integration, there is no product to sell.
  -> Which specific booking systems do target clinics use and can you reliably access the APIs/data needed to manage appointments at scale?

- **Price point (£149/mo) unvalidated with customers** [HIGH] (pricing)
  The founder has picked a flat £149/month per clinic without testing willingness to pay or willingness to switch from current processes. There's no evidence this price matches clinics' perceived value, budget, or procurement thresholds. If clinics perceive the value below this price they will not purchase.
  -> Will target clinics actually commit to paying £149/month for this service in a real purchase or paid pilot?

- **No demand evidence or pilot commitments** [HIGH] (demand_evidence)
  Founder admits no pilots run and no clinic has committed. The core product-market fit assumption — that small private clinics want outsourced/automated appointment & query handling — is untested. Without at least pilot agreements or pre-sells, build-out risks delivering a product nobody adopts.
  -> Can you secure pilot agreements, letters of intent, or paid trials from target clinics before continuing full development?

- **Buyer / decision-maker in clinic not identified** [HIGH] (buyer)
  The plan targets 'small private clinics' but does not specify who will evaluate and pay for the service (practice owner, practice manager, receptionist, or external management company). Different buyers have different pain points, budgets, and procurement processes; this ambiguity undermines pricing, acquisition and product decisions.
  -> Who is the specific buyer and decision-maker at the clinics, and what is their procurement process and budget authority?

- **Assumes clinics want AI handling patient queries (possible misread of preferences)** [MEDIUM] (alternatives)
  The product assumes clinics will be comfortable with AI handling patient queries and appointment requests, but no user research is shown about patient acceptance or clinics' tolerance for automated responses. Clinics may prioritize a human touch, clinical safety, or liability concerns that make them reluctant to deploy AI on patient-facing interactions.
  -> Do clinic staff and patients accept AI-handled communications for queries/appointments, and under what safeguards or limits?

- **Go-to-market / acquisition route is unspecified** [MEDIUM] (acquisition)
  There is no plan or evidence about how you will reach and convince small UK clinics to trial or buy the service (direct sales, partnerships, resellers, marketplace, trade bodies). Without validated acquisition channels and early-conversion signals, demand cannot be scaled even if product assumptions hold.
  -> What are the lowest-cost channels to acquire clinic customers and can you validate conversion through a small outreach experiment?

### evidence_audit

Evidence base: Weak. The document is pre-launch with no pilots, revenue, or customer commitments—only a stated price and broad target market. The most important remaining issue is the lack of any measured demand or willingness-to-pay evidence to validate the £149/month assumption.

- **No measured demand or willingness-to-pay evidence** [HIGH] (demand_evidence)
  The founder explicitly reports no pilots and no clinic commitments; there is therefore no measured evidence that clinics will adopt or pay for the product. At this stage a signed trial, paid pilot, or quantified demand survey is the minimal evidence required to validate the commercial hypothesis. Without any such proof the core claim that clinics will pay £149/mo is untested and load-bearing for the business.
  -> Provide a measured commitment: either a signed paid pilot (one or more UK clinics agreeing to pay £149/month for a trial period) or quantified results from a demand test (number approached, responses, and explicit willingness-to-pay at £149).

- **Price point (£149/mo) is unsupported and unexplained** [HIGH] (pricing)
  The plan states a price of £149 per clinic per month but gives no sourcing or rationale (no willingness-to-pay studies, competitor comparators, or cost-based justification). That single price drives revenue per customer: £149 × 12 = £1,788 per clinic per year, so each clinic contributes £1,788 ARR. The viability of the business depends heavily on that number but it is an unstated assumption with no test plan.
  -> How was £149/month derived—provide the empirical basis (customer interview willingness-to-pay data, competitor pricing comparisons, or a commitment at that price) or an A/B pricing test plan to validate it.

- **Customer segment is too vague to size or prioritise** [MEDIUM] (buyer)
  Labeling the target buyer as 'small private clinics' does not specify who the decision-maker is, clinic size (appointments/day), or an addressable count in the UK. That ambiguity prevents sizing the market, estimating onboarding effort, or designing a targeted outreach test. For a pre-launch idea you must define an initial narrow segment to run pilots and measure conversion.
  -> Define the initial target buyer precisely (decision-maker title, clinic size by staff/appointments or revenue) and provide an estimate of the number of such clinics in the UK you can realistically reach for pilots.

- **No acquisition plan or CAC estimates to reach customers** [MEDIUM] (acquisition)
  The document includes no channels, outreach tactics, or estimates of conversion and customer-acquisition-cost (CAC). Without those inputs you cannot estimate how many leads, trials or sales efforts are required to secure even one paying clinic, or whether £149/mo covers acquisition costs. This is a practical testable gap for pre-launch validation.
  -> State the initial acquisition method(s) you will use for pilots and provide expected conversion rates and a target CAC (or an explicit plan to measure CAC in a first 10-clinic outreach batch).

- **Integration feasibility with booking systems is unstated** [MEDIUM] (assumptions)
  The product depends on integrating with existing booking systems, but no target systems, their API availability, or integration complexity are documented. Integration feasibility will materially affect time-to-pilot and the product's ability to deliver value; it is an assumption that must be tested before scaling. Lack of this information risks underestimating development/time-to-revenue.
  -> List the booking systems you plan to integrate with and for each provide evidence of a viable integration path (public API, partner agreement, or confirmation from a vendor/customer that integration is feasible).

- **Missing unit-economics and load-bearing key numbers (CAC, conversion, churn)** [LOW] (key_numbers)
  There are no stated assumptions for conversion rates, churn, or CAC and no revenue targets or clinic-count goals tied to the £149 price. For example, at £149/mo a single clinic yields £1,788 ARR; but without targets you cannot compute how many clinics are needed to cover development or marketing costs. These are necessary for planning tests and milestones.
  -> Provide target unit-economics for launch testing: expected trial-to-paid conversion, expected monthly churn, and a provisional CAC (or a plan to measure these within the first N pilot outreach attempts).


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['pricing', 'acquisition', 'key_numbers']

## Reuse check

Re-sending the same refinement token refused with 409: yes
