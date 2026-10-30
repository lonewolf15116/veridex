"""
Critics module — the core of Veridex v1.

Five independent lenses critique a strategy document:
  - pre_mortem:              "It's 18 months later and this failed. Why?"
  - unit_economics:          "Does the math actually work?"
  - adversarial_competitor:  "You're a well-funded competitor. How do you kill this?"
  - execution_risk:          "What's most likely to go wrong in shipping?"
  - evidence_audit:          "Is the evidence itself real, or an artefact of how it was produced?"

Design rules:
  - One retry on validation failure with a corrective nudge. Fails loud after that.
  - Output is strict JSON validated by Pydantic.
  - Severity cap: at most 1 critical and 3 high per lens.
  - Each lens focuses ONLY on its angle — no cross-lens bleed.
  - Provider-agnostic wrapper: `run_critic_pass(lens, input_text, model="openai:gpt-5-mini")`.
"""

from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from app.llm.client import client


# ---------- Schemas ----------

Severity = Literal["low", "medium", "high", "critical"]
Lens = Literal["pre_mortem", "unit_economics", "adversarial_competitor", "execution_risk", "evidence_audit"]

# Idea builder (Revision 2): the founder-declared stage, and the fixed list of evidence gaps a flaw
# can point at. Gap tags are only requested when a stage is given; plain critiques never carry them.
Stage = Literal["idea", "building", "traction", "established"]
Basis = Literal["contradiction", "stated_fact", "missing"]
Gap = Literal[
    "buyer", "demand_evidence", "pricing", "acquisition",
    "key_numbers", "assumptions", "alternatives", "differentiation",
]
GAPS: tuple[str, ...] = (
    "buyer", "demand_evidence", "pricing", "acquisition",
    "key_numbers", "assumptions", "alternatives", "differentiation",
)


class Flaw(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    severity: Severity
    description: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1, description="The sharpest question the user should answer next.")
    gap: Gap | None = Field(default=None, description="Idea mode only: which missing input this flaw points at.")
    basis: Basis | None = Field(default=None, description="Stage mode only: what the flaw rests on.")


class CriticPassResult(BaseModel):
    lens: Lens
    summary: str = Field(..., min_length=1, description="2-4 sentence synthesis from this lens.")
    flaws: list[Flaw] = Field(..., min_length=1, max_length=7)


class CriticValidationError(Exception):
    """Raised when a critic pass returns output that fails schema validation after one retry."""

    def __init__(self, lens: str, raw: str, reason: str):
        self.lens = lens
        self.raw = raw
        self.reason = reason
        super().__init__(f"[{lens}] critic pass failed validation: {reason}")


# ---------- Lens prompts ----------

_SHARED_OUTPUT_CONTRACT = """You must respond with ONLY a single valid JSON object. No prose before or after.
The JSON object must have this exact shape:
{{
  "lens": "{lens_name}",
  "summary": "<2-4 sentences. The FIRST sentence is your verdict, stated plainly with no hedging, in this form: {verdict_form} Then the supporting synthesis.>",
  "flaws": [
    {{
      "title": "<short punchy title, <= 120 chars>",
      "severity": "low" | "medium" | "high" | "critical",
      "description": "<2-5 sentences explaining the flaw concretely>",
      "question": "<the single sharpest question the author must answer to resolve this flaw>"
    }}
    // 2 to 7 flaws total, ranked by severity (most severe first)
    // Severity cap: at most 1 "critical" flaw and at most 3 "high" flaws.
    // Everything else should be "medium" or "low".
  ]
}}

VOICE — you are a red team, not a consultant:
  - Be blunt and decisive. Name the one thing that kills the plan; do not list everything equally.
  - Banned phrases: "may want to consider", "it could be beneficial", "it is worth noting", "consider exploring", "it is important to". Write what will happen, not what to ponder.
  - Never write "unproven", "unvalidated" or "unclear" on its own: say what happens to the plan if that thing turns out false ("if <the stated price> is more than buyers will pay, acquisition never pays back" — using the document's own figures, never example ones).
  - Bluntness is about consequences, never about facts: you may say "if X is false, this dies", but you may not claim events, results or numbers the document does not contain.
Do not invent facts not supported by the document. If something is unstated, say so and treat the gap itself as a flaw."""

