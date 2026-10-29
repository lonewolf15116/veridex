# T10-industrial-ai

**Stage:** building

## Input

We're building AI software that monitors industrial equipment for early signs of mechanical failure. We intend to sell annual contracts for $24,000 to large manufacturers, with a target of 15 customers in our first three months. We have two engineers, no dedicated sales staff and no confirmed pilot customers.

**Reviewer expectation:** questions enterprise sales cycles, engineering capacity, integration/deployment; no fabricated customer rejections or procurement timelines.

## First critique

### pre_mortem

The plan rests on several unvalidated assumptions about customers, pricing, and go-to-market that are unlikely to survive real-world sales cycles in heavy industry. The most consequential mistake is the timeline/GT M assumption: expecting 15 annual-contract enterprise customers in three months with two engineers and no pilots or sales resources. Several other core gaps (who the buyer is, whether $24k matches customer willingness to pay, and how this product is meaningfully different from today's solutions) are untested and could each fatally undermine adoption.

- **Impossible customer ramp: 15 enterprise contracts in 3 months with no sales or pilots** [CRITICAL] (acquisition)
  The plan assumes you will convert 15 large manufacturers to $24k annual contracts within three months while having only two engineers, no dedicated sales staff, and no confirmed pilots. This ignores typical enterprise procurement timelines, need for procurement/IT/security approvals, and the usual requirement for pilots/proofs-of-concept before contract signing. Either the timeline or resource plan must be wrong for the stated target to be achievable.
  -> How exactly will you close 15 enterprise deals in three months without sales capacity or pre-existing pilots — name the signed commitments and the shortened procurement steps that make this possible?

- **Price point ($24k/yr) is asserted with no evidence of willingness-to-pay** [HIGH] (pricing)
  You state a $24,000 annual contract price but provide no evidence that large manufacturers will pay that amount for your AI monitoring, nor what that price covers (per site, per asset, support, SLA). Without mapping price to quantified value (downtime avoided, maintenance cost savings) or testing buyer willingness, the price could be too high, too low, or the wrong billing unit. If customers do not see clear ROI at that price, the sales goal collapses.
  -> What customer evidence or calculations show that a named buyer would accept $24k/yr for this product, and what's the smallest experiment to validate that willingness-to-pay?

- **Vague buyer definition — 'large manufacturers' is too broad; buying process unknown** [HIGH] (buyer)
  Identifying the customer as 'large manufacturers' omits who within those organizations decides and signs on industrial monitoring software (maintenance managers, reliability engineers, procurement, plant managers), and says nothing about purchase cadence or pilots required. Enterprise B2B sales typically require champions, procurement cycles, and site-specific validation. Without a clear buyer persona and mapped decision process, you cannot target outreach or design the pilot that will convert.
  -> Who exactly within a target manufacturer is the buyer and decision-maker for this product, and how long does their approval process take?

- **No demand evidence or pilots to validate that customers actually want your specific monitoring solution** [MEDIUM] (demand_evidence)
  You have zero confirmed pilot customers and no cited evidence of demand: no letters of intent, no discovery interviews, and no early adopters. Industrial customers often require asset-specific validation of predictive models and integration tests before committing. Without at least one pilot demonstrating model accuracy and integration, the central demand hypothesis remains untested.
  -> Can you secure a low-effort pilot (one asset, one plant, short duration) and what is the cheapest way to validate model performance and integration with a customer's workflow?

- **Unclear differentiation vs existing monitoring methods and vendors** [MEDIUM] (alternatives)
  The strategy doesn't explain why manufacturers would switch from current alternatives (OEM monitoring, SCADA, manual inspections, third-party service contracts) to your AI software. Without clear differentiation—better accuracy, lower false positives, easier integration, regulatory alignment—customers have no reason to change established, risk-averse maintenance processes. This makes conversion unlikely even if the core model works.
  -> What specific, testable advantages does your product offer over the exact alternatives a named customer currently uses, and how will you prove that in a pilot?

- **Assumes two engineers can deliver production-ready, plant-grade AI monitoring without clarity on scope** [MEDIUM] (assumptions)
  You assume the engineering team can build a deployable, reliable industrial AI monitoring product, but provide no definition of minimum viable scope (supported asset types, data requirements, integration surface, SLAs) or evidence that two engineers can meet industrial reliability/compliance needs. If the product cannot be safely integrated into plant operations, customers will refuse pilots or contracts.
  -> What is the minimal technical scope needed to run a credible pilot on a single asset class, and can your current team deliver that within the proposed timeline?

### unit_economics

The document states a headline price ($24k/year) and an aggressive 15-customer target in 3 months but contains almost no unit-economic detail. Key inputs are missing: cost to serve a customer, CAC by channel, evidence customers will pay $24k, gross margin and payback calculations, and hidden/ongoing costs (onboarding, integration, SLAs). Without those numbers the plan’s financial feasibility and the claimed early traction target are unsupported.

- **Claim of 15 enterprise customers in 3 months is infeasible given no sales resources** [CRITICAL] (acquisition)
  The plan targets 15 enterprise contracts in the first 90 days but the team is two engineers with no dedicated sales staff, no pilots, and no pipeline. Enterprise sales for $24k ARR typically require outreach, pilots, legal/ procurement cycles and dedicated closers; the document provides no channel, conversion, sales-cycle time, or evidence this can be done. This is an internal contradiction: the stated resources cannot credibly produce the stated customer count in that timeframe.
  -> How exactly will you acquire and close 15 enterprise contracts in 90 days — specify channels, required hires or partners, expected conversion rates, and sales-cycle length that make this possible?

- **Price ($24k/yr) has no supporting willingness-to-pay evidence** [HIGH] (pricing)
  The $24k annual price is asserted but there are no pilots, LOIs, customer interviews, ROI calculations, or comparable market benchmarks presented to justify it. For enterprise offerings, willingness-to-pay should be tied to measurable savings (downtime avoided, replacement cost) and supported by customer validation; none is provided. Without that, revenue per user is an unsupported assumption.
  -> What evidence (signed pilots, LOIs, customer ROI calculations, or comparable market pricing) shows target customers will pay $24k/year for this service?

- **No CAC estimates or realistic channel plan for enterprise deals** [HIGH] (acquisition)
  The document includes no customer acquisition cost (CAC) estimates, nor a channel mix (organic, outbound SDR, partnerships, trade shows) to plausibly acquire enterprise accounts. At $24k ARR, CAC can vary widely and materially affect payback and unit economics; claiming rapid scale without CAC assumptions is unsupported. The absence of CAC means LTV/CAC and payback period cannot be calculated.
  -> Provide projected CAC by channel (and why those channels are realistic given your team) and the assumptions used to derive them (conversion rates, lead costs, sales time).

- **Per-customer cost-to-serve is unspecified (compute, storage, integration, support)** [MEDIUM] (key_numbers)
  There are no line items for ongoing costs: model inference/hosting, data storage, retraining, per-customer integrations, onboarding engineering hours, or support SLAs. These costs can be large for industrial deployments (edge devices, integrations with PLC/SCADA, secure networks) and will directly compress gross margin. Without per-customer OPEX you cannot forecast gross margin or scalability.
  -> Provide an itemized per-customer estimate for compute, storage, model inference/retraining, onboarding/integration engineering hours, and support FTE allocation.

- **Gross margin, payback period and hidden recurring costs are unmodelled** [MEDIUM] (key_numbers)
  No gross margin or CAC payback calculations are shown. Hidden or recurring costs common in industrial SaaS — custom integrations, compliance/certifications, liability/insurance, site visits, long pilot periods, and potential refunds/chargebacks — are not considered. These could push payback beyond acceptable limits and make $24k ARR uneconomic.
  -> What are your projected gross margin and CAC payback period at 15 customers and at scale, and which specific cost items could extend payback beyond 12 months?

### adversarial_competitor

You claim an AI condition-monitoring product selling $24k/year to large manufacturers and plan to sign 15 customers in three months, but you have two engineers, no sales team, and no pilots. This is a classic easy-to-neutralize startup: the core tech is incremental (anomaly detection), incumbent platforms can add it quickly, and well-funded competitors can use distribution, free pilots, aggressive pricing, and brand/trust to make your offering redundant before launch. Before you build, you must prove buyer demand, willing-to-pay, and a credible route to enterprise deals.

- **No customer acquisition plan — 15 enterprise deals in 3 months is unsupported** [HIGH] (acquisition)
  You state a target of 15 customers in three months yet have two engineers, no sales hires, and no pilots or channel partners. Enterprise deals typically require pilots, stakeholder alignment, procurement reviews and integrations — none of which you’ve planned for. A well-funded competitor can neutralize you cheaply by offering free short pilots or integrating detection into existing platforms and converting their installed base.
  -> How exactly will you close 15 enterprise annual contracts in three months with your current team and no pilots or sales channels?

- **No evidence customers will pay $24k/year — pricing looks assumed** [HIGH] (demand_evidence)
  You state an annual price of $24,000 but provide no evidence of willingness-to-pay, decision-maker, or ROI support. Without pilots or customer conversations, that price is speculative and easy for competitors to undercut with free trials or deeply discounted initial deployments. A competitor can make you irrelevant by proving ROI to shared prospects first and offering better commercial terms.
  -> What customer interviews, pilots or ROI calculations validate that large manufacturers will commit to $24k/year for your product?

- **Differentiation is vague — incumbents can replicate quickly** [HIGH] (differentiation)
  You describe 'AI software that monitors equipment' but don’t state the unique model, sensor integrations, or outcomes that are proprietary. Basic anomaly detection and alerting is an incremental feature that existing CMMS, PLC vendors, and condition-monitoring SaaS can add in months. The cheapest kill is for an incumbent to ship an 'AI alerts' add-on or a turnkey pilot bundle into their large installed base.
  -> What specific technical or data advantage do you have that an incumbent or platform vendor cannot reproduce within 3–6 months?

- **Pricing and buyer are misaligned — unclear who signs the check** [MEDIUM] (pricing)
  You list a single price but haven’t defined the buyer (plant manager, reliability engineer, corporate procurement) or procurement constraints. Enterprise purchases are negotiated and often bundled with other services; a competitor with channel leverage can offer tied pricing or bundled discounts that you can’t match as a new entrant. Without buyer clarity you’ll miss the right economics and contract structure.
  -> Who is the actual contract buyer and approver for the $24k price, and why will they prefer this standalone annual contract versus an incumbent bundle?

- **Target customer ('large manufacturers') is too broad — no vertical focus** [MEDIUM] (buyer)
  Labeling your customers as 'large manufacturers' leaves out which industries, asset types, or plant profiles you target first. Different subsegments have different sensor stacks, procurement models, and risk tolerance. A well-funded competitor can pick the narrowest, highest-value vertical (e.g., cement, petrochemical, or high-throughput assembly) and dominate with tailored integrations and references.
  -> Which manufacturing verticals, asset classes, and buyer personas are you prioritizing for your initial 15 customers?

- **Ambitious early growth target lacks supporting numbers (sales cycle, CAC, conversion)** [LOW] (key_numbers)
  You provided a headline target (15 customers in three months) but no supporting funnel metrics — expected sales cycle length, conversion rate from pilot to paid, or customer acquisition cost. These are critical to assess feasibility and allow competitors to calculate attack vectors (e.g., subsidized pilots, bundled sales). The cheapest tests are landing pages, low-effort pilots, and advisor-signed letters of intent.
  -> What are your assumed sales cycle, pilot-to-paid conversion rate, and CAC that make 15 customers in three months possible?

### execution_risk

The plan radically underestimates what it takes to ship an enterprise industrial-AI product: two engineers, no pilots, and no sales staff cannot reasonably deliver 15 $24k/year contracts in three months. Major technical, integration, compliance, and go-to-market blockers are either unstated or sequenced incorrectly and will stop pilots and sales cold unless resolved first.

- **Target of 15 enterprise customers in 3 months is operationally impossible with two engineers and no sales staff** [CRITICAL] (acquisition)
  Enterprise sales require pipeline building, pilot agreements, security reviews, legal/contract negotiation and procurement cycles that typically take months. With no dedicated sales/resource capacity and zero confirmed pilots, the stated go-live target and revenue plan cannot be achieved as written. Expect zero or very few signed contracts in that window unless the team radically changes resources or narrows scope.
  -> Exactly how will you source, run pilots with, negotiate contracts for, and close 15 manufacturers within 90 days with only two engineers and no sales hires or channel partners?

- **No confirmed pilots or access to real sensor/failure data — models can’t be built or validated** [HIGH] (demand_evidence)
  Mechanical-failure detection depends on historical sensor telemetry and labeled failure events; those datasets are rarely available and failure events are infrequent. The doc lists no pilot commitments or data-sharing agreements, so the engineering effort risks building models that don’t work on customer data or need extensive rework once real telemetry arrives.
  -> Which customers have committed to provide historical sensor data, streaming telemetry, or labeled failure events for training and POC, and by when?

- **OT/SCADA/PLC integration complexity is underestimated and will create engineering bottlenecks** [HIGH] (assumptions)
  Industrial environments use many protocols, bespoke PLCs, strict network segmentation, and vendor-specific tooling; each new customer may require custom connectors, edge agents, or on-prem deployment. Two generalist engineers cannot build and maintain the variety of integrations needed to support multiple large manufacturers concurrently.
  -> Which specific equipment/vendors/protocols will you support first, and do you have access to those live systems for integration testing and deployment validation?

- **Security, compliance and procurement requirements are unaddressed and will block pilots** [HIGH] (assumptions)
  Large manufacturers typically require vendor security questionnaires, SOC2/ISO controls, OT-network hardening, and legal review before any data or connectivity is allowed. The plan includes none of these controls, meaning expected pilots and contracts will be delayed by lengthy vendor-risk processes or outright denied.
  -> What security controls, certifications, and procurement approvals will you have in place before any customer allows network access or data sharing, and who is owning these efforts?

- **Sequencing: building broad product before securing at least one fast POC will waste engineering effort** [MEDIUM] (acquisition)
  The team appears to be building product prior to validating that the approach works on customer environments, which will likely result in costly rework once real data and integration constraints surface. A focused pilot or synthetic lab test should come first to de-risk model assumptions and integration needs.
  -> Can you commit to a 2–6 week narrow POC with one partner or public/simulated dataset to validate detection approach before expanding engineering scope?

- **Pricing and buyer role are unvalidated — $24k/year may not map to the actual buyer or procurement process** [MEDIUM] (pricing)
  The $24k annual price assumes a straightforward buyer and purchase decision; the doc does not state who (plant manager, maintenance, corporate engineering, procurement) signs or whether that buyer has budget authority for recurring software plus integration services. Missing validation risks rejection of pricing or need for expensive professional services.
  -> Who within target customers is expected to be the buyer of a $24k/year contract, and have any prospects indicated they would pay this price level?

### evidence_audit

Evidence base: Weak. The plan is pre‑launch with no pilots, customers, or performance data; pricing and customer targets are unsupported. The most important remaining issues are missing measured detection performance on real industrial data and absent buyer commitments to validate $24k/year and 15 customers in three months.

- **No measured pilot or detection performance on real industrial data** [HIGH] (demand_evidence)
  You claim an AI that detects early mechanical failure but report no pilots, tests, or historical-data backtests. For industrial monitoring the product's value hinges on measurable detection lead time, true/false positive rates and types of equipment — none are provided. Without measured performance, willingness-to-pay and onboarding expectations are unsupported.
  -> Provide measured pilot results or backtest on real industrial sensor data (sample size, equipment types, detection lead time and precision/recall or false positive rate) that demonstrate the model can detect failures early enough to be valuable.

- **$24k/year price and 15 customers in 3 months are unsupported by buyer commitments** [HIGH] (pricing)
  You state annual contracts of $24,000 and a target of 15 customers in three months (implies $360,000 ARR). There are no LOIs, paid pilots, or survey evidence that large manufacturers will pay $24k/year or convert quickly. Pricing and willingness-to-pay are load-bearing for revenue but are ungevidenced.
  -> Provide signed LOIs, paid pilot commitments, or documented buyer commitments from target manufacturers that demonstrate that at least some customers are willing to pay $24,000/year and that you can convert to paid contracts in the stated timeframe.

- **No acquisition funnel or pipeline to deliver 5 enterprise closes/month** [HIGH] (acquisition)
  15 customers in 3 months equals 5 closed enterprise deals per month. You report no sales staff, no pipeline and no conversion assumptions. Enterprise procurement and technical validation often require multiple meetings and trials; without a concrete funnel (leads → qualified → pilots → closes) the revenue target is unsupported.
  -> Provide a concrete acquisition funnel (current pipeline counts, lead sources, assumed conversion rates at each stage) showing how you will source the leads and close the 15 enterprise contracts within three months (i.e., how many leads/demos/pilots produce 5 closes/month).

- **Missing measured onboarding and integration time per customer** [MEDIUM] (key_numbers)
  Enterprise deployments require data ingestion, integration and model tuning; the plan implies onboarding 15 customers rapidly but gives no implementation timeline or resource estimates. If onboarding takes weeks/months, three-month target may be infeasible even with willing buyers.
  -> State the measured or estimated end-to-end onboarding time per customer (data integration → model validation → production) in days, and provide evidence or a breakdown supporting that estimate.


## Selected questions

- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Impossible customer ramp: 15 enterprise contracts in 3 months with no sales or pilots [critical]
  - why we're asking: unit_economics / Claim of 15 enterprise customers in 3 months is infeasible given no sales resources [critical]
  - why we're asking: unit_economics / No CAC estimates or realistic channel plan for enterprise deals [high]
  - why we're asking: adversarial_competitor / No customer acquisition plan — 15 enterprise deals in 3 months is unsupported [high]
  - why we're asking: execution_risk / Target of 15 enterprise customers in 3 months is operationally impossible with two engineers and no sales staff [critical]
  - why we're asking: execution_risk / Sequencing: building broad product before securing at least one fast POC will waste engineering effort [medium]
  - why we're asking: evidence_audit / No acquisition funnel or pipeline to deliver 5 enterprise closes/month [high]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Price point ($24k/yr) is asserted with no evidence of willingness-to-pay [high]
  - why we're asking: unit_economics / Price ($24k/yr) has no supporting willingness-to-pay evidence [high]
  - why we're asking: adversarial_competitor / Pricing and buyer are misaligned — unclear who signs the check [medium]
  - why we're asking: execution_risk / Pricing and buyer role are unvalidated — $24k/year may not map to the actual buyer or procurement process [medium]
  - why we're asking: evidence_audit / $24k/year price and 15 customers in 3 months are unsupported by buyer commitments [high]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / No demand evidence or pilots to validate that customers actually want your specific monitoring solution [medium]
  - why we're asking: adversarial_competitor / No evidence customers will pay $24k/year — pricing looks assumed [high]
  - why we're asking: execution_risk / No confirmed pilots or access to real sensor/failure data — models can’t be built or validated [high]
  - why we're asking: evidence_audit / No measured pilot or detection performance on real industrial data [high]
- **buyer**: Who has this problem? Be specific.
  - why we're asking: pre_mortem / Vague buyer definition — 'large manufacturers' is too broad; buying process unknown [high]
  - why we're asking: adversarial_competitor / Target customer ('large manufacturers') is too broad — no vertical focus [medium]

## Answer given

**demand_evidence**: We have not spoken to any manufacturers about buying this, and we have no confirmed pilots.

Skipped: acquisition, pricing, buyer

## Refined critique

### pre_mortem

The strategy rests on unvalidated demand and multiple unstated go-to-market assumptions. The founder projects 15 $24k enterprise contracts in 3 months without any customer conversations, pilots, a sales plan, or clarity on the buyer — any one of which could collapse the plan. The most likely killing blow is simple: prospective manufacturers decline to commit to paid pilots or annual contracts because the team has not demonstrated value or secured access to operational data.

- **No demand evidence — zero customer conversations or pilots** [CRITICAL] (demand_evidence)
  The founder admits they have not spoken to any manufacturers and have no confirmed pilots, yet assumes immediate enterprise demand. Building a product for an unvalidated need (15 customers in 3 months) risks producing something nobody will buy. This is the foundational assumption: if customers don't want it, nothing else matters.
  -> Which specific manufacturers have agreed to a pilot or purchase, and can you get at least one signed LOI or paid pilot before proceeding?

- **Pricing claim ($24k/year) is unsupported by buyer research** [HIGH] (pricing)
  The plan states a $24k annual contract to 'large manufacturers' but the founder skipped 'who pays, and roughly how much'. There's no evidence that the relevant buyer (maintenance manager, operations, procurement) sees $24k as the right price or will accept subscription billing for this solution. If the assumed price is wrong, the commercial model and sales targets are invalid.
  -> Who (exact role/title) will sign a $24k/year contract and have they confirmed willingness to pay that amount for this solution?

- **Unrealistic early customer target — ignores enterprise sales and pilot timelines** [HIGH] (acquisition)
  Targeting 15 enterprise customers within the first three months with two engineers and no sales staff presumes a short sales cycle and immediate readiness to buy. Large manufacturers typically require pilots, security reviews, legal procurement cycles and ROI proof; the plan contains no evidence those steps will be compressed or skipped. If pilots are required (and they usually are), the 3-month target is unlikely to be met.
  -> What is the exact sales funnel and timeline that converts a cold enterprise lead into a paying annual contract within 90 days, and who has committed to each step?

- **Unknown buyer — who inside the manufacturer actually has the problem and budget?** [HIGH] (buyer)
  The document does not specify which function (operations, maintenance, reliability engineering, procurement) is the customer decision-maker or payer. Different buyers have different success metrics, budgets, and procurement processes; failing to name and validate the buyer means the product could be built for someone who neither controls budget nor will adopt it.
  -> Which exact organizational role is the target buyer, and have you validated their pain, budget authority, and procurement constraints?

- **Unstated integration/data-access assumption — product may be infeasible without OT access** [MEDIUM] (assumptions)
  Success assumes you can access sensor/telemetry and integrate with industrial OT systems, but this is not discussed. Manufacturers often restrict data, use legacy protocols, or require extensive on-site integration and cybersecurity approvals. If you cannot reliably access the necessary data, the monitoring AI cannot deliver the promised early-failure signals.
  -> Can target customers provide the telemetry and integration access you need, and have any expressed willingness to allow that access under realistic security terms?

- **No clarity on differentiation or alternatives — who will switch from current practices?** [LOW] (differentiation)
  The plan does not state what customers use today (manual inspections, existing analytics, OEM services) nor why they would replace those with this product. Without understanding current alternatives and the switching cost, it's unclear how you will persuade adopters to change behavior and sign an annual contract.
  -> What do target customers use today to detect mechanical failure, and why will they choose your solution over that alternative?

### evidence_audit

Evidence base: Weak. This is a pre-launch plan with zero pilots, zero customer conversations and no validated pricing. The central revenue and early-customer claims (15 customers at $24k in 90 days) are unsupported and lack funnel or buyer-persona evidence.

- **15 customers in 90 days is asserted but unsupported** [HIGH] (acquisition)
  The plan targets 15 enterprise customers in the first three months, which at $24,000 each implies $360,000 in annual contracts (15 × $24,000 = $360,000). There are no pilots, no sales staff, and no described pipeline or conversion rates to justify acquiring 15 large manufacturers that quickly. This is a load-bearing forecast: without concrete commitments or funnel math it is just an aspiration.
  -> Provide either (A) signed commitments (contracts or LOIs) from 15 customers, or (B) a documented sales funnel showing lead volumes, staged conversion rates and timelines that mathematically produce 15 closed enterprise deals within 90 days (show the math).

- **Price point ($24k/yr) to large manufacturers is unvalidated** [HIGH] (pricing)
  You assume each customer will pay $24,000 per year but explicitly state you have not spoken to any manufacturers and have no pilots. Willingness-to-pay at enterprise scale is load-bearing: if target buyers won't accept $24k, the revenue forecast collapses. No evidence (surveys, interviews, LOIs) is provided to support this pricing.
  -> Show direct validation that the specified buyer(s) would pay $24,000/yr — e.g., documented quotes from at least five independent target buyers, signed price LOIs, or at least one paid pilot at that price.

- **Key funnel and unit economics (CAC, sales cycle, LTV) are missing** [MEDIUM] (key_numbers)
  With a target of 15 customers, you must demonstrate acceptable acquisition cost and sales cadence. No CAC, sales-cycle length, expected conversion rates, or customer lifetime are provided, so it's impossible to judge whether the $24k ARPA supports sustainable acquisition economics. For example, if average customer lifetime is unknown, LTV cannot be computed to compare to CAC.
  -> Supply your assumed or measured CAC, expected sales cycle (days), conversion rates at each funnel stage, and assumed customer lifetime (or LTV), and show the arithmetic proving those inputs support 15 customers in 90 days and acceptable payback.

- **No demand evidence — zero customer discovery or pilots** [MEDIUM] (demand_evidence)
  You state explicitly you have not spoken to any manufacturers and have no confirmed pilots. At idea/pre-launch stage this is the most direct evidence gap: without discovery interviews or a pilot, the product-market fit and practical deployability to industrial equipment operators are unknown. This prevents assessing whether the feature set and integration needs match buyer expectations.
  -> Run and document at least 10 structured discovery interviews with the target buyer personas and secure at least one pilot or written pilot commitment; provide notes summarizing pain, current alternatives, and willingness to pilot/pay.

- **Target buyer and decision-maker are not specified** [MEDIUM] (buyer)
  The document says 'large manufacturers' but does not specify which function pays (maintenance/operations/plant manager), company size threshold, industry vertical, or procurement process. Without a clear buyer persona you cannot design the sales approach nor judge the plausibility of rapid enterprise sign-ups.
  -> Define the exact buyer persona(s) (title, department, company size and vertical) and provide evidence (interview notes or org charts) that these personas have budget authority or influence for $24k/year decisions.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['acquisition', 'pricing', 'buyer']

## Reuse check

Re-sending the same refinement token refused with 409: yes
