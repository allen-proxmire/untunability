# Implementation notes (written before any run)

*ED_Attempt_07, model folder. 2026-09-16 (RD4). Choices note 3 (`C1_Model_Spec.md`) left open, written before the timing or any run. Nothing here changes the rule, expected results or exit rule.*

## Readings

**`readings.py` and `readings_v2.py`** are copied from `ED_Attempt_06/model/` unchanged; their SHA-256 hashes are recorded in the ledger (RD4). These are A6's readings v2, which met 6 of 6 calibrations (A6 C70).

## Build (`c1.py`)

**Offspring:**
- **Ordinary events:** c = (geometric draw with p = ½) − 1, giving P(c) = (1/2)^(c+1).
- **The spine event:** c = 1 + negative-binomial(2, ½), giving P(c) = c·(1/2)^(c+1).
- **Next spine event:** chosen uniformly among the spine event's children.

**Seeds:** each tree seed s uses one random stream for all its draws, including the spine choice. So `slice_lengths(T, s)` and the full build for seed s grow the same tree.

**Slices:** slice t+1 lists children in parent order around slice t, and in birth order within a parent.

**Links:**
- **In-slice:** a cycle when L ≥ 3; one link when L = 2; none when L = 1.
- **Forward:** event i with children starting at s_i links to next-slice positions (s_i + j) mod L_{t+1}, for j = 0…c_i.

**Structure checks (S2):**
- **In-slice:** each slice with L ≥ 3 has degree exactly 2 within the slice and one connected piece.
- **Forward count:** forward links out of slice t, counted before merging duplicates, equal L_{t+1} + L_t.
- **Direction:** every forward link joins slice t to t+1.
- **Parent tree:** parent links (event i to its own children) number N − 1 and form one connected piece.

**Readings pattern:** undirected, with self-links and duplicate links removed.

## Flat calibration

**Build:** 200 events in every slice, each with exactly one child, over 200 slices.

**Structure:** in-slice cycles and the forward count and direction are checked. The parent-tree check doesn't apply, since the parent links of a full starting slice form 200 separate lines, so its note is dropped.

## Runs (`c1_run.py`)

- **Slice-length check:** 1,000 seeds (0–999), T = 200 slices, so t = 0…199. **The fit uses t = 10…199,** because note 3's "10…200" has no slice 200 when T = 200.
- **Readings runs:** seeds 0–9, with centre seed 1,000 + s. The flat strip uses centre seed 999.
- **Medians** ignore undefined readings.
- **Outputs:** `c1_run1.txt` and `c1_run1.json`.

## C2a (`c2a.py`, `c2a_run.py`, `c2a_timing.py`), written before any C2a run

*Allen D7 ("defaults are fine, run C2a").*

**Offspring:**
- **Mean:** μ is computed per event from its budget (reading B) or its past-link count (reading A).
- **Draw:** c = geometric(p = 1/(1+μ)) − 1, so P(c) = p(1−p)^c with mean μ. μ = 0 gives c = 0.

**Start:**
- **Slice 0:** L\* events, each with budget 1 (so b_ref = 1).
- **Reading A:** past-link count 2 for slice 0, the balanced value.

**Budget (reading B):**
- **Split:** event x sends b_x/(c_x + 1) along each of its c_x + 1 forward links (targets as in C1).
- **Receive:** each new event sums what arrives.
- **Conservation:** checked every slice to 10⁻⁹ relative.

**Stopping:**
- **Died:** a slice with no offspring.
- **Ran away:** a slice over 10·L\* events. The run stops and is recorded.

**Balance statistics:** for a survivor, mean offspring = the mean of L_{t+1}/L_t over t = T/2…T−2. Mean length = the mean of L_t over t = T/2…T−1.

**Seeds:**
- **Balance runs:** seeds 0–19 per setting (each setting reuses seeds 0–19).
- **Geometry runs:** seeds 100–102.
- **Reading centres:** seed 2000 + 10·s + 10·k.

**Structure (geometry runs):** C1's `build` checks. The parent-tree check is dropped, as for C1's flat strip, since a full starting slice gives a forest.

**Output:** `c2a_run1.txt` and `.json`.

## Timing (`c1_timing.py`)

Build plus readings on the flat strip and on tree seed 0, and slice-length generation on 20 seeds scaled to 1,000. **Timing only.**

## C2b (`c2b.py`, `c2b_timing.py`), written before any C2b run

*Allen D10, D11 ("defaults are fine, add the tilt reading, code C2b and time it"). Choices note 9 left open.*

