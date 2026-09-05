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
| Monoidal functor $F_{\otimes}$ (tensor checks; §9b protocol story) | `src.case_systems.functor` | `MonoidalFunctor` | ✅ | `preserves_tensor()` checks tensor preservation for role pairs; aligns with non-cartesian **specification** for interaction diagrams (§9b), not a production LLM guarantee |
| Naturality square $G(f)\circ\alpha_A = \alpha_B\circ F(f)$ | `src.case_systems.natural_transformation` | `NaturalTransformation.naturality_holds()` (alias `verify_naturality`) | ✅ | Quantifies over `source_functor.source.morphisms` whose endpoints lie in `object_map`; requires `is_complete()` |
| Fluid-S alignment | `src.case_systems.fluid_s` | `FluidSFunctor` | ✅ | `map_object`, `split_probability`, `map_morphism`, `kernel()`, `create_fluid_s_functor()` |
| Eq. `eq-2-1`: $w(g \circ f)=w(g)\cdot w(f)$ | `src.case_systems.case_category` | `CaseCategory.compose()` | ✅ | weight multiplication in `compose()` |
| DAIF surprisal (N400/P600) on morphism | `src.case_systems.case_category` | `CaseCategory.assess_daif_surprisal()` | ✅ | Returns `{"N400_amplitude", "P600_amplitude"}` per Li & Futrell (2024); shallow = semantic surprise, deep = structural discrepancy (§7c) |
| Prompt injection detect (ACC→NOM) | `src.security.cognitive_security` | `CaseFrameValidator.validate_assignment()` | ✅ | Decidable graph check on `Mor(C_protocol)` (§9b); replaces legacy `CaseCategory.detect_prompt_injection()` |

---

## §3 Categorial Grammar

Pregroup grammar and the Lambek calculus, realized as DisCoPy type reductions. This layer imports `case_systems` for case role types.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Pregroup types | `src.diagrams.string_diagram` | `Sentence` + DisCoPy `Ty` | ✅ | Native + DisCoPy dual representations |
| Type reduction / cups | `src.diagrams.string_diagram` | DisCoPy `Cup` | ✅ | DisCoPy enforces Lambek residuation |
| Lambek residuation | (structural — DisCoPy enforces) | — | ✅ | — |
| Lexical entries (Word) | `src.diagrams.string_diagram` | `create_word_diagram_transitive()` | ✅ | `grammar.pregroup.Word` + `eager_parse` |
| Automatic cup placement | `src.diagrams.string_diagram` | `eager_parse()` via `create_word_diagram_*()` | ✅ | DisCoPy determines optimal Cup sequence |
| Passivization / Swap | `src.diagrams.string_diagram` | `create_swap_passive()` | ✅ | `grammar.pregroup.Swap` for type permutation |
| Passivization type reduction — active (eq-3-3) | `src.diagrams.string_diagram` | `create_discopy_passive()` | ✅ | Active-voice verb type $n^r \otimes s \otimes n^l$; permutes noun wires via DisCoPy `Swap`; renders as `discopy_passive.png` |
| Passivization type reduction — patient-promoted (eq-3-4) | `src.diagrams.string_diagram` | `create_discopy_passive()` | ✅ | Surface chain $n_{\text{NOM}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{OBL}} \to s$ with promoted patient as NOM and oblique agent; `Swap` + cup wiring; same renderer as active, different case labels (`discopy_passive.png`) |
| Native DisCoCat string diagram (fig:native-discocat) | `src.visualization.string_diagrams` | `render_discocat_sentence()` | ✅ | Matplotlib render, cross-validates DisCoPy output |

---

## §4 Categorical Semantics (DisCoCat)

The meaning functor from grammar to vector spaces. DisCoCat is argued to be the **algebraic formalization of what transformer attention mechanisms learn**.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$ | `src.diagrams.string_diagram` | `create_tensor_semantics()` | ✅ | `discopy.tensor` — evaluates to numpy meaning vectors |
| Sentence meaning composition (eq. `eq-4-2`) | `src.visualization.discopy_diagrams` | `render_discopy_transitive()` | ✅ | Produces string diagram PNG |

---

## §4b Compact closure and complexity

