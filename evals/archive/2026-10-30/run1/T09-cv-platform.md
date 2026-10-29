# T09-cv-platform

**Stage:** building

## Input

We're creating an AI CV review platform for graduates. Our planned price is 800 per year, and our acquisition target is 25 customers per month. We expect marketing to cost 20 per day but haven't chosen a currency yet. We estimate an average customer lifetime of 2 years.

**Reviewer expectation:** numeric provenance - must not convert 800 into £800/$800, or 20/day into a per-customer CAC; should ask for clarification.

## First critique

### pre_mortem

The plan rests on several untested, high-leverage assumptions: that graduates will pay an annual fee of “800” (currency unspecified) for an ongoing AI CV review subscription, that a meaningful cohort will remain customers for two years, and that the team can acquire 25 customers/month with a daily marketing budget of “20.” The most likely killing blow is pricing/packaging mismatch: prospective users prefer free or one-off help and will not subscribe at the stated price, collapsing demand before launch. Core missing evidence: who exactly the buyer is, willingness-to-pay validation, and a concrete, channel-specific acquisition test.

- **Critical: Price and payment model (800/year) is unvalidated and likely mismatched to buyer willingness** [CRITICAL] (pricing)
  You state a list price of 800 per year but give no currency, no rationale for annual billing, and no evidence that recent graduates will pay an ongoing subscription for CV reviews. Graduates are typically cash-constrained and often prefer one-off, outcome-driven purchases; assuming they will pay a recurring annual fee is a high-risk leap. If this assumption is wrong, the product never reaches steady traction.
  -> What concrete evidence (preorders, paid trials, or willingness-to-pay tests) shows the target graduate cohort will purchase an annual subscription at 800 in a specified currency rather than use free/one-off options?

- **High: No evidence that graduates actually demand a paid AI CV review (stated vs revealed preference)** [HIGH] (demand_evidence)
  The document contains no user research, pilot results, or conversion data to support the core demand hypothesis. You may be confusing expressed interest in 'better CVs' with actual willingness to pay for an AI subscription. Without simple tests (landing page preorders, pricing A/B ads, or paid pilot offers), you won't know if the product solves a monetizable problem.
  -> Can you show a minimal test (landing page with buy button, ad-driven signups with price shown, or paid pilot) that validates conversion at or near the proposed price?

- **High: 'Graduates' is too broad—the true buyer/payer is undefined** [HIGH] (buyer)
  Labeling the customer as 'graduates' leaves huge ambiguity: Are you targeting final-year students, recent grads (<6 months), career switchers, or specific majors/regions? Different segments vary dramatically in budget, urgency, channels, and trust in AI. You also haven't specified who would pay (student, parent, employer, university). This ambiguity makes your pricing, acquisition, and retention assumptions ungrounded.
  -> Which specific graduate segment (age, career stage, geography, field) will you target first, and who within that segment will actually pay for the service?

- **High: Customer lifetime = 2 years is an unsupported subscription assumption** [HIGH] (assumptions)
  Assuming an average customer stays for 2 years implies recurring, repeatable value after graduation. In reality, most graduates need CV help briefly at job search time; retention is likely low unless the product expands into ongoing career services. This overestimates lifetime and underestimates churn risk, biasing product and pricing choices toward subscription when a one-off or credit-based model might be the revealed preference.
  -> Why do you expect customers to retain an annual subscription for two years instead of making a single, short-term purchase, and how will you test actual retention behavior cheaply?

- **Medium: Acquisition plan and the '20 per day' marketing budget are vague and untested** [MEDIUM] (acquisition)
  You state an acquisition target (25/month) and marketing cost (20/day) but neither currency nor channel is specified. There's no evidence these numbers map to realistic cost-per-acquisition in relevant channels (campus partnerships, social ads, Discord/Reddit, career fairs). If the assumed channel CACs are higher than implied, the target acquisition rate won't materialize.
  -> Which specific marketing channels and audience-targeting tactics map the '20/day' budget to an expected cost-per-acquisition, and can you run a small, budgeted ad experiment to validate CAC?

