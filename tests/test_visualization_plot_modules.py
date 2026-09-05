"""Tests for visualization plot entrypoints (coverage backfill / smoke layer).

Per-module behavior is owned by ``test_visualization_<module>.py``. This file
adds redundant exercise of the same entrypoints with real PNG I/O so branch
and guard paths stay covered as matplotlib helpers evolve.

Covers (non-exhaustive):
    - active_inference_plots.plot_belief_distribution
    - quantum_plots.plot_povm_probabilities
    - security_plots.plot_type_violations
    - fluid_s_plots.plot_fluid_s_volition_landscape
    - functor_diagrams.render_functor_diagram

All tests use real mathematical objects (no mocks) and real file I/O with
tempfile, verifying files are created and non-empty. Prefer canonical imports
from ``src.case_systems`` / ``src.security`` etc. rather than reusing names
re-bound inside other modules.
"""

import os
import tempfile

import numpy as np

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.quantum.quantum_case import crisp_case_povm, semantic_state
from src.security.cognitive_security import TypeViolation
from src.case_systems.fluid_s import create_fluid_s_functor
from src.visualization.active_inference_plots import plot_belief_distribution
from src.visualization.quantum_plots import plot_povm_probabilities
from src.visualization.security_plots import plot_type_violations
from src.visualization.fluid_s_plots import plot_fluid_s_volition_landscape


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tmp_png() -> tuple:
    """Return (path, cleanup_fn) for a temporary PNG file."""
    f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    f.close()
    return f.name, lambda: os.path.exists(f.name) and os.unlink(f.name)


def _basic_belief(roles=None, probs=None) -> CaseDiagramBelief:
    """Create a minimal CaseDiagramBelief for testing."""
    roles = roles or [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
    n = len(roles)
    probs = np.array(probs or [1.0 / n] * n)
    return CaseDiagramBelief(roles=roles, probabilities=probs)


def _two_role_povm() -> tuple:
    """Return (CasePOVM, state_vector) for NOM/ACC crisp case."""
    roles = [CaseRole.NOM, CaseRole.ACC]
    povm = crisp_case_povm(roles)
    # NOM-dominant state: mostly |0>
    rho = semantic_state({CaseRole.NOM: 0.8, CaseRole.ACC: 0.2}, roles=roles)
    return povm, rho


# ---------------------------------------------------------------------------
# active_inference_plots
# ---------------------------------------------------------------------------

class TestPlotBeliefDistribution:
    """Tests for plot_belief_distribution (active_inference_plots)."""

    def test_renders_to_file_uniform(self) -> None:
        """Uniform belief distribution renders and saves to a PNG file."""
        path, cleanup = _tmp_png()
        try:
            belief = _basic_belief()
            result = plot_belief_distribution(belief, output_path=path)
            assert result == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            cleanup()

    def test_renders_to_file_peaked(self) -> None:
        """Peaked belief (most probability on NOM) renders correctly."""
        path, cleanup = _tmp_png()
        try:
            belief = CaseDiagramBelief(
                roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
                probabilities=np.array([0.8, 0.1, 0.1]),
            )
            result = plot_belief_distribution(belief, title="Peaked NOM Belief", output_path=path)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            cleanup()

    def test_renders_two_roles(self) -> None:
        """Two-role belief (NOM/ACC) renders without errors."""
        path, cleanup = _tmp_png()
        try:
            belief = CaseDiagramBelief(
                roles=[CaseRole.NOM, CaseRole.ACC],
                probabilities=np.array([0.6, 0.4]),
            )
            result = plot_belief_distribution(belief, output_path=path)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 1000  # real PNG bytes
        finally:
            cleanup()

    def test_renders_all_eight_cases(self) -> None:
        """All 8 standard case roles render without error."""
        path, cleanup = _tmp_png()
        try:
            roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
                     CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC]
            probs = np.ones(8) / 8.0
            belief = CaseDiagramBelief(roles=roles, probabilities=probs)
            result = plot_belief_distribution(belief, output_path=path)
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_default_output_path_is_returned(self) -> None:
        """When output_path is None, returns an auto-generated path string."""
        belief = _basic_belief()
        result = plot_belief_distribution(belief)
        # Should return a string path (auto-generated)
        assert isinstance(result, str)
        assert len(result) > 0
        # Cleanup auto-generated file if it exists
        if os.path.exists(result):
            os.unlink(result)

    def test_custom_title_accepted(self) -> None:
        """Custom title string does not cause errors."""
        path, cleanup = _tmp_png()
        try:
            belief = _basic_belief()
            result = plot_belief_distribution(
                belief,
                title="ERP Prediction Error: NOM vs ACC",
                output_path=path,
            )
            assert os.path.exists(result)
        finally:
            cleanup()


