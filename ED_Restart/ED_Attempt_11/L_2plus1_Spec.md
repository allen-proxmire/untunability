# The 2+1 test: specification

*ED_Attempt_11, note 6. 2026-09-22 (RD6). Ledger: C9, D6. Written before any code. Written plainly; the technical box is at the end.*

## What you decided (D6)

**L-Q7, yes:** only the *total* number of events is conserved; **each slice's size is free to vary.** This revises A10 C-Q2.

## The picture (the ground rule)

**What's built:** a spacetime made of **2D sheets stacked in time**, looping round (16 sheets). Each sheet is a flat surface of triangles shaped like a doughnut, as in attempt 7. **Neighbouring sheets are joined by woven layers** of tetrahedra — ED's layer in one dimension down. Every allowed spacetime counts once. Three totals are held at ED's values:
- **events** (total only, L-Q7);
- **slice links** (automatic in 2D);
- **forward links**, at the flat value.

With those held, the layer's mix is fixed at ED's point: **τ = 1/3.**

**What the program does:** it reshapes the spacetime by small local changes — adding or removing an event on a link within a sheet, and flips — while keeping every piece a proper layer piece. Those are only its tools; every allowed spacetime counts once.

**What we read:**
1. **The spacetime's dimension**, by how fast balls grow. A spread-out 3D spacetime reads like the flat stack; a crammed one reads much higher.
2. **Each sheet's shape** — whether distance across it grows with its size like a flat surface does, or stays short like a small world.
3. **The sizes of the sheets over time.** In the rival theory's spread-out phase they bunch into a "blob" that grows and shrinks — a small universe. If the sheets are free to vary (L-Q7), this can show up.

**What each outcome would mean:**

| outcome | meaning for ED |
|---|---|
| **Spread-out spacetime, from both a flat start and a crowded start** | **In 2+1, ED's own rules give extended spacetime with nothing tuned — confirmed by a run, not just the literature.** The case for 3+1 becomes strong |
| **Crammed or small-world, from both starts** | The literature reading (note 5) was wrong somewhere; take stock |
| **The two starts end in different places** | Not settled, as in attempt 10; take stock of the program before anything else |

## Expected results, fixed now

| | expectation | confidence |
|---|---|---|
| **P0** | Every step leaves a valid layered spacetime: every piece a proper layer piece, the structure check clean, totals within their allowed band | High — a code check |
| **P1** | **The calibration works:** the flat stack reads flat; a deliberately crowded stack at the same totals reads clearly different (by at least 0.5 on the spacetime reading) | Moderate |
| **P2** | **Spread-out:** spacetime reading within 0.5 of the flat stack's; sheets' distances grow like a flat surface's (growth rate within 0.1 of flat's) | **About 65%**, from note 5 |
| **P3** | **The two starts agree** (spacetime readings within 0.3; sheet growth rates within 0.1) | About 50% — attempt 10's histories froze; here slices can change as much as a layer allows, so they should move |
| — | The sheet sizes over time: reported, no expectation fixed (a blob would be the rival theory's signature) | — |

## Cost

- **Building:** a spacetime program on attempt 8's 3D engine, with time labels and layer checks. **Several hours**, with an independent review of the code before it runs, and a check at each gate.
- **Running:** 1–3 hours at two sizes.

---

### Technical box

- **Spacetime:** a 3D simplicial complex with topology T² × S¹, foliated into T = 16 slices; every tetrahedron of type (3,1), (2,2) or (1,3) across consecutive slices. Built on the p3 State (tetrahedra, links, link condition) with a time label per vertex.
- **Start (flat):** each slice a triangular-lattice torus of side L; each prism (slice triangle × tick) cut into three tetrahedra by a global vertex order. Then N₂₂ = 2V per slab, N₃₁ + N₁₃ = 4V, so **τ = 1/3**.
- **Identities (torus slices):** N₁ˢ = 3N₀, N₃₁ = 4N₀, N₁ᵀ = 2N₀ + N₂₂, N₃ = 4N₀ + N₂₂. Holding N₀ and the forward links holds N₂₂ and N₃.
- **Moves (tools, not meanings):**
  - spatial edge split (a new vertex on a spatial link, same slice);
  - its inverse, a spatial-edge contraction under the link condition;
  - 2–3 and 3–2 flips, accepted only if every new tetrahedron is of type (3,1), (2,2) or (1,3).
- **Proposals:** a random vertex and neighbour slot for splits, contractions and 3–2 flips; a random tetrahedron and face for 2–3 flips. Hastings factors are computed from the counts before and after.
- **Weight:** uniform over valid spacetimes, times a soft hold exp(−ε[(N₀ − N₀*)² + (N₂₂ − N₂₂*)²]) with ε small; readings are taken only on configurations exactly at N₀* and N₂₂*.
- **Crowded start:** the flat start rewired by unconstrained flips at fixed N₀, then brought back to N₂₂*. Replaced if it fails P1.
- **Readings:**
  - **Spacetime:** A9's ball-growth reading on the vertex graph of the whole spacetime.
  - **Sheets:** mean distance across each slice against its size, pooled over slices, fitted as size^rate (flat 2D: 0.5).
  - **Profile:** spatial volume n(t), the triangles per slice.
- **Sizes:** L = 10 and 14 (N₀* = 1,600 and 3,136).
- **Settling:** readings every 50 sweeps, until the last third changes by ≤ 5%, or 2 hours per run.
- **Review:** an independent agent checks the move set, the Hastings factors and the layer checks before any run.
