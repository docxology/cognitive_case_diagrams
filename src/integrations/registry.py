"""Shared bounds, role vocabulary, and JSON-safety rules for agent-facing surfaces.

The integration layer wraps existing project methods with transport-level
bounds. Semantic validation (probability sums, stochastic rows, matrix
contracts) stays in the wrapped methods; this module only defines the finite,
bounded envelopes and the strict JSON serialization rule.

Nothing here executes supplied code, opens network connections, or touches
the filesystem outside explicitly contained roots (see artifacts.py).
"""

from __future__ import annotations

import math
from typing import Any

# Transport-level bounds. Every bound is also advertised in the tool JSON
# schema, so oversized requests are rejected before handlers run.
MAX_VECTOR_LENGTH = 64
MAX_MATRIX_DIM = 16
MAX_STEPS = 32
MAX_OBSERVATIONS = 32
MAX_NAME_LENGTH = 64
MAX_QUANTILES = 101
MAX_ARTIFACT_BYTES = 2_000_000
# Final PDF deliverables are one to two orders of magnitude larger than any
# other public artifact but remain single bounded files; the read bound is
# per artifact class (see artifacts.read_bound_for), never a global raise.
MAX_PDF_BYTES = 24_000_000
MAX_ARTIFACT_ENTRIES = 200
MAX_EXPERIMENT_VARIABLES = 256
MAX_FRAME_ASSIGNMENTS = 64

# Case-role vocabulary of src.case_systems.case_category.CaseRole, by enum
# member name. Alignment-specific and core-argument roles are included.
CASE_ROLE_NAMES: tuple[str, ...] = (
    "NOM", "ACC", "GEN", "DAT", "INS", "LOC", "ABL", "VOC",
    "ERG", "ABS", "S", "A", "P",
)


def check_length(values: Any, name: str, maximum: int) -> None:
    """Reject containers longer than the advertised transport bound."""
    if len(values) > maximum:
        raise ValueError(
            f"{name} has {len(values)} items; at most {maximum} are accepted"
        )


def json_safe(value: Any, name: str = "value") -> Any:
    """Return a strictly JSON-serializable copy, rejecting nonfinite floats.

    NumPy arrays and scalars are converted; mappings must have string keys;
    anything else is rejected instead of being stringified silently.
    """
    return _json_safe(value, name, 0)


def _json_safe(value: Any, name: str, depth: int) -> Any:
    if depth > 8:
        raise ValueError(f"{name} nested too deeply for JSON output")
    module = type(value).__module__
    if module == "numpy" or module.startswith("numpy."):
        if hasattr(value, "ndim"):  # ndarray
            return _json_safe(value.tolist(), name, depth + 1)
        if hasattr(value, "item"):  # numpy scalar
            return _json_safe(value.item(), name, depth + 1)
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite, got {value!r}")
        return value
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{name} mapping keys must be strings")
            result[key] = _json_safe(item, f"{name}[{key}]", depth + 1)
        return result
    if isinstance(value, (list, tuple)):
        return [
            _json_safe(item, f"{name}[{index}]", depth + 1)
            for index, item in enumerate(value)
        ]
    raise ValueError(f"{name} of type {type(value).__name__} is not JSON-serializable")
