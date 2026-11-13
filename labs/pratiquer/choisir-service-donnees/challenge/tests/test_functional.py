"""Tests fonctionnels de « Choisir un service de données ».

Le livrable est `challenge/work/data-service-decision.json`. Chaque attendu se
recalcule depuis `data-service-brief.json` : le service retenu est celui du
catalogue qui tient toutes les contraintes, et ses caractéristiques se lisent
dans le catalogue. Un test par état, et chacun échoue sur l'état de départ (le
livrable n'existe pas) :

1. le service retenu tient la charge, l'équipe, le réseau, la reprise et le
   budget ;
2. la décision reprend le moteur, la version, le mode d'exploitation, la
   réplication, les domaines de panne, le RPO, le RTO et le PITR du service ;
3. l'accès est privé, sans exposition à Internet ;
4. la vérification d'une restauration est prévue, par qui le catalogue
   l'attribue ;
5. chaque option du catalogue est comparée, chaque option écartée a sa raison,
   et la décision est justifiée.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "choisir-service-donnees"
REPRIS = ("operating_model", "replication", "failure_domains", "rpo_minutes", "rto_minutes", "point_in_time_recovery")


@pytest.fixture(scope="module")
def brief() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "data-service-brief.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "data-service-decision.json"
    assert chemin.is_file(), message(
        en="data-service-decision.json is missing: no data service is chosen.",
        fr="data-service-decision.json est absent : aucun service de données n'est choisi.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"data-service-decision.json is not valid JSON: {erreur}",
                            fr=f"data-service-decision.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="data-service-decision.json must hold an object.",
                                              fr="data-service-decision.json doit contenir un objet.")
    return contenu


def _ecarts(brief: dict, s: dict) -> list[str]:
    """Les contraintes du brief que le service s ne tient pas."""
    w, obj = brief["workload"], brief["recovery_objectives"]
    regles = {
        "data_model": s["data_model"] == w["data_model"],
        "engine": s["engine"] == w["required_engine"],
        "major_version": w["required_major_version"] in s["major_versions"],
        "extensions": set(w["required_extensions"]) <= set(s["extensions"]),
        "budget": s["monthly_cost_eur"] <= brief["monthly_budget_eur"],
        "operations_hours": s["operations_hours_per_month"] <= brief["team"]["database_operations_capacity_hours_per_month"],
        "private_endpoint": s["private_endpoint"] and not s["internet_endpoint_mandatory"],
        "failure_domains": s["failure_domains"] >= obj["minimum_failure_domains"],
        "rpo": s["rpo_minutes"] <= obj["maximum_rpo_minutes"],
        "rto": s["rto_minutes"] <= obj["maximum_rto_minutes"],
    }
    return [k for k, ok in regles.items() if not ok]


def _service(brief: dict, decision: dict) -> dict | None:
    return next((s for s in brief["service_catalogue"] if s["id"] == decision.get("service_id")), None)


def test_le_service_retenu_tient_toutes_les_contraintes(brief: dict, decision: dict) -> None:
    s = _service(brief, decision)
    assert s is not None, message(
        en=f"The service {decision.get('service_id')!r} is not in the catalogue of the brief.",
        fr=f"Le service {decision.get('service_id')!r} n'est pas dans le catalogue du brief.",
    )
    ecarts = _ecarts(brief, s)
    assert not ecarts, message(
        en=f"The service {s['id']} breaks these constraints of the brief: {ecarts}.",
        fr=f"Le service {s['id']} ne tient pas ces contraintes du brief : {ecarts}.",
    )


def test_la_decision_reprend_les_caracteristiques_du_service(brief: dict, decision: dict) -> None:
    s = _service(brief, decision)
    assert s is not None, message(en="No service of the catalogue is retained.",
                                  fr="Aucun service du catalogue n'est retenu.")
    attendu = {k: s[k] for k in REPRIS}
    attendu["engine"] = s["engine"]
    attendu["major_version"] = brief["workload"]["required_major_version"]
    ecarts = {k: decision.get(k) for k, v in attendu.items() if decision.get(k) != v}
    assert not ecarts, message(
        en=f"These characteristics differ from the retained service in the catalogue: {ecarts}.",
        fr=f"Ces caractéristiques diffèrent du service retenu dans le catalogue : {ecarts}.",
    )


def test_l_acces_est_prive(decision: dict) -> None:
    assert decision.get("private_endpoint") is True and decision.get("internet_exposure") is False, message(
        en="The database is not reached only through a private endpoint: the brief forbids Internet access.",
        fr="La base n'est pas jointe par un point de terminaison privé seulement : le brief interdit l'accès "
        "par Internet.",
    )


def test_la_verification_d_une_restauration_est_prevue(brief: dict, decision: dict) -> None:
    s = _service(brief, decision) or {}
    verification = decision.get("restore_verification")
    defauts = []
    if decision.get("restore_test_owner") != s.get("restore_test_owner"):
        defauts.append(message(en="the restore test is not given to the one the catalogue names",
                               fr="le test de restauration n'est pas confié à qui le catalogue désigne"))
    if not (isinstance(verification, str) and verification.strip()):
        defauts.append(message(en="nothing says how a restore is verified",
                               fr="rien ne dit comment une restauration est vérifiée"))
    assert not defauts, message(
        en=f"The restore verification is not planned: {defauts}. A managed service keeps backups; checking "
        "that they restore stays with the customer.",
        fr=f"La vérification d'une restauration n'est pas prévue : {defauts}. Un service managé garde les "
        "sauvegardes ; vérifier qu'elles se restaurent reste au client.",
    )


def test_chaque_option_est_comparee_et_chaque_rejet_justifie(brief: dict, decision: dict) -> None:
    ids = {s["id"] for s in brief["service_catalogue"]}
    comparaison = decision.get("comparison") or {}
    non_comparees = sorted(i for i in ids if not (isinstance(comparaison.get(i), str) and comparaison[i].strip()))
    rejets = {r.get("service_id"): r.get("reason") for r in decision.get("rejected_options") or [] if isinstance(r, dict)}
    attendus = ids - {decision.get("service_id")}
    sans_raison = sorted(i for i in attendus if not (isinstance(rejets.get(i), str) and rejets[i].strip()))
    justifie = isinstance(decision.get("rationale"), str) and decision["rationale"].strip()
    assert not non_comparees and not sans_raison and justifie, message(
        en=f"The decision is not argued: options not compared {non_comparees}, rejected without a reason "
        f"{sans_raison}{'' if justifie else ', no rationale'}.",
        fr=f"La décision n'est pas argumentée : options non comparées {non_comparees}, écartées sans raison "
        f"{sans_raison}{'' if justifie else ', aucune justification'}.",
    )
