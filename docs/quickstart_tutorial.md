# Quickstart

Install the locked environment from the repository root:

```bash
uv sync --locked --extra mcp
uv run --locked python
```

The package supports Python 3.11 or later. The examples below use synthetic
values and can be pasted into the Python session. Use the
[reproduction guide](reproduction.md) to regenerate study outputs and
render the manuscript.

## A discrete belief update

```python
import numpy as np
from src.case_systems import CaseRole
from src.cognitive import CaseDiagramBelief, update_belief
prior = CaseDiagramBelief([CaseRole.NOM, CaseRole.ACC], np.array([.5, .5]))
posterior = update_belief(prior, np.array([.8, .2]))
np.testing.assert_allclose(posterior.probabilities, [.8, .2])
```

## Candidate enrichment

```python
from src.enriched_cat import standard_enriched_category
raw = standard_enriched_category()
assert raw.full_composition_check()['violations']
closed = raw.composition_closure()
assert not closed.full_composition_check()['violations']
```

The first assertion is a necessary negative control: the standard raw matrix is synthetic and not composition closed. Inspect both matrices before interpreting downstream magnitude. See [method contracts](method_contracts.md) for compatibility changes and scientific limits.
