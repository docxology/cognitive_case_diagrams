# Case Features and Voice Alternation {#sec:case-type-logic}

A case label attached to a drawing is different from a case-refined type enforced by a parser. Most constructors in this project use the same noun object `Ty("n")` and store NOM/ACC distinctions as metadata. They therefore do not reject every mismatched case feature.

A proposed refinement can introduce distinct objects $n_{\mathrm{NOM}}$ and $n_{\mathrm{ACC}}$ and type a transitive verb as $n_{\mathrm{NOM}}^r s n_{\mathrm{ACC}}^l$. Then the intended reductions involve those exact objects. This requires corresponding lexical assignments and explicit coercions where a grammar licenses them; it is not achieved by decorating an unrefined diagram after construction.

Passivization changes grammatical realization while preserving selected semantic participation. The project offers both a schematic passive template and an example using a Swap primitive. These illustrate different representational choices. A Swap is available only in an appropriate symmetric extension and is not itself a general linguistic derivation of passive voice. Nor does changing a participant's grammatical role necessarily change that participant's identity.

![Passive example with Bob in the subject slot and Alice in a supplied oblique slot. “By Alice” is an English oblique phrase; INS is a modeling label in some illustrations, not an English instrumental inflection. The generic noun type does not enforce these role labels.](output/figures/discopy_passive.png){#fig:discopy-passive}

Proof–type correspondences can clarify what a grammar derivation establishes. They do not make arbitrary case assignment computationally identical to Hindley–Milner inference, nor do they guarantee native-speaker judgments. This implementation performs selected typed compositions and role bookkeeping; it does not implement general case-feature inference, a full Lambek prover, or monadic root syntax.
