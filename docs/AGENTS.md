# 🤖 AGENTS.md — docs/

## Overview

The `docs/` directory contains technical reference documentation for the `cognitive_case_diagrams` project (*Compositional Approaches to Linguistic Case for Cognitive Modeling*, [`../manuscript/config.yaml`](../manuscript/config.yaml) `paper.title`). This is the central hub for developer-facing deep dives, API references, theory-to-code mappings, architectural decision records, and extension guides.

## Contents

| File | Purpose |
|------|---------|
| [`architecture_overview.md`](architecture_overview.md) | Package dependency graph, data flow, design principles |
| [`theory_implementation_map.md`](theory_implementation_map.md) | Maps each theoretical concept to its Python implementation |
| [`api_reference.md`](api_reference.md) | Full public API reference for all `src/` modules |
| [`glossary.md`](glossary.md) | ~100 term glossary: math ↔ linguistics ↔ code ↔ distributional RL |
| [`literature_guide.md`](literature_guide.md) | Annotated bibliography (5 pillars + extensions + 2024–2026 frontier) |
| [`manuscript_figure_index.md`](manuscript_figure_index.md) | Index of all manuscript figures and their generation scripts |
| [`extension_guide.md`](extension_guide.md) | How to add new case systems, diagram types, or ML integrations |
| [`quickstart_tutorial.md`](quickstart_tutorial.md) | Step-by-step setup, examples, and test execution |
| [`README.md`](README.md) | Quick-start navigation for the `docs/` hub |

## What Belongs Here

**YES** — put here:
- Architectural decision records (ADRs)
- Theory-to-code mappings (which manuscript equation → which function)
- API references cross-indexed with manuscript sections
- Extension guides, design patterns, and advanced tutorials
- Glossaries, annotated bibliographies, and notation reference links

**NO** — do not put here:
- Source code or test files (those go in `src/` and `tests/`)
- Manuscript text (that goes in `manuscript/`)
- Generated output (that goes in `output/`)

## Architectural Decision Records

### ADR-001: Manuscript-Aligned Package Structure
Each `src/` subpackage maps directly to a manuscript section (`§2` → `case_systems/`, etc.). This alignment makes it trivial to trace any equation or formalism to its implementation.

### ADR-002: Zero-Mock Test Policy
All tests use real mathematical objects. No `MagicMock`, no `patch`. This ensures tests reflect actual computational behavior, not mocked expectations. See `tests/AGENTS.md` for details.

### ADR-003: Visualization Accessibility
All figure fonts must meet the 16pt floor (`FONT_SIZE_FLOOR = 16` in `src/visualization/styles.py`). Export at 150 DPI. This is a hard requirement for publication readability.

### ADR-004: CasePOVM Name Field
`CasePOVM` carries a `name: str = "povm"` field used by `quantum_plots.py` to generate default output filenames. Always set a descriptive name when constructing named POVMs.

### ADR-005: Modular Cognitive + DAIF Packages
`src/cognitive/` uses 6 focused modules (free energy, belief, belief update, prediction error, action selection, reanalysis). Distributional Active Inference (DAIF) was promoted to its own `src/daif/` subpackage (7 modules, 25 public symbols) to cleanly separate point-estimate cognitive methods from full-distributional return representations.

### ADR-006: DisCoCirc Discourse Pipeline
DisCoCirc discourse analysis (§4c) uses the two-stage approach: (1) sentence-level pregroup derivation via DisCoPy, (2) circuit construction with persistent entity wires. The `Discourse` class in `src/diagrams/string_diagram.py` manages entity wire threading. External CCG → DisCoCirc pipelines (e.g., `lambeq` Gen II) are an optional dependency, not required for core functionality.

### ADR-007: Manuscript-Code Parity Enforcement
Every equation label (`\label{eq:...}`) in the manuscript must correspond to a documented Python function. The mapping is tracked in [`theory_implementation_map.md`](theory_implementation_map.md). New equations should be implemented *before* being added to the manuscript, ensuring computational verifiability. The reverse mapping (function → equation) should appear in function docstrings.

### ADR-008: DAIF vs Cognitive Package Boundary
Use `src/cognitive/` for **point-estimate** active inference (scalar beliefs, KL divergence, single-step updates). Use `src/daif/` for **distributional** methods (return distributions, quantile TD, Wasserstein distances, Bethe free energy). If a function operates on `DistributionalReturn` objects or produces `ERPProfile` outputs, it belongs in `daif/`. If it operates on scalar `CaseDiagramBelief` probabilities only, it belongs in `cognitive/`.

### ADR-009: DAIF Convergence Protocol
All DAIF inference runs must produce a `DAIFResult` including convergence diagnostics. The `convergence_diagnostics()` function checks: (1) monotone FE decrease, (2) relative reduction %, (3) final step size < 1% of FE range. When adding new inference algorithms to `src/daif/inference.py`, they must populate  `fe_trajectory` and call `convergence_diagnostics()`. Risk-distortion modes (`neutral`, `optimistic`, `pessimistic`, `CVaR`) must not alter the convergence criterion — they only affect policy selection via `G_policy()`. Quantile calibration can be assessed post-hoc via `quantile_coverage()` from `src/daif/metrics.py`.

## Cross-References

- Theory ↔ Code: See [`theory_implementation_map.md`](theory_implementation_map.md) and individual module `AGENTS.md` files
- Architecture: See [`architecture_overview.md`](architecture_overview.md) for dependency graph and data flow
- Test coverage: run `uv run pytest tests/ --cov=src` from `projects/cognitive_case_diagrams/` (≥90% line coverage on `src/` required; see `tests/AGENTS.md` for policy)
- DAIF subpackage: `src/daif/AGENTS.md` (7 modules, 25 symbols; `tests/test_daif*.py`)
- Manuscript: `manuscript/AGENTS.md`
- Source API: `src/AGENTS.md`
- Terms: [`glossary.md`](glossary.md) (~100 terms across 12 domains)
- Literature: [`literature_guide.md`](literature_guide.md) (80+ BibTeX entries, organized by pillar)

## Documentation Changelog

| Date | Change |
|------|--------|
| 2026-03-22 | Deep DAIF documentation improvements: +26 glossary terms (distributional RL foundations, surprisal decomposition), +6 literature refs (Dabney QR-DQN/IQN, Li-Futrell, Kuleshov, Rowland), DAIF internal architecture mermaid diagram + configurable parameters table, quickstart expanded to 5 DAIF subsections, ADR-009 (convergence protocol), updated cross-reference counts |
| 2026-03-19 | Added `architecture_overview.md`, `glossary.md`, `literature_guide.md`, `quickstart_tutorial.md`; expanded `extension_guide.md` with advanced patterns and CI/CD checklist; added ADR-006 through ADR-008; expanded `README.md` with conceptual roadmap and personas |
| 2026-03-16 | DAIF promoted to `src.daif/` subpackage; §7 split into §7a + §7c; all docs updated |
| 2026-03-15 | Initial docs/ directory created with API reference, theory map, figure index, extension guide |
