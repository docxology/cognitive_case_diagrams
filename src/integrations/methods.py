"""Bounded, schema-validated handlers over existing project methods.

Each handler is a thin adapter: it converts validated JSON input into the
project's validated numerical inputs, calls one existing public method, and
packs the result into a pydantic model whose fields are finite floats. The
wrapped methods keep their own semantic validation (probability sums,
stochastic rows, matrix contracts) and raise ``ValueError`` with the project's
messages; the server maps those onto explicit MCP tool errors.

Handlers never execute supplied code, never write files, and never touch the
network. Annotations are honest: every tool is read-only, non-destructive,
idempotent, and closed-world.
"""

from __future__ import annotations

import inspect
from collections.abc import Sequence
import math
from dataclasses import dataclass
from typing import Annotated, Any, Literal

import numpy as np
from pydantic import BaseModel, Field, FiniteFloat

from ..case_systems.case_category import CaseRole
from ..cognitive.action_selection import expected_free_energy
from ..cognitive.belief import CaseDiagramBelief
from ..cognitive.belief_updating import sequential_belief_update, update_belief
from ..cognitive.free_energy import kl_divergence, variational_free_energy
from ..daif.core import push_forward_return
from ..daif.inference import (
    distributional_case_assignment,
    expected_information_gain,
    variational_message_passing,
)
from ..daif.metrics import convergence_diagnostics
from ..daif.quantile import quantile_td_update
from ..enriched_cat.enriched import EnrichedCategory
from ..numerics import probability_vector, stochastic_matrix
from ..quantum.quantum_case import case_probability, crisp_case_povm, semantic_state
from ..security.cognitive_security import CaseFrameValidator, injection_score
from ..topos_theory.topos import (
    Axiom,
    ClassifyingTopos,
    GeometricTheory,
    TheoryType,
    compare_theory_presentations,
)
from .artifacts import ArtifactIndex
from .experiments import summarize_variables
from .registry import (
    CASE_ROLE_NAMES,
    MAX_ARTIFACT_ENTRIES,
    MAX_EXPERIMENT_VARIABLES,
    MAX_FRAME_ASSIGNMENTS,
    MAX_MATRIX_DIM,
    MAX_NAME_LENGTH,
    MAX_OBSERVATIONS,
    MAX_QUANTILES,
    MAX_STEPS,
    MAX_VECTOR_LENGTH,
    check_length,
)

FiniteVector = Annotated[
    list[FiniteFloat], Field(min_length=1, max_length=MAX_VECTOR_LENGTH)
]
FiniteMatrix = Annotated[
    list[Annotated[list[FiniteFloat], Field(min_length=1, max_length=MAX_MATRIX_DIM)]], Field(min_length=1, max_length=MAX_MATRIX_DIM)
]
RoleName = Literal[
    "NOM", "ACC", "GEN", "DAT", "INS", "LOC", "ABL", "VOC",
    "ERG", "ABS", "S", "A", "P",
]
RoleList = Annotated[list[RoleName], Field(min_length=1, max_length=len(CASE_ROLE_NAMES))]
UnitFloat = Annotated[float, Field(allow_inf_nan=False)]
Gamma = Annotated[float, Field(ge=0.0, le=1.0, allow_inf_nan=False)]
ShortName = Annotated[str, Field(min_length=1, max_length=MAX_NAME_LENGTH)]

_ROLE_MEMBERS = list(CaseRole)
CASE_ROLES_BY_NAME: dict[str, CaseRole] = {role.name: role for role in _ROLE_MEMBERS}


class ScalarResult(BaseModel):
    value: FiniteFloat
    note: str | None = None


class BeliefUpdateResult(BaseModel):
    role_names: list[str]
    posterior: list[FiniteFloat]
    entropy_nats: FiniteFloat
    most_likely_role: str


class SequentialBeliefResult(BaseModel):
    role_names: list[str]
    posteriors: list[list[FiniteFloat]]
    entropies_nats: list[FiniteFloat]
    most_likely_roles: list[str]


