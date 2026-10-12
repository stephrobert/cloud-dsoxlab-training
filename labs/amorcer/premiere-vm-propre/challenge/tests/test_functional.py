"""Tests fonctionnels du lab « Première VM propre ».

Tout est lu sur l'ÉTAT : la description de l'instance par Incus, puis la
machine elle-même par testinfra (`incus exec`). Aucun test ne lit l'historique
du shell ni ne rejoue une commande de l'apprenant.

Faits mesurés le 2026-10-12, Incus 7.2, image `images:ubuntu/noble/cloud` en
machine virtuelle (`--vm`) :

- la machine démarre et cloud-init rend `status: done` en 44 secondes environ,
  image déjà en cache ; le premier tirage de l'image s'y ajoute ;
- la clé `cloud-init.user-data` de l'instance porte, octet pour octet, le
  fichier passé par `--config=cloud-init.user-data="$(cat user-data.yaml)"`, au
  saut de ligne final près (la substitution de commande du shell le retire) :
  c'est ce qui prouve que la machine a été configurée par CE fichier ;
- sur le réseau `lab-amorcer` (NAT, sans IPv6), la seule adresse de portée
  globale est une IPv4 de 10.10.71.0/24.
"""

from __future__ import annotations

import ipaddress
import json

import pytest

from conftest import exiger_workdir, hote_incus, incus_instance, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "amorcer-premiere-vm-propre"

INSTANCE = "boutique-vm1"
RESEAU = "lab-amorcer"
PLAGE = ipaddress.ip_network("10.10.71.0/24")
UTILISATEUR = "boutique"
PAQUETS = ("jq", "tree")
FICHIER_ROLE = "/etc/boutique/role"


@pytest.fixture(scope="module")
def instance() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    trouvee = incus_instance(INSTANCE)
    if trouvee is None:
        pytest.fail(
            f"Aucune instance Incus nommée {INSTANCE}. Le lab demande de la "
            "créer avec `incus launch`, à partir de votre user-data."
        )
    return trouvee


@pytest.fixture(scope="module")
def machine(instance: dict):
    if instance.get("status") != "Running":
        pytest.fail(
            f"{INSTANCE} existe mais n'est pas démarrée (état : "
            f"{instance.get('status')})."
        )
    hote = hote_incus(INSTANCE)
    # cloud-init peut encore travailler si le check suit de près le launch :
    # on lui laisse le temps de finir, borné, plutôt que d'échouer à tort.
    hote.run("timeout 240 cloud-init status --wait")
    return hote


def test_vm_sur_le_reseau_prive_sans_adresse_publique(instance: dict) -> None:
    """Une MACHINE VIRTUELLE, branchée sur le réseau privé du lab, et rien d'autre."""
    assert instance.get("type") == "virtual-machine", (
        f"{INSTANCE} est de type {instance.get('type')} : le lab demande une "
        "machine virtuelle, lancée avec `--vm`."
    )
    cartes = {
        nom: dev
        for nom, dev in (instance.get("expanded_devices") or {}).items()
        if dev.get("type") == "nic"
    }
    reseaux = {dev.get("network") for dev in cartes.values()}
    assert reseaux == {RESEAU}, (
        f"Les cartes réseau de {INSTANCE} sont branchées sur {sorted(map(str, reseaux))} : "
        f"le lab demande le seul réseau privé {RESEAU} (`--network {RESEAU}`)."
    )

    globales = []
    for interface, detail in ((instance.get("state") or {}).get("network") or {}).items():
        if interface == "lo":
            continue
        for adresse in detail.get("addresses") or []:
            if adresse.get("scope") == "global":
                globales.append(ipaddress.ip_address(adresse["address"]))
    assert globales, (
        f"{INSTANCE} n'a encore aucune adresse : attendez la fin du démarrage."
    )
    hors_plage = [str(a) for a in globales if a not in PLAGE]
    assert not hors_plage, (
        f"{INSTANCE} porte des adresses hors du réseau privé {PLAGE} : {hors_plage}."
    )