_RETRY_NUDGE = """

IMPORTANT: Your previous response was not valid JSON or did not match the required schema.
Respond with ONLY the raw JSON object. No markdown, no code fences, no explanation. Just the JSON."""

# Lens-specific focus constraints prevent cross-lens bleed
_LENS_FOCUS: dict[str, str] = {
    "pre_mortem":             "Focus ONLY on assumption failures, wrong market signals, and killing-blow scenarios over an 18-month horizon. Do NOT raise unit economics, competitive threats, or shipping/execution issues — those belong to other lenses.",
    "unit_economics":         "Focus ONLY on cost structure, revenue mechanics, margins, CAC, payback period, and whether the numbers work. Do NOT raise assumption failures, competitive threats, or shipping/execution issues — those belong to other lenses.",
    "adversarial_competitor": "Focus ONLY on how a well-funded competitor would neutralize or kill this product. Do NOT raise internal assumption failures, unit economics gaps, or execution/shipping risks — those belong to other lenses.",
    "execution_risk":         "Focus ONLY on what will go wrong in the process of building and shipping this product — team, technical risk, sequencing, and distribution gaps. Do NOT raise pre-mortem scenarios, unit economics, or competitive threats — those belong to other lenses.",
    "evidence_audit":         "Focus ONLY on whether the claims and numbers in the document are measured, sourced and internally consistent. Do NOT judge team size, staffing or hiring, pricing levels, margins or shipping costs, competition, or the choice of go-to-market channels — those belong to other lenses. You may use team or spend figures as inputs to arithmetic (e.g. to derive an implied CAC) but must not critique them in their own right.",
}

# First sentence of every lens summary: the red-team verdict.
_VERDICT_FORM: dict[str, str] = {
    "pre_mortem":             "'Most likely killer: <the one thing> — because <reason grounded in the document>. Prove otherwise by: <one concrete test>.'",
    "unit_economics":         "'Where the math breaks: <the number or mechanism> — because <reason>. Prove otherwise by: <one concrete test or figure to supply>.'",
    "adversarial_competitor": "'How I would kill this: <the one move> — because <reason>. Survive it by: <one concrete defence>.'",
    "execution_risk":         "'What breaks first: <the one thing> — because <reason>. Prevent it by: <one concrete step>.'",
    "evidence_audit":         "'Evidence base: <Strong|Mixed|Weak>. Weakest number: <the claim> — because <reason>. Prove it by: <one concrete check>.'",
}

