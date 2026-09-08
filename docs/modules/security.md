# security: implementation reference

A finite, supplied-label role-policy checker. Unknown roles are rejected before identity checks; mutable category adjacency is refreshed. Assignment checks use pairwise connectivity in either direction, not a directed authorization trace. No text classifier, authentication service, runtime reference monitor, or measured attack detector is provided.

| Source module | Defined entry points |
| :--- | :--- |
| [cognitive_security.py](../../src/security/cognitive_security.py) | `TypeViolation`, `CaseFrameValidator`, `detect_type_violation`, `injection_score`, `topological_robustness`, `semantic_integrity_check` |

See the [package guide](../../src/security/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
