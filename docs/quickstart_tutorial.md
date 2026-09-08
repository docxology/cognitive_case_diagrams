# Quickstart

From the project root, follow the install, gate, figure, injection, and validation commands in [README](../README.md). The project environment is separate from the sibling template renderer environment. If using external storage, an explicit `UV_CACHE_DIR` and `UV_PROJECT_ENVIRONMENT` in a writable temporary directory can isolate environment issues without changing code.

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
