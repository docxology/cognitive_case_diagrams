# Theory → Implementation Map

Complete mapping from manuscript equations to Python functions in `src/`.

> For function signatures, see [`api_reference.md`](api_reference.md).  
> For term definitions, see [`glossary.md`](glossary.md).  
> **Status key**: ✅ implemented and tested | 🔄 partial | 📋 planned

---

## §2 Case Systems (Functors & Natural Transformations)

The foundation of the framework: linguistic case systems formalized as categories, with alignment typologies as functors. This layer has **no dependencies** on other `src/` packages.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Case roles as objects | `src.case_systems.case_category` | `CaseRole` enum | ✅ | NOM, ACC, DAT, GEN, INS, ABL, ERG, ABS, VOC, S, A, P |
| Morphisms between roles | `src.case_systems.case_category` | `Morphism` | ✅ | `source`, `target`, `label`, `weight` |
| Case category $\mathcal{L}$ | `src.case_systems.case_category` | `CaseCategory` | ✅ | `objects`, `morphisms`, `compose()` |
| Accusative functor $F_{\text{acc}}$ | `src.case_systems.functor` | `AlignmentFunctor` | ✅ | `object_map`, `map_object`, `map_morphism`; `preserves_composition` compares weights |
| Naturality square $G(f)\circ\alpha_A = \alpha_B\circ F(f)$ | `src.case_systems.natural_transformation` | `NaturalTransformation.naturality_holds()` (alias `verify_naturality`) | ✅ | Quantifies over `source_functor.source.morphisms` whose endpoints lie in `object_map`; requires `is_complete()` |
| Fluid-S alignment | `src.case_systems.fluid_s` | `FluidSFunctor` | ✅ | `map_object`, `split_probability`, `map_morphism`, `kernel()`, `create_fluid_s_functor()` |
| Eq. `eq-2-1`: $w(g \circ f)=w(g)\cdot w(f)$ | `src.case_systems.case_category` | `CaseCategory.compose()` | ✅ | weight multiplication in `compose()` |

---

## §3 Categorial Grammar

Pregroup grammar and the Lambek calculus, realized as DisCoPy type reductions. This layer imports `case_systems` for case role types.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Pregroup types | `src.diagrams.string_diagram` | `Sentence` | ✅ | wraps DisCoPy `Ty` |
| Type reduction / cups | `src.diagrams.string_diagram` | DisCoPy `Cup` | ✅ | DisCoPy enforces Lambek residuation |
| Lambek residuation | (structural — DisCoPy enforces) | — | ✅ | — |
| Native DisCoCat string diagram (fig:native-discocat) | `src.visualization.string_diagrams` | `render_discocat_sentence()` | ✅ | Matplotlib render, cross-validates DisCoPy output |

---

## §4 Categorical Semantics (DisCoCat)

The meaning functor from grammar to vector spaces. DisCoCat is argued to be the **algebraic formalization of what transformer attention mechanisms learn**.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$ | `src.diagrams.string_diagram` | `Sentence.to_diagram()` | ✅ | DisCoPy applies the functor |
| Sentence meaning composition (eq. `eq-4-2`) | `src.visualization.discopy_diagrams` | `render_discopy_transitive()` | ✅ | Produces string diagram PNG |

---

## §4b Compact closure and complexity

Snake equation, normal form, and diagram complexity metrics (`04b_compact_closure_complexity.md`).

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Snake equation (eq. `eq-4-3`) | `src.visualization.discopy_diagrams` | `render_discopy_snake()` | ✅ | Verifies `normal_form() == Id(Ty('x'))` |
| Complexity score (eq. `eq-4-4`) | `src.diagrams.complexity_metrics` | `syntactic_complexity_score()` | ✅ | Configurable weights $w_b, w_c, w_d$ |
| Diagram comparison | `src.diagrams.complexity_metrics` | `compare_diagrams()` | ✅ | Returns per-diagram metric dict |

---

## §4c DisCoCirc discourse

The discourse-level extension: nouns become **persistent entity wires** that carry state across sentence boundaries. Dynamic case role reversal is a key insight.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Multi-sentence discourse circuit | `src.visualization.discopy_diagrams` | `render_discopy_discocirc_discourse()` | ✅ | Two-sentence discourse circuit |
| Entity wire persistence | `src.visualization.discopy_diagrams` | `render_discopy_three_sentence_discourse()` | ✅ | Entity state updated per sentence |
| Native DisCoCirc string diagram (fig:native-discourse) | `src.visualization.string_diagrams` | `render_discocirc_discourse()` | ✅ | Matplotlib render, cross-validates DisCoPy discourse output |
| Discourse data structure | `src.diagrams.string_diagram` | `Discourse` | ✅ | Entity wires across `Sentence` list |

