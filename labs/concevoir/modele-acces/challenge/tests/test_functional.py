"""State-based grading for the provider-neutral cloud access model."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "concevoir-modele-acces"


def test_modele_couvre_federation_cycle_de_vie_separation_et_audit() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    context = json.loads((WORKDIR / "access-context.json").read_text(encoding="utf-8"))
    model_path = WORKDIR / "access-model.json"
    assert model_path.is_file(), "Create access-model.json from the provider-neutral requirements."
    model = json.loads(model_path.read_text(encoding="utf-8"))

    identity = model["human_identity"]
    source = context["identity_source"]
    assert identity["source"] == source["directory"]
    assert identity["federation_protocol"].upper() == source["protocol"]
    assert identity["single_sign_on"] is source["sso_required"]
    assert identity["maximum_session_minutes"] <= source["maximum_session_minutes"]

    emergency = model["emergency_access"]
    assert len(emergency["accounts"]) >= 2, "Keep at least two individually controlled recovery accounts."
    for account in emergency["accounts"]:
        assert account["named_owner"].strip()
        assert account["mfa"] is True
        assert account["routine_use"] is False
        assert account["alert_on_use"] is True

    groups = {group["name"]: group for group in model["role_groups"]}
    for required in context["roles"]:
        assert required["name"] in groups
        assert set(required["duties"]) <= set(groups[required["name"]]["duties"])
    developers = set(groups["developers"]["duties"])
    operators = set(groups["production_operators"]["duties"])
    assert "approve_production_change" not in developers
    assert "deploy_production" not in developers
    assert "deploy_production" in operators
    separation = model["separation_of_duties"]
    assert separation["approval_and_production_deployment_use_distinct_people"] is True
    assert separation["production_access_is_temporary"] is True

    lifecycle = {item["event"]: item for item in model["lifecycle"]}
    for event in context["lifecycle_events"]:
        assert event in lifecycle
        assert lifecycle[event]["owner"].strip()
        assert lifecycle[event]["maximum_completion_hours"] > 0
    assert lifecycle["leaver"]["maximum_completion_hours"] <= 4
    assert lifecycle["recertification"]["interval_days"] <= 90

    audit = model["audit"]
    requirements = context["audit_requirements"]
    assert set(requirements["events"]) <= set(audit["events"])
    assert audit["retention_days"] >= requirements["retention_days"]
    assert audit["immutable_destination"] is requirements["immutable_destination"]
    assert audit["readers"] and set(audit["alert_on"]) >= set(requirements["alert_on"])
    assert audit["destination_owner"].strip()
