# T06-video-economics

**Stage:** idea

## Input

We're building an unlimited AI video-generation service for £5 per month. Each generated video costs us approximately £2 in computing expenses. We expect our average subscriber to generate 20 videos monthly, and we will not impose usage limits or charge additional fees.

**Reviewer expectation:** CONTROL - at least one defensible critical (20 x £2 = £40 cost vs £5 revenue), distinguished from merely missing evidence.

## First critique

### pre_mortem

The strategy rests on several unvalidated, high-leverage assumptions about user behavior, cost-per-video, and willingness to accept an unlimited £5/month plan. The single most likely cause of failure is that revealed usage patterns (frequency and intensity) diverged sharply from the stated 20 videos/month average, breaking the model. Several dependencies—cheaper compute or partnerships, a clearly identified buyer, and evidence users prefer unlimited vs. per-unit pricing—were never proven. First tests should validate who the buyer is, how often they will actually generate videos, and whether they prefer unlimited pricing before any build-out.

- **Unvalidated usage-intensity assumption (20 videos/month)** [CRITICAL] (demand_evidence)
  The plan hinges on an average subscriber creating 20 videos per month, but no evidence, survey data, or behavior-based estimate is provided. If real users generate more (or fewer) videos, both cost exposure and perceived value change dramatically. This single assumption directly determines platform sustainability and was never tested.
  -> Who will generate how many videos per month in practice — what does early revealed-behavior testing show?

- **Assumed compute cost of ~£2/video is unproven and treated as fixed** [HIGH] (key_numbers)
  The strategy states each generated video costs approx £2 but provides no sourcing, sensitivity, or contingency if that number changes. The plan implicitly assumes that cost-per-video will remain stable or fall, which is a high-dependency claim. If that cost is higher, volatile, or varies by video type/length, the model's assumptions about feasibility break down.
  -> What is the empirical distribution of actual compute costs per produced video (by resolution/length/model), and how sensitive is the plan to increases there?

- **Assumes users prefer an unlimited £5/month model without demand testing** [HIGH] (pricing)
  The founder chose unlimited access at a single low price but provides no evidence this matches user willingness-to-pay or purchasing behavior. Customers often prefer credits, tiers, or pay-as-you-go for high-variance consumption; the team conflated a low stated price with revealed adoption. If buyers value predictability or need higher quality outputs, they may reject or abuse an unlimited plan.
  -> Do target customers choose unlimited monthly access at £5 in revealed choice tests, or do they prefer per-video/credit/tiered pricing?

- **Implicit dependency on cost-reduction or partner deals was unstated and unvalidated** [HIGH] (assumptions)
  Maintaining unlimited generation implies either sustained low compute costs or partner subsidies, yet no partnerships, supplier commitments, or roadmap for model efficiency were specified. The strategy assumes external conditions (hardware pricing, model efficiency) will remain favorable, a dependency that may not materialize within 18 months. Without proven channels to lower or stabilize costs, the business model is brittle.
  -> What specific cost-reduction or partnership paths are guaranteed or realistically achievable within the 18-month horizon?

- **Target buyer is unspecified — who values unlimited, cheap AI video?** [MEDIUM] (buyer)
  The document never defines whether the product targets hobbyists, creators, marketers, enterprises, or developers. Different buyer segments have dramatically different usage patterns, willingness to pay, and quality requirements, so conflating them is risky. Without a clear buyer, assumptions about average usage and pricing are unfounded.
  -> Which specific customer segment is the primary buyer and what evidence shows they will adopt an unlimited £5/month service?

- **No evidence on alternatives or why customers would choose unlimited over current solutions** [MEDIUM] (differentiation)
  The plan doesn't describe what customers use today (manual production, other AI tools, agencies) or why they would switch to low-cost unlimited generation. This is a misread risk: customers might value higher fidelity, brand safety, or editing control more than volume, so unlimited low-cost generation may not be compelling. The lack of differentiation validation means demand may be weaker than assumed.
  -> What current solutions do target users actually use, and why would they abandon them for unlimited low-cost AI video?

### unit_economics

The provided numbers (£5/month price, £2 compute per generated video, 20 videos/user/month) imply dramatically negative unit economics: compute cost alone is £40/user/month versus £5 revenue. The plan omits essential per-user costs (storage, CDN, support, payments), any evidence customers will pay £5 for unlimited generation, and any CAC/activation assumptions — all of which must be specified and tested before this is viable.

