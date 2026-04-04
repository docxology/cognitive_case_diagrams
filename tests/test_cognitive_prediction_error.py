"""Tests for the prediction_error module — PE and P600 ERP predictions.

All tests use real numpy computations — no mocks.
"""

import pytest

from src.cognitive.prediction_error import prediction_error, p600_amplitude_ratio


class TestPredictionError:
    """Tests for prediction error computation."""

    def test_high_weight_high_error(self) -> None:
        """High-weight morphism produces large PE."""
        assert prediction_error(0.9, 1.0, 0.0) == pytest.approx(0.9)

    def test_low_weight_low_error(self) -> None:
        """Low-weight morphism produces small PE."""
        assert prediction_error(0.2, 1.0, 0.0) == pytest.approx(0.2)

    def test_no_mismatch_zero_error(self) -> None:
        """Zero deviation → zero PE."""
        assert prediction_error(0.9, 0.5, 0.5) == pytest.approx(0.0)

    def test_invalid_weight_raises(self) -> None:
        """Weight outside [0,1] raises ValueError."""
        with pytest.raises(ValueError):
            prediction_error(1.5, 1.0, 0.0)

    def test_negative_weight_raises(self) -> None:
        """Negative weight raises ValueError."""
        with pytest.raises(ValueError):
            prediction_error(-0.1, 1.0, 0.0)

    def test_boundary_weight_zero(self) -> None:
        """Weight=0.0 produces zero PE."""
        assert prediction_error(0.0, 100.0, 0.0) == pytest.approx(0.0)

    def test_boundary_weight_one(self) -> None:
        """Weight=1.0 produces PE equal to absolute deviation."""
        assert prediction_error(1.0, 3.0, 1.0) == pytest.approx(2.0)

    def test_proportional_to_weight(self) -> None:
        """PE ratio approximates weight ratio (P600 prediction)."""
        pe_strong = prediction_error(0.9, 1.0, 0.0)
        pe_weak = prediction_error(0.4, 1.0, 0.0)
        assert pe_strong / pe_weak == pytest.approx(0.9 / 0.4)


class TestP600AmplitudeRatio:
    """Tests for P600 amplitude ratio prediction."""

    def test_computation(self) -> None:
        """Ratio of weights predicts P600 ratio."""
        assert p600_amplitude_ratio(0.9, 0.4) == pytest.approx(0.9 / 0.4)

    def test_equal_weights(self) -> None:
        """Equal weights → ratio of 1."""
        assert p600_amplitude_ratio(0.5, 0.5) == pytest.approx(1.0)

    def test_zero_weak_weight_raises(self) -> None:
        """Zero weak weight raises ValueError."""
        with pytest.raises(ValueError):
            p600_amplitude_ratio(0.5, 0.0)

    def test_strong_out_of_range_raises(self) -> None:
        """Strong weight > 1.0 raises ValueError."""
        with pytest.raises(ValueError):
            p600_amplitude_ratio(1.5, 0.5)
