# Réseau privé, et premières instances sans adresse publique : octl sur feint

Chez Outscale, le **Net est régional** mais chaque **sous-réseau appartient à
une seule sous-région**. Un réseau privé sur deux zones se construit donc avec
**un sous-réseau par sous-région**. Les VM sans IP publique sortent par un
**NAT Service** posé dans un sous-réseau **public**, lui-même routé vers un
**Internet Service** lié au Net. Ce lab vous fait construire cette
architecture avec le CLI officiel `octl`, sans compte, contre l'émulateur
**feint**. C'est la variante Outscale du lab `reseau-prive-scaleway` : le même
besoin, un autre modèle de fournisseur.

Leçon du site qui porte ce lab :
<https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/>.

## Ce que vous saurez faire

- Créer un Net et trois sous-réseaux répartis sur deux sous-régions.
- Créer deux VM **sans IP publique**, une par sous-région.
- Lier un Internet Service au Net et router le sous-réseau public vers lui.
- Poser un NAT Service dans le sous-réseau public et y router les sous-réseaux
  privés.
- Lire l'état obtenu, plutôt que de croire les commandes tapées.

## Prérequis

- **dsoxlab installé** et **Docker** qui répond : feint tourne en conteneur.
- **`octl` installé** (v0.0.32 au moment de l'écriture) : leçon
  <https://blog.stephane-robert.info/docs/cloud/outils/feint/clients/>.
- **Le port 4599 libre** : arrêtez tout feint lancé par vous-même.
- Les notions du module 3 : sous-réseau, table de routage, NAT.

## Durée

45 minutes environ.

## La limite à garder en tête

**feint prouve l'existence des ressources et de leurs liens, pas la sortie
réseau** : il n'achemine aucun paquet. Que la VM sorte réellement par le NAT ne
se constate que sur un vrai compte.

## Démarrer

```bash
dsoxlab run reseau-prive-outscale
cd labs/reseau/prive-outscale/challenge/work
source feint-outscale.env      # ou : eval "$(feint env outscale)"
cat PLAN.md
o() { octl iaas api "$@" --output json --no-upgrade; }
```

La fonction `o` raccourcit les appels. `octl iaas api <Action>` accepte toute
action de l'API Outscale ; en JSON, il rend l'objet créé, ou la liste lue.

## Étape 1 : le Net et ses trois sous-réseaux

```bash
net=$(o CreateNet --IpRange=10.20.0.0/16 | jq -r .NetId)
o CreateTags --ResourceIds="$net" --Tags.0.Key=Name --Tags.0.Value=boutique-net
pub=$(o CreateSubnet --NetId="$net" --IpRange=10.20.0.0/24 --SubregionName=eu-west-2a | jq -r .SubnetId)
pa=$(o CreateSubnet --NetId="$net" --IpRange=10.20.1.0/24 --SubregionName=eu-west-2a | jq -r .SubnetId)
pb=$(o CreateSubnet --NetId="$net" --IpRange=10.20.2.0/24 --SubregionName=eu-west-2b | jq -r .SubnetId)
```

## Étape 2 : la sortie publique

```bash
igw=$(o CreateInternetService | jq -r .InternetServiceId)
o LinkInternetService --InternetServiceId="$igw" --NetId="$net"
rtp=$(o CreateRouteTable --NetId="$net" | jq -r .RouteTableId)
o CreateRoute --RouteTableId="$rtp" --DestinationIpRange=0.0.0.0/0 --GatewayId="$igw"
o LinkRouteTable --RouteTableId="$rtp" --SubnetId="$pub"
```

## Étape 3 : le NAT et la route des sous-réseaux privés

```bash
eip=$(o CreatePublicIp | jq -r .PublicIpId)
nat=$(o CreateNatService --SubnetId="$pub" --PublicIpId="$eip" | jq -r .NatServiceId)
rtv=$(o CreateRouteTable --NetId="$net" | jq -r .RouteTableId)
o CreateRoute --RouteTableId="$rtv" --DestinationIpRange=0.0.0.0/0 --NatServiceId="$nat"
o LinkRouteTable --RouteTableId="$rtv" --SubnetId="$pa"
o LinkRouteTable --RouteTableId="$rtv" --SubnetId="$pb"
```

## Étape 4 : deux VM sans IP publique

```bash
img=$(o ReadImages | jq -r '.[0].ImageId')
vm1=$(o CreateVms --ImageId="$img" --SubnetId="$pa" --VmType=tinav6.c1r1p2 | jq -r '.[0].VmId')
vm2=$(o CreateVms --ImageId="$img" --SubnetId="$pb" --VmType=tinav6.c1r1p2 | jq -r '.[0].VmId')
o CreateTags --ResourceIds="$vm1" --Tags.0.Key=Name --Tags.0.Value=boutique-app-1
o CreateTags --ResourceIds="$vm2" --Tags.0.Key=Name --Tags.0.Value=boutique-app-2
o ReadVms | jq '.[] | {VmId, SubnetId, PublicIp, PrivateIp}'
```

`PublicIp` reste `null` : la VM n'est joignable que depuis le Net.

```bash
dsoxlab check reseau-prive-outscale
dsoxlab clean reseau-prive-outscale
```
