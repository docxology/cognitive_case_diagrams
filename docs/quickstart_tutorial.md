# Quickstart Tutorial

Get up and running with the `cognitive_case_diagrams` codebase in under 10 minutes. This guide walks through environment setup, running examples, generating figures, and running the test suite.

> **Prerequisites**: Python 3.10+ (see `pyproject.toml`), [uv](https://docs.astral.sh/uv/) package manager.  
> **Full API reference**: See [`api_reference.md`](api_reference.md).  
> **Architecture overview**: See [`architecture_overview.md`](architecture_overview.md).

---

## 1. Environment Setup

```bash
# Navigate to the project directory
cd /path/to/template/projects/cognitive_case_diagrams

# Install dependencies with uv (creates .venv automatically)
uv sync --extra dev

# Verify the installation
uv run python -c "from src import CaseRole, CaseCategory; print('✅ src imported successfully')"
```

### Required Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `numpy` | Matrix operations, enriched categories | ≥1.24 |
| `matplotlib` | Figure generation | ≥3.7 |
| `pytest` | Test framework | ≥7.0 |
| `pytest-cov` | Coverage reporting | ≥4.0 |

### Optional Dependencies

| Package | Purpose | Required for |
|---------|---------|-------------|
| `discopy` | String diagram rendering | §3–4 DisCoCat/DisCoCirc figures |
| `lambeq` | QNLP compilation | §4c quantum NLP experiments |
| `scipy` | Advanced matrix operations | Some enriched category functions |

---

## 2. Your First Case Category

Create a case category, explore its morphisms, and compose them:

```python
from src.case_systems import (
    CaseRole, CaseCategory, Morphism,
    standard_case_category, accusative_alignment, ergative_alignment
)

# Create the standard 8-case category
cat = standard_case_category()
print(f"Objects: {len(cat.objects)} case roles")
print(f"Morphisms: {len(cat.morphisms)} grammatical relations")

# Check well-formedness (identity + associativity)
assert cat.is_well_formed(), "Category axioms violated!"

# Inspect a morphism
for m in cat.morphisms[:3]:
    print(f"  {m.source.name} --[{m.label}]--> {m.target.name} (weight={m.weight})")

# Compose two morphisms
f = Morphism(source=CaseRole.NOM, target=CaseRole.ACC, label="acts_on", weight=0.9)
g = Morphism(source=CaseRole.ACC, target=CaseRole.DAT, label="transfers_to", weight=0.8)
h = cat.compose(f, g)
print(f"\nComposed: {h.source.name} --> {h.target.name}")
print(f"Weight: {h.weight} = {f.weight} × {g.weight}")  # 0.72
```

### Alignment Functors

```python
# Compare alignment systems
acc = accusative_alignment()   # {S,A} → NOM, P → ACC
erg = ergative_alignment()     # {S,P} → ABS, A → ERG

print("Accusative:", acc)
# {S: NOM, A: NOM, P: ACC}

print("Ergative:", erg)
# {S: ABS, A: ERG, P: ABS}
```

---

## 3. Enriched Categories and Magnitude

Work with [0,1]-enriched categories and compute categorical magnitude:

```python
import numpy as np
from src.enriched_cat import EnrichedCategory
from src.case_systems import CaseRole

# Define a proximity matrix (hom-values)
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.GEN]
proximity = np.array([
    [1.0, 0.7, 0.4, 0.3],  # NOM
    [0.7, 1.0, 0.5, 0.2],  # ACC
    [0.4, 0.5, 1.0, 0.6],  # DAT
    [0.3, 0.2, 0.6, 1.0],  # GEN
])

ec = EnrichedCategory(name="English-4", roles=roles, proximity_matrix=proximity)

# Check categorical axioms
assert ec.check_identity_axiom(), "Identity axiom violated"
print(f"Hom(NOM, ACC) = {ec.hom_value(CaseRole.NOM, CaseRole.ACC)}")

# Compute magnitude (effective size)
mag = ec.magnitude()
print(f"Magnitude |C| = {mag:.3f}")  # < 4.0 indicates role redundancy

# Find role clusters
clusters = ec.role_clusters(threshold=0.5)
print(f"Clusters at threshold 0.5: {clusters}")
```

---

## 4. Active Inference: Belief Updating

Run a Bayesian belief update over case role assignments:

```python
import numpy as np
from src.cognitive import (
    CaseDiagramBelief, update_belief, variational_free_energy,
    kl_divergence, prediction_error
)
from src.case_systems import CaseRole

# Prior belief: uniform over 4 roles
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.GEN]
prior = CaseDiagramBelief(
    roles=roles,
    probabilities=np.array([0.25, 0.25, 0.25, 0.25])
)
print(f"Prior entropy: {prior.entropy():.3f} nats")

# Observation: strong evidence for NOM
likelihoods = np.array([0.8, 0.1, 0.05, 0.05])
posterior = update_belief(prior, likelihoods)

print(f"Most likely role: {posterior.most_likely_role().name}")
print(f"P(NOM) = {posterior.probability_of(CaseRole.NOM):.3f}")
print(f"Posterior entropy: {posterior.entropy():.3f} nats")

# Compute variational free energy
log_prior = np.log(prior.probabilities + 1e-10)
log_likelihood = np.log(likelihoods + 1e-10)
fe = variational_free_energy(posterior.probabilities, log_likelihood, log_prior)
print(f"Variational free energy: {fe:.3f}")

# Prediction error with precision weighting
pe = prediction_error(enriched_weight=0.9, predicted=0.25, observed=0.8)
print(f"Precision-weighted PE: {pe:.3f}")
```

---

## 5. DAIF: Distributional Active Inference

Run a full distributional inference to get return distributions and ERP profiles:

```python
import numpy as np
from src.daif import (
    distributional_case_assignment, push_forward_return,
    erp_amplitude_profile, convergence_diagnostics,
    wasserstein_return_distance, quantile_coverage,
    implicit_quantile_network_update, distributional_kl,
    return_distribution_entropy
)
from src.cognitive import CaseDiagramBelief
from src.case_systems import CaseRole

# Set up a DAIF inference
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
prior = CaseDiagramBelief(
    roles=roles,
    probabilities=np.array([0.4, 0.35, 0.25])
)

# Observation likelihoods and transition matrix
obs = np.array([0.7, 0.2, 0.1])
trans = np.array([
    [0.8, 0.1, 0.1],
    [0.1, 0.7, 0.2],
    [0.1, 0.2, 0.7]
])

# Run full DAIF inference
result = distributional_case_assignment(
    prior=prior,
    observation_likelihoods=obs,
    transition_matrix=trans,
    n_iterations=10,
    n_quantiles=51
)

print(f"Converged: {result.converged} at iteration {result.convergence_iteration}")
print(f"Final FE: {result.final_fe:.4f}")
print(f"Return distribution mean: {result.return_distribution.mean:.3f}")
print(f"Return distribution std: {result.return_distribution.std():.3f}")
```

### 5a. Convergence Diagnostics

Inspect whether the inference converged properly:

```python
# Analyze convergence quality
diag = convergence_diagnostics(result.fe_trajectory)
print(f"Monotone decrease: {diag['monotone']}")
print(f"Total FE reduction: {diag['total_reduction']:.4f}")
print(f"Relative reduction: {diag['relative_reduction_pct']:.1f}%")
print(f"Converged: {diag['converged']}")
print(f"Mean step size: {diag['mean_step_size']:.6f}")
```

### 5b. Risk-Distorted Inference (IQN)

Run IQN with different risk attitudes:

```python
# Compare risk attitudes on the same return distribution
for mode in ["neutral", "optimistic", "pessimistic", "CVaR"]:
    iqn_result = implicit_quantile_network_update(
        quantile_values=result.return_distribution.quantiles,
        target_quantiles=result.return_distribution.quantiles * 1.05,
        risk_distortion=mode,
    )
    print(f"  {mode:12s} → loss={iqn_result['loss']:.4f}")
```

### 5c. Wasserstein Distance & Distribution Comparisons

Compare return distributions across conditions:

```python
# Run a second inference under different likelihoods
obs_violated = np.array([0.1, 0.7, 0.2])  # Case violation
result_violated = distributional_case_assignment(
    prior=prior, observation_likelihoods=obs_violated,
    transition_matrix=trans, n_iterations=10, n_quantiles=51
)

# Wasserstein distance between the two return distributions
w1 = wasserstein_return_distance(
    result.return_distribution, result_violated.return_distribution, p=1
)
w2 = wasserstein_return_distance(
    result.return_distribution, result_violated.return_distribution, p=2
)
print(f"W₁ distance: {w1:.4f}")
print(f"W₂ distance: {w2:.4f}")

# KL divergence
kl = distributional_kl(result.return_distribution, result_violated.return_distribution)
print(f"KL(congruent ‖ violated): {kl:.4f}")

# Return entropy
h = return_distribution_entropy(result.return_distribution)
print(f"Return entropy H[Z]: {h:.4f} nats")
```

### 5d. ERP Predictions (N400 + P600)

Generate the neurolinguistic ERP profile:

```python
# Generate ERP profile (N400 + P600 waveform)
erp = erp_amplitude_profile(
    belief=result.belief,
    expected_role_index=0,
    enriched_weight=0.9,
    condition="case-violation"
)
print(f"N400 amplitude: {erp.n400_amplitude:.2f} μV")
print(f"P600 amplitude: {erp.p600_amplitude:.2f} μV")
print(f"N400 peak latency: {erp.peak_latency('N400'):.0f} ms")
```

---

## 6. Quantum Case Assignment

Set up a POVM and compute case probabilities:

```python
from src.quantum import CasePOVM
from src.quantum.quantum_case import (
    crisp_case_povm, case_probability, semantic_state
)
from src.case_systems import CaseRole

# Create a crisp (projective) POVM for 3 case roles
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
povm = crisp_case_povm(roles)
print(f"POVM complete: {povm.is_complete()}")

# Create a semantic state (density matrix)
rho = semantic_state(weights={CaseRole.NOM: 0.6, CaseRole.ACC: 0.3, CaseRole.DAT: 0.1})

# Compute case probabilities: P(c|ρ) = Tr(E_c ρ)
for role in roles:
    p = case_probability(povm.elements[role], rho)
    print(f"  P({role.name}) = {p:.3f}")
```

---

## 7. Generate All Figures

Generate the 26 publication figures:

```bash
# From the project root
cd /path/to/template

# Generate all figures via the thin orchestrator
uv run --project projects/cognitive_case_diagrams --extra dev \
    python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Figures are saved to projects/cognitive_case_diagrams/output/figures/
ls projects/cognitive_case_diagrams/output/figures/*.png
```

### Generate Individual Figures

```python
from pathlib import Path
from src.visualization import render_case_category
from src.case_systems import standard_case_category

# Render the standard case category
cat = standard_case_category()
fig = render_case_category(cat, output_path=Path("/tmp/case_category.png"))
print("Figure saved to /tmp/case_category.png")
```

---

## 8. Run the Test Suite

```bash
# Full test suite with coverage (counts change over time)
uv run --project projects/cognitive_case_diagrams --extra dev \
    python -m pytest tests/ --cov=src --cov-report=term-missing -v

# Run tests for a specific package
uv run --project projects/cognitive_case_diagrams --extra dev \
    python -m pytest tests/test_enriched_cat_enriched.py -v

# Run DAIF tests only
uv run --project projects/cognitive_case_diagrams --extra dev \
    python -m pytest tests/test_daif_*.py -v

# Quick smoke test (no coverage)
uv run --project projects/cognitive_case_diagrams --extra dev \
    python -m pytest tests/ -x -q
```

### Coverage Requirements

Thresholds are in `pyproject.toml` (`fail_under = 90` on `src/`). Current line coverage: run  
`uv run pytest tests/ --cov=src --cov-report=term-missing` from `projects/cognitive_case_diagrams/`.  
Per-subpackage reports: e.g. `--cov=src/daif`, `--cov=src/visualization`.

---

## 9. Run the Full Pipeline

Execute the complete build pipeline (tests → analysis → PDF → validation). The active project path is **`projects/cognitive_case_diagrams/`** (template root `./run.sh --project cognitive_case_diagrams`).

```bash
# From the repository root
cd /path/to/template

# Full pipeline (9 stages) — after promotion to projects/
./run.sh --project cognitive_case_diagrams

# Or individual stages:
uv run python scripts/01_run_tests.py --project cognitive_case_diagrams
uv run python scripts/02_run_analysis.py --project cognitive_case_diagrams
uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams
uv run python scripts/04_validate_output.py --project cognitive_case_diagrams
```

---

## Next Steps

| Goal | Resource |
|------|----------|
| Understand the package architecture | [`architecture_overview.md`](architecture_overview.md) |
| Look up a mathematical term | [`glossary.md`](glossary.md) |
| Find which function implements an equation | [`theory_implementation_map.md`](theory_implementation_map.md) |
| Add a new module or figure | [`extension_guide.md`](extension_guide.md) |
| Read the full API signatures | [`api_reference.md`](api_reference.md) |
| Explore the research literature | [`literature_guide.md`](literature_guide.md) |

---

*Last updated: 2026-03-23.*
