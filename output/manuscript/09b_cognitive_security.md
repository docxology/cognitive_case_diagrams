# Role Policies and the Limits of Type-Based Security {#sec:cognitive-security}

A useful prompt-injection analogy is the attempted promotion of processed content into instructions with authority. The security module represents selected role transitions and reports violations relative to a supplied finite policy. It operates on already assigned labels; it does not read arbitrary text and infer trustworthy authority.

`detect_type_violation()` rejects roles outside its category before considering identity transitions. `CaseFrameValidator` checks membership and pairwise licensed connections, refreshing its adjacency view when the mutable category changes. The assignment checker accepts a connection in either direction for its pairwise compatibility test, so its result must not be mistaken for verification of a directed execution trace. Reported severities are hand-selected policy scores, not calibrated attack probabilities.

![A schematic authorized flow and an attempted content-to-authority promotion. The drawing communicates a policy distinction; it is not an observed attack trace or an executable firewall.](output/figures/security_type_violations.png){#fig:security-violations}

The compatibility class `MonoidalFunctor` checks pairwise role separation and existence of corresponding edges. Its method name `preserves_tensor()` is historical: the implementation has no tensor objects or tensorator coherence data. Monoidal functors need not be injective on objects, and two roles mapping to one object does not establish nonmonoidality. Indeed, grammatical alignment deliberately merges some argument distinctions. Whether a merge is prohibited is a policy decision.

![Truth table for the supplied role-separation policy. A failed cell records a label merge or missing edge under this rule, not mathematical failure of a monoidal law and not evidence that a linguistic alignment is malicious.](output/figures/monoidal_functor_security.png){#fig:monoidal-functor-security}

## Requirements for operational enforcement {#sec:cognitive-security-present-day}

A deployed system would need authenticated provenance, trustworthy assignment of roles, authorization at the tool boundary, and a check that the executed action matches the checked request. It would also need adversarial tests spanning indirect instructions, multi-turn context, confused delegation, and permitted role changes. The repository implements none of those system boundaries and reports no detection rate or security benchmark.

## Limits {#sec:cognitive-security-limitations}

Role labels alone cannot detect deception, validate factual claims, or prevent disclosure. A rejected label transition may be a legitimate request under a different policy; an accepted transition may carry harmful or false content. Magnitude, graph topology, and quantum terminology provide no automatic security guarantee. The finite checker remains useful as a transparent specification example when its inputs, rule set, and missing enforcement layer are stated.
