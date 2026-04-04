---
name: ccd-cognitive
description: Scalar active inference on case diagrams — beliefs, variational free energy, belief updates, prediction error, EFE, N400/P600 proxies. Use for §7; use src.daif for distributional returns and full ERP pipeline (§7c).
---

# `src/cognitive/`

## When to use

- Scalar (single-distribution) FEP quantities: KL / variational FE, Bayesian belief updates, precision-weighted PE, expected free energy, simple ERP amplitude proxies.
- **Not** for full return distributions, quantile TD, or Bethe/VMP blocks — those live in [`daif/`](../daif/).

## Primary imports

```python
from src.cognitive import (
    CaseDiagramBelief,
    kl_divergence, variational_free_energy,
    update_belief, sequential_belief_update,
    prediction_error, p600_amplitude_ratio,
    expected_free_energy,
    magnitude_reanalysis_cost, n400_amplitude_proxy,
)
```

## Manuscript

§7, §7b (scalar process theory and verification narrative).

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
