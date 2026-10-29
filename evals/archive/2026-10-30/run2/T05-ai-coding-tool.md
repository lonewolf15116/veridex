# T05-ai-coding-tool

**Stage:** idea

## Input

I want to build an AI coding assistant that explains errors and suggests fixes for beginner programmers. It will cost $12 per month and compete with existing AI coding tools by providing simpler explanations.

**Reviewer expectation:** prioritises differentiation, distribution, willingness to pay; does not assume a crowded market makes success impossible.

## First critique

### pre_mortem

The plan rests on a set of unvalidated assumptions about who will pay, what beginners value, and what an LLM can reliably deliver pedagogically. The single most likely failure was misjudging willingness-to-pay for a subscription $12/mo product versus free or one-off solutions. Several unstated dependencies (clear buyer segment, proof that 'simpler explanations' beat working fixes, and reliable non-hallucinating output) would need cheap, early tests to validate before build.

- **Fatal assumption: beginners will pay $12/month for explanation-focused help** [CRITICAL] (pricing)
  You set a $12/month price with no evidence that target beginners prefer a paid subscription model for error explanations. At idea stage this is the product's revenue model and a single false belief here would kill adoption—if users prefer free, one-off answers or judge the value insufficient, the product won’t acquire or retain customers. This was treated as a given rather than a hypothesis to validate.
  -> Will the specific beginner segment you target actually convert to a $12/month subscription for explanation-focused debugging instead of using free one-off resources or integrated tools?

- **Misread signal: 'simpler explanations' as a defensible, preferred differentiation** [HIGH] (differentiation)
  You assume simpler explanations are the primary unmet need and that beginners will choose your product for clarity alone. You haven't shown that beginners consistently prefer conceptual simplicity over receiving immediate working fixes, example-based solutions, or interactive debugging. Without evidence, 'simple explanations' may be a weak or non-preferred axis of choice.
  -> Do beginners actually prioritize simpler conceptual explanations over concrete, immediately runnable fixes or guided debugging in real-world error-solving sessions?

- **Assumed AI can consistently produce pedagogically-correct, non-hallucinated explanations** [HIGH] (assumptions)
  The plan presumes LLMs can reliably generate accurate, beginner-appropriate explanations and fixes; you have no evidence this can be done at scale without frequent hallucinations or confusing jargon. If the assistant regularly gives incorrect explanations or skips necessary context, beginners will lose trust quickly and churn, undermining the value proposition.
  -> Can the model, with reasonable engineering and prompt design, consistently produce accurate, pedagogically-sound explanations for common beginner errors at an acceptably low error rate?

- **Wrongly assumed users will adopt a separate paid product instead of integrated/free workflows** [HIGH] (acquisition)
  You implicitly assume beginners will switch to or add a standalone subscription service for error help. There is no evidence about how beginners fit new tooling into their workflows (IDE, browser search, forums, classmates). If the natural behavior is to rely on existing free channels or IDE integrations, a separate app will see low usage even if valuable.
  -> Will target beginners choose a separate subscription product for error explanations rather than continuing to use their current mix of IDE hints, search, community Q&A, or ad-hoc help?

- **Unclear who 'beginner programmers' actually are and how their needs differ** [MEDIUM] (buyer)
  The target 'beginner programmers' is stated but undefined (students, bootcamp grads, hobbyists, career-switchers). Different subgroups have different pain points, willingness-to-pay, and channels. Treating them as a single market obscures which segment to validate first and may have led to building the wrong MVP for the most reachable/valuable group.
  -> Which specific beginner subgroup is the primary early adopter (e.g., CS students, bootcampers, hobbyists), and how do their error-solving behaviors, budgets, and preferred channels differ?

### unit_economics

The document gives a price ($12/mo) and a user persona (beginner programmers) but provides no unit-economics inputs required to judge viability: there are no cost-per-user estimates (compute, storage, support, payments), no evidence users will pay $12, no CAC or channels, and no margin or payback calculations. Before building, the founder must (1) validate willingness-to-pay with cheap experiments and (2) estimate marginal serving costs per active user to know what CAC can be rationally paid.