- **Medium: No clear differentiation vs free tools, university services, or one-off human reviewers** [MEDIUM] (differentiation)
  The strategy assumes 'AI CV review' is a strong enough differentiator, but many free AI tools, university career centers, peer networks, and affordable human reviewers already serve graduates. You haven't specified what measurable outcome you deliver better (higher interview invite rate, vetted ATS optimization, recruiter feedback) that would justify the price and subscription model.
  -> What specific outcome (e.g., X% higher interview rate, ATS pass rate, recruiter-validated score) do you deliver that free tools and current alternatives do not, and how will you prove it in a pilot?

### unit_economics

The doc lists price (800/year), a 25 new customers/month target, marketing spend (20/day) and a 2-year average lifetime, but omits currency and every cost input needed to compute unit economics. With missing CAC by channel, cost-to-serve (compute, storage, support, payment fees) and no evidence of willingness-to-pay, you cannot calculate gross margin or payback. First tests: run a small paid-acquisition experiment to measure CPA and a pricing test (landing page / paid pilots) to validate willingness-to-pay before building more product.

- **Currency and core unit inputs are undefined — math is unanchored** [HIGH] (key_numbers)
  You gave price (800/yr) and marketing (20/day) but explicitly 'haven't chosen a currency yet.' Without a currency and consistent units you cannot compute CAC, ARPU, LTV in meaningful terms or compare costs to revenue. This makes every downstream metric (payback, margin) impossible to verify.
  -> What currency are you using and please restate price, marketing spend and all per-period amounts in that currency?

- **Willingness-to-pay is unsupported — 800/yr is an unvalidated hypothesis** [HIGH] (pricing)
  The plan assumes customers will pay 800 per year but provides no evidence (surveys, pilots, price experiments, or anchor customers). You haven't specified who actually pays (student, university, employer) or whether that group can and will pay 800/year. Revenue projections hinge entirely on this untested price.
  -> Who is the paying customer and what concrete validation (paid pilots, preorders, pricing tests or survey results) supports charging 800/year?

- **CAC and acquisition channels are unspecified yet the target implies an unrealistic CPA** [HIGH] (acquisition)
  You target 25 customers/month and list 20/day marketing spend but don't name channels, expected conversion rates, or how spend maps to customers. Without channel-level CPAs you can't verify that 20/day can deliver 25 customers/month or what CAC will be, so the acquisition plan is unsupported by numbers.
  -> Which acquisition channels will you use and what are your assumed channel-level conversion rates and resulting CACs to deliver 25 customers/month?

- **Cost to serve (compute, storage, support, payment processing) is missing** [MEDIUM] (key_numbers)
  There is no per-user estimate for compute (AI inference cost), storage, support (human reviews/CS), or payment processing fees. For an AI CV review product, inference and storage could be material; without these unit costs you cannot estimate gross margin or determine if 800/yr yields attractive unit economics.
  -> Provide per-customer monthly estimates for compute/inference, storage, customer support and payment processing fees so gross margin can be calculated.

- **Payback period and LTV/CAC math are undeclared and fragile** [MEDIUM] (assumptions)
  You state average lifetime = 2 years (implying LTV = 1,600 in your unit) but give no CAC or churn curve, so payback period cannot be calculated. If CAC is higher than assumed or if churn is front-loaded, payback could be far longer than the business can support, but the document contains no sensitivity or break-even analysis.
  -> What is your projected CAC and monthly churn so we can compute LTV:CAC and payback period (in months)?

- **Hidden and operating costs (moderation, refunds, chargebacks, fraud, compliance) are ignored** [MEDIUM] (assumptions)
  No mention of moderation (AI output review), compliance (data/privacy for CVs), refund/chargeback rates, or fraud mitigation. These items can become significant operating costs or increase churn and payment losses, materially changing unit economics if unaccounted for.
  -> Have you estimated potential costs for moderation/review, refunds/chargebacks and privacy/compliance work per customer, and what are those estimates?

