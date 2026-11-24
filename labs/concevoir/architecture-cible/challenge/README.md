# A cloud target for the customer portal

## The situation

The team must move its customer portal to cloud infrastructure. The existing
application is packaged as an OCI image. The service must keep personal data
in the EU, serve across three availability zones, remain below a monthly
budget, and fit the small team's operations capacity.

A scenario says **where we are and what is wrong**, not the steps to take:
finding those is the learner's work.

## Mission

`brief.json` contains the workload requirements and measured facts for two
complete architecture options. The proposal currently lists both options but
does not show how they compare or which trade-offs the team accepts.

Skill targeted: `cloud.architecture.decide`

## Decide on the target architecture

Read `brief.json` and write `decision.json` in the working directory (`challenge/work/`). Compare
both complete options on the six axes provided, select an option that meets
every hard requirement, and record the decision in ADR form.

Use this shape:

```json
{
  "comparison": {
    "virtual_machines": {
      "monthly_cost_eur": 1250,
      "operations_days_per_month": 3,
      "data_residency": "eu",
      "availability_zones": 3,
      "portability": "...",
      "performance": "..."
    },
    "managed_containers": {}
  },
  "adr": {
    "title": "Target architecture for the customer portal",
    "context": "Summarize the workload and hard requirements.",
    "options_considered": ["virtual_machines", "managed_containers"],
    "criteria": ["monthly_cost_eur", "operations_days_per_month", "data_residency", "availability_zones", "portability", "performance"],
    "decision": "<the option you retain>",
    "rationale": "Explain the decision against the requirements.",
    "consequences": ["Record an operational or technical consequence."],
    "accepted_risks": ["Name a residual risk and its mitigation."],
    "review_condition": "State what evidence would make the team revisit the decision."
  }
}
```

The comparison object must contain both options and all six axes. The order of
JSON keys does not matter.

Run `dsoxlab check concevoir-architecture-cible` to see the result.
