# T03-student-marketplace

**Stage:** idea

## Input

I'm planning a marketplace where university students rent textbooks, calculators and other study equipment to one another. The platform would charge a 10% fee on each transaction and launch at one UK university before expanding.

**Reviewer expectation:** recognises two-sided liquidity, trust, disputes, low transaction frequency without declaring the idea unviable.

## First critique

### pre_mortem

The plan rests on multiple untested assumptions about student demand, two-sided liquidity, and willingness to accept peer-to-peer risk and fees. The founder provided no evidence for demand, no plan to reach simultaneous supply and demand at a single university, and no answers on how damage/loss, returns and pricing will be handled. The most likely failure is that the marketplace never reaches repeatable transaction volume because students prefer existing channels or refuse the risk/terms of P2P rentals.

- **No evidence students will prefer peer-to-peer rentals over current options** [CRITICAL] (demand_evidence)
  The document contains no evidence (stated or revealed) that students want to rent textbooks/equipment from peers rather than buy, rent from established vendors, or borrow. The idea assumes latent demand for P2P rentals without surveys, experiments, or pre-commitments. Cheap first tests would be a landing page with signups, simple classified listings to measure response, or a concierge MVP to observe real willingness to pay and rent. Without demonstrated demand the marketplace model cannot launch.
  -> Can you show revealed demand at the target university (actual pre-commitments or completed pilot transactions) proving students will both list items and pay to rent them?

- **Launching at one university assumes achievable two-sided liquidity** [HIGH] (assumptions)
  A two-sided marketplace requires enough simultaneous supply and demand; the founder assumes one UK university will provide sufficient matching volume but provides no evidence about catalog depth, course seasonality, or concentration of needed items. If listings are sparse or renter demand fragmented by course/edition, transactions stall. The first test is to recruit a minimum viable number of sellers and renters for the same courses/dates manually and measure match rates.
  -> Can you secure a repeatable number of simultaneous listings and renter matches at the chosen university for the courses/periods you target?

- **Trust, damage, and returns logistics assumed solvable but unvalidated** [HIGH] (assumptions)
  The plan omits how loss, damage, late returns, cleaning, and exchange logistics will be handled or who bears the risk/cost. Students may refuse to lend valuable items without escrow, deposits, or insurance, or renters may avoid listings with onerous deposit terms. A simple validation is running a small number of manual transactions with proposed deposit/penalty rules to measure default and rejection rates.
  -> What concrete mechanism (deposit, escrow, insurance, university mediation) will make owners comfortable lending and renters comfortable paying, and will students accept those terms in practice?

- **10% platform fee is asserted without testing fee acceptance or who bears it** [HIGH] (pricing)
  Charging a 10% fee is presented as given but there is no evidence students will accept that fee or whether it will be added to renter prices or taken from owners' payouts. Fee sensitivity can meaningfully change willingness to list or to rent. Quick tests: A/B experiments on pricing messaging in listings or explicit pre-signup offers to gauge tolerance for a 10% cut.
  -> Have you validated that the 10% fee is acceptable to both owners and renters (or which side will bear it) using real pricing experiments?

- **Competitive alternatives and differentiation are unspecified** [MEDIUM] (alternatives)
  The founder did not identify existing alternatives students currently use (university bookshops, official rental services, secondhand marketplaces, course-share groups) or explain why students would choose a peer marketplace instead. Without a clear differentiation, you risk building a marginally better listing that users won't switch to. A quick step is mapping current channels at the university and interviewing students about why they use them.
  -> What do students currently use today to access the same items, and what specific advantage will make them switch to your platform?

### unit_economics

The document only states a 10% marketplace fee and a launch at one UK university—no other unit-economic inputs are provided, so the math cannot be evaluated. Critical load-bearing numbers are missing: average transaction value (AOV), transactions per user, who pays the fee, per-transaction costs (payment fees, support, hosting), CAC and channels, and expected refund/fraud rates. First tests to unlock finances: measure AOV and willingness-to-pay (e.g. landing page or concierge listings with pre-commitments), and run a small number of pilot transactions to observe real per-transaction costs and dispute rates.

- **No average transaction value, frequency, or LTV (core revenue drivers missing)** [HIGH] (key_numbers)
  The plan gives a 10% fee but provides no AOV, transactions per user per term/year, retention or lifetime value. Without those numbers you cannot compute revenue per user or whether a 10% take rate yields enough revenue to cover costs. This absence makes any margin, payback, or scalability calculation impossible.
  -> What is the expected average transaction value and transactions per user per year (or lifetime) at launch university?

