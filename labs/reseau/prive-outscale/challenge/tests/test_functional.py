"""Tests fonctionnels du lab « Réseau privé » (Outscale, sur feint).

Tout est lu dans feint par l'API publique d'Outscale (`ReadNets`, `ReadSubnets`,
`ReadVms`, `ReadRouteTables`...), celle qu'appelle `octl`. Aucun test ne lit les
commandes tapées. Comme pour la variante Scaleway, feint prouve l'existence
des ressources et de leurs liens, pas la sortie réseau : il n'achemine aucun
paquet.

Faits mesurés le 2026-10-12, feint v0.13.0 (image épinglée par digest), octl
v0.0.32 :

- le Net est régional, le sous-réseau est lié à UNE sous-région
  (`SubregionName`) : un réseau multi-zones se construit avec un sous-réseau
  par sous-région ;
- `CreateVms` dans un sous-réseau privé rend `PublicIp: null` et une IP privée
  du sous-réseau (`10.20.1.4`, `10.20.2.4`) ;
- `octl iaas api <Action> --output json` déballe l'enveloppe : un objet pour
  une création, une liste pour une lecture. L'API brute, elle, renvoie
  `{"Vms": [...], "ResponseContext": {...}}` : les tests lisent cette forme-là ;
- chaque Net reçoit une table de routage principale, liée à aucun sous-réseau
  explicitement, portant la seule route `local`.
"""

from __future__ import annotations

import pytest

from conftest import exiger_workdir, message, osc_call, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "reseau-prive-outscale"

NOM_NET = "boutique-net"
PLAGE_NET = "10.20.0.0/16"
SOUS_RESEAUX = {
    "public": ("10.20.0.0/24", "eu-west-2a"),
    "prive-a": ("10.20.1.0/24", "eu-west-2a"),
    "prive-b": ("10.20.2.0/24", "eu-west-2b"),
}
VMS = {"boutique-app-1": "prive-a", "boutique-app-2": "prive-b"}


@pytest.fixture(scope="module", autouse=True)
def _lab_joue() -> None:
    exiger_workdir(WORKDIR, LAB_ID)


def _nom(objet: dict) -> str | None:
    for tag in objet.get("Tags") or []:
        if tag.get("Key") == "Name":
            return tag.get("Value")
    return None


@pytest.fixture(scope="module")
def net() -> dict:
    nets = [n for n in osc_call("ReadNets").get("Nets") or [] if _nom(n) == NOM_NET]
    assert len(nets) == 1, message(
        en=f"{len(nets)} Net carrying the tag Name={NOM_NET}: a single one is expected.",
        fr=f"{len(nets)} Net portant le tag Name={NOM_NET} : un seul est attendu.",
    )
    return nets[0]


@pytest.fixture(scope="module")
def sous_reseaux(net: dict) -> dict[str, dict]:
    tous = [s for s in osc_call("ReadSubnets").get("Subnets") or [] if s.get("NetId") == net["NetId"]]
    trouves: dict[str, dict] = {}
    for role, (plage, sous_region) in SOUS_RESEAUX.items():
        candidats = [s for s in tous if s.get("IpRange") == plage]
        assert candidats, message(
            en=f"No subnet {plage} in {NOM_NET}.",
            fr=f"Aucun sous-réseau {plage} dans {NOM_NET}.",
        )
        assert candidats[0].get("SubregionName") == sous_region, message(
            en=f"The subnet {plage} is in {candidats[0].get('SubregionName')}, "
            f"{sous_region} expected.",
            fr=f"Le sous-réseau {plage} est en {candidats[0].get('SubregionName')}, "
            f"{sous_region} attendu.",
        )
        trouves[role] = candidats[0]
    return trouves


def _tables(net: dict) -> list[dict]:
    return [
        t for t in osc_call("ReadRouteTables").get("RouteTables") or []
        if t.get("NetId") == net["NetId"]
    ]


def _table_du_sous_reseau(net: dict, subnet_id: str) -> dict | None:
    for table in _tables(net):
        if any(lien.get("SubnetId") == subnet_id for lien in table.get("LinkRouteTables") or []):
            return table
    return None


def _route_par_defaut(table: dict | None) -> dict | None:
    if table is None:
        return None
    for route in table.get("Routes") or []:
        if route.get("DestinationIpRange") == "0.0.0.0/0":
            return route
    return None


def test_net_regional_et_un_sous_reseau_par_sous_region(net: dict, sous_reseaux: dict) -> None:
    """Le Net sur son plan, et ses trois sous-réseaux dans leurs sous-régions."""
    assert net.get("IpRange") == PLAGE_NET, message(
        en=f"{NOM_NET} covers {net.get('IpRange')}, {PLAGE_NET} expected.",
        fr=f"{NOM_NET} couvre {net.get('IpRange')}, {PLAGE_NET} attendu.",
    )
    assert len(sous_reseaux) == len(SOUS_RESEAUX), message(
        en=f"{len(sous_reseaux)} subnet(s) found, {len(SOUS_RESEAUX)} expected: "
        "one per role, each in its own subregion.",
        fr=f"{len(sous_reseaux)} sous-réseau(x) trouvé(s), {len(SOUS_RESEAUX)} "
        "attendu(s) : un par rôle, chacun dans sa sous-région.",
    )


