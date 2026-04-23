# API Reference

Public API for all `src/` packages in the `cognitive_case_diagrams` project.

> For theory-to-code mapping, see [`theory_implementation_map.md`](theory_implementation_map.md).  
> For term definitions, see [`glossary.md`](glossary.md).  
> For adding new modules, see [`extension_guide.md`](extension_guide.md).  
> For architecture overview, see [`architecture_overview.md`](architecture_overview.md).

---

## Manuscript metrics helper (`src.generate_manuscript_metrics`)

Not one of the nine domain subpackages: a **build-time** module at [`../src/generate_manuscript_metrics.py`](../src/generate_manuscript_metrics.py). It collects test counts, DAIF figures, domain package counts, optional **coverage totals** from `coverage.json` (produce with `uv run pytest tests/ --cov=src --cov-report=json`), installed **NumPy/DisCoPy** versions, and English-word forms for counts; then writes `output/metrics.json` for `${…}` substitution in manuscript Markdown (see [`../manuscript/11c_automated_test_inventory.md`](../manuscript/11c_automated_test_inventory.md) and [`../manuscript/config.yaml`](../manuscript/config.yaml)).

```bash
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=json   # refresh coverage.json at project root
uv run python -m src.generate_manuscript_metrics   # writes output/metrics.json
uv run python -m src.generate_manuscript_metrics --dry-run
uv run python scripts/inject_variables.py          # writes output/manuscript/*.md
```

Public entrypoints: `collect_metrics()`, `write_metrics()` (see module docstring).

---

## `src.case_systems` — Linguistic Case Systems (§2)

### `CaseRole` (enum)
```python
class CaseRole(Enum):
    # Core morphosyntactic cases (8-case inventory)
    NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC

    # Alignment-specific cases
    ERG, ABS

    # Pre-alignment primitives
    S, A, P
```
Case roles used throughout the project. In addition to an 8-case inventory,
the project includes alignment-specific roles (`ERG`, `ABS`) and the universal
primitives (`S`, `A`, `P`) used to define alignment functors.

### `Morphism`
```python
@dataclass(frozen=True)
class Morphism:
    source: CaseRole
    target: CaseRole
    label: str
    weight: float = 1.0      # ∈ [0, 1] — proto-role strength
```

### `CaseCategory`
```python
class CaseCategory:
    objects: set[CaseRole]
    morphisms: list[Morphism]

    def compose(self, f: Morphism, g: Morphism) -> Morphism  # w(g∘f)=w(f)·w(g)
    def is_well_formed(self) -> bool
```

**Factory functions:**
```python
def standard_case_category() -> CaseCategory            # 8-case inventory + canonical morphisms
def minimal_case_category() -> CaseCategory             # minimal transitive: NOM/ACC/INS
def introductory_case_category() -> CaseCategory        # intro figure: +VOC, weighted triangle, addresses
def accusative_alignment() -> dict[CaseRole, CaseRole]  # {S,A}→NOM, P→ACC
def ergative_alignment() -> dict[CaseRole, CaseRole]    # {S,P}→ABS, A→ERG
def tripartite_alignment() -> dict[CaseRole, CaseRole]  # S→ABS, A→ERG, P→ACC
def active_stative_alignment() -> dict[str, dict[CaseRole, CaseRole]]
```

### `AlignmentFunctor`
```python
@dataclass
class AlignmentFunctor:
    name: str
    source: CaseCategory
    target: CaseCategory
    object_map: dict[CaseRole, CaseRole]

    def map_object(role: CaseRole) -> CaseRole
    def map_morphism(morphism: Morphism) -> Morphism  # preserves weight
    def preserves_identity(role: CaseRole) -> bool
    def preserves_composition(f: Morphism, g: Morphism) -> bool  # structure + weight
    def is_injective() -> bool
    def image_roles() -> set[CaseRole]
```

### `NaturalTransformation`
```python
@dataclass
class NaturalTransformation:
    name: str
    source_functor: AlignmentFunctor
    target_functor: AlignmentFunctor
    components: dict[CaseRole, ComponentMorphism]

    def set_component(role: CaseRole, component: ComponentMorphism) -> None
    def is_complete() -> bool
    def component_morphisms() -> list[Morphism]
    def image_roles() -> set[CaseRole]
    def naturality_holds(*, rel_tol: float = 1e-9, abs_tol: float = 1e-9) -> bool
    def verify_naturality(*, rel_tol: float = 1e-9, abs_tol: float = 1e-9) -> bool  # alias
```

Checks naturality on morphisms in ``source_functor.source`` whose endpoints lie in the functor’s ``object_map``; requires ``is_complete()``.

### `FluidSFunctor`
```python
@dataclass
class FluidSFunctor:
    name: str = "Fluid-S"
    volition: VolitionContext = VolitionContext.VOLITIONAL
    volition_probability: float = 1.0     # graded ∈ [0, 1]
    source: CaseCategory | None = None
    target: CaseCategory | None = None

    def map_object(role: CaseRole) -> CaseRole
    def map_object_in_context(role: CaseRole, p_volitional: float) -> dict[CaseRole, float]
    def split_probability(role: CaseRole) -> dict[CaseRole, float]
    def map_morphism(morphism: Morphism) -> Morphism
    def preserves_identity(role: CaseRole) -> bool
    def kernel() -> list[tuple[CaseRole, CaseRole]]
```

