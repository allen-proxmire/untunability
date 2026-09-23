# Untunability: a conservation law fixes the three totals CDT tunes

*Allen Proxmire, 2026-09-23. Written for readers who know causal dynamical triangulations. The plain-language version is in [RESULTS.md](RESULTS.md); the full working is in [ED_Restart/ED_Attempt_11](ED_Restart/ED_Attempt_11/).*

---

## The claim

In CDT the bulk counts are not all independent: the Dehn–Sommerville relations and the foliation leave a small number free, and those are what the couplings are tuned against. **Three conservation laws taken from the Event Density ontology fix all of them, exactly, with no free parameters introduced.**

The result is a *point*, not a region. It is arithmetic, not a simulation.

**What it is not:** it is not a prediction of a measurable quantity, and it is not a derivation of CDT. It says that *if* spacetime is described by a CDT-like foliated triangulation, then a particular conservation structure removes the freedom that is otherwise tuned.

---

## The identities

In 3+1 dimensions with periodic time (χ = 0), the ten counts obey seven constraints. Solving them (AJL, [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267) §3.2; solved symbolically, with N41 and N32 counting both orientations):

```
N1S = N0 + N41/2
N1T = 2·N0 + N32/2
N2S = N41
N2T = 2·N0 + 2·N32 + N41
N3S = N41/2
N3T(3,1) = N32 + 2·N41
N3T(2,2) = 3·N32/2
```

**Three totals remain free: N0, N41, N32.**

## What the conservation laws fix

| free total | fixed by | how |
|---|---|---|
| **N0** | a conserved offspring budget | the number of events per slice is carried forward, not chosen |
| **N41** | a conserved spatial link budget | the budget fixes N3S per slice, and N41 = 2·N3S |
| **N32** | a conserved forward-link count | **N1T = 2·N0 + N32/2** — conserving timelike links fixes N32 given N0 |

Each is a conserved quantity of the ontology, stated before this calculation and not adjusted to it. Together they leave nothing free: **one point of (k₀, Δ, k₄) with nothing tuned.**

**The flat reference point.** Taking the staircase product triangulation of a slab — one piece of each kind per slice simplex — gives N32 = N41 per slab and 7.70 forward links per event at the ontology's density (one vertical plus one diagonal per spatial link).

---

## Where that point sits

### 3+1: close on one order parameter, undetermined on the other

| | ED | CDT phase C |
|---|---|---|
| **N32/N41** | **1.00** | **1.26** at (k₀, Δ) = (2.2, 0.6) — [arXiv:1203.3591](https://arxiv.org/abs/1203.3591) Table 2, from N4 = 2.2625·N41 |
| **N0/N4** | **0.044** | no absolute value published at that point |

For N0/N4 the comparison is a bound rather than a measurement: with N32/N41 = 1.26 and at least 3 four-simplices per vertex in a slice, N0/N4 ≤ 1/(6 × 2.26) = 0.074. **ED's 0.044 lies inside it.** At the A–C transition (k₀ = 4.711, Δ = 0.6) the literature gives N0/N4 ≈ 0.154–0.162 ([arXiv:1802.10434](https://arxiv.org/abs/1802.10434) Table 1), but with N32/N41 small, so it is not a like-for-like comparison.

**Honest status in 3+1: close on N32/N41 (1.00 against 1.26), placement not determined.**

### 2+1: inside the extended phase, with nothing tuned

In 2+1 with toroidal slices, N31 (both orientations) = 2·N2S = 4·N0, so

```
τ = N22 / N3 = N22 / (N22 + 4·N0)
```

The same conservation laws — events conserved, spatial links automatic, forward links at the flat product value N22 = 2V per slab — give

> **τ = 2V / 6V = 1/3, exactly.**

(With N0/N3 = 1/6 and N1/N3 = 7/6, inside AJL's bounds of 1 and 5/4.)

3D CDT ([hep-th/0011276](https://arxiv.org/abs/hep-th/0011276)) has an extended phase for k₀ below ≈ 6.64 and a decoupled phase above; τ ≈ 0.25 at k₀ = 5.25, rising as k₀ falls, and dropping to ≈ 0 above the transition (Fig. 7).

**So in 2+1 these rules are microcanonical 3D CDT at a point on the extended side, away from the transition, with nothing tuned.**

**Caveat, stated plainly:** τ = 1/3 lies beyond the plotted range. It is inferred from the monotone trend and from the absence of a reported further phase at low k₀. That inference is the weakest link in this section.

---

## The instrument was checked first

The program used for the surrounding simulations was run as **plain CDT** before it was used for anything else, with expectations recorded in advance.

It reproduced the published behaviour: τ falling steadily — 0.473, 0.403, 0.295, 0.210 at k₀ = 0, 2, 4, 5 — then dropping sharply to 0.041 at k₀ = 6 and 0.021, 0.016, 0.012, 0.011 at 7, 8, 10, 12. **A steady fall then a sharp drop**, the known first-order behaviour (AJL Fig. 7 gives ≈ 0.25 at k₀ = 5.25 with the transition near 6.6 for spherical slices; ours are toroidal, so a shift is expected). Above the drop the universe collapses into a single slice, as published.

*(Attempt 11, C17. An earlier, shorter run failed to equilibrate and showed no drop; that was recorded and the run redone 100× longer rather than reported.)*

---

## What this does and does not establish

**Does:**
- Three quantities that are otherwise free, and are tuned in practice, are fixed by conservation laws — exactly, with no new parameters.
- The resulting point is not pathological: in 2+1 it sits inside the extended phase rather than the collapsed one.

**Does not:**
- Predict any new measurable quantity.
- Derive CDT, or show that spacetime is a triangulation.
- Determine the placement in 3+1 — only one of two order parameters is comparable, and the other has no published value at the relevant point.
- Escape its modelling choices. Identifying the ontology's budgets with N0 and N3S, and its forward links with N1T, follows from stated decisions about what a tick is. Those decisions are recorded as decisions, in `ED_Restart/ED_Attempt_11/01_Ledger/Assumptions.md` (D3–D6).

**Not peer-reviewed, and not seen by anyone who works on CDT.**

---

## What would settle it

Three questions, for someone in the field:

1. **Is the relation N1T = 2·N0 + N32/2 already used this way?** It is an identity, so the content is entirely in reading it as a conservation law that removes a tuned freedom. If that reading is standard, this is a restatement.
2. **Is there a published N0/N4 at or near (k₀, Δ) = (2.2, 0.6)?** That single number would settle the 3+1 placement.
3. **Is anything known about 3D CDT at τ ≈ 1/3?** It is beyond the published range, and the claim that the extended phase continues there is an inference, not a measurement.

An answer of "yes, that's standard" to the first question closes this cheaply, and that would be worth knowing.
