"""Seeded synthetic paraphrase-family claim corpora.

The generator produces, for a fixed seed and parameters, a corpus of typed
claim records organized in paraphrase families: every member of a family
shares the family's canonical cause, effect, relation, polarity, and regime
(the exact localization key), while the surface phrasing varies through
member-specific qualifier tokens chosen so that within-family cause/effect
token-set Jaccard stays at or above the diagnostics threshold by
construction. A family drawn against ``regime_conflict_rate`` becomes a
conflict family: it straddles two regime labels, and each regime side
carries one polarity-flipped duplicate under that side's regime. Regime
resolution therefore reports two regime-resolved conflicts per conflict
family, while projecting the regime away collapses them into a single
merged conflict. Provenance stubs record the family and member indices
verbatim.

Everything is a pure function of the passed RNG and the explicit
parameters; the same seed always yields byte-identical corpora.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from .adapter import to_canonical_dict

__all__ = [
    "MAX_MECHANISMS",
    "generate_claim_corpus",
    "generate_claim_corpus_seeded",
]

# Word banks are fixed constants: distinct (cause, effect) pairs for the
# first MAX_MECHANISMS family indices, so families never collide on the
# canonical key by accident.
_CAUSE_TERMS = (
    "rainfall", "voltage", "cortisol", "traffic", "calcium", "demand",
    "gravity", "insulin", "dopamine", "nutrients", "vibration", "oxygen",
    "glucose", "sunlight", "pressure", "noise",
)
_EFFECT_TERMS = (
    "runoff", "heating", "alertness", "congestion", "release", "supply",
    "erosion", "uptake", "firing", "growth", "wear", "fatigue", "sorting",
    "melting", "deformation", "interference",
)
_RELATIONS = ("causes", "modulates", "precedes")
_TEMPORAL_SCOPES = ("acute", "sustained", None)
_QUALIFIER_MARKERS = (
    "observed", "reported", "inferred", "summarized", "replicated",
    "documented", "annotated", "extracted",
)

MAX_MECHANISMS = len(_CAUSE_TERMS) * len(_EFFECT_TERMS)


def _family_polarity(index: int) -> str:
    return "positive" if index % 2 == 0 else "negative"


def _validate_parameters(n_mechanisms: int, paraphrases_per_mechanism: int,
                         regime_conflict_rate: float) -> None:
    if isinstance(n_mechanisms, bool) or not isinstance(n_mechanisms, int) \
            or not 1 <= n_mechanisms <= MAX_MECHANISMS:
        raise ValueError(
            f"n_mechanisms must be an integer in [1, {MAX_MECHANISMS}], "
            f"got {n_mechanisms!r}")
    if isinstance(paraphrases_per_mechanism, bool) \
            or not isinstance(paraphrases_per_mechanism, int) \
            or paraphrases_per_mechanism < 1:
        raise ValueError("paraphrases_per_mechanism must be an integer >= 1, "
                         f"got {paraphrases_per_mechanism!r}")
    if isinstance(regime_conflict_rate, bool) \
            or not isinstance(regime_conflict_rate, (int, float)) \
            or not 0.0 <= float(regime_conflict_rate) <= 1.0:
        raise ValueError("regime_conflict_rate must lie in [0, 1], "
                         f"got {regime_conflict_rate!r}")


def generate_claim_corpus(
    rng: np.random.Generator, *, n_mechanisms: int,
    paraphrases_per_mechanism: int, regime_conflict_rate: float,
) -> list[dict[str, Any]]:
    """Generate one deterministic synthetic claim corpus.

    Args:
        rng: Numpy generator (in the experiments, one replicate stream).
        n_mechanisms: Number of paraphrase families (distinct canonical
            mechanisms).
        paraphrases_per_mechanism: Records per family; members share the
            family's canonical cause, effect, relation, and polarity and
            vary only in qualifier tokens.
        regime_conflict_rate: Probability per family of being a conflict
            family. A conflict family straddles two regime labels, and each
            regime side additionally carries one polarity-flipped duplicate
            under that side's regime: the same causal claim asserted with
            the opposite polarity under each of two regimes. At regime
            resolution each side is one conflict (both polarities share the
            regime); projecting the regime away collapses the two sides
            into a single merged conflict.

    Returns:
        List of typed canonical claim records (see
        :func:`src.aggregation.adapter.to_canonical_dict`).

    Raises:
        ValueError: On any out-of-range parameter or invalid draw.
    """
    _validate_parameters(n_mechanisms, paraphrases_per_mechanism,
                         regime_conflict_rate)
    records: list[dict[str, Any]] = []
    for family in range(n_mechanisms):
        cause = _CAUSE_TERMS[family % len(_CAUSE_TERMS)]
        effect = _EFFECT_TERMS[(family // len(_CAUSE_TERMS)) % len(_EFFECT_TERMS)]
        relation = _RELATIONS[family % len(_RELATIONS)]
        polarity = _family_polarity(family)
        flipped = "negative" if polarity == "positive" else "positive"
        conflict = rng.random() < float(regime_conflict_rate)
        sides: tuple[str | None, ...]
        if conflict:
            sides = (f"regime_{family}a", f"regime_{family}b")
        else:
            sides = (f"regime_{family}" if rng.random() < 0.5 else None,)
        temporal_scope = _TEMPORAL_SCOPES[int(rng.integers(0, len(_TEMPORAL_SCOPES)))]
        for member in range(paraphrases_per_mechanism):
            marker = _QUALIFIER_MARKERS[
                int(rng.integers(0, len(_QUALIFIER_MARKERS)))]
            qualifiers = [f"template_{member}", f"{marker} paraphrase"]
            records.append(to_canonical_dict({
                "cause": cause,
                "effect": effect,
                "relation": relation,
                "polarity": polarity,
                "regime": sides[member % len(sides)],
                "temporal_scope": temporal_scope,
                "qualifiers": qualifiers,
                "provenance": {
                    "generator": "src.aggregation.synthetic",
                    "family": family,
                    "member": member,
                    "conflict": conflict,
                },
            }))
        if conflict:
            for side in sides:
                records.append(to_canonical_dict({
                    "cause": cause,
                    "effect": effect,
                    "relation": relation,
                    "polarity": flipped,
                    "regime": side,
                    "temporal_scope": temporal_scope,
                    "qualifiers": ["template_conflict", "flipped duplicate"],
                    "provenance": {
                        "generator": "src.aggregation.synthetic",
                        "family": family,
                        "member": paraphrases_per_mechanism,
                        "conflict": True,
                    },
                }))
    return records


def generate_claim_corpus_seeded(
    seed: int, *, n_mechanisms: int, paraphrases_per_mechanism: int,
    regime_conflict_rate: float,
) -> list[dict[str, Any]]:
    """Seed convenience wrapper around :func:`generate_claim_corpus`."""
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a nonnegative integer, got {seed!r}")
    return generate_claim_corpus(
        np.random.default_rng(seed),
        n_mechanisms=n_mechanisms,
        paraphrases_per_mechanism=paraphrases_per_mechanism,
        regime_conflict_rate=regime_conflict_rate,
    )
