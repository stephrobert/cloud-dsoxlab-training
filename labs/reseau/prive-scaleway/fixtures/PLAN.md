# Plan réseau de la boutique / Shop network plan

| Ressource / Resource | Nom / Name | Où / Where | Valeur / Value |
| --- | --- | --- | --- |
| VPC | `boutique-vpc` | région / region `fr-par` | |
| Private Network | `boutique-prive` | région / region `fr-par` | `10.42.1.0/24` |
| Instance | `boutique-app-1` | zone `fr-par-1` | `DEV1-S`, `ubuntu_noble`, sans IP publique / no public IP |
| Instance | `boutique-app-2` | zone `fr-par-2` | `DEV1-S`, `ubuntu_noble`, sans IP publique / no public IP |
| Public Gateway | `boutique-gw` | zone `fr-par-1` | type `VPC-GW-S`, une IP / one IP |
| Gateway Network | | zone `fr-par-1` | route par défaut poussée / default route pushed, NAT |