**Slices:**
- **Grids:** neighbours are the ±1 shifts along each axis (periodic), so the degree is exactly 2d.
- **Random slices:**
  - **Radius:** set so the expected degree (N − 1)·V_d·r^d equals 10, where V_d = 2, π, 4π/3.
  - **Links:** found with a periodic k-d tree.
  - **Connectedness:** checked with connected components. A disconnected draw is redrawn with seed 1000 + 10·seed + redraw, up to 100 redraws; the count is recorded.

**Update:**
- **Pull:** tanh of each link's difference, summed per event with `bincount`, times K/deg. Every event reads only slice t values, so the update is causal.
- **Storage:** ψ = φ − t in float64.

**Rates:**
- **Persistent:** ω − 1 = σ·g, drawn once from `default_rng(seed)`.
- **Fresh control:** a new σ·g each tick from the same stream.
- **Seeds:** the same seed is used for every size, so the rate draws at different sizes share their leading numbers. Accepted and recorded; they are independent in effect because the slices differ.

**Checks:**
- **Settling marks:** ψ is copied at ⌊2T/3⌋ and ⌊0.9T⌋.
- **Rate spread:** std of (ψ_T − ψ_0.9T)/(T − ⌊0.9T⌋).
- **Largest neighbour difference:** over all links at T.

**Control sampling:** 300 integer times evenly spaced from T − ⌊T/3⌋ to T − 1; duplicates are merged by the set, so there can be slightly fewer than 300 samples at small T.

**Tilt reading (D11):**
- **Grids:** offset r along every axis, r = 1, 2, 4, … ≤ n/2.
- **Random slices:** unweighted shortest paths from 20 sources, r = 1, 2, 4, … while at least 100 pairs sit at exactly distance r.
- **Stored:** tilt(r) = √(mean squared difference)/r. The slope summary is computed in the runner.

**Timing:** 500 steps for every size, kind and noise type, plus the slice build, the tilt pairs, and the tilt sampling cost. A smoke test prints only that the code path completes.

## C2b run 2 (`c2b_run2.py`), written before running

*Allen D13 ("a, rerun with R1 and R2").*

**Code change:** `simulate` takes `sigma` as an argument, defaulting to the module's σ = 0.002, and stores it in each result. Run 1's behaviour is unchanged.

**Run 2 settings:**
- **R1:** σ = 0.0005. E1's rate-spread limit is 0.01 × 0.0005.
- **R2:** seeds 3–12.
- **Output:** `c2b_runs2/`, 6 worker processes.

**Seed overlap:** random-slice seeds follow note 9's 1000 + 10·seed + redraw. So a seed that needed 10 or more redraws could reuse the next seed's slice. Each run stores its slice seed, and the analysis reports any duplicates at the same (d, n).

Everything else as note 9.

## C2b run 3 (`c2b_run3.py`), written before running

*Allen D14 ("a, rerun with the fixes").*

**Settings:** σ = 0.0005; seeds 13–22; output in `c2b_runs3/`.

**Readings:**
- **Pooled:** E2–E4 and the separation check use the pooled W, √(mean over seeds of W²) at each size.
- **E5:** keeps the per-seed median, as in note 9.
- **Per-seed medians** are also reported for E2–E4.

**E1 degree range:** 10 ± 3·√(20/N).

**Random slices:**
- `random_slice(..., scheme="v2")` seeds each draw with 1000·(seed + 1) + redraw, allowing up to 1,000 redraws. No two seeds can share a slice.
- Scheme v1, the default, is unchanged. A check confirmed identical slices to before.

## C3a (`c3a.py`, `c3a_timing.py`), written before any C3a run

*Allen D19 ("defaults are fine, code C3a and time it"). Choices note 13 left open.*

**Slice storage:** a rotation system. `ring[v]` is v's neighbours in counter-clockwise order; consecutive neighbours (a, b) form the triangle (v, a, b).

**The flat start:** a triangular grid with neighbours (i+1, j), (i, j+1), (i−1, j+1), (i−1, j), (i, j−1), (i+1, j−1), periodic.

**Split of x at ring positions i < j:**
- x keeps the arc ring[i..j] and the new event y takes the arc ring[j..i].
- Events inside y's arc swap x for y.
- In u's ring, x becomes (x, y); in w's ring, x becomes (y, x).
- The children's degrees are j − i + 2 and k − (j − i) + 2.

**Collapse of v into a:**
- **Allowed** when v and a share exactly the two ring tips c1 and c2, each tip has degree ≥ 4, and deg v + deg a − 4 ≥ 3. The last condition rules out the closed-tetrahedron case.
- **Rings:** a's ring swaps v for v's inner neighbours n2…n_{k−2}; c1 and c2 drop v; inner neighbours swap v for a.

**Structure check, every tick:**
- the degree sum equals 6V (so V − E + F = 0);
- no ring repeats or contains its own event, and every ring has at least 3 members;
- for every triangle (v, a, b), a's ring has b just before v and b's ring has a just after v. That checks both orientation and that every edge lies in exactly two triangles.

