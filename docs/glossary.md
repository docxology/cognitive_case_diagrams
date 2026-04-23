# Glossary

Comprehensive term reference for *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case*. Maps mathematical notation, linguistic terminology, and cognitive science concepts to their Python implementations.

> Cross-reference: See [`11b_notation.md`](../manuscript/11b_notation.md) for the full mathematical notation table (sections A–K).

---

## Category Theory

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Category** | A collection of objects and morphisms with composition and identity laws | `CaseCategory` | §2 |
| **Object** | An element in a category; here, a linguistic case role | `CaseRole` (enum) | §2 |
| **Morphism** | A structure-preserving map between objects; here, a grammatical relation | `Morphism` (dataclass) | §2 |
| **Functor** | A structure-preserving map between categories; here, an alignment mapping | `AlignmentFunctor` | §2 |
| **Natural transformation** | A family of morphisms connecting two functors, one per object | `NaturalTransformation` | §2 |
| **Compact closed category** | A monoidal category where every object has a dual; enables cups/caps | DisCoPy `rigid.Category` | §3–4 |
| **Monoidal category** | A category with a tensor product ⊗ and unit object I | DisCoPy `monoidal.Category` | §3 |
| **Monoidal functor** | A functor preserving tensor structure: $F(A\otimes B)=F(A)\otimes F(B)$. In its *non-cartesian* reading, models constraints on copying/discarding wires — a **specification-level** hook for the protocol analysis of prompt injection in §9b (not a deployed-API guarantee) | `MonoidalFunctor.preserves_tensor()` | §9b |
| **Enriched category** | A category whose hom-sets are objects in a monoidal category (here, [0,1]) | `EnrichedCategory` | §5 |
| **Classifying topos** | The canonical topos associated with a geometric theory | `ClassifyingTopos` | §6 |
| **Morita equivalence** | When two theories share the same classifying topos | `check_morita_equivalence()` | §6 |

## Enriched Category Theory

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Hom-value** | The [0,1]-valued proximity between two case roles: $\mathcal{C}(A,B) \in [0,1]$ | `EnrichedCategory.hom()` | §5 |
| **Identity axiom** | $\mathcal{C}(A,A) = 1$ — self-similarity is maximal | `EnrichedCategory.__post_init__` / `_validate()` (enforced at construction) | §5 |
| **Composition inequality** | $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ | `check_composition_inequality()` | §5 |
| **Categorical magnitude** | $\|\mathcal{C}\| = \sum_{ij}(Z^{-1})_{ij}$ — the "effective size" of a category | `EnrichedCategory.magnitude()` | §5 |
| **Magnitude homology** | The Leinster–Shulman graded homological invariant $H_k(\mathcal{C})$ that categorifies magnitude from a scalar to a sequence of homology groups, revealing topological structure (clustering, holes) beyond the scalar magnitude | `MagnitudeHomologyMetrics` | §5b |
| **Quantum magnitude homology** | Magnitude homology corrected for quantum decoherence: $\|\mathcal{C}\|_q = \|\mathcal{C}\|(1-\lambda)$, where $\lambda$ is the decoherence penalty bounding classical–quantum comparison (see §5b; LM-enriched magnitude homology in Bradley and Vigneaux 2025) | `compute_quantum_magnitude_homology()` | §5b |
| **Similarity matrix** $Z$ | The proximity matrix whose entries are hom-values | `proximity_matrix` (ndarray) | §5 |

