# daif/ — §7c Distributional Active Inference

DAIF extends point-estimate active inference (`src/cognitive/`) with **return distributions**, quantile TD, VMP/Bethe free energy, and ERP-linked prediction error. Manuscript: §7c (`07c_daif_results.md`).

## Modules

| Module | Role |
|--------|------|
| `types.py` | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |
| `core.py` | Push-forward Bellman, C51-style projection |
| `quantile.py` | QR-DQN / IQN, Wasserstein on returns |
| `inference.py` | Distributional case assignment, VMP, Bethe FE, EIG |
| `prediction.py` | DPE, N400/P600 proxies, synthetic ERP waveforms |
| `policy.py` | `G_policy`, Boltzmann policy, epistemic value |
| `metrics.py` | Convergence diagnostics, distributional KL, quantile coverage |

## Quick import

```python
from src.daif import (
    DistributionalReturn,
    DAIFResult,
    push_forward_return,
    distributional_case_assignment,
    G_policy,
)
# Or from root package:
from src import DistributionalReturn, push_forward_return
```

Full API: [`docs/api_reference.md`](../../docs/api_reference.md) (section `src.daif`). Theory ↔ code: [`docs/theory_implementation_map.md`](../../docs/theory_implementation_map.md). Details: [`AGENTS.md`](AGENTS.md); agent skill: [`SKILL.md`](SKILL.md).
