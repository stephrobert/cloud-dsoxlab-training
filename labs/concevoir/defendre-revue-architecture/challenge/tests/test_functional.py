"""Tests fonctionnels de « Défendre une revue d'architecture ».

Les livrables sont `challenge/work/review.json` et `challenge/work/review.md`.
Chaque attendu se déduit de `review-evidence.json` et de la grille de notation
donnée dans le README du challenge. Un test par état, et chacun échoue sur
l'état de départ (les livrables n'existent pas) :

1. les six axes sont notés selon la grille, chacun avec une preuve citée et un
   constat ;
2. les trois risques retenus sont les trois plus graves (gravité multipliée par
   probabilité), dans l'ordre ;
3. chacun porte une décision, une raison, une action, un responsable, une
   échéance, et le nom de qui l'accepte quand il est accepté ;
4. les limites des preuves sont toutes déclarées, et le rapport au comité
   reprend les six axes et les trois risques.
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "defendre-revue-architecture"
AXES = ("operational-excellence", "security", "reliability", "performance", "cost", "sovereignty")
# La note que donne la grille du README, axe par axe, d'après le type et le
# contenu des preuves du pack : 3 = test ou mesure vérifiés qui tiennent
# l'exigence ; 2 = configuration ou estimation qui la tiennent sans
# vérification ; 1 = exigence non tenue ou non évaluée ; 0 = aucune preuve.
NOTES = {
    "operational-excellence": 2,  # rebuild-config : plan et runbook, aucune reconstruction rejouée
    "security": 1,                # audit-retention : 30 jours de rétention pour 90 exigés
    "reliability": 3,             # recovery-drill : test vérifié, RTO 42 et RPO 12 sous les objectifs
    "performance": 3,             # load-test : mesure vérifiée, p95 184 ms à 65 % de CPU
    "cost": 2,                    # cost-model : estimation sous le budget, aucune facture
    "sovereignty": 1,             # sovereignty-review : juridiction et coût de sortie non évalués
}


@pytest.fixture(scope="module")
def preuves() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "review-evidence.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def revue() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "review.json"
    assert chemin.is_file(), message(
        en="review.json is missing: the review is not written down.",
        fr="review.json est absent : la revue n'est pas écrite.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"review.json is not valid JSON: {erreur}",
                            fr=f"review.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="review.json must hold an object.",
                                              fr="review.json doit contenir un objet.")
    return contenu


def _trois_plus_graves(preuves: dict) -> list[dict]:
    return sorted(preuves["risks"], key=lambda r: (-r["severity"] * r["likelihood"], r["id"]))[:3]


def test_les_six_axes_sont_notes_selon_la_grille(preuves: dict, revue: dict) -> None:
    assert revue.get("architecture") == preuves["architecture"], message(
        en=f"The review is about {revue.get('architecture')!r}, not {preuves['architecture']!r}.",
        fr=f"La revue porte sur {revue.get('architecture')!r}, pas sur {preuves['architecture']!r}.",
    )
    axes = {a.get("id"): a for a in revue.get("axes") or [] if isinstance(a, dict)}
    manquants = sorted(set(AXES) - set(axes))
    assert not manquants, message(en=f"These axes are not assessed: {manquants}.",
                                  fr=f"Ces axes ne sont pas évalués : {manquants}.")
    ecarts = {}
    for axe in AXES:
        a = axes[axe]
        cites = set(a.get("evidence_ids") or [])
        if not cites or not cites <= set(preuves["evidence"]):
            ecarts[axe] = message(en="no valid evidence cited", fr="aucune preuve valide citée")
        elif not (isinstance(a.get("finding"), str) and a["finding"].strip()):
            ecarts[axe] = message(en="no finding", fr="aucun constat")
        elif a.get("score") != NOTES[axe]:
            ecarts[axe] = message(en=f"score {a.get('score')} does not follow the grid",
                                  fr=f"la note {a.get('score')} ne suit pas la grille")
    assert not ecarts, message(
        en=f"These axes are not assessed as the grid and the evidence say: {ecarts}.",
        fr=f"Ces axes ne sont pas évalués comme le disent la grille et les preuves : {ecarts}.",
    )


def test_les_trois_risques_les_plus_graves_sont_retenus(preuves: dict, revue: dict) -> None:
    attendus = [r["id"] for r in _trois_plus_graves(preuves)]
    retenus = [r.get("id") for r in revue.get("top_risks") or [] if isinstance(r, dict)]
    assert retenus == attendus, message(
        en=f"The risks retained ({retenus}) are not the three most serious, in order of severity times "
        "likelihood.",
        fr=f"Les risques retenus ({retenus}) ne sont pas les trois plus graves, dans l'ordre de la gravité "
        "multipliée par la probabilité.",
    )


def test_chaque_risque_porte_une_decision_attribuee(preuves: dict, revue: dict) -> None:
    risques = {r["id"]: r for r in preuves["risks"]}
    attendus = [r["id"] for r in _trois_plus_graves(preuves)]
    decisions = {r.get("id"): r for r in revue.get("top_risks") or [] if isinstance(r, dict)}
    manques = {}
    for rid in attendus:
        d = decisions.get(rid) or {}
        trous = []
        if d.get("evidence_id") != risques[rid]["evidence_id"]:
            trous.append("evidence_id")
        if d.get("decision") not in ("correct", "accept", "defer"):
            trous.append("decision")
        trous += [c for c in ("reason", "action", "owner") if not (isinstance(d.get(c), str) and d[c].strip())]
        try:
            date.fromisoformat(str(d.get("due_date")))
        except ValueError:
            trous.append("due_date")
        if d.get("decision") == "accept" and not (isinstance(d.get("accepted_by"), str) and d["accepted_by"].strip()):
            trous.append("accepted_by")
        if trous:
            manques[rid] = trous
    assert not manques, message(
        en=f"These risks lack part of their decision: {manques}. A decision says what is done, why, by whom, "
        "by when, and who accepts the residual risk.",
        fr=f"Il manque une part de leur décision à ces risques : {manques}. Une décision dit ce qui est fait, "
        "pourquoi, par qui, pour quand, et qui accepte le risque résiduel.",
    )


def test_les_limites_et_le_rapport_au_comite(preuves: dict, revue: dict) -> None:
    oubliees = sorted(set(preuves["evidence_limits"]) - set(revue.get("evidence_limits") or []))
    assert not oubliees, message(
        en=f"These limits of the evidence are not declared: {oubliees}.",
        fr=f"Ces limites des preuves ne sont pas déclarées : {oubliees}.",
    )
    rapport = WORKDIR / "review.md"
    assert rapport.is_file(), message(en="review.md, the report for the architecture board, is missing.",
                                      fr="review.md, le rapport au comité d'architecture, est absent.")
    texte = rapport.read_text(encoding="utf-8")
    absents = [a for a in AXES if a not in texte]
    absents += [r["id"] for r in _trois_plus_graves(preuves) if r["id"] not in texte]
    assert not absents, message(
        en=f"The board report does not mention: {absents}.",
        fr=f"Le rapport au comité ne mentionne pas : {absents}.",
    )
