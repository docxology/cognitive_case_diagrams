---
name: ccd-enriched-cat
description: Source-grounded routing for the enriched_cat examples in cognitive_case_diagrams.
---

# enriched_cat workflow

Use when changing or explaining `src/enriched_cat`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Candidate hom-matrices, explicit multiplicative composition checks, max-product closure, and matrix magnitude. The standard matrix is synthetic and violates composition before closure. Pseudoinverse magnitudes require valid left/right weighting residuals. Threshold clusters are weak connected components, not pairwise-close cliques.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
