# Source packages

Shared numerical input validation is in `numerics.py`; manuscript metrics, substitution, and cross-artifact validation are root helper modules. Package scope follows the table below. Each math package's boundary paragraph lives canonically in its `docs/modules/<pkg>.md` guide; the Contract column links there.

Release helpers separate quality evidence (`release_validation.py`), visual-inspection freshness (`publication_review.py`), citation/deposit metadata (`release_metadata.py`), and portable archive integrity (`release_bundle.py`). The aggregate read-only status reporter (`evidence_status.py`, installed as the `ccd-evidence-status` console command) composes these validators into one machine-readable report with per-stage `missing`/`stale`/`invalid`/`validated` states. These helpers prepare and validate local artifacts; remote publication remains an explicit orchestration action.

| Package | Contract |
| :--- | :--- |
| [case_systems](case_systems/README.md) | [Boundary statement](../docs/modules/case_systems.md) (canonical). |
| [diagrams](diagrams/README.md) | [Boundary statement](../docs/modules/diagrams.md) (canonical). |
| [enriched_cat](enriched_cat/README.md) | [Boundary statement](../docs/modules/enriched_cat.md) (canonical). |
| [topos_theory](topos_theory/README.md) | [Boundary statement](../docs/modules/topos_theory.md) (canonical). |
| [cognitive](cognitive/README.md) | [Boundary statement](../docs/modules/cognitive.md) (canonical). |
| [daif](daif/README.md) | [Boundary statement](../docs/modules/daif.md) (canonical). |
| [quantum](quantum/README.md) | [Boundary statement](../docs/modules/quantum.md) (canonical). |
| [security](security/README.md) | [Boundary statement](../docs/modules/security.md) (canonical). |
| [visualization](visualization/README.md) | [Boundary statement](../docs/modules/visualization.md) (canonical). |
| [experiments](experiments/README.md) | Seeded synthetic validation, exact-target comparisons, replicate uncertainty, paired sensitivity arms, and implementation/configuration provenance. Simulation intervals are not empirical linguistic evidence. |
| [integrations](integrations/README.md) | Optional MCP stdio access to bounded source operations and contained read-only artifacts, with explicit schemas and claim boundaries. |

See [source guidance](AGENTS.md) and [method contracts](../docs/method_contracts.md).