class ScoreDistributionResult(BaseModel):
    mean: FiniteFloat
    variance: FiniteFloat
    std: FiniteFloat
    quantiles: list[FiniteFloat]
    quantile_levels: list[FiniteFloat]
    note: str | None = None


class DistributionalFilteringResult(BaseModel):
    role_names: list[str]
    posterior: list[FiniteFloat]
    fe_trajectory: list[FiniteFloat]
    convergence_iteration: int
    converged: bool
    return_distribution: ScoreDistributionResult | None = None


class QuantileUpdateResult(BaseModel):
    updated_quantiles: list[FiniteFloat]


class MessagePassingResult(BaseModel):
    probabilities: list[FiniteFloat]
    posterior_precision: list[FiniteFloat]
    note: str | None = None


class InformationGainResult(BaseModel):
    per_observation: list[FiniteFloat]
    total: FiniteFloat
    note: str | None = None


class PovmAssignmentResult(BaseModel):
    role_names: list[str]
    probabilities: list[FiniteFloat]
    note: str | None = None


class ViolationEntry(BaseModel):
    source: str
    target: str
    violation_type: str
    severity: FiniteFloat
    description: str


class FrameViolationResult(BaseModel):
    violations: list[ViolationEntry]
    injection_score: FiniteFloat
    note: str | None = None


class AxiomSpec(BaseModel):
    name: ShortName
    antecedent: ShortName
    consequent: ShortName
    sort_variables: Annotated[list[ShortName], Field(max_length=8)] = []


class PresentationSpec(BaseModel):
    name: ShortName
    sorts: Annotated[list[ShortName], Field(max_length=MAX_MATRIX_DIM * 2)]
    relations: Annotated[
        dict[ShortName, Annotated[list[ShortName], Field(max_length=8)]],
        Field(max_length=MAX_MATRIX_DIM * 2),
    ]
    axioms: Annotated[list[AxiomSpec], Field(max_length=MAX_MATRIX_DIM * 2)] = []


class PresentationComparisonResult(BaseModel):
    not_ruled_out: bool
    differences: list[str]
    signature_a: list[int]
    signature_b: list[int]
    note: str | None = None


class MagnitudeResult(BaseModel):
    magnitude: FiniteFloat
    magnitude_deficit: FiniteFloat
    role_count: int
    composition_violations: int
    composition_total: int
    note: str | None = None


class ConvergenceResult(BaseModel):
    monotone: bool
    total_reduction: FiniteFloat
    relative_reduction_pct: FiniteFloat
    n_iterations: int
    converged: bool
    fe_range: Annotated[list[FiniteFloat], Field(min_length=2, max_length=2)]
    mean_step_size: FiniteFloat
    final_delta: FiniteFloat


class VariableEntry(BaseModel):
    identifier: str
    value: FiniteFloat
    unit: str
    ci_low: FiniteFloat | None = None
    ci_high: FiniteFloat | None = None
    confidence_level: FiniteFloat
    sample_unit: str
    interpretation: str


class ExperimentVariablesResult(BaseModel):
    schema_version: str
    config_sha256: str
    seed: int | None = None
    numpy_version: str | None = None
    variable_count: int
    truncated: bool
    variables: list[VariableEntry]


class ArtifactEntry(BaseModel):
    path: str
    uri: str
    mime_type: str
    size_bytes: int


class ArtifactListResult(BaseModel):
    available: bool
    reason: str | None = None
    root: str
    count: int
    truncated: bool
    artifacts: list[ArtifactEntry]


def _roles_from_names(role_names: Sequence[str]) -> list[CaseRole]:
    if len(set(role_names)) != len(role_names):
        raise ValueError("role_names must be unique")
    return [CASE_ROLES_BY_NAME[name] for name in role_names]


def _square_matrix(values: list[list[float]], n: int, name: str) -> list[list[float]]:
    if len(values) != n:
        raise ValueError(f"{name} must have {n} rows to match {n} probabilities")
    for index, row in enumerate(values):
        if len(row) != n:
            raise ValueError(
                f"{name} row {index} has {len(row)} entries; expected {n}"
            )
    return values


def _finite(value: float, name: str) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{name} is not finite; refusing to emit nonfinite JSON")
    return value


