# Road W, part 2: does the slow-wave leak reach a discrete pattern? (on paper)

*ED_Attempt_06, note 3. 2026-09-15 (RD3). Ledger: C8–C14. Literature and reasoning, with one linear-algebra check (nothing evolved in time). No simulation. **Meaning questions W-Q4, W-Q5 and the draft exit rule are for Allen.***

## Where part 1 left it (C8)

**Allen accepted W-Q1–W-Q3 and the exit rule** (D3): each tick, each locus updates from its related neighbours; neighbours count equally, with no stored directions; the pattern is a labelled stand-in.

**Exit-rule verdict for part 1:**
- **ED's carried wave rule is attempt 2's coin-and-shift walk** (A2 C42–C44; the Fourier coin is the working default, A2 D7, not confirmed). That's a first-order walk, not a spreading rule.
- **So part 1's firm argument doesn't cover ED's rule.** Recorded: slow short waves are shown for spreading rules only.
- **Per the rule, the next step is literature on quantum walks on random graphs.** It's done below, alongside the leak question.

## What's known (C9)

| | what it says | source |
|---|---|---|
| **How the leak works** | A detector moving faster than the **slowest wave's speed** (in the preferred frame) is suddenly excited at any energy gap, however small. The threshold doesn't depend on the grain scale, and the rate is proportional to the grain's energy scale: "a violent burst." The detector is **pointlike, on a fixed path, never recoils**. They liken it to Cherenkov radiation | Husain and Louko, *PRL* 116, 061301 (2016), full text |
| **Polymer example** | Slowest wave at 0.8781 of light speed, so the threshold is rapidity 1.3675. **Heavy ions at RHIC reach rapidity about 3** | same |
| **All dimensions** | Inertial detectors get the same leak in every dimension above two (still pointlike) | Louko and Upton, *PRD* 97, 025008 (2018) |
| **Grover walk spectrum** | On any finite connected graph, the Grover walk has eigenvalue +1 about \|E\|−\|V\|+1 times and −1 about \|E\|−\|V\| times, beyond the eigenvalues inherited from the ordinary random walk | Spectral mapping theorem (Higuchi, Konno, Sato, Segawa), as stated in Kubota, Saito, Yoshie, arXiv:2103.05235, Thm 2.1 |
| **Loops trap** | If the graph has more than one independent loop (Betti number above 1), some starting states localize. On ℤ^d the Grover walk spreads and localizes at once | Higuchi, Konno, Sato, Segawa, arXiv:1401.0154 |
| **Disorder in walks** | Static disorder localizes discrete-time quantum walks (Anderson type) | *Sci. Rep.* 7, 12077 (2017) and others |
| **Deformed relativity from walks** | A quantum-walk automaton can keep a relativity principle through **nonlinear boosts**, with an invariant wave number at the grain and "relative locality" | Bibeau-Delisle, Bisio, D'Ariano, Perinotti, Tosini, *EPL* 109, 50003 (2015); Bisio, D'Ariano, Perinotti (2017) |
| **Random discreteness, no frame** | Causal-set discreteness gives Lorentz-invariant "swerves" of particles | Dowker, Henson, Sorkin, *Mod. Phys. Lett. A* 19, 1829 (2004) |
| **Still active** | Detector-coherence probes show a sharp change near the polymer threshold | arXiv:2607.15551 (2026) |

## 1. How the leak works (C10)

- **Picture a boat going faster than some of the water's waves.** It leaves a wake. The detector does the same whenever it outruns some wave.
- **In Husain and Louko's formula,** excitation at a tiny gap needs a wave with speed below the detector's (tanh β > f). **The slowest wave sets the threshold.**
- **The waves that do it are grain-sized.** Only there is f below 1.
- **The detector can hand those waves their momentum for free** because it's pointlike and never recoils.

## 2. What carrying it into ED needs (C11)

**Three things:**

