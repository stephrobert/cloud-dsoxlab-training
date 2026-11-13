# A data service for the order platform

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
