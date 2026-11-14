# Challenge : concevoir un tier applicatif élastique

Lisez `workload.json` et créez `elasticity-plan.json` dans le répertoire de
travail (`challenge/work/`). Utilisez uniquement les mesures et contraintes fournies.

Consignez l'emplacement des sessions, des téléversements et des commandes ;
la prévention des commandes dupliquées lors d'une nouvelle tentative ; les
contrôles de vie et de disponibilité ; le minimum et le maximum de réplicas ;
la capacité de chaque instance ; la demande de pointe restante après la perte
d'une instance ; et la marge de capacité obtenue.

Définissez séparément le scale-out et le scale-in. Précisez métriques, seuils,
fenêtres d'observation, cooldowns et actions. Le scale-in doit drainer les
connexions avant le retrait et ne jamais passer sous le minimum de réplicas.
Indiquez comment vérifier le plan en ajoutant et en retirant une instance,
sans changer le code applicatif.

Utilisez cette forme JSON (les valeurs entre chevrons sont à choisir ou à
calculer) :

```json
{
  "state": {
    "sessions": "<instance_local_memory | sticky_load_balancer | shared_managed_session_store>",
    "uploads": "<instance_local_disk | shared_block_volume | object_storage>",
    "orders": "<où vivent les commandes>",
    "order_retry_protection": "<none | client_side_dedup | idempotency_key>"
  },
  "scale_out_requires_code_change": <true | false>,
  "health_checks": {"liveness": "<…>", "readiness": "<…>"},
  "replicas": {"minimum": <…>, "maximum": <…>},
  "safe_requests_per_second_per_instance": <…>,
  "peak_requests_per_second_after_one_loss": <…>,
  "capacity_after_one_loss_requests_per_second": <…>,
  "capacity_margin_after_one_loss_requests_per_second": <…>,
  "scale_out": {"metric": "per_instance_utilization_percent", "threshold_percent": <…>,
                "window_minutes": <…>, "cooldown_minutes": <…>,
                "action": "<add_one_instance | add_two_instances>"},
  "scale_in": {"metric": "per_instance_utilization_percent", "threshold_percent": <…>,
               "window_minutes": <…>, "cooldown_minutes": <…>,
               "action": "<remove_one_instance | drain_then_remove_one_instance>",
               "connection_drain_seconds": <…>, "never_below_minimum": <true | false>},
  "verification": {"add_instance": "<…>", "lose_instance": "<…>"}
}
```

L'exercice porte sur la conception, pas sur un déploiement ni un test de panne
en direct. Lancez `dsoxlab check concevoir-elasticite` pour consulter le
résultat.
