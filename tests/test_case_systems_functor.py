"""Tests for the functor module.

Validates alignment functor mapping, identity/composition preservation,
injectivity checking, and factory functions.
"""

import pytest

from src.case_systems.functor import (
    AlignmentFunctor,
    accusative_to_ergative_functor,
    tripartite_functor,
    MonoidalFunctor,
)
from src.case_systems.case_category import CaseRole, Morphism, CaseCategory


def _tripartite_style_functor() -> tuple[AlignmentFunctor, Morphism, Morphism]:
    """Core S→A→P with weighted morphisms; target ABS/ERG/ACC."""
    source = CaseCategory(name="CoreChain")
    for r in (CaseRole.S, CaseRole.A, CaseRole.P):
        source.add_role(r)
    f_m = Morphism(CaseRole.S, CaseRole.A, "step1", weight=0.8)
    g_m = Morphism(CaseRole.A, CaseRole.P, "step2", weight=0.5)
    source.add_morphism(f_m)
    source.add_morphism(g_m)
    target = CaseCategory(name="TripTgt")
    for r in (CaseRole.ABS, CaseRole.ERG, CaseRole.ACC):
        target.add_role(r)
    om = {
        CaseRole.S: CaseRole.ABS,
        CaseRole.A: CaseRole.ERG,
        CaseRole.P: CaseRole.ACC,
    }
    return AlignmentFunctor(
        name="TripLike", source=source, target=target, object_map=om
    ), f_m, g_m


class TestAlignmentFunctor:
    """Tests for the AlignmentFunctor class."""

    def test_map_object(self):
        """Object mapping returns correct target role."""
        functor = accusative_to_ergative_functor()
        assert functor.map_object(CaseRole.NOM) == CaseRole.ERG
        assert functor.map_object(CaseRole.ACC) == CaseRole.ABS

    def test_map_object_unknown_raises(self):
        """Mapping an unmapped role raises KeyError."""
        functor = accusative_to_ergative_functor()
        with pytest.raises(KeyError, match="No mapping"):
            functor.map_object(CaseRole.GEN)

    def test_map_morphism(self):
        """Morphism mapping preserves arrow structure."""
        functor = accusative_to_ergative_functor()
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.88)
        mapped = functor.map_morphism(m)
        assert mapped.source == CaseRole.ERG
        assert mapped.target == CaseRole.ABS
        assert "F(" in mapped.label
        assert mapped.weight == pytest.approx(0.88)

    def test_preserves_identity(self):
        """Functor preserves identity morphisms for mapped roles."""
        functor = accusative_to_ergative_functor()
        # S maps to S in both systems
        assert functor.preserves_identity(CaseRole.S)

    def test_image_roles(self):
        """Image function returns correct target roles."""
        functor = accusative_to_ergative_functor()
        image = functor.image_roles()
        assert CaseRole.ERG in image
        assert CaseRole.ABS in image

    def test_preserves_identity_fails(self):
        """Functor logs warning and returns False when identity is not preserved."""
        functor = accusative_to_ergative_functor()
        # Zero mock approach: corrupt target identity generation
        original_identity = functor.target.identity
        
        def bad_identity(role):
            return Morphism(CaseRole.DAT, CaseRole.GEN, "bad", weight=0.0)
            
        functor.target.identity = bad_identity
        assert not functor.preserves_identity(CaseRole.S)
        functor.target.identity = original_identity

    def test_preserves_composition_fails(self):
        """Functor logs warning and returns False when composition is not preserved."""
        functor = accusative_to_ergative_functor()
        # Add required roles and bad morphisms
        f = Morphism(CaseRole.S, CaseRole.A, "f", weight=1.0)
        g = Morphism(CaseRole.A, CaseRole.P, "g", weight=1.0)
        functor.source.add_morphism(f)
        functor.source.add_morphism(g)
        # Acc->Erg maps S->ABS, A->ERG, P->ABS
        # Corrupt the target's compose to return something bad
        original_compose = functor.target.compose
        
        def bad_compose(m1, m2):
            return Morphism(CaseRole.DAT, CaseRole.GEN, "bad", weight=0.0)
            
        functor.target.compose = bad_compose
        assert not functor.preserves_composition(f, g)
        functor.target.compose = original_compose