### adversarial_competitor

This concept is highly attackable: the founder proposes an AI CV-review for graduates at $800/yr with no validation, unclear customer target, and a vague acquisition plan. A well-funded incumbent can neutralize it cheaply by bundling a free/basic AI review into an existing product, undercutting pricing, and using existing distribution (SEO, app store, email lists, partnerships) to capture early users before the startup launches.

- **No evidence graduates will pay $800/year (price + demand unvalidated)** [CRITICAL] (demand_evidence)
  The plan names a price (800/yr) but provides no evidence that graduates will pay that amount or who actually pays (student, parents, schools, employers). At this price point the product is either a premium or enterprise offering — a mismatch vs the 'graduates' buyer implied. This is fatal because a competitor can offer a free/basic alternative and win adoption while the startup struggles to convert.
  -> What validated evidence (surveys with willingness-to-pay, paid pilots, or signed letters of intent) shows a material cohort of graduates will pay 800/year for this service?

- **Differentiation is undefined and trivially copyable** [HIGH] (differentiation)
  No unique features, exclusive data, or barriers to replication are stated. Automated CV feedback is a commodity ML use-case: incumbents or platforms with large user bases can add a similar model + UX and absorb the market. Without a clear defensible moat (unique training data, partnerships with universities/employers, or placement guarantees), the product is easy to neutralize.
  -> What concrete, defensible features or exclusive data/partnerships prevent an incumbent from shipping a functionally equivalent CV-review in weeks?

- **Acquisition plan and unit economics are incoherent** [HIGH] (acquisition)
  They target 25 customers/month with marketing '20 per day' (currency not set) and no channel strategy. There is no CAC, conversion funnel, nor channels listed (SEO, partnerships, campus outreach). A well-funded competitor can exploit this by using existing channels and much lower incremental CAC to procure users at scale before the startup finds a repeatable funnel.
  -> Which specific channels and measured conversion rates produce 25 customers/month and what is the true CAC in a real currency?

- **Unclear buyer segmentation — 'graduates' is too broad** [HIGH] (buyer)
  The target is simply 'graduates' with no segmentation (recent grads, students, geography, discipline). Different buyer segments have very different willingness-to-pay and acquisition costs. Without a prioritized buyer persona, the product cannot focus messaging, partnerships, or pricing — enabling incumbents to pick the most valuable segments and dominate them first.
  -> Which exact graduate segment (age, schooling, region, discipline) is the initial target and why will that segment convert at the proposed price?

- **Key numbers are incomplete and contradictory (marketing cost currency missing)** [MEDIUM] (key_numbers)
  Marketing cost is stated as '20 per day' with no currency, and lifetime is given as 2 years but no churn, ARPU, or CAC are provided. These missing inputs prevent even a basic unit-economics test and let competitors undercut using predictable pricing and subsidies.
  -> Supply the missing unit-economics: currency for marketing cost, expected CAC, conversion rates, ARPU, and churn assumptions that lead to sustainable LTV/CAC.

### execution_risk

The plan lists price, a monthly acquisition target, a daily marketing spend and a 2-year lifetime, but key inputs and operational details are missing. The biggest shipping risks are legal/regulatory obligations around handling resumes (PII), unproven acquisition math (currency/CAC missing), an unsupported willingness-to-pay assumption for graduates at $800/year, and substantial technical work to build a defensible AI reviewer without any data or model plan. Also missing: a validated go-to-market/channel sequence and any team/timeline, which together make delivery and early growth likely to fail or be much slower than implied.

