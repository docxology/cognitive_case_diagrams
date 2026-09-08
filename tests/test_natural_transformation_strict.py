"""P1-10 acceptance controls: transformation identity + strict composition."""
import pytest

from src.case_systems.case_category import CaseCategory, CaseRole
from src.case_systems.functor import AlignmentFunctor
from src.case_systems.natural_transformation import (
    ComponentMorphism,
    IdentityNaturalTransformation,
    NaturalTransformation,
    compose_transformations,
)


def _three_role_setup():
    src_cat = CaseCategory(name="C")
    for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT):
        src_cat.add_role(r)
    tgt_cat = CaseCategory(name="T")
    for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT):
        tgt_cat.add_role(r)
    F = AlignmentFunctor(name="F", source=src_cat, target=tgt_cat,
                         object_map={r: r for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)})
    G = AlignmentFunctor(name="G", source=tgt_cat, target=tgt_cat,
                         object_map={r: r for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)})
    return src_cat, tgt_cat, F, G


def _full_nt(name, f, g, weights):
    nt = NaturalTransformation(name=name, source_functor=f, target_functor=g)
    for r in f.object_map:
        nt.set_component(r, ComponentMorphism(
            object_name=r, source_image=f.object_map[r], target_image=g.object_map[r],
            weight=weights.get(r, 1.0)))
    return nt


class TestWarnOnlyBaseSemantics:
    def test_same_name_different_objects_warn_not_raise(self, caplog):
        # Base semantics preserved (criterion 4: keep the warning): the
        # structural condition decides the warning; no raise at construction.
        c1 = CaseCategory(name="SameName"); c1.add_role(CaseRole.NOM)
        c2 = CaseCategory(name="SameName"); c2.add_role(CaseRole.ACC)
        fa = AlignmentFunctor(name="F", source=c1, target=c1, object_map={CaseRole.NOM: CaseRole.NOM})
        ga = AlignmentFunctor(name="G", source=c2, target=c2, object_map={CaseRole.ACC: CaseRole.ACC})
        with caplog.at_level("WARNING"):
            NaturalTransformation(name="alpha", source_functor=fa, target_functor=ga)
        assert any("do not share categories" in r.message for r in caplog.records)

    def test_genuinely_equal_categories_no_warning(self, caplog):
        c1 = CaseCategory(name="SameName"); c1.add_role(CaseRole.NOM)
        c2 = CaseCategory(name="SameName"); c2.add_role(CaseRole.NOM)
        fa = AlignmentFunctor(name="F", source=c1, target=c1, object_map={CaseRole.NOM: CaseRole.NOM})
        ga = AlignmentFunctor(name="G", source=c2, target=c2, object_map={CaseRole.NOM: CaseRole.NOM})
        with caplog.at_level("WARNING"):
            NaturalTransformation(name="alpha", source_functor=fa, target_functor=ga)
        assert not any("do not share categories" in r.message for r in caplog.records)


class TestIdentityGuard:
    def test_empty_object_map_raises(self):
        src_cat = CaseCategory(name="C")
        F = AlignmentFunctor(name="F", source=src_cat, target=src_cat, object_map={})
        with pytest.raises(ValueError, match="object map"):
            IdentityNaturalTransformation(F)

    def test_identity_covers_every_object(self):
        _, _, F, _ = _three_role_setup()
        ident = IdentityNaturalTransformation(F)
        assert set(ident.components) == set(F.object_map)
        for role, comp in ident.components.items():
            assert comp.source_image == F.object_map[role]
            assert comp.target_image == F.object_map[role]
            assert comp.weight == 1.0


class TestStrictComposition:
    def test_missing_beta_role_raises_listing_roles(self):
        src_cat, tgt_cat, F, G = _three_role_setup()
        alpha = NaturalTransformation(name="a", source_functor=F, target_functor=G)
        for r in F.object_map:
            alpha.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        beta = NaturalTransformation(name="b", source_functor=G, target_functor=G)
        for r in (CaseRole.NOM, CaseRole.ACC):
            beta.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        with pytest.raises(ValueError, match="beta lacks"):
            compose_transformations(alpha, beta)

    def test_missing_alpha_role_raises_both_directions(self):
        src_cat, tgt_cat, F, G = _three_role_setup()
        alpha = NaturalTransformation(name="a", source_functor=F, target_functor=G)
        for r in (CaseRole.NOM, CaseRole.ACC):
            alpha.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        beta = NaturalTransformation(name="b", source_functor=G, target_functor=G)
        for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT):
            beta.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        with pytest.raises(ValueError, match="alpha lacks"):
            compose_transformations(alpha, beta)

    def test_ordinary_composition_exact_on_input(self):
        src_cat, tgt_cat, F, G = _three_role_setup()
        weights = {CaseRole.NOM: 0.9, CaseRole.ACC: 0.7, CaseRole.DAT: 0.5}
        beta_weights = {CaseRole.NOM: 0.8, CaseRole.ACC: 0.6, CaseRole.DAT: 0.4}
        alpha = _full_nt("a", F, G, weights)
        beta = _full_nt("b", G, G, beta_weights)
        comp = compose_transformations(alpha, beta)
        assert comp.is_complete()
        for r in (CaseRole.NOM, CaseRole.ACC, CaseRole.DAT):
            comp_c = comp.components[r]
            assert comp_c.source_image == alpha.components[r].source_image
            assert comp_c.target_image == beta.components[r].target_image
            assert comp_c.weight == weights[r] * beta_weights[r]  # exact product on inputs

    def test_composable_pair_mismatch_raises(self):
        src_cat, tgt_cat, F, G = _three_role_setup()
        alpha = NaturalTransformation(name="a", source_functor=F, target_functor=G)
        for r in F.object_map:
            alpha.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        beta = NaturalTransformation(name="b", source_functor=G, target_functor=G)
        for r in G.object_map:
            beta.set_component(r, ComponentMorphism(object_name=r, source_image=r, target_image=r))
        # Break the alpha->beta thread directly (bypass set_component checks).
        beta.components[CaseRole.NOM] = ComponentMorphism(
            object_name=CaseRole.NOM, source_image=CaseRole.GEN, target_image=CaseRole.NOM)
        with pytest.raises(ValueError, match="target image"):
            compose_transformations(alpha, beta)