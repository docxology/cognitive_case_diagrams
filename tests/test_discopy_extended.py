"""Comprehensive tests for extended DisCoPy integration.

Tests grammar.pregroup.Word, eager_parse, Swap, tensor semantics,
depth/width metrics, and diagram equality — all using real DisCoPy
operations (zero-mock policy).

References:
    Coecke, Sadrzadeh & Clark (2010) — DisCoCat
    de Felice & Coecke (2020) — DisCoCirc
"""

import numpy as np
import pytest

discopy = pytest.importorskip("discopy", reason="discopy required")


class TestWordAndEagerParse:
    """Test grammar.pregroup.Word and eager_parse integration."""

    def test_word_type(self) -> None:
        """Word has correct type attributes."""
        from discopy.grammar.pregroup import Word, Ty

        n = Ty("n")
        w = Word("Alice", n)
        assert w.name == "Alice"
        assert w.cod == n
        assert w.dom == Ty()

    def test_eager_parse_transitive(self) -> None:
        """eager_parse produces correct transitive diagram."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse

        n = Ty("n")
        s = Ty("s")
        diagram = eager_parse(
            Word("Alice", n), Word("chases", n.r @ s @ n.l), Word("Bob", n)
        )
        assert diagram.cod == s
        assert len(diagram.boxes) == 5  # 3 words + 2 cups

    def test_eager_parse_intransitive(self) -> None:
        """eager_parse produces correct intransitive diagram."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse

        n = Ty("n")
        s = Ty("s")
        diagram = eager_parse(Word("Bob", n), Word("runs", n.r @ s))
        assert diagram.cod == s
        assert len(diagram.boxes) == 3  # 2 words + 1 cup

    def test_eager_parse_ditransitive(self) -> None:
        """eager_parse handles ditransitive (4 words)."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse
        from discopy.rigid import Cup

        n = Ty("n")
        s = Ty("s")
        diagram = eager_parse(
            Word("Alice", n),
            Word("gave", n.r @ s @ n.l @ n.l),
            Word("Bob", n),
            Word("cake", n),
        )
        assert diagram.cod == s
        cups = sum(1 for b in diagram.boxes if isinstance(b, Cup))
        assert cups == 3

    def test_word_vs_box_same_codomain(self) -> None:
        """Word and Box produce diagrams with equivalent codomain type string."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse
        from discopy.rigid import Ty as RTy, Box as RBox, Cup as RCup, Id as RId

        n = Ty("n")
        s = Ty("s")
        word_diag = eager_parse(
            Word("A", n), Word("v", n.r @ s @ n.l), Word("B", n)
        )
        rn = RTy("n")
        rs = RTy("s")
        box_diag = (
            RBox("A", RTy(), rn) @ RBox("v", RTy(), rn.r @ rs @ rn.l) @ RBox("B", RTy(), rn)
        )
        box_diag = box_diag >> RCup(rn, rn.r) @ RId(rs) @ RCup(rn.l, rn)
        # Can't compare cross-category types directly; compare string representations
        assert str(word_diag.cod) == str(box_diag.cod) == "s"

    def test_eager_parse_multilingual_isomorphism(self) -> None:
        """All languages produce isomorphic type reductions via eager_parse."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse

        n = Ty("n")
        s = Ty("s")
        languages = {
            "English": ("Alice", "chases", "Bob"),
            "Latin": ("Alicia", "persequitur", "Robertum"),
            "Japanese": ("Arisu-ga", "ou", "Bobu-wo"),
        }
        for lang, (subj, verb, obj) in languages.items():
            d = eager_parse(Word(subj, n), Word(verb, n.r @ s @ n.l), Word(obj, n))
            assert d.cod == s, f"{lang} diagram does not reduce to s"


class TestSwap:
    """Test Swap morphism for passivization."""

    def test_swap_type(self) -> None:
        """Swap(n, s) has correct domain and codomain."""
        from discopy.grammar.pregroup import Swap, Ty

        n = Ty("n")
        s = Ty("s")
        sw = Swap(n, s)
        assert sw.dom == n @ s
        assert sw.cod == s @ n

    def test_swap_type_involution(self) -> None:
        """Double swap preserves domain and codomain types."""
        from discopy.grammar.pregroup import Swap, Ty

        n = Ty("n")
        s = Ty("s")
        double_swap = Swap(n, s) >> Swap(s, n)
        assert double_swap.dom == n @ s
        assert double_swap.cod == n @ s

    def test_passive_same_codomain(self) -> None:
        """Passive and active sentences produce same codomain type."""
        from discopy.grammar.pregroup import Word, Ty, eager_parse

        n = Ty("n")
        s = Ty("s")
        active = eager_parse(
            Word("Alice", n), Word("chases", n.r @ s @ n.l), Word("Bob", n)
        )
        passive = eager_parse(
            Word("Bob", n),
            Word("is_chased_by", n.r @ s @ n.l),
            Word("Alice", n),
        )
        assert active.cod == passive.cod == s


class TestDiagramDepthWidth:
    """Test depth() and width metrics."""

    def test_transitive_depth(self) -> None:
        """Transitive diagram has expected depth."""
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        depth = d.depth()
        assert isinstance(depth, int)
        assert depth >= 2

    def test_intransitive_shallower(self) -> None:
        """Intransitive diagram is shallower than transitive."""
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        intrans = Box("A", Ty(), n) @ Box("v", Ty(), n.r @ s)
        intrans = intrans >> Cup(n, n.r) @ Id(s)
        trans = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        trans = trans >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert intrans.depth() <= trans.depth()

    def test_width_positive(self) -> None:
        """All diagrams have positive width."""
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert d.width > 0

    def test_identity_depth_zero(self) -> None:
        """Identity diagram has depth 0."""
        from discopy.rigid import Ty, Id

        n = Ty("n")
        assert Id(n).depth() == 0


class TestTensorSemantics:
    """Test DisCoCat semantic evaluation in tensor category."""

    def test_tensor_evaluation_shape(self) -> None:
        """Tensor diagram evaluates to correct shape."""
        from discopy.tensor import Box as TBox, Cup as TCup, Id as TId, Dim

        N = Dim(2)
        S = Dim(4)
        subj = TBox("Alice", Dim(1), N, [1.0, 0.0])
        verb = TBox("chases", Dim(1), N @ S @ N, list(np.zeros(16)))
        obj = TBox("Bob", Dim(1), N, [0.0, 1.0])
        diagram = subj @ verb @ obj >> TCup(N, N) @ TId(S) @ TCup(N, N)
        result = diagram.eval()
        assert result.array.shape == (4,)

    def test_tensor_evaluation_nonzero(self) -> None:
        """Non-trivial verb tensor produces non-zero meaning."""
        from discopy.tensor import Box as TBox, Cup as TCup, Id as TId, Dim

        N = Dim(2)
        S = Dim(4)
        verb_arr = np.zeros(2 * 4 * 2)
        verb_arr[0 * 4 * 2 + 0 * 2 + 1] = 1.0
        subj = TBox("Alice", Dim(1), N, [1.0, 0.0])
        verb = TBox("chases", Dim(1), N @ S @ N, verb_arr)
        obj = TBox("Bob", Dim(1), N, [0.0, 1.0])
        diagram = subj @ verb @ obj >> TCup(N, N) @ TId(S) @ TCup(N, N)
        result = diagram.eval()
        assert result.array[0] == pytest.approx(1.0)
        assert np.sum(np.abs(result.array)) > 0

    def test_tensor_evaluation_linearity(self) -> None:
        """Different inputs produce arrays of same shape."""
        from discopy.tensor import Box as TBox, Cup as TCup, Id as TId, Dim

        N = Dim(2)
        S = Dim(4)
        verb_arr = np.zeros(16)
        verb_arr[0] = 1.0
        d1 = (
            TBox("A", Dim(1), N, [1.0, 0.0])
            @ TBox("v", Dim(1), N @ S @ N, verb_arr)
            @ TBox("B", Dim(1), N, [0.0, 1.0])
        )
        d1 = d1 >> TCup(N, N) @ TId(S) @ TCup(N, N)
        d2 = (
            TBox("A", Dim(1), N, [0.5, 0.5])
            @ TBox("v", Dim(1), N @ S @ N, verb_arr)
            @ TBox("B", Dim(1), N, [0.0, 1.0])
        )
        d2 = d2 >> TCup(N, N) @ TId(S) @ TCup(N, N)
        r1 = d1.eval().array
        r2 = d2.eval().array
        assert r1.shape == r2.shape == (4,)

    def test_intransitive_tensor(self) -> None:
        """Intransitive tensor semantics works with 2-arg type."""
        from discopy.tensor import Box as TBox, Cup as TCup, Id as TId, Dim

        N = Dim(2)
        S = Dim(4)
        verb_arr = np.zeros(2 * 4)
        verb_arr[0] = 1.0
        subj = TBox("Bob", Dim(1), N, [1.0, 0.0])
        verb = TBox("runs", Dim(1), N @ S, verb_arr)
        diagram = subj @ verb >> TCup(N, N) @ TId(S)
        result = diagram.eval()
        assert result.array.shape == (4,)


class TestNormalFormAndEquality:
    """Test diagram normal form and equality."""

    def test_snake_equation_holds(self) -> None:
        """Snake equation: cup(cap(x)) = id(x)."""
        from discopy.rigid import Ty, Id, Cup, Cap

        x = Ty("x")
        left_snake = x @ Cap(x.r, x) >> Cup(x, x.r) @ x
        assert left_snake.normal_form() == Id(x).normal_form()

    def test_right_snake_equation(self) -> None:
        """Right snake: cap(x) @ x >> x @ cup(x) = id(x)."""
        from discopy.rigid import Ty, Id, Cup, Cap

        x = Ty("x")
        right_snake = Cap(x, x.l) @ x >> x @ Cup(x.l, x)
        assert right_snake.normal_form() == Id(x).normal_form()

    def test_normal_form_idempotent(self) -> None:
        """Normal form of normal form equals normal form."""
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        nf = d.normal_form()
        assert nf.normal_form() == nf

    def test_different_words_not_equal(self) -> None:
        """Diagrams with different words are not equal."""
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d1 = (
            Box("Alice", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("Bob", Ty(), n)
        )
        d1 = d1 >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        d2 = (
            Box("Carol", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("Dave", Ty(), n)
        )
        d2 = d2 >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert d1.normal_form() != d2.normal_form()


class TestCompactClosedAxioms:
    """Test compact closed category axioms using DisCoPy."""

    def test_cup_cap_types(self) -> None:
        """Cup and Cap have correct domain/codomain types."""
        from discopy.rigid import Ty, Cup, Cap

        n = Ty("n")
        cup = Cup(n, n.r)
        cap = Cap(n.r, n)
        assert cup.dom == n @ n.r
        assert cup.cod == Ty()
        assert cap.dom == Ty()
        assert cap.cod == n.r @ n

    def test_tensor_product_associativity(self) -> None:
        """Tensor product of types is associative."""
        from discopy.rigid import Ty

        a = Ty("a")
        b = Ty("b")
        c = Ty("c")
        assert (a @ b) @ c == a @ (b @ c)

    def test_identity_composition(self) -> None:
        """Identity composed with any diagram gives same diagram."""
        from discopy.rigid import Ty, Box, Id

        n = Ty("n")
        b = Box("x", Ty(), n)
        assert (b >> Id(n)).normal_form() == b.normal_form()
        assert (Id(Ty()) >> b).normal_form() == b.normal_form()

    def test_adjoint_involution(self) -> None:
        """Double adjoint returns to original type: (n.r).l == n."""
        from discopy.rigid import Ty

        n = Ty("n")
        assert n.r.l == n
        assert n.l.r == n


class TestSrcIntegration:
    """Test the new src/ functions that use extended DisCoPy."""

    def test_create_word_diagram_transitive(self) -> None:
        """create_word_diagram_transitive produces valid diagram."""
        from src.diagrams.string_diagram import create_word_diagram_transitive
        from discopy.grammar.pregroup import Ty

        d = create_word_diagram_transitive("Alice", "chases", "Bob")
        assert d.cod == Ty("s")

    def test_create_word_diagram_intransitive(self) -> None:
        """create_word_diagram_intransitive produces valid diagram."""
        from src.diagrams.string_diagram import create_word_diagram_intransitive
        from discopy.grammar.pregroup import Ty

        d = create_word_diagram_intransitive("Bob", "runs")
        assert d.cod == Ty("s")

    def test_create_swap_passive(self) -> None:
        """create_swap_passive produces valid diagram."""
        from src.diagrams.string_diagram import create_swap_passive
        from discopy.grammar.pregroup import Ty

        d = create_swap_passive("Bob", "chased", "Alice")
        assert d.cod == Ty("s")

    def test_create_word_diagram_ditransitive(self) -> None:
        """create_word_diagram_ditransitive produces valid diagram."""
        from src.diagrams.string_diagram import create_word_diagram_ditransitive
        from discopy.grammar.pregroup import Ty

        d = create_word_diagram_ditransitive("Alice", "gave", "Bob", "cake")
        assert d.cod == Ty("s")

    def test_create_tensor_semantics(self) -> None:
        """create_tensor_semantics produces valid meaning vector."""
        from src.diagrams.string_diagram import create_tensor_semantics

        diagram, meaning = create_tensor_semantics("Alice", "chases", "Bob")
        assert meaning.shape == (4,)

    def test_create_tensor_semantics_custom_dims(self) -> None:
        """create_tensor_semantics works with custom dimensions."""
        from src.diagrams.string_diagram import create_tensor_semantics

        _, meaning = create_tensor_semantics(
            "Alice", "chases", "Bob", noun_dim=3, sentence_dim=6
        )
        assert meaning.shape == (6,)

    def test_diagram_depth_metric(self) -> None:
        """diagram_depth returns integer for transitive diagram."""
        from src.diagrams.complexity_metrics import diagram_depth
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert diagram_depth(d) >= 2

    def test_diagram_width_metric(self) -> None:
        """diagram_width returns positive integer."""
        from src.diagrams.complexity_metrics import diagram_width
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert diagram_width(d) > 0

    def test_analyze_diagram_has_depth_width(self) -> None:
        """analyze_diagram populates depth and width fields."""
        from src.diagrams.complexity_metrics import analyze_diagram
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        metrics = analyze_diagram(d, "test")
        assert metrics.depth >= 2
        assert metrics.width > 0

    def test_syntactic_complexity_includes_depth(self) -> None:
        """syntactic_complexity_score incorporates depth term."""
        from src.diagrams.complexity_metrics import syntactic_complexity_score
        from discopy.rigid import Ty, Box, Cup, Id

        n = Ty("n")
        s = Ty("s")
        d = (
            Box("A", Ty(), n)
            @ Box("v", Ty(), n.r @ s @ n.l)
            @ Box("B", Ty(), n)
        )
        d = d >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        score = syntactic_complexity_score(d)
        # 3 words + 0.5*2 cups + 0.25*0 caps + 0.1*depth
        # depth=2 -> 3 + 1.0 + 0 + 0.2 = 4.2
        assert score > 4.0  # Must be > pure word+cup score
