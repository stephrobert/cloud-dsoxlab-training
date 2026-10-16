"""Tests fonctionnels du lab « Réseau privé » (Scaleway, sur feint).

Tout est lu dans feint par l'API publique de Scaleway, celle que le CLI `scw`
emploie lui-même : VPC, Private Network, instances, NIC privées, passerelle et
son attachement. Aucun test ne lit les commandes tapées.

Ce que ces tests prouvent, et ce qu'ils ne prouvent pas : feint n'applique ni
routage ni NAT (« nothing forwards a packet »). Les tests établissent que les
ressources et leurs LIENS existent, pas qu'une instance sort réellement sur
Internet.

Faits mesurés le 2026-10-12, feint v0.13.0 (image épinglée par digest), scw
2.62.0 :

- le VPC et le Private Network sont régionaux (`region: fr-par`, aucun champ de
  zone), et feint ajoute de lui-même un sous-réseau IPv6 en /64 ;
- `scw instance server create ... ip=none` donne `public_ip: null` et
  `public_ips: []` ;
- le même Private Network s'attache à une instance de fr-par-1 et à une de
  fr-par-2, chacune par sa NIC privée zonale ;
- `gateway-network create ... enable-masquerade=true push-default-route=true`
  rend `enable_masquerade: null` dans la réponse de création, mais la lecture
  (`GET .../gateway-networks`) porte bien `masquerade_enabled: true`.
"""

from __future__ import annotations

import ipaddress

import pytest

from conftest import exiger_workdir, message, scw_get, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "reseau-prive-scaleway"

REGION = "fr-par"
VPC = "boutique-vpc"
RESEAU = "boutique-prive"
SOUS_RESEAU = ipaddress.ip_network("10.42.1.0/24")
INSTANCES = {"boutique-app-1": "fr-par-1", "boutique-app-2": "fr-par-2"}
PASSERELLE = "boutique-gw"
ZONE_PASSERELLE = "fr-par-1"


@pytest.fixture(scope="module", autouse=True)
def _lab_joue() -> None:
    exiger_workdir(WORKDIR, LAB_ID)


def _un_seul(objets: list[dict], nom: str, genre: str) -> dict:
    trouves = [o for o in objets if o.get("name") == nom]
    assert trouves, message(
        en=f"No {genre} named {nom} in feint.",
        fr=f"Aucun {genre} nommé {nom} dans feint.",
    )
    assert len(trouves) == 1, message(
        en=f"{len(trouves)} {genre}s named {nom}: a single one is expected. Delete "
        "the duplicates from an earlier attempt.",
        fr=f"{len(trouves)} {genre}s nommés {nom} : un seul est attendu. Supprimez "
        "les doublons d'un essai précédent.",
    )
    return trouves[0]


def _vpc() -> dict:
    return _un_seul(scw_get(f"/vpc/v2/regions/{REGION}/vpcs")["vpcs"], VPC, "VPC")


def _reseau() -> dict:
    reseaux = scw_get(f"/vpc/v2/regions/{REGION}/private-networks")["private_networks"]
    return _un_seul(reseaux, RESEAU, "Private Network")


def _serveurs() -> dict[str, dict]:
    trouves: dict[str, dict] = {}
    for nom, zone in INSTANCES.items():
        serveurs = scw_get(f"/instance/v1/zones/{zone}/servers")["servers"]
        trouves[nom] = _un_seul(serveurs, nom, f"serveur en {zone}")
    return trouves


def _passerelle() -> dict:
    passerelles = scw_get(f"/vpc-gw/v2/zones/{ZONE_PASSERELLE}/gateways")["gateways"]
    return _un_seul(passerelles, PASSERELLE, f"Public Gateway en {ZONE_PASSERELLE}")


def test_vpc_et_reseau_prive_regionaux() -> None:
    """Un VPC, un Private Network régional dans ce VPC, sur le plan d'adressage."""
    vpc = _vpc()
    reseau = _reseau()
    assert reseau.get("vpc_id") == vpc["id"], message(
        en=f"{RESEAU} does not belong to {VPC}: create it with vpc-id=<id of {VPC}>.",
        fr=f"{RESEAU} n'appartient pas à {VPC} : créez-le avec vpc-id=<id de {VPC}>.",
    )
    assert reseau.get("region") == REGION, message(
        en=f"{RESEAU} is in {reseau.get('region')}.",
        fr=f"{RESEAU} est en {reseau.get('region')}.",
    )
    ipv4 = [
        ipaddress.ip_network(s["subnet"])
        for s in reseau.get("subnets") or []
        if ipaddress.ip_network(s["subnet"]).version == 4
    ]
    assert ipv4 == [SOUS_RESEAU], message(
        en=f"IPv4 subnets of {RESEAU}: {[str(s) for s in ipv4]}. The plan "
        f"asks for {SOUS_RESEAU} and it alone.",
        fr=f"Sous-réseaux IPv4 de {RESEAU} : {[str(s) for s in ipv4]}. Le plan "
        f"demande {SOUS_RESEAU} et lui seul.",
    )


