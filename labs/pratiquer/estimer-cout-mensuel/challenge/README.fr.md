# Challenge : estimer un coût cloud mensuel

Lisez `architecture.json` et créez `cost-estimate.json` dans le répertoire de
travail. Utilisez la grille datée et les usages mensuels fournis ; ne recherchez
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

Lancez `dsoxlab check estimer-cout-mensuel` pour consulter le résultat.
