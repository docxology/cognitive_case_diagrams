"""Tests for the Fluid-S context-dependent functor module.

Validates Fluid-S alignment, volition-based mapping, probability splits,
Bats language examples, and enriched weight computations.
All tests use real computations — no mocks.
"""

import pytest

from src.case_systems.case_category import CaseRole
from src.case_systems.fluid_s import (
    FluidSFunctor,
    VolitionContext,
    create_fluid_s_functor,
    bats_fluid_s,
    fluid_s_enriched_weight,
)


class TestFluidSFunctorCreation:
    """Tests for FluidSFunctor construction."""

    def test_default_creation(self) -> None:
        """Default functor is volitional with probability 1.0."""
        f = FluidSFunctor()
        assert f.volition == VolitionContext.VOLITIONAL
        assert f.volition_probability == 1.0

    def test_non_volitional_creation(self) -> None:
        """Non-volitional functor."""
        f = FluidSFunctor(volition=VolitionContext.NON_VOLITIONAL)
        assert f.volition == VolitionContext.NON_VOLITIONAL

    def test_invalid_probability_raises(self) -> None:
        """Probability outside [0,1] raises ValueError."""
        with pytest.raises(ValueError):
            FluidSFunctor(volition_probability=1.5)

    def test_negative_probability_raises(self) -> None:
        """Negative probability raises ValueError."""
        with pytest.raises(ValueError):
            FluidSFunctor(volition_probability=-0.1)


class TestFluidSMapping:
    """Tests for object and morphism mapping."""

    def test_volitional_s_maps_to_nom(self) -> None:
        """Volitional S → NOM (agent-like)."""
        f = create_fluid_s_functor(volitional=True)
        assert f.map_object(CaseRole.NOM) == CaseRole.NOM

    def test_non_volitional_s_maps_to_acc(self) -> None:
        """Non-volitional S → ACC (patient-like)."""
        f = create_fluid_s_functor(volitional=False)
        assert f.map_object(CaseRole.NOM) == CaseRole.ACC

    def test_acc_unchanged(self) -> None:
        """ACC passes through unchanged in both contexts."""
        vol = create_fluid_s_functor(volitional=True)
        nonvol = create_fluid_s_functor(volitional=False)
        assert vol.map_object(CaseRole.ACC) == CaseRole.ACC
        assert nonvol.map_object(CaseRole.ACC) == CaseRole.ACC

    def test_oblique_cases_pass_through(self) -> None:
        """Oblique cases (GEN, DAT, INS, LOC, ABL, VOC) pass through."""
        f = create_fluid_s_functor(volitional=True)
        for role in [CaseRole.GEN, CaseRole.DAT, CaseRole.INS,
                     CaseRole.LOC, CaseRole.ABL, CaseRole.VOC]:
            assert f.map_object(role) == role

    def test_identity_preserved(self) -> None:
        """Functor preserves identity at every role."""
        f = create_fluid_s_functor(volitional=True)
        for role in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            assert f.preserves_identity(role)


class TestFluidSProbability:
    """Tests for graded (probabilistic) Fluid-S mapping."""

    def test_full_volitional_deterministic(self) -> None:
        """p=1.0 gives deterministic NOM mapping for S."""
        f = create_fluid_s_functor(volitional=True, probability=1.0)
        dist = f.split_probability(CaseRole.NOM)
        assert dist[CaseRole.NOM] == pytest.approx(1.0)
        assert dist[CaseRole.ACC] == pytest.approx(0.0)

    def test_full_non_volitional_deterministic(self) -> None:
        """p=0.0 gives deterministic ACC mapping for S."""
        f = create_fluid_s_functor(volitional=True, probability=0.0)
        dist = f.split_probability(CaseRole.NOM)
        assert dist[CaseRole.NOM] == pytest.approx(0.0)
        assert dist[CaseRole.ACC] == pytest.approx(1.0)

    def test_half_probability(self) -> None:
        """p=0.5 gives equal split."""
        f = create_fluid_s_functor(volitional=True, probability=0.5)
        dist = f.split_probability(CaseRole.NOM)
        assert dist[CaseRole.NOM] == pytest.approx(0.5)
        assert dist[CaseRole.ACC] == pytest.approx(0.5)

    def test_non_s_role_deterministic(self) -> None:
        """Non-S roles always give deterministic mapping."""
        f = create_fluid_s_functor(volitional=True, probability=0.5)
        dist = f.split_probability(CaseRole.ACC)
        assert dist[CaseRole.ACC] == pytest.approx(1.0)

    def test_probabilities_sum_to_one(self) -> None:
        """Probability distribution always sums to 1."""
        f = create_fluid_s_functor(volitional=True, probability=0.7)
        dist = f.split_probability(CaseRole.NOM)
        assert sum(dist.values()) == pytest.approx(1.0)

    def test_invalid_context_probability_raises(self) -> None:
        """Invalid p_volitional in map_object_in_context raises."""
        f = FluidSFunctor()
        with pytest.raises(ValueError):
            f.map_object_in_context(CaseRole.NOM, 2.0)


class TestBatsLanguage:
    """Tests for the Bats (Nakh-Daghestanian) canonical example."""

    def test_bats_pair_creation(self) -> None:
        """Bats creates a (volitional, non-volitional) pair."""
        vol, nonvol = bats_fluid_s()
        assert vol.volition == VolitionContext.VOLITIONAL
        assert nonvol.volition == VolitionContext.NON_VOLITIONAL

    def test_bats_volitional_fall(self) -> None:
        """Volitional 'fall on purpose' → S gets ERG-like (NOM)."""
        vol, _ = bats_fluid_s()
        assert vol.map_object(CaseRole.NOM) == CaseRole.NOM

    def test_bats_accidental_fall(self) -> None:
        """Accidental 'fall' → S gets ABS-like (ACC)."""
        _, nonvol = bats_fluid_s()
        assert nonvol.map_object(CaseRole.NOM) == CaseRole.ACC


class TestFluidSKernel:
    """Tests for functor kernel computation."""

    def test_volitional_kernel_empty(self) -> None:
        """Volitional functor: NOM ≠ ACC, so kernel is empty."""
        f = create_fluid_s_functor(volitional=True)
        assert len(f.kernel()) == 0

    def test_non_volitional_kernel_merges(self) -> None:
        """Non-volitional functor: NOM→ACC, ACC→ACC, so kernel = {(NOM,ACC)}."""
        f = create_fluid_s_functor(volitional=False)
        kernel = f.kernel()
        assert len(kernel) == 1
        assert (CaseRole.NOM, CaseRole.ACC) in kernel


class TestEnrichedWeight:
    """Tests for enriched weight computation."""

    def test_full_volitional_weight(self) -> None:
        """Full volition preserves base weight."""
        assert fluid_s_enriched_weight(1.0, 0.9) == pytest.approx(0.9)

    def test_zero_volitional_weight(self) -> None:
        """Zero volition eliminates weight."""
        assert fluid_s_enriched_weight(0.0, 0.9) == pytest.approx(0.0)

    def test_partial_volitional_weight(self) -> None:
        """Partial volition scales weight multiplicatively."""
        assert fluid_s_enriched_weight(0.5, 0.8) == pytest.approx(0.4)

    def test_invalid_volitional_raises(self) -> None:
        """Invalid p_volitional raises ValueError."""
        with pytest.raises(ValueError):
            fluid_s_enriched_weight(1.5, 0.5)

    def test_invalid_base_weight_raises(self) -> None:
        """Invalid base_weight raises ValueError."""
        with pytest.raises(ValueError):
            fluid_s_enriched_weight(0.5, 1.5)
