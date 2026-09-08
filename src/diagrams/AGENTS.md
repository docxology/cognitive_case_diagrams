# Agent notes: diagrams

Read the [project guidance](../../AGENTS.md), [source guidance](../AGENTS.md), and [local module map](README.md).

Explicit DisCoPy pregroup constructions, tensor examples, diagram counts, and entity-name bookkeeping. `Discourse` does not infer coreference or implement a complete DisCoCirc semantic state update. `MagnitudeHomologyMetrics` contains a synthetic cup/cap score, not homology or measured decoherence.

Business logic belongs in these source modules; scripts orchestrate it. Preserve compatible APIs where practical, but document any misleading legacy names and reject invalid input rather than returning plausible substitute results. Add analytic negative controls for changed mathematical contracts. Use fixed inputs or RNG seeds and no mocking frameworks.

Before completion, run the project quality gate and regenerate affected figures, metrics, and hydrated manuscript. The [method contracts](../../docs/method_contracts.md) and [claim ledger](../../docs/claim_ledger.md) must remain consistent with source. Cache, build, and dot-directories are outside the documentation pass. No nested content folders currently require additional guidance.