- **Price ($12/mo) is asserted with no willingness-to-pay evidence** [HIGH] (pricing)
  The plan fixes a $12/month price but offers no evidence (surveys, tests, comparative pricing, or conversion assumptions) that beginner programmers will pay that amount. Revenue per user is therefore unsupported and could be far lower than assumed. Without validated ARPU, you cannot calculate LTV or acceptable CAC.
  -> What direct evidence (pricing tests, paid pilots, or conversion benchmarks) shows beginners will actually subscribe at $12/month?

- **No estimate of marginal cost to serve a single user (compute + storage + support + payments)** [HIGH] (key_numbers)
  There are no estimates for inference costs (LLM or models), storage, support headcount per user, or payment processing fees. AI assistants commonly have meaningful per-session compute costs that can exceed a low monthly ARPU if usage is high. Without a per-user cost, projected gross margin is unknown and the business could be loss-making at any scale.
  -> What is your estimated marginal monthly cost per active paying user, broken down by inference/compute, storage, support, and payment fees?

- **Customer acquisition plan and acceptable CAC are undefined** [HIGH] (acquisition)
  The strategy names no acquisition channels, conversion funnels, or CAC targets; at $12/month ARPU the sustainable CAC may be low. Claims of 'competing by simpler explanations' imply organic/viral acquisition but no mechanism, virality loop, or paid channel economics are given. Without channel-level CAC and conversion rates you cannot assess payback or scale feasibility.
  -> Which specific acquisition channels will you use and what is the expected CAC and conversion rate for each, so we can judge if payback is achievable at $12/mo?

- **Gross margin at scale is unstated and likely sensitive to model costs** [MEDIUM] (key_numbers)
  No gross margin projection is provided for current or scaled usage. If per-inference costs are significant, margins could shrink substantially as active-user sessions increase, and hosting/ops can add fixed/variable costs. You need margin scenarios at different scale points to know whether the product can be profitable.
  -> What are projected gross margins per user at 1k, 10k, and 100k paying users (with clear assumptions for model/inference cost and support overhead)?

- **Payback period and churn assumptions are missing** [MEDIUM] (key_numbers)
  No churn rate, LTV, or CAC-payback calculations are included, so payback period is unknown. For subscription businesses with modest price points, small changes in churn or CAC materially change viability. The document doesn't state what CAC is acceptable for a given churn or how quickly customer acquisition spend must be recovered.
  -> What churn rate and LTV assumptions do you plan to use, and what CAC would be acceptable to achieve a payback period you consider viable (e.g., <12 months)?

- **Hidden operational costs (moderation, refunds, fraud, liability) are not budgeted** [MEDIUM] (assumptions)
  There is no mention of costs for content moderation (bad/misleading code), customer support for debug/refund requests, chargebacks, or legal/compliance risk management. These costs often scale non-linearly for developer tools that produce executable code or advice, and they can materially reduce margins or increase churn.
  -> How will you budget for moderation, dispute handling/refunds, chargebacks, and any compliance/legal costs as the user base grows?

### adversarial_competitor

This idea rests on one narrow differentiator — "simpler explanations" for beginner programming errors — that a well-funded incumbent can neutralize for pennies by shipping a beginner-mode or an "ELI5 / Simple Explanation" toggle in existing tools, bundling it into free tiers, and leveraging massive distribution (IDE plugins, SEO, app stores, bootcamp partnerships). The cheapest kill: add a labeled "Explain like I'm a beginner" preset to our free chat/assistant product, push it to existing users and extension stores, and undercut the $12/month price with a free or enterprise-bundled feature. Before building, the founder must prove paying demand from beginners and a defensible, non-copyable way their explanations are superior — both are currently missing.

- **Core differentiation is trivially copyable** [CRITICAL] (differentiation)
  The product's entire competitive claim is 'simpler explanations.' That is a UI/prompt design choice — not a proprietary model or dataset — and can be implemented as a single preset or toggle in any incumbent assistant within days. Incumbents can label it "Beginner Mode" and ship it to millions of existing users, instantly removing the startup's unique value. Without a demonstrated, hard-to-replicate method (patentable algorithm, exclusive dataset, or community), the differentiation is not defensible.
  -> What concrete, non-trivial mechanism makes your explanations unique and hard for an incumbent to copy in a week?