---

## §5 Enriched Categories

The transition from discrete to continuous: case categories enriched over $[0,1]$, where hom-values represent distributional proximity. This provides the mathematical grounding for connecting symbolic grammar to statistical semantics.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Hom-value $\mathcal{C}(A,B)\in[0,1]$ | `src.enriched_cat.enriched` | `EnrichedCategory.hom_value()` | ✅ | Reads `proximity_matrix` |
| Identity axiom $\mathcal{C}(A,A)=1$ | `src.enriched_cat.enriched` | `EnrichedCategory.check_identity_axiom()` | ✅ | Asserts diagonal = 1 |
| Composition inequality (eq. `eq-5-2`) | `src.enriched_cat.enriched` | `EnrichedCategory.check_composition_inequality()` | ✅ | Returns bool |
| Magnitude $|\mathcal{C}| = \sum_{ij}(Z^{-1})_{ij}$ (eq. `eq-5-3`) | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` | ✅ | Via `np.linalg.inv` |
| Similarity matrix $Z$ (eq. `eq-5-4`) | `src.enriched_cat.enriched` | `EnrichedCategory.proximity_matrix` | ✅ | NumPy ndarray |

## §5b Magnitude Homology

Magnitude as a **complexity invariant** for case systems, and its connection to transformer attention via information geometry.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Effective size = magnitude | `src.enriched_cat.enriched` | `EnrichedCategory.effective_size()` | ✅ | Alias for `magnitude()` |
| Role clusters by proximity | `src.enriched_cat.enriched` | `EnrichedCategory.role_clusters()` | ✅ | Threshold-based grouping |
| Magnitude < n indicates redundancy | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` | ✅ | $\|\mathcal{C}\| < n$ means roles overlap |
| Enriched hom-proximity heatmap | `src.visualization.enriched_diagrams` | `render_enriched_heatmap()` | ✅ | Fig. 15 in manuscript |

---

## §6 Topos Theory

Caramello's bridge technique: when two case-theoretic formalizations have Morita-equivalent classifying toposes, theorems transfer automatically between them.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Geometric theory | `src.topos_theory.topos` | `GeometricTheory` | ✅ | `name`, `axioms`, `sorts` |
| Classifying topos | `src.topos_theory.topos` | `ClassifyingTopos` | ✅ | `theory`, `invariants` |
| Morita equivalence (eq. `eq-6-1`) | `src.topos_theory.topos` | `check_morita_equivalence()` | ✅ | Checks shared interpretations |
| Bridge transfer | `src.topos_theory.topos` | `bridge_transfer()` | ✅ | Data transfer between equivalent theories |

---

## §7a Cognitive Integration (Active Inference)

Active inference as a process theory: agents maintain beliefs over case role assignments and minimize variational free energy through Bayesian updating. This layer uses **point-estimate** (scalar) methods.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Case diagram belief $q(s)$ | `src.cognitive.belief` | `CaseDiagramBelief` | ✅ | Probability distribution over case roles |
| KL divergence $\text{KL}(q \| p)$ | `src.cognitive.free_energy` | `kl_divergence()` | ✅ | Core free energy decomposition |
| Variational free energy $F = \mathbb{E}_q[\log q - \log p]$ | `src.cognitive.free_energy` | `variational_free_energy()` | ✅ | Minimized by perceptual inference |
| Bayesian belief update $q(s) \propto p(o|s) q(s)$ | `src.cognitive.belief_updating` | `update_belief()` | ✅ | Single-step posterior |
| Five-step generative loop (§7) | `src.cognitive.belief_updating` | `sequential_belief_update()` | ✅ | Multi-word processing |
| Precision-weighted PE: $\text{PE} = \pi_f \cdot |\mu_{pred} - \mu_{obs}|$ | `src.cognitive.prediction_error` | `prediction_error()` | ✅ | P600 ERP prediction |
| P600 amplitude ratio $\pi_{strong}/\pi_{weak}$ | `src.cognitive.prediction_error` | `p600_amplitude_ratio()` | ✅ | Predicts ERP ratio |
| Expected free energy $G(\pi)$ (point-estimate) | `src.cognitive.action_selection` | `expected_free_energy()` | ✅ | Action/word selection |
| Garden-path reanalysis $\Delta|\mathcal{C}|$ | `src.cognitive.reanalysis` | `magnitude_reanalysis_cost()` | ✅ | P600 late positivity |
| N400 semantic violation proxy | `src.cognitive.reanalysis` | `n400_amplitude_proxy()` | ✅ | N400 early negativity |

---

## §7c Distributional Active Inference (DAIF)

