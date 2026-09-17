# Taking stock of attempt 6

*ED_Attempt_06, note 8. 2026-09-15 (RD10). Ledger: C40 (road G's verdict), C41 (this stock-take). Nothing computed. Attempt 6 stays open; what comes next is Allen's call.*

## Road G, closed (C40)

**Allen accepted G-Q11 and G-Q12 and the exit rule** (D8). Recorded:

> **Road G:** ED's meanings give the moves, a favoured combination and a reason for three among smooth patterns; the step process they suggest (relations added where rates fail to match, each costing commitment) heads, on paper, to the floor just above two dimensions, not to a smooth three; no rule from ED's meanings found here produces smoothness.

**Road G is closed with that wall.**

## What attempt 6 set out to do

**Two roads carried from attempt 5** (note 1):
- **W:** do waves on a direction-free random pattern travel at one speed, with no short waves slower than light?
- **G:** can a growth rule grow a direction-free, three-dimensional pattern that stays that way?

**Attempt 5's walls to test:**
- the rest frame and the slow-short-wave leak (wall 1);
- no growth rule (wall 2).

## Scorecard

| road | what was found | verdict |
|---|---|---|
| **W part 1** (note 2) | Long waves on a random pattern go the same speed every way. For spreading rules, **every short wave is slower than light**, with or without ticks (firm, with an arithmetic check) | Long waves: good. Short waves: slow, for spreading rules; ED's walk not covered (C8) |
| **W part 2** (note 3) | **Husain and Louko's leak rests on a detector that never recoils.** In ED it becomes two questions: stuck states and unevenness. **Any walk with no stored directions, on a pattern with loops, has at least 1 − 2/(mean neighbours) of its states stuck** (firm, checked) | **Closed with a wall** (C15) |
| **G part 1** (note 4) | **Adding never stretches distances,** so adding alone can't expand. Random attachment and random rewiring lose finite dimension. **Growth needs a named favoured quantity** | Verdict C20 |
| **G part 2** (note 5) | Maximal sync favours small worlds. Maximal commitment favours a single chain. Lasting kinds presuppose space. **Combined: the fewest directions where rates can match is three** | Verdict C27 |
| **G part 3** (note 6) | **The floor in ED's own counts:** the ball-cut must outgrow the √count surplus of random rates, so d > 2, with no ratio. Three is the fewest whole-number dimension | **A reason for three, consistent, not derived** (C33) |
| **G part 4** (note 7) | ED's sync-plus-cost process **heads to just above two dimensions, not a smooth three.** Three is a choice among smooth patterns; nothing found produces smoothness | **Closed with a wall** (C40) |

## Tally

| | after attempt 5 | after attempt 6 |
|---|---|---|
| **Inputs supplied, nothing fitted** | 3 | **3** |
| **Relocated into the law** | 2 | 2 |
| **Proved theorems** | 1 (handedness) | 1. Plus two firm on-paper lemmas, known in form: the stuck-state bound and "adding never stretches" |
| **Open conflicts with observation** | 1 risk (the rest frame) | **1 risk** (the rest frame). **Plus one conflict inside ED:** no stored directions against freely moving waves |
| **New numbers derived** | 0 | **0** |
| **Reasons for three dimensions** | 1 (lasting kinds) | **2** (plus: rates can match only above two, and commitment favours the fewest) |
| **Checks run** | 6 | **+2:** dispersion bounds (5 of 7 as expected, 2 rounding misses with a labelled diagnostic); stuck states (S0, S1, S3 as expected, S2 a harness-label miss with a labelled diagnostic) |

## What's genuinely gained (C41)

1. **The leak question got sharper.** The slow-short-wave leak everyone cites depends on a detector that never recoils. In ED it turns on stuck states and on unevenness, which is smaller and better posed.
2. **A firm bound tied to one of ED's meanings.** "No stored directions" forces a large share of never-moving states wherever the pattern has loops. It's a real consequence, even though it's a wall.
3. **Expansion has a structural requirement.** Adding can't stretch, so ED's expansion needs relations to end or re-route in pairs, or sameness relations to thin.
4. **A second, ratio-free reason for three.** It comes from Allen's sync–commitment duality, read for the pattern. The reading (rates, not ticks in step) was fixed before the floor was worked out; ticks in step would have given 5.
5. **The missing piece is named.** It isn't "a growth rule" in general any more. It's **what makes the pattern smooth**: the thing every programme in attempt 4's survey put in or didn't reach.

## The walls now

| | wall | kind |
|---|---|---|
| **1** | **The rest frame.** Still there. Husain–Louko's leak is reframed, not removed | Risk |
| **2** | **Stuck states.** No stored directions plus loops leaves most wave states unable to move (C12, C15) | **New:** a conflict inside ED's meanings |
| **3** | **Smoothness.** No rule from ED's meanings produces a smooth pattern. ED's own process heads to just above two dimensions (C36, C40) | **Sharpened:** the standing gap since attempt 1 |
| **4** | **Numbers.** G, masses, couplings, and now the sync strength, all inherited | Gap |
| **5** | **The handle-free rule** is chosen, not read from ED's meanings | Fitting risk, labelled |

**Also open:**
- spin and charge;
- which knot is which particle;
- PF-Q2: is the rest frame the pattern's own?
- whether ED's rates actually match (a strength).

**A pattern worth noticing** (look-elsewhere, not a finding):
- **walls 2 and 3 are both about loops.** Stuck states live on loops; a three-dimensional pattern needs loops; smooth patterns are full of short loops (Trugenberger's weighting condenses them);
- **particles are loops too** (A5 C31).

## Honest notes on method

- **Scaling arguments by analogy** carried road G's last step (C36). They're labelled as such, and only a model would test them.
- **Two check misses came from my side:**
  - rounding in a formula (W part 1);
  - a mislabelled count in a script (W part 2).
  
  Both stand as misses, with labelled diagnostics. Lesson: use numerically stable forms, and label counts by the eigenvalue actually tested.
- **A borrowed assumption was stretched.** G-Q10 took whole-number dimension from A5's assumption Q, whose wording is "where a smooth description applies". The stretch was caught at C37. Lesson: quote an assumption's wording before borrowing it.
- **A withdrawn preprint was caught and not used** (G part 2).
- **The fitting guard worked once in the open:** rates versus ticks in step was decided before the floor was known.

## Options (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **A plain-language write-up of attempt 6,** keeping it open | Eight notes' worth of results in one readable place, as attempts 4 and 5 had |
| **(b)** | **Smoothness, on paper:** what makes local rules produce smooth patterns in the literature (time slicing in triangulations, short-loop condensation, others), and whether one of ED's meanings could play that role | Wall 3 is now a named piece; the cheapest next step on the root |
| **(c)** | **A model of the sync-plus-cost process,** rules and expected results first | Tests whether it really heads to just above two dimensions (C36) |
| **(d)** | **Loops, on paper:** stuck states, smoothness and particles, one question or three? | Walls 2 and 3 meet here; look-elsewhere applies |
| **(e)** | **Conclude attempt 6,** as attempts 1–5 were | If you'd rather carry these walls into attempt 7 |

**Proposal: (a), then (b).** Write it up while it's fresh, then take the named missing piece on paper. (c) is worth doing once (b) says what a smoothness-producing rule might look like, so the model tests something ED would actually use.

## Sources

No new sources in this note. All sources are listed in notes 2–7.

---

## Update after notes 9–10 (RD14, C55)

**Allen chose (a) then (b)** (D9). The write-up was written, then smoothness and loops on paper. **Allen accepted S-Q1–S-Q3 and L-Q1–L-Q3** (D10, D11).

### What moved

| step | verdict |
|---|---|
| **Smoothness** (note 9, C47) | **Smoothness has a known recipe:** curvature bounded below, a finite dimension ceiling, quadratic energy. The result is smooth almost everywhere, with one whole-number dimension and no fractals. **ED's meanings supply each ingredient as a labelled reading:** sync as contraction, no infinities, quadratic energy. With the sync floor and commitment's push, **three follows among such patterns.** It needs many short loops. **Consistent, not derived; wall 3 reframed as conditions a growth rule must keep** |
| **Loops** (note 10, C54) | **Wave states split exactly** into a moving sector built from values at loci (2·loci − 1, run by the pattern's random walk, the same walk that defines curvature) and a stuck sector (2·links − 2·loci + 1). **Direction-free matter only touches the moving sector,** so stuck states are dark and loops don't trap light (checked, all as expected). **Wall 2's conflict removed, conditionally** |

### Tally, updated

| | at note 8 | now |
|---|---|---|
| **Inputs supplied, nothing fitted** | 3 | **3** |
| **Relocated into the law** | 2 | 2 |
| **Proved theorems** | 1, plus two firm lemmas | 1, plus **three** firm lemmas known in form (stuck-state bound, adding never stretches, the sector split) |
| **Open conflicts with observation** | 1 risk (rest frame) | **1 risk** (rest frame) |
| **Conflicts inside ED's meanings** | 1 (no stored directions against moving waves) | **0,** conditionally (stuck states are dark) |
| **New numbers derived** | 0 | **0** |
| **Reasons for three dimensions** | 2 | **2.** The second now comes out of conditions rather than assumed smoothness |
| **Checks run in attempt 6** | 2 | **3:** dispersion bounds (5 of 7, 2 rounding misses); stuck states (S2 harness-label miss); sectors (**all as expected**) |

### The walls now

| | wall | now |
|---|---|---|
| **1** | **The rest frame** | Unchanged risk. The zero-speed part of Husain–Louko is gone (stuck states are dark). What's left is the ordinary slow-short-wave question inside the moving sector, with the recoil argument |
| **2** | **Stuck states** | **Reframed: a large dark sector,** no role assigned. Open: leakage when relations rewire |
| **3** | **Smoothness** | **Reframed: conditions a growth rule must keep** (sync as contraction, no infinities, quadratic energy, many short loops). **No growth rule that keeps them has been written or tested** |
| **4** | **Numbers** | G, masses, couplings, sync strength: inherited |
| **5** | **The handle-free rule** | Chosen, labelled |

**Also open:**
- the discrete-to-continuum step for general patterns;
- the Lorentzian (time-ordered) version of the smoothness theorems;
- short waves in the moving sector (slightly slow at lowest order, hand arithmetic);
- spin, charge, which knot is which particle;
- PF-Q2.

**Flagged, not claimed:** a large sector ordinary matter can't touch; stuck states and particles both living on loops.

### What's genuinely gained since note 8

1. **Smoothness is no longer a mystery ingredient.** It's three conditions, each with a reading from ED's meanings.
2. **Light and smoothness run on one operator,** the pattern's own random walk.
3. **The one conflict inside ED's meanings is gone,** conditionally: the meaning that makes most states stuck also makes them dark.

### Method notes

- **The borrowed-assumption lesson from note 8 was applied:** quadratic energy was taken as a new labelled reading, not borrowed from A5's assumption Q.
- **The sector check was written with explicit dimensions and invariance tests first,** and ran clean.

### Options, updated (Allen decides)

| | option | why |
|---|---|---|
| **(a)** | **Specify a model of the constrained growth process, on paper:** sync pulls relations in, relations cost, neighbourhoods don't spread apart. Fix rules, the dimension reading (counting outward, the ball-cut, heat spreading as the smoothness test), sizes, a stopping point, an exit rule and expected results. **No run until Allen confirms** | The paper picture is now consistent. Whether this process grows a smooth three, and how much leaks into the dark sector, only a model can answer |
| **(b)** | **Leakage when relations rewire,** on paper | The main open point from loops |
| **(c)** | **Short waves in the moving sector,** on paper | What's left of wall 1's leak |
| **(d)** | **Conclude attempt 6,** carrying the reframed walls into attempt 7 | A natural break: both roads walked, two walls reframed |

**Proposal: (a).** Writing the model down is still a paper step, and it forces every rule into the open before anything runs. Running it would be a separate yes.

---

## Final stock-take and conclusion (RD30, C90)

**Allen:** "take stock and conclude attempt 6" (D23). **Attempt 6 is concluded.**

### What happened after the update above

| step | what was found | ledger |
|---|---|---|
| **Model specified** (note 11) | CGP: clocks, births onto links, sync pulls, paired rewiring, neighbour cap, curvature floor. Knobs, readings, expected results and exit rule fixed first | C56–C60 |
| **Readings calibrated** (notes 12–13) | Run 1: 2 of 4 test patterns as expected (bias at the grain and at the pattern's edge). Fixed to read the middle range of scales. **Run 2: 6 of 6, including 2 held-out patterns** | C61, C62, C70 |
| **CGP froze** (note 12) | Sync filled every point's link slots before newborns could join; stalled at 50 points | C63–C66 |
| **M2** (note 13) | One change: newborns go *inside* links. No freezes | C67–C69 |
| **M2 timing trial** (note 14) | The tight floor grows **a single ring**: a triangle-closing link bends the ring beyond the floor | C71–C73 |
| **M2 runs** | The full plan cost 5 times its estimate and was cut back twice (reduced plan, then strong sync only). A reboot interrupted one night | C74–C81 |
| **Time order** (notes 15–16) | Both models grew space without ED's time order. In the literature, causality (space doesn't branch) is what gives smooth geometry, and ED already has "order plus number". No known rule combines finite neighbours, no branching, no built-in dimension and a smooth pattern. 2D CDT shows causality gives smoothness only once slice dimension is given | C82–C88 |
| **M2 results** (note 17) | Weak and strong sync: **no run reaches three.** Tight floor: ring. Loose floor: rough, low-dimensional tangle (mass dim about 1.2–2.0, walk dim about 2.4–2.8) or a stall. No floor: small world. A test of space-without-time, as expected | C80, C89 |

### Final tally

| | after attempt 5 | after attempt 6 |
|---|---|---|
| **Inputs supplied, nothing fitted** | 3 | **3** |
| **Relocated into the law** | 2 | 2 |
| **Proved theorems** | 1 | 1, plus **three firm on-paper lemmas** known in form: the stuck-state bound, "adding never stretches", the sector split |
| **Open conflicts with observation** | 1 risk (rest frame) | **1 risk** (rest frame) |
| **Conflicts inside ED's meanings** | — | **0,** conditionally (stuck states are dark) |
| **New numbers derived** | 0 | **0** |
| **Reasons for three dimensions** | 1 | **2** |
| **Checks and models** | — | 3 paper checks, 2 calibration runs, 2 models (CGP froze; M2 ring, tangle or small world) |

### What attempt 6 gained

1. **Waves:** the slow-short-wave worry is sharpened; stuck states turn out dark to ordinary matter; light and smoothness run on one operator.
2. **Growth:** adding alone can't expand; a second, ratio-free reason for three; smoothness has a recipe with a reading from ED's meanings for each ingredient.
3. **Models:** calibrated readings, and two models with clear structural outcomes. Growing space *without* time gives rings, rough tangles, stalls or small worlds.
4. **The missing ingredient named:** ED's time order. The growth question is now a precise open problem, split into two halves:
   - **causal growth where space doesn't branch,** for smoothness (2D CDT shows this half works when slice dimension is given);
   - **sync plus commitment picking slice dimension three.**

### The walls, carried into attempt 7

| | wall | state |
|---|---|---|
| **1** | **The rest frame** | Risk. The zero-speed part of the leak is gone; the ordinary slow-short-wave question remains |
| **2** | **The dark sector** | Stuck states are dark. Leakage when links rewire is open; no role assigned |
| **3** | **Growth and smoothness** | **Open problem, stated precisely:** a finite-neighbour causal growth rule where space doesn't branch, with slice dimension three from sync and commitment |
| **4** | **Numbers** | G, masses, couplings, sync strength: inherited |
| **5** | **The handle-free rule** | Chosen, labelled |

**Also open:**
- spin, charge, which knot is which particle;
- PF-Q2;
- the discrete-to-continuum step;
- the time-ordered smoothness theory;
- short waves in the moving sector.

### Method notes

- **Cost estimates missed twice.** Readings timing left out the curvature reading. A projection used only the cheapest jobs. Both are recorded, and the scope was cut openly each time.
- **A reboot interrupted the run.** No results were lost; the runner resumes.
- **One process check reported nothing running while workers were still finishing jobs.** Unexplained, recorded, and no result was affected.
- **Partial results are labelled as partial.** The full pre-registered M2 verdict wasn't reached.

### Proposed opening road for attempt 7

**M3: growth with time order.**
1. **Causal half first:** with slices given as lines, does ED's no-branching causal growth reproduce 2D CDT's known result (a random tree, dimension 2)?
2. **Then the real question:** with nothing built in, do sync and commitment make slices settle at dimension three?

Specified on paper first, with expected results and a stop rule written in advance.