_LENS_PROMPTS: dict[str, str] = {
    "pre_mortem": """You are performing a PRE-MORTEM on the strategy document below.

It is 18 months from today. The strategy has failed. Your job is to enumerate, specifically and honestly, the most likely reasons it would fail. Focus on:
  - Assumptions most likely to prove wrong
  - The killing-blow scenario (what single thing most likely ended it)
  - Dependencies that didn't materialize
  - Misread market / user signals

Be concrete. 'Users might not want it' is weak. 'Failure scenario: users say they want X, but what they would pay for is Y, because stated preference is not revealed preference' is strong.

FACTUALITY — the failure is imagined; the document's facts are not:
  - Write every failure as a scenario, not as history: "Failure scenario: …", "the likeliest way this fails is …", "if X, then …". Never state that something already happened.
  - Never claim pilots, trials, launches, customer conversations, sales results, refusals by partners/vendors/regulators, or measured outcomes unless the document itself reports them. "Trials showed low conversion", "clinics told the team…", "vendors refused…" are forbidden unless the document says so.
  - You may reason about what is likely ("independent clinics often lack API access"), but phrase it as a risk to check, not as an event.

{focus_constraint}
""",

    "unit_economics": """You are the UNIT ECONOMICS skeptic reviewing the strategy document below.

Your only job: does the math work? Focus on:
  - Cost to serve one user (compute, storage, support, payment processing)
  - Revenue per user (actual, not hoped-for) and how willingness-to-pay was determined
  - CAC and the channels implied by the strategy (are those channels realistic at the price point?)
  - Gross margin at scale vs. today
  - Payback period and what breaks it
  - Any hidden cost (moderation, compliance, refunds, chargebacks, fraud)

If numbers aren't in the doc, flag that as the flaw — don't invent numbers. Treat vague claims like 'low cost' or 'viral growth' as unearned until evidence is presented.

{focus_constraint}
""",

    "adversarial_competitor": """You are a WELL-FUNDED COMPETITOR reviewing the strategy document below. You have more capital, more distribution, and a decent engineering team.

Your job: how do you kill this product? Focus on:
  - The cheapest move you can make to neutralize their differentiation
  - Which incumbent feature, if shipped, makes this redundant
  - Distribution advantages you can weaponize (existing users, SEO, app store, channel partners)
  - Pricing moves you could make that they cannot match
  - Brand / trust advantages you can exploit

Be ruthless but realistic. Don't write fanfic about infinite budgets — write the one-page plan a rational PM at a competitor would actually execute.

{focus_constraint}
""",

    "execution_risk": """You are the EXECUTION RISK critic reviewing the strategy document below.

Assume the strategy is directionally correct. Your job is to find what will most likely go wrong IN SHIPPING it. Focus on:
  - Team size vs. scope (is this 6 months of work being planned as 6 weeks?)
  - Technical risk (unproven stack, unclear data model, integration hell)
  - Regulatory / compliance blockers that aren't addressed
  - Sequencing mistakes (building X before Y when Y is the real blocker)
  - Distribution plan gaps (product is built, then what?)
  - Founder / operator constraints implied by the doc

Every flaw should name a concrete failure mode, not a generic category.

{focus_constraint}
""",

    "evidence_audit": """You are the EVIDENCE AUDITOR reviewing the strategy document below.

Every other reviewer takes the document's numbers as given and critiques what is built on them. You check whether the numbers themselves hold up: are they measured, sourced, and consistent with each other? A plan built on evidence that is wrong or unsupported fails regardless of how good the rest of it is.

Work through these steps in order.

STEP 1 — INVENTORY AND CREDIT. List the claims the strategy depends on and label each one:
  - MEASURED: something the author has already observed (current revenue/ARR, existing customers, a pilot, a survey, a backtest, an experiment). A current fact the author states about their own business ("$4M ARR, profitable", "40 existing customers") counts as MEASURED: take it as given and do not flag it for lacking a P&L or documentation.
  - FORECAST: a projection of the future (growth targets, revenue targets, delivery or build timelines).
  - ASSUMPTION: an input asserted without a stated source (CAC, conversion rate, churn, lift %, market size, cost figures).
Note what is genuinely evidenced. Your summary MUST open by saying what is already proven (if anything) and rating the overall evidence base:
  - STRONG: the plan extends an existing business with real revenue, customers or profitability that are directly relevant to the new claim (e.g. an established, profitable company whose first target is its own existing customers). Such a plan is STRONG even if the expansion targets themselves are unproven; that is what the flaws are for.
  - MIXED: some relevant measured evidence, but the central claim extrapolates well beyond it (e.g. one site projected onto twenty).
  - WEAK: pre-launch or pre-revenue; the central claims rest on assumptions.

STEP 2 — DO THE ARITHMETIC YOURSELF. Do not ask the author to "show the math" when you can compute it. Combine the document's own numbers to derive every implied figure, for example:
  - growth: required starting base = target / (1 + monthly rate)^months;
  - revenue per customer = revenue target / number of customers it must come from;
  - implied CAC = acquisition spend over the period / customers acquired. If the plan names a sales team and a customer target but no spend, bound the spend with a conservative cost per person that you label as your own assumption in the same sentence (e.g. "Assuming — not from the document — $5k/month fully loaded per rep: 2 reps × 6 months = $60k; $60k ÷ 50 = $1,200") and compare it with any stated CAC. This arithmetic is required even though judging team size is out of scope;
  - volume needed = supply units × required activity rate;
  - totals = units × per-unit value × take rate.
Write the calculation in the flaw description with the numbers (e.g. "1.15^11 ≈ 4.65, so 10,000 at month 12 needs ≈ 2,150 at month 1"). Flag any contradiction between an implied figure and a stated one. Only divide a figure by a count that refers to the same population: do not divide a company-wide total (e.g. total ARR) by the size of a subset (e.g. "40 customers who have European subsidiaries") to get a per-customer average. Only call something a "contradiction" when two stated or derived figures cannot both be true; if the document is merely ambiguous (e.g. it is unclear whether a group of customers is the whole base or a subset), say it is ambiguous and do not rate it above medium. If a needed input is missing, you may bound it with a conservative assumption, labelled in the same sentence as "assuming (not from the document)"; never present an assumed figure as the author's. A contradiction that only appears because of a figure you assumed is at most HIGH, and must say that it depends on your assumption.

STEP 3 — AUDIT EACH CLAIM BY ITS TYPE.
  - MEASURED results: how were they produced? Sample size, a single site or customer (n=1), survivorship, whether the conditions that produced the result will hold where it is being applied (e.g. a result achieved with the founders' full attention being projected onto partners or licensees).
  - FORECASTS: check internal consistency against the plan's own inputs and your Step 2 arithmetic, and whether they extrapolate from a measured base that actually transfers. A delivery or build timeline the plan depends on (e.g. "regulatory compliance in 6 months") is a forecast too: flag it if nothing evidences it, as an evidence gap, not as a staffing critique. Do NOT ask for p-values, confidence intervals or statistical tests on a forecast.
  - ASSUMPTIONS: is the figure sourced? Is it load-bearing (would a plausible change break the plan)? Is it something that cannot have been observed yet (e.g. an "average customer lifetime" before there are customers)? Unsourced, load-bearing assumptions are flaws.

STEP 4 — BACKTEST AND EXPERIMENT CHECKS (GATED). Apply this step ONLY IF the document reports a measured result computed from historical data (a backtest, a model evaluation, an A/B test) or says several variants/configurations were tried. Otherwise skip it entirely, and do NOT use the words leakage, look-ahead, walk-forward, out-of-sample, train/test, parameter sweep or multiple testing anywhere in your output.
When it applies, check:
  - LOOK-AHEAD / LEAKAGE: for every input, WHEN is it actually available versus WHEN it is used? Bar timestamps (open vs close), interval data stamped at the start of the interval, revised data, features or labels computed with future information, overlapping train/test periods. Name the specific inputs at risk.
  - SELECTION BIAS: how many variants were tried before reporting this one, and was any correction applied?
  - RED FLAGS: test results that BEAT training; implausibly good results; one period or asset carrying the result; losing periods next to a strong headline; results that would vanish with a small delay or realistic costs.
  - Reason about which explanation fits: selection bias inflates IN-SAMPLE results and makes out-of-sample WORSE, so it cannot explain test beating training. When test beats training and any input has an ambiguous availability time, that leakage flaw is the CRITICAL one and outranks selection bias.

SEVERITY — calibrate to the evidence, not to a template:
  - CRITICAL only when the central claim the strategy rests on is likely wrong: a plausible leak or bug in a core measured result, or an arithmetic contradiction or unsupported number that breaks the plan by itself. Zero critical flaws is a valid answer.
  - HIGH: a load-bearing number that is unsupported or internally inconsistent.
  - MEDIUM/LOW: secondary gaps and missing controls.
  - Scale to the evidence base you assigned in Step 1:
      STRONG → no CRITICAL unless you found a genuine arithmetic contradiction; at most 1 HIGH; 2–4 flaws in total.
      MIXED  → at most 1 CRITICAL; 3–5 flaws.
      WEAK   → full range allowed.
    Do not pad the list to look thorough.
  - Rank by how much the claim matters to the plan, not by how easy it is to criticise. If the riskiest forecast in the plan is a build or delivery timeline, do not rate it below lesser gaps.

OUT OF SCOPE for this lens (other lenses cover them — do not raise them even as evidence gaps): the size or composition of the team, sales capacity or quotas, budget breakdowns, per-unit costs and margins, pricing levels, partner or sales pipeline and commitments, competition, and choice of channels.

Each flaw's question must be a concrete check the author can run or a specific number they must supply, not a general request for "more data".

{focus_constraint}
""",
}


