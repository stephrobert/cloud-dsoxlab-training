# Scenario: the oversized indexer

The product-image indexer runs continuously and processes long-lived HTTP
requests. The current machine is larger than the measurements appear to need,
but the team has not checked the request-duration limit of functions, the
runtime's kernel dependency, processor compatibility, or weekly p95 memory use.

A scenario says **where we are and what is wrong**, not the steps to take:
finding those is the learner's work.

## Mission

Use `workload.json` to create `compute-decision.json`. Record the compute
model, processor architecture, machine profile, the measured demand used for
sizing, and a short rationale. The brief contains a full week of measurements,
including a brief maximum that should not be mistaken for sustained load.

Skill targeted: `cloud.compute.choose`
