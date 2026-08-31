# docs/ — Technical Reference

Technical reference documentation for the `cognitive_case_diagrams` project.

## Canonical manuscript ↔ `src/` map

Section numbers follow [`docs/manuscript/AGENTS.md`](manuscript/AGENTS.md) (same as [`theory_implementation_map.md`](theory_implementation_map.md)). Each `src/` subpackage aligns to one primary section (lettered files such as §2b, §4c, §7c are subordinate to their parent §).

| `src/` package | Manuscript § (primary) |
|----------------|-------------------------|
| `case_systems` | §2 (and §2b) |
| `diagrams` | §3–§4c |
| `enriched_cat` | §5 (and §5b) |
| `topos_theory` | §6 |
| `cognitive` | §7 (scalar active inference; `07_cognitive_integration.md`) |
| `daif` | §7c (`07c_daif_results.md`) |
| `quantum` | §8 (and §8b) |
| `security` | §9b |
| `visualization` | all (figures) |

**Note:** Older docs sometimes used informal labels such as “§7a” for scalar cognitive; that content is the same manuscript **§7** as in the inventory table.

## Where Do I Start?

| You are a... | Start here |
|--------------|-----------|
| **New developer** | [`quickstart_tutorial.md`](quickstart_tutorial.md) → environment setup, code examples, tests |
| **Researcher** reading the paper | [`theory_implementation_map.md`](theory_implementation_map.md) → equation-to-function mapping |
| **Contributor** adding a module | [`extension_guide.md`](extension_guide.md) → templates, dependency rules, CI checklist |
| **Reviewer** checking correctness | [`api_reference.md`](api_reference.md) → full signatures and mathematical context |
| **Anyone** looking up a term | [`glossary.md`](glossary.md) → 117 term rows across math, linguistics, distributional RL, and code |

## Contents

| Document | Description |
|----------|-------------|
| [AGENTS.md](AGENTS.md) | Agent operational guide, ADRs, and architectural decisions |
| [architecture_overview.md](architecture_overview.md) | Package dependency graph, data flow, design principles |
| [theory_implementation_map.md](theory_implementation_map.md) | Manuscript equation → Python function mapping |
| [api_reference.md](api_reference.md) | Full public API reference for all `src/` modules |
| [glossary.md](glossary.md) | 117 term rows: math ↔ linguistics ↔ code ↔ distributional RL |
| [literature_guide.md](literature_guide.md) | Annotated bibliography (five pillars + extensions + sixth-strand synthesis via §7–§7b) |
| [manuscript_figure_index.md](manuscript_figure_index.md) | Figure inventory and generation commands |
| [extension_guide.md](extension_guide.md) | Adding new modules, figures, and manuscript sections |
| [quickstart_tutorial.md](quickstart_tutorial.md) | Step-by-step setup, examples, and test execution |
| [modules/](modules/README.md) | **Per-module technical reference** — one doc per `src/` subpackage |

### Per-Module Documentation (`modules/`)

| Module | §  | Document |
|--------|----|----------|
| `case_systems` | §2 | [case_systems.md](modules/case_systems.md) |
| `diagrams` | §3–4c | [diagrams.md](modules/diagrams.md) |
| `enriched_cat` | §5 | [enriched_cat.md](modules/enriched_cat.md) |
| `topos_theory` | §6 | [topos_theory.md](modules/topos_theory.md) |
| `cognitive` | §7 | [cognitive.md](modules/cognitive.md) |
| `daif` | §7c | [daif.md](modules/daif.md) |
| `quantum` | §8 | [quantum.md](modules/quantum.md) |
| `security` | §9b | [security.md](modules/security.md) |
| `visualization` | All | [visualization.md](modules/visualization.md) |


## Conceptual roadmap: five formal layers, sixth strand, extensions

The manuscript stacks **five formal traditions** (§2–§6), each with a matching `src/` package. A **sixth strand**—ROSE / biolinguistic–neuro interface—runs through **§7–§7b** (and DAIF in §7c), connecting the formal stack to cognitive and neural evidence. **Extensions** (quantum §8; AI and **protocol-level** cognitive security §9–§9b) apply the same mathematics without treating security as a separate “pillar” competing with §9b’s conditional, engineering framing.

