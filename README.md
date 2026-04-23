# Cognitive Case Diagrams

**Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case** — category-theoretic approaches to linguistic case systems in total cognitive scenario understanding

*Daniel Ari Friedman · Active Inference Institute · v2.3 (2026-04-22) · DOI [10.5281/zenodo.19695260](https://doi.org/10.5281/zenodo.19695260)*

---

## Location

This project lives at **`projects/cognitive_case_diagrams/`** and is pipeline-discoverable. Run tests and figure generation **from this directory** (commands below).

## Versions (two numbers)

| What | Where | Meaning |
|------|--------|--------|
| **Python package** | [`pyproject.toml`](pyproject.toml) `project.version` | Semver for the installable `cognitive_case_diagrams` package (currently **2.3.0**). |
| **Manuscript / paper** | [`manuscript/AGENTS.md`](manuscript/AGENTS.md) authorship block, [`manuscript/config.yaml`](manuscript/config.yaml) | Research edition (currently **v2.3**, dated **2026-04-22**, DOI `10.5281/zenodo.19695260`). Bump this when the PDF content or metadata release changes independently of API semver. |

They are intentionally separate: code releases can patch without a full manuscript revision, and manuscript edits do not always require a package version bump.

## Overview

This project formalizes linguistic case systems using category theory, integrating them into the Active Inference framework via the CEREBRUM architecture. The central argument: commutative diagrams are cognitively privileged representations because they simultaneously encode algebraic structure, distributional semantics, and inference processes.

## Formal layers, sixth strand, extensions

| § | Layer / strand | Implementation |
|---|----------------|---------------|
| §2 | Linguistic typology & case systems | `src/case_systems/` |
| §3–4 | Categorial grammar & DisCoCat | `src/diagrams/` |
| §4b | Compact closure, snake, diagram complexity | `src/diagrams/` |
| §4c | DisCoCirc discourse (entity wires) | `src/diagrams/` |
| §5 | [0,1]-enriched categories | `src/enriched_cat/` |
| §6 | Topos theory & Morita equivalence | `src/topos_theory/` |
| §7–§7b | Sixth strand: ROSE / biolinguistic–neuro interface | `src/cognitive/` + manuscript §7b |
| §7c | DAIF & neurolinguistic metrics | `src/daif/` |

**Extensions:** Quantum §8 (`src/quantum/`); AI implications §9; **protocol-level** cognitive security §9b (`src/security/`). Distributional inference code lives in `src/daif/`; §7b ties formal claims to the test suite and verification narrative.

## Quick Start

```bash
# Full pipeline from repo root
./run.sh --project cognitive_case_diagrams

# Tests with coverage (from THIS project directory — path is tests/, not projects/.../tests/)
cd projects/cognitive_case_diagrams
uv sync
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# Same tests from monorepo root (root `default-groups` include `discopy`, `rendering`, and `dev`)
cd /path/to/repository-root
uv sync
uv run pytest projects/cognitive_case_diagrams/tests/

# Generate all manuscript figures (from repo root or this directory)
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Validate markdown (from repository root)
uv run python -m infrastructure.validation.cli markdown projects/cognitive_case_diagrams/manuscript/
```

Do not run `uv sync --group rendering` from `projects/cognitive_case_diagrams/` — those groups are defined only on the **template root** `pyproject.toml`. From this folder use plain `uv sync` (DisCoPy is a normal dependency here).

## Manuscript `${variable}` injection (author workflow)

Run **from `projects/cognitive_case_diagrams/`** so `tests/` and `src/` paths resolve as documented in [`tests/AGENTS.md`](tests/AGENTS.md):

```bash
cd projects/cognitive_case_diagrams

# 1) Tests + JSON coverage (feeds real ${coverage_*} numbers; coverage.json commit policy — tests/AGENTS.md)
uv run pytest tests/ --cov=src --cov-report=json:coverage.json

# 2) Write output/metrics.json
uv run python -m src.generate_manuscript_metrics

# 3) Render substituted chapters to output/manuscript/ (PDF stage prefers this directory when present)
uv run python scripts/inject_variables.py

# 4) Combined PDF from repository root
cd ../..   # template root
uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams
```

Use `scripts/inject_variables.py --dry-run` to print metrics without writing `output/manuscript/`. See [`manuscript/README.md`](manuscript/README.md) and [`docs/api_reference.md`](docs/api_reference.md).

## Project Structure

```
cognitive_case_diagrams/
├── AGENTS.md                    # Agent operational guide (read first)
├── README.md                    # This file
├── pyproject.toml               # Package config + test/coverage settings
├── docs/                        # Technical reference documentation
├── manuscript/                  # Research manuscript (24 section .md + config.yaml + preamble.md + references.bib)
│   ├── 00_abstract.md           # Abstract
│   ├── 01_introduction.md       # §1 Introduction
│   ├── 01a_research_questions.md       # §1a Research Questions
│   ├── 02_case_systems.md       # §2 Case Systems
│   ├── 02b_case_categories.md   # §2b Case Categories
│   ├── 03_categorial_grammar.md # §3 Categorial Grammar
│   ├── 03b_case_type_logic.md   # §3b Case Type Logic
│   ├── 04_categorical_semantics.md  # §4 DisCoCat
│   ├── 04b_compact_closure_complexity.md # §4b Snake equation & complexity metrics
│   ├── 04c_discourse_complexity.md  # §4c DisCoCirc discourse & QNLP
│   ├── 05_enriched_categories.md    # §5 Enriched Categories
│   ├── 05b_magnitude_homology.md    # §5b Magnitude Homology
│   ├── 06_topos_theory.md           # §6 Topos Theory
│   ├── 07_cognitive_integration.md  # §7 Active Inference
│   ├── 07b_diagrammatic_cognition.md # §7b Diagrammatic Cognition & ERP Predictions
│   ├── 07c_daif_results.md          # §7c DAIF Results
│   ├── 08_quantum_active_inference.md # §8 Quantum
│   ├── 08b_quantum_semantics.md     # §8b Quantum Semantics
│   ├── 09_ai_implications.md        # §9 AI Implications
│   ├── 09b_cognitive_security.md    # §9b Cognitive Security
│   ├── 10_conclusion.md             # §10 Conclusion
│   ├── 11_syntactic_sentence_diagrams.md  # App A: Syntactic diagrams
│   ├── 11b_notation.md             # App B: Complete notation reference (A–K)
│   ├── 11c_automated_test_inventory.md # App C: Test suite inventory
│   ├── config.yaml                  # Paper metadata
│   ├── preamble.md                  # LaTeX package declarations for Pandoc rendering
│   └── references.bib               # Bibliography (BibTeX)
├── output/                      # Generated artifacts
│   ├── figures/                 # Matplotlib publication figures
│   ├── pdf/                     # Compiled PDFs
│   └── reports/                 # Analysis reports
├── scripts/                     # Thin orchestrators
│   ├── 01_generate_manuscript_metrics.py  # Collects test counts, DAIF symbols, coverage → output/metrics.json
│   ├── generate_diagrams.py     # Master dispatcher — generates all 30 manuscript figures
│   ├── generate_category_figures.py       # §2 case category + functor figures (5)
│   ├── generate_category_unpacking_figures.py  # §3–§4c pedagogical unpacking PNGs (3)
│   ├── generate_cognitive_figures.py      # §7 / §7c active inference + DAIF figures (5)
│   ├── generate_discopy_figures.py        # §3–§4c DisCoPy + complexity figures (10)
│   ├── generate_quantum_figures.py        # §8 / §9b quantum POVM + security figures (3)
│   ├── generate_syntactic_figures.py      # App A syntactic case panel (1)
│   └── inject_variables.py      # Manuscript ${variable} injection from output/metrics.json
├── src/                         # Scientific source code
│   ├── case_systems/            # §2: CaseRole, CaseCategory, FluidSFunctor
│   ├── diagrams/                # §3–4b: String diagrams, DisCoCirc
│   ├── enriched_cat/            # §5: EnrichedCategory, magnitude
│   ├── topos_theory/            # §6: GeometricTheory, Morita equivalence
│   ├── cognitive/               # §7: CaseDiagramBelief, free energy
│   ├── daif/                    # §7c: DistributionalReturn, DAIF inference, ERP-linked metrics
│   ├── quantum/                 # §8: CasePOVM, case_probability
│   ├── security/                # §9b: TypeViolation, CaseFrameValidator
│   └── visualization/           # Publication-quality figures (15 plot modules + __init__)
└── tests/                       # Full suite — counts via pytest --collect-only
```

## Test & Coverage Status

Latest snapshot (authoritative source: [`output/metrics.json`](../../output/cognitive_case_diagrams/metrics.json)):

| Metric | Value | How to verify |
|--------|-------|----------------|
| Total tests | **1,207** across **64** test files | `cd projects/cognitive_case_diagrams && uv run pytest tests/ --collect-only -q` |
| DAIF-specific tests | **224** across **8** files | `uv run pytest tests/test_daif*.py --collect-only -q` |
| Line + branch coverage | **95.96%** (3510/3604 lines, 789/876 branches) | `uv run pytest tests/ --cov=src --cov-report=term-missing` (≥90% enforced in `pyproject.toml`) |
| Figures | **30** PNGs in `output/cognitive_case_diagrams/figures/` | `ls output/cognitive_case_diagrams/figures/*.png \| wc -l` |
| Policy | **Zero mocks** — all real computations | see `tests/AGENTS.md` |

## Key Dependencies

```toml
[dependencies]
numpy = ">=1.24"         # verified against 2.4.4 in metrics.json
matplotlib = ">=3.7"
networkx = ">=3.0"
pyyaml = ">=6.0"
discopy = ">=1.0.0"      # required in this package — DisCoPy diagrams (verified 1.2.2)
```

## Documentation

Each directory has its own `AGENTS.md` (agent guide) and `README.md` (quick reference).  
See [`AGENTS.md`](AGENTS.md) for the full agent operational guide.