## Linguistic Case Theory

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Meaning-Text Theory (MTT)** | A linguistic framework (Mel'čuk) modeling language as a dependency-based mapping from deep semantic meaning to surface text | §2 (manuscript) | §2 |
| **Actant** | A semantic role required by a predicate's valency in dependency syntax (similar to deep case or kāraka) | §2 (manuscript) | §2 |
| **Case role** | A morphosyntactic function assigned to a noun phrase (NOM, ACC, etc.) | `CaseRole` enum | §2 |
| **Nominative** (NOM) | The subject of an intransitive or transitive verb | `CaseRole.NOM` | §2 |
| **Accusative** (ACC) | The direct object (patient) of a transitive verb | `CaseRole.ACC` | §2 |
| **Ergative** (ERG) | The agent of a transitive verb in ergative-absolutive systems | `CaseRole.ERG` | §2 |
| **Absolutive** (ABS) | The sole argument of an intransitive verb (= patient of transitive) in ergative systems | `CaseRole.ABS` | §2 |
| **Dative** (DAT) | The indirect object / recipient | `CaseRole.DAT` | §2 |
| **Genitive** (GEN) | Possessor or source | `CaseRole.GEN` | §2 |
| **Instrumental** (INS) | The instrument or means | `CaseRole.INS` | §2 |
| **Locative** (LOC) | Spatial location | `CaseRole.LOC` | §2 |
| **Ablative** (ABL) | Source or origin of motion | `CaseRole.ABL` | §2 |
| **Vocative** (VOC) | Direct address | `CaseRole.VOC` | §2 |
| **S** (Sole argument) | The single argument of an intransitive clause | `CaseRole.S` | §2 |
| **A** (Agent-like) | The agent-like argument of a transitive clause | `CaseRole.A` | §2 |
| **P** (Patient-like) | The patient-like argument of a transitive clause | `CaseRole.P` | §2 |
| **Alignment** | How a language groups S, A, P into morphological cases | `accusative_alignment()` etc. | §2 |
| **Split ergativity** | When a language uses different alignments depending on context (tense, animacy, etc.) | §2 (manuscript) | §2 |
| **Fluid-S** | An alignment where the sole argument varies between NOM/ACC based on volition | `FluidSFunctor` | §2 |
| ***Kāraka*** | Pāṇini's system of six thematic relations in Sanskrit grammar | §2 (manuscript) | §2 |
| **Proto-role** | Dowty's gradient entailment clusters (Proto-Agent, Proto-Patient) | `Morphism.weight` | §2 |

## Categorial Grammar & Semantics

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Pregroup grammar** | A type-logical grammar where types form a pregroup (partially ordered group) | DisCoPy `Ty` | §3 |
| **Type reduction** | The cancellation of adjoint types via cup operations: $n \cdot n^r \to 1$ | DisCoPy `Cup` | §3 |
| **String diagram** | A graphical calculus for morphisms in monoidal categories | `Sentence` / `create_discopy_transitive()` | §3 |
| **Cup / Cap** | The unit/counit of a compact closed category; connects adjoint types | DisCoPy `Cup`, `Cap` | §3 |
| **Snake equation** | The zigzag identity $\varepsilon \circ \eta = \text{id}$ proving coherence | `render_discopy_snake()` | §4b |
| **DisCoCat** | Categorical Compositional Distributional Semantics | `create_tensor_semantics()` / `create_word_diagram_transitive()` | §4 |
| **Meaning functor** | $F: \mathbf{Preg} \to \mathbf{FVect}$ mapping grammar to vector spaces | DisCoPy functor | §4 |
| **DisCoCirc** | Discourse-level extension of DisCoCat with persistent entity wires | `Discourse` / `create_discopy_discocirc_discourse()` | §4c |
| **Entity wire** | A persistent noun wire that carries state across sentence boundaries | §4c (manuscript) | §4c |
| **Complexity score** | $c = w_b \cdot \#\text{boxes} + w_c \cdot \#\text{cups} + w_d \cdot \text{depth}$ | `syntactic_complexity_score()` | §4b |

## Active Inference & Cognitive Science

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Active inference** | A framework where agents minimize variational free energy through action and perception | `src.cognitive` | §7 |
| **Variational free energy** | $F = \mathbb{E}_q[\log q - \log p]$ — the bound on surprise | `variational_free_energy()` | §7 |
| **KL divergence** | $D_\text{KL}(q \| p) = \sum q_i \log(q_i / p_i)$ — divergence between distributions | `kl_divergence()` | §7 |
| **Belief** | A probability distribution over case role assignments | `CaseDiagramBelief` | §7 |
| **Belief update** | $q(s) \propto p(o|s) \cdot q(s)$ — Bayesian posterior update | `update_belief()` | §7 |
| **Prediction error** (PE) | $\text{PE} = w_f \cdot |\mu_\text{pred} - \mu_\text{obs}|$ — precision-weighted mismatch | `prediction_error()` | §7 |
| **Expected free energy** (EFE) | $G(\pi) = \text{Ambiguity} - \text{EIG} - \gamma \cdot \text{Pragmatic}$ | `expected_free_energy()` | §7 |
| **P600** | An ERP component (~600ms) reflecting syntactic reanalysis | `p600_amplitude_ratio()` | §7 |
| **N400** | An ERP component (~400ms) reflecting semantic violation | `n400_amplitude_proxy()` | §7 |
| **Garden-path** | A sentence that requires reanalysis mid-parse | `magnitude_reanalysis_cost()` | §7 |
| **Generative model** | The internal model an agent uses to predict sensory input | §7 (manuscript) | §7 |
| **Precision** | The inverse variance of a distribution; controls the weight of prediction errors | $w_f$ in `prediction_error()` | §7 |

## Distributional Active Inference (DAIF)

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Distributional return** | $Z(s) = \mathbb{E}[\sum \gamma^t R_t]$ — a full return distribution, not just expectation | `DistributionalReturn` | §7c |
| **Push-forward return** | $\bar{Z} = R + \gamma T^\top q$ — distributional Bellman operator | `push_forward_return()` | §7c |
| **Quantile TD update** | $\rho_\tau^\kappa(\delta)$ — QR-DQN asymmetric Huber loss | `quantile_td_update()` | §7c |
| **IQN** | Implicit Quantile Network with risk distortion modes | `implicit_quantile_network_update()` | §7c |
| **Wasserstein distance** | $W_p(Z_a, Z_b)$ — optimal transport between return distributions | `wasserstein_return_distance()` | §7c |
| **VMP** | Variational Message Passing — damped precision-weighted belief propagation | `variational_message_passing()` | §7c |
| **Bethe free energy** | $F_\text{Bethe} = \sum_\alpha \text{KL}(b_\alpha \| f_\alpha) - \sum_i (d_i - 1) H(b_i)$ | `bethe_free_energy()` | §7c |
| **DPE** | Distributional Prediction Error: $\pi \cdot (-\log q[\text{role}])$ | `distributional_prediction_error()` | §7c |
| **ERP profile** | Synthetic N400 + P600 waveform with baseline correction | `ERPProfile`, `erp_amplitude_profile()` | §7c |
| **G-policy** | $G(\pi) + \beta \cdot \text{Var}[Z]$ — EFE with distributional risk | `G_policy()` | §7c |
| **DAIFResult** | Complete inference result: belief, FE trajectory, convergence, diagnostics | `DAIFResult` | §7c |

## Distributional RL Foundations

| Term | Definition | Code | §  |
|------|-----------|------|---|
| **C51** | Categorical distributional RL: projects return onto $n$ fixed atoms with softmax probabilities (Bellemare et al. 2017) | `categorical_return_distribution()` | §7c |
| **QR-DQN** | Quantile Regression DQN: learns quantile locations via asymmetric Huber loss $\rho_\tau^\kappa$ (Dabney et al. 2018a) | `quantile_td_update()` | §7c |
| **IQN** | Implicit Quantile Network: samples $\tau \sim U(0,1)$ and learns quantile functions with risk distortion (Dabney et al. 2018b) | `implicit_quantile_network_update()` | §7c |
| **Huber loss** | $L_\kappa(\delta) = \frac{1}{2}\delta^2$ if $|\delta| \leq \kappa$, else $\kappa(|\delta| - \frac{1}{2}\kappa)$; smooths quantile objectives | `quantile_td_update(kappa=...)` | §7c |
| **Risk distortion** | Transforms quantile levels $\tau$ to shape the agent's risk attitude (neutral, optimistic, pessimistic, CVaR) | `implicit_quantile_network_update(risk_distortion=...)` | §7c |
| **Distributional Bellman** | $\mathcal{T}Z(s) \stackrel{D}{=} R + \gamma Z(s')$ — the distributional analogue of the Bellman equation | `distributional_bellman_operator()` | §7c |
| **Categorical projection** | $\Phi$: projects a continuous return distribution onto $n$ discrete atoms (C51-style) | `categorical_return_distribution()` | §7c |
| **Reward vector** | Per-role immediate rewards $R \in \mathbb{R}^n$ used in the push-forward return | `push_forward_return(reward_vector=...)` | §7c |
| **Transition matrix** | Row-stochastic $T \in [0,1]^{n \times n}$ encoding role-to-role transition probabilities | `push_forward_return(transition_matrix=...)` | §7c |
| **Credible interval** | $[\text{CI}_{lo}, \text{CI}_{hi}]$: Bayesian confidence bounds from quantile representation | `DistributionalReturn.ci(alpha=0.05)` | §7c |
| **Return entropy** | $H[Z] = -\sum_k p_k \log p_k$ — Shannon entropy of the discretised return distribution | `return_distribution_entropy()` | §7c |

## Surprisal Decomposition & ERP Mapping

| Term | Definition | Code | §  |
|------|-----------|------|---|
| **Surprisal** | $-\log P(w_i \mid w_{<i})$ — information-theoretic processing cost of a word in context (Hale 2001) | §7, §7c (manuscript) | §7 |
| **Surprisal decomposition** | Li & Futrell (2024): decomposes total surprisal into shallow (lexical/N400) and deep (structural/P600) components | `n400_from_return_distribution()`, `p600_from_precision_update()` | §7c |
| **Calibration error** | Mean $|\text{empirical coverage}(\tau) - \tau|$ — how well predicted quantiles match observed frequencies | `quantile_coverage()` | §7c |
| **Monotone convergence** | Whether free energy decreases at every DAIF iteration (ideal convergence) | `convergence_diagnostics()["monotone"]` | §7c |
| ***assess\_daif\_surprisal*** | Instance method on `CaseCategory` that returns N400 (shallow/semantic) and P600 (deep/structural) surprisal estimates for a given morphism, implementing the Li & Futrell (2024) decomposition: N400 ~ `1 - morphism.weight`, P600 ~ variance across co-occurring role weights | `CaseCategory.assess_daif_surprisal()` | §7c |

## Quantum Semantics

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **POVM** | Positive Operator-Valued Measure — generalized quantum measurement | `CasePOVM` | §8 |
| **POVM element** | $E_c$: a positive semidefinite matrix, with $\sum_c E_c = I$ | `CasePOVM.elements` | §8 |
| **Crisp POVM** | Orthogonal projective measurement: $E_c E_{c'} = \delta_{cc'} E_c$. Special case of a POVM in which all elements are mutually orthogonal one-dimensional projectors; yields deterministic case assignment (see §8b). | `crisp_case_povm()` in `src/quantum/quantum_case.py` | §8b |
| **Graded / context-dependent POVM** | A POVM family $\{E_c^{(\lambda)}\}$ parametrised by a context variable $\lambda$ (here $p_{\text{vol}}$), so that case probabilities $P(c\mid\rho)$ vary continuously with $\lambda$ even when the underlying state $\rho$ is fixed. In this project's Fluid-S implementation the elements remain *mutually orthogonal* one-dimensional projectors at every $\lambda$ (so each individual POVM is still crisp in the formal sense), but the measurement *basis* is rotated through $\theta = (\pi/2)(1 - p_{\text{vol}})$, giving graded case assignment as a function of context. Genuinely *overlapping* POVM elements ($E_c E_{c'} \neq 0$) would be a stricter notion; none of the functions currently ship a graded POVM in that stricter sense — callers who need true element overlap must construct the density matrix and elements directly. | `fluid_s_povm()` in `src/quantum/quantum_case.py` | §8b |
| **Case probability** | $P(c|\rho) = \text{Tr}(E_c \rho)$ — probability of case assignment | `case_probability()` | §8 |
| **Density matrix** | $\rho$: a quantum state representing semantic content | `semantic_state()` | §8 |
| **ZX-calculus** | A graphical calculus for quantum circuits using Z and X spiders | §8 (manuscript) | §8 |
| **TQNN** | Topological Quantum Neural Network — QNN on spin-networks | §8 (manuscript) | §8 |
| **Holographic screen** | A boundary on which quantum measurements are projected | §8 (manuscript) | §8 |

