# Défi : recommander et planifier les évolutions d'architecture

À partir des preuves de `review.json`, créez `plan.json`. Ajoutez une
recommandation par constat, avec son score de risque, son effort, son effet
attendu, son critère de vérification mesurable, son coût mensuel, son risque
résiduel et ses dépendances.

Classez les recommandations par score de risque décroissant. Une action qui
demande au plus un jour-personne est un `quick_win`, les autres sont
`structural`.

Planifiez tous les travaux par sprint. La charge d'un sprint ne doit pas
dépasser la capacité de l'équipe et une recommandation ne peut commencer avant
la fin de ses dépendances. Nommez un responsable qui accepte chaque risque
résiduel.

Le format attendu est décrit dans `challenge/README.md`. La note porte sur le
contenu produit, pas sur les commandes utilisées.