| | needed | ED |
|---|---|---|
| **(i)** | A rest frame, so "moving" means something | **Yes.** ED's substrate has one (A4 C87, D32) |
| **(ii)** | Waves slower than the mover | **Grid rules:** slowest at 1/√3 of light speed (A5 C24), threshold 58% of light speed, which RHIC ions (99.5%) pass easily. **Spreading rules on a random pattern:** yes (part 1). **ED's walk:** it has waves that **don't move at all** (§3) |
| **(iii)** | Something that takes a grain-sized wave's momentum at no energy cost | **Not a real atom.** A grain-sized kick costs about 10¹⁹ GeV, while an ion at RHIC carries about 10³ GeV. That only works if grain-sized states exist at low energy. **But ED's random pattern can take up momentum itself:** with no regular spacing, momentum is only kept for long waves, like a crystal taking the recoil in the Mössbauer effect |

**So the leak, as computed, doesn't carry over directly.** It leans on a detector that never recoils.

**In ED it turns into two sharper questions:**
- **(a) Stuck or slow states at low energy:** does ED's walk have them? §3 says yes.
- **(b) The pattern's unevenness:** a body moving through the pattern's rest frame sees the unevenness sweep past, and can be jiggled by it.
  - **Rough size, if the unevenness is like random placement:** an atom holds about 4×10⁷³ grains (Bohr radius over the Planck length, cubed). Its unevenness is then about 1/√N ≈ 2×10⁻³⁷ of the average.
  - **Tiny. But how strongly matter feels unevenness isn't defined in ED,** and the grain-as-spacing step is a labelled estimate (A5 D10: the grain is a count).

## 3. A wall: direction-free walks have stuck states (C12, C13)

**On paper (C12).** Take a coined walk whose state sits on locus–neighbour pairs, with the same rule at every locus.
- **No stored directions (W-Q2) leaves two moves.** A wave arriving along a link can only be sent back along that link (the "flip-flop" shift). The coin must treat all neighbours alike: a(I + (e^{iθ}−1)P), where P picks out the all-equal share at a locus.
- **Now take a state whose amplitudes add to zero** both leaving and arriving at every locus.
  - The coin just multiplies it by a, and the shift reverses it.
  - **It flips between two states forever and never moves.**
- **Picture:** amplitude running around closed loops of links, cancelling at every locus, so nothing ever leaks out.
- **Counting:** at least 2(links − loci) such states, out of 2·links in all. **So the share that never moves is at least 1 − 2/(mean number of neighbours).**
  - 6 neighbours: at least 2/3.
  - 12 neighbours: at least 5/6.
- **This holds for every coin that treats neighbours alike,** not just Grover.

**The check (C13):** `checks/w2_stuck_states_check.py`, expected results written first. 3 random patterns (79 loci, mean neighbours 5.8–7.3) × 3 coins:

| | expected | run 1 |
|---|---|---|
| **S0** | walk is unitary | **As expected** (≤ 9×10⁻¹⁶) |
| **S1** | stuck count ≥ 2(links − loci) | **As expected in all 9** (e.g. 305–306 against 304) |
| **S2** | Grover: +1 has \|E\|−\|V\|+1, −1 has \|E\|−\|V\| | **Not as expected** (152 and 154, against 153 and 152) |
| **S3** | stuck share = 1 − 2/(mean neighbours), above ½ | **As expected** (0.658, 0.690, 0.725) |

**The S2 miss stands.**
- **A follow-up diagnostic** (`checks/w2_grover_sign_diagnostic.py`, **not pre-registered**) found two errors on my side:
  - the script compared the count at +a (which is −1 for the Grover coin) with the expected count at +1;
  - my expected count left out one eigenvalue inherited from the ordinary walk.
- **Read correctly,** seed 1 gives +1 ×154 and −1 ×152. That matches the theorem.
- **Triangle hand count:** eigenvalue +1 twice. It matches.
- **The stuck space on seed 1 has 305 states,** against the bound of 304.

