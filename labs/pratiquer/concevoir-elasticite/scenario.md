# Prepare the customer portal for variable traffic

The customer portal currently runs three identical application instances.
Traffic has a measured sustained peak of 1,500 requests per second, and each
instance has a tested safe capacity of 800 requests per second at the p95
latency objective. A single-instance loss must not push the remaining tier
above that tested capacity.

The application currently stores sessions and uploaded files on its local
disk. The team wants to add and remove instances without changing application
code, and a client retry after an instance loss must not duplicate an order.
Write an elasticity plan from the workload fixture. Include state placement,
retry safety, health and readiness, the replica floor and ceiling, a loss
calculation, and safe scale-out and scale-in actions.

The fixture is measured exercise data, not a provider guarantee. No service is
deployed and no actual failure or autoscaling event is claimed.

Skill targeted: `cloud.elasticity.design`
