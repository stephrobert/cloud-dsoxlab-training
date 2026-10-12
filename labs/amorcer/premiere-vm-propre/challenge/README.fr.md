# Mission : la machine `boutique-vm1`

5 tâches, 100 points, 30 minutes

Le travail se fait dans `challenge/work`. La machine se crée **à partir de**
`challenge/work/user-data.yaml` : une machine configurée à la main après son
démarrage ne compte pas.

### Tâche 1 : une VM sur le réseau privé, sans adresse publique (20 pts)

Une **machine virtuelle** Incus nommée `boutique-vm1`, démarrée, branchée sur
le seul réseau `lab-amorcer`. Toutes ses adresses de portée globale sont dans
`10.10.71.0/24`.

### Tâche 2 : cloud-init terminé, avec votre user-data (20 pts)

Le user-data de l'instance est exactement `challenge/work/user-data.yaml`, qui
commence par `#cloud-config` et ne porte plus de `???`. cloud-init rend
`status: done`, sans erreur.

### Tâche 3 : l'utilisateur `boutique` (20 pts)

Shell `/bin/bash`, mot de passe verrouillé, absent du groupe `sudo`, et la clé
`challenge/work/cle_lab.pub` autorisée dans son `authorized_keys`.

### Tâche 4 : les paquets (20 pts)

`jq` et `tree` sont installés.

### Tâche 5 : le fichier de rôle (20 pts)

`/etc/boutique/role` contient `app`, appartient à `root:root`, droits `0644`.

## Valider, puis détruire

```bash
dsoxlab check premiere-vm-propre
dsoxlab clean premiere-vm-propre
```

Indices disponibles par `dsoxlab hint`, chacun déduit du score : 10, 15 puis
20 points.