**Tick:**
- **Offspring:** c = geometric(1/(1 + μ)) − 1, with μ = max(0, 1 + (b − 1)) at k = 1.
- **Collapses:** childless events in shuffled order. Allowed partners are chosen uniformly (U) or with weights e^(−λ(ΔE − min ΔE)) (Q). With no partner, the event keeps one child and is counted as forced.
- **Splits:** events with c ≥ 1, in shuffled order, each getting c − 1 splits of its newest child, with pairs chosen the same way as partners.
- **Budget:** a collapse moves budget to the partner. Each surviving event's total, including any absorbed budget, is shared equally among its children.

**ΔE:**
- **split:** (d1 − 6)² + (d2 − 6)² + (du − 5)² + (dw − 5)² − (dx − 6)² − (du − 6)² − (dw − 6)²;
- **collapse:** (da + dv − 10)² + (d1 − 7)² + (d2 − 7)² − (dv − 6)² − (da − 6)² − (d1 − 6)² − (d2 − 6)².

**Calibration R:**
- **Proposal:** pick an event uniformly, then one of its neighbours uniformly.
- **Flip conditions:** both ends have degree ≥ 4, and the opposite tips aren't already linked.
- **Metropolis acceptance:** min(1, [1/(d1+1) + 1/(d2+1)] / [1/dv + 1/da]), which makes the uniform measure stationary.

**Spacetime pattern:**
- **Nodes:** (tick, id).
- **Links:** in-slice links from each slice before its tick; forward links to each child; a collapsed event links to the event that finally absorbed it, following chains within the tick.
- Self-links and repeats removed.

**Readings and eccentricity:**
- **Readings:** readings v2 `all_readings` on the slice adjacency.
- **Eccentricity:** the mean over 20 random events of their largest hop distance.

## C3b (`c3b.py`, `c3b_timing.py`), written before any C3b run

*Allen D23 ("defaults are fine, code C3b and time it"). Choices note 16 left open.*

**Graphs:** undirected sparse adjacency, with self-links and repeats removed.

**The five stand-ins:**
- **F:** a periodic cubic grid.
- **FR:**
  - **Radius:** set so that (N − 1)·(4/3)π r³ = 14.
  - **Links:** found with a periodic k-d tree.
  - **Connectedness:** redraws use seed 1000·(seed + 1) + redraw.
- **B:**
  - **Blocks:** 4×4×4 grids with open edges (degree 3–6).
  - **Tree:** a Prüfer sequence decoded with a heap into a uniform random labelled tree, seeded by 1000·(seed + 1).
  - **Necks:** each tree edge links one uniformly random event of each of its two blocks.
- **H:**
  - **Build:** a configuration model on 6 stubs per event.
  - **Repair:** self-loops and repeated links are fixed by swapping each bad pair's partners with a random pair, for up to 200 passes.
  - **Checks:** the result must be simple and connected, otherwise a redraw.
  - **Recorded:** this is close to, but not exactly, uniform over 6-regular graphs.
- **Cr:**
  - **Build:** G(N, m) with m = round(N√N/2), from random pairs with self-pairs and repeats rejected, so the mean degree is exactly about √N.
  - **Connectedness:** redraws as above.

**Sync solve:**
- **Rates:** ω ~ N(0, 1) with seed 100 + seed, and K = 1.
- **Equation:** L = D − A, with Ω the degree-weighted mean rate.
- **Method:** event 0 is grounded and the reduced system is solved, by conjugate gradient (relative tolerance 10⁻¹²) when the mean degree is above 7 or every degree is 6 (F, FR, H, Cr), and by a direct sparse solve otherwise (B).
- **Checks and readings:** the relative residual of the full system is recorded; φ is centred; the largest |φ_u − φ_v| over links and its link are kept. For B, the runner checks whether that link is a neck.

**Readings:** readings v2 `all_readings` with centre seed 3000 + seed. `small_world` is the exponential-growth flag.

**Timing:** seed 0 of each stand-in at each size. It prints only timings and harness facts (connected, degrees, residual, redraws, whether readings were defined).

**Change after the first timing attempt** (no signal values seen):
- **What happened:** readings v2's walk part took 301 s on B at 8,192 events, and would take hours at 27,648, because diffusion on tree-like graphs is slow.
- **The change:** `readings` now uses only the ball-growth part of readings v2 (`mass_and_cut` on distances from the same 200 centres). That gives d_H, the power and exponential fit qualities, r_max, r_lo and the `small_world` flag.
- **Why it's allowed:** E1–E4 and note 16's reported d_H need nothing else. The walk-based spectral dimension isn't part of C3b.
- **The first attempt** was stopped, and the timing trial rerun with unbuffered output.

