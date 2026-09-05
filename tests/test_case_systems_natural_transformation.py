"""Tests for natural transformation module.

Validates component maps, :meth:`NaturalTransformation.naturality_holds`,
identity transformations, and vertical composition of natural transformations.
"""

import pytest

from src.case_systems.case_category import CaseRole, Morphism, CaseCategory
from src.case_systems.functor import (
    AlignmentFunctor,
    accusative_to_ergative_functor,
    tripartite_functor,
)
from src.case_systems.natural_transformation import (
    NaturalTransformation,
    IdentityNaturalTransformation,
    ComponentMorphism,
    compose_transformations,
)


def make_parallel_functors_with_morphism() -> AlignmentFunctor:
    """Single functor F: Core{S,P} → Surf{NOM,ACC} with one demo morphism S→P."""
    source = CaseCategory(name="CoreDemo")
    source.add_role(CaseRole.S)
    source.add_role(CaseRole.P)
    source.add_morphism(
        Morphism(CaseRole.S, CaseRole.P, "subj_of", weight=0.5)
    )
    target = CaseCategory(name="SurfDemo")
    target.add_role(CaseRole.NOM)
    target.add_role(CaseRole.ACC)
    om = {CaseRole.S: CaseRole.NOM, CaseRole.P: CaseRole.ACC}
    return AlignmentFunctor(
        name="Fdemo", source=source, target=target, object_map=om
    )


class TestNaturality:
    """Naturality squares G(f)∘α_A = α_B∘F(f)."""

    def test_identity_nt_vacuous_when_no_morphisms(self) -> None:
        """Factory functor categories often have no morphisms — check is vacuously true."""
        fn = accusative_to_ergative_functor()
        ident = IdentityNaturalTransformation(fn)
        assert ident.naturality_holds()
        assert ident.verify_naturality()

    def test_identity_nt_with_demo_morphism(self) -> None:
        """Non-empty source morphisms: identity id_F satisfies naturality."""
        fn = make_parallel_functors_with_morphism()
        ident = IdentityNaturalTransformation(fn)
        assert ident.naturality_holds()

    def test_incomplete_returns_false(self) -> None:
        nt = NaturalTransformation(
            name="partial",
            source_functor=accusative_to_ergative_functor(),
            target_functor=accusative_to_ergative_functor(),
        )
        assert not nt.is_complete()
        assert not nt.naturality_holds()

    def test_failing_weight_mismatch_returns_false(self) -> None:
        """A naturality square that does NOT commute returns False.

        Components α_S (w=0.8) and α_P (w=1.0) share endpoints with the
        identity self-maps, so both legs of the square have identical
        endpoints but different weights: G(f)∘α_S = 0.8·0.5 = 0.4 while
        α_P∘F(f) = 0.5·1.0 = 0.5 for f: S→P (w=0.5). The weight-comparison
        branch of :meth:`naturality_holds` must fire.
        """
        fn = make_parallel_functors_with_morphism()
        nt = NaturalTransformation(
            name="weighted",
            source_functor=fn,
            target_functor=fn,
        )
        nt.set_component(CaseRole.S, ComponentMorphism(
            object_name=CaseRole.S,
            source_image=fn.object_map[CaseRole.S],
            target_image=fn.object_map[CaseRole.S],
            weight=0.8,
        ))
        nt.components[CaseRole.P] = ComponentMorphism(
            object_name=CaseRole.P,
            source_image=fn.object_map[CaseRole.P],
            target_image=fn.object_map[CaseRole.P],
            weight=1.0,
        )
        assert nt.is_complete()
        assert not nt.naturality_holds()


