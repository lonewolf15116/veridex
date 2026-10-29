# T07-fitness-saas

**Stage:** traction

## Input

We sell scheduling software to independent fitness studios for £89 per month. We currently have 24 paying studios, £2,136 in monthly recurring revenue and 3 cancellations over the past six months. We want to expand through referrals and partnerships with fitness instructors.

**Reviewer expectation:** CONTROL - credits reported revenue/customers, asks for cohort/acquisition/retention detail, never calls founder-reported metrics independently verified.

## First critique

### pre_mortem

The plan extrapolated from a small, early cohort and hinged on instructor-driven referrals without validating the incentives or buyer alignment. Several core assumptions were untested: that instructors would reliably generate studio signups, that 24 paying studios + few cancellations equals product-market fit, and that £89/month is a scalable price point. The single most likely killer was that instructor partnerships produced little to no conversion because instructors lacked incentive or purchasing influence.

- **Killing-blow: assumed instructors would be an effective acquisition channel** [CRITICAL] (acquisition)
  The strategy explicitly depends on referrals and partnerships with fitness instructors as the growth engine, but there's no evidence instructors have the incentive, reach, or authority to refer/convert studios at scale. If instructors are independent contractors with weak influence over studio platform choices (or no incentive to introduce a paid product), the channel will yield negligible signups and growth stalls. This single failure would prevent scaling beyond the initial 24 studios.
  -> What concrete evidence (conversion rates, committed referral agreements, or compensating incentives) shows instructors will generate studio customers at scale?

- **Early retention interpreted as product-market fit without cohort data** [HIGH] (key_numbers)
  The doc treats 24 paying studios and three cancellations over six months as traction, but provides no cohort-level retention, activation, or new-signup velocity data. That hides whether growth is net-positive, whether cancellations concentrated in particular cohorts, or whether these studios are outliers (e.g., founder network). Assuming this observed stability will hold at scale was unsupported and likely false.
  -> Can you produce cohort-level signup and churn data demonstrating repeatable retention outside the initial users?

- **Buyer vs. referrer mismatch: studios pay but plan targets instructors** [HIGH] (buyer)
  The paying customer is independent fitness studios, yet the expansion plan targets fitness instructors as partners/referrers. The document doesn't show instructors are the decision-makers or even strong influencers in studio purchasing. This misalignment means the chosen growth lever may be incapable of converting the actual buyer.
  -> Who is the decision-maker for purchasing scheduling software at target studios, and what evidence do you have that instructors can and will influence that decision?

- **Pricing assumed to scale from 24 studios with no WTP testing** [MEDIUM] (pricing)
  Current MRR implies those 24 studios accept £89/month, but there's no evidence of segment-wide willingness to pay, price sensitivity, or value-based packaging. Scaling adoption across different studio sizes or geographies may reveal much lower willingness to pay or require different pricing tiers, undermining revenue projections tied to a single price point.
  -> What experiments or market research demonstrate that £89/month is acceptable across the broader target market and different studio segments?

- **Initial users may be unrepresentative (founder-network bias)** [MEDIUM] (demand_evidence)
  Nothing in the document distinguishes whether the first 24 studios came from the founder's network, early-adopter segment, or a representative sample. Treating their behavior as predictive of the wider market is an unstated assumption that likely failed when attempting to scale to less-engaged or more price-sensitive studios.
  -> How representative are the first 24 customers of the target market, and what evidence shows similar studios will adopt at the same rate?

### unit_economics

The document gives price (£89/mo) and current traction (24 customers, £2,136 MRR, 3 cancellations in six months) but omits virtually every cost and acquisition metric needed to validate unit economics. With no per-customer cost to serve, no CAC by channel, no churn rate/LTV calculation, and no evidence that £89 is a defensible price, you cannot compute gross margin, payback period, or scale viability. The stated growth channels (referrals and partnerships) are plausible but unsupported by conversion or cost data, so claims of scalable economics are unproven.

- **No fully loaded cost-to-serve per studio (cannot compute gross margin)** [CRITICAL] (key_numbers)
  The plan provides no breakdown of variable or fixed costs per studio — hosting, compute, storage, backups, third‑party APIs, payment processing fees, monitoring, or amortized engineering. Without a per-customer cost you cannot calculate gross margin or test whether £89/mo yields profitable unit economics at any scale. This omission prevents validation of sustainability even with current MRR.
  -> What is your fully loaded cost to serve one studio per month (hosting, storage, backups, monitoring, third‑party services, payment processing fees, and amortized engineering/support)?