def test_deux_instances_dans_deux_zones_sans_ip_publique() -> None:
    """Une instance par zone, aucune adresse publique."""
    for nom, serveur in _serveurs().items():
        assert serveur.get("zone") == INSTANCES[nom], message(
            en=f"{nom} is in {serveur.get('zone')}, {INSTANCES[nom]} expected.",
            fr=f"{nom} est en {serveur.get('zone')}, {INSTANCES[nom]} attendu.",
        )
        assert serveur.get("public_ip") is None and not serveur.get("public_ips"), message(
            en=f"{nom} carries a public address ({serveur.get('public_ip') or serveur.get('public_ips')}). "
            "Create the instance with ip=none: nothing exposed before the private network.",
            fr=f"{nom} porte une adresse publique ({serveur.get('public_ip') or serveur.get('public_ips')}). "
            "Créez l'instance avec ip=none : rien d'exposé avant le réseau privé.",
        )


def test_le_meme_reseau_prive_attache_dans_chaque_zone() -> None:
    """Un réseau régional, des attachements zonaux : une NIC privée par instance."""
    reseau = _reseau()
    for nom, serveur in _serveurs().items():
        zone = INSTANCES[nom]
        nics = scw_get(f"/instance/v1/zones/{zone}/servers/{serveur['id']}/private_nics")[
            "private_nics"
        ]
        sur_le_reseau = [n for n in nics if n.get("private_network_id") == reseau["id"]]
        assert sur_le_reseau, message(
            en=f"{nom} has no private NIC on {RESEAU}. A NIC is created per zone: "
            f"scw instance private-nic create … zone={zone}.",
            fr=f"{nom} n'a aucune NIC privée sur {RESEAU}. Une NIC se crée par zone : "
            f"scw instance private-nic create ... zone={zone}.",
        )
        assert sur_le_reseau[0].get("zone") == zone, message(
        en=f"The private NIC of {nom} is in {sur_le_reseau[0].get('zone')}, "
        f"{zone} expected: a NIC is created in the instance's own zone.",
        fr=f"La NIC privée de {nom} est en {sur_le_reseau[0].get('zone')}, "
        f"{zone} attendu : une NIC se crée dans la zone de son instance.",
    )


def test_passerelle_publique_avec_son_ip() -> None:
    """La Public Gateway existe, dans sa zone, avec son IP."""
    passerelle = _passerelle()
    assert passerelle.get("type") == "VPC-GW-S", message(
        en=f"{PASSERELLE} is of type {passerelle.get('type')}, VPC-GW-S expected.",
        fr=f"{PASSERELLE} est de type {passerelle.get('type')}, VPC-GW-S attendu.",
    )
    assert (passerelle.get("ipv4") or {}).get("address"), message(
        en=f"{PASSERELLE} has no IP: a Public Gateway requires one.",
        fr=f"{PASSERELLE} n'a pas d'IP : une Public Gateway en exige une.",
    )


def test_passerelle_reliee_avec_route_par_defaut_et_nat() -> None:
    """Le gateway-network relie la passerelle au réseau et pousse la route par défaut."""
    passerelle = _passerelle()
    reseau = _reseau()
    liaisons = scw_get(f"/vpc-gw/v2/zones/{ZONE_PASSERELLE}/gateway-networks")[
        "gateway_networks"
    ]
    liaison = [
        g
        for g in liaisons
        if g.get("gateway_id") == passerelle["id"]
        and g.get("private_network_id") == reseau["id"]
    ]
    assert liaison, message(
        en=f"No gateway-network links {PASSERELLE} to {RESEAU}.",
        fr=f"Aucun gateway-network ne relie {PASSERELLE} à {RESEAU}.",
    )
    assert liaison[0].get("push_default_route") is True, message(
        en="The link does not push the default route: without it, the instances "
        "with no public IP have no path to the outside.",
        fr="La liaison ne pousse pas la route par défaut : sans elle, les instances "
        "sans IP publique n'ont aucun chemin vers l'extérieur.",
    )
    assert liaison[0].get("masquerade_enabled") is True, message(
        en="NAT (masquerade) is not enabled on the link.",
        fr="Le NAT (masquerade) n'est pas activé sur la liaison.",
    )
