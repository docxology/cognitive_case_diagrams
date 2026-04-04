# Appendix C: Automated Test Suite Inventory {#sec:test-suite-inventory}

This appendix lists the test categories behind the counts reported in \autoref{sec:diagrammatic-cognition}. Every test uses real mathematical computations—no mocks or fakes.

- **Categorical axiom tests**: Identity morphism existence, composition associativity, weight invariants, `is_well_formed()` full axiom check
- **Enriched category tests**: Hom-value constraints, composition inequality, categorical magnitude, magnitude deficit, full composition check, role clustering
- **Diagram type tests**: Pregroup diagrams validated for `dom == Ty()` and `cod == s`, correct box counts, diagram equality
- **Metrics tests**: Normal form preservation, depth computation with graceful fallback for pregroup diagrams
- **Natural transformation tests** (20 tests): Component morphism construction, `naturality_holds` / `verify_naturality` on identity and incomplete maps, identity transformation generation, vertical composition of transformations, completeness checking over all domain objects
- **Complexity metrics tests** (17 tests): DisCoPy box/cup/cap counting on transitive/ditransitive diagrams, normal form computation and snake equation verification, syntactic complexity scoring with configurable weights, cross-diagram comparison utilities
- **Topos theory tests** (18 tests): Geometric theory construction from standard and minimal case categories, classifying topos invariant computation, Morita equivalence verification (positive and negative cases), bridge transfer between equivalent theories with transfer-blocking for non-equivalent theories, enriched theory construction
- **Fluid-S tests** (22 tests): Volitional/non-volitional mapping, probability splits, Bats language examples, kernel computation, enriched weight scaling
- **Active inference tests** (107 tests across 7 test files): Belief construction and entropy, KL divergence (Gibbs' inequality, asymmetry), variational free energy, Bayesian belief update with zero-likelihood edge case, sequential multi-word belief update (five-step generative loop with entropy convergence), prediction error scaling including P600 ERP prediction with boundary weights, expected free energy decomposition (epistemic vs pragmatic), magnitude-based garden-path reanalysis cost with symmetry, N400 semantic violation proxy (includes integration tests in `test_cognitive_integration.py`)
- **Quantum case tests** (20 tests): Crisp POVM orthogonal projectors, graded proto-role POVM, Fluid-S basis rotation, density matrix creation, \autoref{eq:eq-8-1} (in \autoref{sec:quantum-semantics}) P(c|ρ) = Tr(E_c ρ) verification
- **Cognitive security tests** (18 tests): Type-violation detection, case frame validation, injection score computation, magnitude-based topological robustness, composition inequality as security boundary
- **Ditransitive tests** (12 tests): Three-argument sentence creation, NOM/ACC/DAT case assignment, DisCoPy diagram with 3 cups, complexity comparison with transitive
- **Visualization tests** (4 tests): Complexity comparison bar chart rendering, normal form comparison chart, radar chart generation—all producing valid PNG output files
- **DAIF subpackage tests** (161 tests across 7 test files with 100% pass rate):
  - `test_daif_core.py` (24 tests): Distributional Bellman operator, push-forward return, C51 categorical projection
  - `test_daif_quantile.py` (21 tests): QR-DQN quantile Huber loss, IQN risk distortion (neutral/optimistic/pessimistic/CVaR), Wasserstein distances $W_1$/$W_2$
  - `test_daif_inference.py` (25 tests): `distributional_case_assignment()` posterior convergence, variational message passing, Bethe free energy, expected information gain
  - `test_daif_prediction.py` (27 tests): DPE precision-weighting, N400/P600 amplitude from return distributions, full `ERPProfile` waveform generation and peak latency
  - `test_daif_policy.py` (19 tests): `G_policy()` EFE + risk term, Boltzmann policy temperature scaling, distributional epistemic value
  - `test_daif_metrics.py` (24 tests): Convergence diagnostics (monotonicity, reduction percentage), distributional KL divergence, quantile calibration error, return entropy

```{=latex}
\newpage
```
