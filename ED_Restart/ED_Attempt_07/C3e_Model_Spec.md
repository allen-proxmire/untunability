# C3e: growing a 3D slice with paired flips (specification, on paper)

*ED_Attempt_07, note 23. 2026-09-18 (RD40). Ledger: C81. **A specification only: no code, nothing run.** Implementation questions C3e-Q1–C3e-Q4 and the expected results are for Allen to confirm; running is a separate yes.*

## Why (from C3d and its diagnostic)

- **C3d fixed two things and broke on a third:** the link balance held and the readings worked, but every slice shrank to 0.56–0.83 of its starting event count.
- **The diagnostic** (not pre-registered, D34) **ruled the ceiling out.** Raising it to 60 or removing it entirely didn't restore the event count; the blocking simply moved from the ceiling to the link budget.
- **The cause is competition for one conserved pool.** A split has to buy about 7 new links. A 2–3 flip buys one. With a full sweep of flips every tick, thousands of link purchases go to rewiring, the pool empties, splits are refused, merges keep running, and the slice shrinks while its remaining events crowd together.
- **ED already decided the rule that fixes this.** Attempt 6 decided that cut-and-rejoin happens **only in pairs** (A6 D5, D8). C3c's spec flagged that a single 2–3 flip changes the link count by one, read "in pairs" loosely, and let it through (C3-Q6). C3e reads it strictly.

## The change (C81)

**Everything from C3d** (note 21 and its D29 guards) **except the flips.**

| | C3d | **C3e** |
|---|---|---|
| **Flip move** | One 2–3 **or** one 3–2, each changing the link count by one | **A pair: one 2–3 and one 3–2 together**, applied to disjoint places, so the link count and the tetrahedron count are **unchanged** |
| **Attempts per tick** | One per event | **One pair per two events** (the same number of individual flips) |
| **Acceptance** | Proposal correction × e^(−ΔS) | The same, with the pair's combined cost change and the pair's proposal correction |
| **Refused if** | Either move invalid | Either move invalid, the two overlap, or the ceiling would break (the link budget can't block a pair, since it's link-neutral) |

**What that buys:** rewiring no longer competes with growth for the link pool. The pool is then used only by splits and merges, which trade links roughly evenly, so the event balance can do its job.

## The rest of the model

- **Sizes:** 8,000 and 13,824 events, as C3d.
- **Settings:** S0 (no pressure), S1 commitment, S2 curvature, S3 sync, S4 all three, at unit strengths.
- **T = 150 ticks**, two seeds. (Lower than C3d's 200: a paired flip does two moves, so ticks cost more. See the plan below.)
- **Link budget:** conserved, at the flat 6.699 links per event.
- **Ceiling:** **60**, with a **no-ceiling contrast** for S0 and S4 at the larger size, one seed each. The diagnostic showed 30 was too tight; 60 is a knob and the contrast shows whether it still matters.
- **Calibration gate first,** as in C3d.
- **Guards kept:** died, ran away, densified.
- **Readings and shape rules:** exactly as C3d (note 21), including the restored spectral dimension and the diameter.

## Expected results, written down before any code

| | expected | why |
|---|---|---|
| **E0** calibration gate | Flat reads flat 3D at both sizes; randomized doesn't | It passed in C3d with the same readings |
| **E1** structure, budgets, ceiling, size | Every structure check exact; both budgets exact; nobody over the ceiling; **event count within ±10% of the start**; **flips never change the link count** | The paired flip is link-neutral by construction, so the pool is left for growth |
| **E2** S0 | **Not flat 3D** at the larger size | Entropy without pressures |
| **E3** S4 | **Flat 3D at both sizes, settled** | The hypothesis, still low confidence |
| **E4** settling | Every setting settled at both sizes | T = 150 at pinned density |
| **E5** flips | Median accepted paired flips per tick above zero in every setting | A check that pairing hasn't made rewiring impossible |
| S1, S2, S3, and the no-ceiling contrast | Reported | Their own pulls; whether the ceiling still matters |

## Exit rule

**First:**
- **E0 fails:** stop before the growth runs; readings revision (recorded).
- **E1 fails on structure, a budget or the ceiling:** a code bug (recorded).
- **E1 fails only on the event count:** **"the two balances still fight: growth cannot be sustained at pinned density"** (not a bug), then take stock of road C.
- **E5 fails** (pairing kills rewiring): recorded, and the pairing rule goes back to Allen.
- **A deciding setting is unsettled:** "not settled in T ticks."

**Then:**

| outcome | record |
|---|---|
| **S4 flat 3D at both sizes, S0 not flat** | **"With the link balance, paired cut-and-rejoin and the ceiling, ED's meanings grow a flat 3D slice at the sizes run: consistent, not derived; the density, the ceiling and the three strengths are knobs."** Then a knob scan |
| **S0 flat 3D at both sizes** | "At pinned density, growth alone keeps a 3D slice flat." Take stock |
| **Density and size hold, but nothing reads flat** | "The balances hold the counts but not the shape: ⟨shapes⟩." Take stock |
| **Anything else** | Recorded as it reads |

## Cost plan

- **Per tick, projected:** about 1.5× C3d's, since each paired attempt does two moves: roughly 20 s at 8,000 and 36 s at 13,824.
- **Per run at T = 150:** about 50 and 90 minutes.
- **Total:** 20 growth runs plus 2 contrast runs plus 4 calibrations, about **7 hours on 3 workers.**
- **The timing trial confirms it first.** If it comes out over about 10 hours, T drops to 100 and that's recorded before any run.

## Implementation questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C3e-Q1** | **A paired flip is one 2–3 and one 3–2 at disjoint places, accepted or refused as one move?** | **Yes** | The strict reading of cut-and-rejoin in pairs (A6 D5, D8); link-neutral by construction |
| **C3e-Q2** | **One pair per two events per tick** (same number of individual flips as before)? | **Yes** | Keeps the rewiring rate comparable to C3c and C3d |
| **C3e-Q3** | **Ceiling 60, with a no-ceiling contrast** for S0 and S4 at the larger size? | **Yes** | The diagnostic showed 30 was too tight; the contrast shows whether 60 still shapes the result |
| **C3e-Q4** | **T = 150** to fit the cost plan? | **Yes** | Paired flips cost more per tick; the timing trial confirms |

## Next step

**If the defaults hold:** code it, run the move tests and the timing trial, then the calibration gate. **The growth runs need a separate yes.**
