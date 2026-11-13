# Défi : recommander et planifier les évolutions d'architecture

À partir des preuves de `review.json`, créez `plan.json` dans `challenge/work/`. Ajoutez une
recommandation par constat, avec son score de risque, son effort, son effet
attendu, son critère de vérification mesurable, son coût mensuel, son risque
résiduel et ses dépendances.

Classez les recommandations par score de risque décroissant. Une action est un
`quick_win` seulement si elle demande au plus l'effort de gain rapide des
échelles, n'a aucune dépendance et est réversible ; les autres sont
`structural`.

Planifiez tous les travaux par sprint. La charge d'un sprint ne doit pas
dépasser la capacité de l'équipe et une recommandation ne peut commencer avant
la fin de ses dépendances. Nommez un responsable qui accepte chaque risque
résiduel.

Utilisez cette forme JSON (les valeurs entre chevrons sont à déduire de
`review.json`) :

```json
{
  "priority_order": ["<id du constat>", "…"],
  "recommendations": [
    {
      "id": "<id du constat>",
      "risk_score": <nombre>,
      "action": "<un changement vérifiable, pas un nom de produit>",
      "expected_effect": "<l'effet sur le constat>",
      "verification_criterion": "<une condition de réussite observable>",
      "effort_days": <nombre>,
      "monthly_cost_eur": <nombre>,
      "residual_risk": "<ce qui reste vrai après l'action>",
      "dependencies": ["<id du constat>"],
      "kind": "<quick_win | structural>",
      "risk_acceptance": {"owner": "<rôle nommé>", "rationale": "<pourquoi ce risque résiduel est accepté>"}
    }
  ],
  "sprints": [
    {"name": "<nom du sprint>", "items": ["<id du constat>"]}
  ]
}
```

Incluez chaque recommandation et son affectation à un sprint. La note porte sur
le contenu produit, pas sur les commandes utilisées.

Lancez `dsoxlab check concevoir-recommander-evolutions-architecture` pour voir le résultat.