- **CAC and acquisition economics are unspecified for the proposed channels** [HIGH] (acquisition)
  Founders say they will expand through referrals and partnerships with instructors but provide no CAC, conversion rates, or proof-of-concept pilots. At £89/mo, channel selection and economics matter — low-price discovery channels and partnership conversion rates can vary widely and may not be free. Without per-channel CAC and funnel metrics, you cannot calculate payback or decide whether growth is affordable.
  -> What are your measured CAC and conversion rates by channel (referral, partnership, paid acquisition) and how do those scale with spend?

- **Pricing/willingness-to-pay is inadequately validated beyond initial customers** [HIGH] (pricing)
  Price is stated as £89/mo but there is no evidence of how that figure was set, whether it was A/B tested, or how price sensitivity and downgrade behavior look. The sample of 24 studios is small and may not represent broader willingness-to-pay or enterprise customers. Without demonstrated renewal rates and willingness-to-pay data, projected revenue per user is an assumption, not a measured input.
  -> How was £89/month chosen and what percent of customers have renewed, upgraded/downgraded, or churned at that price point?

- **Churn/LTV and payback period are not computed despite partial churn signal** [MEDIUM] (key_numbers)
  You report 3 cancellations over six months but no base, cadence, or monthly churn rate is provided, so LTV cannot be calculated. Payback period requires CAC and LTV — both missing — so it's impossible to know how long it takes to recover acquisition cost or what growth breaks profitability. This leaves the business unable to model scale economics or sensitivity to churn.
  -> What is your monthly churn rate, resulting customer lifetime (or LTV at £89/mo), and the payback period given current CAC assumptions?

- **Hidden and operational costs (refunds, chargebacks, fraud, compliance, moderation) are unaccounted** [MEDIUM] (assumptions)
  No estimates are given for refunds/chargebacks, payment disputes, fraud mitigation, legal/regulatory compliance for fitness businesses, or content moderation/onboarding labor. These costs are often non-trivial for subscription SaaS and scale with customers/transactions. Omitting them risks understating true cost-to-serve and overstating gross margin at scale.
  -> What are your assumptions and estimated monthly costs/incidence rates for refunds, chargebacks, fraud prevention, and any regulatory/compliance obligations?

- **Support and onboarding cost per studio is unspecified** [LOW] (key_numbers)
  There is no data on the time or cost to onboard a new studio, nor on ongoing customer support load as the base grows. Support and onboarding are recurring or front-loaded costs that affect early CAC payback and gross margin but are not addressed. Without these numbers you can't model whether support will become a scaling constraint or hidden expense.
  -> How many support/onboarding hours does an average studio require and what is the cost to provide that (salary or outsourced rate) per studio?

### adversarial_competitor

This product shows early revenue but no defensible differentiation, a thin go-to-market plan, and an unsupported price point — all of which a well-funded incumbent can neutralize cheaply. With basic feature parity (a free or low-cost scheduling tier), leverage of existing distribution (SEO, app stores, partner channels) and aggressive promotional pricing, a competitor can replicate or absorb these customers quickly. The founder must prove a moat, validated scalable acquisition channels, and unit economics to survive that pressure.

- **No defensible product differentiation or moat** [CRITICAL] (differentiation)
  The document states only price and current MRR but describes no unique feature, IP, integrations, network effects or service that would prevent incumbents from copying the product. With no visible technical or go-to-market barrier, a well-funded competitor can add an equivalent scheduling feature or bundle it into an existing suite within months. This makes the product vulnerable to rapid neutralization through feature parity or acquisition.
  -> What specific, hard-to-copy feature, integration, or network effect prevents a competitor from reproducing your core value in 2–3 months?

- **Go-to-market plan is under-specified and easily outpaced** [HIGH] (acquisition)
  Acquisition is described only as 'referrals and partnerships with fitness instructors' with no validated channels, funnels, or growth metrics. A deep-pocketed competitor can weaponize existing user bases, SEO, app-store ranking, reseller/channel partners and paid acquisition to swamp any organic referral growth. Without a proven, scalable channel, the startup can't defend against incumbents using breadth and spend to capture the same studios.
  -> Which specific acquisition channels have you validated with measured CAC and conversion, and how will they scale to acquire X new studios per month?

