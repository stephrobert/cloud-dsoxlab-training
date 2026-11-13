# Challenge: choose a data service

Read `data-service-brief.json` and create `data-service-decision.json` in the
working directory (`challenge/work/`). Compare every listed option with the workload, team,
network, recovery and budget constraints.

Record the selected service, engine and operating model; the private endpoint
decision; the replication and failover plan; RPO/RTO targets; point-in-time
recovery; and how the team will verify a restore. Explain the decision and
give each rejected option its reason.

Use only the supplied synthetic catalogue. The artifact is a design decision,
not a deployment or proof of an actual failover.

Use this JSON shape (the values in angle brackets are yours to derive from the brief):

```json
{
  "service_id": "<an id of service_catalogue>",
  "engine": "<…>",
  "major_version": <…>,
  "operating_model": "<…>",
  "private_endpoint": <true | false>,
  "internet_exposure": <true | false>,
  "replication": "<…>",
  "failure_domains": <…>,
  "rpo_minutes": <…>,
  "rto_minutes": <…>,
  "point_in_time_recovery": <true | false>,
  "restore_test_owner": "<…>",
  "restore_verification": "<how a restore is checked>",
  "rationale": "<why this service>",
  "comparison": {"<service id>": "<its fit or why it is rejected>"},
  "rejected_options": [{"service_id": "<…>", "reason": "<…>"}]
}
```

Run `dsoxlab check choisir-service-donnees` to see the result.
