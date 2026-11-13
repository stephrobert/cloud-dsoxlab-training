"""State-based grading for the architecture decision record."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-architecture-cible"
AXES = (
    "monthly_cost_eur",
    "operations_days_per_month",
    "data_residency",
    "availability_zones",
    "portability",
    "performance",
)


def test_adr_comparaison_et_decision_respectent_le_brief() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief = json.loads((WORKDIR / "brief.json").read_text(encoding="utf-8"))
    decision_path = WORKDIR / "decision.json"
    assert decision_path.is_file(), "Create decision.json with the ADR and comparison."
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    comparison = decision["comparison"]
    assert set(comparison) == set(brief["options"]), (
        "Compare both complete architecture options from the brief."
    )
    for option, facts in brief["options"].items():
        assert set(comparison[option]) >= set(AXES), (
            f"The {option} comparison must cover all six required axes."
        )
        for axis in AXES:
            assert comparison[option][axis] == facts[axis], (
                f"The {option} comparison for {axis} does not match the supplied evidence."
            )

    adr = decision["adr"]
    assert set(adr["options_considered"]) == set(brief["options"])
    assert set(adr["criteria"]) == set(AXES), "The ADR must name all six decision axes."
    assert adr["decision"] == "managed_containers", (
        "The virtual-machine option exceeds the team's operations capacity."
    )
    for field in ("title", "context", "rationale", "review_condition"):
        assert isinstance(adr[field], str) and adr[field].strip(), (
            f"The ADR is missing its {field}."
        )
    assert adr["consequences"], "Record at least one consequence of the decision."
    assert adr["accepted_risks"], "Record a residual risk and its mitigation."

    requirements = brief["requirements"]
    chosen = brief["options"][adr["decision"]]
    assert chosen["monthly_cost_eur"] <= requirements["monthly_budget_eur"]
    assert chosen["operations_days_per_month"] <= requirements["max_operations_days_per_month"]
    assert chosen["data_residency"] == requirements["data_region"]
    assert chosen["availability_zones"] >= requirements["minimum_zones"]
