"""Aggregation and localization diagnostics over typed causal claim records.

This package is a synthetic, fail-closed lane mirroring the post-extraction
aggregation layer studied in the Democritus publication (S. Mahadevan,
"Democritus: Homotopy-Localized Causal Discourse Extraction from Language,"
Entropy 2026, doi:10.3390/e28090986): typed records are localized into
canonical claim classes, and pairwise compatibility statistics are computed
inside each class. Nothing here touches a real corpus; every consumer passes
records produced by :mod:`src.aggregation.synthetic` or by an explicitly
trusted upstream extractor.

Fail-closed conventions match the rest of the repository: invalid inputs
raise ``ValueError`` naming the offending line or field, and no function
repairs, drops, or coerces a malformed record.
"""
from .adapter import load_claim_records, to_canonical_dict
from .diagnostics import (
    class_paraphrase_inflation,
    compatibility_graph,
    corpus_paraphrase_inflation,
    normalized_tokens,
    regime_conflicts,
    regime_conflicts_projected,
    token_jaccard,
    triangle_closure,
)
from .localize import canonical_key, localize, without_regime
from .synthetic import generate_claim_corpus, generate_claim_corpus_seeded

__all__ = [
    "load_claim_records",
    "to_canonical_dict",
    "canonical_key",
    "localize",
    "without_regime",
    "class_paraphrase_inflation",
    "corpus_paraphrase_inflation",
    "compatibility_graph",
    "triangle_closure",
    "regime_conflicts",
    "regime_conflicts_projected",
    "normalized_tokens",
    "token_jaccard",
    "generate_claim_corpus",
    "generate_claim_corpus_seeded",
]