Snake equation, normal form, and diagram complexity metrics (`04b_compact_closure_complexity.md`).

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Snake equation (eq. `eq-4-3`) | `src.visualization.discopy_diagrams` | `render_discopy_snake()` | ✅ | Verifies `normal_form() == Id(Ty('x'))` |
| Complexity score (eq. `eq-4-4`) | `src.diagrams.complexity_metrics` | `syntactic_complexity_score()` | ✅ | words + 0.5·cups + 0.25·caps + 0.1·depth |
| Circuit depth (eq. `eq-4-4`) | `src.diagrams.complexity_metrics` | `diagram_depth()` | ✅ | `diagram.depth()` — sequential layer count |
| Circuit width | `src.diagrams.complexity_metrics` | `diagram_width()` | ✅ | `diagram.width` — max parallel wires |
| Diagram comparison | `src.diagrams.complexity_metrics` | `compare_diagrams()` | ✅ | Returns per-diagram `DiagramMetrics` list |

---

## §4c DisCoCirc discourse

The discourse-level extension: nouns become **persistent entity wires** that carry state across sentence boundaries. Dynamic case role reversal is a key insight.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Multi-sentence discourse circuit | `src.visualization.discopy_diagrams` | `render_discopy_discocirc_discourse()` | ✅ | Two-sentence discourse circuit |
| Entity wire persistence | `src.visualization.discopy_diagrams` | `render_discopy_three_sentence_discourse()` | ✅ | Entity state updated per sentence |
| Native DisCoCirc string diagram (fig:native-discourse) | `src.visualization.string_diagrams` | `render_discocirc_discourse()` | ✅ | Matplotlib render, cross-validates DisCoPy discourse output |
| Discourse data structure | `src.diagrams.string_diagram` | `Discourse` | ✅ | Entity wires across `Sentence` list |
| Prompt injection scan (discourse-level) | `src.security.cognitive_security` | `CaseFrameValidator.validate_assignment()` | ✅ | Feed per-entity role assignments from `Discourse.role_history`; flags ACC→NOM alternation violating non-cartesian monoidal structure (§9b). Replaces legacy `Discourse.detect_prompt_injection()` |

---

## §5 Enriched Categories

The transition from discrete to continuous: case categories enriched over $[0,1]$, where hom-values represent distributional proximity. This provides the mathematical grounding for connecting symbolic grammar to statistical semantics.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Hom-value $\mathcal{C}(A,B)\in[0,1]$ | `src.enriched_cat.enriched` | `EnrichedCategory.hom()` | ✅ | Reads `proximity_matrix[i,j]` |
| Identity axiom $\mathcal{C}(A,A)=1$ | `src.enriched_cat.enriched` | `EnrichedCategory.__post_init__` → `_validate()` | ✅ | Enforced at construction; raises `ValueError` on violation |
| Composition inequality (eq. `eq-5-2`) | `src.enriched_cat.enriched` | `EnrichedCategory.check_composition_inequality()` | ✅ | Returns bool |
| Magnitude $|\mathcal{C}| = \sum_{ij}(Z^{-1})_{ij}$ (eq. `eq-5-3`) | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` | ✅ | Via `np.linalg.inv` |
| Similarity matrix $Z$ (eq. `eq-5-4`) | `src.enriched_cat.enriched` | `EnrichedCategory.proximity_matrix` | ✅ | NumPy ndarray |

## §5b Magnitude Homology

Magnitude as a **complexity invariant** for case systems, and its connection to transformer attention via information geometry.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Effective size = magnitude | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` (+ `magnitude_deficit()`) | ✅ | $\lvert\mathcal{C}\rvert$ and $n - \lvert\mathcal{C}\rvert$ quantify effective-size and redundancy respectively |
| Role clusters by proximity | `src.enriched_cat.enriched` | `EnrichedCategory.role_clusters()` | ✅ | Threshold-based grouping |
| Magnitude < n indicates redundancy | `src.enriched_cat.enriched` | `EnrichedCategory.magnitude()` | ✅ | $\|\mathcal{C}\| < n$ means roles overlap |
| Enriched hom-proximity heatmap | `src.visualization.enriched_diagrams` | `render_enriched_heatmap()` | ✅ | Fig. 15 in manuscript |
| Magnitude homology invariant $H_k(\mathcal{C})$ (Leinster-Shulman) | `src.diagrams.complexity_metrics` | `MagnitudeHomologyMetrics` | 🔄 | Graded homology is the theoretical target, not the implemented object: the dataclass records `base_syntactic_complexity: float`, `topological_holes_1d: int`, `estimated_decoherence_rate: float`, `quantum_environment_commutes: bool` — a scalar complexity, a 1-D hole count and a decoherence estimate, with no $H_k$ sequence |
| Quantum decoherence proxy for magnitude homology | `src.diagrams.complexity_metrics` | `compute_quantum_magnitude_homology()` | 🔄 | Computes no $\|\mathcal{C}\|_q$ value: it returns the real syntactic complexity score, a `cups − caps` hole proxy, and `min(1.0, noise · 1.5^holes)` checked against an unsourced 0.25 threshold — illustrative constants, not the $\|\mathcal{C}\|(1-\lambda)$ formula of the §5b caveat |

