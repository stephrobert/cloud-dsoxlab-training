# Défi : choisir le modèle cloud

Lisez `brief.json` et créez `decision.json` dans le répertoire de travail (`challenge/work/`).
Indiquez le modèle de service, le modèle de déploiement et les responsabilités
de sécurité du fournisseur et de l'équipe qui découlent du brief.

Utilisez cette forme JSON (les valeurs entre chevrons sont à choisir) :

```json
{
  "service_model": "<iaas | paas | saas>",
  "deployment_model": "<public | private | hybrid>",
  "responsibilities": {
    "provider": ["<responsabilité>", "…"],
    "team": ["<responsabilité>", "…"]
  },
  "rationale": "<une explication courte, rattachée au brief>"
}
```

Les responsabilités se nomment dans cette liste : `hardware`, `network`,
`operating_system`, `managed_platform`, `application`, `data`, `identities`,
`configuration`.

L'ordre des responsabilités n'a pas d'importance. La note porte sur le contenu
obtenu, pas sur les commandes utilisées pour créer le fichier.

Lancez `dsoxlab check pratiquer-choisir-modele-cloud` pour voir le résultat.