- **No data-privacy / PII compliance plan for handling resumes (possible regulatory shutdown)** [CRITICAL] (assumptions)
  Resumes contain personal and sensitive data; the document has no geography, consent flows, retention policy, security, GDPR/CCPA considerations, or plan for legal counsel. Shipping without compliance risks fines, forced data deletion, or being blocked by cloud providers or enterprise customers. This is a show-stopper for any meaningful user acquisition or onboarding in regulated markets.
  -> In which jurisdictions will you operate and how will you legally collect, store, process, and delete applicant PII (consent, data retention, DSRs, security controls) before you accept real resumes?

- **Acquisition math is unusable: currency, CAC and channel details missing** [HIGH] (key_numbers)
  You state $/800 per year, 25 customers/month and 20 per day marketing spend but didn’t specify currency or conversion assumptions, acquisition channels, conversion rates, or customer funnel. Without currency and CAC estimates you can't tell whether 20/day is adequate or whether 25 customers/month is reachable — this will lead to an underfunded launch or wrong marketing experiments.
  -> What currency are you using, what channels and conversion rates produce 25 customers/month, and what CAC do you expect from 20 (units)/day of marketing spend?

- **Price (800/year) is unsupported for 'graduates' — no evidence graduates will pay** [HIGH] (demand_evidence)
  Charging 800/year to recent graduates is a strong assumption with no validation: no willingness-to-pay tests, no segmentation (senior vs fresh grads), and no alternative payment options (one-off review, freemium). If graduates won’t pay that price the product will need a different monetization or customer segment.
  -> Who exactly is the paying customer (which graduate segment and geography) and what evidence (surveys, preorders, paid pilots) do you have that they will pay 800/year?

- **No data/model plan: building reliable AI CV review requires labelled data and bias controls** [HIGH] (assumptions)
  An ML-driven CV reviewer needs training/evaluation datasets, a rubric, and bias mitigation; none of this is described. Failure modes include producing low-quality or discriminatory advice, high false positives/negatives, or unpredictable outputs that harm users and reputation. Without a plan to obtain labeled resumes and human QA, the product will be brittle at launch.
  -> What labeled data, human-review process, and fairness/QA checks will you use to train and validate the CV reviewer before onboarding paying users?

- **Sequencing risk: building platform before validating acquisition or willingness to pay** [MEDIUM] (acquisition)
  The document implies product development is underway but contains no plan to validate channels, pricing, or target conversion before full build. If you complete the product first and only then discover CAC or price are wrong, you’ll waste months of engineering effort and miss a fast pivot window.
  -> What is your minimum viable test (landing page, preorders, concierge reviews) to validate you can acquire paying graduates at target CAC before building the full product?

- **No team, timeline, or operational plan — scope likely underestimated** [MEDIUM] (assumptions)
  There is no stated team size, roles, or timeline. Building a reliable AI reviewer, UX for CV uploads, secure storage, billing, and onboarding 25 paying customers/month plus support is nontrivial; without resourcing the project will slip, burn out founders, or launch incomplete.
  -> Who is building and operating the product (engineers, ML, legal, customer support) and what timeline and milestones show you can deliver the MVP and handle 25 paying customers/month?

### evidence_audit

Evidence base: Weak. The plan is pre-launch with no real revenue or customer traction; founder lists price, acquisition and spend targets but provides no measured conversion or pilot data. The most important remaining issue is unsupported unit-economics (unspecified currency plus implied CAC and LTV) that drive the plan's conclusions.

- **Currency for price and marketing spend is unspecified** [HIGH] (pricing)
  The plan states a price of 800 per year and marketing at 20 per day but explicitly says no currency chosen. Without a currency, you cannot compute CAC, revenue, LTV or compare costs and price consistently. All derived economics in the document implicitly assume the same currency for both figures; that assumption is unstated and load-bearing.
  -> Specify the currency for the 800/year price and the 20/day marketing cost (are they the same currency?), and confirm units (e.g., 20 per calendar day).