- **Pricing mechanics and willingness-to-pay are unspecified** [HIGH] (pricing)
  It's unclear who pays the 10% fee (lender, renter, or split), whether price elasticity was tested, or whether students will accept adding a fee to tight textbook budgets. A nominal take rate is meaningless without evidence users tolerate it or a pricing model showing who bears it and how it affects demand.
  -> Who pays the 10% fee (lender, renter, or both), and what empirical evidence supports students accepting that fee at typical rent prices?

- **Customer acquisition plan and CAC are not defined** [HIGH] (acquisition)
  No acquisition channels or estimated CAC are provided. Launching at one university implies campus channels, but the strategy lacks realistic channel choices and cost estimates to evaluate payback. At low AOVs, many campus channels (paid ads, partnerships) may produce CACs that exceed contribution margin.
  -> Which specific channels will you use to acquire students at the target university and what is your target CAC per acquired user?

- **Per-transaction and per-user cost-to-serve are not quantified** [MEDIUM] (key_numbers)
  There is no breakdown of payment processing fees, storage/hosting, customer support load, listing moderation, or accounting costs. Even with a 10% fee, per-transaction fixed costs (e.g., 2–3% card fees, support time, hosting) and any holding/escrow costs could consume most or all take rate if unaccounted for.
  -> Provide per-transaction and per-user cost estimates for payment processing, hosting, customer support, escrow/holding, and any required infrastructure.

- **Hidden operational costs (logistics, deposits, refunds, fraud, moderation) are unaddressed** [MEDIUM] (assumptions)
  The plan does not state how damage, late returns, theft, disputes, chargebacks, or fraud will be handled and who bears liability. These events are common in peer-to-peer rentals and can create substantial variable costs or require insurance/escrow that reduce margin.
  -> How will you handle deposits/insurance, damage claims, late returns, disputes and chargebacks, and what rates/costs do you expect from these events?

- **No gross margin, payback period or break-even analysis** [MEDIUM] (key_numbers)
  There is no projection of gross margin today versus at scale, nor a CAC payback period or sensitivity to key variables. Without modelling how take rate, AOV, CAC and support cost interact, it's impossible to know if the business can reach positive unit economics as it scales.
  -> What is your projected gross margin per transaction and the expected CAC payback period under baseline assumptions?

### adversarial_competitor

This is a simple peer-to-peer campus rental marketplace with no evident moat: 10% fee, single-university pilot, and no answers on logistics, trust, or go-to-market. A well-funded incumbent can neutralize it quickly by adding a 'rent' flow to an existing marketplace/app, undercutting fees or subsidizing supply, and leveraging campus distribution and brand to lock demand. Testable weaknesses are clear and cheaply exploitable.

- **No defensible differentiation — trivial to replicate in one product change** [HIGH] (differentiation)
  Founder presents a generic P2P rental marketplace without a unique feature that incumbents can't copy. The core value (rent textbooks/equipment) can be implemented as a toggle or new listing type inside any existing campus marketplace or classifieds app. An incumbent can ship a 'rent' option, reuse existing payments/ratings, and neutralize the startup overnight.
  -> What unique, hard-to-copy product or operational capability makes you the only credible marketplace for campus rentals versus an incumbent shipping a 'rent' listing type?

- **Go-to-market and distribution are unspecified — easily dominated by bigger players** [HIGH] (acquisition)
  The plan only says 'launch at one UK university' with no channels or acquisition strategy. Well-funded competitors can leverage existing user bases, campus reps, university partnerships, SEO for textbook queries, app store pushes, and bookstore/channel partnerships to quickly capture supply and demand. Without a locking distribution play, the founder will be outpaced.
  -> What exact acquisition channels (student groups, uni partnerships, SEO, app store, retail partners) will you use and why can't an incumbent replicate and scale them faster?

- **Trust, logistics and risk management are unaddressed — incumbents can offer safer UX** [HIGH] (assumptions)
  No plan is given for deposits, damage, late returns, authentication of items, insurance, or dispute resolution. These are the hard parts of rentals that determine conversion. Larger players can offer escrow, integrated insurance, campus-verified identities, and returns logistics as defaults, making the founder's bare marketplace look risky.
  -> How will you handle deposits, damage claims, late returns, identity verification and returns logistics in a way that builds trust and is scalable?