class TestNaturalTransformation:
    """Tests for NaturalTransformation class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.functor = accusative_to_ergative_functor()

    def test_creation(self) -> None:
        """Test basic creation of a natural transformation."""
        nt = NaturalTransformation(
            name="test_nt",
            source_functor=self.functor,
            target_functor=self.functor,
        )
        assert nt.name == "test_nt"
        assert len(nt.components) == 0

    def test_set_component_valid(self) -> None:
        """Test setting a valid component morphism."""
        nt = NaturalTransformation(
            name="test",
            source_functor=self.functor,
            target_functor=self.functor,
        )
        # F(S) = ABS, so component should map ABS → ABS
        target = self.functor.object_map[CaseRole.S]
        comp = ComponentMorphism(
            object_name=CaseRole.S,
            source_image=target,
            target_image=target,
        )
        nt.set_component(CaseRole.S, comp)
        assert CaseRole.S in nt.components

    def test_set_component_invalid_source(self) -> None:
        """Test setting a component with mismatched source image."""
        nt = NaturalTransformation(
            name="test",
            source_functor=self.functor,
            target_functor=self.functor,
        )
        bad = ComponentMorphism(
            object_name=CaseRole.S,
            source_image=CaseRole.NOM,  # Wrong — should be ABS
            target_image=CaseRole.ABS,
        )
        with pytest.raises(ValueError):
            nt.set_component(CaseRole.S, bad)

    def test_set_component_unknown_role(self) -> None:
        """Test setting component for role not in functor's object map."""
        nt = NaturalTransformation(
            name="test",
            source_functor=self.functor,
            target_functor=self.functor,
        )
        comp = ComponentMorphism(
            object_name=CaseRole.GEN,
            source_image=CaseRole.GEN,
            target_image=CaseRole.GEN,
        )
        with pytest.raises(ValueError):
            nt.set_component(CaseRole.GEN, comp)

    def test_is_complete_empty(self) -> None:
        """Test completeness check on empty transformation."""
        nt = NaturalTransformation(
            name="test",
            source_functor=self.functor,
            target_functor=self.functor,
        )
        assert not nt.is_complete()

    def test_is_complete_full(self) -> None:
        """Test completeness check on fully populated transformation."""
        nt = IdentityNaturalTransformation(self.functor)
        assert nt.is_complete()

    def test_component_morphisms_list(self) -> None:
        """Test extracting component morphisms."""
        nt = IdentityNaturalTransformation(self.functor)
        morphisms = nt.component_morphisms()
        assert len(morphisms) == len(self.functor.object_map)
        for m in morphisms:
            assert m.source == m.target  # Identity

    def test_image_roles(self) -> None:
        """Test extracting image roles."""
        nt = IdentityNaturalTransformation(self.functor)
        images = nt.image_roles()
        assert isinstance(images, set)
        assert len(images) > 0


