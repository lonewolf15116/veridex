# Evaluation backlog

Observations to test in the next scheduled evaluation round. They are not tuning tasks yet.
Each one needs a reproducible case before any prompt change.

## Open

### 1. Pre-mortem factuality (highest priority)
- Source: external review of the dental-scheduling B2B SaaS critique (paste-a-plan route, 2026-10-30).
- Seen: "Major PMS vendors refused standardized APIs…" and "In pilot deployments the model's uplift collapsed…".
  Neither event is in the founder's plan.
- Cause: the pre-mortem prompt sets the frame "It is 18 months from today. The strategy has failed." The model
  writes imagined failures in the past tense, which reads as if they happened.
- Also seen in Adversarial Competitor: "incumbents can reproduce it within weeks" stated as a timeline, not a threat.
- Test idea: count past-tense event claims that are not in the input across the holdout set. Candidate fix:
  require the scenario to be labelled ("Failure scenario: …") and ban the claim that pilots or integrations happened
  unless the document says so.

### 2. Severity calibration: missing vs contradicted vs false
- Same review: 5 criticals; the reviewer would downgrade 4 to high (missing COGS, unsupported 30% claim,
  replicable prediction, missing compliance plan) and treat data access as a conditional blocker.
- Related to the existing holdout result: severity over-call 5/10 (v3.1), 4/10 after checker round 1.
- Test idea: tag each critical as missing / contradicted / shown false and check that "missing" is never critical
  on its own. The idea-stage rule already does this; the paste-a-plan route does not.

### 3. Assumption provenance in calculations
- Same review: the $1,200 CAC used an assumed $5,000/month rep cost the plan never gave. It was presented as a
  contradiction, not as an illustration. "6.73×" was gross revenue / CAC, labelled like LTV:CAC.
- Related: the Rev 2 live run turned the founder's "800" into "$800" and called a per-day figure "per job".
- Test idea: every figure the model introduces must be marked as its own assumption, and the ratio must be named
  by its true numerator.

### Carried over
- Evidence Audit false alarms on Strong documents (holdout: 6/10 after checker round 1).
- Idea stage: 2 remaining "X not validated" criticals in the I1–I3 run.

## Review closed 2026-10-30 (suite runs 1 and 2, adjudicated with the external reviewer)
Revision 2 stays deployed. Fixed in between: the skipped-question bug (7d907ea, verified on T01/T04/T05).

Adjudicated examples (keep as fixed reference cases):
| Case | Text | Verdict |
| --- | --- | --- |
| T05 run 2, Pre-Mortem | "As a result, trials showed low conversion to subscriptions." | Invented event (failure) |
| T04 run 1, Pre-Mortem | "clinics and some insurers refused to share identifiable patient data" | Invented event (failure) |
| T01 runs 1–2, Evidence Audit | "Conservatively, at $5k fully loaded per rep per month … implied CAC = $1,200" | Unlabelled model assumption (failure) |
| T04 run 2, Evidence Audit | "For context: … signing 100 clinics is £178,800/year; whether that is reachable depends…" | Conditional calculation (acceptable) |
| T01 run 2 | "299 × 12 = $3,588" | Derived from founder input (acceptable) |
| T09 run 1, Adversarial / Execution | "$800/yr" for a price the founder gave without a currency | Invented currency (failure) |

## Next scheduled round: required outcomes
| Check | Required outcome |
| --- | --- |
| Pre-Mortem fabrication (first priority) | No asserted pilots, trials, refusals or conversations absent from the input |
| Model-supplied figures | Explicitly marked as assumptions; never treated as founder evidence inside a calculation |
| Conditional scenarios (e.g. £178,800) | Still permitted |
| Unspecified currency (T09) | Strict: no symbol attached to the founder's figure; alternatives only as labelled hypotheticals |
| Severity | Missing evidence distinguished from a confirmed blocker or contradiction (T06 must keep its criticals) |
| Revision 2 mechanics | No regression in gap tags, routing, single-use refinement |

Screening rules (regex for past-tense verbs, money not in input, currency symbols) only flag candidates. A human or
a checker must confirm each one against the input: hypotheticals like "if clinics refused…" are legitimate, and
fabrication can happen without the listed verbs.

## Round 3 closed 2026-10-30 (tone): accepted, stays deployed
Next round must not reopen tone, factuality, severity or refinement routing. Open items:
| Issue | Priority | Acceptance criterion |
| --- | --- | --- |
| Verdicts that only name missing data | Medium | A verdict must state the failure mechanism and its consequence; naming an unknown is not enough (e.g. not "no CAC data" but how acquisition spend could exceed the margin available to recover it). |
| Founder-supplied currency dropped ("price 5 vs cost 2") | Low | Keep the founder's own currency exactly as written; add none they did not write. |
| Long-term factuality | High | Keep the 0-invented-events check in every suite run. |
| Severity calibration | Medium | Keep critical+missing = 0 and the T06/T07 controls; watch basis mislabelling. |
| T07 empty refinement (once, round 2) | Low | Monitor; if it recurs, fix token redemption so a failed stream does not consume the free refinement. |
