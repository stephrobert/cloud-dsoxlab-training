# Mission : chiffrer l'environnement fourni

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
dsoxlab check challenge-budget-contraint
dsoxlab clean challenge-budget-contraint
```

Indices par `dsoxlab hint`, déduits du score : 10, 15 puis 20 points.
