"""State-based grading for the compute model and sizing decision."""

from __future__ import annotations

import json

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "choisir-modele-calcul"


def test_model_and_architecture_follow_runtime_constraints() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))
    decision_path = WORKDIR / "compute-decision.json"
    assert decision_path.is_file(), "Create compute-decision.json from the workload brief."
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    workload = brief["workload"]
    models = brief["compute_models"]
    assert decision["compute_model"] == "virtual_machine", (
        "The workload requires a custom host kernel module."
    )
    assert models[decision["compute_model"]]["supports_custom_host_kernel_module"] is True
    assert decision["architecture"] == "x86_64", (
        "The native dependency has only been tested on x86_64."
    )
    assert decision["architecture"] in workload["native_dependencies"][0]["tested_architectures"]
    assert isinstance(decision["rationale"], str) and decision["rationale"].strip()

    function_limit = models["function"]["maximum_request_duration_minutes"]
    assert workload["maximum_request_duration_minutes"] > function_limit


def test_size_uses_weekly_p95_growth_compatibility_and_least_cost_profile() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "workload.json").read_text(encoding="utf-8"))
    decision_path = WORKDIR / "compute-decision.json"
    assert decision_path.is_file(), "Create compute-decision.json with the measured sizing."
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    measurements = brief["measurements"]
    p95 = measurements["p95"]
    growth = 1 + measurements["planned_growth_percent"] / 100
    required_cpu = p95["cpu_vcpus_used"] * growth
    required_memory = p95["memory_gib_used"] * growth
    sizing = decision["sizing_demand"]
    assert sizing["cpu_vcpus"] == required_cpu
    assert sizing["memory_gib"] == required_memory
    assert measurements["period_days"] >= 7

    profile = next(
        item for item in brief["machine_catalogue"]
        if item["id"] == decision["machine_profile"]
    )
    assert profile["architecture"] == decision["architecture"]
    assert profile["vcpus"] >= required_cpu
    assert profile["memory_gib"] >= required_memory

    feasible = [
        item for item in brief["machine_catalogue"]
        if (
            item["architecture"] in brief["workload"]["native_dependencies"][0]["tested_architectures"]
            and item["vcpus"] >= required_cpu
            and item["memory_gib"] >= required_memory
        )
    ]
    cheapest_cost = min(item["relative_monthly_cost_units"] for item in feasible)
    assert profile["relative_monthly_cost_units"] == cheapest_cost, (
        "Choose the least-cost compatible profile that meets both p95 demands after growth."
    )
    assert profile["id"] != measurements["current_profile"], (
        "The existing oversized profile is not the least-cost feasible choice."
    )
