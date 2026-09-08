---
name: ccd-cognitive
description: Source-grounded routing for the cognitive examples in cognitive_case_diagrams.
---

# cognitive workflow

Use when changing or explaining `src/cognitive`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Categorical probabilities, fixed-model KL/free energy, Bayesian updates, and uncalibrated mismatch scores. Likelihoods must be finite and nonnegative and have positive evidence. Sequential updates consume each supplied likelihood once. Policy-score inputs are caller-defined; neural interpretations require additional evidence.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
