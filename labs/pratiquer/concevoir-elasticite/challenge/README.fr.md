# Challenge : concevoir un tier applicatif élastique

Lisez `workload.json` et créez `elasticity-plan.json` dans le répertoire de
travail. Utilisez uniquement les mesures et contraintes fournies.

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

L'exercice porte sur la conception, pas sur un déploiement ni un test de panne
en direct. Lancez `dsoxlab check concevoir-elasticite` pour consulter le
résultat.
