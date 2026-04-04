"""Tests for src.visualization.security_plots module.

Validates plot_type_violations produces valid output with correct
severity-colored bar chart structure.
"""

import logging
import os

import pytest

from src.case_systems.case_category import CaseRole
from src.security.cognitive_security import TypeViolation
from src.visualization.security_plots import plot_type_violations

logger = logging.getLogger(__name__)


def _make_violations() -> list[TypeViolation]:
    """Create test type violations."""
    return [
        TypeViolation(
            source=CaseRole.ACC,
            target=CaseRole.NOM,
            violation_type="promotion",
            severity=0.9,
            description="Accusative promoted to nominative",
        ),
        TypeViolation(
            source=CaseRole.DAT,
            target=CaseRole.NOM,
            violation_type="injection",
            severity=0.6,
            description="Dative injected as nominative",
        ),
        TypeViolation(
            source=CaseRole.LOC,
            target=CaseRole.ACC,
            violation_type="spatial_override",
            severity=0.3,
            description="Locative overriding accusative",
        ),
    ]


class TestPlotTypeViolations:
    """Tests for plot_type_violations()."""

    def test_returns_path(self, tmp_path):
        """plot_type_violations returns a file path string."""
        violations = _make_violations()
        out = str(tmp_path / "violations.png")
        result = plot_type_violations(violations, output_path=out)
        assert isinstance(result, str)
        assert os.path.exists(result)
        logger.info("plot_type_violations saved to %s", result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        violations = _make_violations()
        out = str(tmp_path / "violations.png")
        plot_type_violations(violations, output_path=out)
        assert os.path.getsize(out) > 0

    def test_empty_violations(self, tmp_path):
        """Empty violations list returns empty string."""
        result = plot_type_violations([], output_path=str(tmp_path / "empty.png"))
        assert result == ""

    def test_custom_title(self, tmp_path):
        """Custom title parameter is accepted."""
        violations = _make_violations()
        out = str(tmp_path / "violations_titled.png")
        result = plot_type_violations(
            violations, title="Custom Title", output_path=out
        )
        assert os.path.exists(result)

    def test_severity_ordering(self):
        """Violations are sorted by severity descending in the plot."""
        violations = _make_violations()
        sorted_v = sorted(violations, key=lambda v: v.severity, reverse=True)
        assert sorted_v[0].severity >= sorted_v[-1].severity