- **Price is exposed — easy to neutralize with a free/basic tier** [HIGH] (pricing)
  At £89/month there's no stated justification for the price or evidence customers prefer this paid tier over cheaper alternatives. A competitor can undercut by offering a free or low-cost basic scheduling tier (or bundle scheduling into an existing product) that targets independent studios, forcing the startup to either match on price or justify premium features. Given the founder's small base, they likely cannot sustain a prolonged price war.
  -> Why will studios pay £89/month rather than adopt a lower-cost or bundled scheduling product from a larger provider?

- **No competitive benchmarking or awareness of substitutes** [MEDIUM] (alternatives)
  The plan omits any analysis of incumbent scheduling platforms, marketplaces, or DIY alternatives that studios currently use. That blind spot lets competitors frame the startup as redundant and win on trust, features, or integrated ecosystems. Without this competitive map the founder cannot identify defensible positioning or messages to stop churn to larger vendors.
  -> Which incumbent products or stopgap solutions do your target studios currently use, and what are the explicit reasons they would switch to you?

- **Key unit economics and retention metrics are missing** [MEDIUM] (key_numbers)
  The document lists 24 paying studios, MRR, and 3 cancellations but provides no churn rate, CAC, LTV, or payback period. A well-funded competitor can sustain negative unit economics to capture share; without these numbers the founder can't know how long they can defend against aggressive acquisition or discounting. The missing metrics also prevent credible forecasting and counteroffer strategies.
  -> What are your CAC, monthly churn rate, LTV per studio, and customer payback period?

### execution_risk

The plan leans heavily on vague referral and partnership channels without the operational, technical, or compliance scaffolding needed to scale beyond 24 studios. Key delivery risks are missing: a concrete acquisition funnel and partner onboarding, capacity for support/onboarding, integrations with incumbents and payment providers, and regulatory compliance steps. These gaps make the next step (scaling MRR) likely to stall in execution rather than market fit.

- **Distribution is 'referrals and partnerships' — no funnel, incentives, or partner ops** [CRITICAL] (acquisition)
  The entire growth plan is a one-line: 'expand through referrals and partnerships with fitness instructors' with no funnel metrics, partner archetypes, outreach playbook, commercial terms, or onboarding flows. That leaves shipping the partner program prone to zero-scaled outcomes: partners that never refer, partnerships with unclear legal/commercial terms, or a referral mechanic that drives low-quality leads. Without a tested funnel you can build product features for partners and still get no customers.
  -> What are the exact partner types, outreach channels, incentive mechanics, and expected conversion metrics (leads → trials → paid) that will produce predictable studio acquisition?

- **No capacity plan for onboarding & support — churn spike when scaling** [HIGH] (assumptions)
  At 24 studios the founder(s) may be handling setup, migrations, and support ad hoc; the doc does not state headcount, support SLAs, or onboarding automation. Scaling via partnerships/referrals will increase support needs suddenly — missing playbooks, onboarding tooling, or staffing will create long wait times and onboarding failures that cause churn. Building marketing and partner features before automating onboarding will amplify rather than solve churn.
  -> Who will handle onboarding and first-line support at 100–500 studios, what processes/tools will reduce manual work, and what is the hiring/timeline plan to cover that load?

- **Assumes studios will migrate without integrations to incumbent platforms** [HIGH] (alternatives)
  There is no inventory of what competing scheduling/pos tools target customers already use (Mindbody, other regional players) nor a plan for data import, calendar sync, or reservation parity. If studios rely on integrations (calendar, POS, payment reconciling), the product will face integration hell or force customers to double-enter data, blocking adoption. Building feature-set for new customers without integration capabilities will slow partner conversions and increase manual onboarding time.
  -> Which incumbent systems do your target studios currently use, what data integrations are required for them to switch, and which integrations will you prioritize in the next 6 months?

- **Regulatory and payments compliance left unspecified (GDPR/PCI/VAT risk)** [HIGH] (assumptions)
  The plan makes no mention of data protection (GDPR), payment compliance (PCI-DSS), or VAT/tax handling for UK studios; these are hard blockers for onboarding customers and integrating payment processors. Payment disputes, card compliance issues, or mishandled personal data could force feature rollbacks or prevent use by larger studios. Relying on a third-party processor without explicit coverage (or the right contracts) will create legal and operational stoppages.
  -> Which payment processor and data-hosting stack are you using, who holds PCI/GDPR responsibilities, and what steps/contracts are in place to ensure VAT and data-compliance for UK studios?

