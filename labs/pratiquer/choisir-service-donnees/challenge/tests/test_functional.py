"""State-based grading for a managed data-service decision."""

from __future__ import annotations

import json

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "choisir-service-donnees"


def test_selected_service_meets_the_workload_and_team_constraints() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "data-service-brief.json").read_text(encoding="utf-8"))
    decision_path = WORKDIR / "data-service-decision.json"
    assert decision_path.is_file(), "Create data-service-decision.json from the brief."
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    workload = brief["workload"]
    team = brief["team"]
    objectives = brief["recovery_objectives"]
    service = next(
        (item for item in brief["service_catalogue"] if item["id"] == decision["service_id"]),
        None,
    )
    assert service is not None, "Select a service listed in the exercise catalogue."

    assert service["data_model"] == workload["data_model"]
    assert service["engine"] == workload["required_engine"]
    assert workload["required_major_version"] in service["major_versions"]
    assert set(workload["required_extensions"]) <= set(service["extensions"])
    assert service["monthly_cost_eur"] <= brief["monthly_budget_eur"]
    assert service["operations_hours_per_month"] <= team["database_operations_capacity_hours_per_month"]
    assert service["private_endpoint"] is True
    assert service["internet_endpoint_mandatory"] is False
    assert service["failure_domains"] >= objectives["minimum_failure_domains"]
    assert service["rpo_minutes"] <= objectives["maximum_rpo_minutes"]
    assert service["rto_minutes"] <= objectives["maximum_rto_minutes"]

    assert decision["engine"] == workload["required_engine"]
    assert decision["major_version"] == workload["required_major_version"]
    assert decision["operating_model"] == service["operating_model"]
    assert decision["private_endpoint"] is True
    assert decision["internet_exposure"] is False
    assert decision["replication"] == service["replication"]
    assert decision["failure_domains"] == service["failure_domains"]
    assert decision["rpo_minutes"] == service["rpo_minutes"]
    assert decision["rto_minutes"] == service["rto_minutes"]
    assert decision["rpo_minutes"] <= objectives["maximum_rpo_minutes"]
    assert decision["rto_minutes"] <= objectives["maximum_rto_minutes"]
    assert decision["point_in_time_recovery"] is service["point_in_time_recovery"]
    assert decision["restore_test_owner"] == "customer"
    assert isinstance(decision["restore_verification"], str) and decision["restore_verification"].strip()
    assert isinstance(decision["rationale"], str) and decision["rationale"].strip()
    assert decision["rejected_options"], "Name and explain at least one rejected service."


def test_comparison_covers_each_service_and_rejected_option_reasoning() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "data-service-brief.json").read_text(encoding="utf-8"))
    decision_path = WORKDIR / "data-service-decision.json"
    assert decision_path.is_file(), "Create data-service-decision.json with a comparison."
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    services = {item["id"] for item in brief["service_catalogue"]}
    comparison = decision["comparison"]
    assert set(comparison) == services, "Compare every service in the supplied catalogue."
    for service_id in services:
        assert isinstance(comparison[service_id], str) and comparison[service_id].strip(), (
            f"Explain the fit or rejection of {service_id}."
        )

    rejected_ids = {option["service_id"] for option in decision["rejected_options"]}
    assert rejected_ids == services - {decision["service_id"]}
    assert all(option["reason"].strip() for option in decision["rejected_options"])
