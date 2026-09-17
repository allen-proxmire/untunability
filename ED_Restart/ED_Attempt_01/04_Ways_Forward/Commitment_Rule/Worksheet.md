# Commitment rule: derivation worksheet

*Started 2026-09-13. Revision 6, 2026-09-13: every gap in version 0 is now decided. Draft. Nothing here is a result yet.*

**What still needs your answer is listed in [Open_Items.md](Open_Items.md).**

The goal is a rule a computer can run (Rule 1), built from ED's primitives (route 2 in [../Reinforcement_Rule.md](../Reinforcement_Rule.md)), with every added choice written down.

---

## Ground rules for this derivation (frozen)

1. **Every piece cites its primitive**, quoted from `Paper_087` (the canonical 13), 2026-05-13.
2. **Where the text doesn't settle the maths, that is a gap,** filled only by an explicit decision logged before anything that follows from it is computed.
3. **How a gap gets decided, in this order:**
   1. what the author means;
   2. otherwise, the option that adds the least new structure;
   3. **never** by the behaviour it produces.
4. **Rejected options are kept** for later reruns.
5. **The mirror check:** any choice that treats left and right differently is flagged.
6. **"Derived" means traced, not forced.** The rule's status will be CONDITIONAL on its decisions.
7. **Known physics the rule must pass is written down before the rule exists** (see Tests).

---

## What ED means (the author's definitions)

