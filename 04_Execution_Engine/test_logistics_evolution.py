"""Tests for constrained logistics evolution proposals."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from logistics_evolution import validate_logistics_evolution_experiment


def example() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "LOGISTICS_EVOLUTION_EXPERIMENT.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_logistics_evolution_experiment(example()) == []

    self_audit = deepcopy(example())
    self_audit["independent_auditor"] = "Release_and_Integration_Manager"
    assert any("independent_auditor" in error for error in validate_logistics_evolution_experiment(self_audit))

    two_mutations = deepcopy(example())
    two_mutations["challenger_vector"]["wip_capacity"] = 3
    assert any("exactly the declared one" in error for error in validate_logistics_evolution_experiment(two_mutations))

    broken_weights = deepcopy(example())
    broken_weights["challenger_vector"]["queue_weights"]["aging"] = 0.50
    assert any("sum to 1.0" in error for error in validate_logistics_evolution_experiment(broken_weights))

    no_guardrail = deepcopy(example())
    for objective in no_guardrail["objective_vector"]:
        objective["protected_guardrail"] = False
    assert any("protected guardrail" in error for error in validate_logistics_evolution_experiment(no_guardrail))

    unsafe_scope = deepcopy(example())
    unsafe_scope["uncontrolled_high_consequence_work"] = True
    assert any("high-consequence" in error for error in validate_logistics_evolution_experiment(unsafe_scope))

    auto_activation = deepcopy(example())
    auto_activation["automatic_activation"] = True
    assert any("automatic_activation" in error for error in validate_logistics_evolution_experiment(auto_activation))
    print("Logistics evolution experiment tests passed.")


if __name__ == "__main__":
    main()
