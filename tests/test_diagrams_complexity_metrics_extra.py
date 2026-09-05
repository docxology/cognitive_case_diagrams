"""Tests for DiagramMetrics dataclass and complexity_metrics module."""

from src.diagrams.complexity_metrics import (
    DISCOPY_AVAILABLE,
    DiagramMetrics,
)


class TestDiagramMetricsDataclass:
    def test_default_instantiation(self):
        m = DiagramMetrics(name="test")
        assert m.name == "test"
        assert m.box_count == 0
        assert m.word_count == 0
        assert m.cup_count == 0
        assert m.cap_count == 0
        assert m.is_normal_form is False
        assert m.normal_form_box_count == 0
        assert m.dom_type == ""
        assert m.cod_type == ""
        assert m.depth == 0
        assert m.width == 0

    def test_explicit_values(self):
        m = DiagramMetrics(
            name="Alice chases Bob",
            box_count=3,
            word_count=2,
            cup_count=1,
            cap_count=0,
            is_normal_form=True,
            normal_form_box_count=2,
            dom_type="n ⊗ n",
            cod_type="s",
            depth=2,
            width=3,
        )
        assert m.box_count == 3
        assert m.word_count == 2
        assert m.cup_count == 1
        assert m.is_normal_form is True
        assert m.cod_type == "s"
        assert m.depth == 2

    def test_equality(self):
        m1 = DiagramMetrics(name="x", box_count=5)
        m2 = DiagramMetrics(name="x", box_count=5)
        assert m1 == m2

    def test_inequality(self):
        m1 = DiagramMetrics(name="x", box_count=3)
        m2 = DiagramMetrics(name="x", box_count=4)
        assert m1 != m2


class TestDiscopyAvailabilityFlag:
    def test_flag_is_bool(self):
        assert isinstance(DISCOPY_AVAILABLE, bool)

    def test_discopy_is_available_in_this_env(self):
        """discopy 1.2.2 is installed; DISCOPY_AVAILABLE must be True."""
        assert DISCOPY_AVAILABLE is True

    def test_count_boxes_is_callable(self):
        from src.diagrams.complexity_metrics import count_boxes
        assert callable(count_boxes)

    def test_count_boxes_on_real_diagram(self):
        from discopy.rigid import Ty, Box, Cup, Id
        from src.diagrams.complexity_metrics import count_boxes
        n, s = Ty("n"), Ty("s")
        diagram = Box("Alice", Ty(), n) @ Box("runs", Ty(), n.r @ s) >> Cup(n, n.r) @ Id(s)
        assert count_boxes(diagram) == 3  # Alice, runs, Cup


class TestComplexityExamplesModuleImport:
    def test_module_is_importable(self):
        import src.diagrams.complexity_examples as ce
        assert hasattr(ce, 'build_complexity_examples')
        assert callable(ce.build_complexity_examples)

    def test_build_returns_ten_examples(self):
        from src.diagrams.complexity_examples import build_complexity_examples
        examples = build_complexity_examples()
        assert len(examples) == 10
        for label, diagram in examples:
            assert isinstance(label, str) and label

    def test_build_examples_increasing_complexity(self):
        from src.diagrams.complexity_metrics import count_cups
        from src.diagrams.complexity_examples import build_complexity_examples
        examples = build_complexity_examples()
        cup_counts = [count_cups(d) for _, d in examples]
        # Cup count must be non-decreasing (complexity increases)
        assert cup_counts == sorted(cup_counts)


class TestDiscopyDiagramsUtilities:
    def test_resolve_path_none_uses_default(self):
        from pathlib import Path
        from src.visualization.discopy_diagrams import _resolve_path
        result = _resolve_path(None, "default.png")
        assert result == Path("default.png")

    def test_resolve_path_string_returns_path(self):
        from pathlib import Path
        from src.visualization.discopy_diagrams import _resolve_path
        result = _resolve_path("/tmp/out.png", "default.png")
        assert result == Path("/tmp/out.png")

    def test_glyph_safe_rc_context_manager_does_not_raise(self):
        from src.visualization.discopy_diagrams import _glyph_safe_rc
        with _glyph_safe_rc():
            pass  # confirm context manager enters and exits cleanly