# ---------------------------------------------------------------------------
# quantum_plots
# ---------------------------------------------------------------------------

class TestPlotPOVMProbabilities:
    """Tests for plot_povm_probabilities (quantum_plots)."""

    def _nom_dominant_rho(self) -> np.ndarray:
        """2×2 density matrix with NOM probability 0.8, ACC 0.2."""
        return np.diag([0.8, 0.2]).astype(np.complex128)

    def _acc_dominant_rho(self) -> np.ndarray:
        """2×2 density matrix with ACC probability 0.9, NOM 0.1."""
        return np.diag([0.1, 0.9]).astype(np.complex128)

    def _mixed_rho(self) -> np.ndarray:
        """2×2 maximally mixed density matrix (equal NOM/ACC)."""
        return np.diag([0.5, 0.5]).astype(np.complex128)

    def test_renders_crisp_povm_to_file(self) -> None:
        """Crisp NOM/ACC POVM with NOM-dominant state renders to PNG."""
        path, cleanup = _tmp_png()
        try:
            roles = [CaseRole.NOM, CaseRole.ACC]
            povm = crisp_case_povm(roles)
            rho = self._nom_dominant_rho()
            result = plot_povm_probabilities(povm, rho, output_path=path)
            assert result == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            cleanup()

    def test_renders_nom_dominant_state(self) -> None:
        """NOM-dominant density matrix produces valid bar chart PNG."""
        path, cleanup = _tmp_png()
        try:
            roles = [CaseRole.NOM, CaseRole.ACC]
            povm = crisp_case_povm(roles)
            rho = self._nom_dominant_rho()
            result = plot_povm_probabilities(
                povm, rho, title="Pure NOM State", output_path=path
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 1000
        finally:
            cleanup()

    def test_renders_acc_dominant_state(self) -> None:
        """ACC-dominant density matrix produces valid bar chart PNG."""
        path, cleanup = _tmp_png()
        try:
            roles = [CaseRole.NOM, CaseRole.ACC]
            povm = crisp_case_povm(roles)
            rho = self._acc_dominant_rho()
            result = plot_povm_probabilities(
                povm, rho, title="ACC-Dominant State", output_path=path
            )
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_default_output_path(self) -> None:
        """Auto-generated output path is returned as a string."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        rho = self._mixed_rho()
        result = plot_povm_probabilities(povm, rho)
        assert isinstance(result, str)
        if os.path.exists(result):
            os.unlink(result)

    def test_mixed_state_renders(self) -> None:
        """Maximally mixed density matrix renders without error."""
        path, cleanup = _tmp_png()
        try:
            roles = [CaseRole.NOM, CaseRole.ACC]
            povm = crisp_case_povm(roles)
            rho = self._mixed_rho()
            result = plot_povm_probabilities(povm, rho, output_path=path)
            assert os.path.exists(result)
        finally:
            cleanup()


# ---------------------------------------------------------------------------
# security_plots
# ---------------------------------------------------------------------------

class TestPlotTypeViolations:
    """Tests for plot_type_violations (security_plots)."""

    def _make_violations(self, n: int = 2) -> list:
        """Create n TypeViolation objects with varying severity."""
        roles = [(CaseRole.NOM, CaseRole.ACC),
                 (CaseRole.ACC, CaseRole.DAT),
                 (CaseRole.INS, CaseRole.NOM),
                 (CaseRole.LOC, CaseRole.GEN)]
        violations = []
        for i in range(n):
            src, tgt = roles[i % len(roles)]
            violations.append(TypeViolation(
                source=src,
                target=tgt,
                violation_type="missing_morphism",
                severity=0.4 + 0.2 * i,
                description=f"Test violation {i}: {src.name}→{tgt.name}",
            ))
        return violations

    def test_renders_single_violation(self) -> None:
        """A single TypeViolation renders to a PNG successfully."""
        path, cleanup = _tmp_png()
        try:
            violations = self._make_violations(1)
            result = plot_type_violations(violations, output_path=path)
            assert result == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            cleanup()

    def test_renders_multiple_violations(self) -> None:
        """Multiple violations with different severities render correctly."""
        path, cleanup = _tmp_png()
        try:
            violations = self._make_violations(3)
            result = plot_type_violations(violations, title="Prompt Injection Analysis", output_path=path)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 1000
        finally:
            cleanup()

    def test_empty_violations_returns_empty_string(self) -> None:
        """Empty violations list returns empty string (no plot generated)."""
        result = plot_type_violations([])
        assert result == ""

    def test_high_severity_violation(self) -> None:
        """Critical severity (1.0) violation renders without error."""
        path, cleanup = _tmp_png()
        try:
            violations = [TypeViolation(
                source=CaseRole.ACC,
                target=CaseRole.NOM,
                violation_type="case_promotion",
                severity=1.0,
                description="ACC→NOM promotion: critical injection",
            )]
            result = plot_type_violations(violations, output_path=path)
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_medium_severity_violation(self) -> None:
        """Medium severity (0.5) violation renders correctly."""
        path, cleanup = _tmp_png()
        try:
            violations = [TypeViolation(
                source=CaseRole.INS,
                target=CaseRole.NOM,
                violation_type="missing_morphism",
                severity=0.5,
                description="INS→NOM: potential escalation",
            )]
            result = plot_type_violations(violations, output_path=path)
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_default_output_path(self) -> None:
        """Auto-generated output path returned as non-empty string."""
        violations = self._make_violations(1)
        result = plot_type_violations(violations)
        assert isinstance(result, str)
        assert len(result) > 0
        if os.path.exists(result):
            os.unlink(result)

    def test_violations_sorted_by_severity(self) -> None:
        """Function runs and renders when violations are unsorted by severity."""
        path, cleanup = _tmp_png()
        try:
            violations = [
                TypeViolation(CaseRole.NOM, CaseRole.ACC, "missing_morphism", 0.3, "low"),
                TypeViolation(CaseRole.ACC, CaseRole.DAT, "case_promotion", 0.9, "high"),
                TypeViolation(CaseRole.INS, CaseRole.LOC, "missing_morphism", 0.6, "medium"),
            ]
            result = plot_type_violations(violations, output_path=path)
            assert os.path.exists(result)
        finally:
            cleanup()


# ---------------------------------------------------------------------------
# fluid_s_plots
# ---------------------------------------------------------------------------

class TestPlotFluidSVolitionLandscape:
    """Tests for plot_fluid_s_volition_landscape (fluid_s_plots)."""

    def _make_functors_and_verbs(self, n: int = 3) -> tuple:
        """Create n FluidSFunctor instances with probabilities and names."""
        probs = [i / (n - 1) if n > 1 else 0.5 for i in range(n)]
        functors = [
            create_fluid_s_functor(volitional=(p >= 0.5), probability=p)
            for p in probs
        ]
        verbs = [f"verb_{i}" for i in range(n)]
        return functors, probs, verbs

    def test_renders_three_verbs_to_file(self) -> None:
        """Three verbs across the volition spectrum render to PNG."""
        path, cleanup = _tmp_png()
        try:
            functors, probs, verbs = self._make_functors_and_verbs(3)
            result = plot_fluid_s_volition_landscape(
                functors, probs, verbs, output_path=path
            )
            assert result == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            cleanup()

    def test_renders_bats_fall_verbs(self) -> None:
        """Renders the canonical Bats 'fall' volitional contrast."""
        path, cleanup = _tmp_png()
        try:
            vol_functor = create_fluid_s_functor(volitional=True, probability=0.9)
            nonvol_functor = create_fluid_s_functor(volitional=False, probability=0.1)
            result = plot_fluid_s_volition_landscape(
                functors=[vol_functor, nonvol_functor],
                probabilities=[0.9, 0.1],
                verb_names=["fall (volitional)", "fall (accidental)"],
                title="Bats Fluid-S Volition Contrast",
                output_path=path,
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 1000
        finally:
            cleanup()

    def test_empty_input_renders_with_defaults(self) -> None:
        """Empty lists still render (new API uses built-in BATS verb data)."""
        result = plot_fluid_s_volition_landscape([], [], [])
        assert isinstance(result, str)
        assert len(result) > 0
        if os.path.exists(result):
            os.unlink(result)

    def test_mismatched_lengths_renders_with_defaults(self) -> None:
        """Mismatched functor/probability lists still render with defaults."""
        f1 = create_fluid_s_functor(probability=0.7)
        result = plot_fluid_s_volition_landscape([f1, f1], [0.7], ["a", "b"])
        assert isinstance(result, str)
        assert len(result) > 0
        if os.path.exists(result):
            os.unlink(result)

    def test_single_verb_renders(self) -> None:
        """Single verb/functor pairing renders without error."""
        path, cleanup = _tmp_png()
        try:
            f = create_fluid_s_functor(volitional=True, probability=0.8)
            result = plot_fluid_s_volition_landscape(
                [f], [0.8], ["jump"], output_path=path
            )
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_uniform_probabilities_render(self) -> None:
        """All-equal probabilities (0.5) render correctly."""
        path, cleanup = _tmp_png()
        try:
            functors = [create_fluid_s_functor(probability=0.5) for _ in range(4)]
            probs = [0.5, 0.5, 0.5, 0.5]
            verbs = ["slide", "drift", "wander", "flow"]
            result = plot_fluid_s_volition_landscape(
                functors, probs, verbs, output_path=path
            )
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_gradient_probabilities_render(self) -> None:
        """Gradient from 0→1 across many verbs renders correctly."""
        path, cleanup = _tmp_png()
        try:
            n = 5
            probs = [i / (n - 1) for i in range(n)]
            functors = [create_fluid_s_functor(probability=p) for p in probs]
            verbs = ["stumble", "slip", "walk", "run", "jump"]
            result = plot_fluid_s_volition_landscape(
                functors, probs, verbs, output_path=path
            )
            assert os.path.exists(result)
        finally:
            cleanup()

    def test_default_output_path(self) -> None:
        """Auto-generated output path returned as non-empty string."""
        functors, probs, verbs = self._make_functors_and_verbs(2)
        result = plot_fluid_s_volition_landscape(functors, probs, verbs)
        assert isinstance(result, str)
        assert len(result) > 0
        if os.path.exists(result):
            os.unlink(result)


# ---------------------------------------------------------------------------
# functor_diagrams — render_functor_diagram arrow rendering path
# ---------------------------------------------------------------------------

class TestRenderFunctorDiagram:
    """Tests for render_functor_diagram (functor_diagrams).

    Covers uncovered lines 56-100: functor arrow rendering between category sides.
    All tests use real AlignmentFunctor objects — no mocks.
    """

    def test_renders_accusative_to_ergative_to_file(self, tmp_path) -> None:
        """Renders accusative-to-ergative functor with arrows to PNG file."""
        from src.case_systems.functor import accusative_to_ergative_functor
        from src.visualization.functor_diagrams import render_functor_diagram
        import matplotlib
        matplotlib.use("Agg")

        out = tmp_path / "functor_arrows.png"
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor, output_path=out)

        assert out.exists()
        assert out.stat().st_size > 0
        import matplotlib.pyplot as plt
        plt.close("all")

    def test_renders_without_output_path(self) -> None:
        """render_functor_diagram returns Figure when no output_path given."""
        from src.case_systems.functor import accusative_to_ergative_functor
        from src.visualization.functor_diagrams import render_functor_diagram
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use("Agg")

        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor)
        assert fig is not None
        plt.close("all")

    def test_renders_tripartite_functor(self, tmp_path) -> None:
        """Renders tripartite functor (3 roles, injective) to PNG file."""
        from src.case_systems.functor import tripartite_functor
        from src.visualization.functor_diagrams import render_functor_diagram
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use("Agg")

        out = tmp_path / "tripartite.png"
        functor = tripartite_functor()
        fig = render_functor_diagram(functor, output_path=out, title="Tripartite Alignment")

        assert out.exists()
        assert out.stat().st_size > 1000
        plt.close("all")

    def test_renders_with_custom_title(self, tmp_path) -> None:
        """Custom title does not raise errors in render_functor_diagram."""
        from src.case_systems.functor import accusative_to_ergative_functor
        from src.visualization.functor_diagrams import render_functor_diagram
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use("Agg")

        out = tmp_path / "custom_title.png"
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor, output_path=out, title="ACC→ERG: Typological Bridge")

        assert fig is not None
        assert out.exists()
        plt.close("all")

