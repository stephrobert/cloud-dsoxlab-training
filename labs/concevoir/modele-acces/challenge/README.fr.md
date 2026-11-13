# Défi : concevoir le modèle d'accès

Créez `access-model.json` à partir des exigences de `access-context.json`.
Décrivez la source des identités humaines et la fédération, la durée de
session, les comptes de secours, les groupes de rôles et leurs droits, la
séparation des responsabilités, les responsables du cycle de vie et les
exigences du journal d'audit.

Votre conception reste indépendante du fournisseur. N'y incluez ni nom
d'utilisateur réel, ni identifiant, ni syntaxe de politique propre à un cloud.

Les tests inspectent le modèle produit. Ils ne prouvent pas qu'un service IAM
réel l'applique.

Le JSON contient `human_identity`, `emergency_access`, `role_groups`,
`separation_of_duties`, `lifecycle` et `audit`.

```json
{
  "human_identity": {
    "source": "corporate-directory",
    "federation_protocol": "OIDC",
    "single_sign_on": true,
    "maximum_session_minutes": 60
  },
  "emergency_access": {
    "accounts": [
      {"named_owner": "Security lead A", "mfa": true, "routine_use": false, "alert_on_use": true},
      {"named_owner": "Security lead B", "mfa": true, "routine_use": false, "alert_on_use": true}
    ]
  },
  "role_groups": [
    {"name": "developers", "duties": ["read_nonproduction", "deploy_nonproduction"]},
    {"name": "production_operators", "duties": ["approve_production_change", "deploy_production"]},
    {"name": "security_auditors", "duties": ["read_audit_events", "review_access"]}
  ],
  "separation_of_duties": {
    "approval_and_production_deployment_use_distinct_people": true,
    "production_access_is_temporary": true
  },
  "lifecycle": [
    {"event": "joiner", "owner": "People operations", "maximum_completion_hours": 24},
    {"event": "mover", "owner": "Access owner", "maximum_completion_hours": 8},
    {"event": "leaver", "owner": "People operations", "maximum_completion_hours": 4},
    {"event": "recertification", "owner": "Role owner", "maximum_completion_hours": 24, "interval_days": 90}
  ],
  "audit": {
    "events": ["authentication", "privilege_change", "production_access", "policy_denial"],
    "retention_days": 365,
    "immutable_destination": true,
    "destination_owner": "Security operations",
    "readers": ["security_auditors"],
    "alert_on": ["break_glass_use", "privilege_escalation", "audit_delivery_failure"]
  }
}
```
