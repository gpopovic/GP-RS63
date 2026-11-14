"""Audit role loading, stable work identities, and communication signatures."""

from config import (
    load_markdown_role,
    load_role_communication_signature,
    load_role_human_identity,
    load_role_instructions,
)


def main() -> None:
    for role_id in (
        "Executive_Steward_and_Operations_Guard",
        "Chief_Engineer_and_Systems_Architect",
        "Quality_Manager",
    ):
        markdown = load_markdown_role(role_id)
        assert markdown
        assert load_markdown_role(f"{role_id}.md") == markdown

        identity = load_role_human_identity(role_id)
        signature = load_role_communication_signature(role_id)
        instructions = load_role_instructions(role_id)
        assert identity["display_name"] in instructions
        assert identity["preferred_address"] in instructions
        assert signature["cadence"] in instructions
        assert signature["recognition_pattern"] in instructions

    try:
        load_markdown_role("..\\missing_role")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("missing or traversed role prompt must fail closed")
    print("Role loader integration tests passed.")


if __name__ == "__main__":
    main()
