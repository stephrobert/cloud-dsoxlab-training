# Mission: cost the environment provided

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
dsoxlab check challenge-budget-contraint
dsoxlab clean challenge-budget-contraint
```

Hints through `dsoxlab hint`, deducted from the score: 10, 15 then 20 points.
