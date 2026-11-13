"""State-based grading for the evidence-backed architecture review."""

from __future__ import annotations

import json
from datetime import date

from conftest import exiger_workdir, workdir_lab

WORKDIR = workdir_lab(__file__)
LAB_ID = "defendre-revue-architecture"
EXPECTED_SCORES = {
    "operational-excellence": 2,
    "security": 1,
    "reliability": 3,
    "performance": 3,
    "cost": 2,
    "sovereignty": 1,
}


def test_review_cites_evidence_and_uses_the_six_axes() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    evidence = json.loads((WORKDIR / "review-evidence.json").read_text(encoding="utf-8"))
    review_path = WORKDIR / "review.json"
    assert review_path.is_file(), "Create review.json with the scored architecture review."
    review = json.loads(review_path.read_text(encoding="utf-8"))

    assert review["architecture"] == evidence["architecture"]
    assert date.fromisoformat(review["review_date"]) >= date.fromisoformat(evidence["review_date"])
    axes = review["axes"]
    assert {item["id"] for item in axes} == set(EXPECTED_SCORES)
    for item in axes:
        axis_id = item["id"]
        assert item["score"] == EXPECTED_SCORES[axis_id], (
            f"Reassess {axis_id} from the evidence and the 0-3 rubric."
        )
        assert item["evidence_ids"], f"Cite evidence for {axis_id}."
        assert set(item["evidence_ids"]) <= set(evidence["evidence"])
        assert isinstance(item["finding"], str) and item["finding"].strip()

        if item["score"] == 3:
            assert any(
                evidence["evidence"][evidence_id].get("verified") is True
                and evidence["evidence"][evidence_id]["kind"] in ("test", "measurement")
                for evidence_id in item["evidence_ids"]
            ), f"A score of 3 for {axis_id} requires a dated test or measurement."


def test_review_prioritizes_three_risks_and_records_accountable_decisions() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    evidence = json.loads((WORKDIR / "review-evidence.json").read_text(encoding="utf-8"))
    review_path = WORKDIR / "review.json"
    assert review_path.is_file(), "Create review.json with the risk decisions."
    review = json.loads(review_path.read_text(encoding="utf-8"))

    ranked_risks = sorted(
        evidence["risks"],
        key=lambda risk: (-risk["severity"] * risk["likelihood"], risk["id"]),
    )[:3]
    decisions = review["top_risks"]
    assert [item["id"] for item in decisions] == [risk["id"] for risk in ranked_risks]
    for item in decisions:
        risk = next(risk for risk in evidence["risks"] if risk["id"] == item["id"])
        assert item["evidence_id"] == risk["evidence_id"]
        assert item["decision"] in ("correct", "accept", "defer")
        assert isinstance(item["reason"], str) and item["reason"].strip()
        assert isinstance(item["action"], str) and item["action"].strip()
        assert item["owner"].strip(), f"Name an accountable owner for {item['id']}."
        date.fromisoformat(item["due_date"])
        if item["decision"] == "accept":
            assert item["accepted_by"].strip(), "Name who accepts each residual risk."


def test_report_and_evidence_limits_are_present() -> None:
    exiger_workdir(WORKDIR, LAB_ID)
    evidence = json.loads((WORKDIR / "review-evidence.json").read_text(encoding="utf-8"))
    review_path = WORKDIR / "review.json"
    report_path = WORKDIR / "review.md"
    assert review_path.is_file(), "Create review.json before writing the report."
    assert report_path.is_file(), "Write review.md for the architecture board."
    review = json.loads(review_path.read_text(encoding="utf-8"))
    report = report_path.read_text(encoding="utf-8")

    assert set(evidence["evidence_limits"]) <= set(review["evidence_limits"])
    assert review["evidence_limits"]
    for axis in EXPECTED_SCORES:
        assert axis in report, f"The report is missing the {axis} assessment."
    for risk in review["top_risks"]:
        assert risk["id"] in report, f"The report is missing risk {risk['id']}."