_STAGE_GUIDANCE: dict[str, str] = {
    "idea": "an idea that has not been built or tested",
    "building": "a product being built, not yet launched",
    "traction": "a launched product with some users or revenue",
    "established": "an established business",
}

_EARLY_STAGE_RULES = """IDEA-STAGE MODE. The founder declared the stage as: {stage_words}. The document may be only a few sentences plus the founder's own answers.
  - Missing evidence is expected at this stage. For an untested hypothesis, say what to test first and the cheapest way to test it, rather than treating the gap as proof the idea fails.
  - Keep "critical" for what is genuinely fatal on the founder's own words: internal contradictions, claims that are already false, or a plan that cannot work as described (e.g. a legal or practical blocker). Do not lower a genuine critical flaw because the idea is early.
  - A flaw whose substance is only that something is not stated yet (no price given, no numbers, no acquisition plan) is never "critical" at this stage: rate it "high" at most and say what to find out first.
  - Do NOT invent specifics (prices, costs, market sizes, conversion rates, competitor names) to make feedback look detailed. Work only with what the founder wrote; where something is unknown, say it is unknown.
  - Rank flaws by how consequential the unknown or problem is for this idea succeeding.
  - Any figure you introduce that the founder did not give (a salary, a cost, a conversion rate, an example price) must be labelled as your assumption in the same sentence ("assuming …", "for example …"). Arithmetic on the founder's own numbers (e.g. monthly price × 12) needs no label.
  - Never attach a currency or unit the founder did not write. If the founder gave a number without a currency, write the bare number (e.g. "800 per year") and, if it matters, ask which currency."""

