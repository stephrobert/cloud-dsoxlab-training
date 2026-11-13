"""Tests fonctionnels de « Concevoir l'élasticité d'un tier applicatif ».

Le livrable est `challenge/work/elasticity-plan.json`. Chaque attendu se
recalcule depuis `workload.json` (mesures, inventaire de l'état, contraintes de
conception). Un test par état, et chacun échoue sur l'état de départ (le
livrable n'existe pas) :

1. l'état qui doit survivre au remplacement d'une instance quitte l'instance,
   sans changement de code pour monter en charge ;
2. un réessai du client après la perte d'une instance ne crée pas deux
   commandes ;
3. deux contrôles de santé distincts : vivacité et disponibilité ;
4. les bornes de réplicas tiennent les contraintes, et le pic soutenu passe
   encore après la perte d'une instance, calcul à l'appui ;
5. la montée et la descente ont chacune leur métrique, leur seuil, leur
   fenêtre et leur délai, avec un écart entre les seuils et un drainage avant
   retrait ;
6. le plan dit comment le vérifier, en ajoutant puis en perdant une instance.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-elasticite"
# Ce qui survit au remplacement d'une instance : hors de l'instance.
EMPLACEMENTS_PARTAGES = {"sessions": "shared_managed_session_store", "uploads": "object_storage"}


@pytest.fixture(scope="module")
def charge() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def plan() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "elasticity-plan.json"
    assert chemin.is_file(), message(
        en="elasticity-plan.json is missing: no elasticity plan is written down.",
        fr="elasticity-plan.json est absent : aucun plan d'élasticité n'est écrit.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"elasticity-plan.json is not valid JSON: {erreur}",
                            fr=f"elasticity-plan.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="elasticity-plan.json must hold an object.",
                                              fr="elasticity-plan.json doit contenir un objet.")
    return contenu


def _texte(valeur: object) -> bool:
    return isinstance(valeur, str) and bool(valeur.strip())


def test_l_etat_quitte_l_instance(charge: dict, plan: dict) -> None:
    inventaire = charge["state_inventory"]
    etat = plan.get("state") or {}
    ecarts = {}
    for cle, partage in EMPLACEMENTS_PARTAGES.items():
        if inventaire[cle]["must_survive_instance_replacement"] and etat.get(cle) != partage:
            ecarts[cle] = etat.get(cle)
    if etat.get("orders") != inventaire["orders"]["location"]:
        ecarts["orders"] = etat.get("orders")
    if plan.get("scale_out_requires_code_change") is not charge["design_constraints"]["application_code_changes_for_scale_out"]:
        ecarts["scale_out_requires_code_change"] = plan.get("scale_out_requires_code_change")
    assert not ecarts, message(
        en=f"Some state still lives on the instance, or scaling needs code: {ecarts}. What must survive an "
        "instance replacement cannot stay in its memory or on its disk.",
        fr=f"De l'état vit encore sur l'instance, ou monter en charge demande du code : {ecarts}. Ce qui doit "
        "survivre au remplacement d'une instance ne peut rester ni dans sa mémoire ni sur son disque.",
    )


def test_un_reessai_ne_cree_pas_deux_commandes(charge: dict, plan: dict) -> None:
    attendu = "idempotency_key" if charge["state_inventory"]["orders"]["idempotency_key_supported"] else None
    donne = (plan.get("state") or {}).get("order_retry_protection")
    assert donne == attendu, message(
        en=f"Order retries are protected by {donne!r}: a client retry after an instance loss can still create "
        "a second order.",
        fr=f"Les réessais de commande sont protégés par {donne!r} : un réessai du client après la perte d'une "
        "instance peut encore créer une seconde commande.",
    )


def test_deux_controles_de_sante_distincts(charge: dict, plan: dict) -> None:
    exiges = set(charge["design_constraints"]["required_health_checks"])
    controles = plan.get("health_checks") or {}
    vides = sorted(k for k in exiges if not _texte(controles.get(k)))
    confondus = len({controles.get(k) for k in exiges}) < len(exiges)
    assert set(controles) >= exiges and not vides and not confondus, message(
        en=f"The health checks do not hold: missing or empty {vides}{', liveness and readiness are the same' if confondus else ''}. "
        "One says when to restart an instance, the other when to send it traffic.",
        fr=f"Les contrôles de santé ne tiennent pas : absents ou vides {vides}{', vivacité et disponibilité confondues' if confondus else ''}. "
        "L'un dit quand redémarrer une instance, l'autre quand lui envoyer du trafic.",
    )


def test_le_pic_passe_apres_la_perte_d_une_instance(charge: dict, plan: dict) -> None:
    w, c = charge["workload"], charge["design_constraints"]
    r = plan.get("replicas") or {}
    mini, maxi = r.get("minimum"), r.get("maximum")
    defauts = []
    if not (isinstance(mini, int) and isinstance(maxi, int) and c["minimum_instances"] <= mini < maxi <= c["maximum_instances"]):
        defauts.append(message(en=f"replicas {mini}..{maxi} outside the constraints",
                               fr=f"réplicas {mini}..{maxi} hors des contraintes"))
    else:
        restants = mini - w["minimum_failed_instances_to_tolerate"]
        capacite = restants * w["safe_requests_per_second_per_instance"]
        attendu = {
            "safe_requests_per_second_per_instance": w["safe_requests_per_second_per_instance"],
            "peak_requests_per_second_after_one_loss": w["sustained_peak_requests_per_second"],
            "capacity_after_one_loss_requests_per_second": capacite,
            "capacity_margin_after_one_loss_requests_per_second": capacite - w["sustained_peak_requests_per_second"],
        }
        faux = {k: plan.get(k) for k, v in attendu.items() if plan.get(k) != v}
        if faux:
            defauts.append(message(en=f"calculation off: {faux}", fr=f"calcul faux : {faux}"))
        if capacite < w["sustained_peak_requests_per_second"]:
            defauts.append(message(en="the floor does not hold the peak after one loss",
                                   fr="le plancher ne tient pas le pic après une perte"))
    assert not defauts, message(
        en=f"The replica floor does not survive one instance loss at the sustained peak: {defauts}.",
        fr=f"Le plancher de réplicas ne survit pas à la perte d'une instance au pic soutenu : {defauts}.",
    )


def test_les_politiques_de_scaling_sont_sures(charge: dict, plan: dict) -> None:
    c, w = charge["design_constraints"], charge["workload"]
    monte, descend = plan.get("scale_out") or {}, plan.get("scale_in") or {}
    attendu_monte = {"threshold_percent": c["scale_out_utilization_percent"], "window_minutes": c["scale_out_window_minutes"],
                     "cooldown_minutes": c["scale_out_cooldown_minutes"], "action": "add_one_instance"}
    attendu_descend = {"threshold_percent": c["scale_in_utilization_percent"], "window_minutes": c["scale_in_window_minutes"],
                       "cooldown_minutes": c["scale_in_cooldown_minutes"], "action": "drain_then_remove_one_instance",
                       "connection_drain_seconds": c["connection_drain_seconds"], "never_below_minimum": True}
    defauts = {f"scale_out.{k}": monte.get(k) for k, v in attendu_monte.items() if monte.get(k) != v}
    defauts |= {f"scale_in.{k}": descend.get(k) for k, v in attendu_descend.items() if descend.get(k) != v}
    if monte.get("metric") != "per_instance_utilization_percent" or descend.get("metric") != monte.get("metric"):
        defauts["metric"] = (monte.get("metric"), descend.get("metric"))
    if isinstance(monte.get("cooldown_minutes"), (int, float)) and monte["cooldown_minutes"] < w["instance_startup_minutes"]:
        defauts["scale_out.cooldown_minutes < startup"] = monte["cooldown_minutes"]
    assert not defauts, message(
        en=f"The scaling policies are not safe: {defauts}. Out and in each have their threshold, window and "
        "cooldown, with a gap between thresholds and a drain before removal.",
        fr=f"Les politiques de scaling ne sont pas sûres : {defauts}. La montée et la descente ont chacune "
        "leur seuil, leur fenêtre et leur délai, avec un écart entre les seuils et un drainage avant retrait.",
    )


def test_le_plan_dit_comment_le_verifier(plan: dict) -> None:
    v = plan.get("verification") or {}
    manquent = [k for k in ("add_instance", "lose_instance") if not _texte(v.get(k))]
    assert not manquent, message(
        en=f"The plan does not say how to verify it: {manquent}. A design that is never exercised by adding "
        "and losing an instance is only a hope.",
        fr=f"Le plan ne dit pas comment le vérifier : {manquent}. Une conception jamais éprouvée en ajoutant "
        "puis en perdant une instance n'est qu'un espoir.",
    )
