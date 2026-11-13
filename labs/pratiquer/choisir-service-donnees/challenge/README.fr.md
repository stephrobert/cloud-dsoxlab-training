# Challenge : choisir un service de données

Lisez `data-service-brief.json` et créez `data-service-decision.json` dans le
répertoire de travail (`challenge/work/`). Comparez chaque option aux contraintes du workload, de
l'équipe, du réseau, de la reprise et du budget.

Consignez le service retenu, le moteur et le mode d'exploitation ; la décision
sur le point de terminaison privé ; la réplication et la bascule ; les
objectifs RPO/RTO ; la restauration à un instant donné ; et la façon dont
l'équipe vérifiera une restauration. Justifiez la décision et donnez à chaque
option écartée son motif.

Utilisez uniquement le catalogue synthétique fourni. Le livrable est une
décision d'architecture, pas un déploiement ni une preuve de bascule réelle.

Utilisez cette forme JSON (les valeurs entre chevrons sont à déduire du brief) :

```json
{
  "service_id": "<un id de service_catalogue>",
  "engine": "<…>",
  "major_version": <…>,
  "operating_model": "<…>",
  "private_endpoint": <true | false>,
  "internet_exposure": <true | false>,
  "replication": "<…>",
  "failure_domains": <…>,
  "rpo_minutes": <…>,
  "rto_minutes": <…>,
  "point_in_time_recovery": <true | false>,
  "restore_test_owner": "<…>",
  "restore_verification": "<comment une restauration est vérifiée>",
  "rationale": "<pourquoi ce service>",
  "comparison": {"<service id>": "<ce qui convient, ou pourquoi il est écarté>"},
  "rejected_options": [{"service_id": "<…>", "reason": "<…>"}]
}
```

Lancez `dsoxlab check choisir-service-donnees` pour consulter le résultat.
