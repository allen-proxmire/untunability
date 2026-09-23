# Stage B with narrow moves: the updated plan

*ED_Attempt_10, note 14. 2026-09-21 (RD14). Ledger: C24, D15. Specification; updates note 7 for narrow moves (D14). Written before any stage B code. Written plainly; technical detail in the box.*

## What changes from note 7

**1. The moves are narrow** (D14):
- a new event appears on a link;
- an event disappears by stepping back out from between two;
- flips.

**2. The program changes one slice at a time by a balanced bundle of changes**, so every slice keeps exactly its event and link counts (C-Q2, B-Q1). Four bundles:

| bundle | links | events |
|---|---|---|
| **a split and a merge of the same size** | +(1+k) −(1+k) = 0 | +1 −1 = 0 |
| **two flips**, one adding a link, one removing one | +1 −1 = 0 | 0 |
| **a split, a merge one size bigger, and a flip adding a link** | +(1+k) −(2+k) +1 = 0 | 0 |
| **the reverse of that** | 0 | 0 |

**Why the last two are needed:** the flat reference has no spot where a link-removing flip can happen. With paired flips only, it could never flip — frozen again, like the grid in note 13. The mixed bundles let flips start.

**A reading to flag:** attempt 6 decided flips come in pairs (cut-and-rejoin). In a mixed bundle, the tick as a whole stays link-balanced (B-Q1), but a single flip rides with a split and a merge. **I read B-Q1's exact link count as covering what the pairing was for.** Tell me if you disagree.

**3. The starts:**
- **Flat:** the flat reference at ED's density, as in note 6.
- **Crowded:** the same slice, rewired by random flips while holding its event and link counts. Same size, same counts, crammed shape. This replaces attempt 9's W1, whose counts differ, so the two starts are the same system.

## Gates, in order

| | check | pass |
|---|---|---|
| **G1** | **Rings, tiny sizes** (4 events, 3 ticks): the program's frequency for every distinct history against an exact count (each history weighted, as usual, by its symmetries) | Every history visited; frequencies within 3 standard errors |
| **G2** | **3D, every step:** every slice valid, both counts exact; **and every so often, replaying each tick's recorded changes on its slice reproduces the next slice exactly** | Exact, always |
| **G3** | **Readings:** the flat and crowded starts differ by at least 0.1 in the distance growth rate and 1.0 in the spacetime reading, at both sizes | Clearly separated; else sizes rise (recorded) |

## Runs, readings and pass rule

**Runs:** as note 7 — two sizes (12 and 16 per side, built into flat references of about 2,000 and 4,800 events), 32 ticks round the loop, both starts at each size, run until settled.

**The pass rule is note 7's, unchanged:**
- the growth rate of distance with size is within 0.05 of flat's;
- the spacetime reading is within 0.5 of flat's;
- **both starts agree.**

**Cost:** building is the bulk. I'll report at each gate. **Runs are hours each, depending on how fast the slices settle** — measured at the first gate that runs 3D.

**My expectation**, unchanged: close to a coin toss, leaning flat — now a little more, since narrow moves favour flat at every tick (C22).

## Your decision

**D15: update the plan and build it** (your "a"). **The flip-pairing reading above is flagged, not asked.** It doesn't block building; say if you want it otherwise.

---

### Technical box

- **State:** T periodic slices (Slice10P) plus per-tick change sets τ_t.
  - Each change is keyed canonically:
    - S(x, u, y) — x splits along link xu, child y;
    - M(v, a, u) — v merges into a, other pole u;
    - F23(ring, {d, e});
    - F32({d, e}, ring).
  - Its support is the set of events whose stars it changes: {x, u, y} ∪ Lk(xu), {v, a, u} ∪ Lk(va), and {d, e} ∪ ring.
  - Changes within a tick have disjoint supports (B-Q2), so they commute. Their validity depends only on the stars of their support, which are the same in both slices of the tick.
- **Update:** pick t, propose a bundle c valid in S_t, and set S_t′ = c(S_t).
  - **Left tick** (t−1): each part e of c cancels a change d in τ_{t−1} with d⁻¹ = e, or else joins τ_{t−1} if its support is disjoint from the others there.
  - **Right tick** (t): e cancels an identical change d ∈ τ_t, or else e⁻¹ joins τ_t if disjoint.
  - **Cap:** |τ| ≤ round(0.1 V) (C-Q3).
  - **A new child's label** reuses the merged event's label when that cancels, or the label of the matching split in τ_t; otherwise it's a label free in S_{t−1}, S_t and S_{t+1}. The label choice never enters the probabilities, so the chain on unlabelled histories is Markov and symmetric.
- **Proposals, label-invariant:**
  - split: a random event and a random neighbour slot (of 60) → 1/(60V);
  - merge: the same;
  - 2–3: a random tetrahedron and a random face → 1/(2T), where T = E − V is fixed per slice;
  - 3–2: a random event and a random neighbour slot → 2/(60V).
  - Bundle type 1/4 each; matching sizes by rejection.
- **Acceptance:** min(1, q_rev/q_fwd) — 1 for the first two bundles; 4T/(60V) for (split, merge k+1, 2–3) and its inverse (60V)/(4T) for (split k+1, merge k, 3–2). The target is uniform over valid histories, with the usual 1/|Aut| symmetry weighting.
- **G1:**
  - Rings of 4 events, T = 3, cap 2; the same machinery with ring operations (split inserts on a link; merge removes a 2-neighbour event; no flips).
  - Exact: enumerate all valid histories independently, tick by tick with closure; canonicalize by S_0's dihedral relabelings with new labels by (birth tick, position); weight by 1/|Aut|.
  - Compare with sampler frequencies over 2 × 10⁶ steps.
- **Crowded start:** single 2–3/3–2 flips at fixed V, Metropolis with uniform-measure corrections, the link count held within a window of +8 and ended exactly at E, within the ceiling, for 50 sweeps.
- **Readings:** per note 7, with spacetime snapshots built from τ (kids: persisting events plus split children; absorbed: merges).
