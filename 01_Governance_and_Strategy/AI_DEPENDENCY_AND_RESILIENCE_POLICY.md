# AI Dependency and Resilience Policy

## Purpose

Keep Triton able to deliver safely when an AI model, provider, local runtime, MCP server, model registry, identity service, or other critical AI dependency changes, degrades, becomes uneconomic, or becomes unavailable. Local hosting can reduce external dependency; it does not itself prove security, privacy, availability, or legal compliance.

## Dependency Register

The Security Operations and Incident Response Engineer maintains an approved dependency register for every production and material internal workflow. Each entry records:

- dependency type, owner, version or model tag, supplier or repository, licence/terms basis, criticality, and supported environment;
- data classification, approved processing location, network route, telemetry/logging behaviour, and subprocessors where applicable;
- cost unit and approved spend limit where the dependency can create variable spend;
- supported fallback, exit path, recovery point, test date, and residual risk; and
- the configuration baseline and applicable decision record.

The register contains no credentials, customer content, or unrestricted production data.

## Routing and Fallback Principles

1. Select a model route by task risk, capability evidence, latency, cost, and approved data boundary; never by marketing claims or a provider name alone.
2. Keep the primary model, local backup, and any online exception independently configurable. A failed route must not silently send the graph state to a cloud provider.
3. Apply hard iteration, time, and spend limits. After a limit is reached, stop, retain diagnostic evidence, and follow the named human or incident route.
4. Use synthetic fixtures and held-out evaluation cases to test fallbacks. A fallback is not approved merely because it starts or returns text.
5. Treat provider/model upgrades, MCP additions, licence/terms changes, endpoint changes, and new telemetry as configuration changes under ASPICE SUP.8.
6. A monitored integration may automatically detect a failure, collect approved diagnostics, and prepare a repair proposal. It must not apply a production repair until the approved change route has verified tests, impact, release readiness, rollback evidence, and the required human decision.

## Assurance and Recovery

- Before a dependency becomes a baseline, Model Quality Observer validates outcome quality against the same representative evaluation set; Security Operations verifies the technical route; Privacy and Data Protection Officer reviews the data-flow impact; Finance and Risk Controller reviews variable-cost exposure where material.
- At least quarterly, exercise a representative fallback or recovery path for each critical dependency and record the observed recovery result, quality, and limitations.
- If a critical route fails or a supplier changes a material term, Security Operations contains the affected route, Configuration Manager preserves the baseline, and the relevant owners decide whether to restore, route to an already approved alternative, or suspend the capability.

## Boundaries

- Do not represent local execution as "100% secure," "fully sovereign," or compliant by default. These outcomes depend on the actual host, access controls, software supply chain, logging, data flow, jurisdiction, and evidence.
- Do not make cost-savings claims without Triton's measured workload, pricing, utilisation, and quality evidence.
- Do not use a resilience exercise to transmit production customer data outside its approved processing boundary.

## KPIs

Track critical-dependency register coverage, tested-fallback coverage, recovery-test success, unapproved-egress findings, model-route quality, route latency, quality-adjusted cost, variable-spend variance, time to contain, and unresolved high-risk dependencies. Interpret all metrics with workload class, sample size, and data-quality context.
