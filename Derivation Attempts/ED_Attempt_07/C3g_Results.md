# C3g results: sync as a condition, with the units fixed

*ED_Attempt_07, note 29. 2026-09-19 (RD51). Ledger: C99, C100. Run `model/c3g_run.py`: calibration gate, 16 growth runs, 4.4 h on 3 workers. Same model, settings, sizes, seeds, tick count, readings, classification and exit rule as C3f; the only change is the units fix in the sync condition (C98), plus one added expected result (E6, that the condition fires).*

## As pre-registered (C99)

**The gate passed,** identically to C3f.

| setting | sync refusals per tick | slice diameter (flat 15 / 18) | links per event | **spacetime d_H** (flat 3+1 ≈ 4) | largest link strain (flat 6.5 / 6.7) |
|---|---|---|---|---|---|
| **A** commitment + curvature | 0 | 10.5 / 12.5 | 5.15 | 5.98 / 6.44 | 15.6 / 13.8 |
| **B** the same + sync condition | **752–1,489** | **13.5 / 15.0** | 5.12 | **5.89 / 6.33** | 19.6 / 17.6 |
| **C** sync alone | 13–28 | 8.5 / 10.5 | 7.13 | 5.51 / 5.75 | 11.1 / 10.5 |
| **D** no pressure | 0 | 9.0 / 10.5 | 7.15 | 5.52 / 5.80 | 8.9 / 10.7 |

| | result | |
|---|---|---|
| **E0** gate | Passed | **As expected** |
| **E1** structure, budgets, ceiling, flips, size | All exact; counts 1.00 (A), 0.94 (D) | **As expected** |
| **E2** B and C hold their counts | 1.01 and 0.94 | **As expected** |
| **E3** B's spacetime in [3.3, 4.7] | 5.89 and 6.33 | **Not as expected** |
| **E4** D's spacetime not in range | It isn't | **As expected** |
| **E5** every setting measurable | Every slice still too small to measure | **Not as expected** |
| **E6** the condition fires | Up to 1,489 refusals per tick, and B differs from A throughout | **As expected** |

**Exit, by the rule as written: "Too small to measure at these sizes."**

## What the condition actually did (C100)

**It works, in the direction it was meant to, and not nearly far enough.**

- **Slices got wider.** With the condition on, diameters went from 10.5 to **13.5** and from 12.5 to **15.0**, against the flat slice's 15 and 18. That's the first time in six 3D runs that anything moved **toward** flat geometry.
- **The spacetime moved too, slightly:** 6.44 → **6.33** at the larger size, where flat 3+1 should read about 4.
- **The strain moved the other way, as it must:** the largest link strain rose from 13.8 to **17.6**. Refusing to *create* strained links leaves the strain on older links instead of relieving it.
- **It didn't strangle growth:** splits were abandoned 0.1–0.3 times per tick, and event counts held at 1.01.
- **Sync alone does almost nothing** (C against D: diameters 8.5 against 9.0, spacetime 5.51 against 5.52). It only matters alongside commitment and curvature, which is what makes the slice sparse enough for strain to build.

## Where that leaves road C

**The wall stands, but its shape is clearer.**
- **Six 3D runs, and the counts, structure, budgets, ceiling and rewiring are all solved.**
- **No setting is near flat:** spacetime dimensions of 5.5–6.4 against 4, with slices too narrow for the slice readings.
- **But the one reading ED actually argued for — sync as a condition on keeping a common "now" — is the only thing that has pushed the pattern toward flatness.** It's a small push from a threshold set at the 99th percentile of created-link strain.

**The obvious question it raises:** does a tighter threshold push further? That's a knob, and the answer decides whether this is a mechanism or a rounding error.

## Options (Allen decides)

| | option | cost | what it settles |
|---|---|---|---|
| **(a)** | **A short threshold scan,** labelled as a diagnostic: setting B at the larger size, one seed, with the threshold at 6, 3 and 1.5 instead of 10 | About 1.5 h | Whether the push toward flat geometry grows as the condition bites harder, or saturates |
| **(b)** | **Record the wall and conclude road C**, then the attempt 7 write-up and stock-take | — | Closes the road on six runs |
| **(c)** | **The compiled port,** then slices ten times larger so the slice readings resolve | A day or two of work | Whether any of this survives at a size where geometry can be measured properly |

**Proposal: (a), then (b) or (c) depending on what the scan shows.** If tightening the threshold keeps widening the slice, the port becomes worth it; if it saturates well short of flat, road C closes with an honest wall.

## The threshold scan (C101, diagnostic, not pre-registered)

*Setting B at 13,824 events, one seed, T = 150, with the sync threshold at 6, 3 and 1.5 instead of about 10. D44.*

| threshold | events vs start | slice diameter (flat 18) | slice d_H | slice d_s | **spacetime d_H** (flat ≈ 4) | sync refusals per tick | forced keeps per tick | splits abandoned per tick |
|---|---|---|---|---|---|---|---|---|
| **≈10** (C3g) | 1.01 | 15.0 | undefined | undefined | 6.33 | 1,403 | 76 | 0.3 |
| **6** | 1.06 | **25.0** | undefined | undefined | 6.35 | 3,993 | 376 | 0.2 |
| **3** | 1.17 | 23.0 | **4.80** | **1.35** | **5.57** | 9,902 | 1,156 | 0.2 |
| **1.5** | 1.30 | 16.0 | 4.39 | 1.59 | **5.39** | 54,702 | 5,735 | **719** |

**The push doesn't saturate. It also doesn't point at flat space.**

- **Diameters overshoot.** At thresholds 6 and 3 the slices are **wider than flat** (25 and 23 against 18). They aren't becoming flat; they're stretching out.
- **The slice readings, once they're defined, say branched.** At threshold 3 the slice reads mass dimension 4.80 with spectral dimension **1.35**, and at 1.5 it reads 4.39 with 1.59. A spectral dimension below 2 is the branched flag: stringy, tree-like, with thin necks.
- **The spacetime does drift toward 4** (6.33 → 6.35 → 5.57 → 5.39), but that drift comes with the slice becoming stringy, not flat.
- **The tightest setting strangles growth:** 719 splits abandoned per tick, 5,735 forced keeps, and the event count drifting 30% above the start.

**What it means:** tightening the sync condition trades one bad shape for another. Loose, the pattern is crumpled; tight, it is branched; **at these sizes there is no flat middle between them.** That's the same shape as the known result for random 3D geometry, where the crumpled and branched phases meet at a first-order transition with no smooth phase between — except here it happens under ED's own meanings rather than under a tuned coupling.