---

## §6 Topos Theory

Caramello's bridge technique: when two case-theoretic formalizations have Morita-equivalent classifying toposes, theorems transfer automatically between them. The module implements the *invariant screen* for that technique — necessary conditions that can rule equivalence out — not a proof that it holds.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Geometric theory | `src.topos_theory.topos` | `GeometricTheory` | ✅ | `name`, `axioms`, `sorts` |
| Classifying topos | `src.topos_theory.topos` | `ClassifyingTopos` | ✅ | `theory`, `invariants` |
| Morita equivalence (eq. `eq-6-1`) | `src.topos_theory.topos` | `check_morita_equivalence()` | 🔄 | **Necessary conditions only**: compares signature shape (sorts, relations, axioms) exactly plus the arity spectrum. A `True` means "not ruled out", never "equivalent" — exhibiting an equivalence of classifying toposes is out of scope for the module |
| Bridge transfer | `src.topos_theory.topos` | `bridge_transfer()` | 🔄 | Attempts transfer between theories that pass the necessary-condition gate above; the returned dict carries `necessary_conditions_only: True`, so a successful transfer licenses attempting the inference, not asserting its validity |

---

## §7 Cognitive Integration (Active Inference)

Active inference as a process theory: agents maintain beliefs over case role assignments and minimize variational free energy through Bayesian updating. This layer uses **point-estimate** (scalar) methods.

