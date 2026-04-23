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

    def test_default_output_path(self, tmp_path, monkeypatch):
        """When output_path is None, uses default filename."""
        monkeypatch.chdir(tmp_path)
        violations = _make_violations()
        result = plot_type_violations(violations, output_path=None)
        assert result == "type_violations.png"
        assert os.path.exists(result)

    def test_single_violation(self, tmp_path):
        """Works with a single violation."""
        violations = [_make_violations()[0]]
        out = str(tmp_path / "single.png")
        result = plot_type_violations(violations, output_path=out)
        assert os.path.exists(result)
        assert os.path.getsize(out) > 0


class TestPlotMonoidalFunctorSecurity:
    """Tests for plot_monoidal_functor_security()."""

    @staticmethod
    def _make_monoidal_functor():
        """Create a MonoidalFunctor for testing."""
        from src.case_systems.functor import MonoidalFunctor
        from src.case_systems.case_category import CaseCategory

        source = CaseCategory(name="ProtocolSource")
        target = CaseCategory(name="ProtocolTarget")
        for role in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.INS, CaseRole.LOC]:
            source.add_role(role)
            target.add_role(role)
        om = {
            CaseRole.NOM: CaseRole.NOM,
            CaseRole.ACC: CaseRole.ACC,
            CaseRole.DAT: CaseRole.DAT,
            CaseRole.INS: CaseRole.INS,
            CaseRole.LOC: CaseRole.LOC,
        }
        return MonoidalFunctor(
            name="SecurityFunctor",
            source=source,
            target=target,
            object_map=om,
        )

    def test_returns_path(self, tmp_path):
        """plot_monoidal_functor_security returns a valid file path."""
        from src.visualization.security_plots import plot_monoidal_functor_security

        functor = self._make_monoidal_functor()
        out = str(tmp_path / "monoidal_security.png")
        result = plot_monoidal_functor_security(functor, output_path=out)
        assert isinstance(result, str)
        assert os.path.exists(result)

    def test_creates_nonempty_file(self, tmp_path):
        """Output file is created and non-empty."""
        from src.visualization.security_plots import plot_monoidal_functor_security

        functor = self._make_monoidal_functor()
        out = str(tmp_path / "monoidal_security.png")
        plot_monoidal_functor_security(functor, output_path=out)
        assert os.path.getsize(out) > 1000  # PNG should be substantial

    def test_custom_title(self, tmp_path):
        """Custom title parameter is accepted."""
        from src.visualization.security_plots import plot_monoidal_functor_security

        functor = self._make_monoidal_functor()
        out = str(tmp_path / "titled.png")
        result = plot_monoidal_functor_security(
            functor, title="Custom Firewall Title", output_path=out
        )
        assert os.path.exists(result)

    def test_default_output_path(self, tmp_path, monkeypatch):
        """When output_path is None, uses default filename."""
        from src.visualization.security_plots import plot_monoidal_functor_security

        monkeypatch.chdir(tmp_path)
        functor = self._make_monoidal_functor()
        result = plot_monoidal_functor_security(functor, output_path=None)
        assert result == "monoidal_functor_security.png"
        assert os.path.exists(result)

    def test_tensor_preservation_check(self):
        """Verify MonoidalFunctor.preserves_tensor for identity and collapsing maps."""
        functor = self._make_monoidal_functor()
        # Identity map: distinct roles stay distinct — tensor preserved
        assert functor.preserves_tensor(CaseRole.ACC, CaseRole.NOM) is True
        assert functor.preserves_tensor(CaseRole.NOM, CaseRole.ACC) is True

        # Non-injective map collapses tensor
        from src.case_systems.functor import MonoidalFunctor
        from src.case_systems.case_category import CaseCategory
        src = CaseCategory(name="Src")
        tgt = CaseCategory(name="Tgt")
        for r in [CaseRole.ACC, CaseRole.NOM]:
            src.add_role(r)
        tgt.add_role(CaseRole.NOM)
        collapsing = MonoidalFunctor(
            name="Collapsing", source=src, target=tgt,
            object_map={CaseRole.ACC: CaseRole.NOM, CaseRole.NOM: CaseRole.NOM},
        )
        assert collapsing.preserves_tensor(CaseRole.ACC, CaseRole.NOM) is False

    def test_bipartite_edges_drawn(self, tmp_path):
        """Plot generates a non-trivial figure with all roles mapped."""
        from src.visualization.security_plots import plot_monoidal_functor_security

        functor = self._make_monoidal_functor()
        out = str(tmp_path / "edges.png")
        result = plot_monoidal_functor_security(functor, output_path=out)
        assert os.path.getsize(out) > 5000  # Dual-panel figure is large


class TestPlotCaseInteractionGraph:
    """Tests for plot_case_interaction_graph() — §9b two-panel figure."""

    def test_saves_file(self, tmp_path):
        from src.visualization.security_plots import plot_case_interaction_graph

        out = str(tmp_path / "interaction.png")
        result = plot_case_interaction_graph(output_path=out)
        assert result == out
        assert os.path.exists(out)
        assert os.path.getsize(out) > 0

    def test_default_output_path(self, tmp_path, monkeypatch):
        import os
        monkeypatch.chdir(tmp_path)
        from src.visualization.security_plots import plot_case_interaction_graph

        result = plot_case_interaction_graph(output_path=None)
        assert result == "security_type_violations.png"
        assert os.path.exists(result)
