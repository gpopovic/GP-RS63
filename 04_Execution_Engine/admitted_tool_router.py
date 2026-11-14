"""Fail-closed routing among explicitly admitted tool capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ToolCapability:
    tool_id: str
    admission_status: str
    capabilities: tuple[str, ...]
    permitted_data_classes: tuple[str, ...]
    permitted_modes: tuple[str, ...]
    estimated_cost: Decimal
    estimated_latency_ms: int
    evidence_reference: str


@dataclass(frozen=True)
class ToolRoute:
    selected_tool_id: str
    eligible_tool_ids: tuple[str, ...]
    fallback_tool_id: str | None
    fallback_requires_explicit_failure_decision: bool = True


def select_admitted_tool(
    *,
    required_capabilities: tuple[str, ...],
    data_class: str,
    mode: str,
    tools: tuple[ToolCapability, ...],
    explicit_fallback_tool_id: str | None = None,
) -> ToolRoute:
    """Select the lowest-cost/latency eligible tool without silent fallback."""
    if not required_capabilities or any(not item.strip() for item in required_capabilities):
        raise ValueError("required_capabilities must be non-empty")
    if not data_class.strip() or not mode.strip():
        raise ValueError("data_class and mode are required")
    identifiers = [tool.tool_id for tool in tools]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("tool IDs must be unique")
    required = set(required_capabilities)
    eligible = tuple(
        tool
        for tool in tools
        if tool.admission_status == "ADMITTED"
        and required.issubset(set(tool.capabilities))
        and data_class in tool.permitted_data_classes
        and mode in tool.permitted_modes
        and tool.estimated_cost >= 0
        and tool.estimated_latency_ms >= 0
        and bool(tool.evidence_reference.strip())
    )
    if not eligible:
        raise ValueError("no admitted tool satisfies the declared capability and data boundary")
    ordered = tuple(sorted(eligible, key=lambda item: (item.estimated_cost, item.estimated_latency_ms, item.tool_id)))
    fallback: str | None = None
    if explicit_fallback_tool_id is not None:
        fallback_match = next((item for item in ordered if item.tool_id == explicit_fallback_tool_id), None)
        if fallback_match is None:
            raise ValueError("explicit fallback must independently satisfy the same admitted route")
        if fallback_match.tool_id == ordered[0].tool_id:
            raise ValueError("fallback must differ from the selected primary tool")
        fallback = fallback_match.tool_id
    return ToolRoute(ordered[0].tool_id, tuple(item.tool_id for item in ordered), fallback)
