---
name: ccd-topos-theory
description: Source-grounded routing for the topos_theory examples in cognitive_case_diagrams.
---

# topos_theory workflow

Use when changing or explaining `src/topos_theory`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Textual theory presentations and profile comparisons. `ClassifyingTopos` stores presentation statistics only. `compare_theory_presentations()` is the canonical comparison; matching counts are neither necessary nor sufficient for Morita equivalence. `bridge_transfer()` never authorizes theorem transfer without a witness (none is implemented).

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
