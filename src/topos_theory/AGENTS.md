# Agent notes: topos_theory

Read the [project guidance](../../AGENTS.md), [source guidance](../AGENTS.md), and [local module map](README.md).

Textual theory presentations and profile comparisons. `ClassifyingTopos` stores presentation statistics only. `compare_theory_presentations()` is the canonical comparison; matching counts are neither necessary nor sufficient for Morita equivalence. `bridge_transfer()` never authorizes theorem transfer without a witness (none is implemented).

Business logic belongs in these source modules; scripts orchestrate it. Preserve compatible APIs where practical, but document any misleading legacy names and reject invalid input rather than returning plausible substitute results. Add analytic negative controls for changed mathematical contracts. Use fixed inputs or RNG seeds and no mocking frameworks.

Before completion, run the project quality gate and regenerate affected figures, metrics, and hydrated manuscript. The [method contracts](../../docs/method_contracts.md) and [claim ledger](../../docs/claim_ledger.md) must remain consistent with source. Cache, build, and dot-directories are outside the documentation pass. No nested content folders currently require additional guidance.