def update_case_belief(
    role_names: RoleList,
    prior_probabilities: FiniteVector,
    likelihood: FiniteVector,
) -> BeliefUpdateResult:
    """Normalize a supplied prior times a supplied likelihood over case roles.

    The likelihood is caller-supplied synthetic evidence; no sentence is
    parsed. Role names use CaseRole enum members (NOM..P).
    """
    roles = _roles_from_names(role_names)
    if len(prior_probabilities) != len(roles) or len(likelihood) != len(roles):
        raise ValueError(
            f"prior_probabilities and likelihood must both have {len(roles)} entries"
        )
    prior = CaseDiagramBelief(
        roles=roles,
        probabilities=probability_vector(prior_probabilities, "prior_probabilities"),
    )
    posterior = update_belief(prior, np.asarray(likelihood, dtype=np.float64))
    return BeliefUpdateResult(
        role_names=list(role_names),
        posterior=[_finite(float(p), "posterior") for p in posterior.probabilities],
        entropy_nats=posterior.entropy(),
        most_likely_role=posterior.most_likely_role().name,
    )


def sequential_case_belief_update(
    role_names: RoleList,
    prior_probabilities: FiniteVector,
    likelihood_sequence: Annotated[
        list[FiniteVector], Field(min_length=1, max_length=MAX_STEPS)
    ],
) -> SequentialBeliefResult:
    """Apply one supplied likelihood vector per step and return the trajectory.

    Each likelihood is consumed exactly once; the sequence is caller-designed
    synthetic evidence.
    """
    roles = _roles_from_names(role_names)
    if len(prior_probabilities) != len(roles):
        raise ValueError(f"prior_probabilities must have {len(roles)} entries")
    for index, likelihood in enumerate(likelihood_sequence):
        if len(likelihood) != len(roles):
            raise ValueError(
                f"likelihood_sequence[{index}] has {len(likelihood)} entries; "
                f"expected {len(roles)}"
            )
    prior = CaseDiagramBelief(
        roles=roles,
        probabilities=probability_vector(prior_probabilities, "prior_probabilities"),
    )
    trajectory = sequential_belief_update(
        prior, [np.asarray(l, dtype=np.float64) for l in likelihood_sequence]
    )
    return SequentialBeliefResult(
        role_names=list(role_names),
        posteriors=[
            [_finite(float(p), "posterior") for p in state.probabilities]
            for state in trajectory
        ],
        entropies_nats=[state.entropy() for state in trajectory],
        most_likely_roles=[state.most_likely_role().name for state in trajectory],
    )


def kl_divergence_tool(
    q_probabilities: FiniteVector,
    p_probabilities: FiniteVector,
) -> ScalarResult:
    """KL(q||p) between two normalized finite distributions.

    Reports an explicit error instead of nonfinite JSON when p has zero mass
    where q is positive.
    """
    value = kl_divergence(
        probability_vector(q_probabilities, "q_probabilities"),
        probability_vector(p_probabilities, "p_probabilities"),
    )
    return ScalarResult(
        value=_finite(value, "kl_divergence"),
        note="infinite when p has zero mass where q is positive",
    )


def variational_free_energy_tool(
    q_probabilities: FiniteVector,
    log_likelihood: FiniteVector,
    log_prior: FiniteVector,
) -> ScalarResult:
    """Fixed-model variational free energy from supplied log vectors.

    Not a learned or inferred generative model; all inputs are caller-supplied.
    """
    if len(log_likelihood) != len(q_probabilities) or len(log_prior) != len(q_probabilities):
        raise ValueError(
            f"log_likelihood and log_prior must both have {len(q_probabilities)} entries"
        )
    value = variational_free_energy(
        probability_vector(q_probabilities, "q_probabilities"),
        np.asarray(log_likelihood, dtype=np.float64),
        np.asarray(log_prior, dtype=np.float64),
    )
    return ScalarResult(value=_finite(value, "variational_free_energy"))


