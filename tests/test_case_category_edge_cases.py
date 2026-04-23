"""Edge-case tests for CaseCategory and Morphism — weight validation."""
import time

import pytest

from src.case_systems.case_category import (
    CaseCategory,
    CaseRole,
    Morphism,
    minimal_case_category,
    standard_case_category,
)


class TestMorphismWeightValidation:
    def test_weight_at_zero_accepted(self):
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "test", weight=0.0)
        assert m.weight == 0.0

    def test_weight_at_one_accepted(self):
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "test", weight=1.0)
        assert m.weight == 1.0

    def test_weight_midpoint_accepted(self):
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "test", weight=0.5)
        assert m.weight == 0.5

    def test_weight_above_one_raises(self):
        with pytest.raises(ValueError, match="weight must be in"):
            Morphism(CaseRole.NOM, CaseRole.ACC, "bad", weight=1.1)

    def test_weight_negative_raises(self):
        with pytest.raises(ValueError, match="weight must be in"):
            Morphism(CaseRole.NOM, CaseRole.ACC, "bad", weight=-0.01)

    def test_weight_far_above_one_raises(self):
        with pytest.raises(ValueError, match="weight must be in"):
            Morphism(CaseRole.NOM, CaseRole.ACC, "bad", weight=2.5)


class TestAssociativityPerformance:
    def test_associativity_large_sparse_category_under_one_second(self):
        """associativity_holds() on a 20-morphism category must complete quickly."""
        cat = CaseCategory("PerfTest")
        for role in list(CaseRole)[:8]:
            cat.add_role(role)
        roles = list(cat.objects)
        for i in range(min(20, len(roles))):
            src = roles[i % len(roles)]
            tgt = roles[(i + 1) % len(roles)]
            cat.add_morphism(Morphism(src, tgt, f"m{i}", weight=0.8))

        start = time.monotonic()
        cat.associativity_holds()
        elapsed = time.monotonic() - start
        assert elapsed < 1.0, f"associativity_holds took {elapsed:.2f}s (>1s)"

    def test_standard_category_is_well_formed(self):
        cat = standard_case_category()
        assert cat.is_well_formed()


class TestMonoidalFunctorPreservesTensor:
    def _make_monoidal_functor(self):
        """Create a MonoidalFunctor from a 3-role source to 3-role target."""
        from src.case_systems.functor import MonoidalFunctor

        src = CaseCategory("Src3")
        tgt = CaseCategory("Tgt3")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]:
            src.add_role(r)
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]:
            tgt.add_role(r)
        # Add morphisms so preserves_tensor can verify structure
        from src.case_systems.case_category import Morphism as M
        src.add_morphism(M(CaseRole.NOM, CaseRole.ACC, "acts_on"))
        tgt.add_morphism(M(CaseRole.NOM, CaseRole.ACC, "acts_on"))

        return MonoidalFunctor(
            name="TestMonoidal",
            source=src,
            target=tgt,
            object_map={
                CaseRole.NOM: CaseRole.NOM,
                CaseRole.ACC: CaseRole.ACC,
                CaseRole.GEN: CaseRole.GEN,
            },
        )

    def test_injective_functor_preserves_distinct_pair(self):
        f = self._make_monoidal_functor()
        # NOM → NOM, ACC → ACC: distinct, no collapse
        assert f.preserves_tensor(CaseRole.NOM, CaseRole.ACC) is True

    def test_identity_pair_always_preserved(self):
        f = self._make_monoidal_functor()
        # Same role with itself: trivially preserved
        assert f.preserves_tensor(CaseRole.NOM, CaseRole.NOM) is True

    def test_collapsed_roles_fail_tensor(self):
        """A functor that maps two distinct roles to the same target fails tensor check."""
        from src.case_systems.functor import MonoidalFunctor

        src = CaseCategory("SrcCollapse")
        tgt = CaseCategory("TgtCollapse")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.ERG]:
            src.add_role(r)
        for r in [CaseRole.ERG, CaseRole.ABS]:
            tgt.add_role(r)

        f = MonoidalFunctor(
            name="Collapsing",
            source=src,
            target=tgt,
            object_map={
                CaseRole.NOM: CaseRole.ERG,
                CaseRole.ACC: CaseRole.ERG,  # NOM and ACC both → ERG = collapse!
                CaseRole.ERG: CaseRole.ABS,
            },
        )
        assert f.preserves_tensor(CaseRole.NOM, CaseRole.ACC) is False

    def test_unmapped_role_returns_false(self):
        """Role not in object_map → False (unmapped roles cannot preserve tensor)."""
        from src.case_systems.functor import MonoidalFunctor

        src = CaseCategory("SrcPartial")
        tgt = CaseCategory("TgtPartial")
        for r in [CaseRole.NOM]:
            src.add_role(r)
        for r in [CaseRole.NOM]:
            tgt.add_role(r)

        f = MonoidalFunctor(
            name="Partial",
            source=src,
            target=tgt,
            object_map={CaseRole.NOM: CaseRole.NOM},
        )
        # VOC not in object_map
        assert f.preserves_tensor(CaseRole.NOM, CaseRole.VOC) is False


class TestFloatToleranceConstant:
    def test_tolerance_is_defined(self):
        from case_systems.case_category import _FLOAT_TOLERANCE
        assert _FLOAT_TOLERANCE == 1e-9

    def test_weight_at_tolerance_boundary_accepted(self):
        # Exactly at boundary
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "boundary", weight=0.0)
        assert m.weight == 0.0
        m2 = Morphism(CaseRole.NOM, CaseRole.ACC, "boundary2", weight=1.0)
        assert m2.weight == 1.0
