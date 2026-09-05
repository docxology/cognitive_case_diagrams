```latex
\usepackage[margin=1.5cm]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{stmaryrd}
\usepackage{graphicx}
\usepackage{booktabs}
\tolerance=800
\hfuzz=2pt
\hypersetup{colorlinks=true, linkcolor=red, citecolor=red, urlcolor=red}

% Unicode-capable mono font for code listings.
% lmmono lacks the math/Greek/logic glyphs used in Python/categorial-grammar
% code blocks. JuliaMono ships with TeX Live and covers the full set
% (much/divides/QED) that DejaVuSansMono is missing (\\ll, \\mid, \\blacksquare).
% Fonts are looked up by name/file through kpathsea — no machine-specific
% Path. Fallback chain: JuliaMono → DejaVu Sans Mono → LaTeX default mono
% (DejaVu lacks \\ll; the default also lacks \\blacksquare).
\usepackage{fontspec}
\IfFontExistsTF{JuliaMono-Regular}{%
  \setmonofont{JuliaMono-Regular}[
    Extension      = .ttf,
    UprightFont    = *,
    BoldFont       = JuliaMono-Bold,
    ItalicFont     = JuliaMono-RegularItalic,
    BoldItalicFont = JuliaMono-BoldItalic,
    Scale          = MatchLowercase,
  ]
}{%
  \IfFontExistsTF{DejaVu Sans Mono}{%
    \setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]%
  }{%
    % Neither font installed: keep the LaTeX default mono font.
    % Some code glyphs may warn as missing characters.
  }%
}

% Math font for unicode-math: Latin Modern Math has full BMP coverage
% including U+2223 (\mid). Without an explicit \setmathfont, unicode-math's
% fallback chain ends in lmroman text, which lacks U+2223 and produces
% "Missing character" warnings for every \mid/\ll/\gg in math mode.
\setmathfont{latinmodern-math.otf}
```