- **No evidence beginners will pay $12/month for simpler answers** [HIGH] (demand_evidence)
  The price point assumes beginners will convert to a subscription rather than rely on free alternatives (ChatGPT, StackOverflow, docs, course instructors). There's no data on willingness-to-pay, retention, or how much value 'simpler explanations' creates for novices. If users treat it as an occasional help tool, $12/mo is unlikely to stick.
  -> How will you prove that a meaningful share of beginner programmers will pay $12/month for simpler error explanations rather than use free channels?

- **Target buyer is undefined and too broad** [HIGH] (buyer)
  The plan says 'beginner programmers' but does not segment between self-taught hobbyists, CS students, bootcamp grads, or junior devs. These groups have different acquisition channels, price sensitivity, and help habits; without a crisp buyer persona you can't optimize copy, distribution, or product fit.
  -> Which exact beginner segment are you targeting first, and why will they prefer a paid assistant over free alternatives?

- **No go-to-market or acquisition plan — incumbents can drown you** [MEDIUM] (acquisition)
  There is no stated acquisition strategy (SEO, IDE plugins, partnerships with bootcamps, app store placement, or community distribution). A competitor can quickly weaponize existing distribution: push to IDE marketplaces, cross-promote to millions of active users, SEO-optimize "how to fix X error" content, and partner with schools to capture beginners cheaply.
  -> What specific, low-cost acquisition channels will you use to reach beginners and at what expected cost per acquisition?

- **Pricing is exposed to bundling and freemium attack** [MEDIUM] (pricing)
  $12/month is easy for incumbents to undercut by adding a free beginner tier, offering the feature as part of a broader bundle, or subsidizing it for educational partners. The founder offers no rationale why incumbents couldn't include this as a free feature or bundle it with enterprise/paid offerings.
  -> Why can't incumbents neutralize your price advantage by giving a beginner-mode away free or bundling it into existing paid plans?

- **Competitive landscape and current alternatives aren't mapped** [LOW] (alternatives)
  The doc says 'existing AI coding tools' but doesn't identify which tools beginners actually use today (ChatGPT, GitHub Copilot, StackOverflow, teacher/mentors, etc.) or what specific gap remains after those options. Without that map you can't prioritize features or craft messaging that beats current behavior.
  -> Which exact alternatives do beginners use today to fix errors, and why will they switch to your product?

### execution_risk

The plan states a clear product idea and price but omits nearly all operational details required to build and ship a paid AI assistant. The biggest risks are building complex, language-specific diagnostics and integrations before validating demand and distribution, and underestimating technical work needed to run/reproduce code and guarantee correct fixes. Several assumptions (who pays, how to acquire them, privacy/IP handling) are unstated and will block shipping if not resolved early.

- **No evidence beginners will pay $12/mo for 'simpler explanations'** [HIGH] (demand_evidence)
  The document asserts a $12/month subscription but provides no evidence beginners will pay that amount (or pay at all). If willingness-to-pay is low, the whole subscription model fails. The cheapest tests (landing page preorders, paid ads, or concierge explained-error sessions) are not mentioned.
  -> What minimal experiment will you run in days to prove beginners will pay $12/month (or any price) for simpler error explanations?

- **No acquisition or distribution plan for converting users to paid subscribers** [HIGH] (acquisition)
  There is no channel strategy: how to find beginners, onboard them, or convert free users to $12/month subscribers. Building product features before a proven acquisition funnel risks spending months on a product with no customers. Common low-effort channels (coding bootcamps, YouTube, teacher partnerships) are not considered.
  -> Which 1–2 specific acquisition channels will you test first and what is the concrete experiment to validate they scale to payers?

- **Technical blocker: diagnosing and fixing errors reliably without running user code** [HIGH] (assumptions)
  Accurate, actionable fixes often require reproducing runtime errors in a controlled environment; relying only on static error strings or LLM guesswork will produce incorrect or unsafe fixes. Building multi-language parsers, sandboxes, and secure execution environments is substantial engineering and security work that is not acknowledged.
  -> Will you (a) reproduce user code in a sandbox, (b) rely on static/error-text parsing, or (c) use another approach — and how long and costly is that work to implement safely for even one language?

