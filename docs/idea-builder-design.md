# Idea Builder — design (v1)

## Goal
Turn a rough idea into a structured brief that the five lenses can critique fairly, **without the AI inventing anything**. The founder supplies every fact and number. Veridex only asks questions and arranges the answers.

## Flow
1. **Entry.** Above the critique box, a toggle: **"I have a plan"** (today's box) / **"I only have an idea"** (the builder).
2. **Idea.** One box: "Describe your idea in a few sentences."
3. **Stage.** Pick one: *Idea* · *Building (pre-launch)* · *Early traction (some users or revenue)* · *Established business*.
4. **Guided questions.** All optional, and each has a **"Don't know yet"** button:
   1. Who has this problem? Be specific.
   2. What is the problem, and how do they deal with it today?
   3. How do you know? (people you've talked to, data, your own experience)
   4. Your solution, in one or two sentences.
   5. Who pays, and roughly how much?
   6. How will your first customers find you?
   7. **Key numbers.** Rows of *label · value · tag*. The tag is one of **Measured** / **Estimate** / **Don't know**, and the founder chooses it. Suggested labels (none pre-filled): price, customers or users today, revenue today, cost to acquire a customer, conversion rate, market size.
   8. What has to be true for this to work?
   9. What do people use instead today?
5. **Follow-ups (optional, one round).** One cheap model call reads the answers and asks **at most 3** follow-up questions, only where an answer is vague (e.g. "lots of interest" → "How many people, and did any pay or pre-order?"). It never suggests values. The founder answers or skips.
6. **Brief.** **Code** assembles the brief from a fixed template, not the AI. Everything in it is the founder's own text. The founder sees an editable preview, then clicks **Run critique**.

## Brief format (what the lenses receive)
```
# <one-line idea>
Stage: Idea | Building | Early traction | Established

## Customer and problem      (answers 1–2)
## Evidence so far           (answer 3, follow-up answers)
## Solution                  (4)
## Business model            (5)
## Go-to-market              (6)
## Key numbers
| Number | Value | Evidence |      Evidence = Measured / Estimate / Don't know
## Must be true              (8)
## Alternatives              (9)
## Unknowns                  (every "Don't know yet" answer, listed)
```

## How the lenses use it
- The critique request carries an optional **`stage`** field. The backend adds one short calibration paragraph to every lens prompt:
  - *Idea / Building:* missing evidence is expected. Focus on the most important unknowns and the cheapest way to test each one. Keep **critical** for internal contradictions or claims that are already known to be false.
  - *Early traction:* judge the extrapolation from what is measured.
  - *Established:* credit what is proven and be proportionate.
- **Evidence tags** are visible in the brief, so Evidence Audit doesn't have to guess what's measured.
- The checker's strength band takes the declared stage into account (Idea/Building → Weak unless the brief has measured numbers).

## Guarantees against invention
- The brief is built by a template from the founder's input. No model writes brief content.
- The only model call in the builder writes *questions*. Its prompt forbids suggesting numbers or answers, and the backend rejects any follow-up containing a digit.

## Backend
- `POST /api/v1/builder/followups` with `{idea, stage, answers}` → `{questions: [≤3]}`. Uses gpt-5-mini, has its own free limit (10/day per visitor), and costs about $0.001 per call.
- `POST /api/v1/critique/stream` accepts optional `stage` (`idea | building | traction | established`).

## Evaluation (bounded: one round, at most one adjustment)
Three one-line ideas, each run through the builder and then all five lenses, with and without `stage`.

Pass if:
- No follow-up question contains a number or a suggested answer.
- With `stage=idea`, Evidence Audit gives ≤ 1 critical and frames most flaws as "what to test next".
- The other lenses still give specific critiques, not generic ones.

## Out of scope for v1
Saving drafts on the server, accounts, AI-written prose, file or deck upload, voice input.

## Effort
About 0.5 day for the backend, 1–1.5 days for the frontend and 0.5 day for evaluation.
