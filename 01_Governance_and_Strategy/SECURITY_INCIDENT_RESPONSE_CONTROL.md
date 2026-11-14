# Security and Agentic Incident Response Control

## Purpose

Provide a severity- and obligation-driven route to detect, contain, investigate, recover from, communicate, and learn from security incidents affecting Triton systems, data, providers, agents, tools, or dependencies.

## Incident Record

Record the incident ID, detection source and time, known facts, uncertainty, affected assets and data classes, current exposure, severity rationale, containment, evidence-preservation needs, accountable incident lead, legal/privacy/customer notification owners, decisions and timestamps, recovery criteria, and next review point. Preserve chain of custody where required and restrict sensitive evidence to the minimum authorised participants.

## Response Route

1. Triage credibility, scope, safety, privacy, legal, contractual, financial, and continuity exposure. Do not wait for complete root-cause certainty before proportionate containment.
2. Contain the affected credential, tool, model, connector, workflow, host, data route, or release while protecting evidence and avoiding unnecessary destruction or business-wide shutdown.
3. Investigate the attack or failure path, impacted identities and records, persistence, lateral movement, supply-chain exposure, and integrity of the last known-good state. A checksum proves identity of bytes, not that a state is secure or compliant.
4. Recover only to declared criteria: corrected cause or controlled workaround, credential and access review, relevant regression and security checks, data-integrity assessment, monitoring, rollback route, and accountable approval.
5. Make notifications according to the verified jurisdiction, regulator, contract, insurer, affected person, and applicable deadline. A generic timetable never substitutes for legal assessment.
6. Record corrective actions and verify effectiveness independently. Do not automatically convert one incident into a normative agent rule or production control.

## Agentic and Tool Boundaries

External content, prompts, retrieved documents, tool output, and connector metadata are untrusted inputs. Agents receive minimum necessary permissions and may not infer authority from role names, form fields, model confidence, or a schema-valid request. Destructive operations, financial commitments, credential changes, production activation, legal notifications, and release decisions remain with the authorised human and applicable technical control.

## Activation and Evidence Status

This control defines the route; it does not claim a staffed incident team, certified management system, active monitoring, tested restoration, secure sandbox, or regulatory compliance. Each dependency needs named contacts, tested containment and recovery steps, evidence locations, and an exercise or real-incident review appropriate to its risk before `FIT_FOR_DECLARED_USE` can be asserted.
