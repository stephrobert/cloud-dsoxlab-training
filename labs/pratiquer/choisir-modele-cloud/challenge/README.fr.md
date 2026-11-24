# Une équipe produit choisit son modèle cloud

## La situation

L'équipe produit migre une API destinée à ses clients vers le cloud. Elle sait
maintenir son application, mais ne dispose pas d'équipe d'exploitation dédiée.
L'API ne dépend ni d'un noyau ni d'un système d'exploitation particulier, traite
des données personnelles et doit rester sous le contrôle de l'équipe pour les
identités et la configuration applicative.

Un scénario dit **où on est et ce qui ne va pas**, pas la marche à suivre :
c'est le travail de l'apprenant de la trouver.

Les contraintes et le workload sont résumés dans `brief.json`. La proposition
actuelle ne nomme qu'un fournisseur cloud, sans préciser le modèle de service,
le modèle de déploiement ni le partage des responsabilités de sécurité.

Compétence visée : `cloud.model.choose`

## Défi : choisir le modèle cloud

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