- **D1. Commitment.** A step that can't be taken back. It is not a record kept anywhere. Loci keep no memory.
- **D2. Waves and chains.** A wave is a pattern before commitment. A chain is a particle: committed, definite, located. The lottery drum.
- **D3. Scaleless**, reconciled with P08 (RD15). Steps exist, but their size in metres isn't fixed; only counts of steps and ticks are real.
- **D4. Local rate and budget.** Everything at a place ticks at about the same rate. A finite budget is used up by mass. Commitments influence neighbours.
- **D5. Entanglement and space** (Allen's current view). An entangled pattern is spread over positions on the graph, so its parts are in space and move apart as measured. It still resolves in one draw, with no signal. The earlier "not in space" reading isn't needed.

---

## Decisions

| gap | decision | ledger |
|---|---|---|
| G1 | Fixed regular lattice, 1D ring, as a test bed only (see T6) | RD13 |
| G2 | A chain is located at each tick; between ticks its content spreads | RD1, RD9 |
| G3 | Channels Internal, Left, Right | RD13 |
| G4 | a = √b e^{iπ} | RD13 |
| G5 | Spreading between ticks is linear and conserving, connection phase 0 | RD13 |
| G6 | A commitment is a tick, triggered by interaction, at a rate set by the environment | RD2 |
| G7 | A draw is in proportion to bandwidth | RD13 |
| G8 | Unselected options go to zero | RD3 |
| G10a | Channels may be shared; no exclusion assumed | RD4 |
| G11 | A wave usually becomes one chain; an entangled pattern resolves as two in one draw | RD5 |
| G12 | Shared contents: amplitudes add | RD6 |
| G13 | The tick rate belongs to the location | RD7 |
| G14 | A substrate step moves waves; a chain's time is its tick count | RD13 |
| G15 | A chain is its sequence of ticks | RD9 |
| G16 | An entangled pattern resolves at the first interaction of any part | RD13 |
| G17 | Mass at a locus = total bandwidth of chains there | RD13 |
| G18 | Budget settings (below) | RD8, **RD14** |
| G19 | Scaleless reconciled with P08 | **RD15** |
| G20 | Amplification | RD10 |
| G21 | Drawn content keeps its phase | RD11 |
| G22 | No extra memory | RD12 |
| G10b | How P12 enters | **version 1** |

---

## Walkthrough 1: the budget settings (RD14)

The budget is the per-locus bound (RD8). Here is each setting, what it means, the pros and cons, and why it was chosen.

### 1. Budget size: B = 1 at every locus
- **Means:** every locus has the same whole budget, and only fractions of it matter ("half used", "a tenth left").
- **Pros:** fits scaleless (RD15). It is a choice of units, not a claim.
- **Cons:** none of substance.

### 2. Tick rate = base rate × share of budget left
- **Means:** p(u) = r₀ × (B − U(u)) / B. Where more budget is used up, fewer ticks happen, never going below zero.
- **Pros:** the simplest form, and it gives the measured direction: fewer ticks near mass (T1).
- **Cons:** "straight proportion" is a choice. Other smooth forms would give different numbers where the budget is nearly used up, as near a black hole.
- **Why it's still the right start:** where only a tiny share is used, as at the Earth's surface, *any* smooth form looks like a straight proportion to first order. Weak-field tests can't tell the forms apart, and strong-field tests can come later.

### 3. Spreading: on
- **Means:** each substrate step, the used budget at a locus is recomputed as the mass sitting there plus a fraction q of the average used budget of its neighbours:

  U_{t+1}(u) = min(B, M_t(u) + q × average of U_t over the neighbours of u), with 0 < q < 1.
- **Why on, and not off, and this is decisive:** with spreading off, used budget exists only where mass sits. A clock 33 cm *above* the mass would feel nothing, and T1 and T3 would fail for every clock not inside the Earth. Spreading off can't match what's measured.
- **Why this form:**
  - **It's local:** each locus only looks at its neighbours.
  - **It spreads at a finite speed,** one step per tick, so influence doesn't jump across the graph instantly.
  - **It's mirror-symmetric:** it treats left and right neighbours alike.
  - **It settles** into a steady profile around a mass instead of growing forever, because q < 1.
- **Cons, stated plainly:**
  - **It adds one number, q.** q near 1 means the influence reaches far; q small means it stays close.
  - **On the 1D ring the profile falls off exponentially,** not like the 1/r of gravity. 1/r needs three dimensions (C54), so T3 can't be tested on the ring.
  - **A 1/r falloff in 3D would be expected from almost any spreading** (Rule 4), so getting it there would be a requirement met, not evidence.

### 4. The base rate r₀: an explicit free number
- **Means:** r₀ is not given a value. Every result is reported for a range of r₀ (and of q).
- **Pros:** it is honest. r₀ is the per-part scale ED doesn't yet fix (C50). Picking one value quietly would be Rule 5's "settings as laws".
- **Cons:** results come as families of curves, not single answers.

### The count, stated plainly (C51)
Version 0 has **two free numbers, r₀ and q. GRW also has two** (its rate λ and its width r_C). ED only earns something GRW doesn't have if the budget or the graph ends up *fixing* one of them. That is the question to keep in view.

### Two small details, by least structure (Allen can veto)
- **A spread-out part's tick probability** is the average of p over the loci it covers, weighted by its bandwidth there.
- **A hinged pattern ticks if any of its parts triggers:** probability 1 − the product of (1 − p) over its parts. For small p that is about N × p, which is amplification (RD10).

---

## Walkthrough 2: scaleless against P08 (RD15)

- **What P08 says:** the substrate has a characteristic edge length, a smallest scale.
- **What you mean by scaleless:** the substrate has no built-in size.
- **The reconciliation:** both hold if **steps exist, but their size in metres isn't fixed.** The substrate knows "three steps away" and "five ticks later". It doesn't know "three metres" or "five seconds".
- **What that means in practice.**
  - **Everything the rule outputs is a count or a ratio.** How many ticks, what fraction of budget, how many steps.
  - **To compare with experiment,** one conversion has to be measured once, the way picking units works. After that, ED predicts dimensionless ratios.
  - **This is why r₀ and q are pure numbers,** with no seconds or metres attached.
- **What it does not do (C53):** it doesn't remove the preferred-frame problem (T6). That problem comes from the *structure* of the neighbours (which directions exist on the graph), not from how big a step is. A scaleless grid still has its grid directions.

---

## Allen on entanglement and space (D5)

**Allen's point.** He kept ED a scaleless relational graph because of the preferred-frame problem. Entanglement relied on the pattern being "not in space or time", so it could resolve with no signal. But the "not in space" reading may not be wholly needed, because measurements show the particles moving apart in space as they should.

**Claude's view: agreed. "Not in space" isn't needed.**
- **No-signal resolution doesn't require the pattern to be outside space.** In standard quantum mechanics and in collapse models, entangled particles are in space. The resolution is nonlocal, yet it can't be used to send a signal (C52), and a relativistic collapse model does this without any preferred slicing of space-time (C42).
- **In this rule an entangled pattern is spread over graph positions,** and one draw resolves both parts at once. That matches the particles being where they're measured to be.
- **"Space emerges from events" still fits:** the graph is what space is made of, and patterns live on it.

**Crank-safety note.** A nonlocal resolution is exactly the kind of place where a rule can accidentally allow signalling, so **no-signalling is now test T7.**

---

## Tests the rule must pass (written before the rule exists)

| test | known fact | what the rule must do | where it can be tested | ledger |
|---|---|---|---|---|
| **T1** | A clock lower in gravity runs slower | Fewer ticks near more mass | Direction: 1D ring. Size: 3D | C35, C38 |
| **T2** | Mirror check | No left–right preference in the rules | 1D ring | handedness result |
| **T3** | Size and falloff | g·Δh/c² ≈ 3.6 × 10⁻¹⁷ for 33 cm; Newtonian falloff | 3D only (C54) | C35, C38 |
| **T4** | Once-localized particles interfere later | Enough spreading between ticks for interference | 1D ring (qualitatively) | C39 |
| **T5** | Collapse rates are limited by experiment | r₀, q and amplification must respect existing bounds | Needs units, so needs a conversion (RD15) | C43, C45 |
| **T6** | No preferred frame is observed | The graph must not pick out a frame at testable levels | Not on a lattice; a separate question | C48, C53 |
| **T7** | No signalling | Entangled resolution must not let one side's choices change the other side's statistics | 1D ring, with a two-part pattern | C52 |

---

## Rule version 0 (every gap decided)

```
PARAMETERS (explicit free numbers)
  r0  base tick rate per part, per substrate step                     [RD14]
  q   spreading factor, 0 < q < 1                                      [RD14]

STATE  (1D ring of L loci; channels Internal, Left, Right)             [RD13]
  wave  : amplitudes a[u, K] = sqrt(b) exp(i pi) over loci and channels [RD13, RD5]
          an entangled wave is one pattern over several parts          [RD5, D5]
  chain : the sequence of its ticks; its content spreads between ticks [RD9]
  U[u]  : used budget at each locus, B = 1                              [RD8, RD14]

SUBSTRATE STEP  t -> t+1                                                [RD13]
  1. spread all content: linear, conserving, connection phase 0        [RD13]
     shared channels: amplitudes add                                    [RD6]
  2. mass M[u] = total bandwidth of chains at u                        [RD13]
     U[u] <- min(1, M[u] + q * average of U over neighbours of u)       [RD14]
  3. per-part tick probability at u:  p[u] = r0 * (1 - U[u]), >= 0      [RD14]
     a part's p = bandwidth-weighted average of p over its loci        [RD14]
     a pattern ticks with probability 1 - product over parts (1 - p)   [RD10, RD14]
  4. if a pattern ticks:
       a. draw one option (locus, channel), probability proportional to b [RD13]
          an entangled pattern draws one joint outcome for all parts   [RD5, RD13]
       b. every other option goes to zero                               [RD3]
       c. the drawn content keeps its phase                             [RD11]
       d. a wave becomes a chain (or chains)                            [RD5]
       e. the chain spreads again from where it was drawn               [RD9]
     no other memory                                                     [RD12]
  5. P12 feedback: version 1                                            [G10b]

MIRROR CHECK (T2): left and right treated identically at every step
```

---

## Literature gate result (2026-09-13)

Full report: [Literature_Gate_v0.md](Literature_Gate_v0.md).

- **Known in its main parts.** GRW flash collapse, amplification, gravity-linked collapse, time-dilation decoherence and realistic-clock decoherence are all published.
- **The budget's clock effect adds no new prediction in weak gravity** (C59). If it matches measured clocks, it *is* time dilation, which collapse models already have. It remains an explanation of why time dilation happens. ED-specific content could come from the budget fixing r₀ or q, from strong gravity, or from the handedness question.
- **A conflict was found** (C60). A lone particle's clock can't be its count of collapse ticks: it must collapse rarely to interfere, collapse rates are bounded by experiment, and yet lone muons age at exactly the relativistic rate. That adds **test T8** and **gap G23**.

### T8 — isolated particles age by proper time
Muons at γ = 29.33 lived as long as special relativity predicts, to 2 parts in 1000 (C58). Any rule must let a lone particle's internal evolution run at its proper-time rate, independent of how rarely it collapses.

### G23 — what does the budget slow down? — needs Allen
**Proposal:** the local rate factor slows **every** process at a place (spreading, internal evolution and collapses together), so clocks of every size agree.
- **Big hinged things** (clocks, the Earth) tick constantly, so for them "commitment is the tick" still holds.
- **A lone particle's clock** runs through its spreading and internal evolution between its rare ticks.
- **RD9 stands:** a chain is still its history of ticks.
- **G14 changes:** a chain's own time is the locally slowed substrate time it lives through, and its ticks are events in that time.

## Round 7 (2026-09-13): Allen on lone particles, muons and G23

### G23 decided (RD16)
**Allen:** every clock 100 km from a black hole has the same tick rate, because the budget at 100 km is the same.

**Yes, that is the proposal.** Same place, same budget left, so the same rate for *every* process there, big or small: collapses, spreading and internal change like decay all slow together. The Earth draws down commitment on a gradient, so clocks on the ground run slower than clocks above.

### A correction to the gate report: the muon test is about *speed*, not gravity
The CERN muons (C58) lived longer because they were **moving fast** (γ = 29.33), not because they sat in a gravity well. So the budget (a gravity effect) doesn't explain them. ED needs a second slowing: **moving clocks run slower** (G25).

### D6. When lone particles collapse (Allen)
A lone particle collapses when it interacts with the real world. There may be an **interaction cost** that makes that less likely (a new idea, not yet in the rule).

**The catch to watch.** D4 says everything interacts with gravity through the budget. If that ever-present gravity counted as "interacting with the real world", every lone particle would collapse constantly and nothing could interfere (T4). So one of these has to hold:
- the budget background does **not** count as an interaction that triggers a draw; or
- Allen's interaction cost makes those draws rare.

### Allen's point: muons *are* committing
> How else would they decay, have mass, or go slower than c?

**What standard physics says.** A muon decays, has mass and moves slower than light *without* collapsing. Decay is its amplitude to still be a muon shrinking over time. Mass and the speed limit are in its equation of motion. Collapse only happens when its decay products are detected.

**But Allen's instinct has a precise, published form.** A particle of mass m carries an internal "clock" that ticks at its **Compton frequency**, mc²/ħ, and that ticking can be used as a real clock (Lan et al., *Science*, 2013; C61). That is about 1.6 × 10²³ radians per second for a muon, and about 7.8 × 10²⁰ for an electron. So "every massive particle is ticking, and its mass *is* its tick rate" is a respectable idea. Whether atom interferometers really test gravity's effect on that clock is debated (Wolf et al., 2011; C62).

**The key point for the rule.** Those Compton ticks happen constantly, yet electrons and C60 still interfere. So they **cannot** be lottery draws that zero out the other options. That suggests two kinds of tick.

### G24 — are there two kinds of tick? — needs Allen
- **(a) Clock ticks.** Every chain ticks steadily at a rate set by its mass (its own time), slowed by the local budget (RD16) and by speed (G25). These **don't** zero out options, so interference survives. This is where decay, mass and "slower than c" live.
- **(b) Draws.** A tick that also selects one option and zeroes the rest (the lottery drum, RD3). These are triggered by interaction with the real world (D6), and rarely for a lone particle.

**Proposal: (a) and (b) both exist.** "Commitment is the tick" then holds for clock ticks. The lottery draw is the special tick that happens on interaction.

### G25 — why do moving clocks run slower? — needs Allen
**An idea in the spirit of D4:** a chain's own commitment is shared between *moving* and *internal ticking*. The faster it moves through the substrate, the less is left for its internal clock. At light speed, none is left: no ticking, no mass.

This is a well-known popular picture ("everything moves through spacetime at c"), not a derivation. To pass T8 it must give exactly √(1 − v²/c²), which is where the muon measurement is tight to 2 parts in 1000.

### T8, restated
Isolated unstable particles age at their **proper-time** rate, including the slowing from speed (muons, C58), whether or not they undergo draws.

## Round 8 (2026-09-13): mass, moving clocks and a spreading limit

### Decided
- **D7.** Mass is concentrated commitment ("mass without mass"). Every particle has a clock, or it wouldn't be a particle.
- **RD17 (G25).** A moving chain spends commitment on moving, leaving less for ticking, so moving clocks run slower.
- **RD18 (G24).** Two kinds of tick. **Clock ticks:** every chain has them, set by its mass and slowed by budget and motion; they don't zero out options. **Draws:** they pick one option, and are triggered by interaction.

### The split has to be Pythagorean (C63)
"Less left for ticking" has to come out as a specific amount, and the muons decide which:

| how commitment is shared | muons at γ = 29.33 should live longer by | measured |
|---|---|---|
| Straight subtraction: tick share = 1 − v/c | 1720 times | **29.33 times** |
| Pythagorean: (tick share)² + (v/c)² = 1 | 29.33 times | **29.33 times** |

- **Only the Pythagorean split works.** It is special relativity's own formula, so matching it is a *requirement*, not a derivation.
- **Why ED's commitment would split that way is open (G26).** The old corpus's "c − k" slowing was a straight subtraction, so it had the wrong form.

### One wording to drop (C67)
"A fast muon is spread out, not concentrated" doesn't fit relativity. A moving thing is *shorter* along its motion and carries *more* energy, and its rest mass doesn't change. "It spends commitment on moving" says what's needed without that conflict.

### G27 — a spreading limit that forces a recommit (Allen's new idea)
**The idea:** a wave can only spread so far before it has to recommit.

**Literature.**
- **It has a close published relative:** Károlyházy's model (1966) gives each object a *coherence length*, set by its mass, beyond which it can't stay spread out, with no free parameters (C64).
- **Experiments bound it:** atoms have interfered with their two halves 54 cm apart, for about a second (C65).
- **The same family is already being cut down.** A generalized version of Károlyházy's model was excluded by an underground radiation measurement at Gran Sasso (2026 preprint, C68). Any ED spreading limit will face that kind of test.

**For ED:**
- **This could answer D6** (what triggers a draw for a lone particle) without making the gravity budget trigger draws everywhere.
- **Whatever the limit is, it must let an atom spread over more than half a metre** (test T9).
- **If ED could get the limit from the per-locus budget** (a pattern spread too thin over too many loci), that would be a number from ED itself rather than a chosen one, which is exactly the kind of thing C50 asks for.

### T9 — atoms stay coherent over 54 cm
Any spreading limit or draw trigger must allow atom wave packets 54 cm apart to interfere after about 1 second (C65).

### G27 decided (RD19)
**Yes.** A lone particle's draw is triggered when its pattern is spread too thin over too many loci, with the limit coming from the per-locus budget. The gravity budget itself doesn't trigger draws.

**What this adds to the rule** (C75).
- **A lone pattern draws when its largest per-locus share falls below a smallest share, b_min.**
- **Until the budget is shown to fix it, b_min is a third free number,** alongside r₀ and q. GRW has two, so ED has to *reduce* this count to earn anything of its own.
- **T9 applies:** b_min must allow atom wave packets 54 cm apart. That can only be checked once steps are converted to metres (RD15).

## Version 0 built and run (2026-09-13)

- **G28 decided (RD20):** option (a).
- **G29 decided (RD21):** loci are still being born today.
- **Version 0** is in [v0/](v0/): the rule, the tests, a spec frozen before running, and [v0/Results.md](v0/Results.md).

**Results in one line each:**
- **Mirror check:** passes.
- **Budget:** falls off exactly as calculated.
- **Interference:** a lone pattern interferes more the further it spreads before drawing.
- **No signalling:** RD5 read literally *fails*; a draw that fixes only the interacting part passes.

Every frozen prediction came out as predicted.

### G31 decided (RD22)
An entangled pattern's draw fixes only the part that interacts. The other parts become definite through correlation when they interact. This replaces RD5's "resolves as two chains in a single draw" and G16's "resolves at the first interaction of any part". Fixing all parts at once lets Alice signal Bob faster than light (C81).

### V0-D1 — the coin — Allen can veto
Version 0 uses the Grover coin, chosen by least structure. With it, a lone pattern's largest share never drops below about 0.13 (known three-state trapping, C77), so any "too thin" limit below that means a lone particle never draws by thinness. Whether that trapping belongs to ED or only to this coin is worth knowing before RD19's limit is tied to anything physical.

## Round 9 (2026-09-13): what counts as an interaction (G35)

Full note: [Interaction.md](Interaction.md).

- **Experiments show meetings hinge rather than draw:** crossing light, two-photon interference, photons made to interact, colliding atoms, single-photon exchange with a cavity (C114).
- **Interference is lost smoothly with a distinguishing mark left elsewhere** (D² + V² ≤ 1). Where the draw then happens can't be seen from one side; erasers fit RD22 and D1 (C115).
- **G35 splits:**
  - **G35a** (which meetings count) is settled by experiment.
  - **G35b** (what turns a hinge into a draw) is the measurement problem (C119).
- **Options for G35b:**
  - unit handover: ruled out (C116);
  - full budget: ruled out as the everyday trigger (C104, C117);
  - relative draws: conflict with D1 (C118);
  - **proposed: a draw when a mark can no longer be brought back together,** which needs an exact meaning (G36).

### G35 decided (RD27, RD28)
- **G35a (RD27):** patterns that meet hinge; a meeting by itself never draws.
- **G35b (RD28):** a draw happens when a meeting leaves a mark that can no longer be brought back together. Its exact meaning is open (G36).
- **Allen's term "forced commitment" is kept (D10)** with one condition: the meeting leaves a distinguishing mark in the committed world that can't be brought back (C124).
- **G36 first literature pass:** the horizon idea is known in part (Bousso–Susskind), with a risk. In a finite region, irreversibility is only approximate (C125).

## Version 1 built and run (2026-09-13)

Code in [v1/](v1/), with a spec frozen before running and [v1/Results.md](v1/Results.md).

- **No spontaneous draws; meetings hinge; draws only at a detector; local draw.**
- **All 15 tests pass, as predicted:**
  - Partial marks give partial fringes, following Englert's D² + V² ≤ 1 (C127).
  - The eraser works by sorting, and nothing is undone (C128).
  - A mark can be undone before a draw, but not after (C129).
- **Bottom line (C130):** for measurement, ED reproduces standard quantum physics. A requirement met, not evidence.
- **D10's wording is confirmed by Allen:** "mark" is what he meant by "consequence".

## Round 10 (2026-09-13): locus birth

Full note: [../Locus_Birth.md](../Locus_Birth.md).

- **Budget pile-up (C91).** Locus birth resolves it in principle: birth dilutes, and growth faster than spreading lets the budget settle (C131). It isn't urgent for a universe of the observed size (C136).
- **Observations.**
  - Bound systems don't expand (C133).
  - "Space being created" is one reading, not forced (C134).
  - Expansion accelerates (C140).
  - Dark energy may change over time, a hint only (C139).
- **The attachment rule decides whether space stays 3D** (C135, C145).
- **Exact draws face a horizon and entropy-bound tension** (C143).
- **Options for Allen:**
  - **G29b:** (ii) the same small birth chance everywhere (one new number), or (i) commitments make loci.
  - **G30:** (A) local splitting, checked first.
  - **G36:** keep exact as the aim.

### Round 10 decisions and the splitting check (2026-09-13)
- **Decided:**
  - **RD29:** the same tiny birth chance at every locus. One free number (C155).
  - **RD31:** keep exact draws as the aim.
  - **RD30:** local splitting, provisionally. Allen wasn't sure.
- **The dimension check:** none of three readings of local splitting keeps space 3D (C147–C149). They make it stringy, crumpled or a clump. The literature agrees: known programs need a global ingredient to recover dimension (C154).
- **G30 is reopened.**

### Round 11 (2026-09-13): horizon births, Allen's 3D ideas, (B) and (C)
Full note: [../Geometry_B_vs_C.md](../Geometry_B_vs_C.md).
- **Births located at the horizon** pick out a preferred place. A horizon count setting the overall rate is published, and could fix RD29's number, but it competes with exact draws (C158).
- **Allen's 3D ideas (D11):**
  - Knotting only in 3D is correct.
  - "Ordered" is close to Tegmark's argument.
  - With C84 they form a pincer on 3, not a derivation (C162).
- **(C) fits ED better than (B),** but it makes links impermanent and hasn't given clean 3D in the literature (C168).

### Round 12 (2026-09-13): the edge of the record, G30 = (C), first rewiring test
Full note: [../Edge_And_Rewiring.md](../Edge_And_Rewiring.md).
- **Allen (D12):** the horizon is the edge of what's committed, and committed loci don't create loci. G29b is open again (C175).
- **Reading the edge:** an edge in space is heavily constrained by the data; an edge in time (the present) fits (C173).
- **G30 = (C) (RD32):** links rewire; loci are the lasting record.
- **First rewiring test:**
  - "Favour squares" shatters (C176).
  - "Squares like a lattice" gives connected, glass-like near-3D space, but it is 35% too compact (C177).
  - Next candidate: growth from a seed (C178).

### Round 13 (2026-09-13): even births kept; looking for a preference inside ED
Full note: [../Preference.md](../Preference.md).
- **Even births:** Allen keeps them (RD29 stands).
- **ED has no preference Allen knows of (D13).** With no preference, rewiring gives a random tangle (C182).
- **Inside ED's primitives:**
  - P06 (3D) could be imposed.
  - P12 (Σ = Coh − Str − Grad) is the only score.
  - Uniformity alone allows any whole-number dimension (C179).
- **Proposal C184:** P12 as the links' preference:
  - strain = link load against the bandwidth bound;
  - gradient = difference from neighbours;
  - coherence = phases closing around small loops, like Wilson's lattice action.

### Round 14 (2026-09-13): the P12 growth test
- **Allen accepted the P12 reading (RD33).**
- **Test result:** seeded growth with even births and P12-driven rewiring came out connected and glass-like, but with about 4–5 dimensions, not 3 (C185).
- **Leaving out one part barely mattered** (C186).
- **Reading:** at these settings P12 isn't shaping space (C187).

### Round 15 (2026-09-13): the scan fails; P06 imposed
- **Pre-registered scan:** no cell of 27 came out 3D (C188). Growth dimension 3.9–5.2.
- **By Allen's prior decision, P06 is imposed (RD34):** space is 3D by assumption. RD32 and RD33 are parked (C189).

### Round 16 (2026-09-13): stock take; the budget slows spreading
- **Stock take:** [../../Stock_Take.md](../../Stock_Take.md).
- **Budget slows spreading, built** ([v1_budget/](v1_budget/)). Two effects:
  - lingering: every pattern drifts toward the mass;
  - pull: massive-like patterns fall, if commitment is positive.
  - Two frozen predictions were wrong, then explained (C193, C194).
- **Light bending:** one slowing factor for everything is time-only and gives half the measured bending, so RD16 as the whole story is ruled out (C196). New gap G37; proposal: crossing between loci pays s², ticking pays s (C198).

### Round 17 (2026-09-14): G37 decided (RD35); Mercury (G38)
- **RD35:** ticking slows by s, moving between loci by s². Implemented and checked (C199). Light bending is now matched at first order, and massive patterns still fall. One frozen prediction was wrong (M3).
- **Second order:** ED's linear rate 1 − U gives β = 1/2, which Mercury's perihelion rules out (C201). A rate e^(−U) gives β = 1.

### Round 18 (2026-09-14): G38 decided (RD36)
- **RD36:** the rate is e^(−U), and moving slows by e^(−2U). Mercury's β = 1 is matched at second order (C203). The slowed generator is checked (C202).
- **Gravity side so far:**
  - patterns fall (C194);
  - light bending is matched (RD35);
  - Mercury is matched (RD36).
  - All are matched to measurement, none predicted.

### Round 19 (2026-09-14): the Nordtvedt check
- **A linear budget fails lunar laser ranging by about 10⁴** (a 37–44 m Earth–Moon wobble against about 1 cm measured). It also fails binary pulsar bounds (C207).
- **Passing needs the budget to feed back on itself with GR's weights** (C208). New gap G39; proposal (a).
- **Pattern:** every gravity fix matches a measurement. ED's gravity converges on GR.

### Round 20 (2026-09-14): G39 decided (RD37); locus birth and dark energy
- **RD37:** ED's gravity is GR in budget language.
- **Constant births (RD29):** exactly constant dark energy, from a tiny unexplained birth chance, about 2.9 × 10⁻⁶¹ per Planck step (C211).
- **Everpresent Λ** (causal sets) gets the right size without tuning; its data tests are mixed (C210).
- **ED twist:** loci persist, so births can't go negative. ED's version would be one-sided: dark energy that changes but is never negative (C213).
- **G40 options** (C214). Proposal: (b), one-sided fluctuating births.

### Round 21 (2026-09-14): G40 decided (RD38); one-sided against two-sided
- **Toy comparison** (C216): the two-sided version crashes at the strength that matters. The one-sided versions never crash and sometimes give today's universe.
- **Among universes like today** (C217):
  - **Reflecting** always has too much early dark energy, so it is ruled out.
  - **Clipped** has no early problem in half its runs, but its dark energy usually changed by a factor of about 2 since z = 1.
- **Two mistakes of mine, recorded:**
  - run 1 had an integration bug;
  - P1 came from a misread summary (the published figure is 5%, not 53%).
- **G41 proposal:** test the clipped form's today-like runs against real distance data.

### Round 22 (2026-09-14): the distance-data test
- **DESI DR2 BAO:** constant dark energy fits (χ² 14.3). No clipped one-sided universe like today comes within Δχ² 77 (C221).
- **Why:** everpresent dark energy tracks the total density back in time (C222).
- **Result:** the one-sided everpresent form is ruled out. G42 proposal: return to constant births (C223).
- **Big picture:** gravity and dark energy have both returned to standard physics.

### Round 23 (2026-09-14): G42 decided (RD40); audit
- **RD40:** back to constant births.
- **Audit** ([../../Audit.md](../../Audit.md)):
  - which decisions are forced, safe to adjust, unsure or ruled out;
  - Allen's ideas weighed;
  - the ED-I folder is mostly relabelling, with contradicted claims;
  - the handedness theorem against parity violation is the main lead;
  - the Λ thought is the critical density, with a holographic reading that has a published home.

### Round 24 (2026-09-14): handedness line started; horizon-births test
- **Handedness** ([../Handedness_Weak_Force.md](../Handedness_Weak_Force.md)): irreversibility permits handedness, and mirror symmetry blocks it (C241). G43 proposal: spontaneous handedness.
- **Horizon-set births:** as good as constant dark energy on DESI BAO, not better; c ≈ 0.93 replaces the tiny number (C242, C243). G44 open.

### Round 25 (2026-09-14): G43, G44 decided; both tests run; seed crystal
- **Horizon-set births** with supernovae and the CMB: disfavoured (Δχ² +32.8), because BAO and the CMB want different matter densities (C246, C249, C250). G45 proposal: back to constant births.
- **Handedness toy:** a mirror-symmetric, irreversible rule picks a hand, set by the seed's direction; no threshold, and small seeds are slow (C248, C251).
- **Allen's seed crystal (D15):** fits Sakharov's equilibrium condition and the spontaneous choice; ED has no baryon number yet; one choice for the whole visible universe is required (C252–C258). G46 proposal (c).

### Round 26 (2026-09-14): G45, G46 decided; local toy; uniformity
- **RD43:** constant births. **RD44:** local toy run, baryogenesis parked.
- **Local toy:** hands form everywhere and merge; one seed decides only a region in contact; locked-in hands resist an opposite seed (C263, C267, C268). G47 proposal (c).
- **Allen's uniformity note (D16):** homes in Hegel, the Past Hypothesis and CCC; his CCC paper's uniqueness argument carries over as an idea; entropy is the main tension (C259–C261, C265, C266).

### Round 27 (2026-09-14): G47 decided (RD45); feedback in the real rule
- **Finding:** the real rule's spreading is Hermitian, so feedback that keeps it Hermitian can't give winding (C269); C32 is the real question.
- **Options (G48):** phase feedback, one-way hops, feedback at commitment, P12 steering (C271). Proposal: at commitment.

### Round 28 (2026-09-14): G48 decided (RD46); version 2 built and run
- **Version 2:** spreading and draws on one ring, draw rates set by the local flow. All ten frozen predictions right (C275).
- **Finding:** draws only mix, so flow dies; the real rule's two-way hops block winding for any draw rates; lane phases unlock it (C277).
- **G49 proposal:** version 2b with flow-set lane phases and non-unital draws.

### Round 29 (2026-09-14): G49 decided (RD47); version 2b built and run
- **Version 2b:** phases as the arrow of time, set by the flow's size; draws carry motion into committed matter.
- **Result:** no lasting flow in any run, including a constant phase. Purity rises, so the new draws work (C278).
- **Mirror mismatch:** the flow-set phase law amplifies rounding; the code itself is symmetric (C279).
- **G50 proposal:** a gain check, then work out the draw (G36), with outside review alongside (C280).

### Round 30 (2026-09-14): G50 decided (RD48); gain check
- **Response to a draw-rate difference:** clean with a phase (0.012–0.096); zero with no phase, which has 13 steady states (C281, C282).
- **Version 2b's loop gain was 0.32,** which is why its flows died.
- **Door not shut:** a hand needs a standing phase, draws that carry motion off, and a steep rate law (C283). G51 proposal (c).

### Round 31 (2026-09-14): G51 decided (RD49); tuned test; the draw
- **Tuned test** (standing phase, steep rate law, labelled tuned) started with frozen predictions.
- **The draw:** six loose points listed (C286). Candidate meanings: horizon, redundancy, budget (C287). A permanent horizon's capacity, 10¹²², sets how exact draws can be. G52 proposal (d).

### Round 32 (2026-09-14): G52 decided (RD50); tuned test result
- **RD50:** 'can't be brought back' means out of reach of every future path; exact up to the horizon's capacity; redundancy in simulations.
- **Tuned test:** all eight predictions right. A lasting handed flow with nonzero winding, hand chosen by chance, for the amplifying sign only (C288).
- **Reading:** the rule can be handed under three choices of ours; re-check with the rebuilt draw (C289).

### Round 33 (2026-09-14): the draw rebuilt
- **Rebuilt draw (RD50):** fragments with state, meetings as marks, a draw that fixes only the record, redundancy as the stand-in. All ten frozen predictions right on run 2; run 1's two misses were a harness bug (C291).
- **Settled:** trigger, content, tracked mark. **Open:** probabilities, budget, the stand-in's erasure limit (C292).
- **D18 (Allen's sidebar):** the standing phase is a small-loop phase that P12's coherence part scores, but a Wilson-form coherence prefers flux 0, which would remove the hand (C290).

### Round 34 (2026-09-14): consolidation and version 4
- **Consolidation (RD51):** Stock_Take refreshed; Audit section 7; review packet ready (not sent).
- **Version 4:** all nine predictions right. The rebuilt draw with transfer meetings equals version 2b's jumps; finality doesn't matter for population behaviour; the tuned hand survives run for run (C293).
- **End point of the handedness line:** ED can hold a chance-chosen hand but doesn't say why (C294). G54: the main line and an exit rule.

### Round 35 (2026-09-14): G54 decided (RD52); standing phase attempt 1
- **Literature:** mass as a quarter-turn phase puts lane loops at π (no hand); frustrated phase models pick a chirality by chance (C295).
- **Attempt 1:** coherence as read fixes every small-loop phase at 0; no hand (C296). 1 of 3 attempts used.
- **Lead:** a π-preferring coherence is frustrated in 3D and its ground state carries mirror- and time-reversal-odd mixing phases, chosen by chance (C297, C298).

### Round 36 (2026-09-14): G55 decided (RD53); standing phase attempt 2
- **Attempt 2 (frustration route):** the chosen mixing chirality gives no lasting flow; every steady state carries zero flow (C299, C300).
- **Lesson:** the hand needs a phase on the lane loop itself; 2 of 3 attempts used (C301).

### Round 37 (2026-09-14): G56 decided (RD54); attempt 3; exit rule reached
- **Attempt 3 (longer loops):** squares are frustrated under the π reading, but lane loops stay at ±π at every weight; Wilson stays at 0 (C302).
- **Exit rule reached:** three frozen attempts, three failures; ED doesn't fix the ingredient its hand needs (C303). G57 proposal: write ED up as an interpretation.

### Round 38 (2026-09-14): exit rule confirmed (RD55); write-up
- **Allen:** yes to the exit rule; write ED up as an interpretation.
- **Draft 1:** `06_Write_Up/ED_Interpretation_Draft1.md` (summary, the rule, what it reproduces, the theorem and A5, the three attempts, negative results, neighbours, open problems, method, what would reopen ED).

## Recommended step

Allen reviews draft 1 and decides on the review packet.
