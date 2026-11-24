# Préparer la plateforme client à une charge variable

## La situation

La plateforme client tourne actuellement sur trois instances applicatives
identiques. Le pic soutenu mesuré atteint 1 500 requêtes par seconde, et
chaque instance supporte sans dépasser l'objectif de latence au p95 une
capacité testée de 800 requêtes par seconde. La perte d'une instance ne doit
pas faire dépasser cette capacité aux instances restantes.

L'application stocke aujourd'hui les sessions et les fichiers téléversés sur
son disque local. L'équipe veut ajouter et retirer des instances sans changer
le code applicatif ; une nouvelle tentative du client après la perte d'une
instance ne doit pas créer deux commandes. À partir de la fixture, rédigez un
plan d'élasticité qui précise le stockage d'état, la sûreté des nouvelles
tentatives, les contrôles de santé et de disponibilité, les bornes de réplicas,
le calcul après perte d'une instance, et les gestes de scale-out et de scale-in.

La fixture est une mesure d'exercice, pas une garantie fournisseur. Aucun
service n'est déployé et aucune panne ou opération d'autoscaling réelle n'est
revendiquée.

Compétence visée : `cloud.elasticity.design`

## Concevoir un tier applicatif élastique

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
