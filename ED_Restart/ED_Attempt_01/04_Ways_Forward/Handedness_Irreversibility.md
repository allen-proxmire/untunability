# Way forward 2: build on the handedness result

## The result, in one paragraph

Model transport along a chain of N lanes as H(k) = e^{ik}A + e^{−ik}B, with A the forward hop and B the backward hop. If the transport looks the same in a mirror, its winding number, the measure of a preferred direction, is zero for every N and every A. Two controls give it content. Without an arrow of time (reversible, Hermitian transport), no preferred direction is possible at all. With the mirror symmetry broken (one-way hops), the winding is N.

Public repository: https://github.com/allen-proxmire/event-density-streamlined

## What it gives you

- **A guardrail.** Mirror-symmetric rules can't carry a preferred direction.
- **A job for the arrow.** Irreversibility is what makes a preferred direction possible in the first place.
- **A place asymmetry must come from.** If there is a handedness, it is in the state (spontaneous symmetry breaking), not in the rules.

## Honest status

- **Correct.** The proof is three lines, and a numerical check passes for N = 1 to 6.
- **Modest.** It is the principle that a mirror-symmetric system carries no mirror-odd quantity, made explicit.
- **Possibly known.** A closely related statement is published: a mirror symmetry combined with a transpose removes the first-order skin effect, which happens exactly when the winding is nonzero (Kawabata, Sato and Shiozaki, *Physical Review B* 102, 205118, 2020, page 5; checked 2026-09-13). The exact form here was not found in a short search. Being a correct special case of known physics is fine. Presenting it as new would not be. Ledger: C11, C12.
- **A relative of Nielsen–Ninomiya,** not the same theorem. Nielsen–Ninomiya forbids net handedness for reversible lattice hopping even without mirror symmetry. This result is about irreversible hopping, where mirror symmetry is what forces the zero.

## Ways to build on it, in order

1. **Does the state actually break the symmetry?** The theorem says a preferred direction can only arise spontaneously. Test whether it does, in a uniform world with symmetric irreversible rules and chance: [Sim_Spontaneous_Direction/Spec.md](Sim_Spontaneous_Direction/Spec.md). **Status 2026-09-13:** the literature gate showed this is already answered for reinforced random walks, and that the answer depends on the reinforcement law, which ED doesn't fix. Suspended; see [Sim_Spontaneous_Direction/Literature_Gate.md](Sim_Spontaneous_Direction/Literature_Gate.md).

2. **Strengthen the statement. It is more general than written.**
   - *Any reflection matrix.* Step 2 of the proof only uses det(S H S⁻¹) = det H, which holds for any invertible S. So the result doesn't depend on reflection reversing the lanes in particular (M2): any S with S² = 1 will do. A quick numerical check on 2026-09-13 (random S with S² = 1, N = 2 and 3) gave winding 0 every time.
   - *Any hopping range.* The same step works for any smooth periodic H(k) with S H(k) S⁻¹ = H(−k), including hops of two or more sites. The nearest-neighbour form in M1 isn't needed.

   The same check covered hops reaching two sites, again with winding 0 every time.

   **Done 2026-09-13.** `tools/check_result.py` now tests random reflections (generally not unitary) with hop ranges 1 to 3 for N = 1 to 6, and all pass. The paper, the one-page result, the assumptions and the README state the general theorem.

3. **Go beyond one dimension.** On a 2D grid, a preferred direction has two components, and a mirror can flip one axis or both. Work out which invariant measures handedness there and what the mirror forces.

4. **Show it to a physicist who works on non-Hermitian systems.** Ask two questions: "Is this a known special case?" and "Is this the natural way for a reflection to act on channels?" It is small enough to answer in a short conversation.

## What not to do

- **Don't tie it to the weak force** or to the Standard Model's handedness without a calculation. That link was cut from the paper because it didn't hold.
- **Don't claim novelty** until someone who knows the literature has looked.
- **Don't grow it into a framework.** The next step is a second small result, not a larger story.
