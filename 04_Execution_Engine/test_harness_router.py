"""Tests for deterministic, lean harness selection."""
from harness_router import select_harness


def main() -> None:
    assert select_harness("ADMIN", material_risk=False, sensitive_data=False)["harness"] == "LEAN"
    assert select_harness("DELIVERY", material_risk=False, sensitive_data=False)["role_profile"] == "standard_delivery"
    assert select_harness("CROSS_BORDER_DELIVERY", material_risk=False, sensitive_data=False)["role_profile"] == "indo_german_delivery_cell"
    assert select_harness("DELIVERY", material_risk=True, sensitive_data=False)["harness"] == "CONTROLLED"
    assert select_harness("ADMIN", material_risk=False, sensitive_data=True)["harness"] == "CONTROLLED"
    assert select_harness("CROSS_BORDER_DELIVERY", material_risk=True, sensitive_data=True)["role_profile"] == "controlled_change"
    print("Harness router tests passed.")


if __name__ == "__main__":
    main()
