"""Deterministic RNG derivation for the synthetic experiments.

Every random draw in the experiments is addressed by a triple
``(master_seed, stream_name, replicate_index)``. Stream names map to fixed
integer stream ids that are part of the frozen results schema: changing a
stream id changes every number in that stream, so ids are constants here and
never derived from hashing at import time.
"""
from __future__ import annotations

import numpy as np

__all__ = ["STREAM_IDS", "replicate_rng", "master_rng"]

# Fixed stream identifiers (frozen schema; do not renumber).
STREAM_IDS: dict[str, int] = {
    "filtering": 1,
    "calibration": 2,
    "quantile": 3,
    "projection": 4,
    "sensitivity": 5,
    "sanity": 6,
    "quantum": 7,
}


def replicate_rng(seed: int, stream: str, replicate: int) -> np.random.Generator:
    """Return the PCG64 generator for one (stream, replicate) draw set.

    Args:
        seed: Master seed from :class:`ExperimentConfig`.
        stream: One of the keys of ``STREAM_IDS``.
        replicate: Non-negative replicate index.

    Raises:
        KeyError: If ``stream`` is not a registered stream name.
        ValueError: If ``replicate`` is negative.
    """
    if stream not in STREAM_IDS:
        raise KeyError(f"unknown RNG stream {stream!r}; known: {sorted(STREAM_IDS)}")
    if replicate < 0:
        raise ValueError(f"replicate index must be >= 0, got {replicate}")
    seq = np.random.SeedSequence(seed, spawn_key=(STREAM_IDS[stream], replicate))
    return np.random.Generator(np.random.PCG64(seq))


def master_rng(seed: int) -> np.random.Generator:
    """Return the master generator (reserved; studies use replicate streams)."""
    if seed < 0:
        raise ValueError(f"seed must be >= 0, got {seed}")
    return np.random.default_rng(seed)
