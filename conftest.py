"""
Configuration pytest commune au catalogue cloud-dsoxlab-training.

Tous les labs de la vague 1 sont de type `shell` : ils s'exécutent dans
`challenge/work`, sur le poste de l'apprenant. Les tests lisent deux sources
d'ÉTAT, jamais les commandes tapées :

- **feint**, l'émulateur d'API lancé par dsoxlab comme service conteneur. Les
  tests l'interrogent par les API publiques de Scaleway et d'Outscale, exactement
  comme un client officiel, à l'adresse `FEINT_URL` (défaut
  `http://127.0.0.1:4599`).
- **Incus**, sur le poste, pour les machines qui démarrent réellement. Les tests
  y entrent par testinfra, au travers d'un backend `incus exec` défini ici.

Helpers exposés : `workdir_lab()`, `exiger_workdir()`, `scw_get()`,
`osc_call()`, `incus_json()`, `hote_incus()`.

Le rejeu des solutions de référence n'est PAS fait ici : il passe par
`scripts/valider-labs.py`, qui enchaîne `dsoxlab run`, `check`, la solution,
`check` et `clean`. Un lab qui démarre une machine ou remplit un émulateur ne se
rejoue pas proprement depuis une fixture pytest.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent

FEINT_URL = os.environ.get("FEINT_URL", "http://127.0.0.1:4599").rstrip("/")

# feint ne vérifie aucune signature : un jeton bien formé suffit, comme celui
# que produit `feint env scaleway`.
_SCW_TOKEN = "11111111-1111-1111-1111-111111111111"  # noqa: S105 (jeton FICTIF de feint)


# ── Répertoire de travail ────────────────────────────────────────────────────


def message(en: str, fr: str) -> str:
    """Le message d'une assertion, dans la langue de l'apprenant.

    Pourquoi ce helper
    ------------------

    Quand un test échoue, `dsoxlab check` affiche le **message écrit par
    l'auteur** : c'est la seule consigne que l'apprenant reçoit à cet instant.
    Or tout le reste du catalogue existe dans les deux langues (`README.md` et
    `README.fr.md`), et ce texte-là ne peut pas : le contrat dsoxlab impose un
    nom de fichier unique, `challenge/tests/test_functional.py`. Il n'y a donc
    pas de version anglaise possible par duplication, d'où ce choix à
    l'exécution. C'est la même solution que `hints.yaml`, qui porte depuis
    toujours un `text_en` et un `text_fr` côte à côte.

    Pourquoi ici et pas dans dsoxlab
    --------------------------------

    Un test de lab doit rester jouable par un simple `pytest`, sans l'outil
    installé : c'est le test de non-couplage du catalogue. Un
    `from dsoxlab… import` en tête d'un fichier de tests le casserait. dsoxlab
    ne reconnaît donc que la **forme** de l'appel, `message(en=…, fr=…)`.

    La langue vient de `DSOXLAB_LANG`, comme pour le reste de l'outil, et
    l'anglais est le défaut.

    Usage :

        from conftest import lab_host, message

        assert f.exists, message(
            en="/etc/myapp is missing. Create it with ansible.builtin.file.",
            fr="/etc/myapp est absent. Crée-le avec ansible.builtin.file.",
        )
    """
    langue = os.environ.get("DSOXLAB_LANG", "en").lower()
    return fr if langue.startswith("fr") else en


def workdir_lab(fichier_test: str | Path) -> Path:
    """Workdir du lab auquel appartient un fichier de test.

    `<lab>/challenge/work` par défaut ; `LAB_WORKDIR` le surcharge.
    """
    surcharge = os.environ.get("LAB_WORKDIR")
    if surcharge:
        return Path(surcharge)
    return Path(fichier_test).resolve().parents[2] / "challenge" / "work"


def exiger_workdir(workdir: Path, lab_id: str) -> None:
    """Skippe un lab simplement pas joué, échoue si `LAB_WORKDIR` ment."""
    if workdir.is_dir():
        return
    if os.environ.get("LAB_WORKDIR"):
        pytest.fail(f"LAB_WORKDIR pointe sur {workdir}, qui n'existe pas.")
    pytest.skip(
        f"Lab non joué : {workdir} est absent. "
        f"Lancez `dsoxlab run {lab_id}` pour poser l'état de départ."
    )


def etat_lab() -> Path | None:
    """Répertoire d'état du lab, hors workdir, exporté par `dsoxlab check`."""
    valeur = os.environ.get("LAB_STATE_DIR")
    return Path(valeur) if valeur else None


