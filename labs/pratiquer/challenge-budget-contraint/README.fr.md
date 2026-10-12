# Challenge 1 : architecture à budget contraint

Ce challenge clôt le module « Pratiquer sans compte ». Il éprouve la
compétence **estimer le coût d'une architecture** sur un environnement que vous
n'avez pas construit : il faut le **lire**, par le CLI officiel branché sur
l'émulateur **feint**, puis le **chiffrer** sur une grille tarifaire datée.
C'est un challenge, pas un lab guidé : aucune commande n'est donnée.

Leçon du site qui porte ce challenge :
<https://blog.stephane-robert.info/docs/cloud/outils/feint/limites/>.

## Ce qui est éprouvé

- Inventorier un environnement par le CLI, **toutes zones** comprises.
- Appliquer une grille datée **jusqu'à ses règles** : ce qui est facturé, ce
  qui ne l'est pas.
- Conclure sur le **budget**, et repérer ce qui coûte sans servir.

## Prérequis

- Le module 2 de la formation (lire une facture, grilles datées) et les leçons
  du module 2b : feint installé, et **`scw` branché sur feint** :
  <https://blog.stephane-robert.info/docs/cloud/outils/feint/clients/>.
- **dsoxlab** et **Docker** : feint tourne en conteneur, démarré par
  `dsoxlab run`. Le port **4599** doit être libre.

## Durée

45 minutes environ.

## Ce que la note mesure, et ce qu'elle ne mesure pas

La note compare votre `estimation.yaml` à un coût **recalculé** à l'instant du
check, depuis l'état réel de feint et la grille fournie. L'environnement est
**tiré au hasard** à chaque `dsoxlab run` : la réponse d'un autre apprenant ne
vaut rien pour vous.

feint n'émule **aucun prix** : la grille est une grille d'exercice, datée,
dont les montants sont fixés pour ce challenge. Une vraie facture se confronte
aux tarifs relevés chez le fournisseur, à leur date, et à la facture mensuelle,
qui seule fait foi.

```bash
dsoxlab run challenge-budget-contraint
dsoxlab challenge challenge-budget-contraint
```
