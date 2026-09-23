# Reflection-Symmetric Transport Carries No Handedness: A Result About Event Density's Substrate

**Allen Proxmire**

**September 2026**

---

## Abstract

Event Density (ED) describes the world as a discrete substrate: channels carrying a complex phase at indexed loci, with an irreversible arrow of time. This paper asks whether a net handedness, meaning a preferred direction of transport, can be written into the rules of that substrate. It cannot. Model the transport of a family of N channels along a chain as H(k) = Σ_{m=−R}^{R} e^{imk} C_m, where C_m is the matrix for a hop across m loci, and measure net handedness by the winding number of det H(k). If the transport is symmetric under reflection, the winding number is zero. This holds for every number of channels N, every hop range R, every choice of hops, and every way a reflection can act on the channels. ED's rules contain no reflection, so if ED's transport carries a handedness, it comes from a spontaneously broken symmetry in the state of the substrate, not from its rules. Two controls show the question is not empty: one-way hopping has a nonzero winding, and without the arrow no transport in this family could be handed at all. A short script checks the theorem numerically for N = 1 to 6 and R = 1 to 3.

---

## 1. Introduction

A system along a line has a handedness when it distinguishes left from right: on balance, its transport prefers one direction over the other. The question here is where such a handedness could come from in ED: from the rules, or from the state the substrate happens to be in.

The answer depends on two facts about ED:

- **Its rules contain no reflection.** None of ED's thirteen primitives distinguishes a direction in space from its mirror image. (All thirteen are listed in Appendix A.)
- **It has an arrow.** Commitment is irreversible, so forward and backward transport need not mirror each other.

The first fact rules handedness out of the laws. The second makes handedness possible at all. The result below makes both statements precise for a definite model of transport, and proves the first in full generality within that model.

Mathematically the result is modest. It is the principle that a reflection-symmetric system carries no reflection-odd invariant, worked out explicitly for this family of transport maps. A closely related statement is published: a mirror symmetry combined with a transpose removes the first-order skin effect, which in one dimension occurs exactly when the winding is nonzero [4]. What makes it specific to ED is where the symmetry comes from (ED's primitive list) and why the question is worth asking (ED's arrow).

Section 2 states every assumption. Section 3 states and proves the theorem. Section 4 gives the controls, Section 5 the numerical check, Section 6 the consequence for ED, and Section 7 the limits.

---

## 2. Assumptions

The result assumes the items in this section and nothing else.

### 2.1 The ED primitives used

ED has thirteen primitives. The result uses five of them.

| | primitive | what it supplies to the result |
|---|---|---|
| **P03** | **Indexing and spatial homogeneity.** Channels and loci carry discrete indices, and the substrate's rules are the same at every locus. | Transport is the same at every locus, so it can be written in terms of a wavenumber k. |
| **P05** | **Polarity transport.** Polarity is carried along the edges between neighbouring loci. | Transport is made of hops between loci. A single step reaches a neighbouring locus; transport built from several steps reaches further. |
| **P07** | **Channels are basic objects.** Two channels at the same locus are distinct even when their contents coincide. | A family of N distinct channels, so each hop is an N × N matrix. |
| **P09** | **Polarity is a U(1) phase.** Each channel at each locus carries a phase e^{iπ}. | Hop amplitudes are complex numbers. |
| **P11** | **Commitment is irreversible.** No operation of the substrate undoes a commitment. | Forward and backward hops need not mirror each other, so transport need not be Hermitian. |

### 2.2 One property of the primitive list

**No primitive is a reflection.** None of the thirteen primitives (Appendix A) distinguishes a direction in space from its mirror image. So ED's rules are symmetric under reflection.

### 2.3 One definition

**Amplitudes add and scale.** They form a complex vector space, so a hop acts on the N channel amplitudes as an N × N complex matrix.

### 2.4 Modelling assumptions

These are not ED primitives. They are the choices that turn the primitives into something that can be calculated.

**M1. The transport map.** Transport for a family of N channels along a one-dimensional chain is

$$H(k) = \sum_{m=-R}^{R} e^{imk}\,C_m,$$

where C_m is the N × N complex matrix for a hop across m loci (forward for m > 0, backward for m < 0, within a locus for m = 0), R is the longest hop, and k ∈ [−π, π] is the wavenumber. The matrices C_m are independent. In particular C_{−m} need not equal C_m†; this is how the irreversibility of P11 enters the model.

