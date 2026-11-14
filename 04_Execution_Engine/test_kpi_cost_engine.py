"""Smoke tests for KPI-profile coverage and transparent cost forecasting."""

from __future__ import annotations

import json

from config import TRITON_ROOT
from kpi_cost_engine import forecast_hourly_cost, load_role_kpi_profile


def main() -> None:
    registry = json.loads((TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json").read_text())
    roles = [role for department in registry["departments"] for role in department["members"]]
    assert all(load_role_kpi_profile(role)["functional"] for role in roles)
    forecast = forecast_hourly_cost(planned_hours=10, hourly_cost_eur=50)
    assert forecast.base_cost_eur == 500
    assert forecast.reserve_eur == 100
    assert forecast.forecast_at_completion_eur == 600
    print(f"KPI coverage validated for {len(roles)} roles; cost forecast smoke test passed.")


if __name__ == "__main__":
    main()
