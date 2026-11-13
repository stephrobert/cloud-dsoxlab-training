# Choisir un modèle de calcul et le dimensionner sur des mesures

Utilisez un profil mesuré pour sélectionner un modèle de calcul et une taille
de machine compatible.

| | |
|---|---|
| Cible | votre poste, répertoire `challenge/work/`, sans compte cloud |
| Durée | environ 35 minutes |
| Page associée | [la leçon du site](https://www.stephane-robert.info/docs/cloud/compute/machines-et-dimensionnement/) |

```bash
dsoxlab run   choisir-modele-calcul
dsoxlab check choisir-modele-calcul
```

## Ce que vous saurez faire

- Choisir entre machine virtuelle, conteneurs managés et fonctions selon les
  contraintes d'exécution du workload.
- Dimensionner une machine à partir du CPU et de la mémoire au 95e centile
  mesurés sur une semaine, en appliquant la croissance prévue.
- Comparer architectures de processeur et familles sans confondre un pic bref
  avec une charge soutenue.

## Limite de la preuve

Les mesures et le catalogue de machines sont des données d'exercice contrôlées.
Les unités de coût relatives ne sont pas des tarifs fournisseur et aucune
ressource cloud n'est créée.

Voir la leçon :
<https://www.stephane-robert.info/docs/cloud/compute/machines-et-dimensionnement/>.
