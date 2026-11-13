# Choose a compute model and size it from measurements

Use a measured workload profile to select a compute model and a compatible
machine size.

| | |
|---|---|
| Target | your machine, `challenge/work/` directory, no cloud account |
| Duration | about 35 minutes |
| Companion lesson | [the lesson on the site, in French](https://www.stephane-robert.info/docs/cloud/compute/machines-et-dimensionnement/) |

```bash
dsoxlab run   choisir-modele-calcul
dsoxlab check choisir-modele-calcul
```

## What you will be able to do

- Choose between a virtual machine, managed containers and functions from the
  workload's runtime constraints.
- Size a machine from a week's p95 CPU and memory use, with the stated growth
  factor.
- Compare processor architectures and instance families without treating a
  short-lived maximum as sustained demand.

## Evidence boundary

The workload measurements and machine catalogue are controlled exercise data.
Relative cost units are not provider prices, and no cloud resource is created.

See the lesson:
<https://www.stephane-robert.info/docs/cloud/compute/machines-et-dimensionnement/>.
