"""Static layout configuration for category diagram figures.

Constants are declared here so that ``generate_category_figures.py``
remains a thin orchestrator with no domain data inline.
"""

CASE_MINIMAL_NODE_POSITIONS: dict[str, tuple[float, float]] = {
    "NOM": (0.0, 1.0),
    "INS": (0.92, -0.52),
    "ACC": (-0.92, -0.52),
    "VOC": (-0.98, 0.48),
}

CASE_MINIMAL_EDGE_LABEL_PREFIX: dict[tuple[str, str], str] = {
    ("NOM", "INS"): "f: ",
    ("INS", "ACC"): "g: ",
    ("NOM", "ACC"): "h=g\u2218f: ",  # ∘
}

CASE_MINIMAL_LICENSED_CONNECTIONSTYLE: dict[tuple[str, str], str] = {
    ("NOM", "INS"): "arc3,rad=0.05",
    ("INS", "ACC"): "arc3,rad=0.05",
    ("NOM", "ACC"): "arc3,rad=-0.28",
    ("NOM", "VOC"): "arc3,rad=0.12",
}
