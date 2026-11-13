"""Tests fonctionnels de « Recommander et planifier des évolutions d'architecture ».

Le livrable est `challenge/work/plan.json`. Chaque attendu se recalcule depuis
`review.json` (constats, échelles, capacité de l'équipe). Un test par état, et
chacun échoue sur l'état de départ (le livrable n'existe pas) :

1. une recommandation par constat, qui reprend son score de risque, son effort,
   son coût et ses dépendances, et dit l'action, l'effet attendu, le critère de
   vérification et le risque résiduel ;
2. l'ordre de priorité suit le score de risque, du plus fort au plus faible ;
3. chaque recommandation est classée quick_win ou structural selon la règle ;
4. chaque risque résiduel a un responsable qui l'accepte, et une raison ;
5. le planning en sprints tient la capacité de l'équipe et l'ordre des
   dépendances, et place chaque recommandation une fois.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-recommander-evolutions-architecture"
TEXTES = ("action", "expected_effect", "verification_criterion", "residual_risk")


@pytest.fixture(scope="module")
def revue() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "review.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def plan() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "plan.json"
    assert chemin.is_file(), message(
        en="plan.json is missing: no recommendation is written down.",
        fr="plan.json est absent : aucune recommandation n'est écrite.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"plan.json is not valid JSON: {erreur}",
                            fr=f"plan.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="plan.json must hold an object.",
                                              fr="plan.json doit contenir un objet.")
    return contenu


def _par_id(plan: dict) -> dict:
    return {r.get("id"): r for r in plan.get("recommendations") or [] if isinstance(r, dict)}


def _texte(valeur: object) -> bool:
    return isinstance(valeur, str) and bool(valeur.strip())


def test_une_recommandation_complete_par_constat(revue: dict, plan: dict) -> None:
    constats = {c["id"]: c for c in revue["findings"]}
    recos = _par_id(plan)
    assert set(recos) == set(constats), message(
        en=f"The recommendations ({sorted(recos)}) do not match the findings one for one ({sorted(constats)}).",
        fr=f"Les recommandations ({sorted(recos)}) ne répondent pas une à une aux constats ({sorted(constats)}).",
    )
    defauts = {}
    for cid, c in constats.items():
        r = recos[cid]
        trous = []
        if r.get("risk_score") != c["severity"] * c["likelihood"]:
            trous.append("risk_score")
        trous += [k for k in ("effort_days", "monthly_cost_eur", "dependencies") if r.get(k) != c[k]]
        trous += [k for k in TEXTES if not _texte(r.get(k))]
        if trous:
            defauts[cid] = trous
    assert not defauts, message(
        en=f"These recommendations are incomplete or do not match their finding: {defauts}.",
        fr=f"Ces recommandations sont incomplètes ou ne correspondent pas à leur constat : {defauts}.",
    )


def test_l_ordre_de_priorite_suit_le_risque(revue: dict, plan: dict) -> None:
    constats = {c["id"]: c for c in revue["findings"]}
    attendu = sorted(constats, key=lambda i: (-constats[i]["severity"] * constats[i]["likelihood"],
                                              constats[i]["effort_days"], i))
    assert plan.get("priority_order") == attendu, message(
        en=f"The priority order ({plan.get('priority_order')}) does not follow the risk score, highest first.",
        fr=f"L'ordre de priorité ({plan.get('priority_order')}) ne suit pas le score de risque, du plus fort "
        "au plus faible.",
    )


def test_chaque_recommandation_est_bien_classee(revue: dict, plan: dict) -> None:
    maximum = revue["scales"]["quick_win_max_effort_days"]
    recos = _par_id(plan)
    mal = {}
    for c in revue["findings"]:
        attendu = ("quick_win" if c["effort_days"] <= maximum and not c["dependencies"] and c["reversible"]
                   else "structural")
        donne = (recos.get(c["id"]) or {}).get("kind")
        if donne != attendu:
            mal[c["id"]] = donne
    assert not mal, message(
        en=f"These recommendations are wrongly classified: {mal}. A quick win is short, has no dependency and "
        "can be undone.",
        fr=f"Ces recommandations sont mal classées : {mal}. Un gain rapide est court, sans dépendance, et "
        "réversible.",
    )


def test_chaque_risque_residuel_est_accepte(revue: dict, plan: dict) -> None:
    recos = _par_id(plan)
    sans = [c["id"] for c in revue["findings"]
            if not (_texte(((recos.get(c["id"]) or {}).get("risk_acceptance") or {}).get("owner"))
                    and _texte(((recos.get(c["id"]) or {}).get("risk_acceptance") or {}).get("rationale")))]
    assert not sans, message(
        en=f"Nobody accepts the residual risk of: {sans}. Each one needs a named owner and a reason.",
        fr=f"Personne n'accepte le risque résiduel de : {sans}. Chacun demande un responsable nommé et une "
        "raison.",
    )


def test_le_planning_tient_la_capacite_et_les_dependances(revue: dict, plan: dict) -> None:
    constats = {c["id"]: c for c in revue["findings"]}
    capacite = revue["team"]["capacity_person_days_per_sprint"]
    sprints = plan.get("sprints") or []
    termines: set[str] = set()
    vus: list[str] = []
    defauts = []
    for s in sprints:
        items = [i for i in (s.get("items") or []) if i in constats] if isinstance(s, dict) else []
        if not items:
            defauts.append(message(en=f"empty sprint {s.get('name') if isinstance(s, dict) else s}",
                                   fr=f"sprint vide {s.get('name') if isinstance(s, dict) else s}"))
            continue
        charge = sum(constats[i]["effort_days"] for i in items)
        if charge > capacite:
            defauts.append(message(en=f"{s.get('name')} holds {charge} person-days for {capacite}",
                                   fr=f"{s.get('name')} porte {charge} jours-personne pour {capacite}"))
        for i in items:
            avant = set(constats[i]["dependencies"]) - termines
            if avant:
                defauts.append(message(en=f"{i} starts before {sorted(avant)}", fr=f"{i} commence avant {sorted(avant)}"))
        termines.update(items)
        vus += items
    oublies = sorted(set(constats) - set(vus))
    doubles = sorted({i for i in vus if vus.count(i) > 1})
    if oublies:
        defauts.append(message(en=f"not scheduled: {oublies}", fr=f"non planifiés : {oublies}"))
    if doubles:
        defauts.append(message(en=f"scheduled twice: {doubles}", fr=f"planifiés deux fois : {doubles}"))
    assert sprints and not defauts, message(
        en=f"The sprint plan does not hold: {defauts or 'no sprint'}.",
        fr=f"Le planning en sprints ne tient pas : {defauts or 'aucun sprint'}.",
    )
