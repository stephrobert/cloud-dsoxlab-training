# Scénario : l'indexeur surdimensionné

L'indexeur d'images produit tourne en continu et traite des requêtes HTTP de
longue durée. La machine actuelle semble plus grande que nécessaire au vu des
mesures, mais l'équipe n'a vérifié ni la limite de durée des fonctions, ni la
dépendance au noyau, ni la compatibilité processeur, ni la mémoire au 95e
centile sur une semaine.

Un scénario indique **où l'on en est et ce qui ne va pas**, pas la marche à
suivre : c'est à l'apprenant de trouver cette dernière.

## Mission

À partir de `workload.json`, créez `compute-decision.json`. Consignez le modèle
de calcul, l'architecture processeur, le profil de machine, la demande mesurée
utilisée pour le dimensionnement et une justification courte. Le brief fournit
une semaine complète de mesures, dont un maximum bref à ne pas confondre avec
une charge soutenue.

Compétence visée : `cloud.compute.choose`
