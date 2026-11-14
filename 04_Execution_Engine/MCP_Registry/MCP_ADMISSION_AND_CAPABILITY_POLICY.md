# MCP Admission and Capability Policy

## Principle

Skills describe how a role works; MCP servers provide external capability. An MCP is never enabled merely because it is popular or free. It is admitted per capability, role, data class, authority, and reversible test.

## Admission Gate

1. Record provider, repository or official endpoint, licence, maintenance evidence, transport, permissions, data route, and operating cost.
2. Threat-model prompt injection, credential exposure, path/network scope, audit trail, and available least-privilege configuration.
3. Trial only with synthetic or approved non-production data, a narrowly scoped account, and an explicit owner.
4. Measure usefulness, failure rate, latency, human correction, and security/privacy findings.
5. Promote, retain, restrict, or retire through Company Configuration Management.

No MCP may change credentials, publish externally, make financial or legal commitments, delete data, or access production customer data without the authorised human and data route.

## Capability Lanes

| Capability | Primary owners | Default authority |
| --- | --- | --- |
| Local repository and documentation inspection | Architecture, Configuration, Quality | Read-only; workspace allow-list |
| Browser-based research and test automation | Market Intelligence, Testing, Security | Synthetic/public data; approval for authenticated state |
| ALM read and controlled work-item drafting | ALM Administrator, Product Owner, Scrum Master | Read/draft by default; creation/update only after user confirmation |
| Standards and regulatory research | Legal, Privacy, Quality, Research | Source retrieval only; no legal conclusion without reviewer |
| Source-control status and evidence | Configuration, Quality, Security | Read-only unless an approved change record authorises mutation |

## Initial Rule

The catalog records candidates, not installed servers. Each candidate remains `INTAKE` until its technical and governance checks pass.

## Minimum-Sufficient Capability Selection

Tool selection is a constrained decision, not a popularity ranking or a single efficiency formula:

1. Define the evidence needed, required capability, authority, execution mode, data class, environment, and acceptance criterion.
2. Exclude every capability that is not independently admitted for all of those boundaries. A named, installed, local, free, or fast tool is not automatically eligible.
3. Among eligible capabilities, prefer the smallest route expected to satisfy the evidence need. Use measured task-relevant cost, latency, reliability, correction effort, security exposure, and failure consequence where those observations exist; do not invent universal scores or timings.
4. Direct inspection or a deterministic local check can be sufficient. Browser, language-server, cloud, model, or MCP execution is justified only by the evidence need.
5. Declare any fallback in advance or make a new explicit failure decision. A fallback must pass its own admission and may not silently change permissions, data boundary, provider, jurisdiction, cost authority, or mutation scope.
6. Preserve the selected capability, version where relevant, inputs or input references, result, limitations, and decision consequence in proportion to risk.

An auditor may issue a supported pass, defect, limitation, or hypothesis without invoking an MCP when the chosen evidence route is sufficient. Conversely, invoking a tool does not make its output true or complete.
