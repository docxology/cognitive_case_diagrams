"""Agent-facing integration surface for cognitive_case_diagrams.

This package wraps existing project methods with bounded, schema-validated
adapters and exposes them over the Model Context Protocol, alongside
synthetic experiment results and an allowlist of contained project artifacts.

Importing this module does not require the optional ``mcp`` dependency: the
stdio server entry points (``create_mcp_server``, ``main``, ``tool_catalog``)
import lazily. See docs/agent_integrations.md for install, configuration, and
honest capability limits; the claim ledger (docs/claim_ledger.md) and method
contracts (docs/method_contracts.md) are canonical for what each tool means.
"""

from __future__ import annotations

from .artifacts import (
    ArtifactError,
    ArtifactIndex,
    artifact_uri,
    default_artifact_root,
)
from .experiments import (
    EXPERIMENTS_RELATIVE_PATH,
    EXPERIMENTS_RESOURCE_URI,
    ExperimentsNotGeneratedError,
    experiments_path,
    load_experiments,
    summarize_variables,
)
from .registry import CASE_ROLE_NAMES, json_safe

__all__ = [
    "CASE_ROLE_NAMES",
    "EXPERIMENTS_RELATIVE_PATH",
    "EXPERIMENTS_RESOURCE_URI",
    "ArtifactError",
    "ArtifactIndex",
    "ExperimentsNotGeneratedError",
    "artifact_uri",
    "create_mcp_server",
    "default_artifact_root",
    "experiments_path",
    "json_safe",
    "load_experiments",
    "main",
    "summarize_variables",
    "tool_catalog",
]


def __getattr__(name: str):
    """Import the MCP-bound server surface only when actually requested."""
    if name in ("create_mcp_server", "main", "tool_catalog"):
        from . import server

        return getattr(server, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
