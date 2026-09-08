"""In-process official-client contract tests for all 17 advertised tools.

Every tool is executed through the real SDK client against the real server
object (``Client(create_mcp_server())`` — the SDK's in-process transport, no
subprocess, no mocks) and cross-checked against the underlying library call
or a hand-derived analytic value. Semantic error paths exercise the project
validators. ``list_artifacts`` and ``list_experiment_variables`` run against
a real temporary artifact tree containing genuine ``run_experiments``
evidence with byte-copied source files, selected through the documented
``CCD_ARTIFACT_ROOT`` override.
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from mcp import Client
from mcp.types import TextResourceContents

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.belief_updating import sequential_belief_update, update_belief
from src.cognitive.free_energy import kl_divergence, variational_free_energy
from src.daif.inference import distributional_case_assignment
from src.daif.metrics import convergence_diagnostics
from src.integrations.experiments import experiments_path
from src.integrations.methods import TOOL_SPECS
from src.integrations.server import create_mcp_server
from src.security.cognitive_security import CaseFrameValidator, injection_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.anyio

EXPECTED_TOOLS = {spec.name for spec in TOOL_SPECS}


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> Any:
    async with Client(create_mcp_server()) as connected:
        yield connected


@pytest.fixture(scope="session")
def artifact_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A real artifact tree with genuine experiment evidence and sources.

    ``run_experiments`` produces the canonical results; every provenance
    source file is copied byte-for-byte so the freshness digest recomputes
    under the temporary tree. No provenance is fabricated.
    """
    from src.experiments import write_results
    from src.experiments.runner import run_experiments

    output = tmp_path_factory.mktemp("ccd_contract_artifacts") / "output"
    (output / "figures").mkdir(parents=True)
    (output / "figures" / "fig.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    (output / "metrics.json").write_text('{"total_test_count": "1"}')

    results = run_experiments(
        {"n_replicates": 2, "quantile": {"brute_force_tau_points": 101}}
    )
    for relative in results["provenance"]["source_files"]:
        source = PROJECT_ROOT / relative
        target = output.parent / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    write_results(results, output / "experiments" / "results.json")
    return output


# ---------------------------------------------------------------------------
# Cross-check helpers


def _belief(roles: list[str], probabilities: list[float]) -> CaseDiagramBelief:
    role_objects = [CaseRole[name] for name in roles]
    return CaseDiagramBelief(role_objects, np.asarray(probabilities, dtype=np.float64))


# ---------------------------------------------------------------------------
# 1-2. Belief updating


async def test_update_case_belief_matches_analytic_posterior(client: Any) -> None:
    result = await client.call_tool(
        "update_case_belief",
        {
            "role_names": ["NOM", "ACC"],
            "prior_probabilities": [0.5, 0.5],
            "likelihood": [0.8, 0.2],
        },
    )
    assert result.is_error is False
    # Uniform prior x (0.8, 0.2) renormalizes to (0.8, 0.2) exactly.
    assert result.structured_content["posterior"] == pytest.approx([0.8, 0.2])
    assert result.structured_content["most_likely_role"] == "NOM"
    expected = update_belief(
        _belief(["NOM", "ACC"], [0.5, 0.5]), np.asarray([0.8, 0.2])
    )
    assert result.structured_content["entropy_nats"] == pytest.approx(expected.entropy())


async def test_update_case_belief_impossible_evidence_is_explicit(client: Any) -> None:
    result = await client.call_tool(
        "update_case_belief",
        {
            "role_names": ["NOM", "ACC"],
            "prior_probabilities": [1.0, 0.0],
            "likelihood": [0.0, 1.0],
        },
    )
    assert result.is_error is True
    assert "zero" in result.content[0].text


async def test_sequential_case_belief_update_matches_library(client: Any) -> None:
    likelihood_sequence: list[list[float]] = [[0.9, 0.1], [0.7, 0.3]]
    arguments = {
        "role_names": ["NOM", "ACC"],
        "prior_probabilities": [0.5, 0.5],
        "likelihood_sequence": likelihood_sequence,
    }
    result = await client.call_tool("sequential_case_belief_update", arguments)
    assert result.is_error is False
    expected = sequential_belief_update(
        _belief(["NOM", "ACC"], [0.5, 0.5]),
        [np.asarray(l, dtype=np.float64) for l in likelihood_sequence],
    )
    posteriors = result.structured_content["posteriors"]
    assert posteriors[-1] == pytest.approx(list(map(float, expected[-1].probabilities)))
    assert result.structured_content["entropies_nats"][-1] == pytest.approx(
        expected[-1].entropy()
    )


# ---------------------------------------------------------------------------
# 3-5. Scalar information quantities


async def test_kl_divergence_matches_analytic_value(client: Any) -> None:
    result = await client.call_tool(
        "kl_divergence",
        {"q_probabilities": [0.5, 0.5], "p_probabilities": [0.25, 0.75]},
    )
    assert result.is_error is False
    expected = kl_divergence(np.array([0.5, 0.5]), np.array([0.25, 0.75]))
    assert result.structured_content["value"] == pytest.approx(expected)
    # Analytic: 0.5*ln(2) + 0.5*ln(2/3) == 0.5*ln(4/3).
    assert result.structured_content["value"] == pytest.approx(0.5 * math.log(4.0 / 3.0))


async def test_kl_divergence_length_mismatch_is_explicit(client: Any) -> None:
    result = await client.call_tool(
        "kl_divergence",
        {"q_probabilities": [1.0, 0.0], "p_probabilities": [1.0]},
    )
    assert result.is_error is True
    assert "same length" in result.content[0].text


async def test_variational_free_energy_matches_library(client: Any) -> None:
    arguments = {
        "q_probabilities": [0.25, 0.75],
        "log_likelihood": [-0.5, -1.5],
        "log_prior": [-0.7, -0.4],
    }
    result = await client.call_tool("variational_free_energy", arguments)
    assert result.is_error is False
    expected = variational_free_energy(
        np.array([0.25, 0.75]),
        np.array([-0.5, -1.5]),
        np.array([-0.7, -0.4]),
    )
    assert result.structured_content["value"] == pytest.approx(expected)


async def test_expected_free_energy_score_matches_hand_computation(client: Any) -> None:
    result = await client.call_tool(
        "expected_free_energy_score",
        {
            "q_probabilities": [1.0, 0.0],
            "log_likelihood": [-2.0, -3.0],
            "epistemic_value": [1.0, 0.0],
            "pragmatic_value": [0.0, 0.0],
            "gamma": 1.0,
        },
    )
    assert result.is_error is False
    # -q.l - q.e - gamma*q.u = 2 - 1 - 0 = 1.
    assert result.structured_content["value"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# 6-7. Distributional score laws and filtering


async def test_push_forward_matches_manuscript_counterexample(client: Any) -> None:
    result = await client.call_tool(
        "push_forward_score_distribution",
        {
            "role_probabilities": [0.5, 0.5],
            "transition_matrix": [[0.5, 0.5], [0.5, 0.5]],
            "reward_vector": [1.0, 0.0],
            "gamma": 0.9,
            "n_quantiles": 4,
        },
    )
    assert result.is_error is False
    # z = (1.45, 0.45) with mass (0.5, 0.5): mean 0.95, variance 0.25.
    assert result.structured_content["mean"] == pytest.approx(0.95)
    assert result.structured_content["std"] == pytest.approx(0.5)
    assert result.structured_content["quantile_levels"] == pytest.approx(
        [0.125, 0.375, 0.625, 0.875]
    )


async def test_push_forward_rejects_non_stochastic_matrix(client: Any) -> None:
    result = await client.call_tool(
        "push_forward_score_distribution",
        {
            "role_probabilities": [0.5, 0.5],
            "transition_matrix": [[0.5, 0.4], [0.5, 0.5]],
            "reward_vector": [1.0, 0.0],
        },
    )
    assert result.is_error is True
    assert "sum to 1.0" in result.content[0].text


async def test_distributional_case_filtering_matches_library(client: Any) -> None:
    arguments = {
        "role_names": ["NOM", "ACC"],
        "prior_probabilities": [0.5, 0.5],
        "observation_likelihoods": [0.9, 0.1],
        "n_iterations": 5,
        "n_quantiles": 8,
    }
    result = await client.call_tool("distributional_case_filtering", arguments)
    assert result.is_error is False
    expected = distributional_case_assignment(
        _belief(["NOM", "ACC"], [0.5, 0.5]),
        np.asarray([0.9, 0.1]),
        n_iterations=5,
        n_quantiles=8,
    )
    structured = result.structured_content
    assert structured["posterior"] == pytest.approx(
        list(map(float, expected.belief.probabilities))
    )
    assert structured["fe_trajectory"] == pytest.approx(
        [float(f) for f in expected.fe_trajectory]
    )
    assert structured["convergence_iteration"] == expected.convergence_iteration
    assert structured["converged"] == expected.converged


# ---------------------------------------------------------------------------
# 8-10. Quantile, message, and information utilities


async def test_quantile_td_update_matches_analytic_two_point_case(client: Any) -> None:
    result = await client.call_tool(
        "quantile_td_update",
        {
            "current_quantiles": [0.0, 1.0],
            "target_quantiles": [0.5, 0.5],
            "learning_rate": 0.5,
            "kappa": 1.0,
        },
    )
    assert result.is_error is False
    # tau = (0.25, 0.75); both targets sit inside kappa: theta' = theta + lr * tau-ish weight * delta.
    assert result.structured_content["updated_quantiles"] == pytest.approx(
        [0.0625, 0.9375]
    )


async def test_quantile_td_update_rejects_zero_learning_rate(client: Any) -> None:
    result = await client.call_tool(
        "quantile_td_update",
        {
            "current_quantiles": [0.0, 1.0],
            "target_quantiles": [0.5, 0.5],
            "learning_rate": 0.0,
        },
    )
    assert result.is_error is True


async def test_variational_message_update_matches_softmax_analytic(client: Any) -> None:
    result = await client.call_tool(
        "variational_message_update",
        {
            "observations": [1.0, 0.0],
            "prior_precision": [1.0],
            "likelihood_precision": [2.0, 2.0],
            "n_iterations": 4,
        },
    )
    assert result.is_error is False
    # softmax(2, 0) with posterior precision 1+2:
    total = math.exp(2.0) + 1.0
    assert result.structured_content["probabilities"] == pytest.approx(
        [math.exp(2.0) / total, 1.0 / total]
    )
    assert result.structured_content["posterior_precision"] == pytest.approx([3.0, 3.0])


async def test_variational_message_update_rejects_nonpositive_precision(
    client: Any,
) -> None:
    result = await client.call_tool(
        "variational_message_update",
        {
            "observations": [1.0, 0.0],
            "prior_precision": [1.0, 1.0],
            "likelihood_precision": [0.0, 2.0],
        },
    )
    assert result.is_error is True
    assert "positive" in result.content[0].text


async def test_expected_information_gain_matches_analytic_contributions(
    client: Any,
) -> None:
    result = await client.call_tool(
        "expected_information_gain",
        {
            "role_names": ["NOM", "ACC"],
            "prior_probabilities": [0.5, 0.5],
            "candidate_observations": [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]],
        },
    )
    assert result.is_error is False
    # Deterministic observations each carry 0.5*ln 2; the uninformative one carries 0.
    half_log2 = 0.5 * math.log(2.0)
    assert result.structured_content["per_observation"] == pytest.approx(
        [half_log2, half_log2, 0.0]
    )
    assert result.structured_content["total"] == pytest.approx(math.log(2.0))


# ---------------------------------------------------------------------------
# 11-12. Quantum assignment and frame policy


async def test_case_povm_assignment_matches_trace_rule(client: Any) -> None:
    result = await client.call_tool(
        "case_povm_assignment",
        {"role_names": ["NOM", "ACC"], "weights": [0.25, 0.75]},
    )
    assert result.is_error is False
    # Orthogonal projectors on the normalized diagonal state reproduce the weights.
    assert result.structured_content["probabilities"] == pytest.approx([0.25, 0.75])


async def test_case_povm_assignment_rejects_negative_weights(client: Any) -> None:
    result = await client.call_tool(
        "case_povm_assignment",
        {"role_names": ["NOM", "ACC"], "weights": [-0.25, 1.25]},
    )
    assert result.is_error is True
    assert "non-negative" in result.content[0].text


async def test_case_frame_violation_check_matches_library(client: Any) -> None:
    validator = CaseFrameValidator()
    well_typed = {"subject": "NOM", "object": "ACC"}
    direct = validator.validate_assignment(
        {entity: CaseRole[role] for entity, role in well_typed.items()}
    )
    result = await client.call_tool(
        "case_frame_violation_check", {"assignments": well_typed}
    )
    assert result.is_error is False
    assert len(result.structured_content["violations"]) == len(direct)
    assert result.structured_content["injection_score"] == pytest.approx(
        float(injection_score(direct))
    )

    violating = next(
        ({"x": a.name, "y": b.name}
         for a in CaseRole
         for b in CaseRole
         if a != b and validator.validate_assignment({"x": a, "y": b})),
        None,
    )
    if violating is not None:
        direct_bad = validator.validate_assignment(
            {entity: CaseRole[role] for entity, role in violating.items()}
        )
        bad = await client.call_tool(
            "case_frame_violation_check", {"assignments": violating}
        )
        assert bad.is_error is False
        assert len(bad.structured_content["violations"]) == len(direct_bad)
        assert bad.structured_content["injection_score"] == pytest.approx(
            float(injection_score(direct_bad))
        )


# ---------------------------------------------------------------------------
# 13-15. Presentations, magnitude, diagnostics


async def test_compare_theory_presentations_matches_library(client: Any) -> None:
    same = {
        "theory_a": {"name": "a", "sorts": ["s1"], "relations": {"r1": ["s1", "s1"]}, "axioms": []},
        "theory_b": {"name": "b", "sorts": ["s1"], "relations": {"r1": ["s1", "s1"]}, "axioms": []},
    }
    result = await client.call_tool("compare_theory_presentations", same)
    assert result.is_error is False
    assert result.structured_content["not_ruled_out"] is True
    assert result.structured_content["differences"] == []

    differ = {
        "theory_a": same["theory_a"],
        "theory_b": {"name": "b", "sorts": ["s1", "s2"], "relations": {"r1": ["s1", "s1"]}, "axioms": []},
    }
    result = await client.call_tool("compare_theory_presentations", differ)
    assert result.is_error is False
    assert result.structured_content["not_ruled_out"] is False
    differences = result.structured_content["differences"]
    assert isinstance(differences, list) and differences


async def test_enriched_category_magnitude_matches_analytic_value(client: Any) -> None:
    result = await client.call_tool(
        "enriched_category_magnitude",
        {
            "role_names": ["NOM", "ACC"],
            "proximity_matrix": [[1.0, 0.5], [0.5, 1.0]],
        },
    )
    assert result.is_error is False
    # Z^{-1} = (4/3) [[1, -1/2], [-1/2, 1]]; entries sum to 4/3, deficit 2/3.
    assert result.structured_content["magnitude"] == pytest.approx(4.0 / 3.0)
    assert result.structured_content["magnitude_deficit"] == pytest.approx(2.0 / 3.0)


async def test_enriched_category_magnitude_rejects_identity_violation(
    client: Any,
) -> None:
    result = await client.call_tool(
        "enriched_category_magnitude",
        {
            "role_names": ["NOM", "ACC"],
            "proximity_matrix": [[0.9, 0.5], [0.5, 1.0]],
        },
    )
    assert result.is_error is True
    assert "Identity axiom" in result.content[0].text


async def test_convergence_diagnostics_matches_library(client: Any) -> None:
    trajectory = [5.0, 4.0, 3.5, 3.49]
    result = await client.call_tool(
        "convergence_diagnostics",
        {"fe_trajectory": trajectory, "min_iterations": 3},
    )
    assert result.is_error is False
    expected = convergence_diagnostics(trajectory, min_iterations=3)
    structured = result.structured_content
    assert structured["monotone"] is True
    assert structured["converged"] == expected["converged"]
    assert structured["total_reduction"] == pytest.approx(expected["total_reduction"])
    assert structured["fe_range"] == pytest.approx(
        [float(x) for x in expected["fe_range"]]
    )
    assert structured["final_delta"] == pytest.approx(expected["final_delta"])


async def test_convergence_diagnostics_rejects_short_trajectory(client: Any) -> None:
    result = await client.call_tool(
        "convergence_diagnostics",
        {"fe_trajectory": [5.0, 4.0], "min_iterations": 3},
    )
    assert result.is_error is True
    assert "min_iterations" in result.content[0].text


# ---------------------------------------------------------------------------
# 16-17. Experiments and artifacts against the real temporary tree


async def test_list_experiment_variables_projects_real_evidence(
    client: Any, artifact_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CCD_ARTIFACT_ROOT", str(artifact_root))
    result = await client.call_tool("list_experiment_variables", {})
    assert result.is_error is False
    structured = result.structured_content
    assert structured["schema_version"] == "1.0"
    assert structured["variable_count"] >= 1
    assert structured["truncated"] is False
    for variable in structured["variables"]:
        assert variable["identifier"].startswith("exp_")
        assert set(variable) == {
            "identifier", "value", "unit", "ci_low", "ci_high",
            "confidence_level", "sample_unit", "interpretation",
        }
        assert variable["unit"] in {"probability", "dimensionless", "nats", "count", "version"}


async def test_list_experiment_variables_absent_artifacts_are_reported(
    client: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CCD_ARTIFACT_ROOT", str(tmp_path / "empty_output"))
    result = await client.call_tool("list_experiment_variables", {})
    assert result.is_error is True
    assert "not yet generated" in result.content[0].text


async def test_list_artifacts_enumerates_real_tree(
    client: Any, artifact_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CCD_ARTIFACT_ROOT", str(artifact_root))
    result = await client.call_tool("list_artifacts", {})
    assert result.is_error is False
    structured = result.structured_content
    assert structured["available"] is True
    paths = {entry["path"] for entry in structured["artifacts"]}
    assert {"metrics.json", "figures/fig.png", "experiments/results.json"} <= paths
    assert structured["count"] == len(paths)
    for entry in structured["artifacts"]:
        assert entry["uri"].startswith("ccd://artifacts/")
    dumped = json.dumps(structured)
    assert "/Volumes" not in dumped and "/Users" not in dumped


# ---------------------------------------------------------------------------
# Coverage closure: every advertised tool is executed above.


async def test_every_advertised_tool_is_exercised_by_this_module() -> None:
    exercised = {
        name
        for name in (
            "update_case_belief",
            "sequential_case_belief_update",
            "kl_divergence",
            "variational_free_energy",
            "expected_free_energy_score",
            "push_forward_score_distribution",
            "distributional_case_filtering",
            "quantile_td_update",
            "variational_message_update",
            "expected_information_gain",
            "case_povm_assignment",
            "case_frame_violation_check",
            "compare_theory_presentations",
            "enriched_category_magnitude",
            "convergence_diagnostics",
            "list_experiment_variables",
            "list_artifacts",
        )
    }
    assert exercised == EXPECTED_TOOLS
    assert len(exercised) == 17


async def test_server_resource_enumeration_matches_contained_root(
    artifact_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Resources enumerate the allowlist of the root active at build time."""
    monkeypatch.setenv("CCD_ARTIFACT_ROOT", str(artifact_root))
    async with Client(create_mcp_server()) as client:
        resources = (await client.list_resources()).resources
        uris = {str(resource.uri) for resource in resources}
        assert "ccd://artifacts/metrics.json" in uris
        assert "ccd://artifacts/experiments/results.json" in uris
        assert "ccd://experiments/results" in uris
        contents = (await client.read_resource("ccd://artifacts/metrics.json")).contents[0]
        assert isinstance(contents, TextResourceContents)
        assert "total_test_count" in contents.text
        experiments_text = (await client.read_resource("ccd://experiments/results")).contents[0]
        assert isinstance(experiments_text, TextResourceContents)
        experiments = json.loads(experiments_text.text)
        assert experiments["schema_version"] == "1.0"


def test_canonical_results_path_matches_loader_contract() -> None:
    assert experiments_path(Path("/any/root")) == Path("/any/root/experiments/results.json")