class TestAccusativeToErgative:
    """Tests for the accusative-to-ergative functor factory."""

    def test_name(self):
        """Functor has descriptive name."""
        functor = accusative_to_ergative_functor()
        assert "Acc" in functor.name or "Erg" in functor.name

    def test_source_category(self):
        """Source is an Accusative system."""
        functor = accusative_to_ergative_functor()
        assert "Accusative" in functor.source.name

    def test_target_category(self):
        """Target is an Ergative system."""
        functor = accusative_to_ergative_functor()
        assert "Ergative" in functor.target.name

    def test_not_injective(self):
        """Accusative-to-ergative functor is not injective (neutralization)."""
        functor = accusative_to_ergative_functor()
        # Multiple source roles map to same target
        assert not functor.is_injective()


class TestPreservesCompositionEnriched:
    """Functor preserves composition including enriched weights."""

    def test_weighted_morphisms(self) -> None:
        functor, f_m, g_m = _tripartite_style_functor()
        assert functor.preserves_composition(f_m, g_m)


class TestTripartiteFunctor:
    """Tests for the tripartite functor factory."""

    def test_is_injective(self):
        """Tripartite alignment is injective (no neutralization)."""
        functor = tripartite_functor()
        assert functor.is_injective()

    def test_maps_all_core_roles(self):
        """All core argument roles S, A, P are mapped."""
        functor = tripartite_functor()
        assert functor.map_object(CaseRole.S) == CaseRole.ABS
        assert functor.map_object(CaseRole.A) == CaseRole.ERG
        assert functor.map_object(CaseRole.P) == CaseRole.ACC

    def test_three_distinct_targets(self):
        """Three distinct case roles in the image."""
        functor = tripartite_functor()
        image = functor.image_roles()
        assert len(image) == 3


class TestMonoidalFunctor:
    """Tests for the MonoidalFunctor tensor preservation checking."""

    def test_preserves_tensor_with_injective_map(self):
        """Injective functor preserves tensor for distinct mapped roles."""
        source = CaseCategory("Source")
        target = CaseCategory("Target")
        for role in [CaseRole.NOM, CaseRole.ACC]:
            source.add_role(role)
        for role in [CaseRole.ERG, CaseRole.ABS]:
            target.add_role(role)
        functor = MonoidalFunctor(
            name="Injective",
            source=source, target=target,
            object_map={CaseRole.NOM: CaseRole.ERG, CaseRole.ACC: CaseRole.ABS},
        )
        assert functor.preserves_tensor(CaseRole.NOM, CaseRole.ACC)

    def test_preserves_tensor_fails_on_collapse(self):
        """Non-injective functor fails tensor: distinct roles merge."""
        source = CaseCategory("Source")
        target = CaseCategory("Target")
        for role in [CaseRole.S, CaseRole.P]:
            source.add_role(role)
        target.add_role(CaseRole.ABS)
        # Both S and P map to ABS — tensor collapses
        functor = MonoidalFunctor(
            name="Collapsing",
            source=source, target=target,
            object_map={CaseRole.S: CaseRole.ABS, CaseRole.P: CaseRole.ABS},
        )
        assert not functor.preserves_tensor(CaseRole.S, CaseRole.P)

    def test_preserves_tensor_unmapped_role_fails(self):
        """Unmapped roles cannot preserve tensor."""
        source = CaseCategory("Source")
        target = CaseCategory("Target")
        functor = MonoidalFunctor(name="Empty", source=source, target=target)
        assert not functor.preserves_tensor(CaseRole.NOM, CaseRole.ACC)

    def test_preserves_tensor_same_role(self):
        """Self-tensor A ⊗ A always preserves (no collapse possible)."""
        source = CaseCategory("Source")
        target = CaseCategory("Target")
        source.add_role(CaseRole.NOM)
        target.add_role(CaseRole.ERG)
        functor = MonoidalFunctor(
            name="Self",
            source=source, target=target,
            object_map={CaseRole.NOM: CaseRole.ERG},
        )
        assert functor.preserves_tensor(CaseRole.NOM, CaseRole.NOM)
