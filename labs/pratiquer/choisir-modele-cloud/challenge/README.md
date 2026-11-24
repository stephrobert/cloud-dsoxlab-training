# A product team choosing its cloud model

## The situation

The product team is moving a customer-facing API to the cloud. The team can
maintain its application but has no dedicated operations staff. The API has no
kernel or operating-system dependency, handles personal data, and must remain
under the team's control for identity and application configuration.

A scenario says **where we are and what is wrong**, not the steps to take:
finding those is the learner's work.

The constraints and workload are summarized in `brief.json`. The current
proposal names only a cloud provider and does not explain the service model,
deployment model, or division of security responsibilities.

Skill targeted: `cloud.model.choose`

## Choose the cloud model

Read `brief.json` and create `decision.json` in the working directory (`challenge/work/`). Record
the service model, deployment model, and the provider/team security
responsibilities that follow from the brief.

Use this JSON shape (the values in angle brackets are yours to choose):

```json
{
  "service_model": "<iaas | paas | saas>",
  "deployment_model": "<public | private | hybrid>",
  "responsibilities": {
    "provider": ["<responsibility>", "…"],
    "team": ["<responsibility>", "…"]
  },
  "rationale": "<a short explanation tied to the brief>"
}
```

Responsibilities are named from this list: `hardware`, `network`,
`operating_system`, `managed_platform`, `application`, `data`, `identities`,
`configuration`.

The exact ordering of responsibility names does not matter. Your answer is
graded on its resulting content, not on the commands used to create it.

Run `dsoxlab check pratiquer-choisir-modele-cloud` to see the result.
