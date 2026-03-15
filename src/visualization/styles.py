"""Visual styling constants for publication-quality figures.

Defines the colorblind-friendly palette and typography standards
used across all visualization functions. All figures must satisfy
the 16pt font floor for accessibility.
"""

# 16pt minimum font size for accessibility (RASP standard)
FONT_SIZE_FLOOR = 16
FONT_SIZE_TITLE = 20
FONT_SIZE_LABEL = 16
FONT_SIZE_ANNOTATION = 14

# Case role color palette — dark, saturated, colorblind-friendly
CASE_COLORS: dict[str, str] = {
    "NOM": "#2563EB",   # Blue
    "ACC": "#DC2626",   # Red
    "GEN": "#059669",   # Emerald
    "DAT": "#7C3AED",   # Violet
    "INS": "#D97706",   # Amber
    "LOC": "#0891B2",   # Cyan
    "ABL": "#BE185D",   # Rose
    "VOC": "#4B5563",   # Gray
    "ERG": "#9333EA",   # Purple
    "ABS": "#0D9488",   # Teal
    "S": "#6366F1",     # Indigo
    "A": "#EF4444",     # Bright Red
    "P": "#10B981",     # Green
}

# Figure DPI for publication
FIGURE_DPI = 300

# Default figure size (inches)
DEFAULT_FIGSIZE = (10, 8)
WIDE_FIGSIZE = (14, 8)
COMPARISON_FIGSIZE = (16, 6)