**Factory functions:**
```python
def create_fluid_s_functor(volitional: bool = True, probability: float = 1.0) -> FluidSFunctor
def bats_fluid_s() -> tuple[FluidSFunctor, FluidSFunctor]  # (vol, nonvol)
def fluid_s_enriched_weight(p_volitional: float, base_weight: float = 1.0) -> float
```

### Usage Example: Creating a Case Category

```python
from src.case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, accusative_alignment, ergative_alignment
)

# Create the standard 8-case category
cat = standard_case_category()
assert cat.is_well_formed(), "Category axioms violated"

# Compose two morphisms: weight is multiplicative (Eq. eq-2-1)
f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.9)
g = Morphism(CaseRole.ACC, CaseRole.DAT, "transfers_to", weight=0.8)
h = cat.compose(f, g)  # h.weight == 0.72

# Compare alignment systems
acc = accusative_alignment()  # {S,A} → NOM, P → ACC
erg = ergative_alignment()    # {S,P} → ABS, A → ERG
assert acc[CaseRole.S] == CaseRole.NOM
assert erg[CaseRole.S] == CaseRole.ABS
```

> **Mathematical note**: Morphism composition implements $w(g \circ f) = w(g) \cdot w(f)$ from §2. This multiplicative weight propagation encodes the proto-role gradient — see [`glossary.md`](glossary.md#linguistic-case-theory) for details.

### `MonoidalFunctor` (tensor checks; §9b protocol narrative)
```python
class MonoidalFunctor:
    """Tensor-preservation checks on case-alignment maps (cf. §9b).

    Used in the **specification-level** analysis of prompt injection under a
    Categorical Communication Protocol—not as a guarantee on production LLM APIs."""
    source_category: CaseCategory
    target_category: CaseCategory
    object_map: dict[CaseRole, CaseRole]

    def preserves_tensor(role_a: CaseRole, role_b: CaseRole) -> bool
    # Returns False if tensor structure collapses or morphisms are missing —
    # models illicit role merges discussed in §9b.
```

**Phase 2 additions to `CaseCategory`**:
```python
# Added to src/case_systems/case_category.py in Phase 2
class CaseCategory:
    # ... existing methods ...

    def assess_daif_surprisal(
        self, observed: Morphism, predicted_weight: float
    ) -> dict[str, float]:
        """Compute N400 and P600 DAIF surprisal amplitudes.
        Returns {"N400_amplitude": float, "P600_amplitude": float} per the
        Li & Futrell (2024) / Rabovsky et al. (2025) shallow/deep surprisal
        decomposition (§7c).
        N400 ~ |predicted_weight − observed.weight|.
        P600 ~ 1.0 if observed is not structurally licensed, else 0.0."""
```

For categorical type-checking and prompt-injection detection, use
``security.CaseFrameValidator.validate_assignment()`` (see
[`src.security.cognitive_security`](#srcsecurity--cognitive_security)).

---

## `src.diagrams` — String diagrams, complexity, discourse (§3–§4c)

### `string_diagram` — Native Representations

```python
class Sentence:
    text: str
    boxes: list[Box]
    wires: list[Wire]
    case_assignments: dict[str, CaseRole]

    def add_noun(word: str, case_role: CaseRole) -> Wire
    def add_verb(word: str, subject: Wire, obj: Wire = None) -> Wire
    @classmethod
    def transitive(cls, subject, verb, obj) -> Sentence
    @classmethod
    def intransitive(cls, subject, verb) -> Sentence

class Discourse:
    sentences: list[Sentence]
    entity_wires: dict[str, list[Wire]]
    role_history: dict[str, list[CaseRole]]

    def add_sentence(sentence: Sentence) -> None
    def role_reversal_entities() -> list[str]

    @classmethod
    def two_sentence(cls, subj1, verb1, obj1, subj2, verb2) -> Discourse
    @classmethod
    def role_reversal(cls, entity: str, partner: str) -> Discourse
```

For discourse-level prompt-injection detection, build a
``CaseFrameValidator`` from ``src.security.cognitive_security`` and call
``validate_assignment(role_history_per_entity)`` on the relevant slice of
``Discourse.role_history``.

### `ditransitive` — Three-argument constructions
```python
@dataclass
class DitransitiveSentence:
    subject: str
    verb: str
    direct_object: str
    indirect_object: str
    sentence: Sentence  # populated in __post_init__; case NOM (subject) / DAT (indirect_object) / ACC (direct_object)

def create_ditransitive(subject: str, verb: str, indirect_object: str, direct_object: str) -> DitransitiveSentence
def create_discopy_ditransitive(subject, verb, indirect_object, direct_object)  # discopy.grammar.pregroup.Diagram
```

### `string_diagram` — DisCoPy Integration (requires `discopy`)

```python
# Base functions (discopy.rigid.Box)
def create_discopy_transitive(subject, verb, obj) -> rigid.Diagram
def create_discopy_intransitive(subject, verb) -> rigid.Diagram
def create_discopy_passive(subject, verb, agent) -> rigid.Diagram
def create_discopy_snake_equation() -> tuple[Diagram, Diagram, Diagram]
def create_discopy_composition(subject, verb, obj) -> tuple[Diagram, Diagram]
def create_discopy_multilingual(translations=None) -> dict[str, Diagram]

# Extended functions (discopy.grammar.pregroup.Word + eager_parse)
def create_word_diagram_transitive(subject, verb, obj) -> pregroup.Diagram
def create_word_diagram_intransitive(subject, verb) -> pregroup.Diagram
def create_swap_passive(subject, verb, agent) -> pregroup.Diagram
def create_word_diagram_ditransitive(subject, verb, io, do) -> pregroup.Diagram

# Semantic evaluation (discopy.tensor — DisCoCat F: Preg → FVect)
def create_tensor_semantics(
    subject, verb, obj,
    noun_dim=2, sentence_dim=4,
    subject_vec=None, object_vec=None, verb_tensor=None,
) -> tuple[tensor.Diagram, numpy.ndarray]
# Builds diagram in tensor category and evaluates via .eval()
# Returns (diagram, meaning_vector) with meaning_vector.shape == (sentence_dim,)
```

### `complexity_metrics`

```python
@dataclass
class DiagramMetrics:
    name: str
    box_count: int; word_count: int; cup_count: int; cap_count: int
    is_normal_form: bool; normal_form_box_count: int
    dom_type: str; cod_type: str
    depth: int; width: int

def count_boxes(diagram: Diagram) -> int
def count_words(diagram: Diagram) -> int
def count_cups(diagram: Diagram) -> int
def count_caps(diagram: Diagram) -> int
def diagram_depth(diagram: Diagram) -> int    # diagram.depth() — sequential layers
def diagram_width(diagram: Diagram) -> int    # diagram.width — max parallel wires
def compute_normal_form(diagram: Diagram) -> Diagram
def is_in_normal_form(diagram: Diagram) -> bool
def diagrams_equal(d1: Diagram, d2: Diagram) -> bool  # via normal form
def analyze_diagram(diagram: Diagram, name: str) -> DiagramMetrics
def syntactic_complexity_score(diagram: Diagram) -> float
# Formula: words + 0.5*cups + 0.25*caps + 0.1*depth
def compare_diagrams(diagrams: list[tuple[str, Diagram]]) -> list[DiagramMetrics]

@dataclass
class MagnitudeHomologyMetrics:
    base_syntactic_complexity: float
    topological_holes_1d: int
    estimated_decoherence_rate: float
    quantum_environment_commutes: bool

def compute_quantum_magnitude_homology(
    diagram: Diagram,
    environmental_noise: float = 0.05,
) -> MagnitudeHomologyMetrics
```

---

## `src.enriched_cat` — Enriched Categories (§5)

### `EnrichedCategory`
```python
@dataclass
class EnrichedCategory:
    name: str
    roles: list[CaseRole]                  # cardinality $N_C$
    proximity_matrix: np.ndarray           # $N_C \times N_C$ matrix, entries $Z_{ij} \in [0,1]$

    def hom(source: CaseRole, target: CaseRole) -> float
    def check_composition_inequality(a, b, c: CaseRole, *, rel_tol: float = 1e-9) -> bool
    def magnitude() -> float               # ∑ᵢⱼ (Z⁻¹)ᵢⱼ , bounded by $\mathcal{O}(N_C^3)$
    def weighting() -> np.ndarray          # column sums of Z⁻¹
    def coweighting() -> np.ndarray        # row sums of Z⁻¹
    def magnitude_deficit() -> float        # n − |C|
    def full_composition_check() -> dict    # {"holds", "violations", "violation_rate", "total"}
    def role_clusters(threshold: float = 0.6) -> list[set[CaseRole]]
```

> **Identity axiom** $\mathcal{C}(A,A) = 1$ is enforced inside `__post_init__` via `_validate()` at construction time (raises `ValueError` otherwise); no separate `check_identity_axiom()` method is exposed.

**Factory / module constants:**
```python
STANDARD_ROLES: list[CaseRole]           # NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC
STANDARD_PROXIMITY_MATRIX: np.ndarray    # 8×8 canonical proximity matrix
def standard_enriched_category() -> EnrichedCategory
```

### Usage Example: Computing Magnitude

```python
import numpy as np
from src.enriched_cat import EnrichedCategory
from src.case_systems import CaseRole

roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
proximity = np.array([
    [1.0, 0.7, 0.3],
    [0.7, 1.0, 0.5],
    [0.3, 0.5, 1.0],
])

ec = EnrichedCategory(name="3-case", roles=roles, proximity_matrix=proximity)
# Identity axiom C(A,A)=1 is enforced in __post_init__ (raises ValueError if violated).

# Magnitude < n indicates role redundancy
mag = ec.magnitude()  # |C| = sum of (Z⁻¹)_ij
print(f"Magnitude = {mag:.3f}")  # If < 3.0, some roles overlap
print(f"Magnitude deficit = {ec.magnitude_deficit():.3f}")  # n − |C|

# Query a hom-value and composition inequality
print(f"C(NOM, ACC) = {ec.hom(CaseRole.NOM, CaseRole.ACC):.3f}")
assert ec.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)

# Find clusters of similar roles
clusters = ec.role_clusters(threshold=0.6)
# e.g., [{NOM, ACC}] — NOM and ACC are similar above threshold
```

> **Semantics**: Magnitude $|\mathcal{C}| < n$ means the $n$ roles have distributional overlap — the "effective number" of distinct roles is less than the nominal count. See §5, `eq-5-3`.

---

## `src.topos_theory` — Topos Theory (§6)

### `GeometricTheory` / `ClassifyingTopos`
```python
class TheoryType(Enum):
    TYPOLOGICAL; TYPE_LOGICAL; DISTRIBUTIONAL; ENRICHED

@dataclass
class Axiom:
    name: str
    antecedent: str              # e.g. "f: Hom(A,B) ∧ g: Hom(B,C)"
    consequent: str              # e.g. "∃ g∘f: Hom(A,C)"
    sort_variables: list[str]

@dataclass
class GeometricTheory:
    name: str
    theory_type: TheoryType
    sorts: list[str]             # ordered list of sort names
    relation_symbols: dict[str, tuple[str, ...]]
    axioms: list[Axiom]

    def add_sort(sort_name: str) -> None
    def add_relation(name: str, arity: tuple[str, ...]) -> None
    def add_axiom(a: Axiom) -> None
    def signature_invariant() -> tuple[int, int, int]  # (|sorts|, |relations|, |axioms|)
    def arity_spectrum() -> list[int]                  # sorted relation arities

@dataclass
class ClassifyingTopos:
    theory: GeometricTheory
    invariants: dict[str, Any]

def check_morita_equivalence(
    topos1: ClassifyingTopos, topos2: ClassifyingTopos
) -> tuple[bool, list[str]]
    # Returns (equivalent, mismatches) — necessary (not sufficient) invariant check.

def build_typological_theory(
    category: CaseCategory, alignment_name: str = "typological"
) -> GeometricTheory

def build_enriched_theory(enriched_cat: EnrichedCategory) -> GeometricTheory

def bridge_transfer(
    source_topos: ClassifyingTopos, target_topos: ClassifyingTopos,
    property_name: str,
) -> dict
```

---

## `src.cognitive` — Active Inference (§7)

Six focused modules implementing point-estimate active inference:

### `belief`
```python
@dataclass
class CaseDiagramBelief:
    roles: list[CaseRole]
    probabilities: np.ndarray
    name: str = "belief"

    def entropy() -> float            # H(q) = -Σ qᵢ log qᵢ
    def most_likely_role() -> CaseRole
    def probability_of(role: CaseRole) -> float
```

### `free_energy`
```python
def kl_divergence(q: np.ndarray, p: np.ndarray) -> float
    # KL(q ‖ p) = Σ qᵢ log(qᵢ/pᵢ)
def variational_free_energy(
    q: np.ndarray, log_likelihood: np.ndarray, log_prior: np.ndarray
) -> float
    # F = E_q[log q − log p(o|s) − log p(s)]
```

### `belief_updating`
```python
def update_belief(
    prior: CaseDiagramBelief, observation_likelihoods: np.ndarray
) -> CaseDiagramBelief
    # q(s) ∝ p(o|s) · q(s)
def sequential_belief_update(
    prior: CaseDiagramBelief, observation_sequence: Sequence[np.ndarray]
) -> list[CaseDiagramBelief]
    # Five-step generative loop (§7)
```

### `prediction_error`
```python
def prediction_error(
    enriched_weight: float, predicted: float, observed: float
) -> float
    # PE(f) = w_f · |μ_predicted − μ_observed|
def p600_amplitude_ratio(weight_strong: float, weight_weak: float) -> float
    # w_strong / w_weak
```

### `action_selection`
```python
def expected_free_energy(
    q: np.ndarray, log_likelihood: np.ndarray,
    epistemic_value: np.ndarray, pragmatic_value: np.ndarray,
    gamma: float = 1.0
) -> float
    # G(π) = Ambiguity − Epistemic − γ·Pragmatic
```

### `reanalysis`
```python
def magnitude_reanalysis_cost(
    enriched_before: EnrichedCategory, enriched_after: EnrichedCategory
) -> float
    # Δ|C| = ||C_after| − |C_before||
def n400_amplitude_proxy(
    enriched_before: EnrichedCategory, enriched_after: EnrichedCategory
) -> float
    # N400 semantic violation ∝ magnitude change
```

### Usage Example: Belief Update and Prediction Error

```python
import numpy as np
from src.cognitive import (
    CaseDiagramBelief, update_belief,
    variational_free_energy, kl_divergence, prediction_error
)
from src.case_systems import CaseRole

roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.25, 0.50, 0.25]))

# Bayesian update with strong NOM evidence
likelihoods = np.array([0.8, 0.15, 0.05])
posterior = update_belief(prior, likelihoods)
assert posterior.most_likely_role() == CaseRole.NOM

# Compute prediction error with precision weighting
# PE = w_f · |μ_pred − μ_obs| (precision-weighted mismatch)
pe = prediction_error(enriched_weight=0.9, predicted=0.5, observed=0.8)
# Higher PE → larger P600 amplitude in ERP predictions
```

> **ERP link**: `prediction_error()` maps to P600 late positive component. `n400_amplitude_proxy()` maps to N400 early negativity. Together they form the neurolinguistic prediction of §7.

---

## `src.daif` — Distributional Active Inference (§7c)

Dedicated sub-package (7 modules, 25 public symbols — authoritative list in `src/daif/__init__.py::__all__`, also tracked as `daif_symbols` in `output/metrics.json`) implementing full return-distribution inference.

### `types` — Shared Type Containers
```python
class DistributionalReturn(NamedTuple):
    mean: float
    variance: float
    quantiles: np.ndarray       # shape (n_quantiles,), sorted ascending
    quantile_levels: np.ndarray # τ ∈ (0,1), shape (n_quantiles,)
    def std() -> float
    def ci(alpha: float = 0.05) -> tuple[float, float]    # credible interval
    def to_categorical(v_min, v_max, n_atoms) -> np.ndarray

@dataclass
class DAIFResult:
    belief: CaseDiagramBelief
    fe_trajectory: list[float]
    convergence_iteration: int
    return_distribution: DistributionalReturn | None
    diagnostics: dict
    # .converged, .final_fe, .fe_reduction properties

@dataclass
class ERPProfile:
    n400_amplitude: float      # μV (negative = larger N400)
    p600_amplitude: float      # μV (positive)
    waveform_ms: np.ndarray
    waveform_uV: np.ndarray
    condition: str
    dpe: float
    def peak_latency(component: str = "N400") -> float  # ms
```

### `core` — Distributional Bellman Operator
```python
def push_forward_return(
    belief: CaseDiagramBelief,
    transition_matrix: np.ndarray,  # row-stochastic, shape (n, n)
    reward_vector: np.ndarray,      # shape (n,)
    gamma: float = 0.99,
    n_quantiles: int = 51,
) -> DistributionalReturn
    # Z̄ = R + γ T^⊤ q  (distributional Bellman fixed-point)
    # Computational Cost: $\mathcal{O}(N_C \log N_C)$ due to 1D sort

def distributional_bellman_operator(
    belief, transition_matrix, reward_vector,
    gamma=0.99, n_steps=10, n_quantiles=51
) -> list[DistributionalReturn]
    # Multi-step Bellman iteration Tⁿ Z₀ → Z*
    # Time complexity $\mathcal{O}(T \cdot N_C \log N_C)$

def categorical_return_distribution(
    return_dist: DistributionalReturn,
    v_min: float, v_max: float, n_atoms: int = 51
) -> tuple[np.ndarray, np.ndarray]  # (atoms, probs)
    # C51-style distributional projection Φ mapping $\mathbb{R}$ onto $N$ discrete supports
```

### Usage Example: Distributional Bellman Iteration

```python
import numpy as np
from src.cognitive import CaseDiagramBelief
from src.case_systems import CaseRole
from src.daif import push_forward_return, distributional_bellman_operator

roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.3, 0.2]))
trans = np.array([[0.8, 0.1, 0.1], [0.1, 0.7, 0.2], [0.1, 0.2, 0.7]])
reward = np.array([1.0, 0.3, 0.5])

# Single push-forward: Z̄ = R + γ T⊤q
Z = push_forward_return(belief, trans, reward, gamma=0.99, n_quantiles=51)
print(f"Return mean={Z.mean:.3f}, std={Z.std():.3f}")
print(f"95% CI = {Z.ci(alpha=0.05)}")

# Multi-step Bellman iteration for convergence to Z*
trajectory = distributional_bellman_operator(belief, trans, reward, n_steps=10)
# trajectory[-1] is the converged return distribution
```

> **Connection to RL**: `push_forward_return()` implements the distributional Bellman operator from Bellemare et al. (2017), extended to case role distributions per §7c.

### `quantile` — Quantile TD Learning
```python
def quantile_td_update(
    current_quantiles: np.ndarray,
    target_quantiles: np.ndarray,
    learning_rate: float = 0.1,
    kappa: float = 1.0,
) -> np.ndarray
    # QR-DQN: ρ_τ^κ(δ) = |τ − I(δ<0)| · L_κ(δ)

def implicit_quantile_network_update(
    current_quantiles, current_levels,
    target_quantiles, target_levels,
    learning_rate=0.1, kappa=1.0,
    risk_distortion: str = "neutral",  # neutral|optimistic|pessimistic|CVaR
) -> np.ndarray

def wasserstein_return_distance(
    dist_a: DistributionalReturn,
    dist_b: DistributionalReturn,
    p: int = 1,  # 1 or 2
) -> float
    # W_p(Z_a, Z_b) via quantile interpolation
```

### `inference` — Variational Inference
```python
def distributional_case_assignment(
    prior: CaseDiagramBelief,
    observation_likelihoods: np.ndarray,
    transition_matrix: np.ndarray | None = None,
    n_iterations: int = 10,
    convergence_threshold: float = 1e-6,
    n_quantiles: int = 51,
) -> DAIFResult
    # Full DAIF iterative posterior: push-forward → Bayesian update → FE → convergence

def variational_message_passing(
    observations: np.ndarray,
    prior_precision: np.ndarray | float,
    likelihood_precision: np.ndarray | float,
    n_iterations: int = 16,
) -> tuple[np.ndarray, np.ndarray]  # (posterior_mean, posterior_precision)

def bethe_free_energy(
    belief: CaseDiagramBelief,
    factor_beliefs: list[np.ndarray],
    adjacency: np.ndarray,  # shape (n_vars, n_factors)
) -> float
    # F_Bethe = Σ_α KL(b_α‖f_α) − Σ_i (d_i−1) E_b_i[log b_i]

def expected_information_gain(
    current_belief: CaseDiagramBelief,
    candidate_observations: np.ndarray,  # shape (n_obs, n_roles)
) -> np.ndarray  # EIG per candidate observation
```

### `prediction` — ERP Predictions
```python
def distributional_prediction_error(
    belief: CaseDiagramBelief,
    expected_role_index: int,
    enriched_weight: float = 1.0,
) -> float
    # Scalar DPE = w_f · (−log q[expected_role])

def wasserstein_prediction_error(
    predicted: DistributionalReturn,
    observed: DistributionalReturn,
    enriched_weight: float = 1.0,
) -> float
    # Distributional DPE = w_f · W₁(Z_pred, Z_obs)  (Eq. 7c-dpe)

def n400_from_return_distribution(
    return_dist: DistributionalReturn,
    baseline_return: float = 0.0,
    precision: float = 1.0,
    violation_severity: float = 1.0,
) -> float  # N400 μV = −|E[Z] − baseline| · precision · S_violation

def p600_from_precision_update(
    prior_precision: float, posterior_precision: float,
    dpe: float, scaling: float = 1.0, violation_severity: float = 1.0,
) -> float  # P600 μV = scaling · ΔΛ · DPE · S_violation

def erp_amplitude_profile(
    belief: CaseDiagramBelief,
    expected_role_index: int,
    enriched_weight: float = 1.0,
    prior_precision: float = 1.0,
    posterior_precision: float = 2.0,
    t_start_ms: float = -200.0,
    t_end_ms: float = 900.0,
    n_timepoints: int = 1100,
    condition: str = "unknown",
    n400_peak_ms: float = 380.0,
    p600_peak_ms: float = 600.0,
    n400_sigma_ms: float = 60.0,
    p600_sigma_ms: float = 90.0,
) -> ERPProfile
    # Synthetic N400 + P600 waveform with baseline correction
```

### `policy` — Expected Free Energy
```python
def G_policy(
    belief: CaseDiagramBelief,
    log_likelihood: np.ndarray,
    epistemic_value: np.ndarray,
    pragmatic_value: np.ndarray,
    return_dist: DistributionalReturn | None = None,
    gamma: float = 1.0,
    risk_sensitivity: float = 0.0,
) -> float
    # G(π) = Ambiguity − EIG − γ·Pragmatic + β·Var[Z]

def softmax_policy_selection(
    g_values: np.ndarray,
    temperature: float = 1.0,
) -> np.ndarray  # P(π) = exp(−G/T) / Z

def distributional_epistemic_value(
    return_dist: DistributionalReturn,
    reference_variance: float = 1.0,
) -> float  # 0.5 · log(Var[Z] / σ²_ref)
```

### `metrics` — Diagnostics
```python
def convergence_diagnostics(fe_trajectory: list[float], min_iterations: int = 3) -> dict
    # Returns: monotone, total_reduction, relative_reduction_pct, converged,
    #          n_iterations, fe_range, mean_step_size, final_delta

def distributional_kl(
    dist_p: DistributionalReturn, dist_q: DistributionalReturn,
    n_bins: int = 100, epsilon: float = 1e-10,
) -> float  # KL(P‖Q) via histogram discretisation

def quantile_coverage(
    predicted_quantiles: np.ndarray,
    predicted_levels: np.ndarray,
    observed_values: np.ndarray,
) -> dict  # empirical_coverage, calibration_error, max_calibration_error, coverage_table

def return_distribution_entropy(
    return_dist: DistributionalReturn, n_bins: int = 50,
) -> float  # H[Z] in nats
```

### Usage Example: DAIF Diagnostics Pipeline

```python
from src.daif import (
    distributional_case_assignment, convergence_diagnostics,
    wasserstein_return_distance, quantile_coverage,
    distributional_kl, return_distribution_entropy
)

# Run two inferences under different conditions
result_a = distributional_case_assignment(prior, obs_congruent, trans)
result_b = distributional_case_assignment(prior, obs_violation, trans)

# 1. Convergence quality
diag = convergence_diagnostics(result_a.fe_trajectory)
assert diag["monotone"], "FE should decrease monotonically"

# 2. Distribution comparison
w1 = wasserstein_return_distance(result_a.return_distribution, result_b.return_distribution, p=1)
kl = distributional_kl(result_a.return_distribution, result_b.return_distribution)

# 3. Calibration
coverage = quantile_coverage(predicted_quantiles, predicted_levels, observed_values)
print(f"Calibration error: {coverage['calibration_error']:.4f}")

# 4. Entropy
h = return_distribution_entropy(result_a.return_distribution)
```

### DAIF Configurable Parameters Summary

| Parameter | Module(s) | Default | Range | Effect |
|-----------|-----------|---------|-------|--------|
| `n_quantiles` | `core`, `inference` | 51 | 5–201 | Quantile resolution (higher = smoother CDFs, slower) |
| `gamma` | `core`, `policy` | 0.99 | [0, 1) | Discount factor for temporal return |
| `kappa` | `quantile` | 1.0 | [0, ∞) | Huber loss threshold (0 = pure quantile, large = MSE) |
| `risk_distortion` | `quantile` | `"neutral"` | 4 modes | Risk attitude: neutral, optimistic, pessimistic, CVaR |
| `n_iterations` | `inference` | 10 | ≥1 | DAIF convergence iterations |
| `convergence_threshold` | `inference` | 1e-6 | (0, 1) | FE step size for early stopping |
| `temperature` | `policy` | 1.0 | (0, ∞) | Boltzmann softmax temperature |
| `risk_sensitivity` | `policy` | 0.0 | ℝ | Weight of Var[Z] in G-policy |

---

## `src.quantum` — Quantum Case Assignment (§8)

### `CasePOVM`
```python
@dataclass
class CasePOVM:
    roles: list[CaseRole]
    elements: dict[CaseRole, np.ndarray]   # E_c: d×d complex matrices
    dimension: int
    name: str = "povm"

    def is_complete(tolerance: float = 1e-10) -> bool
```

### Module Functions
```python
def crisp_case_povm(roles: list[CaseRole], dimension: int | None = None) -> CasePOVM
def graded_case_povm(roles: list[CaseRole], overlap_matrix: np.ndarray) -> CasePOVM
def fluid_s_povm(p_volitional: float, dimension: int = 2) -> CasePOVM
def case_probability(povm_element: np.ndarray, density_matrix: np.ndarray) -> float
    # Returns Tr(E_c @ ρ).real — single POVM element, not full CasePOVM
def semantic_state(weights: dict[CaseRole, float], dimension: int | None = None,
                   roles: list | None = None) -> np.ndarray  # density matrix ρ
```

### Usage Example: Quantum Case Measurement

```python
from src.quantum import CasePOVM
from src.quantum.quantum_case import crisp_case_povm, case_probability, semantic_state
from src.case_systems import CaseRole

# Crisp (projective) POVM: orthogonal measurement
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
povm = crisp_case_povm(roles)
assert povm.is_complete()  # Σ E_c = I

# Construct semantic density matrix ρ
rho = semantic_state(weights={CaseRole.NOM: 0.6, CaseRole.ACC: 0.3, CaseRole.DAT: 0.1})

# Born rule: P(c|ρ) = Tr(E_c ρ)
# Note: case_probability() takes a single POVM *element* matrix, not the full CasePOVM.
p_nom = case_probability(povm.elements[CaseRole.NOM], rho)
print(f"P(NOM) = {p_nom:.3f}")  # ≈ 0.6 for crisp POVM
```

> **Equation `eq-8-1`**: $P(c \mid \rho) = \text{Tr}(E_c \rho)$ generalizes case assignment to quantum states, enabling superposition of case roles and entangled multi-word assignments.

---

## `src.security` — Cognitive Security (§9b) {#srcsecurity--cognitive_security}

### `TypeViolation`
```python
@dataclass
class TypeViolation:
    source: CaseRole          # Source role of the violating morphism
    target: CaseRole          # Target role of the violating morphism
    violation_type: str        # e.g., 'missing_morphism', 'unknown_role'
    severity: float            # ∈ [0,1] (1.0 = critical)
    description: str           # Human-readable description
```

### `CaseFrameValidator`
```python
class CaseFrameValidator:
    def __init__(self, category: CaseCategory | None = None,
                 enriched: EnrichedCategory | None = None):
        # Defaults to ``standard_case_category()`` when ``category`` is None.
        ...
    def validate_assignment(
        self, assignments: dict[str, CaseRole]
    ) -> list[TypeViolation]
        # Returns a list of TypeViolation instances (empty when well-typed).
```

### Module Functions
```python
def detect_type_violation(category: CaseCategory, source: CaseRole,
                          target: CaseRole) -> TypeViolation | None
def injection_score(violations: list[TypeViolation]) -> float
def topological_robustness(enriched: EnrichedCategory) -> float
def semantic_integrity_check(enriched: EnrichedCategory) -> list[tuple]  # violated triples
```

### Usage Example: Adversarial Injection Detection

```python
from src.security import CaseFrameValidator, injection_score, detect_type_violation
from src.case_systems import CaseRole, standard_case_category

# Set up the case-frame validator with a legitimate case category (§9b protocol story)
cat = standard_case_category()
validator = CaseFrameValidator(category=cat)

# 1) Frame-level validation: map entity names → CaseRole
assignments = {
    "alice": CaseRole.NOM,
    "bob":   CaseRole.ACC,
    "cindy": CaseRole.DAT,
}
violations = validator.validate_assignment(assignments)
score = injection_score(violations)
print(f"Injection score (well-typed frame): {score:.2f}")  # 0.0

# 2) Single-morphism decidable check: detect_type_violation(category, source, target)
bad = detect_type_violation(cat, CaseRole.VOC, CaseRole.NOM)
if bad is not None:
    print(f"Violation: {bad.description} (severity={bad.severity})")
```

> **§9b insight**: Prompt injection is a type violation — adversarial text tries to reassign its case role from ACC (data/patient) to NOM (command/agent). The `CaseFrameValidator` makes this decidable.

---

## `src.visualization` — All Render Functions

Most render functions share the signature pattern:
```python
def render_*(
    data_or_args,
    output_path: Path | None = None,
    title: str = "...",
    **kwargs,
) -> plt.Figure
```

| Function | Module | Description |
|----------|--------|-------------|
| `render_case_category()` | `category_diagrams` | NetworkX graph with case role nodes |
| `render_alignment_comparison()` | `category_diagrams` | 3-panel accusative/ergative/tripartite |
| `render_composition_triangle()` | `category_diagrams` | Morphism composition triangle |
| `render_functor_diagram()` | `functor_diagrams` | Dual-panel category with functor arrows |
| `render_enriched_heatmap()` | `enriched_diagrams` | [0,1]-enriched proximity heatmap |
| `render_complexity_comparison()` | `complexity_plots` | Grouped bar chart of diagram complexity |
| `render_normal_form_comparison()` | `complexity_plots` | Original vs normal form bar chart |
| `render_syntactic_complexity_radar()` | `complexity_plots` | Radar chart of complexity dimensions |
| `render_discopy_transitive()` | `discopy_diagrams` | DisCoPy transitive sentence |
| `render_discopy_composition()` | `discopy_diagrams` | DisCoPy functor composition |
| `render_discopy_snake()` | `discopy_diagrams` | Snake equation contraction |
| `render_discopy_passive()` | `discopy_diagrams` | Passive sentence diagram |
| `render_discopy_sentence_progression()` | `discopy_diagrams` | Progressive complexity panel |
| `render_discopy_multilingual()` | `discopy_diagrams` | Cross-linguistic comparison |
| `render_discopy_ditransitive()` | `discopy_diagrams` | 3-argument sentence diagram |
| `render_discopy_discocirc_discourse()` | `discopy_diagrams` | DisCoCirc discourse circuit |
| `render_discopy_three_sentence_discourse()` | `discopy_diagrams` | Multi-sentence discourse |
| `render_discocat_sentence()` | `string_diagrams` | Manual string diagram |
| `render_discourse_diagram()` | `string_diagrams` | Discourse-level diagram |
| `render_discocirc_discourse()` | `string_diagrams` | DisCoCirc circuit rendering |
| `render_three_sentence_discourse()` | `string_diagrams` | 3-sentence discourse rendering |
| `render_syntactic_panel()` | `syntactic_sentence_diagrams` | Syntactic tree panel |
| `plot_belief_distribution()` | `active_inference_plots` | Case role belief bar chart (snapshot) |
| `plot_alignment_frame_belief_dynamics()` | `active_inference_plots` | §7 scalar alignment-frame trajectory (3-panel) |
| `plot_povm_probabilities()` | `quantum_plots` | POVM measurement bar chart |
| `plot_type_violations()` | `security_plots` | Severity-colored violation bars |
| `plot_fluid_s_volition_landscape()` | `fluid_s_plots` | 2D volition–agentivity heatmap |
| `plot_belief_trajectory()` | `daif_plots` | DAIF belief + return trajectory |
| `plot_free_energy_convergence()` | `daif_plots` | Free energy convergence curve |
| `plot_erp_predictions()` | `daif_plots` | Synthetic N400 + P600 waveforms |
| `render_pregroup_reduction_unpacking()` | `category_unpacking` | Four-panel pregroup reduction walkthrough (Fig 23) |
| `render_discocirc_entity_persistence()` | `category_unpacking` | DisCoCirc entity-persistence role-history ribbon (Fig 24) |
| `render_snake_equation_unpacking()` | `category_unpacking` | Three-panel snake-equation visual derivation (Fig 25) |

*All functions above are re-exported from `src.visualization` (see `src/visualization/__init__.py::__all__`). Last updated: 2026-04-23.*
