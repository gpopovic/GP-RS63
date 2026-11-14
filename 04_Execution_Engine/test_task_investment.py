"""Tests for task-investment and sourcing decision support."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from task_investment import calculate_relative_wsjf, validate_task_investment_record


def example() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "TASK_INVESTMENT_DECISION.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = example()
    assert validate_task_investment_record(payload) == []
    assert calculate_relative_wsjf(payload["relative_wsjf"]) == 4.0

    mixed_units = deepcopy(payload)
    mixed_units["monetary_cost_of_delay"] = {"low_per_day": 1, "base_per_day": 2, "high_per_day": 3, "currency": "EUR", "horizon": "30 days", "evidence_reference": "COD-001"}
    assert any("must not mix" in error for error in validate_task_investment_record(mixed_units))

    fake_protection = deepcopy(payload)
    fake_protection["protected_priority"] = True
    fake_errors = validate_task_investment_record(fake_protection)
    assert any("optional improvement" in error for error in fake_errors)
    assert any("rather than an economic score" in error for error in fake_errors)

    unprotected_mandate = deepcopy(payload)
    unprotected_mandate["obligation_class"] = "MANDATORY_EXTERNAL"
    assert any("requires protected priority" in error for error in validate_task_investment_record(unprotected_mandate))

    false_commit = deepcopy(payload)
    false_commit["decision"] = "COMMIT"
    assert any("approval evidence" in error for error in validate_task_investment_record(false_commit))

    not_ready = deepcopy(payload)
    not_ready["readiness_status"] = "NOT_READY"
    not_ready["decision"] = "COMMIT"
    assert any("COMMIT requires READY" in error for error in validate_task_investment_record(not_ready))

    no_comparison = deepcopy(payload)
    no_comparison["sourcing"]["alternatives"] = no_comparison["sourcing"]["alternatives"][:1]
    assert any("at least two alternatives" in error for error in validate_task_investment_record(no_comparison))

    inconsistent_currency = deepcopy(payload)
    inconsistent_currency["sourcing"]["alternatives"][1]["currency"] = "USD"
    assert any("comparable currency" in error for error in validate_task_investment_record(inconsistent_currency))
    print("Task investment and sourcing tests passed.")


if __name__ == "__main__":
    main()
