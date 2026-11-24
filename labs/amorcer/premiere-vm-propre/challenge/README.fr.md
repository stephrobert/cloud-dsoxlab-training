# La première machine de la boutique

## La situation

**Compétence visée : `cloud.environment.rebuild`.**

La boutique fil rouge de la formation a son architecture chiffrée. Il lui faut
maintenant sa première machine, celle qui portera l'API. L'équipe s'est fixé
trois règles avant d'en créer une seule :

1. **Rien à la main.** Tout ce que la machine porte au démarrage vient d'un
   fichier user-data versionné. Une machine qu'on ne sait pas recréer à
   l'identique est une machine qu'on finira par perdre.
2. **Aucune adresse publique.** La machine naît sur un réseau privé. Elle peut
   sortir chercher ses paquets, personne ne peut entrer.
3. **Rien ne survit à l'essai.** La machine de test est détruite à la fin,
   avec son réseau.

Vous partez d'un poste où Incus fonctionne, d'un réseau privé `lab-amorcer`
préparé par le lab, d'une paire de clés SSH et d'un gabarit de user-data
incomplet. Il n'existe encore aucune machine.

## Mission : la machine `boutique-vm1`

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
dsoxlab check amorcer-premiere-vm-propre
dsoxlab clean amorcer-premiere-vm-propre
```

Indices disponibles par `dsoxlab hint`, chacun déduit du score : 10, 15 puis
20 points.
