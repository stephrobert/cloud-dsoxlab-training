# The bill before the credit card

## The situation

**Skill targeted: `cloud.cost.estimate`.**

The shop's team inherited an environment already deployed: a front end, API
instances, a database and its volume, a gateway, and a few leftovers of trials
nobody remembers. Management set a ceiling: **160 euros excluding VAT per
month**. Before signing anything, it wants a costed estimate, and the list of
what is paid for nothing.

Nobody has an account at the provider: the environment is served by feint,
which the `scw` CLI queries as it would query Scaleway. The price grid dated
today sits in your working directory, with an estimate template to fill.

You change nothing: you read, you count, you conclude.

## Mission: cost the environment provided

5 tasks, 100 points, 45 minutes

The environment is served by feint. Point `scw` at it with
`challenge/work/feint-scaleway.env`. The grid is
`challenge/work/grille-tarifaire.yaml`; the deliverable,
`challenge/work/estimation.yaml`, is filled in place of the template. Budget:
**160 euros excluding VAT per month**.

Rule of the game: the environment is **read**, never changed. Any resource
created or deleted voids the answer.

### Task 1: the instances (20 pts)

`instances`: the number of instances of each commercial type.

### Task 2: block storage (20 pts)

`volumes_go`: the total of the billed block volumes, in GB.

### Task 3: IPs and gateways (20 pts)

`ips_flexibles` and `passerelles`, counted according to the grid's rules.

### Task 4: the monthly cost (20 pts)

`cout_mensuel_eur`: the total, within 50 cents.

### Task 5: the verdict (20 pts)

`dans_le_budget` (`true` or `false`), and `non_rattaches`: every billed
resource attached to nothing, by its name (volume) or its address (IP).

```bash
dsoxlab check pratiquer-challenge-budget-contraint
dsoxlab clean pratiquer-challenge-budget-contraint
```

Hints through `dsoxlab hint`, deducted from the score: 10, 15 then 20 points.