- **Sequencing mistake: plan implies building product before validating explanation quality** [MEDIUM] (assumptions)
  The core differentiator is 'simpler explanations,' yet there's no plan to validate explanation quality against alternatives. Shipping IDE plugins, subscription billing, and LLM integration before manual-testing explanation scripts risks months of work for an unproven core feature.
  -> What lightweight process will you use to validate explanation quality (e.g., manual human-generated explanations, A/B tests) before engineering a full product?

- **Privacy/IP and compliance gaps for user-submitted code are unstated** [MEDIUM] (assumptions)
  Users will paste source code that may be proprietary or sensitive. There is no plan for data handling, retention, or consent; this creates legal and trust risks (GDPR, school policies, company policies) that can block adoption by educators or companies.
  -> How will you handle user code privacy, retention, and consent in your minimum viable implementation to avoid legal or adoption blockers?

- **Differentiation vs. existing tools and current user behavior is unclear** [MEDIUM] (differentiation)
  Claiming 'simpler explanations' as the competitive edge doesn't explain why beginners would switch from ChatGPT, StackOverflow, or free documentation. Without a clear, testable differentiation, distribution and retention assumptions will fail.
  -> What specific explanation outcomes (metrics) will you measure to prove your output is meaningfully simpler and more helpful than existing free alternatives?

### evidence_audit

Evidence base: Weak. This is an idea-stage plan with no revenue, customers, or tested claims — only a declared product concept and price. Nothing in the document proves demand, willingness-to-pay, acquisition economics, or differentiation; the most important gap is measured demand and price validation.

- **No measured demand from target users** [HIGH] (demand_evidence)
  The document asserts beginners will want an AI that explains errors simply, but provides no primary evidence (interviews, surveys, landing-page signups, or paid preorders). Without measured demand you cannot tell if the problem is real or sufficiently painful to pay for a $12/month product. This is the single largest evidence gap for an idea-stage product.
  -> Please provide measured demand evidence: either (a) transcripts/notes from at least 20 interviews with target beginner programmers reporting this specific pain and willingness to pay, or (b) a landing page test that produced at least 100 unique signups and a measured conversion rate to paid commitments at $12/mo.

- **Primary paying customer is undefined** [HIGH] (buyer)
  The plan says 'beginner programmers' but does not define which buyer will pay (self-taught hobbyists, CS undergrads, bootcamp students, teachers, parents, etc.). Different buyer groups have different willingness-to-pay and acquisition channels, so this is a load-bearing ambiguity. Without picking a primary paying segment you cannot validate pricing, acquisition or product features.
  -> Name the single primary paying customer segment you will target first (e.g., self-taught beginners, CS students, bootcamp students) and attach evidence that this segment both experiences the stated pain and is likely to pay (interview notes or quantitative signals).

- **Price ($12/mo) is asserted with no willingness-to-pay evidence** [HIGH] (pricing)
  You state a $12/month price but provide no test or rationale to show target users will pay that. $12/mo equals $144/year per subscriber, but without measured conversion or LTV/CAC this number is arbitrary and load-bearing for any revenue forecast. At idea stage pricing must be validated with customers.
  -> Provide direct pricing-validation data: a landing-page pre-order or paid-signup test showing paid conversion at $12/mo (report visitor→paid conversion and at least 30 paid commitments), or at minimum the results of a pricing-sensitivity survey with N≥100 target users.

- **No acquisition channel or unit-acquisition metrics** [MEDIUM] (acquisition)
  The document contains no acquisition strategy or tested channel metrics (traffic, conversion, CAC). Without at least one channel with measured conversion rates you cannot project customer growth or bound CAC relative to $12/mo. This prevents any credible revenue or payback calculation.
  -> Show a tested acquisition funnel for the chosen target segment with measured metrics (visitors → email → trial → paid) including conversion rates and an empirical or pilot CAC estimate from a real channel (paid ad, content, partnership) or explain how you will obtain those metrics with a concrete test.

- **Unproven differentiation versus existing AI coding tools** [MEDIUM] (differentiation)
  The claim that 'simpler explanations' will beat existing AI coding tools is an assertion without comparative evidence. Competitors already provide explainability and varied output styles; it's unknown whether simplicity is preferred, sufficient, or defensible. Differentiation must be demonstrated with user preference tests or feature outcomes.
  -> Provide comparative user-test results (e.g., blind comparisons with 15–30 target users) showing a measurable preference for your simpler explanations over at least one existing tool, and which specific attributes (clarity, actionability) drive that preference.

