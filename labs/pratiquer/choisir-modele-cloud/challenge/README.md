# Challenge: choose the cloud model

Read `brief.json` and create `decision.json` in the working directory. Record
the service model, deployment model, and the provider/team security
responsibilities that follow from the brief.

Use this JSON shape:

```json
{
  "service_model": "paas",
  "deployment_model": "public",
  "responsibilities": {
    "provider": ["managed_platform"],
    "team": ["application", "data", "identities", "configuration"]
  },
  "rationale": "A short explanation tied to the brief."
}
```

The exact ordering of responsibility names does not matter. Your answer is
graded on its resulting content, not on the commands used to create it.

Run `dsoxlab check pratiquer-choisir-modele-cloud` to see the result.
