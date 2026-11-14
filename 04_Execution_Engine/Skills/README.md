# Triton Skill Registry

Triton uses skills as focused, versioned operating procedures. A skill is not a role: roles own decisions and accountability; skills provide a reusable method, reference set, template, or bounded script.

## Approved Sources

- [OpenAI Skills Catalog](https://github.com/openai/skills): the preferred source for Codex-compatible skills. Use it for Codex and OpenAI documentation, workflow design, and evaluated engineering patterns.
- [Anthropic Agent Skills](https://github.com/anthropics/skills): a reference source for the portable `SKILL.md` layout and specialised document, spreadsheet, PDF, and technical workflows. Check the licence of each individual skill before adoption.
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot): a community source for agent-profile and skill patterns. Treat every item as a candidate, not as an approved control.

## Intake Rule

Before a skill is active in Triton, record its source URL, version or commit, licence, cost model, required tools, data access, owner, tests, and approval in `Skill_Intake/`. Prefer a maintained open-source skill with an auditable repository; otherwise prefer a no-cost skill with transparent terms. Convert adopted guidance into an English Triton-owned skill or role instruction. Do not execute bundled scripts until they have been reviewed.

## Initial Candidate Set

1. OpenAI Docs: current official OpenAI and Codex guidance.
2. Secure code review: read-only review with explicit findings and evidence.
3. Test design and regression testing: test-first, reproducible evidence.
4. Refactoring: small, reversible changes with test protection.
5. Decision-record documentation: record alternatives, evidence, owner, and sign-off.
6. Document, PDF, and spreadsheet processing: only when the appropriate local libraries and privacy classification are available.

## Continuous Evaluation and Evolution

The `Role_Skill_Evolution_Manager` observes role and skill KPIs and can recommend bounded trial variants. Its policy and KPI definitions are in `SKILL_EVOLUTION_GOVERNANCE.md`; `role_skill_observer.py` stores append-only evaluation evidence and makes recommendations only. It cannot overwrite an active role, skill, model route, or MCP configuration.
