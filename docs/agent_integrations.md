# Agent integrations: MCP server, CLI, and skill

`src/integrations` exposes the project's existing numerical methods, synthetic
experiment results, and derived artifacts to coding agents over the official
[Model Context Protocol](https://modelcontextprotocol.io) (MCP) using the
official Python SDK (`mcp` v2 line). Everything is a bounded, read-only,
schema-validated computation over synthetic inputs. Nothing here implements a
linguistic parser, a topos bridge, a distributional learner, an EEG model, or
an operational security system; the [claim ledger](claim_ledger.md) and
[method contracts](method_contracts.md) remain the controlling interpretation
of every advertised capability.

## Install

The server ships as a console script and a module entry point. The MCP SDK is
an optional dependency; the development toolchain includes it by default.

```bash
# From a repository checkout (installs the dev group, which includes mcp):
uv sync
uv run ccd-mcp --version          # console script
uv run python -m src.integrations --version

# From an installed wheel:
python -m pip install "cognitive_case_diagrams[mcp]"
ccd-mcp --version
```

`ccd-mcp --list-tools` prints the full tool catalog (names, descriptions,
annotation hints) as JSON without starting a server. `ccd-mcp --version`
prints the project version. With no arguments the process serves MCP over
stdio until its client disconnects.

## MCP configuration

Point any MCP host at the stdio server. Absolute paths are shown as
placeholders; substitute your checkout location.

Generic JSON host configuration (Claude Desktop-style `mcpServers`):

```json
{
  "mcpServers": {
    "cognitive-case-diagrams": {
      "command": "uv",
      "args": [
        "run", "--project",
        "/absolute/path/to/cognitive_case_diagrams", "ccd-mcp"
      ]
    }
  }
}
```

Installed-wheel configuration (no checkout required):

```json
{
  "mcpServers": {
    "cognitive-case-diagrams": {
      "command": "ccd-mcp"
    }
  }
}
```

Codex `config.toml`:

```toml
[mcp_servers.cognitive_case_diagrams]
command = "uv"
args = ["run", "--project", "/absolute/path/to/cognitive_case_diagrams", "ccd-mcp"]
```

Optional environment: `CCD_ARTIFACT_ROOT` overrides the contained artifact
root (default: the checkout's `output/` directory) for local server runs. The
override never widens access beyond the configured root, and the public
allowlist below still applies.

## Tools (17, all read-only)

Every tool declares `read_only_hint=true`, `destructive_hint=false`,
`idempotent_hint=true`, `open_world_hint=false`. Inputs are bounded
(`vectors <= 64` finite floats, matrices `<= 16 x 16`, observation sequences
`<= 32`, quantile grids `<= 101` levels) and validated twice: structurally by
the transport schema, then semantically by the project's own validators
(probability sums, stochastic rows, matrix contracts). Outputs are finite
JSON via validated pydantic models; a nonfinite or invalid result becomes an
explicit tool error, never a `NaN` in JSON.

| Tool | Implements | One-line contract and limit |
| :--- | :--- | :--- |
| `update_case_belief` | `cognitive.belief_updating.update_belief` | Normalized prior times supplied likelihood; no sentence parsing. |
| `sequential_case_belief_update` | `cognitive.belief_updating.sequential_belief_update` | One supplied likelihood vector per step; each consumed once. |
| `kl_divergence` | `cognitive.free_energy.kl_divergence` | KL(q||p); infinite cases are reported as errors, not emitted. |
| `variational_free_energy` | `cognitive.free_energy.variational_free_energy` | Fixed-model free energy from supplied log vectors. |
| `expected_free_energy_score` | `cognitive.action_selection.expected_free_energy` | Caller-defined score arithmetic; no optimality theorem. |
| `push_forward_score_distribution` | `daif.core.push_forward_return` | Law of dimensionless scores R + gamma*T.T@q; not a Bellman backup. |
| `distributional_case_filtering` | `daif.inference.distributional_case_assignment` | Repeated assimilation of one likelihood; iterations reuse evidence. |
| `quantile_td_update` | `daif.quantile.quantile_td_update` | Pairwise quantile Huber update; unnormalized loss convention. |
| `variational_message_update` | `daif.inference.variational_message_passing` | Single-factor softmax; prior precision is bookkeeping only. |
| `expected_information_gain` | `daif.inference.expected_information_gain` | Per-observation contributions; sum is MI only for a complete alphabet. |
| `case_povm_assignment` | `quantum.quantum_case` | Trace rule on orthogonal projectors over a diagonal mixture; classical probabilities, no interference. |
| `case_frame_violation_check` | `security.cognitive_security` | Supplied-label pairwise checks plus severity aggregate; not a security boundary. |
| `compare_theory_presentations` | `topos_theory.topos.compare_theory_presentations` | Signature-count comparison; neither necessary nor sufficient for Morita equivalence. |
| `enriched_category_magnitude` | `enriched_cat.enriched` | Inverse-sum or residual-validated pseudoinverse magnitude; a matrix statistic. |
| `convergence_diagnostics` | `daif.metrics.convergence_diagnostics` | Change statistics over a supplied trajectory; not proof of a fixed point. |
| `list_experiment_variables` | `src.experiments` results (read-only) | Projects the canonical variables registry; refuses absent or stale evidence. |
| `list_artifacts` | `integrations.artifacts.ArtifactIndex` | Enumerates the public artifact allowlist under the contained root. |

Example call (what a host sends; the SDK validates before the handler runs):

```json
{"name": "update_case_belief", "arguments": {
  "role_names": ["NOM", "ACC"],
  "prior_probabilities": [0.5, 0.5],
  "likelihood": [0.8, 0.2]
}}
```

Errors are explicit and model-readable: `"prior_probabilities must sum to
1.0, got 1.8"`, `"List should have at most 64 items"`,
`"kl_divergence is not finite; refusing to emit nonfinite JSON"`,
`"Unknown tool: does_not_exist"`.

## Resources

| URI | Content |
| :--- | :--- |
| `ccd://capabilities` | Server identity, scope, security model, claim ledger, per-tool contract notes, and the source-bound quality receipt (embedded only when validated; otherwise its explicit `missing`/`stale_or_invalid` status). |
| `ccd://claims` | The claim-ledger snapshot; `docs/claim_ledger.md` is canonical. |
| `ccd://experiments/results` | The canonical `output/experiments/results.json` verbatim when the experiments stage has run; otherwise a structured `{"available": false, "reason": ...}` envelope. Results are served only after the shared fail-closed validator accepts them (schema, finiteness, config hash, recomputed source digests, sanity controls). |
| `ccd://artifacts/<path>` | Concrete allowlisted artifacts, enumerated at startup. |

The artifact allowlist is explicit: `figures/`, `experiments/`,
`manuscript/`, and `web/` trees, plus exactly `metrics.json`,
`manuscript_variables.json`, `reports/quality_receipt.json`,
`reports/publication_review.json`, and
`pdf/cognitive_case_diagrams_combined.pdf`. Hidden components, caches,
`review/`, `release/`, `logs/`, symlinks, and oversized reads (`> 2 MiB`) are
rejected for both listing and direct reads. Path traversal (`..`), absolute
paths, and NUL bytes are rejected before any filesystem access.

## Security model

- **No code execution.** Tool arguments are JSON data; nothing is evaluated,
  imported, or shelled out from request content.
- **No network access.** Handlers call local functions only.
- **Bounded inputs and outputs.** Documented size limits in both the JSON
  schema and the handlers; finite-float outputs enforced by pydantic models.
- **Contained filesystem reads.** Only the allowlisted artifact root is
  readable; containment is enforced at open time, not by convention.
- **Honest annotations.** All tools advertise read-only, non-destructive,
  idempotent, closed-world behavior; the annotations match the code.
- **No secret material.** The served tree contains derived figures, hydrated
  manuscript text, metrics, and receipts. Private reports (telemetry,
  diagnostics, evidence registry, review trees) are outside the allowlist
  precisely because they can contain machine-local absolute paths.

## Verifying an installation

Real end-to-end coverage lives in `tests/test_mcp_server.py` (subprocess
server + official SDK client over stdio) and `tests/test_agent_interface.py`
(containment, experiments loader, CLI). To smoke-test any install by hand:

```bash
ccd-mcp --list-tools | head            # catalog without a server
uv run pytest tests/test_mcp_server.py tests/test_agent_interface.py -q
```

## Evidence status CLI

`ccd-evidence-status` (console script installed with the package, also via
`uv run python scripts/evidence_status.py`) prints one JSON report covering
the release-evidence stages: `quality`, `experiments`, `manuscript`,
`metadata`, `visual_review`, and `release`. Each stage reports `missing`,
`stale`, `invalid`, or `validated` by delegating to the canonical fail-closed
validators (never by re-implementing their checks); the release stage requires
archive verification plus a three-way source binding. The process exits 0 only
when every stage is validated, so a mid-pipeline checkout is expected to exit
1. It performs no generation, no network access, and no writes, and reports
only project-relative artifact paths. The MCP capability summary consumes the
same state mapping with its coarser `stale_or_invalid` vocabulary.

```bash
uv run ccd-evidence-status --project-root .
```

## Installable skill

`skills/cognitive-case-diagrams/` is a self-contained skill folder teaching
agents to configure the server, call its tools, and read its claims honestly.
Copy it into your skill directory:

```bash
cp -r skills/cognitive-case-diagrams "${CODEX_HOME:-$HOME/.codex}/skills/"
```

The repository-root `SKILL.md` routes in-checkout agents to the same
material. The claim ledger and method contracts govern interpretation of
every result; a number returned by these tools is a synthetic model quantity,
not an empirical measurement.
