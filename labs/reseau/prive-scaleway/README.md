# Private network, and first instances with no public address: scw on feint

At Scaleway, the **private network is regional** and its **attachments are
zonal**: a single Private Network covers the `fr-par` region, and each
instance plugs into it through a **private NIC** created in its own zone. An
instance with no public IP reaches the Internet through a **Public Gateway**,
zonal as well, linked to the network by a **gateway-network** that pushes the
**default route** and does NAT. This lab has you build that architecture with
the official `scw` CLI, without an account, against the **feint** emulator.

Lesson of the site that carries this lab (in French):
<https://www.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/>.

## What you will be able to do

- Create a regional VPC and Private Network on a given address plan.
- Create two instances **with no public IP** in two zones of the same region.
- Attach the same private network in each zone, through one NIC per instance.
- Create a Public Gateway and link it to the network, default route and NAT
  on.
- Read the resulting state through the CLI, instead of trusting the commands
  typed.

## Prerequisites

- **dsoxlab installed** and a working **Docker**: feint runs in a container,
  started by `dsoxlab run`.
- **`scw` installed** (2.62.0 at the time of writing): lesson
  <https://www.stephane-robert.info/en/docs/cloud/outils/feint/clients/>.
- **Port 4599 free** on your host: stop any feint you started yourself
  (`feint stop`, or `docker stop` its container).
- The notions of module 3: private network, NAT gateway, default route.

## Duration

About 40 minutes.

## The limit to keep in mind

**feint proves that resources and their links exist, not network egress.** It
forwards no packet, applies neither routing nor NAT, and serves neither PAT
rules nor the gateway bastion. This lab therefore checks that your architecture
is **declared** correctly. That an instance really installs its packages
through the gateway can only be seen on a real account: that is the optional
section "Practise on a European cloud" of the lesson.

## Start

```bash
dsoxlab run reseau-prive-scaleway
cd labs/reseau/prive-scaleway/challenge/work
source feint-scaleway.env      # or: eval "$(feint env scaleway)"
cat PLAN.md
```

`feint-scaleway.env` points `scw` at `http://127.0.0.1:4599` with dummy
credentials: no request goes to Scaleway.

## Step 1: the VPC and the private network, regional

```bash
vpc=$(scw vpc vpc create name=boutique-vpc region=fr-par -o json | jq -r .id)
pn=$(scw vpc private-network create name=boutique-prive vpc-id="$vpc" \
  subnets.0=10.42.1.0/24 region=fr-par -o json | jq -r .id)
scw vpc private-network get "$pn" region=fr-par
```

Note that no **zone** appears: the network covers the whole region.

## Step 2: two instances, two zones, no public IP

```bash
s1=$(scw instance server create name=boutique-app-1 type=DEV1-S \
  image=ubuntu_noble zone=fr-par-1 ip=none -o json | jq -r .id)
s2=$(scw instance server create name=boutique-app-2 type=DEV1-S \
  image=ubuntu_noble zone=fr-par-2 ip=none -o json | jq -r .id)
scw instance server list zone=all
```

`ip=none` is the key point: the `PUBLIC IP` column stays empty.

## Step 3: one network, one NIC per zone

```bash
scw instance private-nic create server-id="$s1" private-network-id="$pn" zone=fr-par-1
scw instance private-nic create server-id="$s2" private-network-id="$pn" zone=fr-par-2
```

The **same** `private-network-id` in both zones: that is what "regional
network, zonal attachments" means.

## Step 4: the gateway, its default route and its NAT

```bash
ip=$(scw vpc-gw ip create zone=fr-par-1 -o json | jq -r .id)
gw=$(scw vpc-gw gateway create name=boutique-gw type=VPC-GW-S ip-id="$ip" \
  zone=fr-par-1 -o json | jq -r .id)
scw vpc-gw gateway-network create gateway-id="$gw" private-network-id="$pn" \
  enable-masquerade=true push-default-route=true zone=fr-par-1
scw vpc-gw gateway-network list zone=fr-par-1 -o json \
  | jq '.[] | {push_default_route, masquerade_enabled}'
```

The **creation** response shows `enable_masquerade: null`: read it back with
`list`, which carries `masquerade_enabled: true`. Reading the state rather than
a command's response is exactly the reflex this lab trains.

```bash
dsoxlab check reseau-prive-scaleway
dsoxlab clean reseau-prive-scaleway
```
