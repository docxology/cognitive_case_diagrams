# quantum: implementation reference

Finite POVMs and density matrices with explicit Hermitian/PSD/normalization checks. The canonical figure uses orthogonal projectors and a diagonal mixture, so it shows classical outcome probabilities, not interference. No quantum hardware, sheaf model, or TQNN is implemented.

| Source module | Defined entry points |
| :--- | :--- |
| [figure_data.py](../../src/quantum/figure_data.py) | `make_quantum_povm_example`, `make_security_violations_example`, `make_monoidal_functor_example` |
| [quantum_case.py](../../src/quantum/quantum_case.py) | `CasePOVM`, `case_probability`, `crisp_case_povm`, `graded_case_povm`, `fluid_s_povm`, `semantic_state` |

See the [package guide](../../src/quantum/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
