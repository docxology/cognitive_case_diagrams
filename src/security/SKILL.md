---
name: ccd-security
description: Source-grounded routing for the security examples in cognitive_case_diagrams.
---

# security workflow

Use when changing or explaining `src/security`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

A finite, supplied-label role-policy checker. Unknown roles are rejected before identity checks; mutable category adjacency is refreshed. Assignment checks use pairwise connectivity in either direction, not a directed authorization trace. No text classifier, authentication service, runtime reference monitor, or measured attack detector is provided.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
