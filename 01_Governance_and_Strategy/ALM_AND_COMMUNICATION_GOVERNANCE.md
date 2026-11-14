# ALM and Communication Governance

## ALM Design Rules

The ALM system is a decision and traceability service, not a reporting theatre. Start with the smallest viable workflow, mandatory evidence only where a decision or risk needs it, and a source-of-truth hierarchy. Every field, status, automation, dashboard, graph, statistic, and integration must have a question, owner, data definition, adoption measure, and retirement review.

The ALM and Jira Product Administrator maintains configuration records, pilot/rollback evidence, and data-quality checks. Feature teams co-design workflow changes; independent assurance reviews material traceability and control changes.

## Agile Framework Precedence and No-Tool Mode

Triton uses SAFe as the governing scaling and decision model. It defines portfolio and product-flow decisions, value alignment, cadence, cross-team dependency management, and escalation when practices conflict. Nexus is an optional delivery-level integration pattern when several Scrum teams build one product increment. Nexus must not create a competing governance layer, duplicate portfolio decisions, or override a SAFe decision.

Apply SAFe proportionately. A single feature or discovery team uses the relevant team-level practices and the approved portfolio/governance decisions; it is not described or operated as an Agile Release Train (ART). Establish an ART only when a persistent, multi-team value stream, shared cadence, and explicit ART operating model are approved.

If a SAFe and Nexus practice conflict, apply this order: applicable law, contract, safety/security/privacy and quality controls; then the approved SAFe decision; then the locally agreed Nexus integration practice; then team working agreements. Record a material conflict, its owner, decision, rationale, and review date in the decision register.

Until a Jira sandbox or another ALM tenant exists, use the controlled Markdown/CSV Shadow Backlog protocol. It is a temporary planning and traceability record, not a second source of truth once Jira is available. The ALM and Jira Product Administrator owns migration mapping, completeness checks, and retirement of the shadow record after the approved import.

## Communication KPIs

| KPI | Meaning | Guardrail |
| --- | --- | --- |
| Decision latency | Time from a decision-ready request to an owned, recorded decision | Segment by work class; do not reward rushed decisions |
| Meeting decision yield | Decisions, resolved risks, or designed outputs per meeting time | Some discovery or trust work is valid without a decision |
| Clarification-loop rate | Rework or repeated clarification attributable to unclear interfaces | Sample causes; never infer blame from message counts |
| Hand-off completeness | Required context and acceptance evidence present at hand-off | Quality gate, not a volume target |
| Focus interruption load | Aggregate unplanned urgent contact and context switching | Team/process level by default; protect privacy |
| Communication improvement effect | Change in load, flow, quality, and inclusion after an experiment | Reject gains that harm quality, safety, or inclusion |

## Cross-Border Working Agreements

For a recurring cross-border team, the Scrum Master, Communication Operations and Effectiveness Manager, and Cross-Border Delivery Manager establish one visible agreement: named decision contacts and continuity cover, overlap window, asynchronous update format, hand-off evidence, urgent escalation path, and protected focus periods. Customer requests enter through the approved product and delivery route; a direct informal request does not silently change scope or interrupt an engineer's planned work. Review the agreement with flow, hand-off, customer-outcome, and workload evidence rather than response-time folklore.

## Privacy and Control

Communication analysis uses aggregated, metadata-minimised, purpose-bound evidence by default. It does not read private content or build individual productivity surveillance. Any exceptional investigation follows the applicable legal, privacy, and incident process.
