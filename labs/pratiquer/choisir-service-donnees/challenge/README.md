# A data service for the order platform

## The situation

The order platform needs a PostgreSQL-compatible relational database. Orders
must retain transactional consistency; the application requires the `pgcrypto`
extension and may reach the database only over a private endpoint.

The service must meet the recovery objectives in the brief. The product team
has no database administrator and can spend at most eight hours per month on
database operations. Choose among the supplied service options and document
the engine, operating model, private connection, replication, failover and
backup-restore verification plan.

The included service catalogue is synthetic exercise data. Its availability
and prices do not describe a real provider. This challenge asks for an
evidence-based design decision, not deployment or a claim that recovery has
been exercised.

Skill targeted: `cloud.data.choose`

## Choose a data service

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