- **Stated marketing spend implies implausibly low CAC and huge LTV:CAC unless justified** [HIGH] (acquisition)
  If marketing is 20/day → 20×30≈600 per month, and you plan 25 customers/month, implied CAC = 600/25 = 24. With price = 800/year and lifetime = 2 years, LTV = 800×2 = 1600, giving LTV:CAC ≈ 1600/24 ≈ 67 and payback ≈ 24/(800/12) ≈ 0.36 months. That is unusually attractive and therefore a red flag unless you can show conversion rates or channel evidence that produce CAC=24. This arithmetic assumes the same currency for price and ad spend (see previous flaw).
  -> Provide measured conversion rates or a channel/campaign example showing that 20/day marketing spend produces 25 paid customers/month (or supply an expected CAC and its source); if you cannot, run a 30-day pilot at 20/day and report paid conversions.

- **Average customer lifetime (2 years) is unsupported and materially affects economics** [MEDIUM] (assumptions)
  You assert a 2-year average lifetime (implying ~50% annual churn) but give no basis. Lifetime drives LTV (LTV = price × lifetime = 1600 under current numbers) and therefore whether acquisition spend is sustainable. With 25 new customers/month (300/year) and churn = 50%/year, steady-state customer base = new_per_year / churn = 300/0.5 = 600 customers → implied steady revenue = 600×800 = 480,000 per year (assuming same currency).
  -> Show the data or rationale for the 2-year lifetime (historical churn from pilots, comparable product benchmarks, or user-research evidence); if none, run a cohort churn measurement over three months and report monthly retention.

- **No demand evidence or pilot to support the 25 customers/month target** [MEDIUM] (demand_evidence)
  The target of 25 customers/month is a forecast with no reported experiments, waitlist, pilot conversions, or survey backing. At idea-stage this is expected, but the plan depends on this rate to claim unit-economics success; without a small test the target is just an assumption.
  -> Run a low-cost pilot (e.g., a 30-day campaign at your stated 20/day spend and a simple landing page) and report paid conversions, cost per paid customer, and funnel conversion rates.

- **Ambiguous definition: are 25 customers/month gross acquisitions or net (after churn)?** [LOW] (key_numbers)
  You state 'acquisition target is 25 customers per month' but do not say whether this is gross new signups, new paying customers, or net new customers after churn. That ambiguity changes growth and ARR math and therefore the interpretation of CAC and marketing effectiveness.
  -> Clarify whether the 25 customers/month figure refers to gross new paid customers, net new customers (post-churn), or something else, and state how you will count them (e.g., first paid month recognized).


## Selected questions

- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / High: No evidence that graduates actually demand a paid AI CV review (stated vs revealed preference) [high]
  - why we're asking: adversarial_competitor / No evidence graduates will pay $800/year (price + demand unvalidated) [critical]
  - why we're asking: execution_risk / Price (800/year) is unsupported for 'graduates' — no evidence graduates will pay [high]
  - why we're asking: evidence_audit / No demand evidence or pilot to support the 25 customers/month target [medium]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Critical: Price and payment model (800/year) is unvalidated and likely mismatched to buyer willingness [critical]
  - why we're asking: unit_economics / Willingness-to-pay is unsupported — 800/yr is an unvalidated hypothesis [high]
  - why we're asking: evidence_audit / Currency for price and marketing spend is unspecified [high]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Medium: Acquisition plan and the '20 per day' marketing budget are vague and untested [medium]
  - why we're asking: unit_economics / CAC and acquisition channels are unspecified yet the target implies an unrealistic CPA [high]
  - why we're asking: adversarial_competitor / Acquisition plan and unit economics are incoherent [high]
  - why we're asking: execution_risk / Sequencing risk: building platform before validating acquisition or willingness to pay [medium]
  - why we're asking: evidence_audit / Stated marketing spend implies implausibly low CAC and huge LTV:CAC unless justified [high]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / Currency and core unit inputs are undefined — math is unanchored [high]
  - why we're asking: unit_economics / Cost to serve (compute, storage, support, payment processing) is missing [medium]
  - why we're asking: adversarial_competitor / Key numbers are incomplete and contradictory (marketing cost currency missing) [medium]
  - why we're asking: execution_risk / Acquisition math is unusable: currency, CAC and channel details missing [high]
  - why we're asking: evidence_audit / Ambiguous definition: are 25 customers/month gross acquisitions or net (after churn)? [low]

