# src/integrations

Agent-facing integration surface: bounded, schema-validated MCP adapters over
the existing numerical packages, the canonical synthetic-experiment results,
and an allowlisted view of the derived `output/` tree. The official MCP
Python SDK (`mcp` v2 line) is an optional dependency; the dev group installs
it by default.

| Module | Contract |
| :--- | :--- |
| `registry.py` | Transport bounds, role vocabulary, strict finite-JSON conversion. No I/O. |
| `artifacts.py` | Contained artifact index. Explicit public allowlist (`figures/`, `experiments/`, `manuscript/`, `web/`, exact approved files and final PDF); traversal, hidden/cache/review/release paths, symlinks, and reads beyond 2 MiB are rejected in both listing and reads. Missing `output/` degrades to "not yet generated", never to an error at startup. |
| `experiments.py` | Canonical `output/experiments/results.json` loader. Absence is "not yet generated"; schema drift, missing provenance, or a failed shared validator (`src.experiments.runner.validate_experiment_results`) is refuse-to-serve. |
| `metadata.py` | Claim-ledger snapshot and per-tool contract notes mirroring the canonical docs; quality receipt embedded only when `src.release_validation.validate_quality_receipt` accepts it (status reported explicitly otherwise). |
| `methods.py` | One thin handler per advertised tool: converts validated JSON to project inputs, calls exactly one existing public method, packs finite results into pydantic models. Semantic validation stays in the wrapped methods. |
| `server.py` | Official SDK wiring: 17 read-only tools, capability/claim/experiments resources, enumerated artifact resources; `main()` CLI (`--list-tools`, `--version`, stdio serve). |

Read [docs/agent_integrations.md](../docs/agent_integrations.md) for
install, host configuration, tool contracts, and the security model. The
claim ledger governs interpretation; these adapters add bounds and honesty,
not capability.
