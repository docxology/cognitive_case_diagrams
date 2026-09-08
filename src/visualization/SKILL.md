---
name: ccd-visualization
description: Source-grounded routing for the visualization examples in cognitive_case_diagrams.
---

# visualization workflow

Use when changing or explaining `src/visualization`. Read [README.md](README.md) and [AGENTS.md](AGENTS.md), then inspect the source signature and relevant tests before calling an API.

Source-generated diagrams and synthetic numerical plots. Captions, labels, units, and provenance must agree with the data. Never create arbitrary confidence bands, empirical comparisons, or physical interpretations from synthetic scores. DisCoPy is a required project dependency; schematic native drawings are not independent proofs.

Verification: from the project root, `uv run python scripts/quality_gate.py --coverage`. Update the [method contracts](../../docs/method_contracts.md) if behavior changes. Do not promote synthetic examples or compatibility names to mathematical, empirical, or operational guarantees.