- **No resourcing/timeline or load-bearing metrics to match scope of 'expansion'** [MEDIUM] (key_numbers)
  The document has MRR and churn counts but omits key build estimates: engineering time for integrations, partner portal, referral tracking, onboarding automation, and hiring needs. That makes it likely the team will under-commit effort (e.g., treating several months of work as a few weeks) or mis-sequence deliverables. Without target timelines and headcount, prioritization decisions will be reactive and the product will miss critical dependencies.
  -> What are the engineering, design, and operations headcount and timeline estimates (in person-months) for the next 6 months, broken down by feature (partner program, integrations, onboarding automation, compliance work)?

### evidence_audit

Evidence base: Mixed. The document shows real early traction (24 paying studios, £2,136 MRR) but extrapolates scaling via referrals/partnerships beyond the measured evidence. The most important remaining issue is missing unit economics (CAC/LTV) and unclear churn/channel conversion data.

- **No CAC or LTV provided — unit economics missing** [HIGH] (key_numbers)
  The plan gives price (£89) and MRR but omits customer acquisition cost (CAC) and lifetime value (LTV), which are required to judge whether scaling via referrals/partnerships is viable. Using the document's numbers and assuming 3 cancellations over six months from a roughly stable base of 24 customers implies monthly churn ≈ 3/(24×6)=0.0208 (2.08%/month) → expected lifetime ≈ 1/0.0208 ≈ 48 months → LTV ≈ £89×48 ≈ £4,272; this is a derived figure based on an unstated assumption. Without an explicit CAC and a validated LTV calculation the growth plan cannot be evaluated.
  -> What is your actual CAC (broken down by channel if available) and the LTV you use (showing the churn calculation and period used) so we can confirm unit economics?

- **Churn figure is ambiguous and likely unreliable** [MEDIUM] (assumptions)
  The document reports '3 cancellations over the past six months' but provides no numerator/denominator timeline: we do not know monthly starting counts, new signups, or whether cancellations are permanent churn or refunds/trials. The derived monthly churn above (≈2.08%/month → ≈23% annual) depends on assuming a stable base of 24 customers; small-sample timing changes would materially change LTV and revenue forecasts.
  -> Provide a monthly cohort table for the past 6–12 months listing customers at period start, new signups, cancellations (with reasons), and period-end customers so churn can be calculated unambiguously.

- **No measured evidence that referrals/partnerships will scale acquisition** [MEDIUM] (acquisition)
  The growth channel named (referrals and partnerships with instructors) is plausible but unsupported: the document contains no pilot results, referral conversion rates, signed partnerships, or projected referral volume. Without even a small experiment (e.g., X referred leads → Y signups), scaling assumptions are untested and load-bearing for the plan.
  -> Share results from any referral/partnership pilots (number of partners engaged, referrals generated, leads converted to paid customers, and timeframe) or provide a concrete, measured funnel estimate (referrals → trials → paid) you will use to model growth.

- **Demand evidence is limited to 24 customers; external validity is unclear** [LOW] (demand_evidence)
  You have 24 paying studios which is useful but a small sample; it's unclear whether they represent a replicable segment (geography, studio size, niche). The document offers no evidence on representativeness, willingness-to-pay variation, or addressable penetration within the target population.
  -> Provide any segmentation of the 24 customers (location, studio size, revenue, how they were acquired) or external demand signals (pipeline, waitlist, inquiries, or market outreach) that show these customers are representative of a larger addressable group.


## Selected questions

- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: pre_mortem / Early retention interpreted as product-market fit without cohort data [high]
  - why we're asking: unit_economics / No fully loaded cost-to-serve per studio (cannot compute gross margin) [critical]
  - why we're asking: unit_economics / Churn/LTV and payback period are not computed despite partial churn signal [medium]
  - why we're asking: unit_economics / Support and onboarding cost per studio is unspecified [low]
  - why we're asking: adversarial_competitor / Key unit economics and retention metrics are missing [medium]
  - why we're asking: execution_risk / No resourcing/timeline or load-bearing metrics to match scope of 'expansion' [medium]
  - why we're asking: evidence_audit / No CAC or LTV provided — unit economics missing [high]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Killing-blow: assumed instructors would be an effective acquisition channel [critical]
  - why we're asking: unit_economics / CAC and acquisition economics are unspecified for the proposed channels [high]
  - why we're asking: adversarial_competitor / Go-to-market plan is under-specified and easily outpaced [high]
  - why we're asking: execution_risk / Distribution is 'referrals and partnerships' — no funnel, incentives, or partner ops [critical]
  - why we're asking: evidence_audit / No measured evidence that referrals/partnerships will scale acquisition [medium]
