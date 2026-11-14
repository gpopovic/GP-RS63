"""Central, platform-independent paths and role-prompt loading for Triton."""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any

TRITON_ROOT = Path(__file__).resolve().parents[1]
ROLES_DIR = TRITON_ROOT / "02_Organization_and_Roles" / "Roles_Descriptions"
COACHES_DIR = TRITON_ROOT / "02_Organization_and_Roles" / "Internal_Coaches"
CORE_ASSISTANTS_DIR = TRITON_ROOT / "02_Organization_and_Roles" / "Core_Assistants"
NORMS_DIR = TRITON_ROOT / "03_Knowledge_Base_RAG" / "Standards_and_Norms"
PROMPTS_DIR = TRITON_ROOT / "04_Execution_Engine" / "Prompts_and_SystemInstructions"
MODEL_OPERATIONS_DIR = TRITON_ROOT / "04_Execution_Engine" / "Local_Model_Operations"
MODEL_OBSERVATIONS_DIR = MODEL_OPERATIONS_DIR / "observations"
LOCAL_TRANSCRIPTION_DIR = TRITON_ROOT / "04_Execution_Engine" / "Local_Transcription"
LOCAL_TRANSCRIPTION_MODEL_DIR = LOCAL_TRANSCRIPTION_DIR / "models"
HUMAN_OPS_DIR = TRITON_ROOT / "05_Human_Interface_and_Ops"
APPROVED_DATA_CAPSULES_DIR = HUMAN_OPS_DIR / "Approved_Data_Capsules"
AGENT_CONSTITUTION_PATH = TRITON_ROOT / "00_Corp_DNA" / "AGENT_COLLABORATION_CONSTITUTION.md"
AGENT_PERSONA_RUNTIME_RULES_PATH = TRITON_ROOT / "00_Corp_DNA" / "AGENT_PERSONA_RUNTIME_RULES.md"
AGENT_PERSONA_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "AGENT_PERSONA_REGISTRY.json"
CORP_BUILDER_CONTROL_BOARD_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "CORP_BUILDER_CONTROL_BOARD.json"
ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"
ROLE_HUMAN_NAME_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_HUMAN_NAME_REGISTRY.json"
ROLE_COMMUNICATION_SIGNATURE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_COMMUNICATION_SIGNATURE_REGISTRY.json"
ROLE_KPI_MATRIX_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_KPI_MATRIX.json"
PRODUCT_WORKSPACES_ROOT = Path(
    os.getenv("TRITON_PRODUCT_WORKSPACES_ROOT", TRITON_ROOT.parent / "Triton_Product_Workspaces")
).expanduser().resolve()
AUTHORISED_RAG_MANIFESTS_DIR = NORMS_DIR.parent / "Authorised_Source_Manifests"


def _default_secure_runtime_dir() -> Path:
    """Return an OS-local state path; secrets must never live in the repository."""
    if os.name == "nt":
        # Packaged Windows apps may virtualise LOCALAPPDATA. The profile-level
        # hidden directory remains stable for backup and operator inspection.
        return Path.home() / ".triton_ai" / "secure-runtime"
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / "TritonAI" / "secure-runtime"


SECURE_RUNTIME_DIR = Path(
    os.getenv("TRITON_SECURE_RUNTIME_DIR", _default_secure_runtime_dir())
).expanduser().resolve()


def load_markdown_role(role_name: str) -> str:
    """Load one approved role prompt without permitting path traversal."""
    filename = Path(role_name).name
    if Path(filename).suffix != ".md":
        filename = f"{filename}.md"

    for directory in (ROLES_DIR, COACHES_DIR, CORE_ASSISTANTS_DIR):
        candidate = (directory / filename).resolve()
        if candidate.parent == directory.resolve() and candidate.is_file():
            return candidate.read_text(encoding="utf-8").strip()

    raise FileNotFoundError(f"Role prompt not found: {filename}")


