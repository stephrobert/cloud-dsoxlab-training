"""State-based grading for a transparent monthly cloud estimate."""

from __future__ import annotations

import json

import pytest

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "estimer-cout-mensuel"


def test_estimate_covers_every_billed_category_and_recomputes() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "architecture.json").read_text(encoding="utf-8"))
    estimate_path = WORKDIR / "cost-estimate.json"
    assert estimate_path.is_file(), "Create cost-estimate.json from the supplied brief."
    estimate = json.loads(estimate_path.read_text(encoding="utf-8"))

    grid = brief["price_grid"]
    usage = brief["monthly_usage"]
    rates = grid["rates"]
    expected: dict[str, tuple[float, str, float]] = {}

    for item in usage["compute"]:
        quantity = item["instances"] * item["hours_per_instance"]
        rate = rates["compute_eur_per_instance_hour"][item["id"]]
        expected[f"compute-{item['id']}"] = (quantity, "instance-hour", rate)

    expected["block-storage"] = (
        usage["block_storage_gib_month"],
        "GiB-month",
        rates["block_storage_eur_per_gib_month"],
    )
    expected["object-storage"] = (
        usage["object_storage_gib_month"],
        "GiB-month",
        rates["object_storage_eur_per_gib_month"],
    )
    expected["snapshot-storage"] = (
        usage["snapshot_storage_gib_month"],
        "GiB-month",
        rates["snapshot_storage_eur_per_gib_month"],
    )
    billable_egress = max(
        0,
        usage["outbound_data_gib"] - rates["egress"]["included_gib_per_month"],
    )
    expected["egress"] = (
        billable_egress,
        "GiB",
        rates["egress"]["eur_per_billable_gib"],
    )
    expected["api-requests"] = (
        usage["api_requests_millions"],
        "million requests",
        rates["api_requests_eur_per_million"],
    )

    line_items = estimate["line_items"]
    assert {line["id"] for line in line_items} == set(expected), (
        "Include each compute class, storage type, billable egress and API requests once."
    )
    calculated_costs = []
    for line in line_items:
        quantity, unit, unit_price = expected[line["id"]]
        assert line["quantity"] == pytest.approx(quantity)
        assert line["unit"] == unit
        assert line["unit_price_eur"] == pytest.approx(unit_price)
        expected_cost = quantity * unit_price
        assert line["monthly_cost_eur"] == pytest.approx(expected_cost)
        calculated_costs.append(expected_cost)

    assert estimate["currency"] == grid["currency"]
    assert estimate["price_grid_as_of"] == grid["as_of"]
    assert estimate["total_monthly_eur"] == pytest.approx(sum(calculated_costs))


def test_estimate_annualizes_and_reports_budget_headroom() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "architecture.json").read_text(encoding="utf-8"))
    estimate_path = WORKDIR / "cost-estimate.json"
    assert estimate_path.is_file(), "Create cost-estimate.json with the budget decision."
    estimate = json.loads(estimate_path.read_text(encoding="utf-8"))

    monthly_total = estimate["total_monthly_eur"]
    budget = brief["price_grid"]["monthly_budget_eur"]
    assert estimate["annualized_eur"] == pytest.approx(monthly_total * 12)
    assert estimate["monthly_budget_eur"] == pytest.approx(budget)
    assert estimate["budget_remaining_eur"] == pytest.approx(budget - monthly_total)
    assert estimate["within_budget"] is (monthly_total <= budget)
