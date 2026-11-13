# Challenge: design an elastic application tier

Read `workload.json` and create `elasticity-plan.json` in the working
directory. Use only the supplied measurements and constraints.

Record the session, upload and order-state locations; how retries avoid
duplicate orders; liveness and readiness checks; the minimum and maximum
replica counts; per-instance capacity; peak demand remaining after one
instance is lost; and the resulting capacity margin.

Define scale-out and scale-in separately. Include their metrics, thresholds,
observation windows, cooldowns and actions. Scale-in must drain connections
before removal and must never go below the required replica floor. State how
you verify the design by adding an instance and by removing one, without
changing application code.

This is a design exercise, not a deployment or a live failure test. Run
`dsoxlab check concevoir-elasticite` to see the result.
