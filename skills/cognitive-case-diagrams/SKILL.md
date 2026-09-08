---
name: cognitive-case-diagrams
description: Configure and use the cognitive_case_diagrams MCP server (bounded synthetic-method tools, experiment results, allowlisted artifacts) and interpret its outputs within the project's claim ledger.
---

# cognitive-case-diagrams MCP server

Serve the repository's synthetic categorical/active-inference examples to any
MCP host. Everything returned is a bounded, read-only computation over
synthetic inputs — a model quantity, never an empirical measurement, and no
tool is a security boundary. Canonical interpretation:
[claim ledger](https://github.com/docxology/cognitive_case_diagrams/blob/main/docs/claim_ledger.md)
and [method contracts](https://github.com/docxology/cognitive_case_diagrams/blob/main/docs/method_contracts.md).

## Configure

Checkout with `uv` installed:

```json
{"mcpServers": {"cognitive-case-diagrams": {"command": "uv",
  "args": ["run", "--project", "/absolute/path/to/cognitive_case_diagrams", "ccd-mcp"]}}}
```

Installed wheel: `{"command": "ccd-mcp"}`. Verify before use:

```bash
ccd-mcp --version && ccd-mcp --list-tools
```

Full details, Codex `config.toml` form, and the `CCD_ARTIFACT_ROOT` override:
[references/tools.md](references/tools.md).

## Use

- 17 read-only tools (belief updates, KL/free-energy scores, score
  distributions, quantile updates, VMP, information gain, POVM assignment,
  frame checks, presentation comparison, magnitude, diagnostics). All
  annotate `read_only=true, destructive=false, idempotent=true,
  open_world=false`; inputs are bounded (vectors <= 64 finite floats,
  matrices <= 16x16) and errors are explicit.
- Resources: `ccd://capabilities` (claims + contracts + quality receipt),
  `ccd://claims`, `ccd://experiments/results` (verbatim when the experiments
  stage has run; a structured "not yet generated" envelope otherwise),
  `ccd://artifacts/<path>` (explicit public allowlist only).
- Read `ccd://capabilities` before citing any result: each tool's contract
  note states what is computed and what is not implemented.
- Evidence status: `ccd-evidence-status` (console script, or
  `uv run python scripts/evidence_status.py`) prints the machine-readable
  per-stage evidence report (`missing`/`stale`/`invalid`/`validated`; exit 0
  only when every stage validates). Read-only: it reuses the canonical
  validators and never generates evidence.

## Boundaries (do not violate)

- Do not describe outputs as measurements, predictions of data, or evidence
  of the named theories; the ledger marks which claims are verified,
  partial, unsupported, or proposed.
- `push_forward_score_distribution` is not a Bellman backup;
  `compare_theory_presentations` does not decide equivalence;
  `case_frame_violation_check` is a supplied-label policy check, not a
  security control.
- If a tool result and the claim ledger disagree, report the discrepancy and
  withhold interpretation until source, tests, and ledger are reconciled.
