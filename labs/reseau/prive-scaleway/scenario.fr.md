# Scénario : le réseau privé de la boutique

**Compétence visée : `cloud.network.design`.**

La boutique a sa première machine amorcée en local. Avant de déclarer la
moindre instance chez un fournisseur, l'équipe pose une règle : **rien
d'exposé avant le réseau privé**. L'API et son frontal tourneront dans deux
zones de la région `fr-par`, sans adresse publique, et sortiront chercher leurs
mises à jour par une passerelle unique.

Le plan d'adressage est arrêté (`PLAN.md`). Il reste à le déclarer chez
Scaleway, et à le prouver par l'état, avant que la première carte bancaire
n'entre en jeu : c'est le rôle de feint, qui sert la même API sans compte.

Vous partez d'un émulateur vide, du CLI `scw` installé et de l'environnement
qui le pointe sur l'émulateur. Aucune ressource n'existe encore.
