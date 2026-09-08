# Topos-Theoretic Bridges: Requirements and Present Scope {#sec:topos-theory}

A geometric theory has a specified signature and axioms in geometric logic. Its classifying topos represents its models across suitable toposes [@caramello2018theories, sec. 2.1.2]. Morita equivalence concerns equivalence of classifying toposes, or equivalently the appropriate natural equivalence of model categories [@caramello2018theories, sec. 2.2.2]. Caramello's bridge programme uses alternative presentations of a common topos to transport invariant information [@caramello2016bridges].

This is stronger than similar vocabulary or matching counts [@caramello2018theories, sec. 2.1.7, sec. 6.1.1, sec. 7.1, sec. 10.1]. Adding a definable relation symbol can change signature size without changing the modeled structure. Conversely, two theories can have equal numbers and arities of symbols while imposing incompatible axioms. Counts of sorts, relations, or axioms are therefore neither necessary nor sufficient conditions for Morita equivalence.

## What the software represents

`GeometricTheory` stores names, relation arities, and textual axiom descriptions. `ClassifyingTopos` is a compatibility name for a presentation-profile container; it does not construct a Grothendieck topology, a category of sheaves, or a classifying universal model. The standard builder supplies ${topos_standard_sorts} sorts and ${topos_standard_relations} relations; the minimal builder supplies ${topos_minimal_sorts} sorts and ${topos_minimal_relations} relations. These are presentation statistics only.

`compare_theory_presentations()` compares those statistics. The deprecated `check_morita_equivalence()` retains the same profile-comparison result with a warning; its Boolean must not be interpreted as Morita equivalence. `bridge_transfer()` reports `morita_equivalent=None` and `transfer_possible=False` because no equivalence witness is supplied, even when profiles match.

![Schematic alignment mapping. A map between selected role labels illustrates a candidate correspondence; it does not construct a geometric morphism or a topos-theoretic bridge.](output/figures/functor_alignment.png){#fig:functor-alignment}

## What a bridge would require {#sec:morita-two-object}

For two candidate case theories, a substantive result would specify their geometric syntax, exhibit the relevant models or sites, construct comparison functors, and prove the required equivalence and coherence. A transferred claim must then be identified as invariant under that equivalence. No such witness is constructed here. A two-object picture or a matching profile cannot replace these steps.

Topos logic also needs careful separation from probability and quantum mechanics. Heyting algebras are distributive, although excluded middle need not hold. Intuitionistic logic is not made classical by “sheaf decoherence,” and no cohomological collapse or thermodynamic limit follows from the present code. Formalizing linguistic theories and testing which invariants survive is a research direction, not an accomplished unification.
