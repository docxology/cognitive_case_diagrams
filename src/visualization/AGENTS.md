# Agent notes: visualization

Read the [project guidance](../../AGENTS.md), [source guidance](../AGENTS.md), and [local module map](README.md).

Source-generated diagrams and synthetic numerical plots. Captions, labels, units, and provenance must agree with the data. Never create arbitrary confidence bands, empirical comparisons, or physical interpretations from synthetic scores. DisCoPy is a required project dependency; schematic native drawings are not independent proofs.

Business logic belongs in these source modules; scripts orchestrate it. Preserve compatible APIs where practical, but document any misleading legacy names and reject invalid input rather than returning plausible substitute results. Add analytic negative controls for changed mathematical contracts. Use fixed inputs or RNG seeds and no mocking frameworks.

Before completion, run the project quality gate and regenerate affected figures, metrics, and hydrated manuscript. The [method contracts](../../docs/method_contracts.md) and [claim ledger](../../docs/claim_ledger.md) must remain consistent with source. Cache, build, and dot-directories are outside the documentation pass. No nested content folders currently require additional guidance.
