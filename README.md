# Cognitive Case Diagrams

**A Cognitive Case for Diagrams: Category-Theoretic Approaches to Linguistic Case Systems in Total Cognitive Scenario Understanding**

*Daniel Ari Friedman · Active Inference Institute · 2026*

---

## Location

This tree currently lives under **`projects/cognitive_case_diagrams/`**. Run tests and figure generation **from this directory** (commands below).

## Overview

This project formalizes linguistic case systems using category theory, integrating them into the Active Inference framework via the CEREBRUM architecture. The central argument: commutative diagrams are cognitively privileged representations because they simultaneously encode algebraic structure, distributional semantics, and inference processes.

## Five Theoretical Pillars

| § | Pillar | Implementation |
|---|--------|---------------|
| §2 | Linguistic Typology & Case Systems | `src/case_systems/` |
| §3–4 | Categorial Grammar & DisCoCat | `src/diagrams/` |
| §4b | Compact closure, snake, diagram complexity | `src/diagrams/` |
| §4c | DisCoCirc discourse (entity wires) | `src/diagrams/` |
| §5 | [0,1]-Enriched Categories | `src/enriched_cat/` |
| §6 | Topos Theory & Morita Equivalence | `src/topos_theory/` |

**Extensions:** Active Inference §7 (`src/cognitive/`), DAIF §7c (`src/daif/`), Quantum POVM §8 (`src/quantum/`), Cognitive Security §9b (`src/security/`). Manuscript §7b (computational verification) is prose + test counts; implementation for distributional inference lives in `src/daif/`.

## Quick Start

```bash
# Full pipeline from repo root
./run.sh --project cognitive_case_diagrams

# Tests with coverage (from THIS project directory — path is tests/, not projects/.../tests/)
cd projects/cognitive_case_diagrams
uv sync
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# Same tests from monorepo root (CI-style; needs root optional groups including discopy)
cd /path/to/repository-root
uv sync --group rendering --group monitoring --group discopy
uv run pytest projects/cognitive_case_diagrams/tests/

# Generate all manuscript figures (from repo root or this directory)
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Validate markdown (from repository root)
uv run python -m infrastructure.validation.cli markdown projects/cognitive_case_diagrams/manuscript/
```

Do not run `uv sync --group rendering` from `projects/cognitive_case_diagrams/` — those groups are defined only on the **template root** `pyproject.toml`. From this folder use plain `uv sync` (DisCoPy is a normal dependency here).

## Project Structure

```
cognitive_case_diagrams/
├── AGENTS.md                    # Agent operational guide (read first)
├── README.md                    # This file
├── pyproject.toml               # Package config + test/coverage settings
├── docs/                        # Technical reference documentation
├── manuscript/                  # Research manuscript (24 Pandoc Markdown files)
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
│   ├── 07b_computational_verification.md # §7b Computational Verification
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
│   ├── preamble.md                  # Pandoc build config
│   └── references.bib               # Bibliography (BibTeX)
├── output/                      # Generated artifacts
│   ├── figures/                 # Matplotlib publication figures
│   ├── pdf/                     # Compiled PDFs
│   └── reports/                 # Analysis reports
├── scripts/                     # Thin orchestrators
│   └── generate_diagrams.py     # Generates all manuscript figures
├── src/                         # Scientific source code
│   ├── case_systems/            # §2: CaseRole, CaseCategory, FluidSFunctor
│   ├── diagrams/                # §3–4b: String diagrams, DisCoCirc
│   ├── enriched_cat/            # §5: EnrichedCategory, magnitude
│   ├── topos_theory/            # §6: GeometricTheory, Morita equivalence
│   ├── cognitive/               # §7: CaseDiagramBelief, free energy
│   ├── daif/                    # §7c: DistributionalReturn, DAIF inference, ERP-linked metrics
│   ├── quantum/                 # §8: CasePOVM, case_probability
│   ├── security/                # §9b: TypeViolation, CaseFrameValidator
│   └── visualization/           # Publication-quality figures (13 plot modules + __init__)
└── tests/                       # Full suite — counts via pytest --collect-only
```

## Test & Coverage Status

| Metric | How to verify |
|--------|----------------|
| Tests | `cd projects/cognitive_case_diagrams && uv run pytest tests/ --collect-only -q` |
| Coverage | `uv run pytest tests/ --cov=src --cov-report=term-missing` (≥90% on `src/` in `pyproject.toml`) |
| Policy | **Zero mocks** — all real computations |

## Key Dependencies

```toml
[dependencies]
numpy = ">=1.24"
matplotlib = ">=3.7"
networkx = ">=3.0"
pyyaml = ">=6.0"
discopy = ">=1.0.0"   # required in this package — DisCoPy diagrams
```

## Documentation

Each directory has its own `AGENTS.md` (agent guide) and `README.md` (quick reference).  
See [`AGENTS.md`](AGENTS.md) for the full agent operational guide.
