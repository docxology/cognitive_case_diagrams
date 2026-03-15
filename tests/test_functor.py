"""Tests for the functor module.

Validates alignment functor mapping, identity/composition preservation,
injectivity checking, and factory functions.
"""

import pytest

from src.case_systems.functor import (
    AlignmentFunctor,
    accusative_to_ergative_functor,
    tripartite_functor,
)
from src.case_systems.case_category import CaseRole, Morphism, CaseCategory


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
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        mapped = functor.map_morphism(m)
        assert mapped.source == CaseRole.ERG
        assert mapped.target == CaseRole.ABS
        assert "F(" in mapped.label

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
