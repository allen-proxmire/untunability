# ED bootstrap, part 1: the shape of ED's coins (on paper)

*ED_Attempt_03, note 3. 2026-09-15 (RD3). Ledger: C14–C18. Paper only: no code was run for this note. Expected results for a later computation are written at the end, before any computation.*

## The idea (note 2, D1)

List ED's own constraints. Look at the space of rules they allow. See whether that space has a **shape** with special points (edges, corners, a centre), and whether ED's rule sits at one. **Start with the coin:** the rule for how stuff at a spot splits among staying, moving left and moving right each step.

## ED's constraints, and which ones act on the coin (C16)

| constraint | what it says | source | status | acts on the coin? |
|---|---|---|---|---|
| **K1. Conserving, linear spreading** | Each step conserves total amount and is linear | A1 RD13 | ED's own | **Yes:** the coin is unitary |
| **K2. Coin, then move** | Internal stays; Right moves right; Left moves left; no extra phase on the move ("connection phase 0") | A1 RD13; v0 spec | ED's own | Fixes the setting the coin works in |
| **K3. Mirror symmetry** | The rule looks the same with left and right swapped | A1 test T2; C79 | ED's own | **Yes** |
| **K4. No signalling** | A draw fixes only the part that interacts | A1 RD22 | ED's own | No (draws) |
| **K5. Probabilities are amount squared** | Forced by Gleason plus no signalling | A1 RD13; A2 C11 | Forced | No (draws) |
| **K6. Draws fix only records; meetings hinge** | | A1 RD27, RD50 | ED's own | No (draws) |
| **K7. No free number** | The coin shouldn't need a chosen number | A1 V0-D1 | Least-structure criterion | Picks isolated points |
| **K8. Channels alike** | Relabelling channels changes nothing | A1 V0-D1 | Choice (Grover); A2 C61 notes the move treats Internal differently | **Yes** |
| **K9. Outcomes alike** | Every outcome equally likely every step | A2 D7 | Working default, adopted after results | **Yes** |

**So:**
- **ED's own constraints on the coin are K1–K3.** K7–K9 are ways of picking one coin, and each is a choice, not something ED forces.
- **K4–K6 act on draws.** No coin choice can break them.

## The coin space itself has no edges (C16)

- **Unitary 3×3 coins (K1)** form a smooth space with 9 real directions. Take away what the walk can't see (an overall phase, and channel phases that cancel out), and **6 remain**.
- **Mirror symmetry (K3)** cuts that to **3**.
- **All of ED's own constraints are equalities**, so they carve smooth surfaces inside a smooth space. **Smooth spaces have no corners.** The conformal bootstrap gets its corners from inequalities (probabilities can't be negative), and ED's coin constraints contain none.

**But a shape with edges appears as soon as you look at the odds** rather than the amplitudes.

## The shape: the coin's odds table (C14, C15, C17)

A coin's odds table (the probability of going from each channel to each other) always has rows and columns that add up to 1. All such tables form the **Birkhoff polytope**, a shape with real corners. **Not every table can come from a coin.** The ones that can (called "unistochastic") are exactly those passing a **chain-link test**: for any two rows, three lengths built from their entries must be able to form a triangle (Au-Yeung and Poon; C14). That's an inequality, and it gives the allowed set a boundary.

**With mirror symmetry, the odds table has only 2 free numbers:**
- **x:** the chance of moving between Internal and a lane;
- **y:** the chance a lane stays itself.

Everything else follows: Internal stays with 1 − 2x, and a lane switches to the other lane with 1 − x − y.

**The mirror-symmetric slice of the Birkhoff polytope is a four-sided shape** with these corners:

| corner (x, y) | what the coin does |
|---|---|
| (0, 1) | **Nothing:** the identity |
| (0, 0) | Swaps Left and Right, Internal untouched |
| (½, ½) | Internal always leaves; lanes half stay, half go to Internal |
| (½, 0) | Internal always leaves; lanes never stay |

**The chain-link test carves the allowed region out of it.** For this slice it reduces to two triangle conditions:
- **Left and Right rows:** lengths x, s, s with s = √(y(1 − x − y)), so the condition is x ≤ 2s;
- **Internal and Left rows:** lengths √((1 − 2x)x), √(xy) and √(x(1 − x − y)) must make a triangle.

## ED's two candidate coins sit at special points of this shape (C17)

**The "channels alike" line** (K8) runs through the shape as y = 1 − 2x, from the identity at (0, 1) toward the corner (½, 0).

| point on the line | x, y | what it is |
|---|---|---|
| **Identity** | 0, 1 | A corner of the polytope (no spreading) |
| **Fair coin** (outcomes alike) | **1/3, 1/3** | **The centre:** the uniform table, where every entry is 1/3. For three channels there's a whole ball of allowed tables around it (C15). Its link triangles are **equilateral** |
| **Grover coin** | **4/9, 1/9** | **The edge:** both link triangles go flat. Past x = 4/9 no coin exists on this line. Grover is the farthest this line can go |

**Where the fair coin's 120° comes from.** Orthogonal rows mean three complex terms must add to zero, so they close into a triangle. At the fair point the three lengths are equal, so the triangle is equilateral, and the terms must point **120° apart**. **The 120° phases of the fair coin aren't an extra ingredient; they're the only way equal odds can be unitary.** (Allen's 120° hint, D5 in attempt 2, has this plain origin. That's known mathematics, not a new finding.)

