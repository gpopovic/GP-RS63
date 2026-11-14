"""Validate distinct, restrained communication signatures for every Triton role."""

from __future__ import annotations

import json

from config import ROLE_COMMUNICATION_SIGNATURE_REGISTRY_PATH, ROLE_REGISTRY_PATH

ALLOWED_CADENCES = {
    "executive_calm", "analytical_structured", "constructive_challenge",
    "coaching_warm", "commercial_clear", "operational_crisp",
    "design_exploratory", "assurance_precise", "crisis_direct",
    "legal_careful", "empathetic_measured", "financial_exact",
}


def main() -> None:
    role_registry = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    signature_registry = json.loads(
        ROLE_COMMUNICATION_SIGNATURE_REGISTRY_PATH.read_text(encoding="utf-8")
    )
    roles = {member for department in role_registry["departments"] for member in department["members"]}
    profiles = signature_registry.get("profiles", {})
    if set(profiles) != roles:
        raise SystemExit(
            f"Communication-signature coverage mismatch: missing={sorted(roles - set(profiles))}; "
            f"unknown={sorted(set(profiles) - roles)}"
        )
    patterns: set[str] = set()
    for role_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise SystemExit(f"Communication signature must be an object: {role_id}")
        cadence = profile.get("cadence")
        pattern = profile.get("recognition_pattern")
        if cadence not in ALLOWED_CADENCES:
            raise SystemExit(f"Invalid communication cadence for {role_id}: {cadence}")
        if not isinstance(pattern, str) or len(pattern.strip()) < 30:
            raise SystemExit(f"Recognition pattern too short or missing: {role_id}")
        pattern_key = pattern.strip().casefold()
        if pattern_key in patterns:
            raise SystemExit(f"Duplicate recognition pattern: {role_id}")
        patterns.add(pattern_key)
    print(f"Role communication signatures valid: {len(profiles)} distinct profiles.")


if __name__ == "__main__":
    main()
