"""Tests fonctionnels du challenge 1, « Architecture à budget contraint ».

Le livrable est `challenge/work/estimation.yaml`. Chaque réponse est comparée à
une valeur RECALCULÉE à l'instant du check, depuis l'état que feint sert par
l'API publique de Scaleway et depuis la grille datée du répertoire de travail.
Aucune réponse attendue n'est écrite dans le dépôt : l'environnement est tiré
au hasard à chaque `dsoxlab run`.

Un contrôle d'intégrité précède tout : l'inventaire de feint doit être celui
que le setup a relevé (`$LAB_STATE_DIR/environnement.json`). Supprimer une
instance ferait baisser la facture sans rien estimer.

Faits mesurés le 2026-10-12, feint v0.13.0, scw 2.62.0 :

- chaque instance créée reçoit un volume racine de 10 Go (`<nom>-root`), listé
  par `scw block volume list` comme tout autre volume ;
- une IP flexible non attachée porte `server: null` ; un volume non attaché
  porte `references: []` ;
- `scw ... list` sans `zone=all` ne montre que la zone par défaut, `fr-par-1` :
  les ressources de `fr-par-2` échappent à qui ne le sait pas ;
- les lectures par le CLI ne modifient pas l'inventaire de feint.
"""

from __future__ import annotations

import json
from collections import Counter

import pytest
import yaml

from conftest import etat_lab, exiger_workdir, message, scw_get, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "pratiquer-challenge-budget-contraint"

ZONES = ("fr-par-1", "fr-par-2", "fr-par-3")
BUDGET_EUR = 160.00
TOLERANCE_EUR = 0.50


def _par_zone(chemin: str, cle: str) -> list[dict]:
    objets: list[dict] = []
    for zone in ZONES:
        objets += scw_get(chemin.format(zone=zone)).get(cle) or []
    return objets