- **Key unit-economics inputs (conversion, churn, LTV, CAC) are missing** [MEDIUM] (key_numbers)
  There are no stated assumptions or measurements for conversion rate (free→paid), monthly churn, CAC, or LTV. Even one given figure—$12/month—cannot be assessed for sustainability without these inputs (e.g., $12/mo = $144/year per user; whether that covers CAC depends on churn and CAC). Missing these numbers prevents any internal consistency checks.
  -> State your assumed or measured conversion rate to paid, expected monthly churn, and target CAC; show the simple arithmetic that converts $12/mo into LTV and payback time (e.g., LTV = $144 / churn, CAC = X → payback = CAC / monthly net revenue).


## Selected questions

- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / Fatal assumption: beginners will pay $12/month for explanation-focused help [critical]
  - why we're asking: unit_economics / Price ($12/mo) is asserted with no willingness-to-pay evidence [high]
  - why we're asking: adversarial_competitor / Pricing is exposed to bundling and freemium attack [medium]
  - why we're asking: evidence_audit / Price ($12/mo) is asserted with no willingness-to-pay evidence [high]
- **differentiation**: Why would customers choose this over the alternatives?
  - why we're asking: pre_mortem / Misread signal: 'simpler explanations' as a defensible, preferred differentiation [high]
  - why we're asking: adversarial_competitor / Core differentiation is trivially copyable [critical]
  - why we're asking: execution_risk / Differentiation vs. existing tools and current user behavior is unclear [medium]
  - why we're asking: evidence_audit / Unproven differentiation versus existing AI coding tools [medium]
- **acquisition**: How will your first customers find you?
  - why we're asking: pre_mortem / Wrongly assumed users will adopt a separate paid product instead of integrated/free workflows [high]
  - why we're asking: unit_economics / Customer acquisition plan and acceptable CAC are undefined [high]
  - why we're asking: adversarial_competitor / No go-to-market or acquisition plan — incumbents can drown you [medium]
  - why we're asking: execution_risk / No acquisition or distribution plan for converting users to paid subscribers [high]
  - why we're asking: evidence_audit / No acquisition channel or unit-acquisition metrics [medium]
- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: adversarial_competitor / No evidence beginners will pay $12/month for simpler answers [high]
  - why we're asking: execution_risk / No evidence beginners will pay $12/mo for 'simpler explanations' [high]
  - why we're asking: evidence_audit / No measured demand from target users [high]

## Answer given

**demand_evidence**: I haven't asked any beginner programmers whether they would pay for this; it's based on my own experience learning to code.

Skipped: pricing, differentiation, acquisition

## Refined critique

### pre_mortem

The strategy failed because core demand and willingness-to-pay were never validated and the product's single stated differentiator ('simpler explanations') did not map to a defensible advantage over free alternatives. Foundational assumptions about who the buyer is, how much they'd pay, and whether an LLM can reliably produce pedagogically sound fixes proved false or untested. The most likely killing blow was that beginners continued to use free LLMs, docs, and community help rather than subscribe, so there were no paying users to sustain the product.

- **No evidence users will pay — fatal assumption** [CRITICAL] (demand_evidence)
  The founder set a $12/month price but has not spoken to any target users or gathered willingness-to-pay data. This assumes stated preference from the founder's own experience maps to actual purchase behavior. Over 18 months the product never acquired enough paying users because willingness-to-pay was never validated and turned out to be much lower or non-existent.
  -> Will target beginner programmers actually pay $12/month for this service (vs using free alternatives), and how do you know?

- **Pricing model and price point unsupported** [HIGH] (pricing)
  A monthly $12 price was chosen without testing pricing models, commitment preferences, or competitor pricing. Beginners often prefer free, one-time purchases, course bundles, or institutional provisioning (schools/bootcamps), so the $12/subscription assumption was misaligned with buyer preferences. As a result, trials showed low conversion to subscriptions.
  -> Why is a $12/month subscription the right pricing structure and price for the specific beginner segment you intend to serve?

