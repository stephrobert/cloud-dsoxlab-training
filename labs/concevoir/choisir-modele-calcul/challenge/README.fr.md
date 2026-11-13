# Challenge : choisir et dimensionner un modèle de calcul

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
