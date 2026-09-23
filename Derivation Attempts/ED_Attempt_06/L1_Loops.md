# Loops, on paper

*ED_Attempt_06, note 10. 2026-09-15 (RD13). Ledger: C47–C53. Literature, reasoning and one linear-algebra check (nothing evolved in time). No simulation. **Meaning questions L-Q1–L-Q3 and the draft exit rule are for Allen.***

## Where smoothness left it (C47)

**Allen accepted S-Q1–S-Q3 and the exit rule** (D10). Recorded:

> **Smoothness:** curvature bounded below, a finite dimension ceiling and quadratic energy give a smooth-almost-everywhere space with one whole-number dimension, fractals excluded; ED's meanings supply these as readings (sync as contraction, no infinities, quadratic energy); with part 3's floor and commitment's push, three follows among such patterns; on a discrete pattern this needs curvature nearly nonnegative at the grain, i.e. many short loops, against the stuck-state wall; the discrete-to-continuum step is not established. **Consistent, not derived; the smoothness wall is reframed as conditions a growth rule must keep.**

## The question

**Smoothness needs many short loops. Stuck states live on loops** (C12). Is there a way through, or do walls 2 and 3 really fight?

## What's known (C48)

| | what it says | source |
|---|---|---|
| **Two kinds of eigenstate** | For the Grover walk, the eigenvalues split into an **"inherited" part**, lifted from the pattern's ordinary random walk, and a **"birth" part** at ±1 whose size is set by the number of loops | Spectral mapping theorem (Higuchi, Konno, Sato, Segawa), as in Kubota, Saito, Yoshie, arXiv:2103.05235, Thm 2.1 (A6 C9) |
| **Random walks on random patterns** | The pattern's random walk (its graph Laplacian) approaches the smooth one on fine random patterns | A6 C2 |
| **Curvature is the same walk** | Ollivier curvature measures how that random walk's steps from neighbours draw together | A6 C42 |

## On paper (C49)

### 1. Every wave state splits exactly in two

**Take ED's walk:** the flip-flop shift, and a coin treating a locus's neighbours alike (W-Q2).
- **Write d for "add up what leaves each locus"** (normalized).
- **Write T = dSd\*** for the pattern's ordinary random walk: from a locus, step to a neighbour.

| sector | what's in it | dimension (connected, non-bipartite pattern) |
|---|---|---|
| **Moving** | States **built from values at loci**: d\*f and Sd\*g | **2·loci − 1** |
| **Stuck** | Everything perpendicular: states adding to zero leaving and arriving at every locus | **2·links − 2·loci + 1** |

**Firm** (algebra, for every coin in the family):
- **the moving sector maps into itself.** One step sends d\*f to a multiple of Sd\*f, and Sd\*g to a mix of d\*g and Sd\*Tg;
- **the stuck sector is exactly its perpendicular,** so the two never mix while the pattern stays fixed;
- **the moving sector's motion is run by T:** for the Grover coin, its frequencies are exactly cos ω = λ for each eigenvalue λ of T.

### 2. Direction-free matter only touches the moving sector

- **Matter feels the pattern only through the walk** (W-Q5). The walk has no stored directions (W-Q2).
- **So a source or absorber at a locus treats that locus's links alike.** What it emits is the all-equal share at that locus: d\*δ, which is in the moving sector.
- **Stuck states are therefore dark to direction-free matter:** never excited by it, never emitting to it, while the pattern is fixed.

### 3. Loops enlarge the dark sector without trapping light

- **Smoothness's short loops add links,** so they enlarge the stuck sector (2·links − 2·loci + 1).
- **The moving sector stays 2·loci − 1** however many loops there are.
- **So loops don't trap light.** They add dark states that direction-free light never enters.
- **Walls 2 and 3 don't fight** once the sectors are seen.

**A striking fit:**
- **The moving sector is run by T,** the pattern's random walk.
- **The smoothness reading S-Q1 (curvature as contraction) is about the same T.**
- **Long waves on a smooth random pattern follow T's smooth limit** (C2, C3). With cos ω = λ, λ ≈ 1 − u gives ω ≈ √(2u), which grows in proportion to the wavenumber: **light-like at long wavelengths, the same every way.**

**Short waves within the moving sector** (hand arithmetic, not script-checked, idealized hops of one length ℓ in every direction):
- λ = sin(kℓ)/(kℓ) gives phase speed f ≈ 1 − (kℓ)²/90 at lowest order.
- **So short waves are still a little slower than light.** Part 1's question survives inside the moving sector, without the zero-speed states.

## The check (C50)

