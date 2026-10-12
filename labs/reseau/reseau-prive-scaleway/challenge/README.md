# Mission: the shop's private network, declared on feint

5 tasks, 100 points, 40 minutes

The plan is in `challenge/work/PLAN.md`, the CLI environment in
`challenge/work/feint-scaleway.env`. Grading reads feint's state, not your
commands. Reminder: feint proves existence and links, not network egress.

### Task 1: regional VPC and private network (20 pts)

`boutique-vpc` and, in that VPC, the Private Network `boutique-prive` in
`fr-par`, with the single IPv4 subnet `10.42.1.0/24`.

### Task 2: two instances, two zones, no public IP (20 pts)

`boutique-app-1` in `fr-par-1` and `boutique-app-2` in `fr-par-2`, with no
public address.

### Task 3: the same network attached in each zone (20 pts)

Each instance carries a private NIC on `boutique-prive`, in its zone.

### Task 4: the Public Gateway (20 pts)

`boutique-gw`, type `VPC-GW-S`, in `fr-par-1`, with its IP.

### Task 5: default route and NAT (20 pts)

A gateway-network links `boutique-gw` to `boutique-prive`, default route pushed
and NAT on.

```bash
dsoxlab check reseau-prive-scaleway
dsoxlab clean reseau-prive-scaleway
```

Hints through `dsoxlab hint`, deducted from the score: 10, 15 then 20 points.
