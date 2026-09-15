"""Fail-closed behavior of the JSONL claim-record adapter (real files)."""
from __future__ import annotations

import json

import pytest

from src.aggregation.adapter import load_claim_records, to_canonical_dict

VALID = {
    "cause": "rainfall",
    "effect": "runoff",
    "relation": "causes",
    "polarity": "positive",
}


def _write(tmp_path, lines):
    path = tmp_path / "claims.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_valid_file_round_trips_typed_view(tmp_path):
    path = _write(tmp_path, [
        json.dumps({**VALID, "regime": "wet", "temporal_scope": "acute",
                    "qualifiers": ["observed"],
                    "provenance": {"page": 3, "note": [1, 2]}}),
        json.dumps(VALID),
    ])
    records = load_claim_records(path)
    assert len(records) == 2
    first = records[0]
    assert first["regime"] == "wet"
    assert first["qualifiers"] == ["observed"]
    assert first["provenance"] == {"page": 3, "note": [1, 2]}
    assert set(first) == {"cause", "effect", "relation", "polarity",
                          "regime", "temporal_scope", "qualifiers",
                          "provenance"}
    # Defaults are filled for absent optional fields.
    second = records[1]
    assert second["regime"] is None
    assert second["temporal_scope"] is None
    assert second["qualifiers"] == []
    assert second["provenance"] == {}
    # to_canonical_dict agrees with the loader on the same record.
    assert to_canonical_dict(json.loads(json.dumps(VALID))) == second


def test_blank_lines_are_skipped(tmp_path):
    path = _write(tmp_path, ["", json.dumps(VALID), "  ", json.dumps(VALID)])
    assert len(load_claim_records(path)) == 2


def test_missing_required_field_names_line_and_field(tmp_path):
    path = _write(tmp_path, [json.dumps(VALID),
                             json.dumps({"cause": "x", "relation": "causes",
                                         "polarity": "positive"})])
    with pytest.raises(ValueError, match="line 2.*'effect'"):
        load_claim_records(path)


def test_bad_polarity_names_line_and_field(tmp_path):
    path = _write(tmp_path, [json.dumps(VALID),
                             json.dumps({**VALID, "polarity": "neutral"})])
    with pytest.raises(ValueError, match="line 2.*'polarity'"):
        load_claim_records(path)


def test_unknown_field_is_rejected(tmp_path):
    path = _write(tmp_path, [json.dumps({**VALID, "confidence": 0.9})])
    with pytest.raises(ValueError, match="line 1.*confidence"):
        load_claim_records(path)


def test_empty_file_raises(tmp_path):
    path = _write(tmp_path, [""])
    with pytest.raises(ValueError, match="no claim records"):
        load_claim_records(path)


def test_invalid_json_names_line(tmp_path):
    path = _write(tmp_path, [json.dumps(VALID), "{not json"])
    with pytest.raises(ValueError, match="line 2.*invalid JSON"):
        load_claim_records(path)


@pytest.mark.parametrize("mutate,field", [
    (lambda r: r.update(cause=""), "cause"),
    (lambda r: r.update(effect=3), "effect"),
    (lambda r: r.update(relation=None), "relation"),
    (lambda r: r.update(regime=""), "regime"),
    (lambda r: r.update(temporal_scope=5), "temporal_scope"),
    (lambda r: r.update(qualifiers=["ok", ""]), "qualifiers"),
    (lambda r: r.update(qualifiers="single"), "qualifiers"),
    (lambda r: r.update(provenance=["not", "a", "dict"]), "provenance"),
])
def test_invalid_optional_fields_rejected_with_field_name(mutate, field):
    record = json.loads(json.dumps(VALID))
    mutate(record)
    with pytest.raises(ValueError, match=f"'{field}'"):
        to_canonical_dict(record)


def test_regime_null_accepted_and_nonstring_rejected():
    null_record = to_canonical_dict(VALID)
    assert null_record["regime"] is None
    with pytest.raises(ValueError, match="'regime'"):
        to_canonical_dict({**VALID, "regime": 0})
