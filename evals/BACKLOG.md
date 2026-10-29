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

## Not yet checked
- Refinement journey on the dental SaaS case (which questions, which lenses re-ran, faithfulness to answers).
  The reviewed output came from the paste-a-plan route, so it says nothing about Rev 2 idea-stage calibration.