## Topos Theory

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Geometric theory** | A first-order theory with specific axiom forms (geometric sequents) | `GeometricTheory` | §6 |
| **Classifying topos** | The canonical topos $\mathcal{E}_\mathbb{T}$ associated with a theory $\mathbb{T}$ | `ClassifyingTopos` | §6 |
| **Morita equivalence** | Two theories with equivalent classifying toposes | `check_morita_equivalence()` | §6 |
| **Bridge transfer** | Moving theorems between Morita-equivalent theories | `bridge_transfer()` | §6 |

## Cognitive Security

| Term | Definition | Code | §  |
|------|-----------|------|----|
| **Type violation** | An illicit case-role reassignment (e.g., ACC→NOM promotion) | `TypeViolation` | §9b |
| **Injection score** | Aggregate severity of detected type violations | `injection_score()` | §9b |
| **Case-theoretic firewall** | Under a fixed interaction protocol, validators that reject morphisms violating relational type constraints (engineering target; see §9b) | `CaseFrameValidator` | §9b |
| **Topological robustness** | Magnitude-based metric for resistance to adversarial perturbation | `topological_robustness()` | §9b |
| **Prompt injection** | An adversarial attack promoting data (ACC) to command (NOM) status. Detected via `CaseFrameValidator.validate_assignment()` over per-entity role assignments | `CaseFrameValidator` | §9b |

