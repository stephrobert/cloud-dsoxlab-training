# Challenge : estimer un coût cloud mensuel

Lisez `architecture.json` et créez `cost-estimate.json` dans le répertoire de
travail (`challenge/work/`). Utilisez la grille datée et les usages mensuels fournis ; ne recherchez
pas de prix en direct et n'inventez pas de poste absent des données.

Présentez une ligne par classe de calcul, puis pour le stockage bloc, le
stockage objet, les snapshots, l'egress facturable et les requêtes API. Chaque
ligne indique son identifiant, la quantité facturée, l'unité, le prix unitaire
en EUR et le coût mensuel. Indiquez aussi le total mensuel, le total annualisé,
le budget, le budget restant et si l'estimation le respecte.

Utilisez 730 heures pour le mois standard. Déduisez la franchise d'egress avant
de tarifer le trafic sortant. Les prix de l'exercice sont synthétiques et ne
sont pas ceux d'un fournisseur ; le résultat est une estimation, pas une
facture.

Utilisez cette forme JSON (les valeurs entre chevrons sont à calculer) :

```json
{
  "currency": "<…>",
  "price_grid_as_of": "<…>",
  "line_items": [
    {"id": "<id>", "quantity": <…>, "unit": "<unit>", "unit_price_eur": <…>, "monthly_cost_eur": <…>}
  ],
  "total_monthly_eur": <…>,
  "annualized_eur": <…>,
  "monthly_budget_eur": <…>,
  "budget_remaining_eur": <…>,
  "within_budget": <true | false>
}
```

Identifiants et unités des lignes : `compute-<classe>` en `instance-hour` (une
ligne par classe de calcul), `block-storage`, `object-storage` et
`snapshot-storage` en `GiB-month`, `egress` en `GiB`, `api-requests` en
`million requests`.

Lancez `dsoxlab check estimer-cout-mensuel` pour consulter le résultat.
