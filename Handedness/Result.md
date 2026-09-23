# The result

## Statement

**Theorem.** Let H(k) = Σ_{m=−R}^{R} e^{imk} C_m be the transport map of a family of N channels, where C_m is the complex N × N matrix for a hop across m loci. Let S be a reflection acting on the channels, a matrix with S² = 1. If the transport is symmetric under reflection, S H(k) S⁻¹ = H(−k), then the winding number of det H(k) about any point off its path is zero. This holds for every N, every hop range R, every reflection S and every choice of hops.

**Nearest-neighbour case.** For H(k) = e^{ik}A + e^{−ik}B, with A the forward hop, B the backward hop and S reversing the order of the channels, the symmetry condition is B = SAS⁻¹, and the winding is zero for every N and every A.

**Consequence for ED.** A transport with net handedness, meaning a nonzero winding, requires S H(k) S⁻¹ ≠ H(−k). ED's rules contain no reflection, so they cannot supply that asymmetry. **If ED's transport carries a handedness, it comes from the state the substrate is in, a spontaneously broken symmetry, and not from its rules.**

The assumptions behind each step are in [Assumptions.md](Assumptions.md). The full account is in [Paper.md](PAPER_Reflection-Symmetric%20Transport%20Carries%20No%20Handedness.md).

## Proof

**1. Symmetry fixes the backward hops.**

$$S\,H(k)\,S^{-1} = \sum_m e^{imk}\,SC_mS^{-1}, \qquad H(-k) = \sum_m e^{imk}\,C_{-m}.$$

These are equal for all k exactly when the coefficients match: C_{−m} = S C_m S⁻¹ for every m. Applying this twice is consistent because S² = 1. So each backward hop is the mirror image of the corresponding forward hop. In the nearest-neighbour case, B = SAS⁻¹.

**2. The determinant is even.** Write f(k) = det H(k). Then

$$f(-k) = \det H(-k) = \det\!\left(S\,H(k)\,S^{-1}\right) = \det H(k) = f(k).$$

**3. The winding is zero.** As k runs over [−π, π], f traces a closed curve. Its winding number about a point z₀ not on the curve is

$$W = \frac{1}{2\pi i}\int_{-\pi}^{\pi} \frac{f'(k)}{f(k) - z_0}\,dk.$$

Because f is even, f′ is odd, so the integrand is odd and the integral over the symmetric interval vanishes. W = 0. ∎

## Why the question is not empty

Handed transport does exist in this family, so the theorem rules something out:

- **Break the symmetry and the winding appears.** With purely one-way hopping (only C_R nonzero), det H(k) = e^{iRNk} det C_R, whose winding about 0 is RN. For nearest-neighbour hopping with B = 0 it is N.
- **Without the arrow, no transport could be handed.** If transport were Hermitian (C_{−m} = C_m†), det H(k) would be real and its winding about any point off the real axis would be zero whatever the symmetry. It is the arrow (P11) that makes forward and backward hops independent, and so makes handedness possible at all.

So the theorem separates two cases: ED's arrow makes handed transport possible, and ED's reflection-symmetric rules keep it out of the laws.

## Check

    python check_result.py

The script checks the theorem for N = 1 to 6. Part 1 uses nearest-neighbour hops with S reversing the channel order. Part 2 uses random reflections S (S² = 1, generally not unitary) and hops reaching R = 1, 2 and 3 loci. In every case it confirms that the determinant is even and that the winding is zero. It also runs the two controls above, showing winding RN for one-way hopping and zero for Hermitian transport.

## How far it reaches

- **This model only.** The result is about the transport model in M1–M3. That ED's substrate transport has this form is assumed, not derived. It does not depend on how far hops reach or on which matrix represents the reflection.
- **One dimension, transport only.** It does not construct relativistic fermions (a Dirac sector). It does not say whether nature's handedness arose this way, or which force is handed.
- **Modest in mathematical terms.** It is the principle that a reflection-symmetric system carries no reflection-odd invariant, made explicit for this family. A closely related statement, for a mirror symmetry combined with a transpose, is published (K. Kawabata, M. Sato and K. Shiozaki, *Physical Review B* 102, 205118, 2020). The exact form here may well be known too.
