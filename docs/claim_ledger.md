# Claim ledger

Statuses distinguish implementation evidence from theory and empirical interpretation. Tests establish specific examples and contracts, not universal validity. The working version and date are canonical in `docs/manuscript/config.yaml`; this ledger tracks claims, not release state.

| Claim | Status | Evidence / action |
| :--- | :--- | :--- |
| Selected pregroup reductions execute | verified | DisCoPy constructors and grammar tests; hand-assigned types |
| Finite Bayesian updates implement normalization | verified | Analytic posterior and impossible-evidence tests |
| Quantile updates use all target samples | verified | Two-point analytic QR counterexample and regression suite |
| C51 helper preserves clipped tail mass | verified | Method/function parity and endpoint examples |
| Supplied POVMs and states satisfy matrix contracts | verified | Hermitian, PSD, completeness, trace and malformed-input tests |
| Standard role matrix is a valid enrichment | unsupported for raw input | Raw composition failure retained; explicit closure added |
| Matrix magnitude measures linguistic information | partially_supported | Matrix statistic implemented; linguistic interpretation untested |
| Theory profiles decide Morita equivalence | unsupported | Counts can change under equivalent presentations; transfer now unavailable |
| All case frameworks have a common classifying topos | unsupported | No equivalence witness, sites, or sheaf construction |
| Local DAIF package reproduces full DAIF / Bellman control | unsupported | Exact dimensionless score contract replaces the former claim |
| VMP/Bethe names imply general factor-graph inference | unsupported | Single-factor update and shared-distribution score documented |
| Seeded synthetic studies characterize utility behavior | verified (synthetic only) | Prespecified runner arms in `src/experiments/`; identity and invalid-input controls; no empirical claim |
| Diagrams improve cognition or predict EEG amplitudes | ambiguous / proposed | Requires controlled human data and physiological calibration |
| Quantum figure exhibits interference | unsupported | Canonical diagonal mixture and projectors have a classical interpretation |
| Case labels secure real agent execution | unsupported | Supplied-label policy only; no authenticated execution boundary |
| Passing-test and coverage claims bind to source | verified via receipt | Source-bound quality receipt in `output/reports/`; stale fingerprints rejected |
| Every statement is certified by automated tests | unsupported | Removed; appendix states test limits |
| Publication status of remote deposit | not_asserted_here | DOI roles are fixed (version DOI for this revision, concept DOI for the series); live deposit state is reported in release notes after verification at the record URL |

Primary literature locators and verification boundaries are in [literature guide](literature_guide.md). Exact compatibility behavior is in [method contracts](method_contracts.md). The [comprehensive review](comprehensive_review.md) distinguishes historical observations from current release evidence.
