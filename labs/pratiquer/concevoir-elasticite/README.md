# Design an elastic application tier

Turn the supplied workload evidence into an elasticity plan. Externalize
sessions and uploads, make request handling safe to retry, and specify health
and readiness checks before changing replica count.

Calculate the minimum replica count that serves the sustained peak even after
one instance is lost. Document scale-out and scale-in with separate thresholds,
observation windows, cooldown and connection draining. The exercise grades a
design artifact; it does not deploy an autoscaler or claim a live failure test.
