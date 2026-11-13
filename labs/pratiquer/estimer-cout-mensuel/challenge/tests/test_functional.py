"""Tests fonctionnels de « Estimer un coût cloud mensuel ».

Le livrable est `challenge/work/cost-estimate.json`. Chaque ligne attendue est
RECALCULÉE depuis la grille datée et les usages de `architecture.json`. Un test
par état, et chacun échoue sur l'état de départ (le livrable n'existe pas) :

1. une ligne par classe de calcul : instances fois heures, au prix de la classe ;
2. le stockage bloc, objet et snapshots, au Gio-mois ;
3. le trafic sortant facturable, une fois la franchise déduite ;
4. les requêtes d'API, au million ;
5. le total mensuel, dans la devise et à la date de la grille ;
6. l'annualisation, le budget, la marge restante et le verdict.
"""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, message, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "estimer-cout-mensuel"


@pytest.fixture(scope="module")
def brief() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    return json.loads((WORKDIR / "architecture.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def estimation() -> dict:
    exiger_workdir(WORKDIR, LAB_ID)
    chemin = WORKDIR / "cost-estimate.json"
    assert chemin.is_file(), message(
        en="cost-estimate.json is missing: no estimate is written down.",
        fr="cost-estimate.json est absent : aucune estimation n'est écrite.",
    )
    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        pytest.fail(message(en=f"cost-estimate.json is not valid JSON: {erreur}",
                            fr=f"cost-estimate.json n'est pas un JSON valide : {erreur}"))
    assert isinstance(contenu, dict), message(en="cost-estimate.json must hold an object.",
                                              fr="cost-estimate.json doit contenir un objet.")
    return contenu


def _attendues(brief: dict) -> dict[str, tuple[float, str, float]]:
    taux, usage = brief["price_grid"]["rates"], brief["monthly_usage"]
    lignes = {f"compute-{c['id']}": (c["instances"] * c["hours_per_instance"], "instance-hour",
                                     taux["compute_eur_per_instance_hour"][c["id"]]) for c in usage["compute"]}
    lignes["block-storage"] = (usage["block_storage_gib_month"], "GiB-month", taux["block_storage_eur_per_gib_month"])
    lignes["object-storage"] = (usage["object_storage_gib_month"], "GiB-month", taux["object_storage_eur_per_gib_month"])
    lignes["snapshot-storage"] = (usage["snapshot_storage_gib_month"], "GiB-month", taux["snapshot_storage_eur_per_gib_month"])
    lignes["egress"] = (max(0, usage["outbound_data_gib"] - taux["egress"]["included_gib_per_month"]), "GiB",
                        taux["egress"]["eur_per_billable_gib"])
    lignes["api-requests"] = (usage["api_requests_millions"], "million requests", taux["api_requests_eur_per_million"])
    return lignes


def _verifier(brief: dict, estimation: dict, ids: list[str]) -> dict:
    attendues = _attendues(brief)
    donnees = {ligne.get("id"): ligne for ligne in estimation.get("line_items") or [] if isinstance(ligne, dict)}
    ecarts = {}
    for i in ids:
        quantite, unite, prix = attendues[i]
        ligne = donnees.get(i)
        if ligne is None:
            ecarts[i] = "absent"
            continue
        faux = []
        if ligne.get("quantity") != pytest.approx(quantite):
            faux.append("quantity")
        if ligne.get("unit") != unite:
            faux.append("unit")
        if ligne.get("unit_price_eur") != pytest.approx(prix):
            faux.append("unit_price_eur")
        if ligne.get("monthly_cost_eur") != pytest.approx(quantite * prix):
            faux.append("monthly_cost_eur")
        if faux:
            ecarts[i] = faux
    return ecarts


def test_le_calcul_est_chiffre_par_classe(brief: dict, estimation: dict) -> None:
    ids = [f"compute-{c['id']}" for c in brief["monthly_usage"]["compute"]]
    ecarts = _verifier(brief, estimation, ids)
    assert not ecarts, message(
        en=f"These compute lines do not recompute from the grid and the usage: {ecarts}.",
        fr=f"Ces lignes de calcul ne se recalculent pas depuis la grille et les usages : {ecarts}.",
    )


def test_le_stockage_est_chiffre(brief: dict, estimation: dict) -> None:
    ecarts = _verifier(brief, estimation, ["block-storage", "object-storage", "snapshot-storage"])
    assert not ecarts, message(
        en=f"These storage lines do not recompute from the grid and the usage: {ecarts}.",
        fr=f"Ces lignes de stockage ne se recalculent pas depuis la grille et les usages : {ecarts}.",
    )


def test_le_trafic_sortant_deduit_la_franchise(brief: dict, estimation: dict) -> None:
    ecarts = _verifier(brief, estimation, ["egress"])
    assert not ecarts, message(
        en=f"The outbound traffic line does not recompute: {ecarts}. Only the data beyond the included "
        "allowance is billed.",
        fr=f"La ligne de trafic sortant ne se recalcule pas : {ecarts}. Seules les données au-delà de la "
        "franchise sont facturées.",
    )


def test_les_requetes_api_sont_chiffrees(brief: dict, estimation: dict) -> None:
    ecarts = _verifier(brief, estimation, ["api-requests"])
    assert not ecarts, message(
        en=f"The API requests line does not recompute: {ecarts}.",
        fr=f"La ligne des requêtes d'API ne se recalcule pas : {ecarts}.",
    )


def test_le_total_mensuel(brief: dict, estimation: dict) -> None:
    grille = brief["price_grid"]
    total = sum(q * p for q, _, p in _attendues(brief).values())
    ecarts = {}
    if estimation.get("currency") != grille["currency"]:
        ecarts["currency"] = estimation.get("currency")
    if estimation.get("price_grid_as_of") != grille["as_of"]:
        ecarts["price_grid_as_of"] = estimation.get("price_grid_as_of")
    if estimation.get("total_monthly_eur") != pytest.approx(total):
        ecarts["total_monthly_eur"] = estimation.get("total_monthly_eur")
    assert not ecarts, message(
        en=f"The monthly total does not hold: {ecarts}. An estimate states its currency and the date of its "
        "price grid, and its total is the sum of every billed line.",
        fr=f"Le total mensuel ne tient pas : {ecarts}. Une estimation dit sa devise et la date de sa grille, "
        "et son total est la somme de chaque ligne facturée.",
    )


def test_l_annualisation_et_la_marge_budgetaire(brief: dict, estimation: dict) -> None:
    total = sum(q * p for q, _, p in _attendues(brief).values())
    budget = brief["price_grid"]["monthly_budget_eur"]
    ecarts = {}
    if estimation.get("annualized_eur") != pytest.approx(total * 12):
        ecarts["annualized_eur"] = estimation.get("annualized_eur")
    if estimation.get("monthly_budget_eur") != pytest.approx(budget):
        ecarts["monthly_budget_eur"] = estimation.get("monthly_budget_eur")
    if estimation.get("budget_remaining_eur") != pytest.approx(budget - total):
        ecarts["budget_remaining_eur"] = estimation.get("budget_remaining_eur")
    if estimation.get("within_budget") is not (total <= budget):
        ecarts["within_budget"] = estimation.get("within_budget")
    assert not ecarts, message(
        en=f"The budget reading does not hold: {ecarts}.",
        fr=f"La lecture du budget ne tient pas : {ecarts}.",
    )