# ── feint : lire l'état par les API publiques ────────────────────────────────


def _requete(methode: str, url: str, corps: dict | None, entetes: dict) -> Any:
    donnees = json.dumps(corps).encode() if corps is not None else None
    requete = urllib.request.Request(url, data=donnees, method=methode)  # noqa: S310 (URL de feint, http local)
    for cle, valeur in entetes.items():
        requete.add_header(cle, valeur)
    try:
        with urllib.request.urlopen(requete, timeout=10) as reponse:  # noqa: S310
            return json.loads(reponse.read() or b"{}")
    except urllib.error.URLError as erreur:
        pytest.fail(
            f"feint ne répond pas sur {FEINT_URL} ({erreur}). Le service démarre "
            "avec `dsoxlab run` : relancez-le, et vérifiez qu'aucun autre feint "
            "n'occupe déjà le port 4599."
        )


def feint_disponible() -> bool:
    try:
        with urllib.request.urlopen(f"{FEINT_URL}/_feint/health", timeout=3):  # noqa: S310
            return True
    except (urllib.error.URLError, OSError):
        return False


def scw_get(chemin: str) -> Any:
    """GET sur l'API Scaleway servie par feint (`/instance/v1/...`)."""
    return _requete(
        "GET",
        f"{FEINT_URL}{chemin}",
        None,
        {"X-Auth-Token": _SCW_TOKEN},
    )


def osc_call(action: str, corps: dict | None = None) -> Any:
    """Appel d'une action de l'API Outscale servie par feint (`ReadNets`...)."""
    return _requete(
        "POST",
        f"{FEINT_URL}/api/v1/{action}",
        corps or {},
        {"Content-Type": "application/json"},
    )


# ── Incus : lire l'état d'une machine réelle ─────────────────────────────────


def incus_json(*args: str) -> Any:
    """`incus <args> --format json`, décodé. None si la commande échoue."""
    proc = subprocess.run(
        ["incus", *args, "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return json.loads(proc.stdout or "null")


def incus_instance(nom: str) -> dict | None:
    """La description complète d'une instance, ou None si elle n'existe pas."""
    instances = incus_json("list", f"^{nom}$") or []
    return instances[0] if instances else None


def hote_incus(nom: str):
    """Hôte testinfra qui entre dans l'instance Incus `nom` par `incus exec`.

    testinfra ne connaît que `lxc exec` ; ce backend en est la transposition
    exacte, pour que les tests emploient `host.user`, `host.package`,
    `host.file` plutôt que de parser des sorties de commandes.
    """
    from testinfra.backend.base import BaseBackend
    from testinfra.host import Host

    class IncusBackend(BaseBackend):
        NAME = "incus"

        def __init__(self, name: str, *args: Any, **kwargs: Any):
            self.name = name
            super().__init__(self.name, *args, **kwargs)

        def run(self, command: str, *args: str, **kwargs: Any):
            cmd = self.get_command(command, *args)
            out = self.run_local(
                "incus exec %s --mode=non-interactive -- /bin/sh -c %s",
                self.name,
                cmd,
            )
            out.command = self.encode(cmd)
            return out

    return Host(IncusBackend(nom))


def commande(*args: str) -> subprocess.CompletedProcess[str]:
    """Lance une commande locale, sans lever : le test juge du code retour."""
    return subprocess.run(list(args), capture_output=True, text=True, check=False)


def citer(args: list[str]) -> str:
    return " ".join(shlex.quote(a) for a in args)
