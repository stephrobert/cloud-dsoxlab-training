# Réseau privé, et premières instances sans adresse publique : scw sur feint

Chez Scaleway, le **réseau privé est régional** et ses **attachements sont
zonaux** : un seul Private Network couvre la région `fr-par`, et chaque
instance s'y branche par une **NIC privée** créée dans sa propre zone. Une
instance sans IP publique sort vers Internet par une **Public Gateway**, zonale
elle aussi, reliée au réseau par un **gateway-network** qui pousse la **route
par défaut** et fait du NAT. Ce lab vous fait construire cette architecture
avec le CLI officiel `scw`, sans compte, contre l'émulateur **feint**.

Leçon du site qui porte ce lab :
<https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/>.

## Ce que vous saurez faire

- Créer un VPC et un Private Network régionaux sur un plan d'adressage donné.
- Créer deux instances **sans IP publique** dans deux zones de la même région.
- Attacher le même réseau privé dans chaque zone, par une NIC par instance.
- Créer une Public Gateway et la relier au réseau, route par défaut et NAT
  activés.
- Lire l'état obtenu par le CLI, plutôt que de croire les commandes tapées.

## Prérequis

- **dsoxlab installé** et **Docker** qui répond : feint tourne en conteneur,
  démarré par `dsoxlab run`.
- **`scw` installé** (2.62.0 au moment de l'écriture) : leçon
  <https://blog.stephane-robert.info/docs/cloud/outils/feint/clients/>.
- **Le port 4599 libre** sur votre poste : arrêtez tout feint que vous auriez
  lancé vous-même (`feint stop`, ou `docker stop` de son conteneur).
- Les notions du module 3 : réseau privé, passerelle NAT, route par défaut.

## Durée

40 minutes environ.

## La limite à garder en tête

**feint prouve l'existence des ressources et de leurs liens, pas la sortie
réseau.** Il n'achemine aucun paquet, n'applique ni routage ni NAT, et ne sert
ni les règles PAT ni le bastion de la passerelle. Ce lab vérifie donc que votre
architecture est **déclarée** correctement. Qu'une instance installe réellement
ses paquets par la passerelle ne se constate que sur un vrai compte : c'est la
section facultative « Pratiquer sur un cloud européen » de la leçon.

## Démarrer

```bash
dsoxlab run reseau-prive-scaleway
cd labs/reseau/reseau-prive-scaleway/challenge/work
source feint-scaleway.env      # ou : eval "$(feint env scaleway)"
cat PLAN.md
```

`feint-scaleway.env` pointe `scw` sur `http://127.0.0.1:4599` avec des
identifiants fictifs : aucune requête ne part vers Scaleway.

## Étape 1 : le VPC et le réseau privé, régionaux

```bash
vpc=$(scw vpc vpc create name=boutique-vpc region=fr-par -o json | jq -r .id)
pn=$(scw vpc private-network create name=boutique-prive vpc-id="$vpc" \
  subnets.0=10.42.1.0/24 region=fr-par -o json | jq -r .id)
scw vpc private-network get "$pn" region=fr-par
```

Notez qu'aucune **zone** n'apparaît : le réseau couvre la région entière.

## Étape 2 : deux instances, deux zones, aucune IP publique

```bash
s1=$(scw instance server create name=boutique-app-1 type=DEV1-S \
  image=ubuntu_noble zone=fr-par-1 ip=none -o json | jq -r .id)
s2=$(scw instance server create name=boutique-app-2 type=DEV1-S \
  image=ubuntu_noble zone=fr-par-2 ip=none -o json | jq -r .id)
scw instance server list zone=all
```

`ip=none` est le point clé : la colonne `PUBLIC IP` reste vide.

## Étape 3 : un réseau, une NIC par zone

```bash
scw instance private-nic create server-id="$s1" private-network-id="$pn" zone=fr-par-1
scw instance private-nic create server-id="$s2" private-network-id="$pn" zone=fr-par-2
```

Le **même** `private-network-id` dans les deux zones : c'est ce que veut dire
« réseau régional, attachements zonaux ».

## Étape 4 : la passerelle, sa route par défaut et son NAT

```bash
ip=$(scw vpc-gw ip create zone=fr-par-1 -o json | jq -r .id)
gw=$(scw vpc-gw gateway create name=boutique-gw type=VPC-GW-S ip-id="$ip" \
  zone=fr-par-1 -o json | jq -r .id)
scw vpc-gw gateway-network create gateway-id="$gw" private-network-id="$pn" \
  enable-masquerade=true push-default-route=true zone=fr-par-1
scw vpc-gw gateway-network list zone=fr-par-1 -o json \
  | jq '.[] | {push_default_route, masquerade_enabled}'
```

La réponse de **création** affiche `enable_masquerade: null` : relisez par
`list`, qui porte `masquerade_enabled: true`. Lire l'état plutôt que la réponse
d'une commande est précisément le réflexe que ce lab entraîne.

```bash
dsoxlab check reseau-prive-scaleway
dsoxlab clean reseau-prive-scaleway
```
