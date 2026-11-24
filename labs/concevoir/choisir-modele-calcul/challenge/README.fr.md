# L'indexeur surdimensionné

## La situation

L'indexeur d'images produit tourne en continu et traite des requêtes HTTP de
longue durée. La machine actuelle semble plus grande que nécessaire au vu des
mesures, mais l'équipe n'a vérifié ni la limite de durée des fonctions, ni la
dépendance au noyau, ni la compatibilité processeur, ni la mémoire au 95e
centile sur une semaine.

Un scénario indique **où l'on en est et ce qui ne va pas**, pas la marche à
suivre : c'est à l'apprenant de trouver cette dernière.

## Mission

À partir de `workload.json`, créez `compute-decision.json`. Consignez le modèle
de calcul, l'architecture processeur, le profil de machine, la demande mesurée
utilisée pour le dimensionnement et une justification courte. Le brief fournit
une semaine complète de mesures, dont un maximum bref à ne pas confondre avec
une charge soutenue.

Compétence visée : `cloud.compute.choose`

## Choisir et dimensionner un modèle de calcul

Lisez `workload.json` et créez `compute-decision.json` dans le répertoire de
travail (`challenge/work/`). Consignez le modèle, l'architecture processeur, le profil de machine
retenu, la demande utilisée pour le dimensionnement et une justification courte.

Utilisez cette forme (les valeurs entre chevrons sont à trouver) :

```json
{
  "compute_model": "<virtual_machine | managed_container | function>",
  "architecture": "<architecture processeur>",
  "machine_profile": "<un id de machine_catalogue>",
  "sizing_demand": {
    "cpu_vcpus": <nombre>,
    "memory_gib": <nombre>
  },
  "rationale": "<pourquoi ce modèle, cette architecture et cette taille>"
}
```

Le brief contient une semaine complète de mesures, dont un maximum bref qui n'a
duré que quelques secondes. Les unités de coût relatives sont des données
d'exercice, pas des prix de fournisseur.

Lancez `dsoxlab check choisir-modele-calcul` pour voir le résultat.
