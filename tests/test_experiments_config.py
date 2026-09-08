"""Config contract tests for src.experiments (real validation, no mocks).

The tests pin the intended public API: strict typed validation (both through
``from_dict`` and through direct dataclass construction followed by
``validate()``), exact round-trips, resource caps tied to the actual
``CaseRole`` population, and the single top-level confidence level that
drives every interval.
"""
from __future__ import annotations

import json

import pytest

from src.case_systems.case_category import CaseRole
from src.experiments import (
    ConfigError,
    ExperimentConfig,
    FilteringConfig,
    ProjectionConfig,
    QuantileConfig,
    SensitivityConfig,
    canonical_config_json,
    config_sha256,
    load_config,
    save_config,
)

_N_ROLES = len(list(CaseRole))


def test_default_config_validates():
    config = ExperimentConfig()
    config.validate()  # must not raise
    assert config.n_replicates >= 2
    assert 0.0 < config.confidence_level < 1.0


def test_round_trip_is_exact():
    config = ExperimentConfig.from_dict({
        "seed": 7,
        "n_replicates": 16,
        "confidence_level": 0.9,
        "filtering": {"n_roles": 4, "evidence_strength": 0.5},
        "projection": {"atom_counts": [5, 9]},
    })
    restored = ExperimentConfig.from_dict(config.to_dict())
    assert restored.to_dict() == config.to_dict()
    assert canonical_config_json(config) == canonical_config_json(restored)


def test_canonical_json_is_order_insensitive():
    a = ExperimentConfig.from_dict({"seed": 1, "n_replicates": 4})
    b = ExperimentConfig.from_dict({"n_replicates": 4, "seed": 1})
    assert canonical_config_json(a) == canonical_config_json(b)
    assert config_sha256(a) == config_sha256(b)
    assert len(config_sha256(a)) == 64


def test_unknown_top_level_key_rejected():
    with pytest.raises(ConfigError, match="Unknown keys in config"):
        ExperimentConfig.from_dict({"seeds": 1})


def test_unknown_section_key_rejected():
    with pytest.raises(ConfigError, match="Unknown keys in calibration"):
        ExperimentConfig.from_dict({"calibration": {"confidence_level": 0.95}})


def test_non_mapping_config_rejected():
    with pytest.raises(ConfigError, match="must be a mapping"):
        ExperimentConfig.from_dict([1, 2, 3])


def test_none_section_rejected():
    with pytest.raises(ConfigError):
        ExperimentConfig.from_dict({"filtering": None})


@pytest.mark.parametrize("payload", [
    {"seed": True},
    {"seed": 2**64},
    {"n_replicates": 1},
    {"n_replicates": "many"},
    {"n_replicates": 100_001},
    {"confidence_level": 0.0},
    {"confidence_level": 1.0},
    {"confidence_level": 1.5},
    {"confidence_level": True},
])
def test_invalid_global_fields_rejected(payload):
    with pytest.raises(ConfigError):
        ExperimentConfig.from_dict(payload)


@pytest.mark.parametrize("payload", [
    {"filtering": {"n_roles": 1}},
    {"filtering": {"n_roles": _N_ROLES + 1}},
    {"filtering": {"evidence_strength": 1.5}},
    {"calibration": {"n_levels": 1}},
    {"calibration": {"n_levels": 201}},
    {"calibration": {"n_observations": 0}},
    {"quantile": {"learning_rate": 0.0}},
    {"quantile": {"kappa": 0.0}},
    {"quantile": {"wasserstein_p": 3}},
    {"quantile": {"brute_force_tau_points": 100}},
    {"projection": {"atom_counts": [1, 5]}},
    {"projection": {"atom_counts": [5, 5]}},
    {"projection": {"atom_counts": [0, 5]}},
    {"projection": {"v_min": 1.0, "v_max": -1.0}},
    {"sensitivity": {"gammas": [0.1, 1.5]}},
    {"sensitivity": {"entropy_bins": [1, 50]}},
    {"sensitivity": {"temperatures": [0.0, 1.0]}},
])
def test_invalid_section_fields_rejected(payload):
    with pytest.raises(ConfigError):
        ExperimentConfig.from_dict(payload)


