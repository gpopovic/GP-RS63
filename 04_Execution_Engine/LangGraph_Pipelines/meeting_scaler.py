"""Recommend a lean, evidence-led meeting set from current delivery conditions."""

from __future__ import annotations

from typing import Literal, TypedDict

DeliveryState = Literal["GREEN", "AMBER", "RED"]


class MeetingScalingInput(TypedDict):
    """Bounded operating inputs; capacity must account for approved leave and holidays."""

    sprint_length_days: int
    feature_team_count: int
    active_customers: int
    external_parties: int
    delivery_state: DeliveryState
    available_capacity_fraction: float
    material_investment_decision: bool
    sow_decision_required: bool
    material_change_required: bool


class MeetingScalingRecommendation(TypedDict):
    """Traceable meeting recommendations without scheduling or changing any records."""

    meeting_ids: list[str]
    capacity_mode: Literal["NORMAL", "REDUCED_SCOPE", "CRITICAL_ONLY"]
    coordination_mode: Literal["ASYNC_FIRST", "EVIDENCE_ROUND_THEN_DECISION", "INCIDENT_COMMAND"]
    rationale: list[str]


def recommend_meetings(context: MeetingScalingInput) -> MeetingScalingRecommendation:
    """Select the smallest relevant meeting set for the current planning cycle."""
    if context["sprint_length_days"] < 1:
        raise ValueError("sprint_length_days must be at least one.")
    if context["feature_team_count"] < 1 or context["active_customers"] < 0:
        raise ValueError("Team and customer counts are invalid.")
    if not 0.0 <= context["available_capacity_fraction"] <= 1.0:
        raise ValueError("available_capacity_fraction must be between zero and one.")

    meetings = ["feature_team_sprint_planning", "feature_team_sprint_review", "feature_team_retrospective"]
    rationale = ["A feature team needs one planning, review, and retrospective loop per sprint."]
    coordination_mode: MeetingScalingRecommendation["coordination_mode"] = "ASYNC_FIRST"

    if context["feature_team_count"] > 1:
        meetings.append("nexus_integration_review")
        rationale.append("Multiple teams require an integrated-increment dependency review.")
    if context["active_customers"] > 0:
        meetings.append("customer_delivery_steering")
        rationale.append("Active customer commitments require a bounded customer steering path.")
    if context["delivery_state"] in {"AMBER", "RED"}:
        meetings.append("weekly_delivery_quality_review")
        rationale.append("Delivery evidence is not GREEN; recovery and quality decisions need a weekly forum.")
    if context["delivery_state"] == "RED":
        meetings.append("event_triggered_crisis_command")
        coordination_mode = "INCIDENT_COMMAND"
        rationale.append("RED state requires containment before routine ceremony.")
    if context["material_investment_decision"]:
        meetings.append("biweekly_feature_investment_review")
        rationale.append("Material investment needs an option decision before capacity commitment.")
    if context["sow_decision_required"]:
        meetings.append("event_triggered_sow_review")
        rationale.append("A Statement of Work requires commercial, delivery, and control review before commitment.")
    if context["material_change_required"]:
        meetings.append("event_triggered_change_control_board")
        coordination_mode = "EVIDENCE_ROUND_THEN_DECISION"
        rationale.append("A material baseline change requires controlled impact assessment and a human decision.")

    capacity = context["available_capacity_fraction"]
    if capacity < 0.70:
        capacity_mode: MeetingScalingRecommendation["capacity_mode"] = "CRITICAL_ONLY"
        rationale.append("Planned available capacity is below 70%; restrict commitment to critical and recovery work.")
    elif capacity < 0.85:
        capacity_mode = "REDUCED_SCOPE"
        rationale.append("Planned available capacity is below 85%; reduce scope and confirm deputy coverage.")
    else:
        capacity_mode = "NORMAL"

    if context["external_parties"] > 3 and coordination_mode == "ASYNC_FIRST":
        coordination_mode = "EVIDENCE_ROUND_THEN_DECISION"
        rationale.append("More than three external parties requires written evidence before a decision forum.")

    return {
        "meeting_ids": list(dict.fromkeys(meetings)),
        "capacity_mode": capacity_mode,
        "coordination_mode": coordination_mode,
        "rationale": rationale,
    }
