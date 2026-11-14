# MCP Registry and Permission Policy

MCP servers provide live data or actions. They are not installed merely because they are popular. Every server must have a named purpose, minimal permissions, a data classification, an owner, a tested failure mode, and an approval record.

## Selection Priority

1. Prefer a maintained open-source server with a clear licence and an auditable source repository.
2. If no suitable open-source option exists, prefer a genuinely no-cost, read-only service with transparent terms and data handling.
3. Prefer the smallest permission scope and local execution over remote execution.
4. Paid, closed-source, write-capable, or credentialed servers require an explicit exception approval; popularity alone is not an exception.

"Free" does not mean trusted. The intake record must state the licence, cost model, maintenance signal, hosting location, data flow, required credentials, and permissions.

## Approved Project Configuration

| Server | Purpose | Access boundary |
| --- | --- | --- |
| `triton-filesystem` | Read and edit the open Triton workspace | Docker-isolated filesystem server; mounted workspace only |
| `mcp-documentation` | Model Context Protocol reference | Read-only public documentation |
| `openai-developer-docs` | Official OpenAI and Codex documentation | Read-only public documentation |

## Candidates Requiring Separate Approval

| Capability | Why it is useful | Gate before activation |
| --- | --- | --- |
| GitHub MCP | Issues, pull requests, repository evidence | Account connection; repository scope; read-only first |
| Search MCP | Current external standards, vendor, or model information | Provider, query-data classification, cost, and retention review |
| Issue tracker / knowledge base MCP | Traceability to approved work items and evidence | System owner, data scope, and write-action policy |
| Docker or cloud administration MCP | Runtime diagnosis and delivery | Least privilege and explicit separation from production |

## Explicitly Not Required

Ollama does not need an MCP server for Triton. The local OpenAI-compatible endpoint is already controlled by `OPENAI_API_BASE`; adding a third-party Ollama MCP would only add another trust boundary.
