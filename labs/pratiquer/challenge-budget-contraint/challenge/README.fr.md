# La facture avant la carte bancaire

## La situation

**Compétence visée : `cloud.cost.estimate`.**

L'équipe de la boutique a hérité d'un environnement déjà déployé : un
frontal, des instances d'API, une base et son volume, une passerelle, et
quelques restes d'essais dont personne ne se souvient. La direction a fixé un
plafond : **160 euros HT par mois**. Avant de signer quoi que ce soit, elle
veut une estimation chiffrée, et la liste de ce qu'on paie pour rien.

Personne n'a de compte chez le fournisseur : l'environnement est servi par
feint, que le CLI `scw` interroge comme il interrogerait Scaleway. La grille
tarifaire datée du jour est posée dans votre répertoire de travail, avec un
gabarit d'estimation à remplir.

Vous ne modifiez rien : vous lisez, vous comptez, vous concluez.

## Mission : chiffrer l'environnement fourni

5 tâches, 100 points, 45 minutes

L'environnement est servi par feint. Pointez `scw` dessus avec
`challenge/work/feint-scaleway.env`. La grille est
`challenge/work/grille-tarifaire.yaml` ; le livrable,
`challenge/work/estimation.yaml`, se remplit à la place du gabarit. Budget :
**160 euros HT par mois**.

Règle du jeu : l'environnement se **lit**, il ne se modifie pas. Toute
ressource créée ou supprimée invalide la copie.

### Tâche 1 : les instances (20 pts)

`instances` : le nombre d'instances de chaque type commercial.

### Tâche 2 : le stockage bloc (20 pts)

`volumes_go` : le total des volumes bloc facturés, en Go.

### Tâche 3 : les IP et les passerelles (20 pts)

`ips_flexibles` et `passerelles`, comptées selon les règles de la grille.

### Tâche 4 : le coût mensuel (20 pts)

`cout_mensuel_eur` : le total, à 50 centimes près.

### Tâche 5 : le verdict (20 pts)

`dans_le_budget` (`true` ou `false`), et `non_rattaches` : chaque ressource
facturée rattachée à rien, par son nom (volume) ou son adresse (IP).

```bash
dsoxlab check pratiquer-challenge-budget-contraint
dsoxlab clean pratiquer-challenge-budget-contraint
```

Indices par `dsoxlab hint`, déduits du score : 10, 15 puis 20 points.
