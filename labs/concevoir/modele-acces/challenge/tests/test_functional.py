"""Tests fonctionnels de « Concevoir le modèle d'accès ».

Le livrable est `challenge/work/access-model.json`, un modèle indépendant du
fournisseur. Chaque attendu se lit dans `access-context.json`. Les tests
inspectent le modèle produit ; ils ne prouvent pas qu'un service IAM réel
l'applique. Un test par état, et chacun échoue sur l'état de départ (le livrable
n'existe pas) :

1. les identités humaines viennent de l'annuaire, fédérées par le protocole
   demandé, en SSO, avec une session au plus aussi longue que l'exigence ;
2. au moins deux comptes d'urgence, chacun nominatif, sous MFA, hors usage
   courant, et qui alerte quand il sert ;
3. chaque rôle a ses tâches, les développeurs n'approuvent ni ne déploient en
   production, et l'approbation et le déploiement passent par deux personnes ;
4. chaque événement du cycle de vie a un responsable et un délai, et le départ
   et la recertification tiennent les exigences du contexte ;
5. l'audit couvre les événements exigés, les garde assez longtemps sur une
   destination immuable, a des lecteurs, un responsable, et alerte où il faut.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-modele-acces"


@pytest.fixture(scope="module")
def contexte() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "access-context.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def modele() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "access-model.json"
    assert chemin.is_file(), message(
        en="access-model.json is missing: no access model is written down.",
        fr="access-model.json est absent : aucun modèle d'accès n'est écrit.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"access-model.json is not valid JSON: {erreur}",
                            fr=f"access-model.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="access-model.json must hold an object.",
                                              fr="access-model.json doit contenir un objet.")
    return contenu


def _texte(valeur: object) -> bool:
    return isinstance(valeur, str) and bool(valeur.strip())


def test_les_identites_humaines_sont_federees(contexte: dict, modele: dict) -> None:
    source = contexte["identity_source"]
    identite = modele.get("human_identity") or {}
    ecarts = []
    if identite.get("source") != source["directory"]:
        ecarts.append("source")
    if str(identite.get("federation_protocol", "")).upper() != source["protocol"].upper():
        ecarts.append("federation_protocol")
    if identite.get("single_sign_on") is not source["sso_required"]:
        ecarts.append("single_sign_on")
    duree = identite.get("maximum_session_minutes")
    if not isinstance(duree, (int, float)) or not 0 < duree <= source["maximum_session_minutes"]:
        ecarts.append("maximum_session_minutes")
    assert not ecarts, message(
        en=f"The human identity does not follow the identity source of the context: {ecarts}.",
        fr=f"L'identité humaine ne suit pas la source d'identités du contexte : {ecarts}.",
    )


def test_les_comptes_d_urgence_sont_controles(modele: dict) -> None:
    comptes = (modele.get("emergency_access") or {}).get("accounts") or []
    assert len(comptes) >= 2, message(
        en=f"{len(comptes)} emergency account(s): one alone is lost with its owner, or used out of habit.",
        fr=f"{len(comptes)} compte(s) d'urgence : un seul se perd avec son titulaire, ou sert par habitude.",
    )
    proprietaires = [c.get("named_owner") for c in comptes]
    defauts = {}
    for i, c in enumerate(comptes):
        trous = [] if _texte(c.get("named_owner")) else ["named_owner"]
        trous += [k for k, v in (("mfa", True), ("routine_use", False), ("alert_on_use", True)) if c.get(k) is not v]
        if trous:
            defauts[i] = trous
    assert not defauts and len(set(proprietaires)) == len(proprietaires), message(
        en=f"The emergency accounts are not individually controlled: {defauts or 'same owner twice'}. Each one "
        "belongs to a named person, uses MFA, stays out of routine use, and raises an alert when used.",
        fr=f"Les comptes d'urgence ne sont pas contrôlés un par un : {defauts or 'même titulaire deux fois'}. "
        "Chacun appartient à une personne nommée, passe par la MFA, reste hors usage courant, et alerte quand "
        "il sert.",
    )


def test_les_roles_separent_approbation_et_deploiement(contexte: dict, modele: dict) -> None:
    groupes = {g.get("name"): set(g.get("duties") or []) for g in modele.get("role_groups") or [] if isinstance(g, dict)}
    manques = {r["name"]: sorted(set(r["duties"]) - groupes.get(r["name"], set())) for r in contexte["roles"]}
    manques = {k: v for k, v in manques.items() if v}
    assert not manques, message(
        en=f"These roles lack duties the context gives them: {manques}.",
        fr=f"Il manque à ces rôles des tâches que le contexte leur donne : {manques}.",
    )
    trop = sorted(groupes.get("developers", set()) & {"approve_production_change", "deploy_production"})
    separation = modele.get("separation_of_duties") or {}
    non_separe = [k for k in ("approval_and_production_deployment_use_distinct_people",
                              "production_access_is_temporary") if separation.get(k) is not True]
    assert not trop and not non_separe, message(
        en=f"Duties are not separated: developers hold {trop or 'nothing extra'}, and these rules are not "
        f"set: {non_separe or 'none'}. Whoever approves a production change does not deploy it alone.",
        fr=f"Les tâches ne sont pas séparées : les développeurs ont {trop or 'rien de plus'}, et ces règles ne "
        f"sont pas posées : {non_separe or 'aucune'}. Qui approuve un changement en production ne le "
        "déploie pas seul.",
    )


def test_le_cycle_de_vie_a_des_responsables_et_des_delais(contexte: dict, modele: dict) -> None:
    exigences = contexte["lifecycle_requirements"]
    evenements = {e.get("event"): e for e in modele.get("lifecycle") or [] if isinstance(e, dict)}
    defauts = {}
    for nom in contexte["lifecycle_events"]:
        e = evenements.get(nom) or {}
        trous = [] if _texte(e.get("owner")) else ["owner"]
        heures = e.get("maximum_completion_hours")
        if not isinstance(heures, (int, float)) or heures <= 0:
            trous.append("maximum_completion_hours")
        if trous:
            defauts[nom] = trous
    depart = (evenements.get("leaver") or {}).get("maximum_completion_hours")
    if isinstance(depart, (int, float)) and depart > exigences["leaver_maximum_hours"]:
        defauts.setdefault("leaver", []).append(f"> {exigences['leaver_maximum_hours']} h")
    intervalle = (evenements.get("recertification") or {}).get("interval_days")
    if not isinstance(intervalle, (int, float)) or not 0 < intervalle <= exigences["recertification_maximum_interval_days"]:
        defauts.setdefault("recertification", []).append("interval_days")
    assert not defauts, message(
        en=f"The lifecycle does not hold: {defauts}. Each event has an owner and a deadline, within the "
        "requirements of the context.",
        fr=f"Le cycle de vie ne tient pas : {defauts}. Chaque événement a un responsable et un délai, dans "
        "les exigences du contexte.",
    )


def test_l_audit_tient_les_exigences(contexte: dict, modele: dict) -> None:
    exige = contexte["audit_requirements"]
    audit = modele.get("audit") or {}
    defauts = []
    if not set(exige["events"]) <= set(audit.get("events") or []):
        defauts.append("events")
    if not isinstance(audit.get("retention_days"), (int, float)) or audit["retention_days"] < exige["retention_days"]:
        defauts.append("retention_days")
    if audit.get("immutable_destination") is not exige["immutable_destination"]:
        defauts.append("immutable_destination")
    if not audit.get("readers"):
        defauts.append("readers")
    if not set(exige["alert_on"]) <= set(audit.get("alert_on") or []):
        defauts.append("alert_on")
    if not _texte(audit.get("destination_owner")):
        defauts.append("destination_owner")
    assert not defauts, message(
        en=f"The audit does not meet the requirements of the context: {defauts}.",
        fr=f"L'audit ne tient pas les exigences du contexte : {defauts}.",
    )