- **Price vs stated compute cost yields immediate, large negative margin** [CRITICAL] (pricing)
  You state £5/month revenue and ~£2 compute cost per generated video with an average of 20 videos/user/month. That implies ~£40/month compute cost per user against only £5 revenue — a ~£35/month loss per active user before any other costs. This single contradiction makes the stated business model financially impossible as written.
  -> Which of these three numbers is wrong — price (£5), cost per video (£2), or average usage (20 videos/mo) — and what validated evidence supports the corrected figure?

- **No evidence users will pay £5 for unlimited generation** [HIGH] (demand_evidence)
  The plan asserts a £5 price but provides no demand evidence, price sensitivity testing, or willingness-to-pay research. At the declared price you must show why customers would choose unlimited access rather than a metered model or competitors. Without customer willingness-to-pay validated, the revenue side is purely speculative.
  -> How did you determine customers will actually pay £5/month for unlimited video generation — show survey/experiment/conversion data or an MVP test plan?

- **No CAC, channels, or realistic acquisition plan at this price point** [HIGH] (acquisition)
  The document names no acquisition channels or expected CAC. Given the negative per-user margin even before CAC, you need channels that cost near-zero or convert virally — claims of 'viral growth' are unproven. Paid channels that produce paying users at scale are unlikely to be profitable at £5/month unless CAC is extremely low, which is unsubstantiated here.
  -> What acquisition channels will you use and what is the measured or projected CAC per paying customer (with supporting tests or benchmarks)?

- **Key per-user costs beyond compute are omitted** [MEDIUM] (key_numbers)
  Only compute cost per generated video is listed. There is no accounting for storage (raw/generated video), CDN/bandwidth, encoding/transcoding, backups, or per-user database costs. These recurring costs (particularly for video) can be material and will further worsen an already negative margin.
  -> Provide estimates for per-user monthly storage, CDN/bandwidth, encoding, and other infra costs (not just compute per generation) or explain why they are negligible.

- **Payback period and CAC recovery not specified and likely impossible** [MEDIUM] (key_numbers)
  With stated revenue and compute costs, gross margin is massively negative so any CAC will never be recovered. No payback period, LTV, churn, or CAC numbers are provided, so it's impossible to model unit economics over time. The business cannot scale if CAC cannot be paid back in a finite time.
  -> Show a one-line LTV = revenue - direct costs calculation and a CAD (CAC) payback analysis — how long to recover CAC given your current numbers?

- **Hidden/operational costs (support, moderation, refunds, fraud, compliance) unaccounted** [LOW] (assumptions)
  There is no mention of support staffing, content moderation, legal/compliance costs, chargebacks/refunds or fraud prevention. For a video generation platform these can be non-trivial, especially as usage and content variety scale, and will further erode margins if not planned for.
  -> List expected operational costs per active user (support, moderation, payments/chargebacks, compliance) or show tests estimating their magnitude.

### adversarial_competitor

This plan sells "unlimited" AI video generation at £5/month while stating a ~£2 cost per generated video and an average of 20 videos/month — a straight loss-making proposition and an open invitation for incumbents to crush. The product has no stated defensible differentiation, no acquisition plan, and no demand evidence; a well-funded competitor can cheaply replicate or out-distribute and out-price it. Below are concrete weak points to exploit and the single sharp questions the founder must answer.

- **Negative unit economics: £5 revenue vs ~£40 expected cost** [CRITICAL] (key_numbers)
  You claim £5/month price, ~£2 cost per video, and 20 videos/month per user — implying ~£40 cost per subscriber versus £5 revenue. That math makes the business model impossible as stated and is fatal unless costs, limits, or pricing change. A competitor can simply wait for burn or force price changes by offering temporary subsidies and then leverage scale.
  -> How do you reconcile the stated £5/month price with a ~£2 per-video cost and an expected 20 videos/month (i.e., where does the ~£35 loss per user come from)?

- **No defensible differentiation — trivial to copy** [HIGH] (differentiation)
  The offering is described only by price and usage; there's no unique model, IP, dataset, or UX that prevents replication. With modest engineering, an incumbent can integrate their existing models or cloud discounts and match features or price quickly. Without a lock-in asset, the startup is commoditized and can be neutralized by feature parity plus distribution.
  -> What unique asset (proprietary model, dataset, patent, exclusive partner, or distribution lock) prevents an incumbent from reproducing your service quickly?