## Answer given

**pricing**: We still haven't decided between pounds and dollars; 800 per year is a placeholder.

Skipped: demand_evidence, acquisition, key_numbers

## Refined critique

### unit_economics

The plan lists a headline price (800/year), an acquisition target (25 customers/month) and a daily marketing spend (20/day) but leaves currency, channels, cost-to-serve and CAC math undefined. Key unit-economics inputs required to assess viability — validated willingness-to-pay, per-user variable costs (compute, storage, payments, support), CAC by channel, gross margin and payback — are missing. Before building further, the founder must produce a simple unit-econ model (price, CAC, LTV, per-user cost, payback) and validate the two weakest links: price and acquisition cost.

- **Price is a placeholder with no currency or WTP validation** [HIGH] (pricing)
  The document states '800 per year' but explicitly hasn't decided between pounds and dollars and gives no evidence that graduates will pay that amount. Revenue per user and LTV depend entirely on this unsupported price and the claimed 2-year lifetime. Without validated willingness-to-pay and a clear currency, every downstream metric (LTV, payback, margin) is unknown.
  -> What currency is 800 in, and what evidence (surveys/paid tests/conversions) shows graduates will actually pay that price annually?

- **CAC not calculated and stated marketing spend is unusable** [HIGH] (acquisition)
  You quote an acquisition target (25 customers/month) and a marketing cost of '20 per day' but haven't tied channels to that spend or shown expected conversion rates, so CAC is undefined. Without channel-level CAC estimates (paid ads, partnerships, campus outreach, organic), the 25/month target and payback assumptions are untestable and possibly unrealistic for the price point.
  -> List the acquisition channels you will use, the planned daily spend in a specific currency per channel, and the expected conversion rate to a paying customer so we can compute CAC.

- **Per-user cost to serve is missing (compute, storage, support, payments)** [HIGH] (key_numbers)
  There is no breakdown of variable costs per user: AI compute for CV review, storage for uploaded files, customer support cost, payment processing fees, or CDN/video costs if used. These line items directly determine gross margin; without them you can't know whether 800/year is profitable at any scale.
  -> Provide per-user estimates (or measured values) for AI inference/hosting, storage, bandwidth, support time/cost, and payment processing fees in a specific currency so we can compute gross margin.

- **Gross margin and unit economics at scale are unspecified** [MEDIUM] (key_numbers)
  Because price, CAC and per-user costs are all undefined, gross margin today and at scale is unknown. There's no view on fixed vs variable costs or how unit economics improve (or worsen) as you scale (e.g., bulk inference discounts vs. increasing support load).
  -> Show a simple P&L per user (revenue, variable cost, contribution margin) and explain which costs are expected to scale linearly versus dilute with scale.

- **Payback period and sensitivity to CAC/LTV are missing** [MEDIUM] (key_numbers)
  You report an average lifetime of 2 years but haven't shown CAC nor monthly churn, so payback period cannot be calculated. There's no sensitivity analysis showing what CAC or churn would 'break' the business (e.g., CAC > LTV or > first-year revenue).
  -> Given a specific currency price and CAC by channel, what is the payback period (months) and at what CAC or churn rate does payback exceed the customer lifetime value?

- **Operational and hidden costs (moderation, refunds, fraud, compliance) are unaccounted** [MEDIUM] (key_numbers)
  The plan doesn't mention costs for content moderation, handling refunds/chargebacks, fraud prevention, or compliance (data protection for student CVs). These can materially increase CAC and support costs and reduce net revenue per user but are entirely absent from the model.
  -> Estimate the expected monthly/annual costs for moderation, chargebacks/refunds, fraud prevention and data-compliance efforts, or explain how you will measure them cheaply during test acquisition.

