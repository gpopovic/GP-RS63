# LangGraph Company Orchestration

## Purpose

Triton uses small, explicit LangGraph workflows rather than one unrestricted super-agent. Each graph loads its role instructions from the canonical Markdown roles, keeps a typed and bounded state, records a gate outcome, and stops or escalates when evidence is insufficient.

## Available Workflows

| Workflow | Use | Control boundary |
| --- | --- | --- |
| `master_graph.py` | Requirements → Architecture → Execution → Independent Review → Validation | Three execution attempts maximum; failed validation stops for follow-up. |
| `governance_meeting_graph.py` | Catalog-defined product, Scrum, Nexus, board, compliance, investment, and crisis meetings | Participant discussion → independent challenger → accountable chair decision or escalation. |
| `deliberation_graph.py` | Bounded role disagreement on one defined issue | Position → challenge → defence → Quality decision; three rounds maximum by default. |
| `corp_builder_control.py` | Multi-model review of a proposed Company OS change | Produces a non-mutating decision brief; human approval and configuration control remain mandatory. |
| `meeting_scaler.py` | Deterministic selection of a lean meeting set from delivery conditions | Recommends only; does not schedule meetings, inspect calendars, or alter capacity records. |

The meeting catalog is the source of truth for chair, participants, required inputs, and required outputs. It includes Feature Investment Review, Sprint Planning, Nexus Integration Review, executive business review, legal/compliance review, and event-triggered crisis command. SAFe retains precedence over Nexus when their practices conflict.

## Local-First Model Allocation

The default configuration assigns the specialist local model to governance participants and chair, and the independent validator model to the challenger. This is a deliberate quality/cost split, not a claim that a model is authoritative. The quality gate, role boundaries, and escalation route still apply.

`TRITON_GOVERNANCE_MODEL`, `TRITON_GOVERNANCE_CHAIR_MODEL`, and `TRITON_GOVERNANCE_CHALLENGER_MODEL` are defined in `.env.example`. A cloud route is never selected merely to improve a meeting response: it follows the existing approved-data-capsule and human-approval policy.

The Corp Builder has two local model lanes. `TRITON_CORP_BUILDER_MODEL` serves the Builder lane; `TRITON_CORP_BUILDER_CONTROLLER_MODEL` serves the independent Controller lane. The membership and routing keys are controlled in `CORP_BUILDER_CONTROL_BOARD.json`.

## Operator Commands

Run these from the repository root. Demo commands do not invoke an LLM or send traces.

```powershell
# Verify the delivery graph and one catalog-defined meeting.
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\test_graph.py
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\test_governance_meeting.py
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\test_corp_builder_control.py
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\test_meeting_scaler.py

# Inspect a deterministic Sprint Planning flow.
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\governance_meeting_graph.py feature_team_sprint_planning "Synthetic evidence only: one ready feature and one dependency." --demo

# Run a local-first, live governance meeting after reviewing .env.
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\governance_meeting_graph.py weekly_delivery_quality_review "Sanitised evidence summary and decision question."

# Review a Company OS change packet. This never applies the change.
04_Execution_Engine\.venv\Scripts\python.exe 04_Execution_Engine\LangGraph_Pipelines\corp_builder_control.py C:\path\to\change_packet.md --demo
```

Use concise, sanitised evidence summaries. Product work and production customer data remain outside the Company OS unless the approved product-workspace data route explicitly allows otherwise.
