"""Tests for FluidSFunctor methods: map_morphism, kernel, bats_fluid_s,
fluid_s_enriched_weight. No mocks — real computations only.
"""
import pytest

from src.case_systems.case_category import CaseRole, Morphism
from src.case_systems.fluid_s import (
    FluidSFunctor,
    VolitionContext,
    bats_fluid_s,
    create_fluid_s_functor,
    fluid_s_enriched_weight,
)


class TestMapMorphism:
    def test_volitional_nom_morphism_stays_nom(self):
        f = create_fluid_s_functor(volitional=True)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "nom_to_acc")
        mapped = f.map_morphism(m)
        assert mapped.source == CaseRole.NOM
        assert mapped.target == CaseRole.ACC

    def test_non_volitional_nom_maps_to_acc(self):
        f = create_fluid_s_functor(volitional=False)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "nom_to_acc")
        mapped = f.map_morphism(m)
        # non-volitional: NOM source → ACC source
        assert mapped.source == CaseRole.ACC

    def test_map_morphism_preserves_weight(self):
        f = create_fluid_s_functor(volitional=True)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "test", weight=0.75)
        mapped = f.map_morphism(m)
        assert abs(mapped.weight - 0.75) < 1e-12

    def test_oblique_morphism_passes_through(self):
        f = create_fluid_s_functor(volitional=True)
        m = Morphism(CaseRole.DAT, CaseRole.INS, "dat_to_ins")
        mapped = f.map_morphism(m)
        assert mapped.source == CaseRole.DAT
        assert mapped.target == CaseRole.INS


class TestKernel:
    def test_volitional_kernel_empty(self):
        """Volitional: NOM→NOM, ACC→ACC — no two distinct roles collapse."""
        f = create_fluid_s_functor(volitional=True)
        assert f.kernel() == []

    def test_non_volitional_kernel_has_pair(self):
        """Non-volitional: NOM→ACC, ACC→ACC — NOM and ACC collapse."""
        f = create_fluid_s_functor(volitional=False)
        kernel = f.kernel()
        assert len(kernel) == 1
        roles_in_kernel = {r for pair in kernel for r in pair}
        assert CaseRole.NOM in roles_in_kernel
        assert CaseRole.ACC in roles_in_kernel

    def test_kernel_returns_list(self):
        assert isinstance(create_fluid_s_functor().kernel(), list)


class TestBatsFluidS:
    def test_returns_tuple_of_two(self):
        result = bats_fluid_s()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_both_are_fluid_s_functors(self):
        vol, nonvol = bats_fluid_s()
        assert isinstance(vol, FluidSFunctor)
        assert isinstance(nonvol, FluidSFunctor)

    def test_volitional_functor_is_volitional(self):
        vol, _ = bats_fluid_s()
        assert vol.volition == VolitionContext.VOLITIONAL

    def test_non_volitional_functor_is_non_volitional(self):
        _, nonvol = bats_fluid_s()
        assert nonvol.volition == VolitionContext.NON_VOLITIONAL

    def test_functors_map_s_differently(self):
        """Core Bats distinction: S maps to different cases depending on volition."""
        vol, nonvol = bats_fluid_s()
        assert vol.map_object(CaseRole.NOM) != nonvol.map_object(CaseRole.NOM)


class TestFluidSEnrichedWeight:
    def test_full_volition_returns_base_weight(self):
        assert abs(fluid_s_enriched_weight(1.0, 0.9) - 0.9) < 1e-12

    def test_zero_volition_returns_zero(self):
        assert abs(fluid_s_enriched_weight(0.0, 0.8)) < 1e-12

    def test_partial_volition(self):
        result = fluid_s_enriched_weight(0.6, 1.0)
        assert abs(result - 0.6) < 1e-12

    def test_result_in_zero_one(self):
        for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
            w = fluid_s_enriched_weight(p)
            assert 0.0 <= w <= 1.0

    def test_invalid_probability_raises(self):
        with pytest.raises(ValueError, match="p_volitional"):
            fluid_s_enriched_weight(1.5)

    def test_invalid_base_weight_raises(self):
        with pytest.raises(ValueError, match="base_weight"):
            fluid_s_enriched_weight(0.5, 1.5)
