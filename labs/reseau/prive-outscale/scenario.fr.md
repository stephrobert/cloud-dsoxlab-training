# Scénario : le même réseau, chez un autre fournisseur

**Compétence visée : `cloud.network.design`.**

La boutique veut garder une porte de sortie : son réseau privé doit pouvoir se
déclarer chez Outscale comme chez Scaleway. Le besoin ne change pas : deux
zones, aucune adresse publique sur les machines, une seule sortie contrôlée
vers Internet. Le modèle, lui, change : chez Outscale, un sous-réseau vit dans
une seule sous-région, et la sortie passe par un NAT Service et des tables de
routage que vous liez vous-même.

Le plan est arrêté (`PLAN.md`). Vous partez d'un émulateur vide et du CLI
`octl` pointé sur lui. Aucune ressource n'existe encore.
