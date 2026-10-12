# Journal des modifications

**Language:** [English](./CHANGELOG.md) · [Français](./CHANGELOG.fr.md)

Tous les changements notables de ce projet sont consignés dans ce fichier. Le
format s'appuie sur [Keep a Changelog](https://keepachangelog.com/).

Ce dépôt est un **catalogue de contenu**, pas une bibliothèque. Une version se
publie par un tag, qui produit une archive signée (voir
[RELEASING.fr.md](./RELEASING.fr.md)) ; l'unité qui compte reste le lab.

## [Non publié]

### Ajouté

- **Le catalogue**, sur la structure du catalogue DevSecOps, lui-même aligné
  sur Kubernetes, Linux et Terraform : contrat `meta.yml` et `meta.fr.yml`,
  réseau `lab-cloud` réservé en `10.10.70.0/24`, méta-tests du dépôt, README
  bilingues dont le catalogue est généré, chaîne CI et de publication reprise
  à l'identique (zizmor, actionlint, poutine, Plumber, CodeQL, Scorecard,
  archive signée et provenance SLSA).
- **La grille d'objectifs** (`curriculums.yml`) : les 18 compétences `cloud.*`
  candidates du contrat de la formation. Chaque lab cite celle qu'il éprouve,
  et `tests/test_curriculums.py` le vérifie contre ses `skills`.
- **Vague 1 des labs**, modules 2b, 2c et 3 de la formation :
  - `pratiquer-challenge-budget-contraint`, challenge 1 : un environnement tiré
    au hasard dans feint, lu par `scw` et chiffré sur une grille d'exercice
    datée du 2026-10-12 ;
  - `amorcer-premiere-vm-propre` : une VM Incus amorcée par cloud-init sur un
    réseau privé, vérifiée par testinfra, détruite par `clean` ;
  - `reseau-prive-scaleway` et `reseau-prive-outscale` : le réseau privé
    multi-zones déclaré sur feint par `scw` puis par `octl`.
- **Deux preuves de validation** : `scripts/valider-labs.py`, par les vraies
  commandes dsoxlab, et `scripts/verify-solutions.py`, sans dsoxlab, qui
  démarre feint et joue `setup.yaml` lui-même.

### Mesuré

- Les quatre labs rendent 0 avant le travail et 100 après, par dsoxlab 0.3.1,
  feint v0.13.0 (image épinglée par digest), scw 2.62.0, octl v0.0.32 et
  Incus 7.2, sans conteneur, instance ni réseau laissé derrière.
- Contrôles négatifs : une IP publique sur une instance ne fait tomber que la
  tâche 2 du lab Scaleway ; une table privée non liée en `eu-west-2b` ne fait
  tomber que la tâche 5 du lab Outscale ; un inventaire limité à la zone par
  défaut rend 40/100 au challenge ; une ressource supprimée le rend 0/100.