- **Pricing is vulnerable — 10% fee is easy to undercut or subsidize** [MEDIUM] (pricing)
  Charging 10% on transactions gives incumbents a clear lever: they can launch with 0% fees, promotional credits, or subsidized shipping to drown the marketplace. With deeper pockets they can afford temporary negative margin to lock supply/demand and make your fee-based model uncompetitive.
  -> Why will students and listers accept a 10% platform fee when a better-funded competitor can subsidize transactions or offer superior economics?

- **No demand evidence — unclear students will list or prefer P2P rentals** [MEDIUM] (demand_evidence)
  The document provides no evidence that students want peer-to-peer rentals rather than libraries, buy/sell groups, course reserves, or campus bookstores. Without even pilot surveys or experiments, it's unknown whether enough supply and demand will appear to sustain a marketplace.
  -> What are the simplest, cheapest tests you will run in the target university to prove both supply (students willing to list items) and demand (students willing to pay to rent)?

- **Buyer segment and unit flows are unspecified — which students and items drive liquidity?** [LOW] (buyer)
  Founder hasn't specified which student groups (first-years, STEM, postgrads) or which items (core textbooks vs. calculators vs. lab equipment) they'll prioritize. Different segments have different turnover, price points, and trust needs; lack of focus makes go-to-market and product decisions scattershot.
  -> Which specific student segments and item categories will you target in the pilot to reach the needed supply-demand liquidity quickly?

### execution_risk

The plan is directionally plausible but omits the operational, regulatory and technical primitives a rental marketplace needs to actually run. The biggest risks are not market demand but the unaddressed logistics/escrow/liability model, trust & safety for peer-to-peer exchanges, payments/compliance work, and no concrete university launch playbook — any of which will stop shipping or cause immediate failure at launch.

- **No end-to-end operational model for pickups, returns, damage and escrow** [CRITICAL] (assumptions)
  The document assumes transactions can just happen on-platform with a 10% fee but gives no process for custody of items, inspection on return, deposits/holds or insurance. Without an escrow hold or a concrete returns/damage resolution flow you will see lost items, chargebacks and legal liability that can sink the marketplace before scale. This is a blocking implementation and legal problem, not a later polish.
  -> What is the exact end-to-end exchange flow you'll operate on day one, including who physically holds items, how funds are escrowed/held and released, how damage/loss claims are resolved, and who bears liability?

- **No trust & safety plan for campus peer-to-peer transactions** [HIGH] (assumptions)
  Students may be unwilling to meet strangers or hand over textbooks/expensive equipment without clear trust mechanisms. The doc lacks ID verification, ratings, dispute resolution, supervised drop-off options, or campus partnership agreements — all of which are required to get both sides to transact. Failure here will mean listings exist but no one books them, or worse, reputational/physical safety incidents.
  -> How will you establish and enforce trust and safety at launch (identity verification, rating system, safe pickup locations or campus partnerships) so students are comfortable listing and borrowing?

- **Payments, escrow and compliance work is unspecified and likely non-trivial** [HIGH] (assumptions)
  Charging a fee implies handling payments, but you haven't selected a payments provider or described escrow/hold mechanics, refunds, chargeback handling, VAT/tax treatment or GDPR-compliant data handling. Implementing secure payment flows and escrow logic, and meeting PCI/GDPR/tax rules will require engineering and legal work that is frequently underestimated.
  -> Which payment/escrow provider and legal/tax approach will you use, and how will you implement fund holds, refunds/chargebacks and regulatory compliance from day one?

- **Chicken-and-egg launch sequencing: no concrete plan to secure supply before product build** [HIGH] (acquisition)
  You plan to launch at one university but provide no channel or commitment strategy to recruit the initial lenders or guarantee a baseline of listings. Building a product before locking supply (or a seeded inventory/partner) risks a dead marketplace at launch. The right sequence is validating supply and captive demand manually before building full platform features.
  -> How will you recruit and lock in an initial set of lenders and listings at the target university (exact numbers, channels and commitments) before—or as part of—your launch?

- **Operational workload and team capacity are undefined and likely underestimated** [MEDIUM] (assumptions)
  No team, roles or hiring plan are specified for operations tasks: customer support, inspections, dispute resolution, logistics coordination and partnership management. Those functions typically require multiple full-time people even for a single-campus pilot; lacking capacity will cause slow responses, poor dispute outcomes and churn.
  -> Who will run day-to-day operations (fulfillment, quality checks, disputes, customer support) for the pilot and what headcount/hours and budget have you allocated for months 0–6?