- **Acquisition channel unspecified — incumbents can preempt distribution** [HIGH] (acquisition)
  No customer acquisition or go-to-market plan is given. Large competitors can push the same capability through existing channels (email lists, in-app prompts, bundled subscriptions, app stores, SEO) and capture demand before you build momentum. Your ability to reach users is the decisive battleground here.
  -> How will you acquire customers cheaply at scale, and why can't incumbents block those channels or out-spend you to capture them first?

- **Pricing is easily weaponizable by incumbents** [HIGH] (pricing)
  A well-funded competitor can neutralize your price advantage by bundling video generation into existing subscriptions, offering limited free tiers, or temporarily subsidizing usage to starve you of customers. You offer no lock or margin buffer to withstand predatory or bundled pricing moves from incumbents.
  -> How will you defend a £5/month price against incumbents who can bundle, subsidize, or temporarily undercut you to protect their user base?

- **No evidence users will create 20 videos/month or pay for "unlimited"** [MEDIUM] (demand_evidence)
  The plan assumes heavy usage (20 videos/month) and willingness-to-pay for unlimited access without any demand testing. If actual usage or willingness-to-pay is lower, the unit economics change but if higher, losses worsen. This is an unvalidated behavioral assumption that incumbents can quickly test and exploit.
  -> What evidence do you have that target users will both generate ~20 videos/month and pay £5 for unlimited access?

### execution_risk

The plan has a fatal internal contradiction between price and stated cost that prevents the product from being operable as described. Beyond that, the founder has not validated core inputs (per-video cost, user usage) nor addressed immediate blockers to shipping: legal/moderation requirements, infra/ops complexity, sequencing (abuse/quotas), or any go-to-market plan. Each of these gaps will prevent a safe, launchable product unless resolved before wider development.

- **Pricing vs stated cost makes the product impossible to operate as described** [CRITICAL] (key_numbers)
  You promise £5/month for unlimited video generation while claiming ~£2 compute cost per generated video and 20 videos/month per user. That implies ~£40 in compute cost per subscriber against £5 revenue — the service as priced cannot be paid for and therefore cannot be shipped at scale. This is an internal contradiction that must be resolved before any engineering work continues, because it determines everything from infrastructure budget to acquisition strategy.
  -> Which of these three numbers is wrong (price, £2/video cost, or 20 videos/user) — and how will you fund the resulting per-user loss while you build?

- **No empirical validation of usage or cost assumptions before building** [HIGH] (demand_evidence)
  You treat 20 videos/month and £2/video as facts but provide no evidence or test plan. Building full product, infra and billing on these untested numbers risks delivering a system that immediately bleeds money or doesn't meet user needs. The correct sequence is a small experiment to measure real per-video compute cost at your target fidelity and to observe real user generation behavior.
  -> What is your cheapest, time-boxed experiment to validate both real per-video compute cost at target quality and how many videos a typical user will generate in a month?

- **No plan for content-moderation, legal or regulatory blockers (deepfakes, copyright)** [HIGH] (assumptions)
  Unlimited video generation is a high-risk content product: deepfakes, copyrighted source material, defamation and age-related restrictions can create immediate legal exposure, payment processor blocks, or platform delistings. You haven't specified policies, detection systems, consent/rights flow, or a takedown/legal process — leaving shipping likely to be blocked by third parties or to create customer-facing takedowns.
  -> How will you prevent, detect, and legally handle disallowed or infringing generated content (e.g., deepfakes, copyrighted inputs) before offering unrestricted generation to subscribers?

- **Underestimated infrastructure and ops complexity for 'unlimited' video generation** [MEDIUM] (assumptions)
  An unlimited offering requires orchestration of heavy ML inference, GPU autoscaling, cost controls, video transcoding, storage (hot/cold) and CDN distribution plus monitoring and observability. The doc has no team plan, vendor choices, or runbooks; building these pieces is non-trivial and will take months and experienced SRE/ML engineers, not a few weeks.
  -> Who on the team will provision and operate GPU fleets, autoscaling, storage and monitoring, and what is your minimal infra design and ETA to run 100 concurrent video jobs safely?

