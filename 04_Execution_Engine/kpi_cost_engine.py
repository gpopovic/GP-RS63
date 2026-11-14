"""Resolve role KPI profiles and calculate transparent cost forecasts."""

from __future__ import annotations

from dataclasses import dataclass

from config import load_role_kpi_profile


@dataclass(frozen=True)
class CostForecast:
    """A base estimate and its separately visible risk reserve."""

    base_cost_eur: float
    reserve_eur: float
    forecast_at_completion_eur: float


def forecast_hourly_cost(
    planned_hours: float,
    hourly_cost_eur: float,
    reserve_rate: float = 0.20,
) -> CostForecast:
    """Calculate a transparent forecast without concealing contingency in the base."""
    if planned_hours < 0 or hourly_cost_eur < 0:
        raise ValueError("Planned hours and hourly cost must be non-negative.")
    if not 0 <= reserve_rate <= 1:
        raise ValueError("reserve_rate must be between zero and one.")
    base = planned_hours * hourly_cost_eur
    reserve = base * reserve_rate
    return CostForecast(base, reserve, base + reserve)


def forecast_cloud_token_cost(
    planned_input_tokens: int,
    planned_output_tokens: int,
    input_eur_per_million: float,
    output_eur_per_million: float,
    reserve_rate: float = 0.20,
) -> CostForecast:
    """Calculate a cloud-model forecast from an approved provider price card."""
    if min(planned_input_tokens, planned_output_tokens) < 0:
        raise ValueError("Planned token counts must be non-negative.")
    base = (
        planned_input_tokens * input_eur_per_million / 1_000_000
        + planned_output_tokens * output_eur_per_million / 1_000_000
    )
    return forecast_hourly_cost(1.0, base, reserve_rate)
