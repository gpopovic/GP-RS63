"""Tests for admitted capability routing and explicit fallback."""

from decimal import Decimal

from admitted_tool_router import ToolCapability, select_admitted_tool


def tool(identifier: str, status: str, cost: str, latency: int, data: tuple[str, ...] = ("PUBLIC",)) -> ToolCapability:
    return ToolCapability(
        tool_id=identifier,
        admission_status=status,
        capabilities=("document-read",),
        permitted_data_classes=data,
        permitted_modes=("READ_ONLY",),
        estimated_cost=Decimal(cost),
        estimated_latency_ms=latency,
        evidence_reference=f"evidence://{identifier}/admission",
    )


def main() -> None:
    tools = (tool("FAST", "ADMITTED", "0.01", 100), tool("FALLBACK", "ADMITTED", "0.02", 200), tool("CHEAP_UNREVIEWED", "INTAKE", "0", 10))
    route = select_admitted_tool(
        required_capabilities=("document-read",),
        data_class="PUBLIC",
        mode="READ_ONLY",
        tools=tools,
        explicit_fallback_tool_id="FALLBACK",
    )
    assert route.selected_tool_id == "FAST"
    assert route.eligible_tool_ids == ("FAST", "FALLBACK")
    assert route.fallback_requires_explicit_failure_decision is True

    try:
        select_admitted_tool(
            required_capabilities=("document-read",),
            data_class="CONFIDENTIAL",
            mode="READ_ONLY",
            tools=tools,
        )
    except ValueError as error:
        assert "no admitted tool" in str(error)
    else:
        raise AssertionError("an unapproved data route must fail closed")
    print("Admitted tool routing tests passed.")


if __name__ == "__main__":
    main()
