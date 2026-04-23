# cognitive/ — §7: Active Inference as a Process Theory

Scalar-belief active inference: variational free energy, belief updating, and prediction-error proxies. **Distributional** inference (return distributions, quantile TD, DAIF) lives in [`../daif/`](../daif/).

## Modules

| Module | Description |
|--------|-------------|
| `belief.py` | `CaseDiagramBelief` — probability distribution over case roles |
| `free_energy.py` | `kl_divergence`, `variational_free_energy` |
| `belief_updating.py` | `update_belief`, `sequential_belief_update` |
| `prediction_error.py` | `prediction_error`, `p600_amplitude_ratio` |
| `action_selection.py` | `expected_free_energy` |
| `reanalysis.py` | `magnitude_reanalysis_cost`, `n400_amplitude_proxy` |

## Quick Import

```python
# From focused modules (canonical)
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.free_energy import kl_divergence, variational_free_energy
from src.cognitive.belief_updating import update_belief, sequential_belief_update
from src.cognitive.prediction_error import prediction_error, p600_amplitude_ratio
from src.cognitive.action_selection import expected_free_energy
from src.cognitive.reanalysis import magnitude_reanalysis_cost, n400_amplitude_proxy

# Or from the package (flat namespace)
from src.cognitive import CaseDiagramBelief, update_belief, kl_divergence
```

See [`AGENTS.md`](AGENTS.md) for full derivations and electrophysiological predictions; [`SKILL.md`](SKILL.md) for agent routing.