**So, in Allen's shape language:**
- **"Outcomes alike" is the centre** of the allowed shape.
- **"Channels alike, as spread-out as possible" is the edge** point of its line.
- **Attempt 2's coin question was centre versus edge.** Attempt 2 found the centre hosts a hand and the edge doesn't.

## A correction to attempt 2 (C18)

Attempt 2 said the plain Fourier coin is "**the one** fair coin that needs no phase chosen" (A2 C60). **On paper, that's too strong.**

- **A coin can be both fair and channels-alike.** Take C = I + βJ, with J the all-ones matrix and β = e^{±i150°}/√3. It's unitary, every odds entry is 1/3, it's unchanged by any relabelling of the channels, and it needs no chosen number.
- **Where it sits in the fair family.** One quantity doesn't change under any of the walk's hidden-phase freedoms: C_II² / (C_LL C_RR). It equals 1 for this coin and e^{−iφ}·ω for the fair family at phase φ. **That puts it at φ = 120°** (or its mirror-conjugate), which is still to be confirmed by computation.
- **What attempt 2 found there:** at φ = 120° the hand formed from 6 of 7 starts at gain 3 and 5 of 7 at gain 10 (A2 C58). That's inside the band, though not in its most robust core.

**So there are two parameter-free fair coins:** the plain one (φ = 0) and the channels-alike one (φ = 120°). Attempt 2's claim needs that qualification. Its other results stand.

## What this does and doesn't give

**Does:**
- **An exact, non-numerological picture of ED's coin choices:** centre and edge of a known shape.
- **Numbers fixed by shape:** 1/3; 1/9 and 4/9; 120°.
- **A correction** to one attempt 2 claim.

**Doesn't:**
- **Physics numbers.** Everything here is known mathematics about 3×3 unitary matrices.
- **A reason from ED's own constraints** (K1–K3) to put the coin at the centre, the edge, or anywhere else. Those constraints are equalities and don't single out a point. The picking is still done by a choice (K7–K9).

**Where edges could come from ED itself:** ED's inequality-type rules all live in the **draw and budget** sector, not the coin:
- the budget capped at 1 (A1 RD14, RD16);
- thinness thresholds (A1 RD19);
- the record threshold (A1 RD50).

**If ED has an "Ising kink", that's the sector where it would be.**

## Expected results for part 2 (written before any computation)

If part 2 is run, a script would check:

| | check | expected result |
|---|---|---|
| **E1** | 20,000 random mirror-symmetric unitary coins | Every odds table passes both chain-link conditions and lies in the four-sided slice. None falls outside. Samples come within 0.01 of the chain-link boundary |
| **E2** | Grover's odds (4/9, 1/9) | Both link conditions hold with equality, to 10⁻¹² |
| **E3** | The fair point (1/3, 1/3) | Its link triangles are equilateral, and the angles closing them are 120°, to 10⁻¹² |
| **E4** | C = I + βJ, β = e^{±i150°}/√3 | Unitary, fair and mirror-symmetric to 10⁻¹². Equivalent (overall phase, channel phases, ring momentum gauge) to the fair family at φ = 120° or its conjugate |
| **E5** | The channels-alike line | Coins exist for exactly x ≤ 4/9 |

## Part 2 results (C19)

*Run 1, `checks/coin_shape_check_run1.txt`. The expected results above were written before this run.*

| | result |
|---|---|
| **E1** | All 20,000 random mirror-symmetric coins land inside the chain-link region, and some come within a billionth of its edge. None outside |
| **E2** | Grover's odds are exactly (4/9, 1/9), with both triangles flat: **on the edge** |
| **E3** | The fair coin's triangles have equal sides of 1/3 and close with **120° turns** |
| **E4** | The fair, channels-alike coin is exactly the fair family's member at **φ = 120°**, and its mirror-conjugate is the partner at 240° |
| **E5** | Channels-alike coins reach exactly x = 4/9 and no further |

**All five as expected.** The correction to attempt 2 stands: there are **two** parameter-free fair coins, the plain one (φ = 0) and the channels-alike one (φ = 120°).

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(e)** | **Part 2: run the checks above** | Confirms the paper picture and the correction to A2 C60 |
| **(f)** | **Bootstrap the draw and budget sector:** list ED's inequality-type rules and ask whether they make a shape with special points | Where ED's own edges live, and so where an ED "kink" could be |
| **(g)** | **The coin decision as centre versus edge:** does ED's meaning prefer the centre (no outcome favoured) or the edge (channels alike, maximally spread)? | Allen's call; this note gives it a sharper form |

**Proposal: (e), then (f).** (e) is short and settles the correction; (f) is where a source of specificity could actually be.

**Update:** (e) is done (above). (f) is done too: [Draw_Budget_Bootstrap.md](Draw_Budget_Bootstrap.md) (note 4).

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C14 | Au-Yeung, Poon, "3 × 3 orthostochastic matrices and the convexity of generalized numerical ranges", *Linear Algebra Appl.* 27, 69–79 (1979); chain-link (triangle) conditions for 3 × 3 unistochasticity, as described in arXiv:0708.4051 and arXiv:math-ph/0603077 | Search listings; original not read |
| C15 | Bengtsson, Ericsson, Kuś, Tadej, Życzkowski, "Birkhoff's polytope and unistochastic matrices, N = 3 and N = 4", *Commun. Math. Phys.* 259, 307–324 (2005) | Abstract via search listing |