@pytest.fixture(scope="module")
def grille() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return yaml.safe_load((WORKDIR / "grille-tarifaire.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def reel(grille: dict) -> dict:
    """L'environnement tel que feint le sert, et son coût sur la grille."""
    reference = etat_lab()
    if reference and (reference / "environnement.json").is_file():
        attendus = json.loads((reference / "environnement.json").read_text(encoding="utf-8"))
        etat = scw_get("/_feint/state")
        presents = sorted(r["ID"] for r in etat.get("resources") or [])
        assert presents == attendus, message(
            en="The environment provided was modified since `dsoxlab run` (a resource "
            "created or deleted). This challenge is played READ-only: run "
            "`dsoxlab run pratiquer-challenge-budget-contraint` again, which draws a new environment.",
            fr="L'environnement fourni a été modifié depuis `dsoxlab run` (ressource "
            "créée ou supprimée). Ce challenge se joue en LECTURE seule : relancez "
            "`dsoxlab run pratiquer-challenge-budget-contraint`, qui tire un nouvel environnement.",
        )

    serveurs = _par_zone("/instance/v1/zones/{zone}/servers", "servers")
    volumes = _par_zone("/block/v1alpha1/zones/{zone}/volumes", "volumes")
    ips = _par_zone("/instance/v1/zones/{zone}/ips", "ips")
    passerelles = _par_zone("/vpc-gw/v2/zones/{zone}/gateways", "gateways")

    instances = Counter(s["commercial_type"] for s in serveurs)
    volumes_go = sum(v["size"] for v in volumes) // 1_000_000_000
    heures = grille["heures_par_mois"]
    cout = (
        sum(n * grille["instances_eur_par_heure"][t] * heures for t, n in instances.items())
        + volumes_go * grille["volume_bloc_eur_par_go_et_par_mois"]
        + len(ips) * grille["ip_flexible_eur_par_mois"]
        + sum(
            grille["passerelle_vpc_gw_s_eur_par_mois"]
            for p in passerelles
            if p.get("type") == "VPC-GW-S"
        )
    )
    orphelins = {v["name"] for v in volumes if not v.get("references")} | {
        i["address"] for i in ips if not i.get("server")
    }
    return {
        "instances": dict(instances),
        "volumes_go": volumes_go,
        "ips_flexibles": len(ips),
        "passerelles": len(passerelles),
        "cout": round(cout, 2),
        "orphelins": orphelins,
    }


@pytest.fixture(scope="module")
def estimation() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    fichier = WORKDIR / "estimation.yaml"
    assert fichier.is_file(), message(
        en="challenge/work/estimation.yaml has disappeared.",
        fr="challenge/work/estimation.yaml a disparu.",
    )
    try:
        contenu = yaml.safe_load(fichier.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as erreur:
        pytest.fail(message(
            en=f"estimation.yaml is not readable YAML: {erreur}",
            fr=f"estimation.yaml n'est pas un YAML lisible : {erreur}",
        ))
    assert isinstance(contenu, dict), message(
        en="estimation.yaml must be a YAML dictionary.",
        fr="estimation.yaml doit être un dictionnaire YAML.",
    )
    return contenu


def test_instances_par_type(estimation: dict, reel: dict) -> None:
    """Le nombre d'instances de chaque type, toutes zones confondues."""
    donne = {str(k): v for k, v in (estimation.get("instances") or {}).items()}
    assert donne == reel["instances"], message(
        en=f"instances: {donne}. The count does not match the environment. "
        "Did you look at every zone?",
        fr=f"instances : {donne}. Le compte ne correspond pas à l'environnement. "
        "Avez-vous regardé toutes les zones ?",
    )


def test_volumes_en_go(estimation: dict, reel: dict) -> None:
    """Le total des volumes bloc facturés, en Go."""
    assert estimation.get("volumes_go") == reel["volumes_go"], message(
        en=f"volumes_go: {estimation.get('volumes_go')}. The total does not match. "
        "Read the grid's rules again on what is billed.",
        fr=f"volumes_go : {estimation.get('volumes_go')}. Le total ne correspond pas. "
        "Relisez les règles de la grille sur ce qui est facturé.",
    )


def test_ips_et_passerelles(estimation: dict, reel: dict) -> None:
    """Les IP flexibles d'instance et les passerelles, comptées à part."""
    assert estimation.get("ips_flexibles") == reel["ips_flexibles"], message(
        en=f"ips_flexibles: {estimation.get('ips_flexibles')}, does not match.",
        fr=f"ips_flexibles : {estimation.get('ips_flexibles')}, ne correspond pas.",
    )
    assert estimation.get("passerelles") == reel["passerelles"], message(
        en=f"passerelles: {estimation.get('passerelles')}, does not match.",
        fr=f"passerelles : {estimation.get('passerelles')}, ne correspond pas.",
    )


def test_cout_mensuel(estimation: dict, reel: dict) -> None:
    """Le coût mensuel, à 50 centimes près."""
    donne = estimation.get("cout_mensuel_eur")
    assert isinstance(donne, int | float) and not isinstance(donne, bool), message(
        en="cout_mensuel_eur must be a number, in euros.",
        fr="cout_mensuel_eur doit être un nombre, en euros.",
    )
    assert abs(donne - reel["cout"]) <= TOLERANCE_EUR, message(
        en=f"cout_mensuel_eur: {donne}. The gap with the cost recomputed on the grid "
        f"exceeds {TOLERANCE_EUR} euro.",
        fr=f"cout_mensuel_eur : {donne}. L'écart au coût recalculé sur la grille "
        f"dépasse {TOLERANCE_EUR} euro.",
    )


def test_budget_et_ressources_non_rattachees(estimation: dict, reel: dict) -> None:
    """Le verdict sur le budget, et ce qui coûte sans servir."""
    attendu = reel["cout"] <= BUDGET_EUR
    assert estimation.get("dans_le_budget") is attendu, message(
        en=f"dans_le_budget: {estimation.get('dans_le_budget')}, does not match "
        "the environment's cost compared with the mission's budget.",
        fr=f"dans_le_budget : {estimation.get('dans_le_budget')}, ne correspond pas "
        "au coût de l'environnement comparé au budget de la mission.",
    )
    donne = {str(x) for x in (estimation.get("non_rattaches") or [])}
    assert donne == reel["orphelins"], message(
        en=f"non_rattaches: {sorted(donne)}. The list of billed resources "
        "attached to nothing does not match.",
        fr=f"non_rattaches : {sorted(donne)}. La liste des ressources facturées "
        "rattachées à rien ne correspond pas.",
    )