def test_n_roles_cap_matches_case_role_population():
    # The maximum admissible role count is the actual CaseRole population.
    ExperimentConfig.from_dict({"filtering": {"n_roles": _N_ROLES}}).validate()


def test_resource_caps_bind_list_lengths():
    with pytest.raises(ConfigError, match="at most 8"):
        ExperimentConfig.from_dict(
            {"projection": {"atom_counts": [2 * k + 3 for k in range(9)]}})


def test_enabled_sections_follow_flags_and_order():
    config = ExperimentConfig.from_dict({
        "filtering": {"enabled": False},
        "calibration": {"enabled": False},
        "quantile": {"enabled": False},
        "projection": {"enabled": False},
        "sensitivity": {"enabled": False},
        "sanity": {"enabled": False},
    })
    assert config.enabled_sections() == []
    default = ExperimentConfig()
    assert default.enabled_sections() == [
        "filtering", "calibration", "quantile", "projection",
        "sensitivity", "sanity",
    ]


# --------------------------------------------------------------------------
# Direct dataclass construction must satisfy the same validation contract
# as from_dict; validate() is the enforcement point.
# --------------------------------------------------------------------------
def test_direct_dataclass_negative_controls():
    with pytest.raises(ConfigError):
        ExperimentConfig(seed=2**64).validate()
    with pytest.raises(ConfigError):
        ExperimentConfig(n_replicates=1).validate()
    with pytest.raises(ConfigError):
        ExperimentConfig(confidence_level=1.0).validate()
    with pytest.raises(ConfigError):
        FilteringConfig(n_roles=1).validate()
    with pytest.raises(ConfigError):
        FilteringConfig(n_roles=_N_ROLES + 1).validate()
    with pytest.raises(ConfigError):
        FilteringConfig(evidence_strength=-0.1).validate()
    with pytest.raises(ConfigError):
        FilteringConfig(n_iterations=0).validate()
    with pytest.raises(ConfigError):
        SensitivityConfig(temperatures=[0.0]).validate()
    with pytest.raises(ConfigError):
        QuantileConfig(learning_rate=0.0).validate()
    with pytest.raises(ConfigError):
        QuantileConfig(wasserstein_p=3).validate()
    with pytest.raises(ConfigError):
        ProjectionConfig(atom_counts=[5, 5]).validate()
    with pytest.raises(ConfigError):
        ProjectionConfig(v_min=2.0, v_max=1.0).validate()


@pytest.mark.parametrize("section", ["filtering", "calibration", "quantile",
                                     "projection", "sensitivity", "sanity"])
def test_enabled_must_be_boolean(section):
    cls = {
        "filtering": FilteringConfig,
        "calibration": __import__(
            "src.experiments.config", fromlist=["CalibrationConfig"]).CalibrationConfig,
        "quantile": QuantileConfig,
        "projection": ProjectionConfig,
        "sensitivity": SensitivityConfig,
        "sanity": __import__(
            "src.experiments.config", fromlist=["SanityConfig"]).SanityConfig,
    }[section]
    with pytest.raises(ConfigError):
        instance = cls(enabled="yes")  # type: ignore[arg-type]
        instance.validate()


def test_save_and_load_round_trip(tmp_path):
    config = ExperimentConfig.from_dict({"seed": 11, "n_replicates": 8})
    path = save_config(config, tmp_path / "nested" / "config.json")
    loaded = load_config(path)
    assert loaded.to_dict() == config.to_dict()
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["seed"] == 11


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path / "absent.json")


def test_load_malformed_file_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="not valid JSON"):
        load_config(path)
