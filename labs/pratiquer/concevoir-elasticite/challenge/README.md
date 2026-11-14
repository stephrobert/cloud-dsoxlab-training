# Challenge: design an elastic application tier

Read `workload.json` and create `elasticity-plan.json` in the working
directory (`challenge/work/`). Use only the supplied measurements and constraints.

Record the session, upload and order-state locations; how retries avoid
duplicate orders; liveness and readiness checks; the minimum and maximum
replica counts; per-instance capacity; peak demand remaining after one
instance is lost; and the resulting capacity margin.

Define scale-out and scale-in separately. Include their metrics, thresholds,
observation windows, cooldowns and actions. Scale-in must drain connections
before removal and must never go below the required replica floor. State how
you verify the design by adding an instance and by removing one, without
changing application code.

Use this JSON shape (the values in angle brackets are yours to choose or
compute):

```json
{
  "state": {
    "sessions": "<instance_local_memory | sticky_load_balancer | shared_managed_session_store>",
    "uploads": "<instance_local_disk | shared_block_volume | object_storage>",
    "orders": "<where orders live>",
    "order_retry_protection": "<none | client_side_dedup | idempotency_key>"
  },
  "scale_out_requires_code_change": <true | false>,
  "health_checks": {"liveness": "<…>", "readiness": "<…>"},
  "replicas": {"minimum": <…>, "maximum": <…>},
  "safe_requests_per_second_per_instance": <…>,
  "peak_requests_per_second_after_one_loss": <…>,
  "capacity_after_one_loss_requests_per_second": <…>,
  "capacity_margin_after_one_loss_requests_per_second": <…>,
  "scale_out": {"metric": "per_instance_utilization_percent", "threshold_percent": <…>,
                "window_minutes": <…>, "cooldown_minutes": <…>,
                "action": "<add_one_instance | add_two_instances>"},
  "scale_in": {"metric": "per_instance_utilization_percent", "threshold_percent": <…>,
               "window_minutes": <…>, "cooldown_minutes": <…>,
               "action": "<remove_one_instance | drain_then_remove_one_instance>",
               "connection_drain_seconds": <…>, "never_below_minimum": <true | false>},
  "verification": {"add_instance": "<…>", "lose_instance": "<…>"}
}
```

This is a design exercise, not a deployment or a live failure test. Run
`dsoxlab check concevoir-elasticite` to see the result.
