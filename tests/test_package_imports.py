"""Integration tests: top-level package import paths."""

import subprocess
import sys


def test_import_src_does_not_eagerly_load_heavy_dependencies():
    """PEP 562 lazy loading: `import src` must not pull discopy/matplotlib/networkx."""
    code = "import src, sys; missing = {'discopy', 'matplotlib', 'networkx'} & sys.modules.keys(); assert not missing, missing"
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


def test_unknown_attribute_fails_closed():
    import src
    try:
        src.nonexistent_export
    except AttributeError as exc:
        assert "nonexistent_export" in str(exc)
    else:
        raise AssertionError("expected AttributeError for unknown export")


def test_subpackage_module_access():
    import src
    import src.visualization as viz
    assert src.visualization is viz


def test_dir_covers_all_exports():
    import src
    names = dir(src)
    assert "CaseRole" in names and "push_forward_return" in names

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
