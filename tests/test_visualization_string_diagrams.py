"""Coverage-boosting tests for visualization.string_diagrams module.

Targets uncovered branches: verb-box matching, cup connections with entity
wires, file saving, and discourse diagram rendering edge cases.
"""

import logging
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.case_systems.case_category import CaseRole
from src.diagrams.string_diagram import (
    N, S, Wire, Box, Sentence, Discourse,
)
from src.visualization.string_diagrams import (
    render_discocat_sentence,
    render_discourse_diagram,
    render_discocirc_discourse,
    render_three_sentence_discourse,
)

logger = logging.getLogger(__name__)


class TestRenderDiscocatSentence:
    """Tests for render_discocat_sentence function."""

    def test_basic_intransitive(self):
        """Test rendering an intransitive sentence (no verb matching branches)."""
        s = Sentence.intransitive("Alice", "runs")
        fig = render_discocat_sentence(s)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_transitive_with_cups(self):
        """Test transitive sentence triggers verb-box matching and cup arcs."""
        s = Sentence.transitive("Alice", "chases", "Bob")
        fig = render_discocat_sentence(s)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_custom_title(self):
        """Test custom title override."""
        s = Sentence.intransitive("Alice", "runs")
        fig = render_discocat_sentence(s, title="Custom Title")
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_save_to_file(self, tmp_path):
        """Test saving to output_path triggers file save and log."""
        s = Sentence.transitive("Alice", "chases", "Bob")
        out = tmp_path / "test_sentence.png"
        fig = render_discocat_sentence(s, output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0
        plt.close(fig)

    def test_sentence_no_verb(self):
        """Test sentence with no verb box (no 's' wire type)."""
        # Create a sentence with only noun boxes
        n_wire = Wire(N)
        box1 = Box("Alice", cod=[n_wire])
        box2 = Box("Bob", cod=[n_wire])
        s = Sentence(
            text="Alice Bob",
            boxes=[box1, box2],
            case_assignments={"Alice": CaseRole.NOM, "Bob": CaseRole.ACC},
        )
        fig = render_discocat_sentence(s)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_verb_with_entity_dom_wire(self):
        """Test verb with dom wires that have entity references for cup arcs."""
        n_wire = Wire(N)
        s_wire = Wire(S)
        entity_wire = Wire(N, entity="Alice")

        verb_box = Box("chases", dom=[entity_wire], cod=[s_wire])
        noun_box = Box("Alice", cod=[n_wire])

        s = Sentence(
            text="Alice chases",
            boxes=[noun_box, verb_box],
            case_assignments={"Alice": CaseRole.NOM},
        )
        fig = render_discocat_sentence(s)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_verb_entity_not_found(self):
        """Test verb with entity reference that doesn't match any noun box."""
        s_wire = Wire(S)
        entity_wire = Wire(N, entity="Charlie")
        n_wire = Wire(N)

        verb_box = Box("chases", dom=[entity_wire], cod=[s_wire])
        noun_box = Box("Alice", cod=[n_wire])

        s = Sentence(
            text="Alice chases",
            boxes=[noun_box, verb_box],
            case_assignments={"Alice": CaseRole.NOM},
        )
        # Should not raise (StopIteration caught)
        fig = render_discocat_sentence(s)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)


class TestRenderDiscourseDiagram:
    """Tests for render_discourse_diagram function."""

    def test_basic_discourse(self):
        """Test basic two-sentence discourse rendering."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        fig = render_discourse_diagram(d)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_discourse_custom_title(self):
        """Test discourse with custom title."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        fig = render_discourse_diagram(d, title="Custom Discourse")
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_discourse_save_file(self, tmp_path):
        """Test discourse diagram saves to file."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        out = tmp_path / "discourse.png"
        fig = render_discourse_diagram(d, output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0
        plt.close(fig)

    def test_role_reversal_discourse(self):
        """Test three-sentence role reversal discourse."""
        d = Discourse.role_reversal("Alice", "Bob")
        fig = render_discourse_diagram(d)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)


class TestConvenienceFunctions:
    """Tests for convenience rendering functions."""

    def test_render_discocirc_discourse(self, tmp_path):
        """Test the canonical two-sentence discourse."""
        out = tmp_path / "discocirc.png"
        fig = render_discocirc_discourse(output_path=out)
        assert isinstance(fig, matplotlib.figure.Figure)
        assert out.exists()
        plt.close(fig)

    def test_render_discocirc_no_path(self):
        """Test discocirc without output path."""
        fig = render_discocirc_discourse()
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

    def test_render_three_sentence(self, tmp_path):
        """Test the three-sentence role reversal."""
        out = tmp_path / "three_sent.png"
        fig = render_three_sentence_discourse(output_path=out)
        assert isinstance(fig, matplotlib.figure.Figure)
        assert out.exists()
        plt.close(fig)

    def test_render_three_sentence_no_path(self):
        """Test three-sentence without output path."""
        fig = render_three_sentence_discourse()
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)
