---
name: cognitive-case-diagrams
description: Route cognitive_case_diagrams agent work to the MCP server, bounded method tools, and the honest claim ledger before calling or interpreting anything.
---

# Cognitive case diagrams — agent entry point

This repository serves its synthetic numerical examples to agents over MCP
(`src/integrations`, official Python SDK) and documents the honest scope of
every name in [docs/method_contracts.md](docs/method_contracts.md) and
[docs/claim_ledger.md](docs/claim_ledger.md). All canonical numerical inputs
are synthetic; a returned number is a model quantity, not an empirical
measurement, and no tool is a security boundary.

## Serving agents

- Configure an MCP host with `ccd-mcp` (console script) or
  `python -m src.integrations` per [docs/agent_integrations.md](docs/agent_integrations.md).
- `ccd-mcp --list-tools` prints the bounded tool catalog; the server exposes
  17 read-only tools, capability/claim resources, synthetic experiment
  results, and an allowlisted artifact index.
- Tool semantics (what each tool actually computes and what it does not) are
  in `docs/agent_integrations.md` and the `ccd://capabilities` resource.

## Working in the checkout

- Source work: read [src/AGENTS.md](src/AGENTS.md) and the owning package's
  README/AGENTS/SKILL first; source signatures and tests are authoritative.
- Regeneration order and gates: [README.md](README.md) and
  [scripts/README.md](scripts/README.md); the quality gate enforces the 90%
  line-and-branch floor and no mocking.
- Interpretation boundaries live in [docs/claim_ledger.md](docs/claim_ledger.md);
  do not restate unsupported claims as established results.
