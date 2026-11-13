# Défi : concevoir le modèle d'accès

Créez `access-model.json` dans `challenge/work/` à partir des exigences de `access-context.json`.
Décrivez la source des identités humaines et la fédération, la durée de
session, les comptes de secours, les groupes de rôles et leurs droits, la
séparation des responsabilités, les responsables du cycle de vie et les
exigences du journal d'audit.

Votre conception reste indépendante du fournisseur. N'y incluez ni nom
d'utilisateur réel, ni identifiant, ni syntaxe de politique propre à un cloud.

Les tests inspectent le modèle produit. Ils ne prouvent pas qu'un service IAM
réel l'applique.

Le JSON contient `human_identity`, `emergency_access`, `role_groups`,
`separation_of_duties`, `lifecycle` et `audit`, sous cette forme (les valeurs
entre chevrons sont à déduire de `access-context.json`) :

```json
{
  "human_identity": {
    "source": "<…>",
    "federation_protocol": "<…>",
    "single_sign_on": <true | false>,
    "maximum_session_minutes": <…>
  },
  "emergency_access": {
    "accounts": [
      {"named_owner": "<…>", "mfa": <…>, "routine_use": <…>, "alert_on_use": <…>}
    ]
  },
  "role_groups": [
    {"name": "<…>", "duties": ["<…>"]}
  ],
  "separation_of_duties": {
    "approval_and_production_deployment_use_distinct_people": <…>,
    "production_access_is_temporary": <…>
  },
  "lifecycle": [
    {"event": "<…>", "owner": "<…>", "maximum_completion_hours": <…>, "interval_days": <… pour un événement périodique>}
  ],
  "audit": {
    "events": ["<…>"],
    "retention_days": <…>,
    "immutable_destination": <…>,
    "destination_owner": "<…>",
    "readers": ["<…>"],
    "alert_on": ["<…>"]
  }
}
```