## C3c (`c3c.py`, `c3c_timing.py`), written before any C3c run

*Allen D26 ("defaults are fine, code C3c and time it"). Choices note 18 left open.*

**Storage:**
- **Tetrahedra:** sorted 4-tuples with ids.
- **Per event:** the set of tetrahedra containing it, and its neighbour set.
- **Per edge:** its valence.
- **Random draws:** the tetrahedron ids and the valence-3 edges are kept in random-access sets.
- **Every move** is "remove these tetrahedra, add these," so the valences and neighbour sets update in one place.

**The flat start:**
- **The grid:** a periodic n³ cube grid. Each cube is cut into 6 tetrahedra along its long diagonal, one per ordering of the three axes.
- **Checks:** no repeated tetrahedra, degree 14, T = 6V, E = 7V.

**Merge v → a:**
- **Allowed when:** the common neighbours of v and a (other than each other) are exactly the vertices of Lk(va); the common edges of their links (triangles opposite v not containing a, and opposite a not containing v) are exactly the edges of Lk(va); and the links share no triangle. That's the 3D link condition of Dey–Edelsbrunner.
- **Plan:** remove every tetrahedron containing v; re-add those not containing a with v replaced by a.

**Split x at neighbour u** (C3c-Q1): new child y. Each tetrahedron {x, u, p, q} becomes {y, u, p, q}, and {x, y, p, q} is added.

**Flips:**
- **2–3:** a random tetrahedron and a random face (uniform over triangles). Refused if the two apexes coincide or are already linked.
- **3–2:** a random valence-3 edge whose three surrounding tetrahedra have exactly three ring vertices. Refused if that triangle already exists.
- **Proposal correction:** F_before / n3_after for 2–3, and n3_before / F_after for 3–2 (F = 2T), so zero cost gives the uniform measure.
- **Acceptance:** min(1, correction × e^(−ΔS)).
- **S0:** "flips always accepted if valid" (note 18) is implemented as no cost-based rejection, with the proposal correction still applied, so S0's flips and calibration RC sample the same uniform measure. Recorded as an interpretation.

**ΔS:**
- **Valences:** the changes are summed over the removed and added tetrahedra.
- **Links born and links that die:** these carry the commitment term (±α) and the sync term (∓γ·(Δφ/(σ/K))²).
- **Curvature:** λ times the change in (valence − 5.1043)², over edges present before or after.
- **A new split child** uses its parent's tick count.

**Tick order:**
1. offspring;
2. merges in shuffled order (partners weighted by e^(−ΔS), with a forced keep if none are allowed);
3. splits in shuffled order (c − 1 splits of the newest child, options one per neighbour, weighted);
4. one flip sweep of V attempts, each a 2–3 or 3–2 with probability ½;
5. the C2b tick update over current links.

**Inheritance:** merged events pass their budget to the partner. Children inherit rate and tick count and share the budget equally.

**Structure check:**
- every triangle in exactly two tetrahedra;
- V − E + F − T = 0;
- no repeated tetrahedra;
- every event's link a closed surface with Euler characteristic 2, connected, whose vertices match the neighbour set.

**Readings** (`slice_readings`):
- **Ball growth:** C3b's `readings` (seed as given), giving d_H and the exponential flag.
- **Degree:** mean and largest.
- **Valence:** mean, spread and mean (valence − 5.1043)².
- **Neck strain:** C3b's `sync_steady_state` largest link difference, with its residual.

**Move tests before timing** (harness only):
- **Direct moves** on n = 4 and 6: 35–40 merges, 40 splits, 3 flip sweeps.
- **Growth ticks:** 10 ticks each of S0 and S4, with the check after every tick.
- **Results:** every check clean; budget conserved exactly; budget, rate and tick-count keys matching the event set.

## C3c runner (`c3c_run.py`), written before running

*Allen D27 ("defaults are fine, run C3c").*

**Run length:** T = 500.

**Rates and randomness:** rates come from the run's own random stream (seed s), drawn before the first tick. Choices and flips use the same stream.

**Checks:**
- **Readings** at ticks 250, 375 and 500, with seed 3000 + 10·s + size index.
- **Structure** is checked after every tick. A failure stops the run and is recorded.

**Stopping and resuming:**
- **State** (slice, stream, budget, rates, tick counts, records) is pickled every 50 ticks and removed on completion.
- **A restarted job** resumes from its last checkpoint.

**Classification:**
- **Booleans:** with two seeds, the growth flag counts only if it's set in both.
- **Numbers:** medians.
- **In-run sync strain:** the largest |φ_x − φ_y| over links, divided by σ/K.
