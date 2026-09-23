# Untunability: a conservation law fixes the three totals CDT tunes

*Allen Proxmire, 2026-09-23. Written for readers who know causal dynamical triangulations. The plain-language version is in [RESULTS.md](RESULTS.md); the full working is in [Derivation Attempts/ED_Attempt_11](Derivation%20Attempts/ED_Attempt_11/).*

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
| **N0/N4** | **0.044** | no value published at that point; **0.152–0.164 at the nearest measured boundary** — see below |

For N0/N4 the comparison was originally a bound rather than a measurement: with N32/N41 = 1.26 and at least 3 four-simplices per vertex in a slice, N0/N4 ≤ 1/(6 × 2.26) = 0.074, and ED's 0.044 lies inside it.

**That bound turned out to be the weaker statement.** A published *measurement* of N0/N4 exists at the A–C transition, and it is three times ED's value. **See "What the literature says", question 2 — this is where the 3+1 claim currently stands or falls.**

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

**Caveat as originally stated:** τ = 1/3 lies beyond the range plotted in AJL's figure, and was inferred from the monotone trend and the absence of a reported further phase at low k₀.

**That caveat has since been discharged** — the validated program reaches τ = 1/3 directly, at about k₀ = 3.2. See "What the literature says", question 3.

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
- Determine the placement in 3+1 — and the published measurement nearest to the relevant point runs against it, by a factor of about three in vertex density.
- Escape its modelling choices. Identifying the ontology's budgets with N0 and N3S, and its forward links with N1T, follows from stated decisions about what a tick is. Those decisions are recorded as decisions, in `Derivation Attempts/ED_Attempt_11/01_Ledger/Assumptions.md` (D3–D6).

**Not peer-reviewed, and not seen by anyone who works on CDT.**

---

## What the literature says

Three questions were put to the literature rather than left for a referee. The answers sharpen the claim and expose one tension.

### 1. Are the identities, read this way, standard?

**The identities are standard; the reading is not — and the difference matters more than it first appears.**

That the counts leave three free totals is textbook: in four dimensions six variables are related by three independent equations, so the coupling space is three-dimensional, and the Regge action is written

```
S_R = −(κ₀ + 6Δ)·N0 + κ₄·(N41 + N32) + Δ·N41
```

with κ₀, Δ, κ₄ conjugate to exactly the three totals at issue.

**But in CDT those totals are ensemble variables.** They are summed over, and the couplings fix only their expectation values. ED does something different in kind: it **fixes the counts themselves**. That is a *microcanonical* restriction, not a different choice of couplings.

**So the claim should be stated more carefully than "ED sits at a point of CDT's map":**

> ED's conservation laws pick out a definite point in the space of bulk counts. Whether that point corresponds to any CDT coupling is the question — it does so only if CDT's ensemble actually reaches those expectation values.

That reframing is the useful outcome of asking. It also makes the claim falsifiable in a way the original phrasing was not.

### 2. Is there a published N0/N4 to compare against?

**Yes, and it is the clearest tension in this document.**

The CDT review ([arXiv:1203.3591](https://arxiv.org/abs/1203.3591), §7.3.1 and Fig. 21) uses **N0/N4 as the order parameter conjugate to κ₀**, and reports it at the A–C transition (κ₀ = 4.711, Δ = 0.6, N4 = 120k):

> **N0/N4 jumps between roughly 0.152 and 0.164**, with phase C on the *smaller* side.

**ED's value is 0.044** — well below anything measured there. N0/N4 does fall as κ₀ falls, so moving from 4.711 to the canonical 2.2 moves CDT in ED's direction; but no published value at (2.2, 0.6) was found, and a factor of roughly three is a large gap to close.

**In CDT's own order parameters, ED's point is:**

| | ED |
|---|---|
| N0/N4 *(conjugate to κ₀)* | **0.044** |
| (N41 − 6·N0)/N4 *(conjugate to Δ; the review's second order parameter)* | **0.236** |

**Honest status: unresolved, and leaning against.** If CDT's phase C does not reach N0/N4 ≈ 0.044, then ED's point is not on CDT's map in 3+1, and the untunability claim survives only in 2+1. **Anyone with a CDT code can settle this in an afternoon**, and it should be settled before the claim is pressed further.

### 3. Is τ = 1/3 reachable in 3D CDT?

**Yes — and this one resolves in the claim's favour.**

The earlier caveat was that τ = 1/3 lies beyond the range plotted in AJL's Fig. 7. But the program used here, **run as plain CDT and validated against that same figure**, reaches it directly: τ = 0.473 at k₀ = 0, 0.403 at k₀ = 2, 0.295 at k₀ = 4. **τ = 1/3 falls between k₀ = 2 and 4, at roughly k₀ ≈ 3.2** — comfortably inside the extended phase, with the collapse transition not appearing until between k₀ = 5 and 6.

This is consistent with the published structure: after tuning the cosmological constant, 3D CDT's phase space is **one-dimensional in k₀**, extended at low k₀, with a single first-order transition to decoupled slices as k₀ rises. No further phase is reported below.

**So in 2+1 the claim stands as written**, and now on a measurement rather than an extrapolation.

---

## Where that leaves it

- **2+1: the claim holds.** ED's conservation fixes τ = 1/3 exactly, and that value is reachable, inside the extended phase, on a validated instrument.
- **3+1: the claim is unresolved, with a specific number deciding it.** ED needs N0/N4 ≈ 0.044 to be inside phase C. Published values near the A–C transition are three times larger. **This is the number to check.**
- **The framing is microcanonical**, and that is the honest way to state it: ED fixes counts; CDT fixes couplings and lets counts fluctuate. The claim is that ED's fixed point is one CDT would have had to tune its way to — *if* the ensemble reaches it.

**Sources:** [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267) (the 3+1 identities) · [hep-th/0011276](https://arxiv.org/abs/hep-th/0011276) (3D CDT phases) · [arXiv:1203.3591](https://arxiv.org/abs/1203.3591) (review; order parameters, Fig. 21) · [arXiv:1802.10434](https://arxiv.org/abs/1802.10434) (phase-diagram table) · [Scholarpedia, Causal Dynamical Triangulation](http://www.scholarpedia.org/article/Causal_Dynamical_Triangulation)