- **No distribution or customer-acquisition plan to actually get paying users** [MEDIUM] (acquisition)
  You state a price but provide no channel, cost-per-acquisition estimate, or launch plan. Without a validated acquisition funnel you will build a product that has no tested way to reach customers or to prove demand, and you won't be able to stress-test costs with real users.
  -> What is the first paid or organic channel you will use to acquire subscribers and how will you measure its cost-effectiveness before a broader launch?

- **Sequencing risk: offering 'unlimited' before building throttles, billing controls and anti-abuse** [MEDIUM] (assumptions)
  Launching an unlimited plan without usage metering, fraud detection, rate-limits or emergency caps invites immediate abuse or runaway bills from a small number of users. The product should be shipped gated (invite/pilot), with hard quotas and monitoring, then relaxed once behavior and costs are understood.
  -> What minimal throttles, monitoring and emergency-cost cutoffs will you implement for launch to prevent a small cohort from creating catastrophic costs?

### evidence_audit

Evidence base: Weak. The document is pre-launch and provides no measured pilots, benchmarks or sourcing for price, cost-per-video, or usage. Most importantly, the stated numbers create an arithmetic contradiction that makes unit economics negative unless one or more inputs are changed and evidenced.

- **Unit economics are impossible: £5 revenue vs £40 cost per user** [CRITICAL] (key_numbers)
  At the stated inputs the plan loses money on every subscriber: revenue £5/month versus cost = 20 videos × £2 = £40/month, so contribution margin = £5 − £40 = −£35/user-month. This single arithmetic contradiction breaks the whole plan unless one of the core numbers (price, cost per video, or usage) is changed and evidenced. The document gives no measured data, pilot or scenario that resolves this gap.
  -> Show the concrete scenario that yields non-negative contribution margin at £5/mo by providing the measured cost-per-video and measured (or pilot-validated) average videos/month such that 5 ≥ cost_per_video × avg_videos.

- **Claimed ~£2 per generated video is unsourced and incompatible with price** [HIGH] (key_numbers)
  The document asserts ~£2 compute cost per video but provides no breakdown, benchmark or measurement. For the £5/mo unlimited price to be viable at the claimed 20 videos/month the per-video cost must be ≤£0.25 (5/20), so £2 is an order of magnitude too high. Without a cost model or evidence of dramatic cost-reduction, the £2 figure undermines feasibility.
  -> Provide a detailed cost breakdown and supporting measurements that justify the ~£2 per-video figure, and if you intend to keep £5/mo show a credible plan (with numbers) to reduce cost per video to ≤£0.25.

- **Average usage assumption (20 videos/month) is load-bearing and unsupported** [HIGH] (assumptions)
  Average videos/user of 20/month is central: it multiplies into compute costs and determines break-even. No survey, pilot, or comparable benchmark is provided. Given current pricing and claimed costs, break-even requires average usage ≤2.5 videos/month (5/2), so the assumed 20× is incompatible with any positive margin without other changes.
  -> Provide evidence (pilot data, surveys, or benchmarks) that average subscribers will generate 20 videos/month, or state the empirically supported average and show the resulting contribution margin at £5/mo.

- **Pricing (£5 unlimited) has no customer willingness-to-pay evidence** [MEDIUM] (pricing)
  The plan sets a customer-facing price and unlimited usage but offers no evidence customers would pay £5 for unlimited AI video generation. Willingness-to-pay, perceived value, and competitive alternatives determine whether users accept this price; none are cited. Pricing without demand evidence could lead to a mismatch between assumed subscriber numbers and reality.
  -> Share evidence that customers will pay £5/mo for unlimited video generation (e.g. surveys, landing-page signups with price, preorders, or paid pilot results).

- **No acquisition/CAC inputs provided to validate scale or LTV assumptions** [MEDIUM] (acquisition)
  The document lacks any acquisition plan or CAC estimate, so there's no way to assess whether subscribers can be acquired at a cost that makes the (already-negative) unit economics remotely recoverable via lifetime value. Even an idea-stage product must show a plausible path to acquiring users at a sustainable cost.
  -> Provide expected CAC with supporting data (pilot campaign results, channel benchmarks, or landing-page conversion rates) and show how CAC compares to customer lifetime contribution given your price and cost assumptions.


## Selected questions

- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: pre_mortem / Assumed compute cost of ~£2/video is unproven and treated as fixed [high]
  - why we're asking: unit_economics / Key per-user costs beyond compute are omitted [medium]
  - why we're asking: unit_economics / Payback period and CAC recovery not specified and likely impossible [medium]
  - why we're asking: adversarial_competitor / Negative unit economics: £5 revenue vs ~£40 expected cost [critical]
  - why we're asking: execution_risk / Pricing vs stated cost makes the product impossible to operate as described [critical]
  - why we're asking: evidence_audit / Unit economics are impossible: £5 revenue vs £40 cost per user [critical]
  - why we're asking: evidence_audit / Claimed ~£2 per generated video is unsourced and incompatible with price [high]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / Unvalidated usage-intensity assumption (20 videos/month) [critical]
  - why we're asking: unit_economics / No evidence users will pay £5 for unlimited generation [high]
  - why we're asking: adversarial_competitor / No evidence users will create 20 videos/month or pay for "unlimited" [medium]
  - why we're asking: execution_risk / No empirical validation of usage or cost assumptions before building [high]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Assumes users prefer an unlimited £5/month model without demand testing [high]
  - why we're asking: unit_economics / Price vs stated compute cost yields immediate, large negative margin [critical]
  - why we're asking: adversarial_competitor / Pricing is easily weaponizable by incumbents [high]
  - why we're asking: evidence_audit / Pricing (£5 unlimited) has no customer willingness-to-pay evidence [medium]
- **acquisition**: How will your first customers find you?
  - why we're asking: unit_economics / No CAC, channels, or realistic acquisition plan at this price point [high]
  - why we're asking: adversarial_competitor / Acquisition channel unspecified — incumbents can preempt distribution [high]
  - why we're asking: execution_risk / No distribution or customer-acquisition plan to actually get paying users [medium]
  - why we're asking: evidence_audit / No acquisition/CAC inputs provided to validate scale or LTV assumptions [medium]

## Answer given

**pricing**: The £5 per month is our current plan and we have not tested it with any customers.

Skipped: key_numbers, demand_evidence, acquisition

## Refined critique

### unit_economics

The math that is provided doesn't work: at the stated assumptions a subscriber generates £40 of compute cost per month (20 videos × £2) while paying only £5, producing a deeply negative unit margin. Key inputs are untested or missing: willingness-to-pay, CAC and channels, other operating costs (storage/support/moderation/payments), and no plan to reach positive gross margin or a reasonable payback period.

- **Per-user variable cost (20 × £2) is far larger than the price (£5)** [CRITICAL] (key_numbers)
  Using the founder's own numbers, a single subscriber producing 20 videos at £2 each costs £40/month while the subscriber only pays £5/month, a negative £35 margin before any other costs. This is an internal arithmetic contradiction that makes the stated business model impossible as written. Until one of these three numbers (cost per video, videos per user, or price) changes, the unit economics are fatally broken.
  -> Which of these three inputs is incorrect: the £2/video compute cost, the 20 videos/month usage assumption, or the £5/month price — and please supply evidence for the correct value?

- **Price (£5) is unvalidated — willingness-to-pay unsupported** [HIGH] (pricing)
  The founder declares £5/month but explicitly states it has not been tested with customers, so there is no evidence customers will accept this price, especially if alternative products exist. Pricing is the primary lever to fix the negative unit economics, but no willingness-to-pay data, experiments, or comparable benchmarks are provided. Without validated pricing the revenue side is speculative.
  -> What concrete evidence (surveys, paid trials, A/B pricing experiments, or preorders) supports that customers will pay £5/month for unlimited video generation?

- **No CAC, channels or acquisition plan — unrealistic at this price point** [HIGH] (acquisition)
  The document lists no customer-acquisition channels, expected CAC, or conversion funnels. Given the negative unit economics from the provided numbers, any realistic CAC (even very low) would worsen losses; the plan implicitly relies on zero-cost viral acquisition, which is unproven and unspecified. You cannot assess payback without explicit CAC assumptions and channel viability at this price.
  -> Which specific channels will you use, what CAC do you expect from each (with sources or benchmarks), and how can those CACs be profitable given the current per-user economics?

