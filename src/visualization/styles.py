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
POLAR_FIGSIZE = (8, 8)        # Radar / polar charts
NARROW_FIGSIZE = (9, 6)       # Two-column comparison bars
SQUARE_FIGSIZE = (8, 6)       # Single compact charts
DISCOPY_SINGLE_FIGSIZE = (10, 5)      # Single DisCoPy sentence
DISCOPY_WIDE_FIGSIZE = (16, 6)        # Wide DisCoPy sentence
DISCOPY_DISCOURSE_FIGSIZE = (22, 6)   # Multi-sentence discourse

# ─── Semantic colours (reused across multiple modules) ──────────────────────
COLOR_EDGE = "#1F2937"            # Dark charcoal — edges, box outlines
COLOR_TEXT = "#374151"            # Slightly lighter — axis text, labels
COLOR_NEUTRAL = "#6B7280"         # Mid-gray — fallback/unknown case roles
COLOR_WIRE = "#D1D5DB"            # Light gray — connecting wires
COLOR_ANNOTATION_DARK = "#333333" # Near-black — annotation overlay text
COLOR_FUNCTOR_ARROW = "#9333EA"   # Purple — functor mapping arrows
COLOR_ENTITY_WIRE = "#3B82F6"     # Blue — entity state wires in DisCoCirc
COLOR_ENTITY_BORDER = "#1E40AF"   # Dark blue — entity wire border
COLOR_UNKNOWN = "#808080"          # Pure mid-gray — truly unknown/unmapped roles

# ─── Severity colour tiers (§9b Cognitive Security) ─────────────────────────
COLOR_SEVERITY_HIGH = "#e74c3c"    # Red   — severity ≥ SEVERITY_HIGH_THRESHOLD
COLOR_SEVERITY_MED = "#f39c12"     # Orange — severity ≥ SEVERITY_MED_THRESHOLD
COLOR_SEVERITY_LOW = "#f1c40f"     # Yellow — severity < SEVERITY_MED_THRESHOLD

SEVERITY_HIGH_THRESHOLD: float = 0.8   # Maps to COLOR_SEVERITY_HIGH
SEVERITY_MED_THRESHOLD: float = 0.5    # Maps to COLOR_SEVERITY_MED (else LOW)

# ─── Bar chart layout constants ──────────────────────────────────────────────
BAR_ALPHA: float = 0.85            # Standard bar opacity
BAR_EDGE_COLOR: str = "black"      # Bar edge colour
BAR_WIDTH_NARROW: float = 0.25    # Grouped bar chart (3-bar groups)
BAR_WIDTH_STANDARD: float = 0.35  # Two-bar comparison
BAR_WIDTH_WIDE: float = 0.6       # Single-metric bars

# ─── Axis / grid constants ───────────────────────────────────────────────────
GRID_ALPHA: float = 0.3     # Grid line transparency
LINE_WIDTH_WIRE: float = 2.0
LINE_WIDTH_EDGE: float = 2.0
MARKER_SIZE: float = 12.0

# ─── Threshold constants (algorithm-level) ───────────────────────────────────
HEATMAP_TEXT_PIVOT: float = 0.6    # Enriched heatmap: white text if value > pivot
FLUID_S_AGENT_THRESHOLD: float = 0.5   # Fluid-S: line for ergative vs. absolutive


def mathtext_safe_arrows(text: str) -> str:
    """Replace Unicode symbols Helvetica often lacks with mathtext ``$...$`` fragments.

    Covers arrows, checkmarks, and ring operator (composition) so titles and NetworkX
    labels render when ``font.sans-serif`` resolves to Helvetica.
    """
    if not text:
        return text
    return (
        text.replace("\u2192", r"$\rightarrow$")
        .replace("\u21d2", r"$\Rightarrow$")
        .replace("\u2190", r"$\leftarrow$")
        .replace("\u2194", r"$\leftrightarrow$")
        .replace("\u2713", r"$\checkmark$")
        .replace("\u2717", r"$\times$")
        .replace("\u2218", r"$\circ$")
    )
