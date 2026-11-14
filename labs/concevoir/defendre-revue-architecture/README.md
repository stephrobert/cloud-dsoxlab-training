# Defend a cloud architecture review with evidence

Review the customer portal using its architecture and measurement evidence.

| | |
|---|---|
| Target | your machine, `challenge/work/` directory, no cloud account |
| Duration | about 45 minutes |
| Companion lesson | [the lesson on the site, in French](https://www.stephane-robert.info/docs/cloud/fondamentaux/well-architected-frameworks/) |

```bash
dsoxlab run   defendre-revue-architecture
dsoxlab check defendre-revue-architecture
```

## What you will be able to do

- Score six architecture axes from 0 to 3 and cite evidence for each score.
- Rank the highest risks, record an ADR decision for each, and assign an owner
  and due date to every action.
- State clearly what the supplied evidence does not prove.

## Evidence boundary

The evidence pack is a controlled snapshot from a local exercise. It is not a
live cloud account, provider bill, or proof of real IAM enforcement or
dataplane behavior. A score of 3 is justified only by a dated test or
measurement in that snapshot.

See the lesson:
<https://www.stephane-robert.info/docs/cloud/fondamentaux/well-architected-frameworks/>.