def load_role_instructions(role_name: str) -> str:
    """Load a role together with Triton's shared collaboration constitution."""
    constitution = AGENT_CONSTITUTION_PATH.read_text(encoding="utf-8").strip()
    persona_rules = AGENT_PERSONA_RUNTIME_RULES_PATH.read_text(encoding="utf-8").strip()
    role = load_markdown_role(role_name)
    persona_profile = load_persona_profile(role_name)
    human_identity = load_role_human_identity(role_name)
    communication_signature = load_role_communication_signature(role_name)
    kpi_profile = load_role_kpi_profile(role_name)
    return (
        f"{constitution}\n\n---\n\n{persona_rules}\n\n---\n\n"
        f"Configured persona profile:\n{json.dumps(persona_profile, ensure_ascii=False)}"
        f"\n\nConfigured fictional work identity:\n{json.dumps(human_identity, ensure_ascii=False)}"
        f"\n\nConfigured communication signature:\n{json.dumps(communication_signature, ensure_ascii=False)}"
        f"\n\nConfigured KPI profile:\n{json.dumps(kpi_profile, ensure_ascii=False)}"
        f"\n\n---\n\n{role}"
    )


def load_persona_profile(role_name: str) -> dict[str, Any]:
    """Load one configured functional persona without accepting path fragments."""
    role_id = Path(role_name).name.removesuffix(".md")
    registry = json.loads(AGENT_PERSONA_REGISTRY_PATH.read_text(encoding="utf-8"))
    raw_profile = registry.get("profiles", {}).get(role_id)
    if not isinstance(raw_profile, list) or len(raw_profile) != 3:
        raise KeyError(f"Persona profile not found: {role_id}")

    return dict(zip(registry["profile_format"], raw_profile, strict=True))


def load_role_human_identity(role_name: str) -> dict[str, str]:
    """Load one stable fictional work identity without implying a real person."""
    role_id = Path(role_name).name.removesuffix(".md")
    registry = json.loads(ROLE_HUMAN_NAME_REGISTRY_PATH.read_text(encoding="utf-8"))
    profile = registry.get("profiles", {}).get(role_id)
    if not isinstance(profile, dict):
        raise KeyError(f"Human work identity not found: {role_id}")
    display_name = profile.get("display_name")
    preferred_address = profile.get("preferred_address")
    if not isinstance(display_name, str) or not isinstance(preferred_address, str):
        raise ValueError(f"Invalid human work identity: {role_id}")
    return {"display_name": display_name, "preferred_address": preferred_address}


def load_role_communication_signature(role_name: str) -> dict[str, str]:
    """Load one restrained, role-specific communication signature."""
    role_id = Path(role_name).name.removesuffix(".md")
    registry = json.loads(ROLE_COMMUNICATION_SIGNATURE_REGISTRY_PATH.read_text(encoding="utf-8"))
    profile = registry.get("profiles", {}).get(role_id)
    if not isinstance(profile, dict):
        raise KeyError(f"Communication signature not found: {role_id}")
    cadence = profile.get("cadence")
    recognition_pattern = profile.get("recognition_pattern")
    if not isinstance(cadence, str) or not isinstance(recognition_pattern, str):
        raise ValueError(f"Invalid communication signature: {role_id}")
    return {"cadence": cadence, "recognition_pattern": recognition_pattern}


def load_corp_builder_model_lane(role_name: str) -> str | None:
    """Return the configured Corp Builder model environment key for one role."""
    role_id = Path(role_name).name.removesuffix(".md")
    board = json.loads(CORP_BUILDER_CONTROL_BOARD_PATH.read_text(encoding="utf-8"))
    matches = [
        str(lane["environment_key"])
        for lane in board.get("model_lanes", [])
        if role_id in lane.get("roles", [])
    ]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous Corp Builder model lane for: {role_id}")
    return matches[0] if matches else None


def load_role_kpi_profile(role_name: str) -> dict[str, list[str]]:
    """Load the controlled common and functional KPI profile for one canonical role."""
    role_id = Path(role_name).name.removesuffix(".md")
    registry = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    matrix = json.loads(ROLE_KPI_MATRIX_PATH.read_text(encoding="utf-8"))
    departments = [
        department["id"]
        for department in registry["departments"]
        if role_id in department["members"]
    ]
    if len(departments) != 1:
        raise KeyError(f"Unknown or ambiguous canonical role: {role_id}")
    department_id = departments[0]
    return {
        "common": list(matrix["common_metric_ids"]),
        "functional": list(matrix["department_profiles"][department_id]),
    }
