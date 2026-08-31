# 🤖 AGENTS.md — cognitive_case_diagrams

> **Agent operational guide** for the `cognitive_case_diagrams` project.  
> Read this first before modifying any source, manuscript, or test file.

**Publication title** (canonical): *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case* — [`docs/manuscript/config.yaml`](docs/manuscript/config.yaml) `paper.title`. (Version 2.3, 2026-04-22, DOI [10.5281/zenodo.19695260](https://doi.org/10.5281/zenodo.19695260).)

**Path:** `projects/cognitive_case_diagrams/` — pipeline-discoverable. Run `uv run pytest` and figure scripts from the project directory.

**Versions:** The **Python package** semver is in [`pyproject.toml`](pyproject.toml) (`project.version`, e.g. **2.3.0**). The **manuscript edition** (e.g. **v2.3**, 2026-04-22) is recorded in [`docs/manuscript/AGENTS.md`](docs/manuscript/AGENTS.md) and [`docs/manuscript/config.yaml`](docs/manuscript/config.yaml). Patch bumps can track manuscript releases; they may still diverge when only one side changes.

---

## 📋 Table of Contents

1. [Project Mission](#project-mission)
2. [Architecture Overview](#architecture-overview)
3. [Module Map (Manuscript Aligned)](#module-map-manuscript-aligned)
4. [Directory Structure](#directory-structure)
5. [Pipeline and Entry Points](#pipeline-and-entry-points)
6. [Testing Standards](#testing-standards)
7. [Manuscript Standards](#manuscript-standards)
8. [Documentation Standards](#documentation-standards)
9. [Operational Procedures](#operational-procedures)

---

## 🎯 Project Mission

The manuscript formalizes linguistic case systems using category theory and integrates them into the Active Inference framework via the CEREBRUM architecture. The core thesis: commutative diagrams are cognitively privileged representations because they simultaneously encode:

- The **algebraic structure** of case role relations (functors, morphisms)
- The **distributional semantics** of NLP (DisCoCat, DisCoCirc, QNLP)
- The **inference process** of cognitive agents (active inference, free energy)

**Five converging theoretical pillars:**

| § | Pillar | Key Formalism |
|---|--------|---------------|
| §2 | Linguistic Typology | Case roles as objects, alignment as functors |
| §3–4 | Categorial Grammar | Lambek calculus, pregroup, DisCoCat |
| §4b | Compact closure / complexity | Snake, normal form, `syntactic_complexity_score` |
| §4c | DisCoCirc discourse | Entity-state wires, `Discourse`, discourse circuits |
| §5 | Enriched Categories | [0,1]-hom-values, categorical magnitude |
| §6 | Topos Theory | Morita equivalence, geometric theories |

**Advanced extensions (§7–§9b):**

| § | Extension | Module |
|---|-----------|--------|
| §7 | Active inference (scalar beliefs, variational FEP) | `src/cognitive/` |
| §7c | Distributional Active Inference (DAIF) | `src/daif/` |
| §8 | Quantum POVM Case Assignment | `src/quantum/` |
| §9b | Cognitive Security | `src/security/` |

**Section naming:** The manuscript uses **§7** for scalar active inference (`07_cognitive_integration.md`), **§7b** for computational verification, **§7c** for DAIF (`07c_daif_results.md`). Package comments and docs use the same numbers — see [`src/__init__.py`](src/__init__.py) import blocks and `__all__`.

---

## 🏗️ Architecture Overview

```
cognitive_case_diagrams/
├── AGENTS.md               ← You are here
├── README.md               ← Quick start
├── pyproject.toml          ← Package config + test/coverage settings
├── docs/                   ← Technical reference documentation
├── docs/manuscript/             ← Research manuscript (Pandoc Markdown)
├── output/                 ← Generated artifacts (figures, PDFs, reports)
├── scripts/                ← Thin orchestrators (NO scientific logic here)
├── src/                    ← All scientific business logic (Layer 2)
│   ├── case_systems/       ← §2: Case theory, alignment, Fluid-S
│   ├── diagrams/           ← §3–§4c: String diagrams, complexity, discourse, ditransitive
│   ├── enriched_cat/       ← §5: Enriched categories, magnitude
│   ├── topos_theory/       ← §6: Topos, Morita equivalence
│   ├── cognitive/          ← §7: Active inference, free energy (scalar beliefs)
│   ├── daif/               ← §7c: Distributional Active Inference (return distributions)
│   ├── quantum/            ← §8: POVM, quantum case
│   ├── security/           ← §9b: Cognitive security, type violations
│   └── visualization/      ← Publication-quality figure generation
└── tests/                  ← Full suite: `uv run pytest tests/ --collect-only -q` (≥90% line coverage on `src/` required)
```

### Thin Orchestrator Pattern

**CRITICAL**: `scripts/` are **thin orchestrators** only. They:
- Import domain logic from `src/`
- Import utilities from `infrastructure/`
- Handle I/O and rendering
- Contain **NO** scientific, mathematical, or statistical logic

Putting business logic in scripts **breaks the architecture**.

---

## 📦 Module Map (Manuscript-Aligned)

| Manuscript Section | Python Package | Key Classes/Functions |
|-------------------|---------------|----------------------|
| §2 Case Systems | `src.case_systems` | `CaseRole`, `CaseCategory`, `Morphism`, `AlignmentFunctor`, `FluidSFunctor`, `NaturalTransformation` |
| §3–4 Grammar/Semantics | `src.diagrams` | `Sentence`, `Discourse`, `string_diagram`; optional `discopy_diagrams` (visualization) |
| §4b Compact closure / complexity | `src.diagrams`, visualization | `complexity_metrics`, snake/normal-form checks (DisCoPy) |
| §4c DisCoCirc discourse | `src.diagrams`, visualization | `Discourse` (`string_diagram`), `render_discopy_discocirc_discourse`, `render_discocirc_discourse` |
| §5 Enriched | `src.enriched_cat` | `EnrichedCategory`, `magnitude()`, `role_clusters()` |
| §6 Topos | `src.topos_theory` | `GeometricTheory`, `ClassifyingTopos`, `check_morita_equivalence()` |
| §7 Active Inference | `src.cognitive` | `CaseDiagramBelief`, `kl_divergence()`, `variational_free_energy()`, `update_belief()`, `sequential_belief_update()`, `prediction_error()`, `p600_amplitude_ratio()`, `expected_free_energy()`, `magnitude_reanalysis_cost()`, `n400_amplitude_proxy()` |
| §7c DAIF | `src.daif` | `DistributionalReturn`, `DAIFResult`, `ERPProfile`, `push_forward_return()`, `distributional_case_assignment()`, `G_policy()`, `distributional_prediction_error()`, `convergence_diagnostics()`, and related quantile/VMP/Bethe APIs (see `src/__init__.py` `__all__`) |
| §8 Quantum | `src.quantum` | `CasePOVM`, `case_probability()`, `crisp_case_povm()`, `fluid_s_povm()` |
| §9b Security | `src.security` | `TypeViolation`, `CaseFrameValidator`, `detect_type_violation()`, `injection_score()` |
| Visualization | `src.visualization` | All plot/render functions (`uv run pytest tests/ --cov=src/visualization`) |

---

## 📂 Directory Structure

See each directory's own **AGENTS.md** and **README.md** for detailed documentation:

| Directory | AGENTS.md | README.md | Purpose |
|-----------|-----------|-----------|---------|
| [`docs/`](docs/) | [AGENTS.md](docs/AGENTS.md) | [README.md](docs/README.md) | Technical reference and API docs |
| [`docs/manuscript/`](docs/manuscript/) | [AGENTS.md](docs/manuscript/AGENTS.md) | [README.md](docs/manuscript/README.md) | Research manuscript (inventory in docs/manuscript/AGENTS.md) |
| [`output/`](output/) | [AGENTS.md](output/AGENTS.md) | [README.md](output/README.md) | Generated artifacts |
| [`scripts/`](scripts/) | [AGENTS.md](scripts/AGENTS.md) | [README.md](scripts/README.md) | Thin orchestrators |
| [`src/`](src/) | [AGENTS.md](src/AGENTS.md) | [README.md](src/README.md) | Scientific source code |
| [`src/case_systems/`](src/case_systems/) | [AGENTS.md](src/case_systems/AGENTS.md) | [README.md](src/case_systems/README.md) | §2: Case theory |
| [`src/diagrams/`](src/diagrams/) | [AGENTS.md](src/diagrams/AGENTS.md) | [README.md](src/diagrams/README.md) | §3–§4c: Grammar, semantics, complexity, discourse |
| [`src/enriched_cat/`](src/enriched_cat/) | [AGENTS.md](src/enriched_cat/AGENTS.md) | [README.md](src/enriched_cat/README.md) | §5: Enriched categories |
| [`src/topos_theory/`](src/topos_theory/) | [AGENTS.md](src/topos_theory/AGENTS.md) | [README.md](src/topos_theory/README.md) | §6: Topos theory |
| [`src/cognitive/`](src/cognitive/) | [AGENTS.md](src/cognitive/AGENTS.md) | [README.md](src/cognitive/README.md) | §7: Active inference |
| [`src/daif/`](src/daif/) | [AGENTS.md](src/daif/AGENTS.md) | [README.md](src/daif/README.md) | §7c: Distributional Active Inference |
| [`src/quantum/`](src/quantum/) | [AGENTS.md](src/quantum/AGENTS.md) | [README.md](src/quantum/README.md) | §8: Quantum POVM |
| [`src/security/`](src/security/) | [AGENTS.md](src/security/AGENTS.md) | [README.md](src/security/README.md) | §9b: Cognitive security |
| [`src/visualization/`](src/visualization/) | [AGENTS.md](src/visualization/AGENTS.md) | [README.md](src/visualization/README.md) | Publication figures |
| [`tests/`](tests/) | [AGENTS.md](tests/AGENTS.md) | [README.md](tests/README.md) | Full test suite (no mocks); counts via `pytest --collect-only` |

---

## Pipeline and Entry Points

### Run Full Pipeline

Requires the project under `projects/cognitive_case_diagrams/`.

```bash
./run.sh --project cognitive_case_diagrams
```

### Individual Stages

**Note (2026-08-31, verified):** the numbered root scripts referenced earlier here (`scripts/01_run_tests.py`, `scripts/03_render_pdf.py`, …) exist only in the **template monorepo root**, not in this repository — running them from this checkout fails with "No such file or directory". From the monorepo checkout use its canonical `scripts/pipeline/stage_*.py` entry points (see the monorepo root `CLAUDE.md`); from this standalone checkout use the local commands below.

```bash
# From THIS project directory (standalone checkout):
cd projects/cognitive_case_diagrams        # or this repo root if standalone

# Tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# Figures / analysis
uv run python scripts/generate_diagrams.py

# Manuscript metrics + ${variable} injection (see "Manuscript metrics" below)
uv run python -m src.generate_manuscript_metrics
uv run python scripts/inject_variables.py
```

### Generate Figures Only

Works from any cwd if you use the path below (repo root) or run from inside this project with `uv run python scripts/generate_diagrams.py`.

```bash
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py
```

**§9b monoidal functor security figure:** When analysis builds `monoidal_functor_security` (`plot_monoidal_functor_security` in `src/visualization/security_plots.py`), `src.case_systems.functor` may log tensor-preservation failures (for example merges that collapse distinct roles). Those messages are intentional diagnostic output for the visualization—the figure illustrates failures— and are not treated as pipeline errors.

### Run Tests with Coverage

```bash
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=term-missing -v
```

### Manuscript metrics and `${variable}` injection

[`src/generate_manuscript_metrics.py`](src/generate_manuscript_metrics.py) writes [`output/metrics.json`](output/metrics.json). [`scripts/inject_variables.py`](scripts/inject_variables.py) substitutes `${…}` into numbered manuscript chapters and writes [`output/manuscript/`](output/manuscript/); the PDF renderer prefers that directory when present ([`infrastructure/rendering/pipeline.py`](../../../infrastructure/rendering/pipeline.py) `_resolve_manuscript_dir`).

```bash
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=json:coverage.json
uv run python -m src.generate_manuscript_metrics
uv run python scripts/inject_variables.py
# From template repository root:
uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams
```

`coverage.json` policy (commit or regenerate): [`tests/AGENTS.md`](tests/AGENTS.md). Placeholder catalog: [`docs/manuscript/config.yaml`](docs/manuscript/config.yaml).

---

## 🧪 Testing Standards

### Coverage Requirements
- **≥ 90%** total coverage on `src/` (line + branch; `branch = true` in `pyproject.toml`; `uv run pytest tests/ --cov=src --cov-report=term-missing`)
- Test and file counts change over time; use `uv run pytest tests/ --collect-only -q` and `ls tests/test_*.py | wc -l`
- Coverage enforced via `pyproject.toml` `[tool.coverage.report] fail_under = 90`

### Zero-Mock Policy (ABSOLUTE PROHIBITION)
**Never use** `MagicMock`, `unittest.mock.patch`, `mocker.patch`, or any mock framework.

All tests must use real objects:
- Real `numpy` arrays and matrices
- Real `matplotlib` figure generation to temp files
- Real `CaseDiagramBelief`, `CasePOVM`, `TypeViolation`, `FluidSFunctor` instances
- Real file I/O with `tempfile.NamedTemporaryFile`

### Test File → Source Module Mapping (`tests/test_*.py`)

Files follow the `test_{package}_{module}.py` naming convention:

| Test File | Source Module |
|-----------|--------------|
| `test_case_systems_case_category.py` | `src/case_systems/case_category.py` |
| `test_case_systems_fluid_s.py` | `src/case_systems/fluid_s.py` |
| `test_case_systems_functor.py` | `src/case_systems/functor.py` |
| `test_case_systems_natural_transformation.py` | `src/case_systems/natural_transformation.py` |
| `test_diagrams_string_diagram.py` | `src/diagrams/string_diagram.py` |
| `test_diagrams_string_diagram_coverage.py` | `src/diagrams/string_diagram.py` (coverage) |
| `test_diagrams_complexity_metrics.py` | `src/diagrams/complexity_metrics.py` |
| `test_diagrams_complexity_metrics_coverage.py` | `src/diagrams/complexity_metrics.py` (coverage) |
| `test_diagrams_complexity_examples.py` | `src/diagrams/complexity_examples.py` |
| `test_diagrams_complexity_examples_coverage.py` | `src/diagrams/complexity_examples.py` (coverage) |
| `test_diagrams_ditransitive.py` | `src/diagrams/ditransitive.py` |
| `test_diagrams_generator.py` | `scripts/generate_diagrams.py` |
| `test_enriched_cat_enriched.py` | `src/enriched_cat/enriched.py` |
| `test_topos_theory_topos.py` | `src/topos_theory/topos.py` |
| `test_cognitive_integration.py` | `src/cognitive/` (integration) |
| `test_cognitive_belief.py` | `src/cognitive/belief.py` |
| `test_cognitive_free_energy.py` | `src/cognitive/free_energy.py` |
| `test_cognitive_belief_updating.py` | `src/cognitive/belief_updating.py` |
| `test_cognitive_prediction_error.py` | `src/cognitive/prediction_error.py` |
| `test_cognitive_action_selection.py` | `src/cognitive/action_selection.py` |
| `test_cognitive_reanalysis.py` | `src/cognitive/reanalysis.py` |
| `test_daif_types.py` | `src/daif/types.py` |
| `test_daif_core.py` | `src/daif/core.py` |
| `test_daif_quantile.py` | `src/daif/quantile.py` |
| `test_daif_inference.py` | `src/daif/inference.py` |
| `test_daif_prediction.py` | `src/daif/prediction.py` |
| `test_daif_policy.py` | `src/daif/policy.py` |
| `test_daif_metrics.py` | `src/daif/metrics.py` |
| `test_quantum_quantum_case.py` | `src/quantum/quantum_case.py` |
| `test_security_cognitive_security.py` | `src/security/cognitive_security.py` |
| `test_cross_module_coverage.py` | Cross-module coverage (enriched, case_category) |
| `test_visualization_styles.py` | `src/visualization/styles.py` |
| `test_visualization_category_diagrams.py` | `src/visualization/category_diagrams.py` |
| `test_visualization_enriched_diagrams.py` | `src/visualization/enriched_diagrams.py` |
| `test_visualization_functor_diagrams.py` | `src/visualization/functor_diagrams.py` |
| `test_visualization_string_diagrams.py` | `src/visualization/string_diagrams.py` |
| `test_visualization_complexity_plots.py` | `src/visualization/complexity_plots.py` |
| `test_visualization_active_inference_plots.py` | `src/visualization/active_inference_plots.py` |
| `test_visualization_quantum_plots.py` | `src/visualization/quantum_plots.py` |
| `test_visualization_security_plots.py` | `src/visualization/security_plots.py` |
| `test_visualization_fluid_s_plots.py` | `src/visualization/fluid_s_plots.py` |
| `test_visualization_discopy_diagrams.py` | `src/visualization/discopy_diagrams.py` |
| `test_visualization_daif_plots.py` | `src/visualization/daif_plots.py` |
| `test_visualization_plot_modules.py` | Multi-module visualization coverage |
| `test_visualization_syntactic_sentence_diagrams.py` | `src/visualization/syntactic_sentence_diagrams.py` |
| `test_visualization_syntactic_coverage.py` | Syntactic diagram coverage |
| `test_property_based.py` | Algebraic property tests (composition inequality, magnitude positivity, weight bounds) |
| `test_generate_manuscript_metrics.py` | `src/generate_manuscript_metrics.py` |

---

## 📝 Manuscript Standards

### Pandoc Markdown Conventions
- Use `[@author_year]` for citations (Pandoc-citeproc style)
- Use `$$...$$` blocks for display equations with `{#eq:label}` cross-refs
- Use `{#fig:label}` for figure cross-references
- Use `{#sec:label}` for section cross-references
- Never use raw LaTeX; use Pandoc-compatible Markdown

### Equation Labeling
All principal equations must have labels, e.g.:
```markdown
$$P(c \mid \rho) = \text{Tr}(E_c \rho)$$ {#eq:quantum-case}
```

### Chapter File Naming
| File | Section | Title |
|------|---------|-------|
| `00_abstract.md` | — | Abstract |
| `01_introduction.md` | §1 | Introduction |
| `01a_research_questions.md` | §1a | Research Questions |
| `02_case_systems.md` | §2 | Case Systems |
| `02b_case_categories.md` | §2b | Case Categories |
| `03_categorial_grammar.md` | §3 | Categorial Grammar |
| `03b_case_type_logic.md` | §3b | Case Type Logic |
| `04_categorical_semantics.md` | §4 | Categorical Semantics |
| `04b_compact_closure_complexity.md` | §4b | Compact closure / diagram complexity |
| `04c_discourse_complexity.md` | §4c | Discourse Complexity |
| `05_enriched_categories.md` | §5 | Enriched Categories |
| `05b_magnitude_homology.md` | §5b | Magnitude Homology |
| `06_topos_theory.md` | §6 | Topos Theory |
| `07_cognitive_integration.md` | §7 | Cognitive Integration |
| `07b_diagrammatic_cognition.md` | §7b | Diagrammatic Cognition & ERP Predictions |
| `07c_daif_results.md` | §7c | DAIF Results |
| `08_quantum_active_inference.md` | §8 | Quantum Active Inference |
| `08b_quantum_semantics.md` | §8b | Quantum Semantics |
| `09_ai_implications.md` | §9 | AI Implications |
| `09b_cognitive_security.md` | §9b | Cognitive Security |
| `10_conclusion.md` | §10 | Conclusion |
| `11_syntactic_sentence_diagrams.md` | App A | Syntactic Diagrams |
| `11b_notation.md` | App B | Complete Notation Reference (sections A–K) |
| `11c_automated_test_inventory.md` | App C | Automated test inventory |

---

## 📚 Documentation Standards

Every directory **MUST** have:
- **`AGENTS.md`**: Detailed agent-facing technical documentation (architecture, patterns, gotchas)
- **`README.md`**: Human-facing quick reference (purpose, quick start, key APIs)

Documentation must be kept in sync with code. When adding a new class or function:
1. Update the relevant `AGENTS.md` module table
2. Update the relevant `README.md` API summary
3. Add tests (maintaining ≥90% coverage)
4. Update the manuscript if it's a new theoretical contribution

---

## ⚙️ Operational Procedures

### Adding a New Source Module

1. Create `src/{subpackage}/new_module.py` with docstring, logging, and type hints
2. Export from `src/{subpackage}/__init__.py`
3. Export from `src/__init__.py` if part of the public API
4. Create `tests/test_new_module.py` (zero-mock, real data only)
5. Update `src/{subpackage}/AGENTS.md` and `README.md`
6. Verify coverage: `pytest tests/ --cov=src --cov-report=term-missing`

### Adding a Manuscript Section

1. Create `docs/manuscript/NN_section.md` following naming convention
2. Add to `preamble.md` include list
3. Add appropriate equations with `{#eq:}` labels
4. Add figure references that point to `output/figures/`
5. Update `references.bib` for any new citations
6. Update `11b_notation.md` if new symbols are introduced

### Modifying the Visualization Pipeline

1. Implement function in `src/visualization/{module}.py`
2. Export from `src/visualization/__init__.py`
3. Call from `scripts/generate_diagrams.py`
4. Add tests in `tests/test_plot_modules.py` or `tests/test_visualization.py`
5. Add figure caption reference in the appropriate manuscript section

### Troubleshooting

| Issue | Solution |
|-------|---------|
| Coverage below 90% | Check `--cov-report=term-missing`; add tests for uncovered lines |
| Hanging tests | Add `--timeout=30` flag; check for blocking matplotlib calls |
| Import errors | Ensure `pythonpath = ["src"]` in `pyproject.toml`; run from project root |
| PDF render fails | Check `preamble.md` include order; validate with `uv run python -m infrastructure.validation.cli markdown docs/manuscript/` (monorepo root: `projects/cognitive_case_diagrams/docs/manuscript/`) |
| `CasePOVM.name` error | All `CasePOVM` instances have `name: str = "povm"` default field |
