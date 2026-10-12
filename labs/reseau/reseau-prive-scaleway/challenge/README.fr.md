# Mission : le réseau privé de la boutique, déclaré sur feint

5 tâches, 100 points, 40 minutes

Le plan est dans `challenge/work/PLAN.md`, l'environnement du CLI dans
`challenge/work/feint-scaleway.env`. La note lit l'état de feint, pas vos
commandes. Rappel : feint prouve l'existence et les liens, pas la sortie
réseau.

### Tâche 1 : VPC et réseau privé régionaux (20 pts)

`boutique-vpc` et, dans ce VPC, le Private Network `boutique-prive` en
`fr-par`, avec le seul sous-réseau IPv4 `10.42.1.0/24`.

### Tâche 2 : deux instances, deux zones, aucune IP publique (20 pts)

`boutique-app-1` en `fr-par-1` et `boutique-app-2` en `fr-par-2`, sans
adresse publique.

### Tâche 3 : le même réseau attaché dans chaque zone (20 pts)

Chaque instance porte une NIC privée sur `boutique-prive`, dans sa zone.

### Tâche 4 : la Public Gateway (20 pts)

`boutique-gw`, type `VPC-GW-S`, en `fr-par-1`, avec son IP.

### Tâche 5 : route par défaut et NAT (20 pts)

Un gateway-network relie `boutique-gw` à `boutique-prive`, route par défaut
poussée et NAT activé.

```bash
dsoxlab check reseau-prive-scaleway
dsoxlab clean reseau-prive-scaleway
```

Indices par `dsoxlab hint`, déduits du score : 10, 15 puis 20 points.
