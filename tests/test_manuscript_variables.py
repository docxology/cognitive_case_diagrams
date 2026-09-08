"""Tests for the typed manuscript variable registry (no mocks, real files).

Covers registry invariants, strict metric validation, the schema-1.0
experiments reader, the negative-control claim scanner, and the variables
manifest round trip on real tmp evidence built by
:mod:`tests.fixtures_manuscript`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

pytest_plugins = ("fixtures_manuscript",)

from src.manuscript_variables import (  # noqa: E402
    EXPERIMENT_UNITS,
    EXPERIMENT_VARIABLE_NAMES,
    FORMATS,
    PROVENANCE_CLASSES,
    TOKEN_RE,
    UNITS,
    VariableSpec,
    format_float,
    read_experiment_variables,
    scan_hard_coded_claims,
    spec_by_name,
    validate_metrics,
    validate_token_name,
    variable_specs,
    write_variables_manifest,
)


# ---------------------------------------------------------------------------
# Registry invariants
# ---------------------------------------------------------------------------


def test_specs_are_unique_and_pattern_addressable() -> None:
    specs = variable_specs()
    assert len(specs) > 40
    for name in specs:
        validate_token_name(name)
        assert TOKEN_RE.fullmatch("${" + name + "}")


def test_every_spec_has_known_unit_format_and_provenance() -> None:
    for spec in variable_specs().values():
        assert spec.format in FORMATS, spec
        assert spec.provenance in PROVENANCE_CLASSES, spec
        allowed = EXPERIMENT_UNITS if spec.provenance == "experiments" else UNITS
        assert spec.unit in allowed, spec
        assert spec.description.strip() and spec.source.strip(), spec


def test_experiment_specs_agree_with_runner_definitions() -> None:
    from src.experiments.runner import experiment_variable_definitions

    definitions = experiment_variable_definitions()
    specs = variable_specs()
    assert set(definitions) == set(EXPERIMENT_VARIABLE_NAMES)
    for name, definition in definitions.items():
        spec = specs[name]
        assert spec.provenance == "experiments"
        assert spec.unit == definition["unit"]


def test_receipt_and_experiment_specs_are_declared() -> None:
    specs = variable_specs()
    for name in ("total_tests_passed", "coverage_percent", "quality_fingerprint_short"):
        assert specs[name].provenance == "quality_receipt"
    assert specs["exp_sanity_analytic_identities_pass"].unit == "count"
    assert specs["exp_sensitivity_entropy_bins_max_abs_effect"].unit == "nats"


def test_invalid_spec_constructions_rejected() -> None:
    with pytest.raises(ValueError):
        VariableSpec(
            name="bad-dash",
            unit="count",
            format="integer",
            provenance="computed",
            description="dash is not token addressable",
            source="test",
        )
    with pytest.raises(ValueError):
        VariableSpec(
            name="ok_name",
            unit="cubits",
            format="integer",
            provenance="computed",
            description="unknown unit",
            source="test",
        )


# ---------------------------------------------------------------------------
# Strict metric validation
# ---------------------------------------------------------------------------


def test_fixture_metrics_pass_strict_validation(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    specs = validate_metrics(metrics)
    assert specs["total_test_count"].provenance == "collection"
    assert metrics["total_test_count"] == "2"
    assert metrics["publication_status"] == "release manuscript"


def test_unknown_metric_key_rejected() -> None:
    with pytest.raises(ValueError, match="Unregistered manuscript variables"):
        validate_metrics({"invented_statistic": "1"})


def test_missing_required_variable_rejected() -> None:
    with pytest.raises(ValueError, match="Required manuscript variables missing"):
        validate_metrics({"total_test_files": "3"})


def test_nonfinite_value_rejected_for_decimal_format(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    metrics["coverage_percent"] = "inf"
    with pytest.raises(ValueError, match="coverage_percent"):
        validate_metrics(metrics)


def test_malformed_decimal_rejected(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    metrics["coverage_percent"] = "ninety"
    with pytest.raises(ValueError, match="coverage_percent"):
        validate_metrics(metrics)


def test_malformed_integer_rejected(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    metrics["total_test_count"] = "7.5"
    with pytest.raises(ValueError, match="total_test_count"):
        validate_metrics(metrics)


def test_empty_value_rejected(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    metrics["total_test_count"] = ""
    with pytest.raises(ValueError, match="total_test_count"):
        validate_metrics(metrics)


def test_word_format_rejects_digits(gate_tree: Path) -> None:
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    metrics["daif_modules_word"] = "se7en"
    with pytest.raises(ValueError, match="daif_modules_word"):
        validate_metrics(metrics)


def test_format_float_rejects_nonfinite() -> None:
    assert format_float(0.5) == "0.5"
    with pytest.raises(ValueError):
        format_float(float("nan"))


# ---------------------------------------------------------------------------
# Experiments reader (schema 1.0)
# ---------------------------------------------------------------------------


def test_read_experiment_variables_from_real_runner(gate_tree: Path) -> None:
    collected = read_experiment_variables(gate_tree)
    assert set(collected) == set(EXPERIMENT_VARIABLE_NAMES)
    # The sanity control is a numeric 0/1 flag, never a JSON boolean.
    flag = collected["exp_sanity_analytic_identities_pass"]
    assert flag in ("1", "0")


def test_missing_results_file_named_in_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="results.json"):
        read_experiment_variables(tmp_path)


def _tamper_results(root: Path, mutate) -> None:
    path = root / "output" / "experiments" / "results.json"
    payload = json.loads(path.read_text())
    mutate(payload)
    path.write_text(json.dumps(payload))


def test_bad_schema_version_rejected(gate_tree: Path) -> None:
    _tamper_results(gate_tree, lambda p: p.update(schema_version="9.9"))
    with pytest.raises(ValueError, match="schema_version"):
        read_experiment_variables(gate_tree)


def test_non_hex_config_hash_rejected(gate_tree: Path) -> None:
    _tamper_results(
        gate_tree,
        lambda p: p["provenance"].update(config_sha256="nothex"),
    )
    with pytest.raises(ValueError, match="config_sha256"):
        read_experiment_variables(gate_tree)


def test_boolean_value_rejected(gate_tree: Path) -> None:
    name = next(iter(EXPERIMENT_VARIABLE_NAMES))
    _tamper_results(
        gate_tree,
        lambda p: p["variables"][name].update(value=True),
    )
    with pytest.raises(ValueError, match="finite number"):
        read_experiment_variables(gate_tree)


def test_nonfinite_value_rejected(gate_tree: Path) -> None:
    name = next(iter(EXPERIMENT_VARIABLE_NAMES))
    _tamper_results(
        gate_tree,
        lambda p: p["variables"][name].update(value=float("inf")),
    )
    with pytest.raises(ValueError, match="non-finite"):
        read_experiment_variables(gate_tree)


def test_unknown_identifier_rejected(gate_tree: Path) -> None:
    _tamper_results(
        gate_tree,
        lambda p: p["variables"].update(
            {"exp_future_statistic": {"value": 1.0, "unit": "count"}}
        ),
    )
    with pytest.raises(ValueError, match="exp_future_statistic"):
        read_experiment_variables(gate_tree)


def test_unit_mismatch_rejected(gate_tree: Path) -> None:
    name = next(iter(EXPERIMENT_VARIABLE_NAMES))
    _tamper_results(
        gate_tree,
        lambda p: p["variables"][name].update(unit="nats"),
    )
    with pytest.raises(ValueError, match="do not match their study metrics"):
        read_experiment_variables(gate_tree)


def test_missing_provenance_fields_rejected(gate_tree: Path) -> None:
    _tamper_results(gate_tree, lambda p: p["provenance"].pop("seed"))
    with pytest.raises(ValueError, match="seed"):
        read_experiment_variables(gate_tree)


# ---------------------------------------------------------------------------
# Negative-control scanner
# ---------------------------------------------------------------------------


def test_caption_literal_is_flagged() -> None:
    findings = scan_hard_coded_claims(
        {"c.md": "![masses 0.8 on NOM](p.png){#fig:x}"}
    )
    assert findings == ["c.md: unbacked numeric literal '0.8' in prose"]


def test_math_decimal_input_is_flagged() -> None:
    findings = scan_hard_coded_claims({"m.md": "Supplied input $p=0.8$ drives it."})
    assert findings == ["m.md: unbacked numeric literal '0.8' in math"]


def test_math_decimal_result_is_flagged() -> None:
    findings = scan_hard_coded_claims({"g.md": "With $\\gamma=0.9$ mean is $0.95$."})
    assert len(findings) == 2
    assert all(f.endswith("in math") for f in findings)


def test_structural_identity_and_tokens_pass() -> None:
    chapters = {
        "s.md": (
            "Since $Z_{ii}=1$ and $a\\in[0,1]$, the two-role weighting holds. "
            "The suite ran ${total_test_count} checks."
        )
    }
    assert scan_hard_coded_claims(chapters) == []


def test_injected_kappa_weights_pass() -> None:
    chapters = {
        "k.md": (
            "$$\\kappa(D)=N_{\\mathrm{lex}}+${complexity_weight_cups}"
            "N_{\\mathrm{cup}}+${complexity_weight_caps}N_{\\mathrm{cap}}"
            "+${complexity_weight_depth}d(D).$$"
        )
    }
    assert scan_hard_coded_claims(chapters) == []


def test_component_labels_are_exempt_but_evidence_counts_are_not() -> None:
    chapters = {
        "n.md": (
            "The N400 and P600 inspired proxies echo C51 and PCG64 names, "
            "while sample E6 remains a supplied label."
        )
    }
    findings = scan_hard_coded_claims(chapters)
    assert any("'6'" in finding for finding in findings)
    assert not any("N400" in finding or "P600" in finding for finding in findings)
    assert not any("'400'" in finding or "'600'" in finding for finding in findings)


def test_token_values_are_invisible_to_scanner() -> None:
    chapters = {"t.md": "Result is ${exp_filter_posterior_accuracy_mean} nats."}
    assert scan_hard_coded_claims(chapters) == []


# ---------------------------------------------------------------------------
# Variables manifest
# ---------------------------------------------------------------------------


def test_manifest_roundtrip_validates(gate_tree: Path) -> None:
    from src.manuscript_variables import validate_variables_manifest

    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    manifest = validate_variables_manifest(gate_tree, metrics)
    assert manifest["schema"] == "ccd-manuscript-variables-v1"
    assert set(manifest["variables"]) == set(metrics)


def test_missing_manifest_rejected(gate_tree: Path) -> None:
    from src.manuscript_variables import validate_variables_manifest

    (gate_tree / "output" / "manuscript_variables.json").unlink()
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    with pytest.raises(FileNotFoundError):
        validate_variables_manifest(gate_tree, metrics)


def test_tampered_manifest_rejected(gate_tree: Path) -> None:
    from src.manuscript_variables import validate_variables_manifest

    path = gate_tree / "output" / "manuscript_variables.json"
    manifest = json.loads(path.read_text())
    manifest["variables"]["total_test_count"]["value"] = "999"
    path.write_text(json.dumps(manifest))
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    with pytest.raises(ValueError, match="stale"):
        validate_variables_manifest(gate_tree, metrics)


def test_manifest_rebinds_after_regeneration(gate_tree: Path) -> None:
    from src.manuscript_variables import validate_variables_manifest

    path = gate_tree / "output" / "manuscript_variables.json"
    manifest = json.loads(path.read_text())
    manifest["variables"]["total_test_count"]["value"] = "999"
    path.write_text(json.dumps(manifest))
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    write_variables_manifest(gate_tree, metrics)
    assert validate_variables_manifest(gate_tree, metrics)["schema"] == (
        "ccd-manuscript-variables-v1"
    )


def test_spec_by_name_lookup() -> None:
    assert spec_by_name("total_figures") is not None
    assert spec_by_name("no_such_variable") is None