- **Gross margin at scale will be massively negative; payback period undefined** [MEDIUM] (assumptions)
  Given revenue of £5 and stated variable cost of £40 per active user, gross margin is deeply negative and will scale linearly with users — losses grow as you add customers. No payback period is calculable because LTV < 0 under current inputs. The plan lacks the levers (price change, cost reductions, usage caps) quantified to restore a positive gross margin or finite payback period.
  -> What precise changes (new price, target cost-per-video, or hard usage limits) will you implement and by how much to achieve positive gross margin and a finite payback period?

- **Missing other per-user operating costs (storage, support, payments, moderation, refunds)** [MEDIUM] (key_numbers)
  Only compute cost per generated video is mentioned; there is no estimate for storage/CDN, customer support, payment processing fees, content moderation, fraud prevention, chargebacks/refunds, or monitoring — all of which add to per-user cost. These omitted costs will further worsen already-negative unit economics and could introduce variable costs tied to video size/length.
  -> Have you estimated and included per-user costs for storage/CDN, support, payment fees, moderation, refunds/chargebacks, and fraud prevention, and if so what are those numbers?

- **No test plan to validate usage and price cheaply** [LOW] (demand_evidence)
  As an idea-stage plan the founder skipped which numbers are estimates vs. measured and has no described experiments to validate core inputs (usage per user, willingness-to-pay, cost per video at scale). The cheapest way to reduce uncertainty is missing: e.g., landing-page pricing tests, small paid pilot with limited users, or cost-profiling of the generation pipeline. Without quick tests the plan will continue to rely on unsupported assumptions.
  -> What is your cheapest, fastest experiment to validate (a) how many videos an average user will actually create and (b) whether customers will pay £5/month for the service?

### evidence_audit

Evidence base: Weak. There is no measured traction or validated customer data; all core unit economics and pricing are asserted, not sourced. The most important issue is an arithmetic contradiction: £5/month revenue versus ~£40 variable cost per user implied by the founder's numbers.

- **Arithmetic contradiction: per-user unit economics lose ~£35/month** [CRITICAL] (key_numbers)
  You state £5 revenue per subscriber per month, an expected 20 videos per subscriber per month, and a cost of ~£2 per generated video. That implies a variable cost of 20 × £2 = £40 per subscriber per month versus revenue of £5, a £35 loss before any other costs. Those three numbers cannot all be true for a viable subscription business as described. This is a direct arithmetic contradiction that breaks the core claim.
  -> Which of the three numbers is incorrect or how exactly will you cover the implied £35 loss per subscriber per month (provide corrected values or the mechanism that makes these economics work)?

- **No evidence users will generate 20 videos/month or accept unlimited usage** [HIGH] (assumptions)
  The plan's traffic and cost assumptions depend heavily on the claim that an average subscriber will create 20 videos per month. You provide no user research, pilot metrics, or comparative product usage to support that figure. If actual usage is materially different the unit economics and capacity planning change dramatically.
  -> Provide measured evidence (pilot data, user interviews with quantified intent, or usage metrics from a comparable product) that the average subscriber will generate ~20 videos per month and will pay £5 for unlimited generation.

- **£2 per-video compute cost is unsourced and likely incomplete** [HIGH] (key_numbers)
  The single per-video cost figure is asserted without a breakdown or measurement method. It may exclude important components (model inference variability by length/resolution, retries, orchestration, storage, CDN egress, previewing, or amortized training/engineering costs). An incorrect per-unit cost will change the entire economics calculation.
  -> Show the detailed cost calculation and measurement that produces the ~£2/video number (include model & instance type, average video length/resolution, GPU time per video, IO/storage/CDN, and whether this is peak or average cost).

- **No customer acquisition plan or implied CAC provided** [MEDIUM] (acquisition)
  You have not described how you will acquire the first customers or provided any estimate of CAC. Without an acquisition channel and an expected CAC, you cannot assess how many paying users you'll get or how long it takes to scale to a viable base — this matters especially given weak unit economics.
  -> What specific first-customer channels will you use and what are your expected CAC and conversion rates (or a conservative bound) to acquire the initial cohort of subscribers?


## Refinement meta

- Lenses re-run: unit_economics, evidence_audit
- Lenses not re-run: pre_mortem, adversarial_competitor, execution_risk
- Gaps filled: ['pricing']
- Gaps skipped: ['key_numbers', 'demand_evidence', 'acquisition']

## Reuse check

Re-sending the same refinement token refused with 409: yes
