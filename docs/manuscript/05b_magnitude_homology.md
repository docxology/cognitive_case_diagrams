# Magnitude, Weightings, and Numerical Sensitivity {#sec:magnitude-homology}

For a finite similarity matrix $Z$, a weighting $w$ and coweighting $v$ satisfy $Zw=\mathbf1$ and $v^T Z=\mathbf1^T$. When both exist, their sums agree because $v^T Zw$ can be evaluated in either order. If $Z$ is invertible, the matrix magnitude is

$$
\lvert Z\rvert=\mathbf1^T Z^{-1}\mathbf1.
$$ {#eq:eq-5-3}

For a two-role example $Z=\left(\begin{smallmatrix}1&a\\a&1\end{smallmatrix}\right)$ with $0\leq a<1$, the weighting is $(1/(1+a),1/(1+a))$ and the magnitude is $2/(1+a)$. At $a=1$, the inverse does not exist, yet weightings and coweightings do exist and have sum one. Singularity therefore does not by itself make magnitude undefined.

The implementation uses an inverse for well-conditioned nonsingular matrices and a pseudoinverse when required. In the latter case it checks the left and right weighting residuals; a least-squares vector that fails these equations is not accepted as magnitude. Matrix mutation invalidates the cached inverse. A near-singular result remains sensitive to perturbations, and residual tolerances are numerical criteria rather than exact proofs.

For the raw illustrative matrix, the generated inverse-sum statistic is ${enriched_magnitude}, with two-norm condition number approximately ${enriched_z_condition}. Its object count minus that statistic is ${enriched_magnitude_deficit}. These describe this chosen matrix; the raw matrix's failed enrichment axioms preclude presenting the result as a categorical invariant of a validated linguistic model.

Magnitude homology is a distinct graded construction [@leinster2021magnitude]. The project does not construct its chain complex, differentials, or homology groups. A cup-minus-cap count is not a substitute. Likewise, a magnitude deficit is not automatically an entropy, a redundancy estimate, a reanalysis cost, or a security margin. Those interpretations require additional assumptions and evidence.

For positive hom-values, the transformation $d(i,j)=-\log Z_{ij}$ converts the multiplicative composition inequality to a triangle inequality. Zero hom-values correspond to infinite distance, and symmetry is still an additional condition. This connection explains a mathematical relationship between similarity and distance; it does not identify arbitrary attention matrices with metric spaces.
