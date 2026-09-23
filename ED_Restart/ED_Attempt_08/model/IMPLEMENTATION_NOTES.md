# Implementation notes (ED_Attempt_08)

*Written before any code is run. Each section is fixed before the thing it describes is built, following attempt 7's habit.*

## The port (E2, note 2's C6; D3)

**What it is:** attempt 7's `c3c`–`c3f` rewritten onto flat integer arrays with the inner loop compiled by Numba. **Same model, same knobs, same moves, same acceptance rule.** The only intended differences are representation and speed.

**Environment:** `numba 0.67.0` and `llvmlite 0.49.0` installed 2026-09-19. **numpy stayed at 2.4.4** — numba 0.67 accepts `numpy<2.6`, so nothing was downgraded and attempt 7's code runs unchanged in the same interpreter. Recorded because a library change that moved numpy would have made attempt 7 unreproducible.

**Readings are copied, not rewritten:** `readings.py`, `readings_v2.py`, `c3a.py`, `c3b.py` copied from `../ED_Attempt_07/model/` with matching SHA-256 prefixes (`3d5320d3adb6e407`, `e25b73ab4fcff02a`, `c76fc789ee509235`, `86d76dfdb28174b5`), the same way attempt 7 took its readings from attempt 6. They take a scipy sparse adjacency matrix, and the port supplies one.

### Data structures

| attempt 7 | the port | why |
|---|---|---|
| `tets: tid -> 4-tuple` | `tv[tid, 0:4]` int32, sorted; `t_alive` | Contiguous, no hashing to read a tetrahedron |
| `tetkey: 4-tuple -> tid` | Open-addressing hash on a 64-bit mix of the four ids, **collisions resolved by comparing `tv` rows** | Exactness does not depend on the hash |
| `vt: vertex -> set of tids` | Arena with power-of-two size classes and per-class free lists; per vertex `(start, len, cap)` | Sets per vertex were the memory cost that exhausted 15 GB |
| `nbrs: vertex -> set` | The same arena scheme | Degree is then `len`, read in O(1) |
| `val: edge -> valence` | Open-addressing hash on `min*2^32 + max` → edge slot; `e_a`, `e_b`, `e_val` arrays with a free list | Edge lookup is the innermost operation in the model |
| `tid_set`, `val3` (RandomSet) | Index-swap pools over slots, same add/discard/choice semantics | Unchanged in behaviour |
| `next_id` monotone, ids never reused | **Vertex slots are reused from a free list** | Otherwise 150 ticks at n = 52 would allocate about 10 million vertex slots |

**Slot reuse changes iteration order relative to attempt 7.** That is already covered by note 2's C5: the random path cannot be reproduced by construction, which is why the validation ladder is tiers 1–3 rather than bit-for-bit.

### Randomness

**The port carries its own generator** — splitmix64 seeding xoshiro256\*\* — rather than numba's, so a run is reproducible from a seed **within the port**, independent of numba's version and of thread count. Draws needed: uniform, integer below n, geometric, and a Fisher–Yates shuffle. `geometric(p)` uses the inverse CDF, `k = floor(log(u)/log(1-p)) + 1`, matching the distribution of attempt 7's `rng.geometric`, not its draws. The rate spread `omega` is drawn once at setup in numpy, outside the kernel.

### Move plans and the per-move edge delta

Every gate (`allowed`), the cost change (`delta_S`) and `n3_after_exact` need the same thing: **the change in valence for each edge the move touches.** In attempt 7 that was a Python dict built per call. In the port it is a **scratch open-addressing table cleared by a stamp counter**, so no allocation happens inside a tick. Plans are written into preallocated scratch buffers (4,096 tetrahedra, enough for any star at a ceiling of 60).

### What is kept identical, on purpose

- **The move set:** link-condition merge, star split, 2–3 and 3–2 flips, and **paired flips** (one 2–3 and one 3–2 at disjoint places, refused if the 2–3 would create the triangle the 3–2 needs absent).
- **The gates:** budget (`born - dies > max(pool, 0)`), ceiling (60), and the sync condition with the **units fix** — raw tick differences divided by σ/K before comparing with `s_max`.
- **The cost:** `S = alpha*E + lam*sum (valence - 5.104)^2`, with no sync term.
- **The acceptance rule:** `corr * exp(-dS)`, with `corr = n3_now / max(n3_after, 1)` for paired flips.
- **The constants:** `FLAT_VALENCE = 5.1043`, `SIGMA = 0.0005`, `K = 0.5`, `K_RESPONSE = 1.0`, `FLAT_LINKS_PER_EVENT = 6.699`, `CEILING = 60`, `SYNC_FACTOR = 1.5`, `TETS_PER_EVENT_CAP = 20`.
- **`check()` runs every tick,** as in attempt 7, and its time is reported separately so the growth cost and the checking cost can be told apart.

### Verification, before any timing is quoted

**Tier 1** — for the same state and the same proposed move: `link_condition`, the budget gate, the ceiling gate, the sync gate, `n3_after_exact` and `delta_S` agree with attempt 7 exactly (integers bitwise, floats to 1e-12).
**Tier 2** — a fixed scripted sequence of moves from the same start gives an identical complex in both codes: same V, E, T, same sorted degree sequence, `check()` clean in both.
**Tier 3** — whole runs at n = 24, eight seeds in the port, with attempt 7's two values per setting inside the port's spread.

**No per-tick time is quoted until tiers 1 and 2 pass.**