The distributional extension: agents maintain the parameterised cumulative density function (CDF) of case diagrams via fixed-length quantile vectors. Inference resolves locally over factor graphs rather than assuming mean-field factorization.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Return distribution $Z(s) = \mathbb{E}[\sum \gamma^t R_t]$ | `src.daif.types` | `DistributionalReturn` | ✅ | `quantiles` array $\in \mathbb{R}^N$, mapped monotonically to $N$ uniform CDF intervals |
| DAIF inference result | `src.daif.types` | `DAIFResult` | ✅ | Exposes explicit `fe_trajectory` for diagnosing factor graph convergence |
| ERP waveform profile | `src.daif.types` | `ERPProfile` | ✅ | Struct binding peak $\mu$ times to voltage deflections |
| Push-forward return (Eq. 7-1) $Z = R + \gamma T^\top q$ | `src.daif.core` | `push_forward_return()` | ✅ | Fixed-point step returning $L^1$ optimal $\tau$-quantiles via 1D sort |
| Multi-step Bellman iteration $T^n Z_0$ | `src.daif.core` | `distributional_bellman_operator()` | ✅ | Contraction mapping enforcing contractive bound $\gamma < 1$ |
| C51 categorical projection $\Phi Z$ | `src.daif.core` | `categorical_return_distribution()` | ✅ | Linearly interpolates quantiles onto $N$ fixed voltage supports |
| Quantile Huber loss $\rho^\kappa_\tau$ (Eq. 7-2) | `src.daif.quantile` | `quantile_td_update()` | ✅ | Differentiable transition bridging absolute and $L^2$ distances via threshold $\kappa$ |
| IQN risk-distorted update | `src.daif.quantile` | `implicit_quantile_network_update()` | ✅ | Applies non-linear functions to index $\tau$: neutral / optimistic / pessimistic / CVaR |
| Wasserstein distance $W_p(Z_a, Z_b)$ | `src.daif.quantile` | `wasserstein_return_distance()` | ✅ | Inverse-CDF map: $(\int_0^1 \|F^{-1}(\tau) - G^{-1}(\tau)\|^p d\tau)^{1/p}$ |
| Distributional DAIF posterior | `src.daif.inference` | `distributional_case_assignment()` | ✅ | Evaluates conjugate belief against threshold $\epsilon=10^{-6}$ |
| Precision-weighted VMP | `src.daif.inference` | `variational_message_passing()` | ✅ | Sum-product with sequential damping to arrest cycle oscillations |
| Bethe free energy (Eq. 7-3) $F_{\text{Bethe}}$ | `src.daif.inference` | `bethe_free_energy()` | ✅ | Subtracts intersection entropy terms for loopy geometries |
| Expected information gain EIG$(o^*)$ | `src.daif.inference` | `expected_information_gain()` | ✅ | Computes discrete KL divergence iteratively conditioned on $o^*$ |
| DPE $= \pi \cdot (-\log q[\text{role}])$ | `src.daif.prediction` | `distributional_prediction_error()` | ✅ | Weights entropy by precision scalar $\pi \in \mathbb{R}^+$ |
| N400 from return distribution | `src.daif.prediction` | `n400_from_return_distribution()` | ✅ | Evaluates linear discrepancy from established prior expectation |
| P600 from precision update $\Delta\Lambda \cdot \text{DPE}$ | `src.daif.prediction` | `p600_from_precision_update()` | ✅ | Binds parameter reassignment cost to voltage amplitude |
| Full ERP waveform (Eq. 7-4) | `src.daif.prediction` | `erp_amplitude_profile()` | ✅ | Gaussian superposition of generated components |
| EFE with risk $G(\pi) + \beta \text{Var}[Z]$ | `src.daif.policy` | `G_policy()` | ✅ | Augments EFE with explicit variance penalty $\beta$ |
| Boltzmann policy $P(\pi) \propto e^{-G/T}$ | `src.daif.policy` | `softmax_policy_selection()` | ✅ | Controls policy entropy via thermal parameter $T$ |
| Distributional epistemic value | `src.daif.policy` | `distributional_epistemic_value()` | ✅ | Computed from bounding variance distributions |
| FE convergence diagnostics | `src.daif.metrics` | `convergence_diagnostics()` | ✅ | Validates structural descent $d(\text{FE})/dt \leq 0$ |
| KL between return distributions | `src.daif.metrics` | `distributional_kl()` | ✅ | Resolves using uniform binning for continuous intervals |
| Quantile calibration | `src.daif.metrics` | `quantile_coverage()` | ✅ | Test protocol asserting mass conservation across $\tau$ partitions |
| Return entropy $H[Z]$ | `src.daif.metrics` | `return_distribution_entropy()` | ✅ | Limits $Z$ to atomic discretization sequence before calculation |
| Li-Futrell surprisal (shallow → N400) | `src.daif.prediction` | `n400_from_return_distribution()` | ✅ | Converts lexical surprisal bound directly into voltage offset |
| Li-Futrell surprisal (deep → P600) | `src.daif.prediction` | `p600_from_precision_update()` | ✅ | Isolates syntactic restructuring cost |
| DAIF belief trajectory (Fig. 17b) | `src.visualization.daif_plots` | `plot_belief_trajectory()` | ✅ | Renders temporal evolution as confidence funnel |
| DAIF free energy convergence (Fig. 17c) | `src.visualization.daif_plots` | `plot_free_energy_convergence()` | ✅ | Verifies discrete limits algorithmically |
| DAIF ERP predictions (Fig. 17d) | `src.visualization.daif_plots` | `plot_erp_predictions()` | ✅ | Overlays theoretical outputs against physiological noise limits |

