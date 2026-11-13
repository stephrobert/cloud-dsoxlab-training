"""State-based grading for the architecture improvement plan."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-recommander-evolutions-architecture"


def test_recommandations_sont_verifiables_classees_et_planifiables() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    review = json.loads((WORKDIR / "review.json").read_text(encoding="utf-8"))
    plan_path = WORKDIR / "plan.json"
    assert plan_path.is_file(), "Create plan.json with one recommendation per finding."
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    findings = {finding["id"]: finding for finding in review["findings"]}
    recommendations = plan["recommendations"]
    assert {item["id"] for item in recommendations} == set(findings), (
        "Provide exactly one recommendation for each review finding."
    )
    by_id = {item["id"]: item for item in recommendations}
    expected_rank = sorted(
        findings,
        key=lambda finding_id: (
            -findings[finding_id]["severity"] * findings[finding_id]["likelihood"],
            findings[finding_id]["effort_days"],
            finding_id,
        ),
    )
    assert plan["priority_order"] == expected_rank, (
        "Rank by severity multiplied by likelihood, highest risk first."
    )

    for finding_id, finding in findings.items():
        recommendation = by_id[finding_id]
        assert recommendation["risk_score"] == finding["severity"] * finding["likelihood"]
        assert recommendation["effort_days"] == finding["effort_days"]
        assert recommendation["monthly_cost_eur"] == finding["monthly_cost_eur"]
        assert recommendation["dependencies"] == finding["dependencies"]
        for field in ("action", "expected_effect", "verification_criterion", "residual_risk"):
            assert isinstance(recommendation[field], str) and recommendation[field].strip(), (
                f"{finding_id} is missing a useful {field}."
            )
        expected_kind = (
            "quick_win"
            if (
                finding["effort_days"] <= review["scales"]["quick_win_max_effort_days"]
                and not finding["dependencies"]
                and finding["reversible"]
            )
            else "structural"
        )
        assert recommendation["kind"] == expected_kind
        accepted = recommendation["risk_acceptance"]
        assert accepted["owner"].strip() and accepted["rationale"].strip(), (
            f"{finding_id} needs a named owner and a reason for accepting its residual risk."
        )

    capacity = review["team"]["capacity_person_days_per_sprint"]
    sprints = plan["sprints"]
    completed: set[str] = set()
    assert sprints, "Schedule all work into one or more sprints."
    for sprint in sprints:
        items = sprint["items"]
        assert items, "Do not include an empty sprint."
        assert len(items) == len(set(items)), "A recommendation must appear only once in a sprint."
        assert sum(by_id[item]["effort_days"] for item in items) <= capacity
        for item in items:
            assert set(by_id[item]["dependencies"]) <= completed, (
                f"{item} is scheduled before its dependencies are complete."
            )
        completed.update(items)
    assert completed == set(findings), "The sprint plan must schedule every recommendation."