```
┌──────────────────────────────────────────────────────────────────────┐
│   Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case │
├─────────────┬────────────┬────────────┬───────────┬────────────────────┤
│  Layer 1    │  Layer 2   │  Layer 3   │ Layer 4   │   Layer 5          │
│ Case &      │ Categorial │ DisCoCat + │ Enriched  │ Topos (geometric   │
│ typology    │ grammar    │ DisCoCirc  │ categories│ theories, bridges) │
│ §2          │ §3         │ §4–§4c     │ §5        │ §6                 │
│ case_systems│ diagrams   │ diagrams   │ enriched  │ topos_theory       │
│             │            │            │ _cat      │                    │
├─────────────┴────────────┴────────────┴───────────┴────────────────────┤
│ Sixth strand: ROSE / neuro interface — §7, §7b, §7c (`cognitive/`, `daif/`) │
├──────────────────────────────────────────────────────────────────────┤
│ Extensions: §8 quantum; §9–§9b AI + cognitive security (`security/`); │
│ figures via `visualization/` across sections                          │
└──────────────────────────────────────────────────────────────────────┘
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
| `DPE = w_f · (−log q[role])` | `src.daif.prediction` | `distributional_prediction_error()` |
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
| `cognitive/` | §7 | Point-estimate active inference, ERP predictions |
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

## Why this layered structure?

No single formalism captures the full expressivity of linguistic case systems. The **five formal layers** contribute distinct lenses:

1. **Case theory (§2)** grounds the work in typological data — attested alignment patterns (accusative, ergative, tripartite, split-S). Without this, the mathematics would lack empirical purchase.

2. **Categorial grammar (§3)** bridges syntax and semantics through the Curry–Howard–Lambek correspondence. Pregroup types serve as linear logic propositions whose proofs are the grammatical derivations themselves. The key insight: *cup-counting measures syntactic complexity*.

3. **DisCoCat + DisCoCirc (§4–§4c)** lifts the grammar into compositional distributional semantics. The meaning functor $\hat{F}: \mathbf{Gram} \to \mathbf{FVect}$ maps syntactic derivations to linear maps over meaning spaces. DisCoCirc extends this to discourse-level circuits where entity wires persist across sentence boundaries.

4. **Enriched categories (§5)** replace Boolean hom-sets with $[0,1]$-valued proximity measures, enabling *graded* judgments of case similarity. Categorical magnitude $|\mathcal{C}| = \sum_{ij}(Z^{-1})_{ij}$ measures the “effective number” of distinct case roles — a quantity that can track reanalysis costs.

5. **Topos theory (§6)** supplies the meta-theoretic bridge: different linguistic theories are geometric theories whose classifying toposes can be compared via Morita equivalence, enabling inter-theoretic translation without loss of structural information.

**Sixth strand.** **§7–§7b** synthesize the formal stack with **ROSE** and the **biolinguistic–neuro interface** (computational verification, cognitive integration). **§7c (DAIF)** shows distributional return representations over case-role beliefs linking to interpretable ERP predictions (N400, P600)—a falsifiable neurolinguistic test.

**Extensions.** **§8** (quantum semantics) and **§9–§9b** (AI implications and **protocol-level** cognitive security) show the structures are computational; §9b analyzes prompt injection under fixed interaction protocols, not as an automatic guarantee on today’s APIs.

## Verified Metrics

Canonical counts, verified as of 2026-04-22 (v2.3 release):

| Metric | Count | Source of Truth |
|--------|-------|-----------------|
| Manuscript sections | 24 `.md` section files | `docs/manuscript/config.yaml` chapter list |
| Publication figures | **30** PNGs | `output/cognitive_case_diagrams/figures/` + `docs/manuscript_figure_index.md`; authoritative live count in `output/metrics.json::total_figures` |
| BibTeX entries | **106** keys | `docs/manuscript/references.bib` (live count: `grep -c '^@' docs/manuscript/references.bib`) |
| Total tests | **1,207** | `output/metrics.json::total_test_count` |
| Test files | **64** | `tests/test_*.py` (authoritative live count in `output/metrics.json::total_test_files`) |
| `src/` subpackages | **9** | `case_systems`, `cognitive`, `daif`, `diagrams`, `enriched_cat`, `quantum`, `security`, `topos_theory`, `visualization` |
| DAIF modules | **7** | `src/daif/` directory (non-`__init__.py`) |
| DAIF public symbols | **25** | `src/daif/__init__.py` `__all__` (see `generate_manuscript_metrics.py` for `${daif_symbols}`) |
| DAIF tests | **224** across **8** files | `tests/test_daif*.py` (`output/metrics.json::daif_tests`) |
| Cognitive modules | **7** | `src/cognitive/` (`action_selection`, `belief`, `belief_updating`, `figure_data`, `free_energy`, `prediction_error`, `reanalysis`) |
| Quantum modules | **2** | `src/quantum/` (`quantum_case`, `figure_data`) |
| Visualization modules | **15** (+ `__init__.py`) | `src/visualization/` non-`__init__` module listing |
| `src/` line + branch coverage | **95.96%** (3510/3604 lines, 789/876 branches) | `output/metrics.json::coverage_percent` |
| Glossary terms | 117 (table rows) | `docs/glossary.md` |
| ADR count | 12 | `docs/AGENTS.md` (ADR-001 through ADR-012) |
| `\autoref{}` cross-references | 104 | `docs/manuscript/*.md` grep |
| Notation appendix sections | 11 (A–K) | `docs/manuscript/11b_notation.md` |
| Installed DisCoPy / NumPy | **1.2.2 / 2.4.4** | `output/metrics.json::discopy_version`, `numpy_version` |

## Design Philosophy

This project follows several non-obvious architectural principles:

- **Zero-Mock Testing (ADR-002)**: All tests use real mathematical computations. A test of `magnitude()` inverts an actual proximity matrix; it does not mock `numpy.linalg.inv`. This ensures that test failures reflect genuine mathematical errors, not implementation-mocking mismatches.

- **Manuscript-Aligned Factoring (ADR-001)**: The `src/` package structure mirrors the manuscript section numbering exactly. This is not organizational convenience — it encodes the theoretical dependency graph. `case_systems` has no internal dependencies because case roles are the foundational objects; `daif` depends on `cognitive` and `enriched_cat` because distributional active inference requires both belief updating and enriched proximity measures.

- **Documentation Duality (ADR-011)**: Every directory carries both `AGENTS.md` (machine-readable operational guide for AI agents) and `README.md` (human-readable quick reference). The `SKILL.md` files additionally provide MCP-aligned capability descriptors. This triple redundancy is intentional — each format serves a different reader (AI agent, human developer scanning, AI tool invoker).

- **Show, Not Tell**: The manuscript derives all claims from computations performed by the `src/` code. Every figure is generated from real mathematical operations. The `generate_manuscript_metrics.py` script introspects the test suite and DAIF module inventory to inject verified counts as `${variable}` placeholders at build time, ensuring the manuscript can never cite a stale number.

*Last updated: 2026-04-22.*
