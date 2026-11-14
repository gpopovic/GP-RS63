"""Triton's role-driven Requirements -> Architecture -> Execution -> Review -> Validation graph."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Literal, TypedDict

from dotenv import load_dotenv

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import (  # noqa: E402
    TRITON_ROOT,
    load_corp_builder_model_lane,
    load_markdown_role,
    load_role_instructions,
)
from Local_Model_Operations.model_observer import assess_model  # noqa: E402
from Local_Model_Operations.gpu_relief import release_configured_models  # noqa: E402
from adaptive_harness import select_adaptive_harness  # noqa: E402
from model_class_router import ModelClass, require_admitted_model, select_model_class  # noqa: E402
from online_escalation import load_approved_data_capsule  # noqa: E402
from execution_evidence import validate_execution_evidence  # noqa: E402

load_dotenv(TRITON_ROOT / ".env")
load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)

RoleRunner = Callable[[str, str, str], str]
ValidationStatus = Literal["PASS", "FAIL"]

VALIDATION_MARKER = re.compile(
    r"^\s*(?:#{1,6}\s+|[-*+]\s+)?(?:\*\*|__|`)?RESULT:\s*(PASS|FAIL)(?:\*\*|__|`)?\s*(?:\r?\n|$)",
    re.IGNORECASE,
)


def parse_validation_status(report: str) -> ValidationStatus:
    """Accept a controlled first-line result marker, including light Markdown formatting."""
    match = VALIDATION_MARKER.match(report)
    return "PASS" if match and match.group(1).upper() == "PASS" else "FAIL"
ModelTarget = tuple[str, str, str, str, str]


class TritonState(TypedDict):
    """State exchanged only through the controlled pipeline stages."""

    task: str
    requirements: str
    architecture: str
    implementation: str
    independent_review: str
    validation: str
    validation_status: ValidationStatus
    attempts: int


def build_openai_runner(
    *,
    default_class: ModelClass = "STANDARD",
    specialist_class: ModelClass = "STANDARD",
    validator_class: ModelClass = "STANDARD",
    max_model_calls: int = 7,
) -> RoleRunner:
    """Create a role-aware OpenAI-compatible client for local or proxy models."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as error:
        raise RuntimeError(
            "Install runtime dependencies: pip install -r requirements.txt"
        ) from error

    default_model = os.getenv("TRITON_DEFAULT_MODEL", os.getenv("TRITON_MODEL", "gpt-4o-mini"))
    specialist_model = os.getenv("TRITON_SPECIALIST_MODEL", default_model)
    validator_model = os.getenv("TRITON_VALIDATOR_MODEL", default_model)
    governance_model = os.getenv("TRITON_GOVERNANCE_MODEL", specialist_model)
    governance_chair_model = os.getenv("TRITON_GOVERNANCE_CHAIR_MODEL", governance_model)
    governance_challenger_model = os.getenv("TRITON_GOVERNANCE_CHALLENGER_MODEL", validator_model)
    corp_builder_model = os.getenv("TRITON_CORP_BUILDER_MODEL", specialist_model)
    corp_builder_controller_model = os.getenv("TRITON_CORP_BUILDER_CONTROLLER_MODEL", validator_model)
    max_output_tokens = int(os.getenv("TRITON_MAX_OUTPUT_TOKENS", "600"))
    if max_model_calls < 1:
        raise ValueError("max_model_calls must be positive.")
    clients: dict[ModelTarget, ChatOpenAI] = {}
    calls_made = 0

    local_base_url = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
    local_api_key = os.getenv("OPENAI_API_KEY", "not-needed")

    def approved_data_capsule(provider: str, region: str) -> str:
        """Read only a specifically approved, bounded capsule for an online escalation."""
        capsule_id = os.getenv("TRITON_ONLINE_DATA_CAPSULE_ID", "").strip()
        configured_path = os.getenv("TRITON_ONLINE_DATA_CAPSULE_PATH", "").strip()
        if not capsule_id or not configured_path:
            raise RuntimeError("Online escalation requires an approved data capsule ID and path.")
        load_markdown_role("Data_Escalation_Officer")
        return load_approved_data_capsule(
            capsule_id, configured_path, provider=provider, region=region
        ).content

    def online_target() -> ModelTarget | None:
        """Return the first approved escalation tier; local routing remains preferred."""
        execution_approved = os.getenv("TRITON_ONLINE_EXECUTION_APPROVED", "false").lower() == "true"
        capsule_approved = os.getenv("TRITON_ONLINE_DATA_CAPSULE_APPROVED", "false").lower() == "true"
        capsule_id = os.getenv("TRITON_ONLINE_DATA_CAPSULE_ID", "").strip()
        capsule_path = os.getenv("TRITON_ONLINE_DATA_CAPSULE_PATH", "").strip()
        if not (execution_approved and capsule_approved and capsule_id and capsule_path):
            return None

        for prefix, region in (
            ("TRITON_EU_FALLBACK", "EU/EEA"),
            ("TRITON_US_FALLBACK", "US"),
            ("TRITON_CN_FALLBACK", "CN"),
        ):
            enabled = os.getenv(f"{prefix}_ENABLED", "false").lower() == "true"
            approved = os.getenv(f"{prefix}_APPROVED", "false").lower() == "true"
            base_url = os.getenv(f"{prefix}_BASE_URL", "").strip()
            model = os.getenv(f"{prefix}_MODEL", "").strip()
            provider = os.getenv(f"{prefix}_PROVIDER", "").strip()
            if enabled and approved and base_url and model and provider:
                return model, base_url, os.getenv(f"{prefix}_API_KEY", "not-needed"), provider, region
        return None

    def target_for(role: str, configured_model: str, required_class: ModelClass) -> ModelTarget:
        auto_routing = os.getenv("TRITON_AUTO_MODEL_ROUTING_ENABLED", "true").lower() == "true"
        if auto_routing:
            health = assess_model(configured_model, role)
            if health.decision == "ROUTE_TO_LOCAL_BACKUP" and health.recommended_model:
                target = health.recommended_model, local_base_url, local_api_key, "LOCAL", "LOCAL"
                require_admitted_model(target[0], required_class)
                return target
            if health.decision == "ESCALATE_FOR_HUMAN_SIGN_OFF":
                approved_online_target = online_target()
                if approved_online_target:
                    require_admitted_model(approved_online_target[0], required_class)
                    return approved_online_target
        target = configured_model, local_base_url, local_api_key, "LOCAL", "LOCAL"
        require_admitted_model(target[0], required_class)
        return target

    def client_for(target: ModelTarget) -> ChatOpenAI:
        if target not in clients:
            model_name, base_url, api_key, _provider, _region = target
            clients[target] = ChatOpenAI(
                model=model_name,
                api_key=api_key,
                base_url=base_url,
                temperature=0,
                max_tokens=max_output_tokens,
            )
        return clients[target]

    def run(role_name: str, role_prompt: str, work_item: str) -> str:
        nonlocal calls_made
        stage_name, separator, actual_role = role_name.partition(" | ")
        selected_model = {
            "Independent Code Reviewer": specialist_model,
            "Code Validator": validator_model,
            "Governance Participant": governance_model,
            "Governance Chair": governance_chair_model,
            "Governance Challenger": governance_challenger_model,
        }.get(stage_name, default_model)
        if separator:
            lane = load_corp_builder_model_lane(actual_role)
            if lane == "TRITON_CORP_BUILDER_MODEL":
                selected_model = corp_builder_model
            elif lane == "TRITON_CORP_BUILDER_CONTROLLER_MODEL":
                selected_model = corp_builder_controller_model
        role_key = {
            "Independent Code Reviewer": "specialist",
            "Code Validator": "validator",
            "Governance Participant": "specialist",
            "Governance Chair": "specialist",
            "Governance Challenger": "validator",
        }.get(stage_name, "primary")
        required_class = {
            "Independent Code Reviewer": specialist_class,
            "Code Validator": validator_class,
            "Governance Participant": specialist_class,
            "Governance Chair": default_class,
            "Governance Challenger": validator_class,
        }.get(stage_name, default_class)
        target = target_for(role_key, selected_model, required_class)
        is_online_target = target[3] != "LOCAL"
        submitted_work_item = approved_data_capsule(target[3], target[4]) if is_online_target else work_item
        if calls_made >= max_model_calls:
            raise RuntimeError(f"Approved model-call cap reached: {max_model_calls}.")
        calls_made += 1
        response = client_for(target).invoke(
            [
                ("system", role_prompt),
                ("user", f"Pipeline stage: {role_name}\n\nWork item:\n{submitted_work_item}"),
            ]
        )
        return str(response.content)

    return run


