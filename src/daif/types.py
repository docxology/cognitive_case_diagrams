"""Shared type definitions for Distributional Active Inference (DAIF).

Provides typed data containers used across all DAIF sub-modules:
DistributionalReturn, DAIFResult, ERPProfile.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import NamedTuple

import numpy as np

from ..cognitive.belief import CaseDiagramBelief

logger = logging.getLogger(__name__)


class DistributionalReturn(NamedTuple):
    """Full distributional representation of a return distribution Z(s).

    Stores the moments and quantile parameterization of the return
    distribution maintained by the DAIF agent, as per Akgül et al. (2026).

    Attributes:
        mean: Expected return E[Z].
        variance: Return variance Var[Z].
        quantiles: Sorted array of quantile values.
        quantile_levels: Corresponding quantile levels τ ∈ (0, 1).
    """
    mean: float
    variance: float
    quantiles: np.ndarray
    quantile_levels: np.ndarray

    def std(self) -> float:
        """Standard deviation of the return distribution."""
        return float(np.sqrt(self.variance))

    def ci(self, alpha: float = 0.05) -> tuple[float, float]:
        """Approximate (1-alpha) credible interval using stored quantiles.

        Args:
            alpha: Significance level. Default 0.05 → 95% CI.

        Returns:
            (lower, upper) quantile values.
        """
        lo = float(np.interp(alpha / 2, self.quantile_levels, self.quantiles))
        hi = float(np.interp(1 - alpha / 2, self.quantile_levels, self.quantiles))
        return lo, hi

    def to_categorical(self, v_min: float, v_max: float, n_atoms: int = 51) -> np.ndarray:
        """Project quantiles onto a C51-style categorical support.

        Args:
            v_min: Minimum support value.
            v_max: Maximum support value.
            n_atoms: Number of categorical atoms.

        Returns:
            Probability mass on each atom (sums to 1).
        """
        atoms = np.linspace(v_min, v_max, n_atoms)
        # Histogram the quantiles onto atoms
        counts, _ = np.histogram(self.quantiles, bins=np.append(atoms, v_max + 1e-8))
        total = counts.sum()
        if total == 0:
            return np.full(n_atoms, 1.0 / n_atoms)
        return counts.astype(np.float64) / total


@dataclass
class DAIFResult:
    """Result container for distributional case assignment inference.

    Attributes:
        belief: Final posterior CaseDiagramBelief.
        fe_trajectory: Free energy at each iteration.
        convergence_iteration: Iteration at which ΔF < threshold (or n_iters).
        return_distribution: Full return distribution at convergence.
        diagnostics: Dict of additional diagnostic statistics.
    """
    belief: CaseDiagramBelief
    fe_trajectory: list[float]
    convergence_iteration: int
    return_distribution: DistributionalReturn | None = None
    diagnostics: dict = field(default_factory=dict)

    @property
    def converged(self) -> bool:
        """True if iteration converged before the maximum iteration count."""
        return self.convergence_iteration < len(self.fe_trajectory)

    @property
    def final_fe(self) -> float:
        """Free energy at final iteration."""
        return self.fe_trajectory[-1] if self.fe_trajectory else float("nan")

    @property
    def fe_reduction(self) -> float:
        """Total reduction in free energy: F_0 - F_final."""
        if len(self.fe_trajectory) < 2:
            return 0.0
        return self.fe_trajectory[0] - self.fe_trajectory[-1]


@dataclass
class ERPProfile:
    """Predicted electrophysiological response profile from DAIF.

    Contains predicted N400 and P600 amplitudes and simulated
    waveform arrays for visualization and comparison with empirical data.

    Attributes:
        n400_amplitude: Predicted N400 amplitude in μV (negative = larger N400).
        p600_amplitude: Predicted P600 amplitude in μV (positive).
        waveform_ms: Time axis in milliseconds (e.g., −200 to 900 ms).
        waveform_uV: Voltage trace in μV.
        condition: Label for the violation condition (e.g., 'congruent').
        dpe: Distributional prediction error that generated both ERP components.
    """
    n400_amplitude: float
    p600_amplitude: float
    waveform_ms: np.ndarray
    waveform_uV: np.ndarray
    condition: str = "unknown"
    dpe: float = 0.0

    def peak_latency(self, component: str = "N400") -> float:
        """Return time (ms) of peak component amplitude.

        Args:
            component: 'N400' (200–500 ms) or 'P600' (500–900 ms).

        Returns:
            Latency in ms of the component peak.
        """
        if component == "N400":
            mask = (self.waveform_ms >= 200) & (self.waveform_ms <= 500)
        elif component == "P600":
            mask = (self.waveform_ms >= 500) & (self.waveform_ms <= 900)
        else:
            raise ValueError(f"Unknown component: {component!r}. Use 'N400' or 'P600'.")

        if not mask.any():
            return float("nan")
        win_ms = self.waveform_ms[mask]
        win_uV = self.waveform_uV[mask]
        if component == "N400":
            idx = np.argmin(win_uV)
        else:
            idx = np.argmax(win_uV)
        return float(win_ms[idx])
