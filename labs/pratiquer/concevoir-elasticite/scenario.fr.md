# Préparer la plateforme client à une charge variable

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
