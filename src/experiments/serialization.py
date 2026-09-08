"""Exact, finite-enforcing serialization for experiment results.

``results_to_json`` produces deterministic text: sorted keys, fixed indent,
ASCII, and ``allow_nan=False`` so a non-finite value fails loudly instead of
producing invalid JSON. ``write_results`` validates finiteness first and
creates parent directories; the default path is the canonical artifact
``output/experiments/results.json`` (parent orchestration owns the call).
"""
from __future__ import annotations

import json
from pathlib import Path

from .runner import DEFAULT_RESULTS_PATH, assert_finite_json
from src.release_validation import write_json_atomic

__all__ = ["results_to_json", "write_results"]


def results_to_json(results: dict) -> str:
    """Serialize results to deterministic JSON text.

    Raises:
        ValueError: If any value is non-finite (``allow_nan=False``).
    """
    assert_finite_json(results)
    return json.dumps(results, indent=2, sort_keys=True, ensure_ascii=True,
                      allow_nan=False) + "\n"


def write_results(results: dict, path: str | Path | None = None) -> Path:
    """Validate and write results JSON. Returns the written path.

    The default target is ``output/experiments/results.json`` relative to the
    working directory; parent orchestration decides when and whether to call
    this. Raises before writing if any value is non-finite.
    """
    target = Path(DEFAULT_RESULTS_PATH if path is None else path)
    assert_finite_json(results)
    write_json_atomic(target, results)
    return target
