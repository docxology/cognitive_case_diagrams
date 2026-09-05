# 🤖 AGENTS.md — docs/

## Overview

The `docs/` directory contains technical reference documentation for the `cognitive_case_diagrams` project (*Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case*, v2.3 / 2026-04-22, [`docs/manuscript/config.yaml`](manuscript/config.yaml) `paper.title`). This is the central hub for developer-facing deep dives, API references, theory-to-code mappings, architectural decision records, and extension guides.

## Contents

| File | Purpose |
|------|---------|
| [`architecture_overview.md`](architecture_overview.md) | Package dependency graph, data flow, design principles |
| [`theory_implementation_map.md`](theory_implementation_map.md) | Maps each theoretical concept to its Python implementation |
| [`api_reference.md`](api_reference.md) | Full public API reference for all `src/` modules |
| [`glossary.md`](glossary.md) | Table glossary: math ↔ linguistics ↔ code ↔ distributional RL |
| [`literature_guide.md`](literature_guide.md) | Annotated bibliography (five pillars + extensions + sixth-strand synthesis via §7–§7b) |
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
- Manuscript text (that goes in `docs/manuscript/`)
- Generated output (that goes in `output/`)

## Architectural Decision Records

### ADR-001: Manuscript-Aligned Package Structure
Each `src/` subpackage maps directly to a manuscript section (`§2` → `case_systems/`, etc.). This alignment makes it trivial to trace any equation or formalism to its implementation.

### ADR-002: Zero-Mock Test Policy
All tests use real mathematical objects. No `MagicMock`, no `patch`. This ensures tests reflect actual computational behavior, not mocked expectations. See `tests/AGENTS.md` for details.

### ADR-003: Visualization Accessibility
All figure fonts must meet the 16pt floor (`FONT_SIZE_FLOOR = 16` in `src/visualization/styles.py`). Export at `FIGURE_DPI = 300`, the value the same module enforces. This is a hard requirement for publication readability.

### ADR-004: CasePOVM Name Field
`CasePOVM` carries a `name: str = "povm"` field used by `quantum_plots.py` to generate default output filenames. Always set a descriptive name when constructing named POVMs.

### ADR-005: Modular Cognitive + DAIF Packages
`src/cognitive/` uses 7 focused modules (`free_energy`, `belief`, `belief_updating`, `prediction_error`, `action_selection`, `reanalysis`, `figure_data`). Distributional Active Inference (DAIF) was promoted to its own `src/daif/` subpackage (7 modules, 25 public symbols in `daif.__all__`) to cleanly separate point-estimate cognitive methods from full-distributional return representations.

### ADR-006: DisCoCirc Discourse Pipeline
DisCoCirc discourse analysis (§4c) uses the two-stage approach: (1) sentence-level pregroup derivation via DisCoPy, (2) circuit construction with persistent entity wires. The `Discourse` class in `src/diagrams/string_diagram.py` manages entity wire threading. External CCG → DisCoCirc pipelines (e.g., `lambeq` Gen II) are an optional dependency, not required for core functionality.

### ADR-007: Manuscript-Code Parity Enforcement
Every equation label (`\label{eq:...}`) in the manuscript must correspond to a documented Python function. The mapping is tracked in [`theory_implementation_map.md`](theory_implementation_map.md). New equations should be implemented *before* being added to the manuscript, ensuring computational verifiability. The reverse mapping (function → equation) should appear in function docstrings.

### ADR-008: DAIF vs Cognitive Package Boundary
Use `src/cognitive/` for **point-estimate** active inference (scalar beliefs, KL divergence, single-step updates). Use `src/daif/` for **distributional** methods (return distributions, quantile TD, Wasserstein distances, Bethe free energy). If a function operates on `DistributionalReturn` objects or produces `ERPProfile` outputs, it belongs in `daif/`. If it operates on scalar `CaseDiagramBelief` probabilities only, it belongs in `cognitive/`.

### ADR-009: DAIF Convergence Protocol
All DAIF inference runs must produce a `DAIFResult` including convergence diagnostics. The `convergence_diagnostics()` function checks: (1) monotone FE decrease, (2) relative reduction %, (3) final step size < 1% of FE range. When adding new inference algorithms to `src/daif/inference.py`, they must populate  `fe_trajectory` and call `convergence_diagnostics()`. Risk-distortion modes (`neutral`, `optimistic`, `pessimistic`, `CVaR`) must not alter the convergence criterion — they only affect policy selection via `G_policy()`. Quantile calibration can be assessed post-hoc via `quantile_coverage()` from `src/daif/metrics.py`.

### ADR-010: Figure Count Parity
The manuscript figure count must remain synchronized across four sources of truth: (1) the `docs/manuscript_figure_index.md` inventory table, (2) the physical PNG files in `output/figures/`, (3) Markdown image references in `docs/manuscript/*.md` (standard image syntax, paths under `output/figures/`), and (4) the `${total_figures}` metric auto-injected from `output/metrics.json` by `src.generate_manuscript_metrics.collect_metrics`. As of this revision the canonical count is **30 figures** (original 27 plus three pedagogical unpacking companions for §3, §4b, §4c — `pregroup_reduction_unpacking.png`, `snake_equation_unpacking.png`, `discocirc_entity_persistence.png`). Any commit adding or removing a figure must update all four; the `generate_diagrams.py` orchestrator enforces source (2) by enumerating render calls, and the metrics generator enforces source (4) by counting PNGs in `output/figures/`.