- **Differentiation ('simpler explanations') was insufficient against free alternatives** [HIGH] (differentiation)
  The strategy assumes simpler explanations alone will make users choose this product over free LLMs, StackOverflow, course forums, or IDE-integrated help. In practice, those alternatives already produce explanations and many beginners prioritized integration, interactivity, or free access over simplified prose. The product therefore failed to capture users who had easier-to-access substitutes.
  -> Why will beginners choose this product's 'simpler explanations' instead of free LLMs, community answers, or IDE/help integration?

- **Assumed LLM reliability and pedagogical quality did not hold** [HIGH] (assumptions)
  The plan depends on an AI reliably diagnosing errors and producing beginner-friendly, correct explanations and fixes. This assumption wasn't tested; early users reported incorrect or confusing fixes that eroded trust. Because beginners are fragile learners, inconsistent accuracy was enough to stop adoption and drive negative word-of-mouth.
  -> Can the model consistently generate correct, pedagogically appropriate explanations and fixes for the common beginner errors in our target scope?

- **Target buyer is underspecified (who pays?)** [MEDIUM] (buyer)
  Saying 'beginner programmers' is too broad — self-learners, CS students, bootcamp attendees, hobbyists and corporate trainees have different pain points and payment routes. Without a specific buyer profile, you couldn't tailor messaging, pricing, or acquisition, so experiments failed to find an early paying cohort.
  -> Which exact beginner segment (e.g., self-learners, bootcamp students, CS101 students) is the paying customer, and why will they pay?

- **No acquisition hypothesis or channel tests** [MEDIUM] (acquisition)
  There was no plan or evidence for how to reach the chosen beginner segment cost-effectively. Assumed organic discovery didn't materialize; free alternatives dominated search and referral channels. Without early, cheap customer acquisition tests, the product never found a growth channel to reach enough trialists to prove demand.
  -> Through which specific channels will you acquire beginners and can you demonstrate low-cost conversion from those channels in an experiment?

### evidence_audit

Evidence base: Weak. The plan is entirely pre-launch and rests only on the founder's personal experience; there are no user interviews, pricing tests, acquisition experiments, or comparative usability data. The most important gap is the lack of validated demand and willingness-to-pay from beginner programmers for a $12/month product.

- **No demand evidence from target users** [HIGH] (demand_evidence)
  The founder admits they have not asked any beginner programmers whether they would pay. Willingness to pay and the value of 'simpler explanations' are load-bearing for a subscription product but currently unsupported by interviews, surveys, trials or preorders. Without basic user validation the central commercial claim (people will pay $12/month) is untested.
  -> Provide concrete validation from the target group: run and report at least 30 structured interviews or a landing-page test showing quantified willingness-to-pay (how many said they'd pay $12/mo and why), including raw counts and methodology.

- **Price point ($12/mo) is asserted, not tested** [HIGH] (pricing)
  The $12/month price is stated with no supporting evidence or rationale. Price is a key input to revenue, conversion and positioning; an unsupported price makes downstream revenue or MRR targets meaningless. There is no evidence of sensitivity testing, competitor comparison, or conversion assumptions at that price.
  -> Show results of a pricing test or willingness-to-pay study for $12/mo among beginners (e.g., survey with at least 100 respondents or paid-preorder signups), reporting the conversion rate to paid at $12 and the test method.

- **No validated customer acquisition channel or CAC estimate** [MEDIUM] (acquisition)
  The plan includes no data or experiments showing how beginner programmers will be reached or how much it costs to acquire them. Acquisition and CAC are necessary to forecast growth and unit economics; without any measured channel performance the plan can't produce credible customer or revenue projections.
  -> Run and report one acquisition experiment (e.g., community post, paid ad, partnership) targeted at beginners that produced measurable signups; supply visitors, signups, and cost per signup so you can compute an initial CAC.

- **Differentiation claim ('simpler explanations') is vague and untested** [MEDIUM] (differentiation)
  The product's competitive edge is stated as 'simpler explanations' but there is no evidence this is distinct from or preferred over existing AI coding tools. It's unclear whether simplicity translates into higher conversion, retention or task success for beginners versus alternatives.
  -> Provide comparative user-test results (even small-scale: 10–20 beginners) showing a measurable preference or better task completion/understanding using your explanations versus a leading existing tool, with the metrics you used.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['pricing', 'differentiation', 'acquisition']

## Reuse check

Re-sending the same refinement token refused with 409: yes