**What it means:**
- **Most states of any direction-free walk on a pattern with loops never move.** A 3D pattern has many loops.
- **For waves:** part of any local wave stays put forever. That's a wall for road W, separate from the leak.
- **For the leak:** zero-speed states put the threshold speed at zero, if matter couples to them.
- **The tension:** W-Q2 forces this. The Fourier coin (A2 D7) escapes it, but it needs **an order among each locus's neighbours.** That's stored structure, which W-Q2 excludes.
- **Flagged resemblance, not a finding** (look-elsewhere): stuck states live on closed loops, and ED's particles are closed loops of commitments (A5 C31).

## 4. One other exit in the literature (C9, C14)

- **Deformed relativity:** walks can keep a relativity principle through nonlinear boosts, with no frame where the slow waves "are."
- **That would remove Husain and Louko's premise.**
- **But ED's substrate has a rest frame** (D32). Whether a deformed reading could hide that frame belongs to PF-Q2, which is still open.

## What it means (C14)

- **Husain and Louko's leak doesn't transfer as computed.** In ED it becomes (a) stuck or slow states and (b) unevenness felt by moving matter.
- **(a) is now sharp.** ED's decided meanings (a random pattern with loops, no stored directions) force a large share of stuck states for every coined walk of the carried kind.
- **(b) is tiny on rough numbers,** but not defined in ED.
- **Recorded conflict:** between W-Q2 (no stored directions) and freely moving waves. It isn't a conflict with data.

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **W-Q4** | **Keep W-Q2 and record stuck states as a wall for road W?** The alternative is to let each locus carry an order of its neighbours, which the Fourier coin needs | **Keep W-Q2; record the wall** | Least structure. An order at every locus is added, stored structure: an input the census guard would count |
| **W-Q5** | **Does matter feel the pattern only through the same walk,** with no separate coupling to unevenness? | **Yes** | Least structure. Question (b) then becomes a property of the walk |

## Draft exit rule (Allen to confirm)

- **With W-Q4's default:** record **"road W: long waves direction-free (C3); ED's direction-free walk on a random pattern with loops has at least a share 1 − 2/(mean neighbours) of states that never move (C12, C13); the Husain–Louko leak as computed does not transfer, and in ED it turns on these stuck states and on unevenness (C11)."** Close road W with the wall recorded.
- **If W-Q4 is relaxed:** record the neighbour order as a labelled input (the input list grows). The next step is the Fourier-type coin on random patterns: literature first, then a check with expected results first only if Allen wants.
- **No simulation.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide W-Q4, W-Q5** and confirm the exit rule | Settles whether road W closes on the wall |
| **(b)** | **Road G** (growth rule) | Stuck states need loops. Whether ED's pattern has loops, and how many, is exactly what a growth rule decides |
| **(c)** | **Stuck states as matter?** On paper | The loop resemblance. Look-elsewhere applies |

**Proposal: (a), then (b).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C9 | Husain and Louko, arXiv:1508.05338 (full text); Louko and Upton, arXiv:1710.06954 (full text, abstract and model sections); Kubota, Saito, Yoshie, arXiv:2103.05235 (Theorem 2.1, full text); Higuchi, Konno, Sato, Segawa, arXiv:1401.0154 (listing); *Sci. Rep.* 7, 12077 (2017) (listing); Bibeau-Delisle et al., arXiv:1310.6760 (abstract); Bisio, D'Ariano, Perinotti, arXiv:1707.08455 (listing); Dowker, Henson, Sorkin, gr-qc/0311055 (listing); arXiv:2607.15551 (listing) | As shown |
| C13 | `checks/w2_stuck_states_check.py` → `w2_stuck_states_check_run1.txt`; `checks/w2_grover_sign_diagnostic.py` → `w2_grover_sign_diagnostic.txt` (follow-up) | Run 2026-09-15 |
| — | A2-ledger C42–C44, D7; A4-ledger C87, D32; A5-ledger C24, C31, D10; A6 C3, C4, C7 | Earlier ledgers |
