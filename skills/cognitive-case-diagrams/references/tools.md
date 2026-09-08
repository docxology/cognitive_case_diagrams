# Tools, resources, and configuration reference

## Server launch and host configuration

| Mode | Command | Notes |
| :--- | :--- | :--- |
| Checkout (dev) | `uv run ccd-mcp` | Console script from the repo root; `uv sync` installs the dev group incl. `mcp`. |
| Module | `python -m src.integrations` | Equivalent entry point. |
| Installed wheel | `ccd-mcp` | After `pip install "cognitive_case_diagrams[mcp]"`. |

Diagnostics without a server: `ccd-mcp --list-tools` (JSON catalog),
`ccd-mcp --version`.

Generic JSON host (`mcpServers`):

```json
{
  "mcpServers": {
    "cognitive-case-diagrams": {
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/cognitive_case_diagrams", "ccd-mcp"]
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

Installed-wheel form: `"command": "ccd-mcp"` with no args. Optional env:
`CCD_ARTIFACT_ROOT` (absolute path) redirects the contained artifact root for
local runs; the allowlist below still applies inside that root.

## Tool inventory (all read-only; bounds: vectors <= 64 finite floats, matrices <= 16x16, sequences <= 32, quantile levels <= 101)

| Tool | Computes (implements) | Honest limit |
| :--- | :--- | :--- |
| `update_case_belief` | Normalized prior x likelihood (`cognitive.belief_updating.update_belief`) | Supplied synthetic evidence; no parsing. |
| `sequential_case_belief_update` | Per-step updates over a likelihood sequence | Each vector consumed once. |
| `kl_divergence` | KL(q\|\|p) (`cognitive.free_energy`) | Infinite case = explicit error. |
| `variational_free_energy` | Fixed-model free energy | Not a learned model. |
| `expected_free_energy_score` | Caller-defined score arithmetic | No optimality theorem. |
| `push_forward_score_distribution` | Law of R + gamma*T.T@q (`daif.core`) | Not a Bellman backup (mean 0.95 counterexample in docs). |
| `distributional_case_filtering` | Repeated likelihood assimilation | Iterations reuse evidence. |
| `quantile_td_update` | Pairwise quantile Huber update | Unnormalized Huber convention. |
| `variational_message_update` | Single-factor precision-weighted softmax | Not factor-graph inference. |
| `expected_information_gain` | p(o)*KL(posterior\|\|prior) contributions | MI only for a complete normalized alphabet. |
| `case_povm_assignment` | Trace rule, orthogonal projectors, diagonal state | Classical probabilities; no interference. |
| `case_frame_violation_check` | Supplied-label pairwise checks + severity | Not a security boundary. |
| `compare_theory_presentations` | Signature count/arity comparison | Not a Morita-equivalence decision. |
| `enriched_category_magnitude` | Inverse-sum / pseudoinverse magnitude | Matrix statistic only. |
| `convergence_diagnostics` | Trajectory change statistics | Not proof of a fixed point. |
| `list_experiment_variables` | Projection of canonical results variables | Refuses absent/stale evidence (fail-closed validator). |
| `list_artifacts` | Public artifact allowlist index | Contained root only. |

Example call and reply shape:

```json
{"name": "update_case_belief", "arguments": {"role_names": ["NOM", "ACC"],
 "prior_probabilities": [0.5, 0.5], "likelihood": [0.8, 0.2]}}
```

structured reply: `{"role_names": [...], "posterior": [...],
"entropy_nats": 0.5..., "most_likely_role": "NOM"}`.

## Resources

- `ccd://capabilities` — identity, scope, security model, claim ledger,
  per-tool contract notes, quality receipt (only embedded when validated;
  otherwise `missing`/`stale_or_invalid` with detail).
- `ccd://claims` — claim-ledger snapshot (canonical: `docs/claim_ledger.md`).
- `ccd://experiments/results` — canonical `output/experiments/results.json`
  verbatim once generated and validator-accepted; otherwise
  `{"available": false, "reason": ...}`.
- `ccd://artifacts/<path>` — allowlisted artifacts: `figures/`,
  `experiments/`, `manuscript/`, `web/`, `metrics.json`,
  `manuscript_variables.json`, `reports/quality_receipt.json`,
  `reports/publication_review.json`, `pdf/cognitive_case_diagrams_combined.pdf`.

## Security and failure behavior

- JSON-only inputs; no code execution, no network, no writes.
- Rejections you may see: `"artifact path is not on the public allowlist"`,
  `"artifact path must not traverse outside the artifact root"`,
  `"artifact exceeds the 2000000-byte read bound"`,
  `"prior_probabilities must sum to 1.0, got 1.8"`,
  `"List should have at most 64 items"`, `"Unknown tool: ..."`.
- Verification receipts: `tests/test_mcp_server.py` (real subprocess server +
  official SDK client over stdio) and `tests/test_agent_interface.py`
  (containment, experiments validator, CLI).
