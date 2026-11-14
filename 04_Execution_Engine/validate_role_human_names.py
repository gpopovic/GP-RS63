"""Validate stable fictional human-style names for every canonical Triton role."""

from __future__ import annotations

import json

from config import ROLE_HUMAN_NAME_REGISTRY_PATH, ROLE_REGISTRY_PATH


def main() -> None:
    role_registry = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    name_registry = json.loads(ROLE_HUMAN_NAME_REGISTRY_PATH.read_text(encoding="utf-8"))
    roles = {
        member
        for department in role_registry["departments"]
        for member in department["members"]
    }
    profiles = name_registry.get("profiles", {})
    missing = sorted(roles - set(profiles))
    unknown = sorted(set(profiles) - roles)
    if missing or unknown:
        raise SystemExit(f"Human-name registry coverage mismatch: missing={missing}; unknown={unknown}")

    display_names: set[str] = set()
    preferred_names: set[str] = set()
    for role_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise SystemExit(f"Human-name profile must be an object: {role_id}")
        display_name = profile.get("display_name")
        preferred = profile.get("preferred_address")
        if not isinstance(display_name, str) or not display_name.strip():
            raise SystemExit(f"Missing display_name: {role_id}")
        if not isinstance(preferred, str) or not preferred.strip():
            raise SystemExit(f"Missing preferred_address: {role_id}")
        display_key = display_name.strip().casefold()
        preferred_key = preferred.strip().casefold()
        if display_key in display_names:
            raise SystemExit(f"Duplicate human display name: {display_name}")
        if preferred_key in preferred_names:
            raise SystemExit(f"Duplicate preferred address: {preferred}")
        display_names.add(display_key)
        preferred_names.add(preferred_key)

    if profiles["Executive_Steward_and_Operations_Guard"]["preferred_address"] != "Pepper":
        raise SystemExit("Pepper identity must remain stable.")
    if profiles["Chief_Engineer_and_Systems_Architect"]["preferred_address"] != "Jarvis":
        raise SystemExit("Jarvis identity must remain stable.")
    print(f"Human-name registry valid: {len(profiles)} unique fictional work identities.")


if __name__ == "__main__":
    main()
