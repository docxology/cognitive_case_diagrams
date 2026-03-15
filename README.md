# Cognitive Case Diagrams

**A Cognitive Case for Diagrams: Category-Theoretic Approaches to Linguistic Case Systems in Total Cognitive Scenario Understanding**

## Overview

This project formalizes linguistic case systems using category theory, integrating them into the Active Inference framework via the CEREBRUM architecture. It argues that commutative diagrams are cognitively privileged representations for case assignment.

## Five Converging Pillars

1. **Linguistic Typology** — Case roles as categorical objects, alignment as functors
2. **Categorial Grammar** — Lambek calculus, pregroup types, string diagrams
3. **DisCoCat** — Compact closed categories for compositional distributional semantics
4. **Enriched Categories** — [0,1]-enrichment for distributional proximity
5. **Topos Theory** — Morita equivalence for inter-theoretic transfer

## Project Structure

```
cognitive_case_diagrams/
├── src/                          # Source modules
│   ├── case_category.py          # Core case category (roles, morphisms, alignment)
│   ├── enriched.py               # [0,1]-enriched categories & magnitude
│   ├── functor.py                # Alignment functors
│   ├── string_diagram.py         # DisCoCat/DisCoCirc + real DisCoPy integration
│   └── visualization/            # Publication-quality figure generation
│       ├── styles.py             # Color palette & typography
│       ├── category_diagrams.py  # Case category graphs
│       ├── enriched_diagrams.py  # Hom-value heatmaps
│       ├── functor_diagrams.py   # Functor mapping diagrams
│       ├── string_diagrams.py    # Native string diagrams
│       └── discopy_diagrams.py   # Real DisCoPy rendering
├── tests/                        # 104+ tests (zero-mock)
├── scripts/                      # Thin orchestrator
│   └── generate_diagrams.py      # Generates 18 canonical figures
├── manuscript/                   # Research manuscript (12 chapters)
└── output/figures/               # Generated figures
```

## Quick Start

```bash
# Run tests
python -m pytest projects/cognitive_case_diagrams/tests/ -v

# Generate figures
python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Run pipeline
./run.sh --project cognitive_case_diagrams
```

## Dependencies

- `numpy`, `matplotlib`, `networkx`, `pyyaml` (core)
- `discopy>=1.0.0` (optional, for DisCoPy-based categorical diagrams)