- **differentiation**: Why would customers choose this over the alternatives?
  - why we're asking: adversarial_competitor / No defensible product differentiation or moat [critical]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Pricing assumed to scale from 24 studios with no WTP testing [medium]
  - why we're asking: unit_economics / Pricing/willingness-to-pay is inadequately validated beyond initial customers [high]
  - why we're asking: adversarial_competitor / Price is exposed — easy to neutralize with a free/basic tier [high]

## Answer given

**acquisition**: We plan to grow through referrals and partnerships with fitness instructors; we haven't measured how well either works yet.

Skipped: key_numbers, differentiation, pricing

## Refined critique

### unit_economics

The document gives one hard unit: 24 customers paying £89/mo (MRR £2,136) and 3 cancellations in six months. Beyond that, there are no cost inputs (COGS, hosting, support, payment fees), no CAC or channel metrics, and no LTV/payback calculations — so key unit economics (gross margin, CAC payback, sensitivity to churn) are unanswerable. Several critical numbers are missing and must be provided before the business case can be evaluated.

- **No per-customer cost (COGS) or cost-to-serve provided** [CRITICAL] (key_numbers)
  The plan lists price and MRR but gives zero detail on the costs to serve one studio: compute, storage, backups, third-party APIs, payment processing fees, and support time. Without per-customer COGS you cannot compute gross margin, contribution, or scale economics. This is the single biggest blocker to validating profitability or payback.
  -> What are the measured or estimated per-studio monthly COGS (hosting/compute, storage, payment processing fees, and average support cost in staff-hours converted to £/month)?

- **CAC and channel economics are unmeasured yet pivotal** [HIGH] (acquisition)
  Growth is planned via referrals and partnerships but no CAC, conversion rates, or funnel metrics are reported for those channels. At an £89/month price point, different channels (paid ads, partnerships, affiliates) have very different CACs and payback times; claiming low-cost growth without measured channel unit economics is unsupported. Without channel-specific CAC you cannot know if customer acquisition is profitable or how long payback will be.
  -> For each planned channel (referrals, instructor partnerships), what CAC, conversion rate, and measured payback period have you observed or are you assuming?

- **Price acceptance at scale and churn drivers are undocumented** [HIGH] (pricing)
  You charge £89/mo and 24 studios currently pay that, but there's no evidence this price scales across the target market or how sensitive churn is to price. The document reports 3 cancellations over six months but doesn't provide cohort churn rate, reasons for churn, or whether £89 is per location/instructor. LTV cannot be calculated without validated price durability and churn metrics.
  -> Provide cohort churn (monthly or annualized) and evidence that £89/month is a sustainable price point per paying unit (and clarify what a 'unit' is — studio/location/instructor).

- **Gross margin at scale is unspecified and likely to change** [MEDIUM] (key_numbers)
  There are no projections of gross margin today or at scale; as you grow, support costs, cloud usage, and payment disputes typically rise and can compress margins. Without cost curves (per-customer variable costs and fixed-cost amortization) you can't assess scalability or whether margins improve or worsen with growth.
  -> What is your projected gross margin today and at 1k and 10k studios, with the line-item drivers (variable vs fixed costs) shown?

- **Payback period and sensitivity not calculated** [MEDIUM] (assumptions)
  No CAC or COGS means no CAC payback period is computed; the plan doesn't state how long investment in acquisition must be recovered or which parameters would break payback (higher churn, higher CAC, lower ARPU). This leaves go/no-go decisions and runway planning ungrounded.
  -> What is the expected CAC payback period under current assumptions and which single parameter change (e.g., +20% CAC, +50% churn) would push payback past 12 months?