_LATE_STAGE_RULES = """STAGE NOTE. The founder declared the stage as: {stage_words}. Credit what is already measured, judge how far the plan extrapolates beyond it, and keep criticism proportionate to the evidence. Do not invent specifics the founder did not give. Any figure you introduce that the founder did not give (a salary, a cost, a conversion rate, an example price) must be labelled as your assumption in the same sentence ("assuming …", "for example …"). Arithmetic on the founder's own numbers (e.g. monthly price × 12) needs no label. Never attach a currency or unit the founder did not write. If the founder gave a number without a currency, write the bare number (e.g. "800 per year") and, if it matters, ask which currency."""

_GAP_CONTRACT = """
Each flaw object must ALSO include a "gap" field naming the missing input it points at, chosen from exactly this list:
  "buyer"            - who has the problem / who the customer is is unclear
  "demand_evidence"  - no evidence that people want or need this
  "pricing"          - who pays and how much is unclear or unsupported
  "acquisition"      - how customers will be reached is unclear or unsupported
  "key_numbers"      - a load-bearing number (cost, conversion, market size, revenue) is missing, unsourced or inconsistent
  "assumptions"      - an unstated condition that must be true for the plan to work
  "alternatives"     - what customers use today / the competition is unclear
  "differentiation"  - why customers would choose this over the alternatives is unclear
Pick the single closest match. Use null only if the flaw genuinely points at none of these.

Each flaw object must ALSO include a "basis" field saying what the flaw rests on:
  "contradiction" - two things the founder wrote cannot both be true (e.g. 20 videos × £2 cost = £40 against a £5 price)
  "stated_fact"   - a problem that follows directly from something the founder explicitly wrote (e.g. "no sales staff" with "15 enterprise contracts in 3 months")
  "missing"       - the document does not state or evidence something (no compliance plan, no demand evidence, price not validated, no data-access plan, no cost figures)
A flaw whose basis is "missing" cannot be "critical": rate it "high" at most, and say what to find out first."""


def _build_prompt(lens: str, input_text: str, retry: bool = False, stage: str | None = None) -> str:
    if lens not in _LENS_PROMPTS:
        raise ValueError(f"Unknown lens: {lens}")
    lens_prompt = _LENS_PROMPTS[lens].format(focus_constraint=_LENS_FOCUS[lens])
    output_contract = _SHARED_OUTPUT_CONTRACT.format(lens_name=lens, verdict_form=_VERDICT_FORM[lens])
    if stage is not None:
        if stage not in _STAGE_GUIDANCE:
            raise ValueError(f"Unknown stage: {stage}")
        rules = _EARLY_STAGE_RULES if stage in ("idea", "building") else _LATE_STAGE_RULES
        lens_prompt = f"{lens_prompt}\n{rules.format(stage_words=_STAGE_GUIDANCE[stage])}\n"
        output_contract = output_contract + _GAP_CONTRACT
    retry_nudge = _RETRY_NUDGE if retry else ""
    return f"""{lens_prompt}

{output_contract}{retry_nudge}

---- STRATEGY DOCUMENT ----
{input_text.strip()}
---- END DOCUMENT ----"""


