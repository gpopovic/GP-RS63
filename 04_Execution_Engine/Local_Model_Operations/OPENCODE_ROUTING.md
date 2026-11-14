# OpenCode Local-First Routing

## Purpose

Use OpenCode as a local-first companion to Triton's controlled model-routing policy. This document governs selection in the OpenCode terminal; it does not replace `MODEL_GOVERNANCE.md` for the LangGraph runtime.

## Local Model Roles

| OpenCode selection | Model | Use it for |
| --- | --- | --- |
| `build` | `ollama-local/qwen3:4b` | Small implementation tasks, repository navigation, command/tool use, and bounded edits |
| `local-analysis` | `ollama-local/qwen3:4b` | Reading, structured analysis, drafting, and explaining; no autonomous edits |
| `local-review` | Not configured | Reserved for a distinct, benchmark-admitted `STANDARD` or `FLAGSHIP` reviewer; do not substitute the builder model merely to preserve a second lane |

Do not claim that a local result is sufficient merely because it completed. Use the appropriate reviewer and quality gate for material work.

`gemma3:4b` remains installed in Ollama for direct, tool-free conversation (`ollama run gemma3:4b`). It is deliberately not offered inside OpenCode: this local model reports no tool capability, while OpenCode agent sessions require tool support.

## Cloud Escalation

Local models are the default. Before selecting any OpenAI or Google Gemini provider, OpenCode must stop and ask the user for a specific approval that states:

1. why the local route is insufficient;
2. the intended provider and model, if configured;
3. the scope and data classification; and
4. the minimum approved data capsule.

Never send production customer data, credentials, personal data, proprietary source code, or restricted standards content to a cloud provider. Follow `ONLINE_ESCALATION_POLICY.md` and the Data Escalation Officer's approval route. A user must actively configure the provider with `/connect` and select it with `/models`; no provider credential or cloud-model default is stored in this project.

## Operator Routine

1. Start OpenCode in `C:\git\Triton_AI_Corp`.
2. Use `build` for local implementation. Use `local-review` only after an independent reviewer has been admitted; until then, apply the defined human or approved online review gate.
3. Use `local-analysis` for non-editing repository work. Use direct Ollama for a tool-free Gemma conversation.
4. If quality remains insufficient after a bounded local attempt, request cloud-escalation approval rather than silently changing provider.
