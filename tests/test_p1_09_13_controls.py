"""P1-09/P1-13 acceptance controls: finite/invalid/extreme cases (real numerics)."""
import numpy as np
import pytest

from src.case_systems.case_category import CaseCategory, CaseRole, Morphism
from src.daif.prediction import n400_from_return_distribution, p600_from_precision_update
from src.daif.types import DistributionalReturn


def _category():
    cat = CaseCategory(name="Ctl")
    for role in (CaseRole.NOM, CaseRole.ACC):
        cat.add_role(role)
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on"))
    return cat


def _dist(mean):
    return DistributionalReturn(mean=mean, variance=0.0,
                                quantiles=np.array([mean]), quantile_levels=np.array([0.5]))


class TestP1_09SurprisalValidation:
    def test_ordinary_values_unchanged(self):
        cat = _category()
        out = cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), 0.5)
        assert out == {"N400_amplitude": 0.5, "P600_amplitude": 0.0}
        assert cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), 0.0)["N400_amplitude"] == 1.0
        assert cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), 1.0)["N400_amplitude"] == 0.0

    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf"), -1.0, 1.5, -0.1])
    def test_invalid_predicted_weight_raises(self, bad):
        cat = _category()
        with pytest.raises(ValueError, match="predicted_weight"):
            cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), bad)

    def test_boundaries_accepted(self):
        cat = _category()
        assert cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), 0.0)["N400_amplitude"] == 1.0
        assert cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.ACC, "x"), 1.0)["N400_amplitude"] == 0.0

    def test_structurally_unlicensed_flag_unchanged(self):
        cat = _category()
        out = cat.assess_daif_surprisal(Morphism(CaseRole.NOM, CaseRole.DAT, "x"), 0.5)
        assert out["P600_amplitude"] == 1.0


class TestP1_13N400FiniteContract:
    def test_ordinary_value_unchanged(self):
        assert n400_from_return_distribution(_dist(0.5), 0.0, 1.0, 1.0) == -0.5

    def test_representable_extreme_computes(self):
        assert n400_from_return_distribution(_dist(1e300), -1e300, 1.0, 1.0) == -2e300

    def test_overflow_raises_valueerror(self):
        m = float(np.finfo(np.float64).max)
        with pytest.raises(ValueError, match="not representable"):
            n400_from_return_distribution(_dist(m), -m, 1.0, 1.0)

    def test_zero_factor_exact_zero(self):
        assert n400_from_return_distribution(_dist(1e300), -1e300, 0.0, 1.0) == 0.0


class TestP1_13P600FiniteContract:
    def test_ordinary_value_unchanged(self):
        assert p600_from_precision_update(0.0, 1.0, 2.0, 1.0, 1.0) == 2.0
        assert p600_from_precision_update(1.0, 1.0, 2.0) == 0.0

    def test_representable_extreme_computes(self):
        assert p600_from_precision_update(0.0, 1e150, 1e150, 1.0, 1.0) == np.float64(1e150) ** 2

    def test_overflow_raises_valueerror(self):
        with pytest.raises(ValueError, match="not representable"):
            p600_from_precision_update(0.0, 1e308, 1e308, 1e308, 1.0)

    def test_zero_severity_exact_zero(self):
        assert p600_from_precision_update(0.0, 1e308, 1e308, 1e308, 0.0) == 0.0
