# topos_theory: implementation reference

Textual theory presentations and profile comparisons. `ClassifyingTopos` stores presentation statistics only. `compare_theory_presentations()` is the canonical comparison; matching counts are neither necessary nor sufficient for Morita equivalence. `bridge_transfer()` never authorizes theorem transfer without a witness (none is implemented).

| Source module | Defined entry points |
| :--- | :--- |
| [topos.py](../../src/topos_theory/topos.py) | `TheoryType`, `Axiom`, `GeometricTheory`, `ClassifyingTopos`, `compare_theory_presentations`, `check_morita_equivalence`, `build_typological_theory`, `build_enriched_theory`, `bridge_transfer` |

See the [package guide](../../src/topos_theory/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