## Discourse and Compositionality

| Term | Definition | Code | §  |
|------|-----------|------|---|
| **DisCoCirc** | Discourse-level extension of DisCoCat where entity wires persist across sentence boundaries, enabling multi-sentence semantic composition | `Discourse` class | §4c |
| **Entity wire** | A persistent wire in a DisCoCirc circuit representing an entity referenced across multiple sentences | `Discourse.entity_wires` | §4c |
| **Sentence progression** | The sequential accumulation of semantic information as each sentence updates the discourse state | `discopy_sentence_progression.png` | §4c |
| **Cup-counting** | The measure of syntactic complexity by counting the number of cups (contractions) in a pregroup derivation | `count_cups()` / `DiagramMetrics.cup_count` in `src.diagrams.complexity_metrics` | §3b |
| **Meaning functor** | The structure-preserving map $\hat{F}: \mathbf{Gram} \to \mathbf{FVect}$ sending pregroup derivations to linear maps over meaning spaces | §4 (manuscript) | §4 |
| **Compact closure** | The property of a monoidal category where every object has an adjoint (dual), enabling cup/cap morphisms for composition | DisCoPy `rigid` module | §4b |

## Build and Documentation Infrastructure

| Term | Definition | Code | §  |
|------|-----------|------|---|
| **Zero-mock policy** | The architectural constraint that all tests use real mathematical computations, never `MagicMock` or `patch` | ADR-002 | all |
| **Figure parity** | The requirement that figure counts are synchronized across `manuscript_figure_index.md`, `output/figures/`, and manuscript `![...]` references | ADR-010 | all |
| **Documentation duality** | The standard that every directory carries `AGENTS.md` (machine-readable), `README.md` (human-readable), and `SKILL.md` (AI skill descriptor) | ADR-011 | all |
| **Manuscript variable injection** | The build-time substitution of `${VARIABLE}` placeholders in the manuscript with computed values from `generate_manuscript_metrics.py` | `generate_manuscript_metrics.py` | all |
| **Thin orchestrator** | A script that contains no business logic, only import-and-call orchestration of `src/` modules | root `scripts/*.py` | all |
| **Alignment functor** | A structure-preserving map between case systems of different typological alignments (ACC↔ERG, etc.) | `accusative_alignment()` etc. | §2 |

---

*Last updated: 2026-04-22. For mathematical notation details, see [Appendix B — Notation Reference](../manuscript/11b_notation.md).*