def test_cloud_init_termine_avec_votre_user_data(instance: dict, machine) -> None:
    """La machine a été configurée par VOTRE fichier, et cloud-init a fini sans erreur."""
    fichier = WORKDIR / "user-data.yaml"
    assert fichier.is_file(), "challenge/work/user-data.yaml a disparu."
    contenu = fichier.read_text(encoding="utf-8")
    assert contenu.startswith("#cloud-config\n"), (
        "La première ligne de user-data.yaml doit être exactement #cloud-config : "
        "sans elle, cloud-init ignore tout le fichier."
    )
    assert "???" not in contenu, "user-data.yaml contient encore des ???."

    pose = (instance.get("config") or {}).get("cloud-init.user-data", "")
    assert pose.rstrip() == contenu.rstrip(), (
        f"Le user-data de {INSTANCE} n'est pas celui de challenge/work/user-data.yaml. "
        "Recréez la machine à partir du fichier : une configuration faite à la main "
        "après le démarrage ne se reconstruit pas."
    )

    statut = machine.run("cloud-init status --format json")
    assert statut.rc in (0, 2), f"cloud-init status a échoué : {statut.stderr}"
    rapport = json.loads(statut.stdout)
    assert rapport.get("status") == "done", (
        f"cloud-init n'a pas terminé (status : {rapport.get('status')})."
    )
    assert not rapport.get("errors"), (
        f"cloud-init a terminé avec des erreurs : {rapport.get('errors')}. "
        "Lisez /var/log/cloud-init.log dans la machine."
    )


def test_utilisateur_boutique(machine) -> None:
    """L'utilisateur existe, sans mot de passe, sans sudo, joignable par la clé du lab."""
    utilisateur = machine.user(UTILISATEUR)
    assert utilisateur.exists, f"L'utilisateur {UTILISATEUR} n'existe pas."
    assert utilisateur.shell == "/bin/bash", (
        f"Le shell de {UTILISATEUR} est {utilisateur.shell}, /bin/bash attendu."
    )
    assert "sudo" not in utilisateur.groups, (
        f"{UTILISATEUR} est dans le groupe sudo : ce compte applicatif n'a pas "
        "à administrer la machine."
    )

    etat = machine.run(f"passwd -S {UTILISATEUR}").stdout.split()
    assert len(etat) > 1 and etat[1] == "L", (
        f"Le mot de passe de {UTILISATEUR} n'est pas verrouillé (passwd -S : "
        f"{' '.join(etat)}). Posez lock_passwd: true."
    )

    cle = (WORKDIR / "cle_lab.pub").read_text(encoding="utf-8").split()
    autorisees = machine.file(f"/home/{UTILISATEUR}/.ssh/authorized_keys")
    assert autorisees.exists, f"/home/{UTILISATEUR}/.ssh/authorized_keys n'existe pas."
    assert cle[1] in autorisees.content_string, (
        "La clé publique challenge/work/cle_lab.pub n'est pas autorisée pour "
        f"{UTILISATEUR}."
    )


def test_paquets_installes(machine) -> None:
    """Les paquets viennent du user-data, installés au premier démarrage."""
    manquants = [p for p in PAQUETS if not machine.package(p).is_installed]
    assert not manquants, f"Paquets absents de {INSTANCE} : {manquants}."


def test_fichier_de_role(machine) -> None:
    """Le fichier qui dit à quoi sert la machine, avec les bons droits."""
    role = machine.file(FICHIER_ROLE)
    assert role.exists, f"{FICHIER_ROLE} n'existe pas."
    assert role.content_string.strip() == "app", (
        f"{FICHIER_ROLE} contient {role.content_string.strip()!r}, `app` attendu."
    )
    assert role.user == "root" and role.group == "root", (
        f"{FICHIER_ROLE} appartient à {role.user}:{role.group}, root:root attendu."
    )
    assert role.mode == 0o644, (
        f"{FICHIER_ROLE} a les droits {oct(role.mode)}, 0644 attendus."
    )
