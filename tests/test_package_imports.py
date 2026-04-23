"""Integration tests: top-level package import paths."""


def test_top_level_case_role_import():
    from src import CaseRole
    assert CaseRole.NOM.value == "Nominative"


def test_top_level_morphism_import():
    from src import Morphism, CaseRole
    m = Morphism(source=CaseRole.NOM, target=CaseRole.ACC, label="acts_on")
    assert m.source == CaseRole.NOM


def test_top_level_standard_category_import():
    from src import standard_case_category
    cat = standard_case_category()
    assert len(cat.objects) > 0


def test_top_level_enriched_import():
    from src import standard_enriched_category
    cat = standard_enriched_category()
    assert cat.magnitude() > 0


def test_top_level_daif_imports():
    from src import push_forward_return, distributional_bellman_operator
    assert callable(push_forward_return)
    assert callable(distributional_bellman_operator)
