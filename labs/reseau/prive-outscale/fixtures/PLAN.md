# Plan réseau de la boutique, Outscale / Shop network plan, Outscale

| Ressource / Resource | Tag `Name` | Où / Where | Valeur / Value |
| --- | --- | --- | --- |
| Net | `boutique-net` | région / Region `eu-west-2` | `10.20.0.0/16` |
| Subnet public | | `eu-west-2a` | `10.20.0.0/24` (NAT Service) |
| Subnet privé / private | | `eu-west-2a` | `10.20.1.0/24` |
| Subnet privé / private | | `eu-west-2b` | `10.20.2.0/24` |
| VM | `boutique-app-1` | subnet `10.20.1.0/24` | sans IP publique / no public IP |
| VM | `boutique-app-2` | subnet `10.20.2.0/24` | sans IP publique / no public IP |
| Internet Service | | lié au Net / linked to the Net | |
| NAT Service | | subnet public | une IP publique / one public IP |
| Route table publique / public | | subnet public | `0.0.0.0/0` vers / to Internet Service |
| Route table privée / private | | les deux subnets privés / both private subnets | `0.0.0.0/0` vers / to NAT Service |