def expected_free_energy_score(
    q_probabilities: FiniteVector,
    log_likelihood: FiniteVector,
    epistemic_value: FiniteVector,
    pragmatic_value: FiniteVector,
    gamma: UnitFloat = 1.0,
) -> ScalarResult:
    """Caller-defined score -q.l - q.e - gamma*q.u over supplied vectors.

    This is a policy-score arithmetic helper, not a derived expected free
    energy; the caller is responsible for scaling and interpretation.
    """
    size = len(q_probabilities)
    if any(len(v) != size for v in (log_likelihood, epistemic_value, pragmatic_value)):
        raise ValueError(
            f"log_likelihood, epistemic_value, and pragmatic_value must all have {size} entries"
        )
    value = expected_free_energy(
        probability_vector(q_probabilities, "q_probabilities"),
        np.asarray(log_likelihood, dtype=np.float64),
        np.asarray(epistemic_value, dtype=np.float64),
        np.asarray(pragmatic_value, dtype=np.float64),
        gamma,
    )
    return ScalarResult(value=_finite(value, "expected_free_energy"))


def push_forward_score_distribution(
    role_probabilities: FiniteVector,
    transition_matrix: FiniteMatrix,
    reward_vector: FiniteVector,
    gamma: Gamma = 0.99,
    n_quantiles: Annotated[int, Field(ge=2, le=MAX_QUANTILES)] = 51,
) -> ScoreDistributionResult:
    """Law of dimensionless scores R + gamma*T.T@q with mass q_i per role.

    Positions index roles; role labels are not used. This is a heuristic score
    distribution, not a Bellman backup or discounted cumulative reward.
    """
    n = len(role_probabilities)
    probabilities = probability_vector(role_probabilities, "role_probabilities")
    matrix = stochastic_matrix(
        np.asarray(_square_matrix(transition_matrix, n, "transition_matrix"), dtype=np.float64),
        n,
    )
    if len(reward_vector) != n:
        raise ValueError(f"reward_vector must have {n} entries to match probabilities")
    # Roles are position placeholders; the distribution is over index space.
    if n > len(_ROLE_MEMBERS):
        raise ValueError(f"role_probabilities supports at most {len(_ROLE_MEMBERS)} case roles")
    placeholder_roles = _ROLE_MEMBERS[:n]
    belief = CaseDiagramBelief(roles=placeholder_roles, probabilities=probabilities)
    result = push_forward_return(belief, matrix, np.asarray(reward_vector, dtype=np.float64), gamma, n_quantiles)
    return ScoreDistributionResult(
        mean=_finite(result.mean, "mean"),
        variance=_finite(result.variance, "variance"),
        std=_finite(result.std(), "std"),
        quantiles=[_finite(float(q), "quantiles") for q in result.quantiles],
        quantile_levels=[float(t) for t in result.quantile_levels],
        note="dimensionless score law; not a Bellman return backup",
    )


def distributional_case_filtering(
    role_names: RoleList,
    prior_probabilities: FiniteVector,
    observation_likelihoods: FiniteVector,
    n_iterations: Annotated[int, Field(ge=1, le=MAX_STEPS)] = 10,
    convergence_threshold: UnitFloat = 1e-6,
    n_quantiles: Annotated[int, Field(ge=2, le=MAX_QUANTILES)] = 51,
) -> DistributionalFilteringResult:
    """Repeatedly assimilate one supplied likelihood through Markov filter steps.

    Every iteration reuses the same evidence; one iteration models one
    observation. Convergence of the loop is not evidence about the world.
    """
    roles = _roles_from_names(role_names)
    if len(prior_probabilities) != len(roles) or len(observation_likelihoods) != len(roles):
        raise ValueError(
            f"prior_probabilities and observation_likelihoods must both have {len(roles)} entries"
        )
    prior = CaseDiagramBelief(
        roles=roles,
        probabilities=probability_vector(prior_probabilities, "prior_probabilities"),
    )
    result = distributional_case_assignment(
        prior,
        np.asarray(observation_likelihoods, dtype=np.float64),
        n_iterations=n_iterations,
        convergence_threshold=convergence_threshold,
        n_quantiles=n_quantiles,
    )
    distribution = result.return_distribution
    return DistributionalFilteringResult(
        role_names=list(role_names),
        posterior=[_finite(float(p), "posterior") for p in result.belief.probabilities],
        fe_trajectory=[_finite(float(f), "fe_trajectory") for f in result.fe_trajectory],
        convergence_iteration=result.convergence_iteration,
        converged=result.converged,
        return_distribution=(
            ScoreDistributionResult(
                mean=_finite(distribution.mean, "mean"),
                variance=_finite(distribution.variance, "variance"),
                std=_finite(distribution.std(), "std"),
                quantiles=[_finite(float(q), "quantiles") for q in distribution.quantiles],
                quantile_levels=[float(t) for t in distribution.quantile_levels],
            )
            if distribution is not None
            else None
        ),
    )