### ADR-011: Documentation Duality Standard
Every `src/` subpackage must carry three complementary documentation files: (1) `AGENTS.md` — machine-readable operational guide (architecture, API, ADRs), (2) `README.md` — human-readable quick reference, (3) `SKILL.md` — MCP-aligned skill descriptor enabling AI agents to discover and invoke module capabilities without hallucinating API signatures. This three-file standard extends to `scripts/`, `tests/`, and `docs/` directories.

### ADR-012: Cross-Linguistic Typological Coverage
Alignment functors (`accusative_alignment()`, `ergative_alignment()`, `tripartite_alignment()`, `active_stative_alignment()`) must cover the four major morphosyntactic alignment systems attested in natural languages. The `FluidSFunctor` additionally handles split-S systems where agent/patient of intransitives is context-dependent. Any new alignment system added to `src/case_systems/` must be validated against attested typological data (cf. Dixon, 1994; Comrie, 1978).

## Cross-References

- Theory ↔ Code: See [`theory_implementation_map.md`](theory_implementation_map.md) and individual module `AGENTS.md` files
- Architecture: See [`architecture_overview.md`](architecture_overview.md) for dependency graph and data flow
- Test coverage: run `uv run pytest tests/ --cov=src` from this project root (`projects/ongoing/ActiveInference/cognitive_case_diagrams/` inside the template monorepo) — ≥90% line coverage on `src/` required; see `tests/AGENTS.md` for policy
- DAIF subpackage: `src/daif/AGENTS.md` (7 modules, 25 public symbols in `daif.__all__`; `tests/test_daif*.py`)
- Manuscript: `docs/manuscript/AGENTS.md`
- Source API: `src/AGENTS.md`
- Terms: [`glossary.md`](glossary.md) (term rows grouped by domain section; the file itself is the count of record)
- Literature: [`literature_guide.md`](literature_guide.md) (106 BibTeX entries in `docs/manuscript/references.bib`; five pillars plus extensions and sixth-strand reading synthesis)

## Documentation Changelog

| Date | Change |
|------|--------|
| 2026-04-22 | v2.3 release sync: canonical title corrected across all AGENTS/README files to match `config.yaml` (`Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case`); DOI `10.5281/zenodo.19695260` propagated; `cognitive/` module count corrected 6→7 (ADR-005); `quantum/` module count corrected 1→2; `visualization/` module count corrected 13/14→15; scripts inventory includes `01_generate_manuscript_metrics.py` and `generate_category_unpacking_figures.py`; figure count reaffirmed at 30; pipeline stage numbering aligned to the engine's `scripts/pipeline/stage_*.py` DAG at the template monorepo root (the stage inventory lives there, not in this doc) |
| 2026-04-10 | Manuscript section files: removed redundant per-file `**Version**` / `**Status**` lines; edition single-sourced in `config.yaml`; updated [`docs/manuscript/README.md`](manuscript/README.md) |
| 2026-04-09 | Glossary table row count set to **117** (`docs/README.md`, hub bullets); `coverage.json` ignored at repo root |
| 2026-04-09 | Bibliography inventory aligned to **101** `@` entries in `docs/manuscript/references.bib` (manuscript AGENTS, `docs/README.md`, `literature_guide.md`) |
| 2026-04-10 | Documentation coherence: unified manuscript § numbering across `docs/`, `src/**/*.md`, and theory map (§7 scalar cognitive, §7c DAIF, §8 quantum); corrected DAIF `__all__` count to 25; aligned `architecture_overview` / `extension_guide` topos imports with code (`enriched_cat`); canonical map in `docs/README.md` |
| 2026-04-05 | Final hardening audit: added missing `discopy_sentence_progression.png` to figure index; fixed stale counts (test files 46→63, figures 26→27, bib entries 80+→101); added ADR-010 (figure count parity), ADR-011 (documentation duality), ADR-012 (cross-linguistic coverage); updated all `Last updated` dates; fixed MD060/MD022/MD032 lint warnings across 7 docs; enriched glossary, literature guide, and architecture overview with substantive content |
| 2026-03-22 | Deep DAIF documentation improvements: +26 glossary terms (distributional RL foundations, surprisal decomposition), +6 literature refs (Dabney QR-DQN/IQN, Li-Futrell, Kuleshov, Rowland), DAIF internal architecture mermaid diagram + configurable parameters table, quickstart expanded to 5 DAIF subsections, ADR-009 (convergence protocol), updated cross-reference counts |
| 2026-03-19 | Added `architecture_overview.md`, `glossary.md`, `literature_guide.md`, `quickstart_tutorial.md`; expanded `extension_guide.md` with advanced patterns and CI/CD checklist; added ADR-006 through ADR-008; expanded `README.md` with conceptual roadmap and personas |
| 2026-03-16 | DAIF promoted to `src.daif/` subpackage; §7 cluster expanded (§7, §7b, §7c); all docs updated |
| 2026-03-15 | Initial docs/ directory created with API reference, theory map, figure index, extension guide |