- **Product primitives (inventory model, calendars, deposits, condition grading) are unspecified — risk of rework** [MEDIUM] (assumptions)
  The platform will need a concrete data model for listing availability across academic terms, recurring rentals, condition grading, deposit amounts, late fees and pricing rules. Building generic or incorrect primitives will require expensive rearchitecture once edge cases appear (overlapping term rentals, lost books mid-term, partial returns).
  -> What exact listing and rental data model (availability rules, condition states, deposit and fee logic, return windows) will you implement first to support typical textbook term rentals?

### evidence_audit

Evidence base: Weak. The document is an unproven idea with only a stated 10% fee and single-university launch. The most important remaining issues are lack of measured demand/supply evidence and missing unit-economics and acquisition assumptions.

- **No measured evidence that students will rent (demand)** [CRITICAL] (demand_evidence)
  The plan assumes students want to rent rather than buy or borrow, but provides no survey, pilot or other measured evidence from the target university. This is load-bearing: a marketplace needs demonstrated demand before fees, growth or expansion are meaningful. Without even a small-sample willingness-to-rent metric the core hypothesis is untested.
  -> Provide measured demand evidence: a survey or pilot from the target university showing the percentage of students who would rent study materials (sample size, question wording, and raw response counts), or actual rental requests from a pilot.

- **Fee alone (10%) is insufficient — key unit economics missing** [HIGH] (key_numbers)
  Saying the platform will charge a 10% fee does not show viability because average transaction value, transaction frequency, take rate, and operating costs are not specified. Revenue per transaction is 0.10 × (average rent price) — with the average rent price unstated, ARPU and break-even transaction volume cannot be computed, so the financial feasibility is unknown.
  -> State the assumed or measured average rent price, expected transactions per active user per month, and a target monthly revenue (or runway) so you can show how many transactions/users are needed to hit that target.

- **No acquisition plan or CAC estimate to reach critical mass** [HIGH] (acquisition)
  Launching at one university requires an acquisition strategy and CAC estimate to create both supply and demand, but none is given. Without a CAC and channel conversion rates you cannot determine whether the 10% take can cover acquisition or how many leads are required to seed the marketplace.
  -> Provide the planned customer acquisition channels and measured or assumed CAC (with the experiment or basis for the assumption) and show the math linking CAC to required LTV or transaction volume to reach payback.

- **No evidence students will supply listings or accept rental logistics** [MEDIUM] (assumptions)
  A marketplace needs supply: students willing to list textbooks/equipment and handle handoff, deposits, damage risk and scheduling. The document contains no evidence that owners will participate or what share of students would list items, nor how logistics (meetups, shipping, deposits) will work in practice.
  -> Provide measured evidence (survey responses, signups, pre-committed listers, or a mini-pilot) showing the share of students willing to list items and the proposed logistics (dropoff/meetup/shipping and deposit/refund approach) tested at the target campus.

- **No account of current alternatives and why students would switch** [MEDIUM] (alternatives)
  The plan does not identify existing alternatives students use (buying used books, university bookshop, peer-to-peer borrowing, online marketplaces) or provide evidence why they would prefer a rental marketplace. Without this, differentiation and the willingness to pay the 10% fee are unsupported.
  -> List the main current alternatives students use for study materials at the target university and provide user research or pilot data showing the reasons students would choose your rental marketplace over those alternatives.


## Selected questions

