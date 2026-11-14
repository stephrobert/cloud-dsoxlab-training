# Challenge: choose and size a compute model

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
