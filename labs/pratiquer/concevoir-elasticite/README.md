# Design an elastic application tier

Turn the supplied workload evidence into an elasticity plan. Externalize
sessions and uploads, make request handling safe to retry, and specify health
and readiness checks before changing replica count.

| | |
|---|---|
| Target | your machine, `challenge/work/` directory, no cloud account |
| Duration | about 35 minutes |
| Companion lesson | [the lesson on the site, in French](https://www.stephane-robert.info/docs/cloud/fondamentaux/elasticite-vs-scalabilite/) |

```bash
dsoxlab run   concevoir-elasticite
dsoxlab check concevoir-elasticite
```

Calculate the minimum replica count that serves the sustained peak even after
one instance is lost. Document scale-out and scale-in with separate thresholds,
observation windows, cooldown and connection draining. The exercise grades a
design artifact; it does not deploy an autoscaler or claim a live failure test.