---

## §8 Quantum Active Inference

DisCoCat string diagrams compiled into ZX-calculus quantum circuits. Case assignment modeled as POVM measurement on quantum states.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| POVM element $E_c$ | `src.quantum.quantum_case` | `CasePOVM.elements` | ✅ | Complex hermitian matrices mapping roles linearly |
| Case probability $P(c\|\rho) = \text{Tr}(E_c\rho)$ (eq. `eq-8-1`) | `src.quantum.quantum_case` | `case_probability()` | ✅ | Evaluated algebraically via `np.trace(E_c @ rho).real` over field $\mathbb{C}$ |
| Crisp projective measurement | `src.quantum.quantum_case` | `crisp_case_povm()` | ✅ | Defines strict rank-1 orthogonal basis frames |
| Graded POVM | `src.quantum.quantum_case` | `graded_case_povm()` | ✅ | Configurable non-orthogonal frames spanning identity |
| Semantic state density matrix $\rho$ | `src.quantum.quantum_case` | `semantic_state()` | ✅ | Bounded trace-1 positive semi-definite construction |

---

## §9b Cognitive Security

Adversarial injections interpreted formally as algebraic type violations rather than sentiment anomalies. Operations detect unverified state promotions directly on the underlying case graph.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Type-violation detection | `src.security.cognitive_security` | `detect_type_violation()` | ✅ | Validates invariant mapping $\phi : \text{ACC} \to \text{NOM}$ |
| Injection scoring | `src.security.cognitive_security` | `injection_score()` | ✅ | Integrates total mass of unmapped morphisms |
| Case frame validation | `src.security.cognitive_security` | `CaseFrameValidator` | ✅ | Intersects empirical graph with permitted grammar limits |
| Topological robustness | `src.security.cognitive_security` | `topological_robustness()` | ✅ | Expresses security state as subset magnitude $\|\mathcal{C}\|_\text{secure}$ |
| Semantic integrity | `src.security.cognitive_security` | `semantic_integrity_check()` | ✅ | Asserts identity constraints on $Z$ trace matrices |

---

## Appendix: Notation → Code Symbol Mapping

Selected entries from `11b_notation.md` (App B) mapped to Python identifiers:

| Notation (Manuscript) | Python Identifier | Package |
|----------------------|-------------------|---------|
| $\mathcal{C}$ | `CaseCategory` | `case_systems` |
| $\text{Ob}(\mathcal{C})$ | `CaseCategory.objects` | `case_systems` |
| $\text{Hom}(A, B)$ | `EnrichedCategory.hom_value(A, B)` | `enriched_cat` |
| $F: \mathcal{C} \to \mathcal{D}$ | `AlignmentFunctor` | `case_systems` |
| $\alpha: F \Rightarrow G$ | `NaturalTransformation` | `case_systems` |
| $\|\mathcal{C}\|$ | `EnrichedCategory.magnitude()` | `enriched_cat` |
| $Z$ (similarity matrix) | `EnrichedCategory.proximity_matrix` | `enriched_cat` |
| $q(s)$ | `CaseDiagramBelief.probabilities` | `cognitive` |
| $F$ (free energy) | `variational_free_energy()` | `cognitive` |
| $G(\pi)$ | `G_policy()` | `daif` |
| $Z(s)$ (return dist.) | `DistributionalReturn` | `daif` |
| $E_c$ (POVM) | `CasePOVM.elements[role]` | `quantum` |
| $\rho$ (density matrix) | `semantic_state()` return value | `quantum` |

---

*Last updated: 2026-03-19 — Added §5b magnitude homology mapping, conceptual narrative paragraphs for each section, implementation status badges, and Appendix notation → code symbol mapping. DAIF promoted to `src.daif/` subpackage (7 modules, 25 symbols); §7 split into §7a (cognitive) + §7c (DAIF).*
