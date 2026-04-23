"""Tests for natural transformation — partial morphisms, composition, identity."""
import pytest

from src.case_systems.case_category import CaseCategory, CaseRole, Morphism
from src.case_systems.functor import AlignmentFunctor
from src.case_systems.natural_transformation import (
    ComponentMorphism,
    IdentityNaturalTransformation,
    NaturalTransformation,
    compose_transformations,
)


def _two_object_category(name: str) -> CaseCategory:
    cat = CaseCategory(name=name)
    cat.add_role(CaseRole.NOM)
    cat.add_role(CaseRole.ACC)
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.9))
    return cat


def _make_identity_functor(src: CaseCategory, tgt: CaseCategory) -> AlignmentFunctor:
    return AlignmentFunctor(
        name="id",
        object_map={CaseRole.NOM: CaseRole.NOM, CaseRole.ACC: CaseRole.ACC},
        source=src,
        target=tgt,
    )


class TestIdentityNaturalTransformation:
    def test_identity_is_complete(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        id_nat = IdentityNaturalTransformation(f)
        assert id_nat.is_complete()

    def test_identity_naturality_holds(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        id_nat = IdentityNaturalTransformation(f)
        assert id_nat.naturality_holds()

    def test_identity_components_are_self_loops(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        id_nat = IdentityNaturalTransformation(f)
        for role, comp in id_nat.components.items():
            assert comp.source_image == comp.target_image


class TestPartialMorphismHandling:
    def test_morphism_outside_object_map_skipped_not_error(self):
        """Morphisms with endpoints outside the functor's domain must be silently skipped."""
        src = CaseCategory(name="full")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            src.add_role(r)
        src.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.8))
        src.add_morphism(Morphism(CaseRole.NOM, CaseRole.DAT, "transfers_to", weight=0.7))

        tgt = CaseCategory(name="partial_tgt")
        tgt.add_role(CaseRole.NOM)
        tgt.add_role(CaseRole.ACC)
        tgt.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.8))

        # Functor only maps NOM and ACC (not DAT)
        f = AlignmentFunctor(
            name="partial",
            object_map={CaseRole.NOM: CaseRole.NOM, CaseRole.ACC: CaseRole.ACC},
            source=src,
            target=tgt,
        )
        id_nat = IdentityNaturalTransformation(f)
        # Should not raise; DAT morphism is silently skipped
        result = id_nat.naturality_holds()
        assert result is True


class TestComposeTransformations:
    def test_mismatched_functors_raises(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        other = _two_object_category("other")
        f1 = _make_identity_functor(src, tgt)
        f1.name = "F"
        f2 = AlignmentFunctor(
            name="G",
            object_map={CaseRole.NOM: CaseRole.NOM, CaseRole.ACC: CaseRole.ACC},
            source=other,
            target=tgt,
        )
        alpha = IdentityNaturalTransformation(f1)
        beta = IdentityNaturalTransformation(f2)
        with pytest.raises(ValueError, match="Cannot compose"):
            compose_transformations(alpha, beta)

    def test_valid_composition_produces_correct_name(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        alpha = IdentityNaturalTransformation(f)
        beta = IdentityNaturalTransformation(f)
        # Rename target functor to match: alpha.target == beta.source
        beta.source_functor = alpha.target_functor
        composite = compose_transformations(alpha, beta)
        assert "∘" in composite.name


class TestNaturalTransformationValidation:
    def test_set_component_validates_functor_images(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        nat = NaturalTransformation(name="α", source_functor=f, target_functor=f)
        # Wrong source_image should raise
        bad_comp = ComponentMorphism(
            object_name=CaseRole.NOM,
            source_image=CaseRole.ACC,  # should be NOM
            target_image=CaseRole.NOM,
        )
        with pytest.raises(ValueError, match="Component source"):
            nat.set_component(CaseRole.NOM, bad_comp)

    def test_incomplete_transformation_naturality_returns_false(self):
        src = _two_object_category("src")
        tgt = _two_object_category("tgt")
        f = _make_identity_functor(src, tgt)
        nat = NaturalTransformation(name="incomplete", source_functor=f, target_functor=f)
        # Don't add any components
        assert nat.naturality_holds() is False
