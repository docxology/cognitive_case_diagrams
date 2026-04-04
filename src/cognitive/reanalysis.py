"""Garden-path reanalysis cost and ERP magnitude proxies — §7 of the manuscript.

Magnitude-based reanalysis cost for garden-path sentences (P600)
and N400 semantic violation proxy via categorical magnitude change.
"""

import logging

from ..enriched_cat.enriched import EnrichedCategory

logger = logging.getLogger(__name__)


def magnitude_reanalysis_cost(
    enriched_before: EnrichedCategory,
    enriched_after: EnrichedCategory,
) -> float:
    """Compute garden-path reanalysis cost via magnitude change.

    The processing cost of reanalyzing a garden-path sentence should
    correlate with the change in categorical magnitude between the
    initial and revised case diagrams (manuscript §7).

    Δ|C| = ||C_after| − |C_before||

    Args:
        enriched_before: Enriched category before reanalysis.
        enriched_after: Enriched category after reanalysis.

    Returns:
        Absolute magnitude change (non-negative).
    """
    mag_before = enriched_before.magnitude()
    mag_after = enriched_after.magnitude()
    cost = abs(mag_after - mag_before)
    logger.info(
        "Reanalysis cost: |%.4f − %.4f| = %.4f",
        mag_after, mag_before, cost,
    )
    return cost


def n400_amplitude_proxy(
    enriched_before: EnrichedCategory,
    enriched_after: EnrichedCategory,
) -> float:
    """Compute N400 semantic violation proxy via magnitude change.

    The manuscript (§7) predicts that N400 amplitude for *semantic*
    violations correlates with the change in categorical magnitude,
    complementing the P600 prediction for *syntactic* violations.

    The N400 reflects early semantic retrieval difficulty, while the
    P600 reflects late structural reanalysis. Both map onto magnitude
    change, but are triggered by different violation types.

    Δ|C|_semantic = ||C_after| − |C_before||

    Args:
        enriched_before: Enriched category before semantic violation.
        enriched_after: Enriched category after semantic reanalysis.

    Returns:
        N400 amplitude proxy (non-negative float).
    """
    mag_before = enriched_before.magnitude()
    mag_after = enriched_after.magnitude()
    proxy = abs(mag_after - mag_before)
    logger.info(
        "N400 proxy: |%.4f − %.4f| = %.4f",
        mag_after, mag_before, proxy,
    )
    return proxy