class TestIdentityNaturalTransformation:
    """Tests for identity natural transformations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.functor = accusative_to_ergative_functor()

    def test_creation(self) -> None:
        """Test identity transformation creates components for all objects."""
        ident = IdentityNaturalTransformation(self.functor)
        assert ident.name.startswith("id_")
        assert ident.is_complete()

    def test_identity_components_are_self_maps(self) -> None:
        """Test that each component maps F(A) to F(A)."""
        ident = IdentityNaturalTransformation(self.functor)
        for role, comp in ident.components.items():
            assert comp.source_image == comp.target_image

    def test_number_of_components_matches_functor(self) -> None:
        """Identity has one component per object in functor domain."""
        ident = IdentityNaturalTransformation(self.functor)
        assert len(ident.components) == len(self.functor.object_map)

    def test_identity_on_tripartite(self) -> None:
        """Identity transformation works on tripartite functor too."""
        tri = tripartite_functor()
        ident = IdentityNaturalTransformation(tri)
        assert ident.is_complete()
        assert len(ident.components) == len(tri.object_map)


class TestComposition:
    """Tests for vertical composition of natural transformations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.functor = accusative_to_ergative_functor()

    def test_compose_identity_identity(self) -> None:
        """Test id ∘ id = complete transformation."""
        id1 = IdentityNaturalTransformation(self.functor)
        id2 = IdentityNaturalTransformation(self.functor)
        composite = compose_transformations(id1, id2)
        assert composite.is_complete()

    def test_compose_preserves_all_components(self) -> None:
        """Composition preserves all objects from both transformations."""
        id1 = IdentityNaturalTransformation(self.functor)
        id2 = IdentityNaturalTransformation(self.functor)
        composite = compose_transformations(id1, id2)
        assert len(composite.components) == len(self.functor.object_map)

    def test_compose_mismatched_functors_raises(self) -> None:
        """Composing transformations with incompatible functors fails."""
        other = tripartite_functor()
        alpha = IdentityNaturalTransformation(self.functor)
        beta = IdentityNaturalTransformation(other)
        with pytest.raises(ValueError):
            compose_transformations(alpha, beta)

    def test_composite_name(self) -> None:
        """Test that composite name includes both transformation names."""
        id1 = IdentityNaturalTransformation(self.functor)
        id2 = IdentityNaturalTransformation(self.functor)
        composite = compose_transformations(id1, id2)
        assert "∘" in composite.name

    def test_composite_source_image_from_first(self) -> None:
        """Composite source_image comes from first transformation."""
        id1 = IdentityNaturalTransformation(self.functor)
        id2 = IdentityNaturalTransformation(self.functor)
        composite = compose_transformations(id1, id2)
        for role in composite.components:
            assert composite.components[role].source_image == \
                   id1.components[role].source_image

    def test_composite_weight_is_enriched_product(self) -> None:
        """Vertical composition multiplies component weights (§4–5).

        Both transformations live on the same functor, so every component is
        trivially composable: w(β_A ∘ α_A) = w(α_A) · w(β_A).
        """
        fn = make_parallel_functors_with_morphism()
        alpha = NaturalTransformation(name="alpha", source_functor=fn, target_functor=fn)
        beta = NaturalTransformation(name="beta", source_functor=fn, target_functor=fn)
        for role in (CaseRole.S, CaseRole.P):
            image = fn.object_map[role]
            alpha.set_component(role, ComponentMorphism(
                object_name=role, source_image=image, target_image=image, weight=0.8))
            beta.set_component(role, ComponentMorphism(
                object_name=role, source_image=image, target_image=image, weight=0.5))
        composite = compose_transformations(alpha, beta)
        for role in (CaseRole.S, CaseRole.P):
            assert composite.components[role].weight == pytest.approx(0.4)

    def test_compose_incomposable_components_raises(self) -> None:
        """α_A must land where β_A starts, componentwise.

        ``set_component`` already enforces each transformation's own endpoints,
        so a composability mismatch is only reachable via directly assigned
        components (the dataclass permits it; other tests use that path).
        """
        fn = make_parallel_functors_with_morphism()
        alpha = NaturalTransformation(name="alpha", source_functor=fn, target_functor=fn)
        beta = NaturalTransformation(name="beta", source_functor=fn, target_functor=fn)
        # α_S: NOM → ACC (lands on ACC) while β_S: NOM → NOM (starts at NOM).
        alpha.components[CaseRole.S] = ComponentMorphism(
            object_name=CaseRole.S,
            source_image=fn.object_map[CaseRole.S],
            target_image=fn.object_map[CaseRole.P],
        )
        alpha.components[CaseRole.P] = ComponentMorphism(
            object_name=CaseRole.P,
            source_image=fn.object_map[CaseRole.P],
            target_image=fn.object_map[CaseRole.P],
        )
        beta.components[CaseRole.S] = ComponentMorphism(
            object_name=CaseRole.S,
            source_image=fn.object_map[CaseRole.S],
            target_image=fn.object_map[CaseRole.S],
        )
        beta.components[CaseRole.P] = ComponentMorphism(
            object_name=CaseRole.P,
            source_image=fn.object_map[CaseRole.P],
            target_image=fn.object_map[CaseRole.P],
        )
        with pytest.raises(ValueError, match="Cannot compose at S"):
            compose_transformations(alpha, beta)