def build_demo_runner() -> RoleRunner:
    """Deterministic runner for smoke tests; it never calls a model or network."""
    def run(role_name: str, _role_prompt: str, work_item: str) -> str:
        if role_name == "Code Validator":
            return "RESULT: PASS\nDeterministic smoke-test validation completed."
        return f"[DEMO {role_name}] Processed: {work_item[:180]}"

    return run


def build_graph(runner: RoleRunner):
    """Build the LangGraph state machine with independent review and retry cap."""
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as error:
        raise RuntimeError(
            "LangGraph is required. Install runtime dependencies: pip install -r requirements.txt"
        ) from error

    prompts = {
        "Requirements_Engineer": load_role_instructions("Requirements_Engineer"),
        "Software_Architect": load_role_instructions("Software_Architect"),
        "Code_Executor": load_role_instructions("Code_Executor"),
        "ROLE_Korrektor": load_role_instructions("ROLE_Korrektor"),
        "Code_Validator": load_role_instructions("Code_Validator"),
    }

    def requirements(state: TritonState) -> dict[str, str]:
        return {"requirements": runner("Requirements Engineer", prompts["Requirements_Engineer"], state["task"])}

    def architecture(state: TritonState) -> dict[str, str]:
        return {"architecture": runner("Software Architect", prompts["Software_Architect"], state["requirements"])}

    def execution(state: TritonState) -> dict[str, object]:
        attempt = state["attempts"] + 1
        context = (
            f"Architecture:\n{state['architecture']}\n\n"
            f"Previous independent review:\n{state['independent_review']}\n\n"
            f"Previous validation:\n{state['validation']}"
        )
        return {"implementation": runner("Code Executor", prompts["Code_Executor"], context), "attempts": attempt}

    def independent_review(state: TritonState) -> dict[str, str]:
        context = (
            f"Requirements:\n{state['requirements']}\n\n"
            f"Architecture:\n{state['architecture']}\n\n"
            f"Implementation:\n{state['implementation']}"
        )
        return {
            "independent_review": runner(
                "Independent Code Reviewer", prompts["ROLE_Korrektor"], context
            )
        }

    def validation(state: TritonState) -> dict[str, str]:
        context = (
            f"Requirements:\n{state['requirements']}\n\n"
            f"Architecture:\n{state['architecture']}\n\n"
            f"Implementation:\n{state['implementation']}\n\n"
            f"Independent review:\n{state['independent_review']}"
        )
        report = runner("Code Validator", prompts["Code_Validator"], context)
        status = parse_validation_status(report)
        return {"validation": report, "validation_status": status}

    def next_after_validation(state: TritonState) -> Literal["execution", "end"]:
        return "end" if state["validation_status"] == "PASS" or state["attempts"] >= 3 else "execution"

    graph = StateGraph(TritonState)
    graph.add_node("requirements", requirements)
    graph.add_node("architecture", architecture)
    graph.add_node("execution", execution)
    graph.add_node("independent_review", independent_review)
    graph.add_node("validation", validation)
    graph.add_edge(START, "requirements")
    graph.add_edge("requirements", "architecture")
    graph.add_edge("architecture", "execution")
    graph.add_edge("execution", "independent_review")
    graph.add_edge("independent_review", "validation")
    graph.add_conditional_edges("validation", next_after_validation, {"execution": "execution", "end": END})
    return graph.compile()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Triton's master delivery graph.")
    parser.add_argument("task", nargs="?", default="Create a typed hello-world service with a unit test.")
    parser.add_argument("--workflow", choices=("discovery", "coding", "architecture", "built_environment", "service_operation"), default="coding")
    parser.add_argument("--task-type", choices=("ROUTINE", "COMPLEX", "FINAL_REVIEW"), default="COMPLEX")
    parser.add_argument("--material-risk", action="store_true")
    parser.add_argument("--sensitive-data", action="store_true")
    parser.add_argument("--max-model-calls", type=int, default=7)
    parser.add_argument("--workspace-id", help="External product workspace required for a live coding release assessment.")
    parser.add_argument("--execution-evidence", type=Path, help="JSON test evidence in that workspace's 04_Evidence directory.")
    parser.add_argument("--demo", action="store_true", help="Run deterministically without an LLM call.")
    args = parser.parse_args()

    if not args.demo and args.workflow == "coding":
        if not args.workspace_id or not args.execution_evidence:
            raise ValueError("A live coding assessment requires --workspace-id and --execution-evidence.")
        evidence_errors = validate_execution_evidence(args.workspace_id, args.execution_evidence)
        if evidence_errors:
            raise ValueError("Execution evidence failed: " + "; ".join(evidence_errors))

    if args.demo:
        # A local smoke test must not submit traces or require LangSmith credentials.
        os.environ["LANGCHAIN_TRACING_V2"] = "false"

    try:
        model_route = select_model_class(
            args.task_type, material_risk=args.material_risk, sensitive_data=args.sensitive_data
        )
        harness_plan = select_adaptive_harness(
            args.workflow, material_risk=args.material_risk, sensitive_data=args.sensitive_data
        )
        execution_controls = (
            f"Workflow={harness_plan.workflow_id}; role_profile={harness_plan.role_profile}; "
            f"model_class={model_route.model_class}; approved_call_cap={args.max_model_calls}; "
            f"human_gate_required={model_route.requires_human_gate or harness_plan.requires_human_approval}."
        )
        runner = build_demo_runner() if args.demo else build_openai_runner(
            default_class=model_route.model_class,
            specialist_class="STANDARD",
            validator_class="FLAGSHIP" if args.material_risk else "STANDARD",
            max_model_calls=args.max_model_calls,
        )
        final_state = build_graph(runner).invoke(
            {
            "task": f"{args.task}\n\nExecution controls: {execution_controls}",
            "requirements": "",
            "architecture": "",
            "implementation": "",
            "independent_review": "",
            "validation": "",
            "validation_status": "FAIL",
            "attempts": 0,
            }
        )
    finally:
        if not args.demo:
            release_configured_models()
    print(f"Quality gate: {final_state['validation_status']}")
    print(f"Executor attempts: {final_state['attempts']}/3")
    print(f"Validation summary: {final_state['validation']}")


if __name__ == "__main__":
    main()
