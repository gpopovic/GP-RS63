# Triton AI Corp: Agentic Development Rules

Before generating or changing code and prompts, consult the applicable roles under `02_Organization_and_Roles/`. System prompts must never be hard-coded in Python; load them only from Markdown files in this structure.

Use platform-independent `pathlib.Path` paths, central configuration from `04_Execution_Engine/config.py`, clear type hints, and small testable modules. Observe standards stored in `03_Knowledge_Base_RAG/Standards_and_Norms/` and document human approvals under `05_Human_Interface_and_Ops/Manual_Quality_Gates/`.

Codex must also follow `01_Governance_and_Strategy/CODEX_SELF_CORRECTION_AND_EXECUTION_PROFILE.md`. In particular: inspect evidence before designing a process, distinguish a passed check from maturity or fitness for use, use the minimum sufficient assurance route, do not invent universal thresholds, and convert each supported criticism into a root cause, a replacement rule, and verification evidence. External review folders are read-only unless the user explicitly authorises changes there.
