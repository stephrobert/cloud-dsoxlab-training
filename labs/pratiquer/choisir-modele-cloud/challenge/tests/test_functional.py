"""Tests fonctionnels de « Choisir le modèle cloud ».

Le livrable est `challenge/work/decision.json`. Chaque attendu se déduit de
`brief.json`. Un test par état, et chacun échoue sur l'état de départ (le
livrable n'existe pas) :

1. le modèle de service : l'équipe maintient son application, sans équipe
   d'exploitation ni dépendance au système ou au noyau, donc une plateforme
   managée ;
2. le modèle de déploiement : rien dans le brief n'exige du privé ni de
   l'hybride ;
3. le partage des responsabilités : le fournisseur porte la plateforme
   managée, l'équipe garde application, données, identités et configuration, et
   la décision est justifiée.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "pratiquer-choisir-modele-cloud"
EQUIPE = {"application", "data", "identities", "configuration"}
FOURNISSEUR_EN_PAAS = {"managed_platform", "operating_system", "hardware", "network"}


@pytest.fixture(scope="module")
def brief() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "brief.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "decision.json"
    assert chemin.is_file(), message(
        en="decision.json is missing: no cloud model is chosen.",
        fr="decision.json est absent : aucun modèle cloud n'est choisi.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"decision.json is not valid JSON: {erreur}",
                            fr=f"decision.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="decision.json must hold an object.",
                                              fr="decision.json doit contenir un objet.")
    return contenu


def _modele_attendu(brief: dict) -> str:
    c, equipe = brief["constraints"], brief["team"]
    if c["kernel_dependency"] or c["operating_system_dependency"] or equipe["operations_staff"]:
        return "iaas"
    return "paas" if equipe["application_maintenance"] else "saas"


def test_le_modele_de_service_suit_le_brief(brief: dict, decision: dict) -> None:
    attendu = _modele_attendu(brief)
    assert decision.get("service_model") == attendu, message(
        en=f"The service model {decision.get('service_model')!r} does not follow the brief: who maintains the "
        "application, who runs the system, and what the workload depends on.",
        fr=f"Le modèle de service {decision.get('service_model')!r} ne suit pas le brief : qui maintient "
        "l'application, qui exploite le système, et de quoi la charge dépend.",
    )


def test_le_modele_de_deploiement_suit_le_brief(decision: dict) -> None:
    assert decision.get("deployment_model") == "public", message(
        en=f"The deployment model {decision.get('deployment_model')!r} answers a requirement the brief does "
        "not state.",
        fr=f"Le modèle de déploiement {decision.get('deployment_model')!r} répond à une exigence que le brief "
        "ne pose pas.",
    )


def test_les_responsabilites_sont_partagees_selon_le_modele(decision: dict) -> None:
    resp = decision.get("responsibilities") or {}
    fournisseur, equipe = set(resp.get("provider") or []), set(resp.get("team") or [])
    defauts = []
    if "managed_platform" not in fournisseur:
        defauts.append(message(en="the provider does not carry the managed platform",
                               fr="le fournisseur ne porte pas la plateforme managée"))
    if not equipe >= EQUIPE:
        defauts.append(message(en=f"the team does not keep {sorted(EQUIPE - equipe)}",
                               fr=f"l'équipe ne garde pas {sorted(EQUIPE - equipe)}"))
    if equipe & FOURNISSEUR_EN_PAAS:
        defauts.append(message(en=f"the team takes on {sorted(equipe & FOURNISSEUR_EN_PAAS)}, which the provider "
                               "runs on a managed platform",
                               fr=f"l'équipe prend {sorted(equipe & FOURNISSEUR_EN_PAAS)}, que le fournisseur "
                               "exploite sur une plateforme managée"))
    if not (isinstance(decision.get("rationale"), str) and decision["rationale"].strip()):
        defauts.append(message(en="no rationale", fr="aucune justification"))
    assert not defauts, message(
        en=f"The shared responsibility does not hold: {defauts}.",
        fr=f"Le partage des responsabilités ne tient pas : {defauts}.",
    )
