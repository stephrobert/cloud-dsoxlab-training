# Mission : le réseau privé de la boutique chez Outscale, déclaré sur feint

5 tâches, 100 points, 45 minutes

Le plan est dans `challenge/work/PLAN.md`, l'environnement du CLI dans
`challenge/work/feint-outscale.env`. La note lit l'état de feint, pas vos
commandes ; feint prouve l'existence et les liens, pas la sortie réseau.

### Tâche 1 : le Net et ses sous-réseaux (20 pts)

Le Net `10.20.0.0/16`, tag `Name=boutique-net`, et ses trois sous-réseaux :
`10.20.0.0/24` et `10.20.1.0/24` en `eu-west-2a`, `10.20.2.0/24` en
`eu-west-2b`.

### Tâche 2 : deux VM, deux sous-régions, aucune IP publique (20 pts)

`boutique-app-1` dans `10.20.1.0/24`, `boutique-app-2` dans `10.20.2.0/24`
(tag `Name`), sans IP publique.

### Tâche 3 : la sortie publique (20 pts)

Un Internet Service lié au Net, et une route `0.0.0.0/0` vers lui dans la
table liée au sous-réseau `10.20.0.0/24`.

### Tâche 4 : le NAT Service (20 pts)

Un NAT Service dans `10.20.0.0/24`, avec son IP publique.

### Tâche 5 : la route des sous-réseaux privés (20 pts)

`10.20.1.0/24` et `10.20.2.0/24` ont leur route `0.0.0.0/0` vers ce NAT
Service.

```bash
dsoxlab check reseau-prive-outscale
dsoxlab clean reseau-prive-outscale
```

Indices par `dsoxlab hint`, déduits du score : 10, 15 puis 20 points.