def quantile_td_update_tool(
    current_quantiles: FiniteVector,
    target_quantiles: FiniteVector,
    learning_rate: Annotated[float, Field(gt=0.0, le=1.0, allow_inf_nan=False)] = 0.1,
    kappa: Annotated[float, Field(gt=0.0, allow_inf_nan=False)] = 1.0,
) -> QuantileUpdateResult:
    """Pairwise quantile Huber update averaged over all target samples.

    Current and target counts may differ; the Huber loss is unnormalized
    (coordinate learning-rate convention).
    """
    updated = quantile_td_update(
        np.asarray(current_quantiles, dtype=np.float64),
        np.asarray(target_quantiles, dtype=np.float64),
        learning_rate=learning_rate,
        kappa=kappa,
    )
    return QuantileUpdateResult(
        updated_quantiles=[_finite(float(q), "updated_quantiles") for q in updated]
    )


def variational_message_update(
    observations: FiniteVector,
    prior_precision: FiniteVector,
    likelihood_precision: FiniteVector,
    n_iterations: Annotated[int, Field(ge=1, le=MAX_STEPS * 2)] = 16,
) -> MessagePassingResult:
    """Single-factor softmax of precision-weighted evidence with bookkeeping.

    The implicit prior is uniform; prior precision affects only returned
    bookkeeping. This is not general factor-graph or loopy inference.
    """
    size = len(observations)
    q, posterior_precision = variational_message_passing(
        np.asarray(observations, dtype=np.float64),
        np.asarray(prior_precision, dtype=np.float64),
        np.asarray(likelihood_precision, dtype=np.float64),
        n_iterations=n_iterations,
    )
    if len(prior_precision) not in (1, size) or len(likelihood_precision) not in (1, size):
        raise ValueError(
            f"precisions must have length {size} (or 1 to broadcast)"
        )
    return MessagePassingResult(
        probabilities=[_finite(float(p), "probabilities") for p in q],
        posterior_precision=[_finite(float(l), "posterior_precision") for l in posterior_precision],
        note="uniform-prior softmax; not general factor-graph inference",
    )


def expected_information_gain_tool(
    role_names: RoleList,
    prior_probabilities: FiniteVector,
    candidate_observations: Annotated[
        list[FiniteVector], Field(min_length=1, max_length=MAX_OBSERVATIONS)
    ],
) -> InformationGainResult:
    """Per-observation p(o)*KL(posterior||prior) contributions for candidates.

    The sum is mutual information only when columns sum to one over a
    complete observation alphabet; otherwise these are design scores.
    """
    roles = _roles_from_names(role_names)
    if len(prior_probabilities) != len(roles):
        raise ValueError(f"prior_probabilities must have {len(roles)} entries")
    for index, row in enumerate(candidate_observations):
        if len(row) != len(roles):
            raise ValueError(
                f"candidate_observations[{index}] has {len(row)} entries; expected {len(roles)}"
            )
    prior = CaseDiagramBelief(
        roles=roles,
        probabilities=probability_vector(prior_probabilities, "prior_probabilities"),
    )
    contributions = expected_information_gain(prior, np.asarray(candidate_observations, dtype=np.float64))
    values = [float(c) for c in contributions]
    return InformationGainResult(
        per_observation=[_finite(v, "per_observation") for v in values],
        total=_finite(sum(values), "total"),
        note="sum equals mutual information only for a normalized complete alphabet",
    )


