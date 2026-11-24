# The same network, at another provider

## The situation

**Skill targeted: `cloud.network.design`.**

The shop wants to keep an exit door: its private network must be declarable at
Outscale as well as at Scaleway. The need does not change: two zones, no public
address on the machines, a single controlled way out to the Internet. The model
does change: at Outscale, a subnet lives in a single Subregion, and the way out
goes through a NAT Service and route tables you link yourself.

The plan is settled (`PLAN.md`). You start from an empty emulator and the
`octl` CLI pointed at it. No resource exists yet.

## Mission: the shop's private network at Outscale, declared on feint

5 tasks, 100 points, 45 minutes

The plan is in `challenge/work/PLAN.md`, the CLI environment in
`challenge/work/feint-outscale.env`. Grading reads feint's state, not your
commands; feint proves existence and links, not network egress.

### Task 1: the Net and its subnets (20 pts)

The Net `10.20.0.0/16`, tag `Name=boutique-net`, and its three subnets:
`10.20.0.0/24` and `10.20.1.0/24` in `eu-west-2a`, `10.20.2.0/24` in
`eu-west-2b`.

### Task 2: two VMs, two Subregions, no public IP (20 pts)

`boutique-app-1` in `10.20.1.0/24`, `boutique-app-2` in `10.20.2.0/24`
(`Name` tag), with no public IP.

### Task 3: the public way out (20 pts)

An Internet Service linked to the Net, and a `0.0.0.0/0` route to it in the
table linked to subnet `10.20.0.0/24`.

### Task 4: the NAT Service (20 pts)

A NAT Service in `10.20.0.0/24`, with its public IP.

### Task 5: the route of the private subnets (20 pts)

`10.20.1.0/24` and `10.20.2.0/24` have their `0.0.0.0/0` route to that NAT
Service.

```bash
dsoxlab check reseau-prive-outscale
dsoxlab clean reseau-prive-outscale
```

Hints through `dsoxlab hint`, deducted from the score: 10, 15 then 20 points.