### evidence_audit

Evidence base: Weak. This is a pre-launch plan consisting only of stated assumptions (price, marketing spend, acquisition target, and lifetime) with no measured traction or validation. What is proven are only the founder's declared assumptions; the most important remaining issue is the absence of validated demand and unspecified currency, which makes revenue/CAC/LTV calculations ambiguous.

- **No measured evidence that graduates want or will pay for this** [CRITICAL] (demand_evidence)
  The document contains no demand evidence (interviews, surveys, pilots, waitlist, or pre-sales) demonstrating that graduates will use or pay for an AI CV review at the planned price. At pre-launch this is the single most load-bearing unknown — without validated demand the stated acquisition and revenue targets are speculative.
  -> Provide measured demand evidence: number of graduate interviews or survey responses, willingness-to-pay metrics, pilot signups, or other concrete tests showing willingness to buy at ~800/year.

- **Currency/units for price and marketing are unspecified** [HIGH] (key_numbers)
  The plan gives a price of '800 per year' and a marketing cost of '20 per day' but explicitly says the currency hasn't been chosen. Without a currency/unit these core figures cannot be turned into revenue, CAC or LTV in a consistent way. For example: 25 customers/month → 300 new customers/year → 300×800 = 240,000 (units); marketing 20/day → 20×30 = 600 (units)/month — both totals are uninterpretable until you state the currency.
  -> State the currency for the 800/year price and the 20/day marketing cost and confirm whether both figures are in the same currency; then provide the projected annual revenue in that currency.

- **Implied CAC from the stated marketing budget conflicts with acquisition target** [MEDIUM] (acquisition)
  If the marketing budget is 20/day → 20×30 ≈ 600/month and that produces 25 customers/month, implied CAC = 600/25 = 24 (units) per customer. Combined with an assumed LTV of 800×2 = 1,600 this gives an LTV:CAC ≈ 66.7, which is unusually high and suggests either the budget isn't the whole acquisition spend or conversion assumptions are missing. The plan never states whether that 20/day is the sole acquisition spend or what conversion funnel produces 25 paid customers.
  -> Is the 20/day marketing budget intended to be the sole acquisition spend; if so, provide channel-level funnel numbers (impressions, clicks, leads, free trials to paid) that justify 600/month producing 25 paying customers (CAC=24).

- **Average customer lifetime (2 years) is asserted but unsourced** [MEDIUM] (assumptions)
  The 2-year lifetime is a load-bearing assumption used to compute LTV (800×2 = 1,600) and payback timelines, but no retention data or rationale is provided. At pre-launch average lifetime cannot be observed and must be justified by comparable products, pilot cohorts, or explicit retention assumptions.
  -> What empirical basis or comparable-product assumption produces the 2-year average lifetime; provide the churn rate, retention curve, or evidence used to set this figure.

- **Acquisition rate, lifetime and headline revenue are not reconciled** [MEDIUM] (key_numbers)
  Stating '25 customers per month' and a 2-year lifetime implies a steady-state customer base of 25 × 24 = 600 customers, which would produce 600 × 800 = 480,000/year steady-state ARR. But 25×12×800 = 240,000 would be first-year new-customer revenue. The document never states whether the target is first-year revenue, steady-state ARR, or a cohort projection, so the topline outcome is ambiguous.
  -> Do you intend 240,000 to be first-year new-customer revenue or 480,000 to be steady-state ARR? Provide a 24-month cohort projection (customers, churn, net adds, and resulting ARR) so the revenue timeline is explicit.


## Refinement meta

- Lenses re-run: unit_economics, evidence_audit
- Lenses not re-run: pre_mortem, adversarial_competitor, execution_risk
- Gaps filled: ['pricing']
- Gaps skipped: ['demand_evidence', 'acquisition', 'key_numbers']

## Reuse check

Re-sending the same refinement token refused with 409: yes
