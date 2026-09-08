# Introduction: Case, Composition, and the Limits of a Shared Diagram {#sec:introduction}

A sentence distinguishes participants and the relations between them. In “Alice chases Bob,” changing which participant occupies the subject position changes the interpretation. A representation that stores only an unordered pair of names loses this distinction. Case diagrams make selected relations visible and provide small objects on which to exercise composition, uncertainty, and interpretation.

Three meanings of *case* must remain separate. Morphological case concerns forms and marking; grammatical relations concern positions such as subject and object; semantic roles concern participation in an event. They can correlate without coinciding. NOM is not a universal synonym for agent, and ACC does not always denote a patient. Our examples use role labels as modeling choices, not as a claim that every language has the same inventory.

![A hand-specified 4-role graph used to introduce the notation. Nodes denote selected role labels and arrows denote named relations. This is a modeling example, not a graph extracted from a corpus.](output/figures/case_category_minimal.png){#fig:case-minimal}

Categorical compositional distributional semantics provides a mathematical account of how typed grammatical reductions can guide operations on word representations [@coecke2010mathematical]. Enriched-category constructions give a different route from suitable text-extension probabilities to mathematical structure [@bradley2021enriched]. Neither result implies that an arbitrary role graph, attention matrix, or probability table automatically satisfies the relevant categorical axioms.

## Contributions and evidence {#sec:whats-new}

This work contributes a connected exposition and reproducible examples, together with checks that expose where the examples stop. The categorical core distinguishes formal DisCoPy reductions from lightweight role bookkeeping. The numerical core tests normalization, support, composition inequalities, matrix sensitivity, quantile conventions, and measurement validity. The manuscript then uses those contracts to delimit proposed cognitive and security interpretations.

The repository contains no trained linguistic model or empirical dataset. Terms such as *prediction*, *precision*, and *return* in compatibility APIs therefore need the operational definitions given below. A synthetic calculation can verify arithmetic under stated assumptions; it cannot establish those assumptions as facts about language or the brain.

The reading order follows a dependency chain: alignment labels; graph and grammar constructions; semantic evaluation; enrichment and magnitude; the distinct requirements of topos theory; filtering and distributional utilities; synthetic statistical behavior of those utilities; measurement analogies; and proposed agent protocols. The research questions in [@sec:research-questions] identify which parts are implemented and which require new evidence. The synthetic-statistics section [@sec:synthetic-statistics] reports seeded computations of the utilities' own behavior and adds no empirical claim.