| Manuscript Element | Module | Class / Function | Status | Notes |
|---|---|---|---|---|
| Case diagram belief $q(s)$ | `src.cognitive.belief` | `CaseDiagramBelief` | ✅ | Probability distribution over case roles |
| KL divergence $\text{KL}(q \| p)$ | `src.cognitive.free_energy` | `kl_divergence()` | ✅ | Core free energy decomposition |
| Variational free energy $F = \mathbb{E}_q[\log q - \log p]$ | `src.cognitive.free_energy` | `variational_free_energy()` | ✅ | Minimized by perceptual inference |
| Bayesian belief update $q(s) \propto p(o|s) q(s)$ | `src.cognitive.belief_updating` | `update_belief()` | ✅ | Single-step posterior |
| Five-step generative loop (§7) | `src.cognitive.belief_updating` | `sequential_belief_update()` | ✅ | Multi-word processing |
| Precision-weighted PE: $\text{PE} = w_f \cdot |\mu_{pred} - \mu_{obs}|$ | `src.cognitive.prediction_error` | `prediction_error()` | ✅ | P600 ERP prediction |
| P600 amplitude ratio $w_{\mathrm{strong}}/w_{\mathrm{weak}}$ | `src.cognitive.prediction_error` | `p600_amplitude_ratio()` | ✅ | Predicts ERP ratio |
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
| Multi-step belief push-forward | `src.daif.core` | `distributional_bellman_operator()` | 🔄 | Forward recursion over beliefs, **not** a value backup: step $k$ returns the distribution of $R + \gamma (T^\top q_k)$. It does not converge to the Bellman fixed point $Z^* = TZ^*$; read the output as a discounted one-step return under an evolving belief, never as a value function (see the module docstring for the worked counterexample) |
| C51 categorical projection $\Phi Z$ | `src.daif.core` | `categorical_return_distribution()` | ✅ | Linearly interpolates quantiles onto $N$ fixed voltage supports |
| Quantile Huber loss $\rho^\kappa_\tau$ (Eq. 7-2) | `src.daif.quantile` | `quantile_td_update()` | ✅ | Differentiable transition bridging absolute and $L^2$ distances via threshold $\kappa$ |
| IQN risk-distorted update | `src.daif.quantile` | `implicit_quantile_network_update()` | ✅ | Applies non-linear functions to index $\tau$: neutral / optimistic / pessimistic / CVaR |
| Wasserstein distance $W_p(Z_a, Z_b)$ | `src.daif.quantile` | `wasserstein_return_distance()` | ✅ | Inverse-CDF map: $(\int_0^1 \|F^{-1}(\tau) - G^{-1}(\tau)\|^p d\tau)^{1/p}$ |
| Distributional DAIF posterior | `src.daif.inference` | `distributional_case_assignment()` | ✅ | Evaluates conjugate belief against threshold $\epsilon=10^{-6}$ |
| Precision-weighted VMP | `src.daif.inference` | `variational_message_passing()` | ✅ | Sum-product with sequential damping to arrest cycle oscillations |
| Bethe free energy (Eq. 7-3) $F_{\text{Bethe}}$ | `src.daif.inference` | `bethe_free_energy()` | ✅ | Subtracts intersection entropy terms for loopy geometries |
| Expected information gain EIG$(o^*)$ | `src.daif.inference` | `expected_information_gain()` | ✅ | Computes discrete KL divergence iteratively conditioned on $o^*$ |
| DPE scalar (Eq. 7c-dpe-scalar) $= w_f \cdot (-\log q[c])$ | `src.daif.prediction` | `distributional_prediction_error()` | ✅ | Weights cross-entropy by enriched morphism weight $w_f$ |
| DPE Wasserstein (Eq. 7c-dpe) $= w_f \cdot W_1(Z_{\text{pred}}, Z_{\text{obs}})$ | `src.daif.prediction` | `wasserstein_prediction_error()` | ✅ | Precision-weighted distributional mismatch |
| DPE_semantic (Eq. 7c-dpe-semantic) $= \lvert \mathbb{E}[Z_{\text{pred}}] - \mathbb{E}[Z_{\text{obs}}] \rvert$ | `src.daif.prediction` | `n400_from_return_distribution()` | ✅ | Mean-return mismatch — heuristic (N400-tracking) component |
| DPE_structural (Eq. 7c-dpe-structural) $= W_1(Z_{\text{pred}}, Z_{\text{obs}})$ | `src.daif.prediction` | `wasserstein_prediction_error()` → `p600_from_precision_update()` | ✅ | Wasserstein-1 mismatch — discrepancy/update (P600-tracking) component |
| N400 (Eq. 7c-n400) $= -\,\mathrm{DPE}_{\text{semantic}} \cdot w_c \cdot S_{\text{viol}}$ | `src.daif.prediction` | `n400_from_return_distribution()` | ✅ | Signed negative per ERP convention |
| P600 (Eq. 7c-p600) $= s \cdot \Delta\Lambda \cdot \mathrm{DPE}_{\text{structural}} \cdot S_{\text{viol}}$ | `src.daif.prediction` | `p600_from_precision_update()` | ✅ | $s$ is dimensionless amplitude-calibration scalar (default 1.0) |
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
| DAIF belief trajectory (Fig. 17b) | `src.visualization.daif_plots` | `plot_belief_trajectory()` | ✅ | Renders temporal evolution; bottom-panel fan is a proxy, not a 51-quantile push-forward decomposition (explicit in caption) |
| DAIF free energy convergence (Fig. 17c) | `src.visualization.daif_plots` | `plot_free_energy_convergence()` | ✅ | Real `fe_trajectory` + real KL/log-lik decomposition via optional `kl_trajectory` / `loglik_trajectory` kwargs |
| DAIF ERP predictions (Fig. 17d) | `src.visualization.daif_plots` | `plot_erp_predictions()` | ✅ | Real DAIF-predicted N400/P600 via optional `n400_amplitudes` / `p600_amplitudes` kwargs; literature-typical ranges shown with error bars |
| Limitations & neurobiological scope (§daif-limitations) | N/A | Documented in `docs/manuscript/07c_daif_results.md` | 📋 | Mean-field approximation trade-off, enriched-category unification conjecture, single-sentence empirical scope, PAC-latency gap (ROSE) |
| Supporting utilities (§daif-support-utils) | `src.daif.policy`, `src.daif.core` | `distributional_epistemic_value()`, `categorical_return_distribution()` | ✅ | Documented as explicit support for Eq. 7c-g risk term and Eq. 7c-c51 projection |

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
| Topological robustness | `src.security.cognitive_security` | `topological_robustness()` | ✅ | Returns $R = \lvert\mathcal{C}\rvert / n$. Bounded in $(0, 1]$ **only** for hom-matrices satisfying the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B)\cdot\mathcal{C}(B,C)$; `EnrichedCategory._validate` does not enforce that axiom, so a user-supplied matrix can yield $R > 1$ (the function logs a warning when it does) |
| Semantic integrity | `src.security.cognitive_security` | `semantic_integrity_check()` | ✅ | Asserts identity constraints on $Z$ trace matrices |