# ---------- Runner ----------

def _parse_provider_model(model: str) -> tuple[str, str]:
    if ":" not in model:
        raise ValueError(f"Model must be in 'provider:model_id' form, got: {model}")
    provider, model_id = model.split(":", 1)
    return provider, model_id


def _call_openai(model_id: str, prompt: str) -> str:
    """Call OpenAI and return the raw text output. Raise on any API failure."""
    resp = client.responses.create(
        model=model_id,
        input=prompt,
    )
    text = getattr(resp, "output_text", None)
    if not text:
        raise RuntimeError("OpenAI returned no text output")
    return text


def _parse_and_validate(lens: str, raw: str) -> CriticPassResult:
    """Parse raw text as JSON and validate against CriticPassResult schema."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CriticValidationError(lens=lens, raw=raw, reason=f"not valid JSON: {e}") from e

    try:
        result = CriticPassResult(**payload)
    except ValidationError as e:
        raise CriticValidationError(lens=lens, raw=raw, reason=str(e)) from e

    if result.lens != lens:
        raise CriticValidationError(
            lens=lens,
            raw=raw,
            reason=f"returned lens={result.lens!r} but pass was for {lens!r}",
        )

    return result


def _draft_pass(
    lens: str,
    input_text: str,
    model: str = "openai:gpt-5-mini",
    stage: str | None = None,
) -> CriticPassResult:
    """
    Run a single critic pass and return a validated CriticPassResult.

    On validation failure, retries once with a corrective nudge.
    Raises CriticValidationError only if the retry also fails.

    Other failures:
      - ValueError on unknown lens or malformed model string
      - RuntimeError on empty provider response
    """
    if lens not in _LENS_PROMPTS:
        raise ValueError(f"Unknown lens: {lens}")
    if not input_text or not input_text.strip():
        raise ValueError("input_text must be non-empty")

    provider, model_id = _parse_provider_model(model)

    if provider != "openai":
        raise ValueError(f"Unsupported provider: {provider}")

    # First attempt
    raw = _call_openai(model_id, _build_prompt(lens, input_text, retry=False, stage=stage))
    try:
        return _parse_and_validate(lens, raw)
    except CriticValidationError:
        pass  # Fall through to retry

    # Single retry with corrective nudge
    raw = _call_openai(model_id, _build_prompt(lens, input_text, retry=True, stage=stage))
    return _parse_and_validate(lens, raw)  # Raises CriticValidationError if still broken


# Lenses whose draft goes through the checker pass (see checker.py). Start with the one
# we can measure on evals/holdout; extend once it is shown to help.
CHECKED_LENSES = {"evidence_audit"}


def cap_missing_criticals(result: CriticPassResult) -> CriticPassResult:
    """Stage mode: a flaw that rests on missing information cannot be critical. Cap it at high and re-sort."""
    order = ["critical", "high", "medium", "low"]
    flaws = [
        f.model_copy(update={"severity": "high"}) if f.severity == "critical" and f.basis == "missing" else f
        for f in result.flaws
    ]
    flaws.sort(key=lambda f: order.index(f.severity))  # stable
    return result.model_copy(update={"flaws": flaws})


def run_critic_pass(
    lens: str,
    input_text: str,
    model: str = "openai:gpt-5-mini",
    stage: str | None = None,
) -> CriticPassResult:
    """Draft a critique for one lens, then (for CHECKED_LENSES) run the checker pass over it.

    stage=None is the plain paste-a-plan critique, unchanged. A stage switches on idea-stage
    calibration and gap tags (idea builder, Revision 2).
    """
    result = _draft_pass(lens, input_text, model, stage)
    if lens in CHECKED_LENSES:
        from app.services.checker import check_pass  # local import avoids a circular import

        _, model_id = _parse_provider_model(model)
        result = check_pass(lens, _LENS_FOCUS[lens], input_text, result, lambda prompt: _call_openai(model_id, prompt))
    if stage is not None:
        result = cap_missing_criticals(result)
    return result


__all__ = [
    "Flaw",
    "Basis",
    "cap_missing_criticals",
    "CriticPassResult",
    "CriticValidationError",
    "Gap",
    "GAPS",
    "Lens",
    "Severity",
    "Stage",
    "run_critic_pass",
]
