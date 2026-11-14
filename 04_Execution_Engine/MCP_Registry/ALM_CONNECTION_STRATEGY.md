# ALM Connection Strategy

## Recommended Order

1. Continue with the controlled Shadow Backlog until an actual sandbox exists.
2. Evaluate **OpenProject Community Edition** as the free self-hosted default: it supports hybrid work management and exposes documented REST and MCP interfaces.
3. Use **Atlassian Rovo MCP** only if a Jira tenant is selected and the user completes OAuth authorisation; start read-only.
4. Treat Plane Community Edition as a secondary open-source evaluation option. It has a REST API and webhooks, but its Community Edition does not provide every governance feature; do not assume a native MCP endpoint without verifying the deployed version.

## Connection Sequence

1. Create a sandbox with synthetic work items.
2. The ALM Administrator defines the smallest usable information model and import mapping from the Shadow Backlog.
3. Connect with a least-privilege account; test read-only discovery, then draft creation, then explicitly confirmed updates.
4. Reconcile IDs, owners, states, links, and evidence before declaring the ALM system of record.
5. Measure administrative burden, traceability completeness, decision usefulness, and failed automation attempts; retain a rollback/export route.

## No Hidden Connection

Triton stores no tenant URL, token, OAuth refresh token, or credentials in this repository. Activation requires a separate local secret configuration and an approved data route.
