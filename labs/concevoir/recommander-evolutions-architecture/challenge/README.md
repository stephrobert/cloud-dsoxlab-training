# Challenge: recommend and schedule architecture improvements

Use the review evidence in `review.json` to create `plan.json`. Include a
recommendation for each finding, with its risk score, effort, expected effect,
measurable verification criterion, monthly cost, residual risk and dependencies.

Rank the recommendations by risk score, highest first. Classify an action as `quick_win` only when it takes at most two person-days,
has no dependency and is reversible; classify the others as `structural`.

Schedule all work in sprints. A sprint may contain no more than the team's
capacity, and a recommendation must not start before its dependencies finish.
Name an owner who accepts each residual risk.

Use this JSON shape:

```json
{
  "priority_order": ["database_private", "audit_retention", "regional_recovery"],
  "recommendations": [
    {
      "id": "database_private",
      "risk_score": 20,
      "action": "A verifiable change, not a product name.",
      "expected_effect": "The effect on the finding.",
      "verification_criterion": "An observable pass condition.",
      "effort_days": 1.5,
      "monthly_cost_eur": 0,
      "residual_risk": "What remains true after the action.",
      "dependencies": [],
      "kind": "structural",
      "risk_acceptance": {"owner": "Named role", "rationale": "Why this residual risk is accepted."}
    }
  ],
  "sprints": [
    {"name": "sprint-alpha", "items": ["database_private", "audit_retention"]},
    {"name": "sprint-beta", "items": ["regional_recovery"]}
  ]
}
```

Include all three recommendations and their sprint assignments. The score
measures resulting contents, not the commands used to create them.
