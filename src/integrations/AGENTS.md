# src/integrations agent guidance

This package is the only place that bridges agents to the numerical
packages. Keep the adapters thin: no new mathematics, no second validation
layer, no writes. The wrapped methods' own validators raise the errors you
see over MCP; bounds live in `registry.py` and are mirrored in the JSON
schemas.

Ownership split (current revision): `registry.py`, `artifacts.py`,
`experiments.py`, `metadata.py`, and `methods.py` are root-owned; the MCP
wiring (`server.py`, `__main__.py`, `__init__.py`), the tests
(`tests/test_mcp_server.py`, `tests/test_agent_interface.py`), the docs
(`docs/agent_integrations.md`), and the installable skill are
integration-lane-owned. Coordinate before changing tool names, bounds, or
the artifact allowlist — tests and docs pin them.

Hard rules: all tools stay read-only with honest annotations; outputs must
be finite JSON (refuse, never stringify); no absolute paths in public
resource metadata or error payloads; artifact access stays inside the
allowlist; the claim ledger outranks any convenience rewording of a limit.
