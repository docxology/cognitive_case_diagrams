"""Fail-closed JSONL adapter for typed causal claim records.

Each JSONL line is one JSON object with EXACTLY the declared fields:

- required: ``cause``, ``effect``, ``relation`` (nonempty strings) and
  ``polarity`` (``"positive"`` or ``"negative"``);
- optional: ``regime`` (nonempty string or ``null``), ``temporal_scope``
  (nonempty string or ``null``), ``qualifiers`` (list of strings, default
  ``[]``), and ``provenance`` (object, preserved verbatim, default ``{}``).

Every deviation raises :class:`ValueError` naming the line number and the
offending field: missing required fields, wrong types, empty strings,
invalid polarity values, and unknown extra fields are all rejected. An
empty file (no records) also raises. No record is repaired, dropped, or
coerced; the adapter only fills declared defaults for absent optional
fields, so downstream consumers see one typed record shape.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "POLARITIES",
    "REQUIRED_FIELDS",
    "ALLOWED_FIELDS",
    "load_claim_records",
    "to_canonical_dict",
]

REQUIRED_FIELDS: tuple[str, ...] = ("cause", "effect", "relation", "polarity")
POLARITIES = frozenset({"positive", "negative"})
OPTIONAL_FIELDS: tuple[str, ...] = (
    "regime", "temporal_scope", "qualifiers", "provenance")
ALLOWED_FIELDS = frozenset(REQUIRED_FIELDS) | frozenset(OPTIONAL_FIELDS)


def _reject(origin: str, field: str, detail: str) -> None:
    raise ValueError(f"{origin}: field {field!r} {detail}")


def _require_nonempty_str(origin: str, record: Mapping[str, Any],
                          field: str) -> str:
    value = record[field]
    if not isinstance(value, str) or not value.strip():
        _reject(origin, field, f"must be a nonempty string, got {value!r}")
    return value


def _require_str_or_none(origin: str, record: Mapping[str, Any],
                         field: str) -> str | None:
    value = record.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        _reject(origin, field,
                f"must be a nonempty string or null, got {value!r}")
    return value


def _canonicalize(record: Any, origin: str) -> dict[str, Any]:
    """Validate one record and return the typed canonical dict."""
    if not isinstance(record, Mapping):
        raise ValueError(f"{origin}: record must be a JSON object, "
                         f"got {type(record).__name__}")
    for field in REQUIRED_FIELDS:
        if field not in record:
            _reject(origin, field, "is required but missing")
    unknown = sorted(set(record) - ALLOWED_FIELDS)
    if unknown:
        _reject(origin, ", ".join(unknown),
                f"is/are unknown; allowed fields are {sorted(ALLOWED_FIELDS)}")
    canonical: dict[str, Any] = {
        field: _require_nonempty_str(origin, record, field)
        for field in ("cause", "effect", "relation")
    }
    polarity = record["polarity"]
    if polarity not in POLARITIES:
        _reject(origin, "polarity",
                f"must be one of {sorted(POLARITIES)}, got {polarity!r}")
    canonical["polarity"] = polarity
    canonical["regime"] = _require_str_or_none(origin, record, "regime")
    canonical["temporal_scope"] = _require_str_or_none(
        origin, record, "temporal_scope")
    qualifiers = record.get("qualifiers", [])
    if not isinstance(qualifiers, list) \
            or not all(isinstance(q, str) and q.strip() for q in qualifiers):
        _reject(origin, "qualifiers", "must be a list of nonempty strings, "
                f"got {qualifiers!r}")
    canonical["qualifiers"] = list(qualifiers)
    provenance = record.get("provenance", {})
    if not isinstance(provenance, Mapping):
        _reject(origin, "provenance",
                f"must be an object, got {type(provenance).__name__}")
    # Preserved verbatim: no key, value, or ordering normalization.
    canonical["provenance"] = dict(provenance)
    return canonical


def to_canonical_dict(record: Any) -> dict[str, Any]:
    """Validate one claim record and return its typed canonical view.

    Raises:
        ValueError: Naming the offending field for any missing required
            field, wrong type, invalid polarity, or unknown extra field.
    """
    return _canonicalize(record, "record")


def load_claim_records(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate a JSONL claim-record file, fail-closed.

    Whitespace-only lines are skipped; every other line must be one valid
    claim record. Returns the list of typed canonical dicts in file order.

    Raises:
        ValueError: Naming the line number and field for the first invalid
            record, or when the file contains no records at all.
    """
    records: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            origin = f"line {line_number}"
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{origin}: invalid JSON ({exc})") from exc
            records.append(_canonicalize(parsed, origin))
    if not records:
        raise ValueError(f"{path}: file contains no claim records")
    return records
