"""Official MCP stdio server for cognitive_case_diagrams.

Wires the bounded handlers in ``methods.TOOL_SPECS`` onto the official SDK
(``mcp`` v2 line, ``MCPServer``), registers the capability/claim and
synthetic-experiment resources, and enumerates allowlisted project artifacts
as concrete resources. All tools are honest read-only computations: bounded,
schema-validated inputs; finite JSON outputs via pydantic models; no supplied
code execution; artifact reads confined to the public allowlist.

Launch with the ``ccd-mcp`` console script or ``python -m src.integrations``.
"""

from __future__ import annotations

import argparse
import functools
import inspect
import json
import logging
import sys
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import ValidationError

from . import metadata
from .artifacts import ArtifactIndex
from .experiments import (
    EXPERIMENTS_RESOURCE_URI,
    ExperimentsNotGeneratedError,
    load_experiments,
)
from .methods import TOOL_SPECS

READ_ONLY_ANNOTATIONS = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)

EXPERIMENTS_PENDING_ENVELOPE = {
    "available": False,
    "reason": (
        "synthetic experiment results not yet generated; written by the "
        "experiments stage to output/experiments/results.json"
    ),
}


def _error_message(exc: Exception) -> str:
    """First line of a project validation error, for the MCP tool result."""
    text = str(exc).strip()
    return text.splitlines()[0] if text else type(exc).__name__


def _wrapped(handler: Any) -> Any:
    """Surface project validation errors as explicit, model-readable errors."""

    @functools.wraps(handler)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return handler(*args, **kwargs)
        except FileNotFoundError as exc:
            # ExperimentsNotGeneratedError and similar absence states are
            # expected, model-readable outcomes, not crashes.
            raise ToolError(_error_message(exc)) from exc
        except (ValueError, ValidationError) as exc:
            raise ToolError(_error_message(exc)) from exc

    # methods.py compiles annotations as strings (`from __future__ import
    # annotations`); evaluate them against the handler's own module globals so
    # the SDK's synthetic pydantic models see real types, not unresolvable
    # forward references.
    wrapper.__signature__ = inspect.signature(handler, eval_str=True)  # type: ignore[attr-defined]
    return wrapper


def _register_tools(server: MCPServer) -> None:
    for spec in TOOL_SPECS:
        server.tool(
            name=spec.name,
            description=spec.description,
            annotations=READ_ONLY_ANNOTATIONS,
        )(_wrapped(spec.handler))


def _register_artifact_resource(server: MCPServer, entry: dict[str, Any]) -> None:
    relative: str = entry["path"]
    mime: str = entry["mime_type"]

    @server.resource(entry["uri"], title=relative, mime_type=mime)
    def read_artifact() -> str | bytes:
        """Allowlisted project artifact under the contained artifact root."""
        content, detected = ArtifactIndex().read(relative)
        if detected.startswith("text/") or detected == "application/json":
            return content.decode("utf-8")
        return content


def _register_resources(server: MCPServer) -> None:
    @server.resource(
        "ccd://capabilities",
        title="Capabilities and claims",
        mime_type="application/json",
    )
    def capabilities() -> str:
        """Capability, claim, and quality metadata; receipt embedded only when validated."""
        return json.dumps(metadata.capability_metadata(), indent=2, sort_keys=True)

    @server.resource("ccd://claims", title="Claim ledger", mime_type="application/json")
    def claims() -> str:
        """Claim-ledger snapshot; docs/claim_ledger.md is canonical."""
        return json.dumps(
            {"claims": metadata.CLAIMS, "canonical_sources": metadata.CANONICAL_SOURCES},
            indent=2,
            sort_keys=True,
        )

    @server.resource(
        EXPERIMENTS_RESOURCE_URI,
        title="Synthetic experiment results",
        mime_type="application/json",
    )
    def experiments() -> str:
        """Verbatim canonical experiment results; absence means not yet generated."""
        try:
            payload = load_experiments(ArtifactIndex().root)
        except ExperimentsNotGeneratedError:
            return json.dumps(EXPERIMENTS_PENDING_ENVELOPE, indent=2, sort_keys=True)
        return json.dumps(payload, indent=2, sort_keys=True)

    index = ArtifactIndex()
    if index.available:
        for entry in index.entries()["artifacts"]:
            _register_artifact_resource(server, entry)


def create_mcp_server() -> MCPServer:
    """Build the MCP server with all tools and resources registered."""
    server = MCPServer(
        name=metadata.SERVER_NAME,
        instructions=metadata.SERVER_INSTRUCTIONS,
        version=metadata.project_version(),
    )
    _register_tools(server)
    _register_resources(server)
    return server


def tool_catalog() -> list[dict[str, Any]]:
    """Name, description, and annotation hints for every advertised tool."""
    return [
        {
            "name": spec.name,
            "description": spec.description,
            "annotations": {
                "read_only": True,
                "destructive": False,
                "idempotent": True,
                "open_world": False,
            },
        }
        for spec in TOOL_SPECS
    ]


def main(argv: list[str] | None = None) -> int:
    """Console entry point: serve MCP over stdio (or print catalog/version)."""
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    parser = argparse.ArgumentParser(
        prog="ccd-mcp",
        description=(
            "MCP stdio server exposing bounded cognitive_case_diagrams methods, "
            "synthetic experiment results, and allowlisted project artifacts."
        ),
    )
    parser.add_argument(
        "--list-tools", action="store_true", help="print the tool catalog as JSON and exit"
    )
    parser.add_argument("--version", action="store_true", help="print the server version and exit")
    args = parser.parse_args(argv)
    if args.version:
        print(metadata.project_version())
        return 0
    if args.list_tools:
        print(json.dumps(tool_catalog(), indent=2, sort_keys=True))
        return 0
    create_mcp_server().run(transport="stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