- **Hidden operational costs (refunds, chargebacks, fraud, compliance, moderation) are ignored** [LOW] (key_numbers)
  The plan does not mention costs for refunds/chargebacks, fraud prevention, or compliance (e.g., data protection, local tax/GDPR guidance), all of which add non-trivial ongoing costs for SaaS serving payments and customer data. These items can be material per-customer expenses as you scale and affect net margin and support load.
  -> Estimate your current and projected rates and monthly cost of refunds/chargebacks, fraud prevention tooling, and compliance overhead (legal/process) per month or per customer.

### execution_risk

The plan relies on untested acquisition channels and omits critical operational and compliance details required to scale beyond the current 24 customers. Key implementation risks include regulatory blockers (payments/data protection), unclear resourcing for onboarding & support, and missing billing/metrics that will cause revenue and churn surprises. Several technical and sequencing gaps (integrations, building partner features before validated economics) increase the chance of costly rework or stalled growth.

- **Regulatory blockade: GDPR / PCI / VAT not addressed** [CRITICAL] (assumptions)
  The document says you have paying UK studios but contains no plan for GDPR data processing, PCI-compliant payment handling, or VAT collection/reporting. If these aren't in place you risk blocked payment flows, fines, or being unable to legally store attendee/personal data as you scale. This is a hard stop for expansion into other UK/EU studios and for partner integrations that exchange personal data.
  -> How are you currently handling GDPR data processing, PCI-compliant payments, and VAT collection/reporting for paying studios?

- **Unvalidated referral/partnership channel will leave pipeline empty** [HIGH] (acquisition)
  Growth is pinned exclusively on referrals and fitness-instructor partnerships but the team reports no measured conversion or referral rate. The likely failure mode is low organic referral volume or poor conversion from partner leads, producing a thin pipeline and stalled MRR growth. Without tested acquisition funnels you’ll burn time and money building features for customers you can’t reliably reach.
  -> What referral and partner conversion metrics have you measured (referral rate, conversion %, lead velocity) and what are the unit economics for these channels?

- **Onboarding & support will bottleneck growth (team-size unspecified)** [HIGH] (assumptions)
  There is no information on the team, roles, or operational processes for onboarding, training, and support. As signups scale, manual onboarding or unanswered support requests will increase churn and founder time spent on ops. The realistic failure mode is growth causing service degradation and a rising cancellation rate because you lack documented, staffed processes.
  -> What team headcount and documented onboarding/support processes are in place to scale from 24 studios to the next milestones, and how long does each onboarding take today?

- **Recurring billing & dunning ops are unproven — revenue leakage risk** [HIGH] (key_numbers)
  Monthly £89 subscriptions and MRR are stated but there is no detail on the billing system, dunning, failed-payment handling, refund rules, or accounting/VAT flows. The likely failure mode: failed payments, manual reconciliation, and unnoticed churn that depress revenue as customer count grows. Building partner/bulk billing without robust recurring billing will create operational debt and cash surprises.
  -> Which billing provider and automated dunning/accounting processes are in production, and what are your current failed-payment and manual-reconciliation rates?

- **Integration & data-model risk with studio tooling left unspecified** [MEDIUM] (alternatives)
  The plan doesn't state how the product integrates with common studio ecosystems (booking platforms, payment processors, calendars) or how the data model handles classes, recurring bookings, waitlists, and refunds. If the product uses an incompatible model you'll face expensive refactors or force studios to change workflows, increasing friction to adoption. This is a technical rework risk that delays partner onboarding.
  -> Which external systems do target studios currently use, and how does your data model and integration plan support those systems?

- **Sequencing mistake: building partner features before validating LTV/CAC** [MEDIUM] (key_numbers)
  You plan to expand via partnerships and referrals but haven't recorded the unit economics or minimum validated traction required to justify building partner portals or integrations. The failure mode is investing months in partner tooling that doesn't move the key metrics, wasting engineering cycles. Prioritizing partner features before proving per-channel economics will slow progress and increase burn.
  -> What are your target CAC, LTV, payback period, and the minimum traction thresholds that would justify investment in partner integrations or partner-facing features?


## Refinement meta

- Lenses re-run: unit_economics, execution_risk
- Lenses not re-run: pre_mortem, adversarial_competitor, evidence_audit
- Gaps filled: ['acquisition']
- Gaps skipped: ['key_numbers', 'differentiation', 'pricing']

## Reuse check

Re-sending the same refinement token refused with 409: yes
