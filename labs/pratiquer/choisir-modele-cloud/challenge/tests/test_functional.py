"""State-based grading for the cloud model decision artifact."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "pratiquer-choisir-modele-cloud"


def test_decision_selects_models_and_assigns_responsibilities() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    brief_path = WORKDIR / "brief.json"
    decision_path = WORKDIR / "decision.json"
    assert brief_path.is_file(), "The workload brief is missing from the workspace."
    assert decision_path.is_file(), "Create decision.json with your model decision."

    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    decision = json.loads(decision_path.read_text(encoding="utf-8"))

    assert brief["team"]["operations_staff"] is False
    assert brief["team"]["application_maintenance"] is True
    assert brief["constraints"]["operating_system_dependency"] is False
    assert brief["constraints"]["personal_data"] is True
    assert decision["service_model"] == "paas", (
        "Choose a managed platform model: the team maintains its application "
        "but has no operations staff or operating-system dependency."
    )
    assert decision["deployment_model"] == "public", (
        "The brief gives no requirement for a private or hybrid deployment."
    )
    responsibilities = decision["responsibilities"]
    assert "managed_platform" in responsibilities["provider"]
    for responsibility in ("application", "data", "identities", "configuration"):
        assert responsibility in responsibilities["team"], (
            f"The team remains responsible for {responsibility}."
        )
    assert isinstance(decision["rationale"], str) and decision["rationale"].strip(), (
        "Explain how the chosen models follow from the workload constraints."
    )
