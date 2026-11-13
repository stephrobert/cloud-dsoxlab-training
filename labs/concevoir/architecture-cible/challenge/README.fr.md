# Défi : décider de l'architecture cible

Lisez `brief.json` et écrivez `decision.json` dans le répertoire de travail (`challenge/work/`).
Comparez les deux options complètes selon les six axes fournis, retenez celle
qui respecte toutes les exigences impératives et consignez la décision sous
forme d'ADR.

Utilisez cette structure :

```json
{
  "comparison": {
    "virtual_machines": {
      "monthly_cost_eur": 1250,
      "operations_days_per_month": 3,
      "data_residency": "eu",
      "availability_zones": 3,
      "portability": "...",
      "performance": "..."
    },
    "managed_containers": {}
  },
  "adr": {
    "title": "Architecture cible du portail client",
    "context": "Résumez le workload et les contraintes impératives.",
    "options_considered": ["virtual_machines", "managed_containers"],
    "criteria": ["monthly_cost_eur", "operations_days_per_month", "data_residency", "availability_zones", "portability", "performance"],
    "decision": "<l'option retenue>",
    "rationale": "Justifiez la décision au regard des exigences.",
    "consequences": ["Consignez une conséquence opérationnelle ou technique."],
    "accepted_risks": ["Nommez un risque résiduel et sa mesure de réduction."],
    "review_condition": "Précisez quelle preuve conduirait à réexaminer la décision."
  }
}
```

L'objet de comparaison doit contenir les deux options et les six axes. L'ordre
des clés JSON n'a pas d'importance.

Lancez `dsoxlab check concevoir-architecture-cible` pour voir le résultat.
