"""State-based grading for an elasticity design artifact."""

from __future__ import annotations

import json

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-elasticite"


def test_plan_externalizes_state_and_preserves_retry_safety() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))
    plan_path = WORKDIR / "elasticity-plan.json"
    assert plan_path.is_file(), "Create elasticity-plan.json from the workload evidence."
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    inventory = brief["state_inventory"]
    assert inventory["sessions"]["must_survive_instance_replacement"] is True
    assert plan["state"]["sessions"] == "shared_managed_session_store"
    assert inventory["uploads"]["must_survive_instance_replacement"] is True
    assert plan["state"]["uploads"] == "object_storage"
    assert plan["state"]["orders"] == inventory["orders"]["location"]
    assert inventory["orders"]["idempotency_key_supported"] is True
    assert plan["state"]["order_retry_protection"] == "idempotency_key"
    assert brief["design_constraints"]["application_code_changes_for_scale_out"] is False
    assert plan["scale_out_requires_code_change"] is False

    checks = brief["design_constraints"]["required_health_checks"]
    assert set(plan["health_checks"]) == set(checks)
    assert plan["health_checks"]["readiness"] != plan["health_checks"]["liveness"]
    assert all(
        isinstance(description, str) and description.strip()
        for description in plan["health_checks"].values()
    )
    assert isinstance(plan["verification"]["add_instance"], str)
    assert plan["verification"]["add_instance"].strip()
    assert isinstance(plan["verification"]["lose_instance"], str)
    assert plan["verification"]["lose_instance"].strip()


def test_replica_floor_survives_one_loss_at_sustained_peak() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))
    plan_path = WORKDIR / "elasticity-plan.json"
    assert plan_path.is_file(), "Create elasticity-plan.json with a loss-capacity calculation."
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    workload = brief["workload"]
    constraints = brief["design_constraints"]
    replicas = plan["replicas"]
    assert replicas["minimum"] >= constraints["minimum_instances"]
    assert replicas["maximum"] <= constraints["maximum_instances"]
    assert replicas["minimum"] < replicas["maximum"]
    assert replicas["minimum"] - workload["minimum_failed_instances_to_tolerate"] >= 1
    assert replicas["minimum"] <= workload["current_instances"]

    capacity = plan["safe_requests_per_second_per_instance"]
    assert capacity == workload["safe_requests_per_second_per_instance"]
    surviving_instances = replicas["minimum"] - workload["minimum_failed_instances_to_tolerate"]
    surviving_capacity = surviving_instances * capacity
    assert plan["peak_requests_per_second_after_one_loss"] == workload[
        "sustained_peak_requests_per_second"
    ]
    assert plan["capacity_after_one_loss_requests_per_second"] == surviving_capacity
    assert plan["capacity_margin_after_one_loss_requests_per_second"] == (
        surviving_capacity - workload["sustained_peak_requests_per_second"]
    )
    assert surviving_capacity >= workload["sustained_peak_requests_per_second"]


def test_scale_policies_have_hysteresis_windows_and_safe_drain() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))
    plan_path = WORKDIR / "elasticity-plan.json"
    assert plan_path.is_file(), "Create elasticity-plan.json with safe scale policies."
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    constraints = brief["design_constraints"]
    scale_out = plan["scale_out"]
    scale_in = plan["scale_in"]
    assert scale_out["metric"] == "per_instance_utilization_percent"
    assert scale_in["metric"] == scale_out["metric"]
    assert scale_out["threshold_percent"] == constraints["scale_out_utilization_percent"]
    assert scale_in["threshold_percent"] == constraints["scale_in_utilization_percent"]
    assert scale_in["threshold_percent"] < scale_out["threshold_percent"]
    assert scale_out["window_minutes"] == constraints["scale_out_window_minutes"]
    assert scale_in["window_minutes"] == constraints["scale_in_window_minutes"]
    assert scale_out["cooldown_minutes"] == constraints["scale_out_cooldown_minutes"]
    assert scale_in["cooldown_minutes"] == constraints["scale_in_cooldown_minutes"]
    assert scale_out["cooldown_minutes"] >= brief["workload"]["instance_startup_minutes"]
    assert scale_out["action"] == "add_one_instance"
    assert scale_in["action"] == "drain_then_remove_one_instance"
    assert scale_in["connection_drain_seconds"] == constraints["connection_drain_seconds"]
    assert scale_in["never_below_minimum"] is True