`checks/l1_sectors_check.py`, expected results written first. Same 3 stand-in patterns (79 loci), 3 coins:

| | expected | run 1 |
|---|---|---|
| **L0** | moving dimension 2·loci − 1 = 157; stuck 2·links − 2·loci + 1 | **As expected** (157, and 305, 353, 417) |
| **L1** | the moving sector maps into itself, all 9 cases | **As expected** (error ≤ 6 × 10⁻¹⁵) |
| **L2** | the sectors are perpendicular and fill everything | **As expected** (overlap ≤ 5 × 10⁻¹⁶) |
| **L3** | Grover frequencies in the moving sector = ±arccos λ(T), plus 0 once | **As expected** (mismatch ≤ 5 × 10⁻¹⁵) |

**All as expected. No misses.**

## What it means (C51)

- **Wall 2's conflict is removed, conditionally.** "No stored directions" makes most wave states stuck, but the same meaning makes them **dark**: direction-free matter never touches them. Light lives in the moving sector, which loops don't shrink.
- **The Husain–Louko question** (C11): the zero-speed states no longer set the threshold, because matter can't reach them. What's left is the ordinary slow-short-wave question inside the moving sector (f ≈ 1 − (kℓ)²/90 at lowest order), with the recoil argument of C11 still applying.
- **Smoothness and light share one operator:** the pattern's random walk.
- **Inputs:** unchanged (still 3). This removes a conflict; it doesn't shorten the input list.

## Open, and flagged (C52)

- **When relations rewire** (growth, G-Q2), the sectors themselves shift. Amplitude on rewired links can land in the new stuck sector. How much leaks per rewiring isn't worked out.
- **The dark sector is large:** at least 1 − 2/(mean neighbours) of all states. It has no role assigned.
  - **Flagged resemblance, not a finding** (look-elsewhere): a large sector that ordinary matter can't touch.
  - **Also flagged:** stuck states live on loops, and particles are loops (A5 C31).
  - **Neither is claimed.**
- **Direction-free coupling is a reading** of W-Q2 and W-Q5 applied to sources (L-Q1). A coupling that treats a locus's links unequally would reach the stuck sector.
- **The patterns are hand-built stand-ins** (W-Q3). The split is exact on any fixed pattern, but which pattern ED grows is still open (road G).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **L-Q1** | **Does matter act on the walk only at loci, treating a locus's relations alike?** | **Yes** | No stored directions (W-Q2); matter feels the pattern only through the walk (W-Q5) |
| **L-Q2** | **Is light the moving sector** (states built from locus values)? | **Yes** | Follows from L-Q1: it's the only sector matter can make |
| **L-Q3** | **Is the stuck sector real but dark,** with no role assigned yet? | **Yes, with the resemblances flagged** | It's there in the algebra; claiming a role would be fitting |

## Draft exit rule (Allen to confirm)

- **With L-Q1–L-Q3 accepted:** record
  > **"Loops: for ED's direction-free coined walks, wave states split exactly into a moving sector built from locus values (dimension 2·loci − 1, run by the pattern's random walk, the same walk that defines curvature) and a stuck sector (2·links − 2·loci + 1); direction-free matter only touches the moving sector, so stuck states are dark while the pattern is fixed; smoothness's short loops enlarge the dark sector without trapping light. Wall 2's conflict is removed, conditionally, and reframed as a dark sector. Open: leakage when relations rewire, the dark sector's role, and slow short waves within the moving sector."**
- **If L-Q1 is rejected** (matter may treat links unequally): wall 2 stands as in C15.
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide L-Q1–L-Q3** and confirm the exit rule | Settles whether wall 2 is reframed |
| **(b)** | **Update attempt 6's stock-take and write-up** | Two walls moved since note 8 (smoothness reframed, stuck states dark) |
| **(c)** | **A model of the constrained growth process** (sync pulls relations in, relations cost, neighbourhoods don't spread apart), expected results first | The picture is now consistent enough for a model to test something ED would use |
| **(d)** | **Leakage when relations rewire,** on paper | The main open point here |

**Proposal: (a), then (b),** then choose between (c) and concluding attempt 6.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C48 | Kubota, Saito, Yoshie, arXiv:2103.05235, Theorem 2.1 (PDF read locally, A6 C9); Higuchi, Konno, Sato, Segawa, arXiv:1401.0154 (listing, A6 C9); A6 C2 and C42 sources | Earlier in attempt 6 |
| C50 | `checks/l1_sectors_check.py` → `checks/l1_sectors_check_run1.txt` | Run 2026-09-15 |
| — | A5-ledger C31; A6 C2, C3, C9, C11–C15, C40, C42–C47 | Earlier ledgers |
