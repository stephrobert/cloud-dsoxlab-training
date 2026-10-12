# Private network, and first instances with no public address: octl on feint

At Outscale, the **Net is regional** but each **subnet belongs to a single
Subregion**. A private network over two zones is therefore built with **one
subnet per Subregion**. VMs with no public IP go out through a **NAT Service**
placed in a **public** subnet, itself routed to an **Internet Service** linked
to the Net. This lab has you build that architecture with the official `octl`
CLI, without an account, against the **feint** emulator. It is the Outscale
variant of the `reseau-prive-scaleway` lab: the same need, another provider
model.

Lesson of the site that carries this lab (in French):
<https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/>.

## What you will be able to do

- Create a Net and three subnets spread over two Subregions.
- Create two VMs **with no public IP**, one per Subregion.
- Link an Internet Service to the Net and route the public subnet to it.
- Place a NAT Service in the public subnet and route the private subnets to
  it.
- Read the resulting state, instead of trusting the commands typed.

## Prerequisites

- **dsoxlab installed** and a working **Docker**: feint runs in a container.
- **`octl` installed** (v0.0.32 at the time of writing): lesson
  <https://blog.stephane-robert.info/docs/cloud/outils/feint/clients/>.
- **Port 4599 free**: stop any feint you started yourself.
- The notions of module 3: subnet, route table, NAT.

## Duration

About 45 minutes.

## The limit to keep in mind

**feint proves that resources and their links exist, not network egress**: it
forwards no packet. That the VM really goes out through the NAT can only be
seen on a real account.

## Start

```bash
dsoxlab run reseau-prive-outscale
cd labs/reseau/reseau-prive-outscale/challenge/work
source feint-outscale.env      # or: eval "$(feint env outscale)"
cat PLAN.md
o() { octl iaas api "$@" --output json --no-upgrade; }
```

The `o` function shortens the calls. `octl iaas api <Action>` accepts any
action of the Outscale API; in JSON it returns the object created, or the list
read.

## Step 1: the Net and its three subnets

```bash
net=$(o CreateNet --IpRange=10.20.0.0/16 | jq -r .NetId)
o CreateTags --ResourceIds="$net" --Tags.0.Key=Name --Tags.0.Value=boutique-net
pub=$(o CreateSubnet --NetId="$net" --IpRange=10.20.0.0/24 --SubregionName=eu-west-2a | jq -r .SubnetId)
pa=$(o CreateSubnet --NetId="$net" --IpRange=10.20.1.0/24 --SubregionName=eu-west-2a | jq -r .SubnetId)
pb=$(o CreateSubnet --NetId="$net" --IpRange=10.20.2.0/24 --SubregionName=eu-west-2b | jq -r .SubnetId)
```

## Step 2: the public way out

```bash
igw=$(o CreateInternetService | jq -r .InternetServiceId)
o LinkInternetService --InternetServiceId="$igw" --NetId="$net"
rtp=$(o CreateRouteTable --NetId="$net" | jq -r .RouteTableId)
o CreateRoute --RouteTableId="$rtp" --DestinationIpRange=0.0.0.0/0 --GatewayId="$igw"
o LinkRouteTable --RouteTableId="$rtp" --SubnetId="$pub"
```

## Step 3: the NAT and the route of the private subnets

```bash
eip=$(o CreatePublicIp | jq -r .PublicIpId)
nat=$(o CreateNatService --SubnetId="$pub" --PublicIpId="$eip" | jq -r .NatServiceId)
rtv=$(o CreateRouteTable --NetId="$net" | jq -r .RouteTableId)
o CreateRoute --RouteTableId="$rtv" --DestinationIpRange=0.0.0.0/0 --NatServiceId="$nat"
o LinkRouteTable --RouteTableId="$rtv" --SubnetId="$pa"
o LinkRouteTable --RouteTableId="$rtv" --SubnetId="$pb"
```

## Step 4: two VMs with no public IP

```bash
img=$(o ReadImages | jq -r '.[0].ImageId')
vm1=$(o CreateVms --ImageId="$img" --SubnetId="$pa" --VmType=tinav6.c1r1p2 | jq -r '.[0].VmId')
vm2=$(o CreateVms --ImageId="$img" --SubnetId="$pb" --VmType=tinav6.c1r1p2 | jq -r '.[0].VmId')
o CreateTags --ResourceIds="$vm1" --Tags.0.Key=Name --Tags.0.Value=boutique-app-1
o CreateTags --ResourceIds="$vm2" --Tags.0.Key=Name --Tags.0.Value=boutique-app-2
o ReadVms | jq '.[] | {VmId, SubnetId, PublicIp, PrivateIp}'
```

`PublicIp` stays `null`: the VM is reachable from the Net only.

```bash
dsoxlab check reseau-prive-outscale
dsoxlab clean reseau-prive-outscale
```
