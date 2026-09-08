"""Capability and claim metadata for the MCP server.

``docs/claim_ledger.md`` and ``docs/method_contracts.md`` are canonical; the
constants below are a packaged snapshot for wheel installs where ``docs/`` is
absent, and for agents that want the honest status of every advertised claim
without reading the repository. Keep them in sync when the canonical documents
change. Quality metadata is never synthesized: the ``quality_receipt`` section
embeds ``src.release_validation.validate_quality_receipt`` output when the
receipt is current, and reports its explicit status otherwise.
"""

from __future__ import annotations

from importlib.metadata import version, PackageNotFoundError

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]
from pathlib import Path
from typing import Any

SERVER_NAME = "cognitive-case-diagrams"

SERVER_INSTRUCTIONS = (
    "Bounded, schema-validated wrappers over the cognitive_case_diagrams "
    "synthetic numerical examples (case-role categories, Bayesian belief "
    "updates, distributional active-inference utilities, quantum case POVMs, "
    "role-policy checks, theory-presentation profiles, enriched magnitudes), "
    "plus synthetic experiment results and contained project artifacts. All "
    "canonical numerical inputs are synthetic; every result is an explicit "
    "model quantity, not an empirical measurement or a security boundary. "
    "All tools are read-only computations. See the ccd://capabilities and "
    "ccd://claims resources for the claim ledger and method contracts."
)

CLAIMS: list[dict[str, str]] = [
    {
        "claim": "Selected pregroup reductions execute",
        "status": "verified",
        "evidence": "DisCoPy constructors and grammar tests; hand-assigned types",
    },
    {
        "claim": "Finite Bayesian updates implement normalization",
        "status": "verified",
        "evidence": "Analytic posterior and impossible-evidence tests",
    },
    {
        "claim": "Quantile updates use all target samples",
        "status": "verified",
        "evidence": "Two-point analytic QR counterexample and regression suite",
    },
    {
        "claim": "C51 helper preserves clipped tail mass",
        "status": "verified",
        "evidence": "Method/function parity and endpoint examples",
    },
    {
        "claim": "Supplied POVMs and states satisfy matrix contracts",
        "status": "verified",
        "evidence": "Hermitian, PSD, completeness, trace and malformed-input tests",
    },
    {
        "claim": "Standard role matrix is a valid enrichment",
        "status": "unsupported for raw input",
        "evidence": "Raw composition failure retained; explicit closure added",
    },
    {
        "claim": "Matrix magnitude measures linguistic information",
        "status": "partially_supported",
        "evidence": "Matrix statistic implemented; linguistic interpretation untested",
    },
    {
        "claim": "Theory profiles decide Morita equivalence",
        "status": "unsupported",
        "evidence": "Counts can change under equivalent presentations; transfer now unavailable",
    },
    {
        "claim": "All case frameworks have a common classifying topos",
        "status": "unsupported",
        "evidence": "No equivalence witness, sites, or sheaf construction",
    },
    {
        "claim": "Local DAIF package reproduces full DAIF / Bellman control",
        "status": "unsupported",
        "evidence": "Exact dimensionless score contract replaces the former claim",
    },
    {
        "claim": "VMP/Bethe names imply general factor-graph inference",
        "status": "unsupported",
        "evidence": "Single-factor update and shared-distribution score documented",
    },
    {
        "claim": "Diagrams improve cognition or predict EEG amplitudes",
        "status": "ambiguous / proposed",
        "evidence": "Requires controlled human data and physiological calibration",
    },
    {
        "claim": "Quantum figure exhibits interference",
        "status": "unsupported",
        "evidence": "Canonical diagonal mixture and projectors have a classical interpretation",
    },
    {
        "claim": "Case labels secure real agent execution",
        "status": "unsupported",
        "evidence": "Supplied-label policy only; no authenticated execution boundary",
    },
]

CANONICAL_SOURCES = {
    "claim_ledger": "docs/claim_ledger.md",
    "method_contracts": "docs/method_contracts.md",
    "api_reference": "docs/api_reference.md",
    "agent_integrations": "docs/agent_integrations.md",
}

