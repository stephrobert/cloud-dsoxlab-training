# The oversized indexer

## The situation

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

## Choose and size a compute model

Read `workload.json` and create `compute-decision.json` in the working
directory (`challenge/work/`). Record the model, processor architecture, selected machine profile,
the demand used for sizing, and a concise rationale.

Use this shape (the values in angle brackets are yours to find):

```json
{
  "compute_model": "<virtual_machine | managed_container | function>",
  "architecture": "<processor architecture>",
  "machine_profile": "<an id from machine_catalogue>",
  "sizing_demand": {
    "cpu_vcpus": <number>,
    "memory_gib": <number>
  },
  "rationale": "<why this model, this architecture and this size>"
}
```

The brief holds a full week of measurements, including a short maximum that
lasted only seconds. Relative cost units are exercise data, not provider
prices.

Run `dsoxlab check choisir-modele-calcul` to see the result.