---

## Appendix: Notation → Code Symbol Mapping

Selected entries from `11b_notation.md` (App B) mapped to Python identifiers:

| Notation (Manuscript) | Python Identifier | Package |
|----------------------|-------------------|---------|
| $\mathcal{C}$ | `CaseCategory` | `case_systems` |
| $\text{Ob}(\mathcal{C})$ | `CaseCategory.objects` | `case_systems` |
| $\text{Hom}(A, B)$ | `EnrichedCategory.hom(A, B)` | `enriched_cat` |
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

## Verification Protocol

To independently verify that every theory-to-code mapping above is correct:

### Step 1: Run the Full Test Suite

From the project root (the directory holding `src/`, `tests/` and `pyproject.toml`):

```bash
uv run pytest tests/ --cov=src -v
```

This runs every `tests/test_*.py` file (authoritative live count in `output/metrics.json::total_test_files`; 64 as of this revision). Coverage must exceed the 90 % floor on `src/` declared by `[tool.coverage.report] fail_under = 90` in `pyproject.toml`; the measured figure is `output/metrics.json::coverage_percent` — read it there rather than quoting a number from prose. Every row in the tables above has at least one corresponding `assert` in the test suite.

### Step 2: Verify Specific Equations

Each equation can be verified in isolation. For example, to confirm that the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ is enforced:

```bash
uv run pytest tests/test_enriched_cat_enriched.py -k "composition_inequality" -v
```

### Step 3: Check Notation–Code Alignment

The Appendix notation table above maps every mathematical symbol used in the manuscript to its Python identifier. To verify completeness, check that every `\label{eq:...}` in the manuscript has a corresponding entry:

```bash
grep -r '\\label{eq:' docs/manuscript/ | wc -l
```

### Step 4: Generate and Inspect Figures

All 30 figures are generated from the same `src/` code used above. To regenerate and verify:

```bash
uv run python scripts/generate_diagrams.py
ls -la output/figures/*.png | wc -l  # Should match output/metrics.json::total_figures (30 as of this revision)
```

### Traceability Invariant

The mapping states a **bidirectional traceability invariant**: every manuscript equation must have a Python implementation, and every public function in `src/` must trace back to a manuscript equation (or to a utility/visualization role documented in [`api_reference.md`](api_reference.md)). ADR-007 records the intent.

The invariant is currently a **convention, not a gate** — nothing in the test suite
checks it, and it has drifted before. Verify it by hand with:

```bash
uv run python - <<'PY'
import importlib, pathlib, re
docs = "\n".join(p.read_text() for p in pathlib.Path("docs").rglob("*.md"))
for pkg in ("case_systems", "diagrams", "enriched_cat", "topos_theory",
            "cognitive", "daif", "quantum", "security", "visualization"):
    mod = importlib.import_module(f"src.{pkg}")
    missing = [n for n in mod.__all__
               if not re.search(rf"\b{re.escape(n)}\b", docs)]
    print(pkg, "undocumented:", missing)
PY
```

Making this real means turning that check into a test asserting, for each package's
`__all__`, that every symbol appears by word-boundary match in `api_reference.md`,
this file, or `docs/manuscript/*.md`.

---

*Scope: all 9 `src/` subpackages are mapped; the DAIF layer covers `daif_symbols` public symbols across `daif_modules` modules (live values in `output/metrics.json`, currently 25 across 7). Figure-to-code traceability covers every figure in `output/figures/` (`output/metrics.json::total_figures`), including the three pedagogical unpacking companions for §3 / §4b / §4c. Most rows are ✅; the 🔄 rows above mark places where the code implements a screen or an approximation rather than the full theoretical object, and each says which.*

