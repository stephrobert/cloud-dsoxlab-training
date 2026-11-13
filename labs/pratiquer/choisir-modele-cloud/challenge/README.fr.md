# Défi : choisir le modèle cloud

Lisez `brief.json` et créez `decision.json` dans le répertoire de travail.
Indiquez le modèle de service, le modèle de déploiement et les responsabilités
de sécurité du fournisseur et de l'équipe qui découlent du brief.

Utilisez cette structure JSON :

```json
{
  "service_model": "paas",
  "deployment_model": "public",
  "responsibilities": {
    "provider": ["managed_platform"],
    "team": ["application", "data", "identities", "configuration"]
  },
  "rationale": "Une explication concise, liée au brief."
}
```

L'ordre des responsabilités n'a pas d'importance. La note porte sur le contenu
obtenu, pas sur les commandes utilisées pour créer le fichier.

Lancez `dsoxlab check pratiquer-choisir-modele-cloud` pour voir le résultat.
