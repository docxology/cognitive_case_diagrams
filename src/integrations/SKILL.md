---
name: ccd-integrations
description: Route MCP/agent-integration work (tools, resources, containment, experiments projection) in cognitive_case_diagrams to src/integrations and its pinned contracts.
---

# Integration surface workflow

Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then
[docs/agent_integrations.md](../docs/agent_integrations.md). Tool names,
bounds, allowlist entries, and experiments projection fields are pinned by
`tests/test_mcp_server.py` and `tests/test_agent_interface.py` — update those
tests in the same change. The claim ledger
([docs/claim_ledger.md](../docs/claim_ledger.md)) is canonical for what each
tool means; adapters must not soften a documented limit.