The simplest case is nearest-neighbour hopping, R = 1 with C_0 = 0:

$$H(k) = e^{ik}A + e^{-ik}B,$$

with A = C_1 the forward hop and B = C_{−1} the backward hop.

**M2. How reflection acts.** Reflection reverses direction along the chain, sending k → −k. It also acts on the channels through some N × N matrix S. Reflecting twice changes nothing, so S² = 1. The natural example reverses the order of the channels (channel i goes to channel N + 1 − i), but the result does not depend on which S is used. A transport is reflection-symmetric when

$$S\,H(k)\,S^{-1} = H(-k) \quad \text{for all } k.$$

**M3. The measure of handedness.** Net handedness is measured by the winding number of det H(k) as k runs once over [−π, π]. For a closed curve f(k) in the complex plane and a point z₀ not on it, the winding number is

$$W = \frac{1}{2\pi i}\int_{-\pi}^{\pi} \frac{f'(k)}{f(k) - z_0}\,dk,$$

the number of times the curve goes around z₀. For non-Hermitian hopping models this is the standard invariant, known as the point-gap winding number [2, 3]. A nonzero value means transport along the chain prefers one direction; on a chain with ends, it shows up as states piling up at one end. Its simplest example is the Hatano–Nelson model [1], in which unequal forward and backward hopping gives a nonzero winding.

### 2.5 Mathematics used

Determinants, and the winding number of a closed curve in the complex plane.

---

## 3. The theorem

**Theorem.** Let H(k) = Σ_{m=−R}^{R} e^{imk} C_m with C_m complex N × N matrices, and let S be an N × N matrix with S² = 1. If S H(k) S⁻¹ = H(−k) for all k, then the winding number of det H(k) about any point off its path is zero. This holds for every N, every R, every such S, and every choice of the hops C_m.

**Nearest-neighbour case.** For H(k) = e^{ik}A + e^{−ik}B with S reversing the order of the channels, the symmetry condition is B = SAS⁻¹, and the winding number is zero for every N and every forward hop A.

### Proof

**Step 1: symmetry fixes the backward hops.** Conjugating by S and reversing k give

$$S\,H(k)\,S^{-1} = \sum_{m} e^{imk}\,S C_m S^{-1}, \qquad H(-k) = \sum_{m} e^{-imk}\,C_m = \sum_{m} e^{imk}\,C_{-m}.$$

The functions e^{imk} for different m are linearly independent, so these are equal for all k exactly when their coefficients match: C_{−m} = S C_m S⁻¹ for every m. Applying this twice gives C_m = S² C_m S⁻², which holds automatically because S² = 1. So each backward hop is the mirror image of the corresponding forward hop, and only the forward hops and the part of C_0 that commutes with S are free. In the nearest-neighbour case this is B = SAS⁻¹.

**Step 2: the determinant is even.** Write f(k) = det H(k). Since the determinant is unchanged by conjugation,

$$f(-k) = \det H(-k) = \det\!\left(S\,H(k)\,S^{-1}\right) = \det H(k) = f(k).$$

**Step 3: the winding is zero.** f is a polynomial in e^{ik} and e^{−ik}, so it is smooth and periodic, and f(k) traces a closed curve as k runs over [−π, π]. Take any z₀ not on the curve. Because f is even, f′ is odd, so the integrand f′(k)/(f(k) − z₀) is odd. The integral of an odd function over the symmetric interval [−π, π] is zero. So W = 0. ∎

Geometrically: as k runs from 0 to π the curve traces a path, and as k runs from −π to 0 it traces the same path backwards. A curve that retraces itself goes around no point.

Steps 2 and 3 use only the symmetry condition and the invertibility of S. The condition S² = 1 is what makes S a reflection, and it is what makes Step 1 consistent.

---

## 4. Why the question is not empty

The theorem would say nothing if no transport in this family could be handed. Two controls show that handed transport exists, and what makes it possible.

**Break the symmetry and the winding appears.** Take purely one-way hopping: only C_R is nonzero, with det C_R ≠ 0. Then

$$\det H(k) = \det(e^{iRk}C_R) = e^{iRNk}\det C_R,$$

a circle of radius |det C_R| traversed RN times. Its winding number about 0 is RN. For nearest-neighbour hopping (R = 1, B = 0) it is N. So transport in this family can carry any amount of handedness once the reflection symmetry is broken.

**Without the arrow, no transport could be handed.** Suppose instead that transport were Hermitian, the case in which forward and backward hops mirror each other in time: C_{−m} = C_m† for every m. Then H(k)† = H(k), so det H(k) is real for every k. A curve on the real line goes around no point off the real line, so the winding is zero whatever the symmetry. It is the arrow (P11), through the independence of C_m and C_{−m} in M1, that makes handed transport possible at all.

**The smallest case.** For N = 1 and nearest-neighbour hopping, S = ±1 and the symmetry condition is simply B = A. The transport is H(k) = 2A cos k, a segment traced back and forth, with winding zero. Taking |B| ≠ |A| instead gives the Hatano–Nelson model [1], whose curve is an ellipse around 0 with winding +1 or −1.

So the theorem separates two cases. ED's arrow makes handed transport possible, and ED's reflection-symmetric rules keep it out of the laws.

---

## 5. Numerical check

The script `check_result.py` (requires numpy) checks the theorem and both controls directly.

```
python check_result.py
```

It has two parts.

- **Part 1: the nearest-neighbour case.** R = 1, and S reverses the order of the channels.
- **Part 2: the general case.** For each hop range R = 1, 2, 3, it draws random reflections: matrices S = P D P⁻¹ with D diagonal with entries ±1 and P a random invertible complex matrix, so S² = 1 but S is generally not a permutation or even unitary.

For each N from 1 to 6, and each S, it:

1. **Tests the theorem.** It draws 20 random transports satisfying C_{−m} = S C_m S⁻¹, confirms S H(k) S⁻¹ = H(−k) at a random k, and computes det H(k) at 4000 values of k. It reports how far f(k) is from f(−k), relative to the size of f, and the winding number about a random point off the curve.
2. **Runs the one-way control.** With only C_R nonzero it computes the winding about 0, which should be RN.
3. **Runs the Hermitian control.** With C_{−m} = C_m† it computes the winding about a point just off the real axis, which should be 0.

Part 2 uses 5 random reflections for each R and N.

Output:

```
Part 1: nearest-neighbour hops (R = 1), S reverses the channel order
N  max|f(k)-f(-k)|/max|f|  symmetric windings | one-way winding | Hermitian windings
1  9.2e-16  [0] | 1 | [0]
2  1.6e-15  [0] | 2 | [0]
3  2.3e-15  [0] | 3 | [0]
4  3.2e-15  [0] | 4 | [0]
5  3.4e-15  [0] | 5 | [0]
6  3.9e-15  [0] | 6 | [0]

Part 2: any reflection S (S^2 = 1), hops of range R = 1; one-way winding should be 1*N
N  max|f(k)-f(-k)|/max|f|  symmetric windings | one-way winding | Hermitian windings
1  9.5e-16  [0] | 1 | [0]
2  2.5e-15  [0] | 2 | [0]
3  2.2e-14  [0] | 3 | [0]
4  4.8e-14  [0] | 4 | [0]
5  8.5e-14  [0] | 5 | [0]
6  7.1e-15  [0] | 6 | [0]

Part 2: any reflection S (S^2 = 1), hops of range R = 2; one-way winding should be 2*N
N  max|f(k)-f(-k)|/max|f|  symmetric windings | one-way winding | Hermitian windings
1  1.8e-15  [0] | 2 | [0]
2  4.3e-15  [0] | 4 | [0]
3  1.2e-13  [0] | 6 | [0]
4  3.3e-14  [0] | 8 | [0]
5  8.1e-14  [0] | 10 | [0]
6  2.6e-13  [0] | 12 | [0]

Part 2: any reflection S (S^2 = 1), hops of range R = 3; one-way winding should be 3*N
N  max|f(k)-f(-k)|/max|f|  symmetric windings | one-way winding | Hermitian windings
1  2.9e-15  [0] | 3 | [0]
2  4.2e-15  [0] | 6 | [0]
3  1.4e-14  [0] | 9 | [0]
4  5.2e-14  [0] | 12 | [0]
5  4.8e-14  [0] | 15 | [0]
6  5.5e-14  [0] | 18 | [0]

result holds for N = 1..6, any reflection S, hop range R = 1..3
```

The determinant is even to machine precision, and the symmetric winding is always 0. The one-way winding is RN and the Hermitian winding is 0, as Section 4 says. The script exits with an error if any of these fails.

---

## 6. Consequence for ED

By the theorem, a nonzero winding requires S H(k) S⁻¹ ≠ H(−k) for every reflection S: the transport must break the reflection symmetry. By Section 2.2, ED's rules contain no reflection, so they cannot supply that asymmetry. Therefore:

> **If ED's transport carries a net handedness, the handedness comes from the state the substrate is in, a spontaneously broken symmetry, and not from its rules.**

This is the familiar pattern of a ferromagnet. Its laws treat every direction alike, yet the magnet picks one. The theorem says that in ED, handedness in transport can only arise that way.

---

## 7. How far the result reaches

- **This model only.** The result concerns the transport model defined by M1–M3. That ED's substrate transport has this form and that the winding number is the right measure of handedness are assumptions, not derivations. The result does not depend on how far hops reach or on which matrix represents a reflection on the channels.
- **Transport only.** The result does not construct relativistic fermions, and it does not say whether nature's handedness arose this way or which force in nature is handed.
- **One dimension.** The chain is one-dimensional. How a reflection constrains handedness on a grid of two or more dimensions is not addressed here.
- **A negative result about the rules.** It shows that ED's rules cannot contain a handedness in this model. It does not show that ED's substrate does break the symmetry, or how it would.
- **Mathematically modest.** It is the principle that a reflection-symmetric system carries no reflection-odd invariant, made explicit for this family. A closely related statement, for a mirror symmetry combined with a transpose, is published [4]. The exact form here was not found in a short literature search, and it may well be known.

### Could it have come out wrong?

The proof is short, so the result's content lies in its inputs and its controls:

- **The controls could have failed.** If the arrow did not make handed transport possible (Section 4), the theorem would be empty. It does: one-way hopping has winding RN.
- **The symmetry claim could fail.** If any ED primitive turned out to be a reflection, Section 2.2 would fail, and the consequence in Section 6 would not follow. The full list is in Appendix A so that this can be checked.
- **The model could be wrong for ED.** If ED's transport is not of the form M1, or handedness is not measured by the winding number, the theorem still holds but no longer applies to ED.

---

## Appendix A. The thirteen ED primitives

Listed so that the property in Section 2.2 can be checked. Only P03, P05, P07, P09 and P11 are used by the result.

| | primitive |
|---|---|
| P01 | A discrete substrate exists, carrying the structure the other primitives describe. |
| P02 | Chains (persistent sequences of events) participate in channels at loci. Participation is a basic relation. |
| P03 | Channels and loci carry discrete indices, and the substrate's rules are the same at every locus. |
| P04 | Each channel at each locus carries a non-negative bandwidth, additive over disjoint channels. |
| P05 | Polarity is transported along the edges between neighbouring loci. |
| P06 | Space has three dimensions, plus one of time. |
| P07 | Channels are basic objects: two channels at the same locus are distinct even when their contents coincide. |
| P08 | The substrate has a smallest length scale. |
| P09 | Polarity is a U(1) phase. |
| P10 | The substrate supports several distinct types of rule. |
| P11 | Commitment is irreversible: at a commitment event a chain's participation collapses to a single channel, and no operation of the substrate undoes it. |
| P12 | Each chain carries a stability functional, Σ = Coh − Str − Grad (coherence minus strain minus gradient content). |
| P13 | The substrate's rules are the same at every time. |

None of these distinguishes a direction in space from its mirror image. P11 distinguishes the future from the past, which is a different asymmetry, and it is the one Section 4 shows is needed for handed transport to be possible.

---

## References

[1] N. Hatano and D. R. Nelson, "Localization transitions in non-Hermitian quantum mechanics," *Physical Review Letters* **77**, 570 (1996).

[2] Z. Gong, Y. Ashida, K. Kawabata, K. Takasan, S. Higashikawa and M. Ueda, "Topological phases of non-Hermitian systems," *Physical Review X* **8**, 031079 (2018).

[3] K. Kawabata, K. Shiozaki, M. Ueda and M. Sato, "Symmetry and topology in non-Hermitian physics," *Physical Review X* **9**, 041015 (2019).

[4] K. Kawabata, M. Sato and K. Shiozaki, "Higher-order non-Hermitian skin effect," *Physical Review B* **102**, 205118 (2020).
