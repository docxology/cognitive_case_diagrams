---
name: ccd-quantum
description: Source-grounded routing for the quantum examples in cognitive_case_diagrams.
---

# quantum workflow

Use when changing or explaining `src/quantum`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Finite POVMs and density matrices with explicit Hermitian/PSD/normalization checks. The canonical figure uses orthogonal projectors and a diagonal mixture, so it shows classical outcome probabilities, not interference. No quantum hardware, sheaf model, or TQNN is implemented.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
