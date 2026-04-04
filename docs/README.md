# docs/ — Technical Reference

Technical reference documentation for the `cognitive_case_diagrams` project.

## Where Do I Start?

| You are a... | Start here |
|--------------|-----------|
| **New developer** | [`quickstart_tutorial.md`](quickstart_tutorial.md) → environment setup, code examples, tests |
| **Researcher** reading the paper | [`theory_implementation_map.md`](theory_implementation_map.md) → equation-to-function mapping |
| **Contributor** adding a module | [`extension_guide.md`](extension_guide.md) → templates, dependency rules, CI checklist |
| **Reviewer** checking correctness | [`api_reference.md`](api_reference.md) → full signatures and mathematical context |
| **Anyone** looking up a term | [`glossary.md`](glossary.md) → ~100 terms across math, linguistics, distributional RL, and code |

## Contents

| Document | Description |
|----------|-------------|
| [AGENTS.md](AGENTS.md) | Agent operational guide, ADRs, and architectural decisions |
| [architecture_overview.md](architecture_overview.md) | Package dependency graph, data flow, design principles |
| [theory_implementation_map.md](theory_implementation_map.md) | Manuscript equation → Python function mapping |
| [api_reference.md](api_reference.md) | Full public API reference for all `src/` modules |
| [glossary.md](glossary.md) | ~100 term glossary: math ↔ linguistics ↔ code ↔ distributional RL |
| [literature_guide.md](literature_guide.md) | Annotated bibliography (5 pillars + extensions + 2024–2026 research) |
| [manuscript_figure_index.md](manuscript_figure_index.md) | Figure inventory and generation commands |
| [extension_guide.md](extension_guide.md) | Adding new modules, figures, and manuscript sections |
| [quickstart_tutorial.md](quickstart_tutorial.md) | Step-by-step setup, examples, and test execution |

## Conceptual Roadmap: Five Pillars

The project synthesizes five research traditions into one categorical framework. Each pillar has a corresponding `src/` package and manuscript section:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    A Cognitive Case for Diagrams                     │
├─────────────┬────────────┬────────────┬───────────┬─────────────────┤
│  Pillar 1   │  Pillar 2  │  Pillar 3  │ Pillar 4  │   Pillar 5      │
│ Case Theory │ Categorial │ DisCoCat + │ Enriched  │ Topos Theory    │
│ Typology    │ Grammar    │ DisCoCirc  │ Categories│ Bridges         │
│ §2          │ §3         │ §4–4c      │ §5        │ §6              │
│ case_systems│ diagrams   │ diagrams   │ enriched  │ topos_theory    │
│             │            │            │ _cat      │                 │
├─────────────┴────────────┴────────────┴───────────┴─────────────────┤
│                        Extensions                                    │
│ §7: Active Inference (cognitive/ + daif/)                            │
│ §8: Quantum Semantics (quantum/)                                     │
│ §9: AI Implications + Cognitive Security (security/)                 │
│ All: Visualization (visualization/)                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Cross-References

| Need | Go to |
|------|-------|
| How does DAIF inference work? | `src/daif/AGENTS.md` |
| How does §5 magnitude work? | `src/enriched_cat/AGENTS.md` |
| Where is the POVM equation implemented? | `src/quantum/AGENTS.md` |
| How to add a new figure? | [`extension_guide.md`](extension_guide.md) |
| Test coverage breakdown? | `tests/AGENTS.md` |
| Full pipeline stages? | Root `AGENTS.md` |
| Package dependency graph? | [`architecture_overview.md`](architecture_overview.md) |
| What does "magnitude" mean? | [`glossary.md`](glossary.md) |
| What papers underpin DAIF? | [`literature_guide.md`](literature_guide.md) |

## Theory → Code Quick Map

| Formula | Module | Function |
|---------|--------|----------|
| `P(c\|ρ) = Tr(E_c ρ)` | `src.quantum.quantum_case` | `case_probability()` |
| `\|C\| = Σ (Z⁻¹)ᵢⱼ` | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` |
| `F = E_q[log q − log p]` | `src.cognitive.free_energy` | `variational_free_energy()` |
| `KL(q ‖ p) = Σ qᵢ log(qᵢ/pᵢ)` | `src.cognitive.free_energy` | `kl_divergence()` |
| `q(s) ∝ p(o\|s) q(s)` | `src.cognitive.belief_updating` | `update_belief()` |
| `Z = R + γ T⊤q` (push-forward) | `src.daif.core` | `push_forward_return()` |
| `ρ_τ^κ(δ)` (quantile Huber) | `src.daif.quantile` | `quantile_td_update()` |
| `W_p(Z_a, Z_b)` (Wasserstein) | `src.daif.quantile` | `wasserstein_return_distance()` |
| `DPE = π · (−log q[role])` | `src.daif.prediction` | `distributional_prediction_error()` |
| `G(π) + β Var[Z]` (EFE+risk) | `src.daif.policy` | `G_policy()` |
| `F_Bethe = Σ KL(b_α‖f_α) − Σ (d_i−1) H(b_i)` | `src.daif.inference` | `bethe_free_energy()` |
| `C(A,C) ≥ C(A,B)·C(B,C)` | `src.enriched_cat.enriched` | `check_composition_inequality()` |
| Morita equivalence | `src.topos_theory.topos` | `check_morita_equivalence()` |

## Source Package Map (Manuscript-Aligned)

| `src/` Package | Manuscript Section | Key Concepts |
|----------------|-------------------|-------------|
| `case_systems/` | §2 | Case roles, functors, natural transformations |
| `diagrams/` | §3–§4c | DisCoCat, DisCoCirc discourse (§4c), pregroups, complexity (§4b) |
| `enriched_cat/` | §5 | [0,1]-enriched categories, magnitude |
| `topos_theory/` | §6 | Geometric theories, classifying toposes, Morita |
| `cognitive/` | §7a | Point-estimate active inference, ERP predictions |
| `daif/` | §7c | Distributional return Z(s), VMP, Bethe FE, ERP profiles |
| `quantum/` | §8 | POVM case assignment, density matrices |
| `security/` | §9b | Adversarial injection, topological robustness |
| `visualization/` | all | Publication figures (150 DPI, 16pt min font) |

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | ≥ 3.11 | Runtime |
| uv | latest | Package management |
| numpy | ≥ 1.24 | Matrix operations |
| matplotlib | ≥ 3.7 | Figure rendering |
| pytest | ≥ 7.0 | Testing |
| discopy | ≥ 1.1 | String diagrams (optional for §3–4 figures) |
| lambeq | ≥ 0.12 | QNLP (optional for §4c experiments) |
