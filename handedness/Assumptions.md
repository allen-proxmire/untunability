# Assumptions

Everything [the result](Result.md) assumes, and nothing else.

## From ED's primitives

ED's substrate has thirteen primitives. The result uses five of them.

||primitive|what it supplies|
|-|-|-|
|P03|Loci are indexed, and space is homogeneous.|Transport is the same at every locus, so it can be written in terms of a wavenumber k.|
|P05|Polarity is transported between neighboring loci.|Transport is made of hops between loci: forward, backward, or within a locus. Transport built from several steps reaches further.|
|P07|Channels are distinct, basic objects.|A family of N channels, so each hop is an N × N matrix.|
|P09|Polarity is a U(1) phase.|Hop amplitudes are complex numbers.|
|P11|Commitment is irreversible.|Forward and backward hops need not mirror each other, so transport can be non-Hermitian. Without this, det H(k) would be real and no transport could be handed.|

**One definition.** Amplitudes add and scale: they form a complex vector space. This lets the hops act as matrices.

**One property of the primitive list.** No primitive is a reflection, so ED's rules are symmetric under reflection.

## Modelling assumptions

These are not ED primitives. They are the choices that turn the primitives into something that can be calculated.

||assumption|
|-|-|
|M1|Transport for a family of N channels along a chain is H(k) = Σ_{m=−R}^{R} e^{imk} C_m, with C_m the hop across m loci. The simplest case is nearest-neighbour hopping, H(k) = e^{ik}A + e^{−ik}B, with A the forward hop and B the backward hop.|
|M2|Reflection sends k → −k and acts on the channels by some matrix S with S² = 1. Reversing the order of the channels (channel i ↦ channel N+1−i) is the natural example, but the result holds for every such S. A reflection-symmetric transport satisfies S H(k) S⁻¹ = H(−k).|
|M3|Net handedness is measured by the winding number of det H(k) as k runs once around its period. This is the standard invariant for non-Hermitian hopping models.|

## Mathematics used

Determinants, and the winding number of a closed curve in the complex plane.
