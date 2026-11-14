# Scenario: an architecture review with no actionable plan

An architecture review has identified three issues in the customer platform:
a public database endpoint, incomplete audit-log retention, and no tested
regional recovery path. The engineering team has a fixed capacity of two
person-days per sprint, and the recovery work depends on the audit trail.

A scenario says **where we are and what is wrong**, not the steps to take:
finding those is the learner's work.

The findings, evidence, risk scales and effort estimates are in `review.json`.
The review document lists observations but gives the team no verifiable
recommendations, priority order or feasible delivery plan.

Skill targeted: `cloud.architecture.recommend`