def case_povm_assignment(
    role_names: RoleList,
    weights: FiniteVector,
) -> PovmAssignmentResult:
    """Trace-rule probabilities for orthogonal projectors on a diagonal state.

    The state is the classical diagonal mixture rho = diag(normalized weights);
    the canonical construction has a classical interpretation and shows no
    interference. No hardware or cognition claim is implemented.
    """
    roles = _roles_from_names(role_names)
    if len(weights) != len(roles):
        raise ValueError(f"weights must have {len(roles)} entries")
    weight_array = np.asarray(weights, dtype=np.float64)
    if np.any(weight_array < 0):
        raise ValueError("weights must be non-negative")
    if weight_array.sum() <= 0:
        raise ValueError("weights must sum to a positive value")
    povm = crisp_case_povm(roles)
    density = semantic_state(dict(zip(roles, weight_array)), roles=roles)
    probabilities = [case_probability(povm.elements[role], density) for role in roles]
    return PovmAssignmentResult(
        role_names=list(role_names),
        probabilities=[_finite(p, "probabilities") for p in probabilities],
        note="orthogonal projectors on a diagonal mixture; classical outcome probabilities",
    )


def case_frame_violation_check(
    assignments: Annotated[
        dict[ShortName, RoleName], Field(max_length=MAX_FRAME_ASSIGNMENTS)
    ],
) -> FrameViolationResult:
    """Check supplied entity-to-role assignments against the standard category.

    Pairwise policy checks in either direction plus the severity aggregate.
    Supplied-label policy only; not an operational security boundary.
    """
    validator = CaseFrameValidator()
    violations = validator.validate_assignment(
        {entity: CASE_ROLES_BY_NAME[role] for entity, role in assignments.items()}
    )
    score = injection_score(violations)
    return FrameViolationResult(
        violations=[
            ViolationEntry(
                source=v.source.name,
                target=v.target.name,
                violation_type=v.violation_type,
                severity=v.severity,
                description=v.description,
            )
            for v in violations
        ],
        injection_score=_finite(float(score), "injection_score"),
        note="supplied-label policy checks; no authenticated execution boundary",
    )


def compare_theory_presentations_tool(
    theory_a: PresentationSpec,
    theory_b: PresentationSpec,
) -> PresentationComparisonResult:
    """Compare signature counts and arity spectra of two finite presentations.

    Counts are presentation-dependent: a match is neither necessary nor
    sufficient for Morita equivalence, and no axiom semantics are compared.
    """
    def build(spec: PresentationSpec) -> ClassifyingTopos:
        theory = GeometricTheory(
            name=spec.name,
            theory_type=TheoryType.TYPOLOGICAL,
            sorts=list(spec.sorts),
            relation_symbols={k: tuple(v) for k, v in spec.relations.items()},
            axioms=[
                Axiom(
                    name=a.name,
                    antecedent=a.antecedent,
                    consequent=a.consequent,
                    sort_variables=list(a.sort_variables),
                )
                for a in spec.axioms
            ],
        )
        return ClassifyingTopos(theory=theory)

    not_ruled_out, differences = compare_theory_presentations(build(theory_a), build(theory_b))
    signature_a = list(build(theory_a).theory.signature_invariant())
    signature_b = list(build(theory_b).theory.signature_invariant())
    return PresentationComparisonResult(
        not_ruled_out=not_ruled_out,
        differences=differences,
        signature_a=signature_a,
        signature_b=signature_b,
        note="presentation counts only; not a Morita-equivalence decision",
    )