def test_deux_vms_dans_deux_sous_regions_sans_ip_publique(sous_reseaux: dict) -> None:
    """Une VM par sous-réseau privé, aucune adresse publique."""
    vms = osc_call("ReadVms").get("Vms") or []
    for nom, role in VMS.items():
        trouvees = [v for v in vms if _nom(v) == nom and v.get("State") != "terminated"]
        assert len(trouvees) == 1, message(
            en=f"{len(trouvees)} VMs carrying the tag Name={nom}: a single one is expected.",
            fr=f"{len(trouvees)} VM portant le tag Name={nom} : une seule est attendue.",
        )
        vm = trouvees[0]
        attendu = sous_reseaux[role]
        assert vm.get("SubnetId") == attendu["SubnetId"], message(
            en=f"{nom} is not in the subnet {attendu['IpRange']}.",
            fr=f"{nom} n'est pas dans le sous-réseau {attendu['IpRange']}.",
        )
        assert not vm.get("PublicIp"), message(
            en=f"{nom} carries the public IP {vm.get('PublicIp')}: nothing exposed before "
            "the private network.",
            fr=f"{nom} porte l'IP publique {vm.get('PublicIp')} : rien d'exposé avant "
            "le réseau privé.",
        )


def test_internet_service_lie_et_route_publique(net: dict, sous_reseaux: dict) -> None:
    """Le sous-réseau public sort par l'Internet Service lié au Net."""
    services = [
        s for s in osc_call("ReadInternetServices").get("InternetServices") or []
        if s.get("NetId") == net["NetId"]
    ]
    assert services, message(
        en=f"No Internet Service linked to {NOM_NET} (LinkInternetService).",
        fr=f"Aucun Internet Service lié à {NOM_NET} (LinkInternetService).",
    )
    route = _route_par_defaut(_table_du_sous_reseau(net, sous_reseaux["public"]["SubnetId"]))
    assert route and route.get("GatewayId") == services[0]["InternetServiceId"], message(
        en="The public subnet has no 0.0.0.0/0 route to the Internet Service: "
        "a route table linked to that subnet must carry it.",
        fr="Le sous-réseau public n'a pas de route 0.0.0.0/0 vers l'Internet Service : "
        "une table de routage liée à ce sous-réseau doit la porter.",
    )


def test_nat_service_dans_le_sous_reseau_public(sous_reseaux: dict) -> None:
    """Le NAT Service vit dans le sous-réseau public, avec son IP publique."""
    nats = [
        n for n in osc_call("ReadNatServices").get("NatServices") or []
        if n.get("SubnetId") == sous_reseaux["public"]["SubnetId"]
    ]
    assert nats, message(
        en="No NAT Service in the public subnet 10.20.0.0/24.",
        fr="Aucun NAT Service dans le sous-réseau public 10.20.0.0/24.",
    )
    assert nats[0].get("State") == "available", message(
        en=f"The NAT Service is {nats[0].get('State')!r}, `available` expected: "
        "as long as it is not, the private subnets have no path out.",
        fr=f"Le NAT Service est en {nats[0].get('State')!r}, `available` attendu : "
        "tant qu'il ne l'est pas, les sous-réseaux privés n'ont aucun chemin vers "
        "l'extérieur.",
    )
    assert nats[0].get("PublicIps"), message(
        en="The NAT Service has no public IP.",
        fr="Le NAT Service n'a pas d'IP publique.",
    )


def test_sous_reseaux_prives_sortent_par_le_nat(net: dict, sous_reseaux: dict) -> None:
    """Les deux sous-réseaux privés ont leur route par défaut vers le NAT Service."""
    nats = {
        n["NatServiceId"]
        for n in osc_call("ReadNatServices").get("NatServices") or []
        if n.get("SubnetId") == sous_reseaux["public"]["SubnetId"]
    }
    for role in ("prive-a", "prive-b"):
        route = _route_par_defaut(_table_du_sous_reseau(net, sous_reseaux[role]["SubnetId"]))
        assert route and route.get("NatServiceId") in nats, message(
            en=f"The subnet {sous_reseaux[role]['IpRange']} has no "
            "0.0.0.0/0 route to the NAT Service of the public subnet.",
            fr=f"Le sous-réseau {sous_reseaux[role]['IpRange']} n'a pas de route "
            "0.0.0.0/0 vers le NAT Service du sous-réseau public.",
        )
