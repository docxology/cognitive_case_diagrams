"""Tests for natural transformation module.

Validates component maps, naturality squares, identity transformations,
and vertical composition of natural transformations.
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