def enriched_category_magnitude(
    role_names: RoleList,
    proximity_matrix: FiniteMatrix,
) -> MagnitudeResult:
    """Magnitude of a supplied [0,1] proximity matrix over case roles.

    Identity axiom C(A,A)=1 and bounds are validated; magnitude uses inverse
    sums or a residual-validated pseudoinverse. This is a matrix statistic,
    not a linguistic-information measure.
    """
    roles = _roles_from_names(role_names)
    n = len(roles)
    matrix = np.asarray(_square_matrix(proximity_matrix, n, "proximity_matrix"), dtype=np.float64)
    category = EnrichedCategory(name="supplied", roles=roles, proximity_matrix=matrix)
    check = category.full_composition_check()
    return MagnitudeResult(
        magnitude=_finite(category.magnitude(), "magnitude"),
        magnitude_deficit=_finite(category.magnitude_deficit(), "magnitude_deficit"),
        role_count=n,
        composition_violations=len(check["violations"]),
        composition_total=check["total"],
        note="supplied synthetic matrix; not a linguistic-information measure",
    )


def convergence_diagnostics_tool(
    fe_trajectory: FiniteVector,
    min_iterations: Annotated[int, Field(ge=2, le=8)] = 3,
) -> ConvergenceResult:
    """Change statistics over a supplied free-energy trajectory.

    A small final change is a reported statistic, not proof of a unique fixed
    point.
    """
    if len(fe_trajectory) < min_iterations:
        raise ValueError(
            f"fe_trajectory length ({len(fe_trajectory)}) < min_iterations ({min_iterations})"
        )
    diag = convergence_diagnostics(list(fe_trajectory), min_iterations=min_iterations)
    return ConvergenceResult(
        monotone=bool(diag["monotone"]),
        total_reduction=_finite(float(diag["total_reduction"]), "total_reduction"),
        relative_reduction_pct=_finite(float(diag["relative_reduction_pct"]), "relative_reduction_pct"),
        n_iterations=int(diag["n_iterations"]),
        converged=bool(diag["converged"]),
        fe_range=[_finite(float(x), "fe_range") for x in diag["fe_range"]],
        mean_step_size=_finite(float(diag["mean_step_size"]), "mean_step_size"),
        final_delta=_finite(float(diag["final_delta"]), "final_delta"),
    )


def list_experiment_variables(
    limit: Annotated[int, Field(ge=1, le=MAX_EXPERIMENT_VARIABLES)] = 128,
) -> ExperimentVariablesResult:
    """Project the stable variables registry of the canonical experiments file.

    Reads output/experiments/results.json under the contained
    artifact root. Absence of the file is reported as an explicit error: the
    results are written by the experiments stage, never synthesized here.
    """
    summary = summarize_variables(ArtifactIndex().root, limit=limit)
    return ExperimentVariablesResult(**summary)


def list_artifacts_tool() -> ArtifactListResult:
    """Enumerate contained files under the artifact root (default output/).

    Traversal, symlink escapes, and oversize reads are rejected at read time.
    """
    entries = ArtifactIndex().entries()
    check_length(entries["artifacts"], "artifacts", MAX_ARTIFACT_ENTRIES)
    return ArtifactListResult(
        available=entries["available"],
        reason=entries.get("reason"),
        root=entries["root"],
        count=entries["count"],
        truncated=entries["truncated"],
        artifacts=[ArtifactEntry(**entry) for entry in entries["artifacts"]],
    )


@dataclass(frozen=True)
class ToolSpec:
    """A bounded tool: name, honest description, and the handler to call."""

    name: str
    description: str
    handler: Any


def _spec(handler: Any) -> ToolSpec:
    return ToolSpec(name=handler.__name__.removesuffix("_tool"), description=inspect.getdoc(handler) or "", handler=handler)


TOOL_SPECS: list[ToolSpec] = [
    _spec(update_case_belief),
    _spec(sequential_case_belief_update),
    _spec(kl_divergence_tool),
    _spec(variational_free_energy_tool),
    _spec(expected_free_energy_score),
    _spec(push_forward_score_distribution),
    _spec(distributional_case_filtering),
    _spec(quantile_td_update_tool),
    _spec(variational_message_update),
    _spec(expected_information_gain_tool),
    _spec(case_povm_assignment),
    _spec(case_frame_violation_check),
    _spec(compare_theory_presentations_tool),
    _spec(enriched_category_magnitude),
    _spec(convergence_diagnostics_tool),
    _spec(list_experiment_variables),
    _spec(list_artifacts_tool),
]

__all__ = ["TOOL_SPECS", "ToolSpec"]
