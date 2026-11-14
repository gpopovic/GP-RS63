# Role Source Mapping and Skill Derivation

## Purpose

Triton does not copy job descriptions from frameworks. It derives executable, reviewable role skills from their public responsibilities, interfaces, work products, and quality expectations. This preserves traceability while keeping Triton's prompts and skills original, practical, and maintainable.

## Source Families

| Source family | What Triton derives | What it does not copy or automate |
| --- | --- | --- |
| Automotive SPICE | Process ownership, expected outcomes, work-product evidence, verification, configuration, and quality interfaces | Licensed standard text; certification decisions; accountable human sign-off |
| SAFe | Product/value responsibilities, architectural alignment, flow facilitation, portfolio and team collaboration | A rigid organisational chart or framework branding without a business need |
| Nexus | Cross-team integration, shared backlog, dependency visibility, integrated increment, and shared Definition of Done | A separate hierarchy; the integration function may be a temporary team |
| Architecture and construction delivery | Client brief, design coordination, structural evidence, cost, site quality, and staged decision gates | Engineering judgement, statutory submissions, or structural approval by an unlicensed agent |

## Derivation Method

Every Triton role or skill must define the following before activation:

1. **Accountability:** the outcome for which the role is answerable.
2. **Authority and boundary:** decisions it may make, decisions it must escalate, and tools it may use.
3. **Inputs and outputs:** traceable inputs, expected work products, and their storage location.
4. **Collaboration contract:** which roles challenge, defend, integrate, or approve the work.
5. **Quality criteria:** objective checks, evidence, Definition of Done, and acceptance owner.
6. **Conflict protocol:** position, evidence-based challenge, defense or correction, Quality Manager resolution, then escalation after three unresolved material cycles.
7. **Evaluation:** representative tasks, failure cases, and measurable pass criteria.

## Initial Role and Skill Families

| Family | Role or capability | Primary source pattern | Triton implementation direction |
| --- | --- | --- | --- |
| Product and strategy | Product Owner / Product Management | SAFe customer value, backlog, strategy | Own priority, acceptance evidence, and stakeholder feedback; never silently redefine a requirement |
| Flow and coordination | Release Train Engineer / Team Coach | SAFe flow facilitation | Facilitate dependency and risk resolution; do not become the technical decision owner |
| Executive operating stewardship | COO support / operations coordination | Lean flow, evidence-based governance, and agile facilitation | Coordinate cross-functional decisions and founder briefs; do not waive accountable specialist gates |
| Integration | Integration Lead (temporary team capability) | Nexus Integration Team | Make dependencies and integrated Definition of Done visible; coordinate rather than replace delivery teams |
| Engineering | System Architect, Requirements Engineer, Code Executor, Code Validator | Automotive SPICE and SAFe | Maintain traceable requirements, architecture, implementation, verification, and independent challenge |
| Technical operations | Chief Engineer and Systems Architect | Architecture governance, configuration management, and engineering operations | Coordinate shared toolchain and execution architecture; require admission, evidence, testing, and rollback |
| Assurance | Quality Manager, Configuration Manager, Safety and Compliance Engineer | Automotive SPICE | Control baselines, evidence, deviations, and quality gates; escalate rather than waive material controls |
| Built environment | Lead Architect, Structural Engineer, Cost Planner, Information Manager, Site Quality Inspector | RIBA-style staged delivery | Maintain brief/design/structural/cost/site evidence and interfaces; require qualified human sign-off for regulated decisions |

## Reusable Skill Modules

The initial skills should be small modules, not broad personas:

- Requirements elicitation and traceability
- Architecture decision records and interface control
- Independent review, rebuttal, and correction
- Test design, evidence, and regression control
- Configuration baseline and change impact analysis
- Dependency and integrated-increment management
- Design coordination, structural-review preparation, cost evidence, and site-quality inspection

## Authority Note

Triton agents can prepare evidence, identify contradictions, and recommend decisions. Legal approvals, statutory submissions, safety cases, financial commitments, and licensed architecture or structural-engineering decisions remain human responsibilities and require the documented human sign-off process.
