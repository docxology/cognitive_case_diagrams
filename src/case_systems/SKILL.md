---
name: ccd-case-systems
description: Source-grounded routing for the case_systems examples in cognitive_case_diagrams.
---

# case_systems workflow

Use when changing or explaining `src/case_systems`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Finite role graphs, labelled path composition, alignment maps, and natural-transformation helpers. Endpoint and weight predicates do not certify arbitrary categories or functors. `MonoidalFunctor.preserves_tensor()` is a role-separation policy, not a monoidal-law test. Fluid-S probabilities are supplied modeling inputs.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
