"""Tests fonctionnels de « Décider d'une architecture cloud cible ».

Le livrable est `challenge/work/decision.json` : la comparaison des deux options
du brief, et l'ADR qui en tire la décision. Un test par état, et chacun échoue
sur l'état de départ (le livrable n'existe pas) :

1. la comparaison couvre les deux options, sur les six axes, avec les valeurs
   mesurées du brief ;
2. l'ADR est complet : options, critères, contexte, justification, condition de
   révision, conséquences et risque accepté ;
3. la décision retient l'option qui tient TOUTES les exigences dures du brief.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-architecture-cible"
AXES = (
    "monthly_cost_eur",
    "operations_days_per_month",
    "data_residency",
    "availability_zones",
    "portability",
    "performance",
)
CHAMPS_TEXTE = ("title", "context", "rationale", "review_condition")


@pytest.fixture(scope="module")
def brief() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "brief.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin: Path = WORKDIR / "decision.json"
    assert chemin.is_file(), message(
        en="decision.json is missing: neither the comparison nor the decision is written down.",
        fr="decision.json est absent : ni la comparaison ni la décision ne sont écrites.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"decision.json is not valid JSON: {erreur}",
                            fr=f"decision.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(
        en="decision.json must hold an object with a comparison and an ADR.",
        fr="decision.json doit contenir un objet, avec une comparaison et un ADR.",
    )
    return contenu


def test_la_comparaison_reprend_les_faits_du_brief(brief: dict, decision: dict) -> None:
    comparaison = decision.get("comparison") or {}
    manquantes = sorted(set(brief["options"]) - set(comparaison))
    assert not manquantes, message(
        en=f"The comparison leaves out these options of the brief: {manquantes}.",
        fr=f"La comparaison laisse de côté ces options du brief : {manquantes}.",
    )
    ecarts = {}
    for option, faits in brief["options"].items():
        ligne = comparaison.get(option) or {}
        for axe in AXES:
            if ligne.get(axe) != faits[axe]:
                ecarts[f"{option}.{axe}"] = ligne.get(axe, "absent")
    assert not ecarts, message(
        en=f"These comparison values are missing or differ from the measured facts of the brief: {ecarts}.",
        fr=f"Ces valeurs de la comparaison manquent ou diffèrent des faits mesurés du brief : {ecarts}.",
    )


def test_l_adr_est_complet(brief: dict, decision: dict) -> None:
    adr = decision.get("adr") or {}
    manques = []
    if set(adr.get("options_considered") or []) != set(brief["options"]):
        manques.append("options_considered")
    if set(adr.get("criteria") or []) != set(AXES):
        manques.append("criteria")
    manques += [c for c in CHAMPS_TEXTE if not (isinstance(adr.get(c), str) and adr[c].strip())]
    manques += [c for c in ("consequences", "accepted_risks") if not adr.get(c)]
    assert not manques, message(
        en=f"The ADR is incomplete: {manques}. A decision record states the options weighed, the criteria, "
        "why, what it costs, the risk accepted and when to revisit it.",
        fr=f"L'ADR est incomplet : {manques}. Un enregistrement de décision dit les options pesées, les "
        "critères, pourquoi, ce que cela coûte, le risque accepté et quand y revenir.",
    )


def test_la_decision_tient_les_exigences_dures(brief: dict, decision: dict) -> None:
    choix = (decision.get("adr") or {}).get("decision")
    assert choix in brief["options"], message(
        en=f"The ADR decides on {choix!r}, which is none of the options of the brief.",
        fr=f"L'ADR retient {choix!r}, qui n'est aucune des options du brief.",
    )
    exigences = brief["requirements"]
    faits = brief["options"][choix]
    non_tenues = []
    if faits["monthly_cost_eur"] > exigences["monthly_budget_eur"]:
        non_tenues.append("monthly_budget_eur")
    if faits["operations_days_per_month"] > exigences["max_operations_days_per_month"]:
        non_tenues.append("max_operations_days_per_month")
    if faits["data_residency"] != exigences["data_region"]:
        non_tenues.append("data_region")
    if faits["availability_zones"] < exigences["minimum_zones"]:
        non_tenues.append("minimum_zones")
    assert not non_tenues, message(
        en=f"The option {choix} breaks these hard requirements of the brief: {non_tenues}.",
        fr=f"L'option {choix} ne tient pas ces exigences dures du brief : {non_tenues}.",
    )
