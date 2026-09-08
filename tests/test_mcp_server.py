"""Real stdio MCP client tests for the cognitive_case_diagrams server.

Every test launches the actual server as a subprocess (``python -m
src.integrations.server``) and drives it with the official MCP Python SDK
client over stdio: initialization, tool listing, tool calls (happy paths,
schema rejections, semantic errors, unknown tools), resource reads
(capabilities, claims, artifacts, experiments), and containment behavior
against traversal and non-allowlisted URIs. No mocks, no in-memory shortcuts.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from PIL import Image
from mcp import Client, MCPError, StdioServerParameters
from mcp.types import TextResourceContents

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.belief_updating import update_belief

pytestmark = pytest.mark.anyio

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOOL_COUNT = 17


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> Any:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.integrations.server"],
        cwd=str(PROJECT_ROOT),
    )
    async with Client(params) as connected:
        yield connected


@pytest.fixture
async def artifact_client(tmp_path: Path) -> Any:
    """Exercise real artifact files without depending on generated checkout output."""
    output = tmp_path / "output"
    (output / "figures").mkdir(parents=True)
    (output / "review").mkdir()
    (output / "reports").mkdir()
    (output / "metrics.json").write_text(json.dumps({"fixture_only": True, "total_test_count": 2}))
    Image.new("RGB", (32, 32), "blue").save(output / "figures/example.png")
    (output / "review/private.txt").write_text("private fixture")
    (output / "reports/diagnostics.json").write_text("{}")
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.integrations.server"],
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "CCD_ARTIFACT_ROOT": str(output)},
    )
    async with Client(params) as connected:
        yield connected


# ---------------------------------------------------------------------------
# Initialization and discovery


async def test_initialize_reports_identity_and_capabilities(client: Any) -> None:
    assert client.server_info.name == "cognitive-case-diagrams"
    assert client.server_info.version
    assert client.server_capabilities.tools is not None
    assert client.server_capabilities.resources is not None
    assert client.instructions and "synthetic" in client.instructions.lower()


async def test_list_tools_is_bounded_annotated_and_schematized(client: Any) -> None:
    tools = (await client.list_tools()).tools
    assert len(tools) == EXPECTED_TOOL_COUNT
    names = [tool.name for tool in tools]
    assert len(names) == len(set(names))
    for tool in tools:
        assert tool.annotations is not None
        assert tool.annotations.read_only_hint is True
        assert tool.annotations.destructive_hint is False
        assert tool.annotations.idempotent_hint is True
        assert tool.annotations.open_world_hint is False
        assert tool.description
        assert tool.input_schema["type"] == "object"
        assert isinstance(tool.input_schema["properties"], dict)
        assert tool.output_schema is not None


async def test_update_belief_schema_is_bounded_and_vocabulary_checked(
    client: Any,
) -> None:
    tools = (await client.list_tools()).tools
    schema = next(t for t in tools if t.name == "update_case_belief").input_schema
    role_items = schema["properties"]["role_names"]["items"]
    assert set(role_items["enum"]) >= {"NOM", "ACC", "ERG", "P"}
    assert schema["properties"]["prior_probabilities"]["maxItems"] == 64
    assert set(schema["required"]) == {"role_names", "prior_probabilities", "likelihood"}


# ---------------------------------------------------------------------------
# Tool calls


async def test_update_case_belief_matches_direct_library_call(client: Any) -> None:
    result = await client.call_tool(
        "update_case_belief",
        {
            "role_names": ["NOM", "ACC"],
            "prior_probabilities": [0.5, 0.5],
            "likelihood": [0.8, 0.2],
        },
    )
    assert result.is_error is False
    expected = update_belief(
        CaseDiagramBelief([CaseRole.NOM, CaseRole.ACC], np.array([0.5, 0.5])),
        np.array([0.8, 0.2]),
    )
    posterior = result.structured_content["posterior"]
    assert posterior == pytest.approx(list(map(float, expected.probabilities)))
    assert result.structured_content["entropy_nats"] == pytest.approx(expected.entropy())
    assert result.structured_content["most_likely_role"] == "NOM"


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
    # docs/manuscript/07c_daif_results.md: the score mean is 0.95, not 5.0.
    assert result.structured_content["mean"] == pytest.approx(0.95)


async def test_semantic_validation_error_is_explicit(client: Any) -> None:
    result = await client.call_tool(
        "update_case_belief",
        {
            "role_names": ["NOM", "ACC"],
            "prior_probabilities": [0.9, 0.9],
            "likelihood": [0.5, 0.5],
        },
    )
    assert result.is_error is True
    assert "sum to 1.0" in result.content[0].text


async def test_transport_bound_rejects_oversized_input(client: Any) -> None:
    result = await client.call_tool(
        "update_case_belief",
        {
            "role_names": ["NOM"],
            "prior_probabilities": [0.0] * 65,
            "likelihood": [1.0],
        },
    )
    assert result.is_error is True
    assert "at most 64" in result.content[0].text


async def test_nonfinite_output_is_refused_not_emitted(client: Any) -> None:
    result = await client.call_tool(
        "kl_divergence",
        {"q_probabilities": [1.0, 0.0], "p_probabilities": [0.0, 1.0]},
    )
    assert result.is_error is True
    assert "finite" in result.content[0].text


async def test_unknown_tool_is_an_explicit_error(client: Any) -> None:
    result = await client.call_tool("does_not_exist", {})
    assert result.is_error is True
    assert "Unknown tool" in result.content[0].text


async def test_experiment_variables_tool_matches_canonical_file(client: Any) -> None:
    from src.integrations.artifacts import ArtifactIndex
    from src.integrations.experiments import experiments_path

    result = await client.call_tool("list_experiment_variables", {})
    canonical = experiments_path(ArtifactIndex().root)
    if canonical.is_file():
        assert result.is_error is False
        variables = result.structured_content["variables"]
        assert variables
        for variable in variables:
            assert set(variable) == {
                "identifier", "value", "unit", "ci_low", "ci_high",
                "confidence_level", "sample_unit", "interpretation",
            }
    else:
        # The canonical results file does not exist until the experiments
        # stage runs; the tool must say so in a model-readable error.
        assert result.is_error is True
        assert "not yet generated" in result.content[0].text


# ---------------------------------------------------------------------------
# Resources


async def test_capabilities_and_claims_resources_are_path_free(client: Any) -> None:
    capabilities = json.loads(
        (await client.read_resource("ccd://capabilities")).contents[0].text
    )
    claims = json.loads((await client.read_resource("ccd://claims")).contents[0].text)
    assert len(capabilities["claims"]) >= 13
    assert len(capabilities["tool_contracts"]) == EXPECTED_TOOL_COUNT
    assert capabilities["quality_receipt"]["status"] in {
        "validated",
        "missing",
        "stale_or_invalid",
    }
    assert len(claims["claims"]) == len(capabilities["claims"])
    for payload in (json.dumps(capabilities), json.dumps(claims)):
        assert "/Volumes" not in payload
        assert "/Users" not in payload


async def test_artifact_resources_enumerate_allowlist_only(artifact_client: Any) -> None:
    resources = (await artifact_client.list_resources()).resources
    uris = [str(resource.uri) for resource in resources]
    artifact_uris = [uri for uri in uris if uri.startswith("ccd://artifacts/")]
    assert "ccd://artifacts/metrics.json" in artifact_uris
    assert any(uri.endswith(".png") for uri in artifact_uris)
    assert not any(
        marker in uri
        for uri in uris
        for marker in ("telemetry", "diagnostics", "review", "evidence_registry", "/Users", "/Volumes")
    )


async def test_metrics_resource_is_valid_json(artifact_client: Any) -> None:
    contents = (await artifact_client.read_resource("ccd://artifacts/metrics.json")).contents[0]
    assert isinstance(contents, TextResourceContents)
    assert contents.mime_type == "application/json"
    assert "total_test_count" in json.loads(contents.text)


async def test_png_resource_is_a_bounded_blob(artifact_client: Any) -> None:
    resources = (await artifact_client.list_resources()).resources
    png_uri = next(
        str(resource.uri)
        for resource in resources
        if str(resource.uri).startswith("ccd://artifacts/figures/")
        and str(resource.uri).endswith(".png")
    )
    contents = (await artifact_client.read_resource(png_uri)).contents[0]
    assert contents.mime_type == "image/png"
    assert len(contents.blob) > 100  # type: ignore[attr-defined]


async def test_traversal_and_non_allowlisted_uris_are_refused(client: Any) -> None:
    for uri in (
        "ccd://artifacts/../../pyproject.toml",
        "ccd://artifacts/telemetry.json",
        "ccd://artifacts/review/private.log",
        "ccd://artifacts/figures/nonexistent.png",
    ):
        with pytest.raises(MCPError):
            await client.read_resource(uri)


async def test_experiments_resource_reports_absence_or_valid_results(
    client: Any,
) -> None:
    contents = (await client.read_resource("ccd://experiments/results")).contents[0]
    payload = json.loads(contents.text)
    from src.integrations.experiments import experiments_path
    from src.integrations.artifacts import ArtifactIndex

    canonical = experiments_path(ArtifactIndex().root)
    if canonical.is_file():
        assert payload["schema_version"] == "1.0"
        assert payload["provenance"]["config_sha256"]
    else:
        assert payload["available"] is False
        assert "not yet generated" in payload["reason"]
