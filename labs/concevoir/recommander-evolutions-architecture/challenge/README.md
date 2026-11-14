# Challenge: recommend and schedule architecture improvements

Use the review evidence in `review.json` to create `plan.json` in `challenge/work/`. Include a
recommendation for each finding, with its risk score, effort, expected effect,
measurable verification criterion, monthly cost, residual risk and dependencies.

Rank the recommendations by risk score, highest first. Classify an action as
`quick_win` only when it takes at most the quick-win effort of the scales, has
no dependency and is reversible; classify the others as `structural`.

Schedule all work in sprints. A sprint may contain no more than the team's
capacity, and a recommendation must not start before its dependencies finish.
Name an owner who accepts each residual risk.

Use this JSON shape (the values in angle brackets are yours to derive from
`review.json`):

```json
{
  "priority_order": ["<finding id>", "…"],
  "recommendations": [
    {
      "id": "<finding id>",
      "risk_score": <number>,
      "action": "<a verifiable change, not a product name>",
      "expected_effect": "<the effect on the finding>",
      "verification_criterion": "<an observable pass condition>",
      "effort_days": <number>,
      "monthly_cost_eur": <number>,
      "residual_risk": "<what remains true after the action>",
      "dependencies": ["<finding id>"],
      "kind": "<quick_win | structural>",
      "risk_acceptance": {"owner": "<named role>", "rationale": "<why this residual risk is accepted>"}
    }
  ],
  "sprints": [
    {"name": "<sprint name>", "items": ["<finding id>"]}
  ]
}
```

Include every recommendation and its sprint assignment. The score measures
resulting contents, not the commands used to create them.

Run `dsoxlab check concevoir-recommander-evolutions-architecture` to see the result.
