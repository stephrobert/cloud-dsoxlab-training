# Un service de données pour la plateforme de commandes

La plateforme de commandes a besoin d'une base relationnelle compatible avec
PostgreSQL. Les commandes doivent conserver leur cohérence transactionnelle ;
l'application utilise l'extension `pgcrypto` et ne doit joindre la base que
par un point de terminaison privé.

Le service doit respecter les objectifs de reprise du dossier. L'équipe
produit n'a pas de DBA et peut consacrer au plus huit heures par mois à
l'exploitation de la base. Choisissez une option du catalogue et consignez le
moteur, le mode d'exploitation, l'accès privé, la réplication, la bascule et le
plan de vérification d'une sauvegarde restaurée.

Le catalogue fourni est une donnée synthétique d'exercice. Ses disponibilités
et ses tarifs ne décrivent aucun fournisseur réel. Le challenge évalue une
décision argumentée, pas un déploiement ni une reprise réellement éprouvée.

Compétence visée : `cloud.data.choose`
