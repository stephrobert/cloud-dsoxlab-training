"""Tests fonctionnels de « Choisir et dimensionner un modèle de calcul ».

Le livrable est `challenge/work/compute-decision.json`. Chaque valeur attendue
est RECALCULÉE depuis `workload.json`, jamais écrite ici. Un test par état, et
chacun échoue sur l'état de départ (le livrable n'existe pas) :

1. le modèle de calcul est le seul qui accepte le module noyau de l'hôte et la
   durée maximale d'une requête, et la décision est justifiée ;
2. l'architecture processeur est une de celles où la dépendance native a été
   testée ;
3. la demande de dimensionnement est le p95 de la semaine, augmenté de la
   croissance prévue (le maximum bref n'est pas une charge soutenue) ;
4. le profil retenu est le moins cher de ceux qui tiennent cette demande sur
   une architecture testée.
"""

from __future__ import annotations

import json
import math

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "choisir-modele-calcul"


@pytest.fixture(scope="module")
def brief() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "compute-decision.json"
    assert chemin.is_file(), message(
        en="compute-decision.json is missing: no compute decision is written down.",
        fr="compute-decision.json est absent : aucune décision de calcul n'est écrite.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"compute-decision.json is not valid JSON: {erreur}",
                            fr=f"compute-decision.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="compute-decision.json must hold an object.",
                                              fr="compute-decision.json doit contenir un objet.")
    return contenu


def _demande(brief: dict) -> tuple[float, float]:
    mesures = brief["measurements"]
    croissance = 1 + mesures["planned_growth_percent"] / 100
    return mesures["p95"]["cpu_vcpus_used"] * croissance, mesures["p95"]["memory_gib_used"] * croissance


def _architectures_testees(brief: dict) -> set[str]:
    testees: set[str] | None = None
    for dep in brief["workload"]["native_dependencies"]:
        archis = set(dep["tested_architectures"])
        testees = archis if testees is None else testees & archis
    return testees or set()


def test_le_modele_de_calcul_tient_les_contraintes_d_execution(brief: dict, decision: dict) -> None:
    charge = brief["workload"]
    possibles = sorted(
        nom for nom, m in brief["compute_models"].items()
        if (m["supports_custom_host_kernel_module"] or not charge["requires_custom_host_kernel_module"])
        and (m["maximum_request_duration_minutes"] is None
             or m["maximum_request_duration_minutes"] >= charge["maximum_request_duration_minutes"])
    )
    choix = decision.get("compute_model")
    assert choix in possibles, message(
        en=f"The compute model {choix!r} cannot run this workload: the host kernel module or the longest "
        "request rules it out.",
        fr=f"Le modèle de calcul {choix!r} ne peut pas faire tourner cette charge : le module noyau de l'hôte "
        "ou la plus longue requête l'excluent.",
    )
    justification = decision.get("rationale")
    assert isinstance(justification, str) and justification.strip(), message(
        en="The decision has no rationale: nothing says why this model, this architecture and this size.",
        fr="La décision n'a pas de justification : rien ne dit pourquoi ce modèle, cette architecture et "
        "cette taille.",
    )


def test_l_architecture_est_celle_ou_la_dependance_est_testee(brief: dict, decision: dict) -> None:
    archi = decision.get("architecture")
    assert archi in _architectures_testees(brief), message(
        en=f"The architecture {archi!r} is not one on which the native dependency has been tested.",
        fr=f"L'architecture {archi!r} n'est pas une de celles où la dépendance native a été testée.",
    )


def test_la_demande_vient_du_p95_de_la_semaine_et_de_la_croissance(brief: dict, decision: dict) -> None:
    cpu, memoire = _demande(brief)
    donnee = decision.get("sizing_demand") or {}
    ecarts = {}
    for cle, attendu in (("cpu_vcpus", cpu), ("memory_gib", memoire)):
        valeur = donnee.get(cle)
        if not isinstance(valeur, (int, float)) or not math.isclose(valeur, attendu, rel_tol=0, abs_tol=0.01):
            ecarts[cle] = valeur
    assert not ecarts, message(
        en=f"The sizing demand does not match the week-long measurements and the planned growth: {ecarts}. "
        "A peak of a few seconds is not sustained demand.",
        fr=f"La demande de dimensionnement ne correspond pas aux mesures de la semaine et à la croissance "
        f"prévue : {ecarts}. Un pic de quelques secondes n'est pas une charge soutenue.",
    )


def test_le_profil_est_le_moins_cher_qui_tient_la_demande(brief: dict, decision: dict) -> None:
    cpu, memoire = _demande(brief)
    testees = _architectures_testees(brief)
    faisables = [m for m in brief["machine_catalogue"]
                 if m["architecture"] in testees and m["vcpus"] >= cpu and m["memory_gib"] >= memoire]
    moins_cher = min(m["relative_monthly_cost_units"] for m in faisables)
    profil = next((m for m in brief["machine_catalogue"] if m["id"] == decision.get("machine_profile")), None)
    assert profil is not None, message(
        en=f"The machine profile {decision.get('machine_profile')!r} is not in the catalogue of the brief.",
        fr=f"Le profil de machine {decision.get('machine_profile')!r} n'est pas dans le catalogue du brief.",
    )
    assert profil in faisables, message(
        en=f"The profile {profil['id']} does not hold the sizing demand on a tested architecture.",
        fr=f"Le profil {profil['id']} ne tient pas la demande de dimensionnement sur une architecture testée.",
    )
    assert profil["relative_monthly_cost_units"] == moins_cher, message(
        en=f"The profile {profil['id']} holds the demand, but a compatible profile costs less.",
        fr=f"Le profil {profil['id']} tient la demande, mais un profil compatible coûte moins cher.",
    )
