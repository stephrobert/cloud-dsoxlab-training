# Journal des modifications

**Language:** [English](./CHANGELOG.md) · [Français](./CHANGELOG.fr.md)

Tous les changements notables de ce projet sont consignés dans ce fichier. Le
format s'appuie sur [Keep a Changelog](https://keepachangelog.com/).

Ce dépôt est un **catalogue de contenu**, pas une bibliothèque. Une version se
publie par un tag, qui produit une archive signée (voir
[RELEASING.fr.md](./RELEASING.fr.md)) ; l'unité qui compte reste le lab.

## [0.2.1] - 2026-10-19

### Modifié

- **Chaque `doc_url` pointe désormais `www.stephane-robert.info`.** Le site est
  passé de `blog.` à `www.`, et l'ancien hôte redirige en 301 vers le même
  chemin. Rien n'était cassé : `validate-structure --check-urls` suit les
  redirections, et ce catalogue était vert avant qu'une ligne change. La
  migration est une mise au propre et non une réparation : un `doc_url` doit
  pointer la page, pas dépendre d'une redirection qu'il faudra bien retirer un
  jour.

  Les chemins sont identiques entre les deux hôtes : seul l'hôte a changé. Les
  359 `doc_url` que les catalogues déclarent ont été cherchés dans le dépôt du
  site, hors réseau : ils y existent tous, y compris vingt-trois pages que
  l'ancien hôte rendait en 404.

## [0.2.0] - 2026-10-17

### Modifié

- **Le validateur lit le contrat, plus l'encadré du terminal.**
  `scripts/valider-labs.py` lisait le score dans ce que `dsoxlab check`
  *affiche*. Cet encadré est de l'interface : il a changé en dsoxlab 0.4.0 et
  la regex a cessé de trouver quoi que ce soit. Il lit désormais
  `check --json`, qui porte un `schema`, et cette lecture vit dans
  `scripts/verdict_check.py`, **identique dans les douze catalogues**.

- **Trois verdicts, pas deux.** Une exécution dont tous les tests collectés ont
  skippé n'a rien mesuré : elle est **SKIP**, ni verte ni rouge, et reste à
  mesurer. La peindre en rouge accuserait le lab de ce qui manque au poste.
  `--check` sort donc en `10` dans ce cas, contre `1` pour un ROUGE, à l'image
  de `dsoxlab doctor --strict` où 9 se répare et 10 se remesure.

- **Le README prend la structure de référence** commune aux douze catalogues :
  quatorze sections, dans les deux langues. Sept d'entre elles décrivent
  dsoxlab et non le sujet, et sont donc identiques partout.

### Exige

- **dsoxlab 0.4.1 ou plus récent**, qui a introduit le champ `status` de
  `check --json`. Sans lui, le validateur refuse de conclure plutôt que de
  deviner.

### En propre

- la borne de version du moteur est déclarée dans la CI et dans le hook de pre-push.

## [0.1.1] - 2026-10-14

### Corrigé

- « Feint » prend une majuscule dans les titres des labs de réseau privé,
  dans les deux langues.
- Deux labs réattestés avec la dsoxlab 0.3.5.

### Modifié

- La procédure de release réatteste les labs modifiés depuis leur verdict.

## [0.1.0] - 2026-10-12

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
[0.1.1]: https://github.com/stephrobert/cloud-dsoxlab-training/releases/tag/v0.1.1
