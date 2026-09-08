# Agent notes: cognitive

Read the [project guidance](../../AGENTS.md), [source guidance](../AGENTS.md), and [local module map](README.md).

Categorical probabilities, fixed-model KL/free energy, Bayesian updates, and uncalibrated mismatch scores. Likelihoods must be finite and nonnegative and have positive evidence. Sequential updates consume each supplied likelihood once. Policy-score inputs are caller-defined; neural interpretations require additional evidence.

Business logic belongs in these source modules; scripts orchestrate it. Preserve compatible APIs where practical, but document any misleading legacy names and reject invalid input rather than returning plausible substitute results. Add analytic negative controls for changed mathematical contracts. Use fixed inputs or RNG seeds and no mocking frameworks.

Before completion, run the project quality gate and regenerate affected figures, metrics, and hydrated manuscript. The [method contracts](../../docs/method_contracts.md) and [claim ledger](../../docs/claim_ledger.md) must remain consistent with source. Cache, build, and dot-directories are outside the documentation pass. No nested content folders currently require additional guidance.