- **demand_evidence**: How do you know people want this? (people you've talked to, data, your own experience)
  - why we're asking: pre_mortem / No evidence students will prefer peer-to-peer rentals over current options [critical]
  - why we're asking: adversarial_competitor / No demand evidence — unclear students will list or prefer P2P rentals [medium]
  - why we're asking: evidence_audit / No measured evidence that students will rent (demand) [critical]
- **acquisition**: How will your first customers find you?
  - why we're asking: unit_economics / Customer acquisition plan and CAC are not defined [high]
  - why we're asking: adversarial_competitor / Go-to-market and distribution are unspecified — easily dominated by bigger players [high]
  - why we're asking: execution_risk / Chicken-and-egg launch sequencing: no concrete plan to secure supply before product build [high]
  - why we're asking: evidence_audit / No acquisition plan or CAC estimate to reach critical mass [high]
- **key_numbers**: Which numbers is this plan relying on? Give each one's value and whether it is measured, an estimate, or unknown.
  - why we're asking: unit_economics / No average transaction value, frequency, or LTV (core revenue drivers missing) [high]
  - why we're asking: unit_economics / Per-transaction and per-user cost-to-serve are not quantified [medium]
  - why we're asking: unit_economics / No gross margin, payback period or break-even analysis [medium]
  - why we're asking: evidence_audit / Fee alone (10%) is insufficient — key unit economics missing [high]
- **pricing**: Who pays, and roughly how much?
  - why we're asking: pre_mortem / 10% platform fee is asserted without testing fee acceptance or who bears it [high]
  - why we're asking: unit_economics / Pricing mechanics and willingness-to-pay are unspecified [high]
  - why we're asking: adversarial_competitor / Pricing is vulnerable — 10% fee is easy to undercut or subsidize [medium]

## Answer given

**demand_evidence**: I haven't surveyed or interviewed any students yet; the idea comes from my own experience as a student.

Skipped: acquisition, key_numbers, pricing

## Refined critique

### pre_mortem

The plan rests almost entirely on untested behavioral and market assumptions: that students at a single UK campus will both list and rent study items from peers, that a 10% fee is acceptable, and that customers can be acquired without a defined channel. The most likely failure is a liquidity collapse at launch—insufficient listings or renters at the pilot university leading to zero transactions. Before building, the founder must validate demand, willingness to pay, and repeatable acquisition on the ground with cheap, early experiments.

- **Critical: Marketplace liquidity will not materialize at a single campus** [CRITICAL] (assumptions)
  The strategy assumes a two-sided marketplace can reach the required density from day one at one university, but there is no evidence of supply (students willing to list items) or demand (students willing to rent from peers). The killing-blow scenario is launch with few or no listings and few renters, producing no transactions and collapsing any network effects. At idea stage this is fatal because a marketplace cannot function without a plan or evidence for both sides before build.
  -> What exact minimum numbers of listings and active renters are required to make the pilot viable, and how will you prove you can recruit both sides before building the product?

- **High: No evidence students actually want peer-to-peer rentals** [HIGH] (demand_evidence)
  Founder relies solely on personal experience and has not interviewed or surveyed target students, so demand is assumed rather than demonstrated. Students' revealed preferences may be to buy used, borrow for free, rely on university services, or use digital resources — any of which would undercut the rental model. Without even basic qualitative evidence, the core value proposition is unproven.
  -> Do representative students at the pilot campus prefer renting study items from peers over their current behaviors, and why would they switch?

- **High: Acquisition channels are undefined; assumption of organic campus growth** [HIGH] (acquisition)
  The plan leaves unanswered how the first customers will find the marketplace, implicitly assuming campus virality or word-of-mouth will supply both sides. If organic adoption doesn't appear immediately, there is no fallback and the pilot will not reach necessary density. This dependency on an unspecified, fragile acquisition channel is a likely cause of failure.
  -> Specifically how will you acquire the first listings and renters at the pilot university (channels, expected conversion rates, and cost to test) before building the platform?

- **High: Pricing model (10% fee) and who pays it are untested** [HIGH] (pricing)
  A 10% fee is stated without evidence that owners or renters will accept it, or which side will bear the cost. Willingness to pay for peer-to-peer rental services may be low or asymmetric (owners vs renters), and incorrect assumptions here would break revenue and value dynamics. This untested pricing assumption could deter listings or rentals once the product is live.
  -> Who will pay the 10% fee (owner, renter, split), and what evidence shows that target users accept that fee at the pilot campus?

- **Medium: Current alternatives and revealed preferences are unknown** [MEDIUM] (alternatives)
  The founder hasn't identified what students currently do to obtain textbooks, calculators and equipment (buy new/used, borrow, use library/university services, or digital materials). Without mapping existing solutions and why they succeed, the offering may not address the real unmet need or could be a poor fit for behaviors that are hard to change. Misreading stated preference (would you rent?) vs revealed preference (what you actually do) is a likely misstep.
  -> What do students currently use today to obtain these items, and what behaviors must change for them to adopt peer rentals?

- **Medium: Unclear who the primary customer is (owner vs renter) and how value is delivered** [MEDIUM] (buyer)
  The document doesn't specify whether the product is designed to primarily solve a problem for owners (monetizing unused textbooks) or renters (cheaper access), nor how trust, pickup, and damage-risk will be handled. If the core value proposition isn't targeted to a real pain point for a clear buyer, onboarding and retention will suffer. This ambiguity obscures which tests to run and which metrics matter.
  -> Which side of the marketplace is the primary customer (owner or renter), what exact problem are you solving for them, and how will you validate that solution cheaply?

### evidence_audit

Evidence base: Weak. The founder provides only personal experience and no measured demand, pricing, acquisition, or numeric targets for the launch university. The single most important gap is lack of any measured demand or conversion data at the target university, which prevents credible revenue or growth projections. Several load‑bearing inputs (who pays, average price, CAC, behavioral assumptions) are also missing.

- **No validated demand at the launch university** [HIGH] (demand_evidence)
  The founder reports zero interviews or surveys and offers only personal experience as evidence. For a marketplace, even an idea-stage plan must show measurable student interest at the chosen university before building. Without counts (e.g., signups, survey responses or commitments) the central hypothesis—that students will supply and rent items peer‑to‑peer—is unsupported.
  -> Provide measured demand evidence from the target university: how many students were surveyed/interviewed, what percent said they would use a student-to-student rental marketplace, and how many signups/commitments (email/holds/pre‑rents) do you currently have?

- **Who pays and how much per transaction is unspecified** [HIGH] (pricing)
  The document states a 10% fee but does not say whether renters or lenders pay it, nor the expected average rental price. Revenue per transaction = 10% × average price. Even using a conservative labeled assumption (example: average rental price P = £10), revenue = £1 per transaction; to earn £1,000/month you'd need 1,000 transactions. Without the actual payer and average price the fee alone is meaningless.
  -> State who pays the 10% fee (renter or lender) and provide an evidence‑based estimate of the average rental price per transaction at your launch university (or measured willingness‑to‑pay data)?

- **No acquisition plan, CAC or early conversion targets** [HIGH] (acquisition)
  The founder skipped how first customers will find the platform. You cannot assess viability without a channel, expected conversion rates, or a CAC bound. For example, to reach 500 transacting users you need defined outreach and conversion (e.g., signups → listings → transactions). With no numbers, required marketing effort and viability are unknown.
  -> Provide a concrete acquisition plan for the first university with expected conversion funnel numbers (impressions → signups → listed items → first transaction) and an estimated CAC per transacting user based on an explicit channel or pilot.

- **No baseline numeric targets or revenue model provided** [MEDIUM] (key_numbers)
  The plan lacks load‑bearing key numbers: target transactions per month, first‑year revenue, average item price, and item availability. Revenue formula is Transactions × Avg Price × 10% (take rate). For example, with Avg Price = £15, each transaction yields £1.50; to reach £5,000/term you'd need ≈3,333 transactions. Without targets you can't judge whether the 10% fee and single‑university launch can reach sustainable scale.
  -> Publish baseline numeric targets for the first 12 months: target transactions per month, average rental price, expected listings available, and resulting monthly revenue (using Revenue = transactions × avg price × 10%).

- **Unclear who the buyer is and which side of the two‑sided market to prioritize** [MEDIUM] (buyer)
  The document does not state whether the primary customer is the renter or the lender (owner). That matters for pricing, acquisition prioritization and trust mechanisms. Two‑sided marketplaces must select which side to subsidize early; this plan gives no evidence or decision on that choice.
  -> Identify the primary paying customer (renter or lender) you will prioritize at launch and provide the rationale or evidence for that choice (e.g., survey data showing willingness to pay or evidence of supply willingness to list).

- **Key behavioral assumptions are unstated and untested** [LOW] (assumptions)
  The plan implicitly assumes students prefer peer rentals over existing options, trust peers to lend/buy back items, and will transact frequently enough. These are load‑bearing behavioral assumptions but are neither named nor tested. At idea stage these should be the first experiments.
  -> List the top 3 behavioral assumptions (e.g., preference for peer rental, trust in peer listings, frequency of rentals) and describe a single low‑cost experiment you will run to validate each one within 4 weeks.


## Refinement meta

- Lenses re-run: pre_mortem, evidence_audit
- Lenses not re-run: unit_economics, adversarial_competitor, execution_risk
- Gaps filled: ['demand_evidence']
- Gaps skipped: ['acquisition', 'key_numbers', 'pricing']

## Reuse check

Re-sending the same refinement token refused with 409: yes