TOOL_CONTRACT_NOTES: list[dict[str, str]] = [
    {
        "tool": "update_case_belief",
        "implements": "src.cognitive.belief_updating.update_belief",
        "contract": "Normalized prior times supplied likelihood",
        "limit": "Likelihood is supplied synthetic evidence; no sentence parsing",
    },
    {
        "tool": "sequential_case_belief_update",
        "implements": "src.cognitive.belief_updating.sequential_belief_update",
        "contract": "Repeats update_belief over a supplied observation sequence",
        "limit": "Each likelihood vector is consumed once; sequence is caller-designed",
    },
    {
        "tool": "kl_divergence",
        "implements": "src.cognitive.free_energy.kl_divergence",
        "contract": "KL(q||p) for finite normalized vectors",
        "limit": "Infinite when p has zero mass where q is positive (reported as an error)",
    },
    {
        "tool": "variational_free_energy",
        "implements": "src.cognitive.free_energy.variational_free_energy",
        "contract": "Fixed-model variational free energy from supplied logs",
        "limit": "Not a learned or inferred generative model",
    },
    {
        "tool": "expected_free_energy_score",
        "implements": "src.cognitive.action_selection.expected_free_energy",
        "contract": "Caller-defined -q.l - q.e - gamma*q.u score",
        "limit": "No optimality theorem; units must be scaled by the caller",
    },
    {
        "tool": "push_forward_score_distribution",
        "implements": "src.daif.core.push_forward_return",
        "contract": "Law of dimensionless scores R + gamma*T.T@q with mass q_i",
        "limit": "Not a Bellman backup; not a discounted cumulative reward",
    },
    {
        "tool": "distributional_case_filtering",
        "implements": "src.daif.inference.distributional_case_assignment",
        "contract": "Repeated likelihood assimilation with Markov prediction",
        "limit": "Iterations reuse the same evidence; one iteration models one observation",
    },
    {
        "tool": "quantile_td_update",
        "implements": "src.daif.quantile.quantile_td_update",
        "contract": "Pairwise quantile Huber update averaged over target samples",
        "limit": "Huber loss is unnormalized; not a Bellman return",
    },
    {
        "tool": "variational_message_update",
        "implements": "src.daif.inference.variational_message_passing",
        "contract": "Single-factor softmax of precision-weighted evidence",
        "limit": "Not general factor-graph inference; prior precision is bookkeeping only",
    },
    {
        "tool": "expected_information_gain",
        "implements": "src.daif.inference.expected_information_gain",
        "contract": "Per-observation p(o)*KL(posterior||prior) contributions",
        "limit": "Sum is mutual information only for a normalized complete observation alphabet",
    },
    {
        "tool": "case_povm_assignment",
        "implements": "src.quantum.quantum_case (crisp_case_povm, semantic_state, case_probability)",
        "contract": "Trace rule probabilities for orthogonal projectors on a diagonal state",
        "limit": "Classical outcome probabilities; no interference, hardware, or cognition claim",
    },
    {
        "tool": "case_frame_violation_check",
        "implements": "src.security.cognitive_security (CaseFrameValidator, injection_score)",
        "contract": "Pairwise type checks of supplied role assignments plus severity aggregate",
        "limit": "Supplied-label policy only; not an operational security boundary",
    },
    {
        "tool": "compare_theory_presentations",
        "implements": "src.topos_theory.topos.compare_theory_presentations",
        "contract": "Compares signature counts and arity spectra of two presentations",
        "limit": "Match is neither necessary nor sufficient for Morita equivalence",
    },
    {
        "tool": "enriched_category_magnitude",
        "implements": "src.enriched_cat.enriched (EnrichedCategory.magnitude)",
        "contract": "Inverse-sum or residual-validated pseudoinverse magnitude",
        "limit": "Matrix statistic; no unconditional entropy, redundancy, or security meaning",
    },
    {
        "tool": "convergence_diagnostics",
        "implements": "src.daif.metrics.convergence_diagnostics",
        "contract": "Change statistics over a supplied free-energy trajectory",
        "limit": "A small final change is not proof of a unique fixed point",
    },
    {
        "tool": "list_experiment_variables",
        "implements": "src.experiments.write_results output (read-only)",
        "contract": "Projects the stable variables registry of the canonical results file",
        "limit": "Values are synthetic-computation outputs; absence is reported, never synthesized",
    },
    {
        "tool": "list_artifacts",
        "implements": "src.integrations.artifacts.ArtifactIndex",
        "contract": "Enumerates contained files under the artifact root",
        "limit": "Derived output/ artifacts only; traversal, symlinks, and oversize reads are rejected",
    },
]


def project_version(project_root: Path | None = None) -> str:
    """Return the declared project version without importing heavy modules."""
    root = project_root if project_root is not None else _default_project_root()
    try:
        with (root / "pyproject.toml").open("rb") as handle:
            return str(tomllib.load(handle)["project"]["version"])
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        try:
            return version("cognitive_case_diagrams")
        except PackageNotFoundError:
            return "unknown"


def _default_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def quality_receipt_summary(project_root: Path | None = None) -> dict[str, Any]:
    """Embed the validated quality receipt, or its explicit failure status.

    The receipt is never faked: missing files report ``missing``, stale or
    inconsistent receipts report ``stale_or_invalid`` with the validator's
    message, and only a fully validated receipt is embedded — under a
    ``receipt`` key whose own ``status`` field is removed so the contract
    vocabulary stays the only ``status`` in this section. The state mapping
    is shared with ``src.evidence_status`` so the MCP and CLI surfaces
    cannot drift.
    """
    from src.evidence_status import quality_stage
    from src.release_validation import validate_quality_receipt

    root = project_root if project_root is not None else _default_project_root()
    stage = quality_stage(root)
    if stage["state"] == "validated":
        receipt: dict[str, Any] = validate_quality_receipt(root)
        payload = {key: value for key, value in receipt.items() if key != "status"}
        return {"status": "validated", "receipt": payload}
    if stage["state"] == "missing":
        return {"status": "missing", "detail": stage["detail"]}
    return {"status": "stale_or_invalid", "detail": stage["detail"]}


def capability_metadata(project_root: Path | None = None) -> dict[str, Any]:
    """Assemble the ccd://capabilities payload."""
    root = project_root if project_root is not None else _default_project_root()
    return {
        "server": SERVER_NAME,
        "project_revision": project_version(root),
        "project_version": project_version(root),
        "scope": (
            "Synthetic numerical examples and derived artifacts only; not a "
            "linguistic parser, topos bridge, distributional learner, EEG "
            "model, or operational security system."
        ),
        "security_model": {
            "tool_inputs": "bounded, schema-validated, finite JSON",
            "tool_outputs": "finite JSON via validated pydantic models",
            "execution": "no supplied code, commands, or queries are executed",
            "filesystem": (
                "reads confined to the contained artifact root "
                "(default output/; CCD_ARTIFACT_ROOT overrides for local runs)"
            ),
            "annotations": "all tools declare read-only, non-destructive, idempotent, closed-world",
        },
        "claims": CLAIMS,
        "tool_contracts": TOOL_CONTRACT_NOTES,
        "quality_receipt": quality_receipt_summary(root),
        "canonical_sources": CANONICAL_SOURCES,
    }
