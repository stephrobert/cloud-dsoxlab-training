# Challenge: choose and size a compute model

Read `workload.json` and create `compute-decision.json` in the working
directory. Record the model, processor architecture, selected machine profile,
the p95 demand after planned growth, and a concise rationale.

Use this shape:

```json
{
  "compute_model": "virtual_machine",
  "architecture": "x86_64",
  "machine_profile": "m7i.xlarge",
  "sizing_demand": {
    "cpu_vcpus": 3.84,
    "memory_gib": 12.48
  },
  "rationale": "Explain the runtime, compatibility and measured-sizing decision."
}
```

Use the week-long p95 measurements and the stated growth factor. The brief
maximum lasted only seconds; do not size the workload as if that were sustained
demand. Select the least-cost profile that meets both sizing demands and is
compatible with the tested processor architecture. Relative cost units are
exercise data, not provider prices.

Run `dsoxlab check choisir-modele-calcul` to see the result.
