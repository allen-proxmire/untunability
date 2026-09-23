# On/off loci: working through Allen's picture

*ED_Attempt_03, note 6. 2026-09-15 (RD8, D3, D4). Ledger: C35–C41. Paper and arithmetic only; no model. Allen asked to "poke at it", so the problems get as much space as the fits.*

## Allen's picture

> "ive always thought of loci/commitment as on or off. my body occupies some loci, they are on - committing to other loci that my body is on." (D4)

> "in a discrete picture, gravity doesnt extend forever. there is a floor." (D3)

**The comparison.** Attempt 1 gave each locus a **smooth budget**, U from 0 to 1. Allen's picture is **binary**: a locus is on or off, and commitment is a relation among the on-loci of one body.

## 1. What "on" has to mean (C36)

**First poke: "on" can't mean "full all the time".**
- **The size mismatch.** Attempt 1 tied the budget to gravity, U ≈ GM/(rc²) (A1 C104). A locus that's full all the time then holds about a Planck mass in a Planck volume, roughly 10⁹³ times denser than water.
- **A body at that density.** A 70 kg body holds about 3 × 10⁹ Planck masses, but spreads over about 2 × 10¹⁰³ Planck-sized loci. If "on" meant "full, all the time", almost none of the body's loci could be on.
- **An electron can't even be one full locus.** Its mass is only 4 × 10⁻²³ of a Planck mass.

**What works: "on" is a moment, not a state.**
- **Each tick,** a locus is on or off.
- **A body's mass is how often its loci are on:** an electron's loci are on about once every 2 × 10²² ticks.
- **This matches what attempt 1 already had.** A particle's clock ticks at a rate set by its mass (the Compton clock, A1 C61), with "a pattern holding a full locus ticks once per step" (A1 RD24). Attempt 1's own number for an electron one Planck length away, 4.2 × 10⁻²³ (A1 C104), is exactly this ratio.

**So Allen's picture fits attempt 1's normalization, as long as "on" means "on at this tick".**

## 2. Graded gravity by counting (C36)

**How graded gravity comes from on/off.** If gravity is the influence of on-events reaching a locus, then far away it's the *average* count. That's attempt 1's budget, with mass given by how often loci are on. With attempt 1's spreading rule it gives the 1/r fall-off in three dimensions (A1 C84–C87).

**What this does and doesn't buy.** Counting reproduces weak-field gravity, but it gives **no new weak-field numbers**.

## 3. The floor, poked (C37)

**A hard floor erases ordinary gravity.** Suppose influence below one whole on-event per locus per tick simply doesn't count.
- **At Earth's surface,** Earth's gravity gives about **7 × 10⁻¹⁰** of a count per locus per tick. A hard floor at one count would erase it entirely.
- **Everything measured in gravity is far below one count per locus per tick.** So a hard floor at that level is ruled out by everyday weight.

**What a discrete picture does allow:**
- **Graininess.** Counts come in whole events, but over many ticks the *average* is what clocks and orbits feel. Ordinary clocks see about 10⁴³ ticks per second, so the graininess averages away. There's a floor on single events, not on gravity's average.
- **A very deep floor.** If the floor is "at least one event over the universe's whole history", it sits around 1 in 10⁶¹ (Planck ticks in a Hubble time). That's far below anything measured, so it's consistent but untestable. Gravity must still reach unweakened over at least 10¹⁶ metres (A1 C86, C87).

**So D3 survives only as graininess, or as a floor far too deep to see.** A floor that cuts gravity off at a measurable level doesn't.

## 4. The main finding: on/off gives attempt 1's slowing rules (C38)

**The assumptions, stated plainly:**

| | assumption |
|---|---|
| **O1** | At each tick, a locus is on or off |
| **O2** | A process (a clock tick, a hop) at a locus can happen only if the locus is off at that tick |
| **O3** | Each distant source independently turns the locus on with a small chance u_i, adding up to the gravity field Φ = Σ u_i ≈ GM/(rc²) |
| **O4** | A hop between two loci needs both to be off |

**What follows:**
- **Clocks slow by the chance that no source has turned the locus on:** Π(1 − u_i) = e^(−Φ). The correction is the sum of the *squares* of the individual u_i, which are each tiny (4 × 10⁻²³ for an electron), not Φ². So it's exact for any practical purpose.
- **Motion slows by the square of that,** because a hop needs two loci off (O4): e^(−2Φ).

**These are exactly attempt 1's two matched rules.** Clocks by e^(−U) (A1 RD36) and motion by the square (A1 RD35). Attempt 1 chose them to match Mercury's orbit and light bending, and described e^(−U) as "used budget removes a share of what's left". **On/off gives the reason:** independent claims on a binary locus multiply, and multiplying gives an exponential.

**The pokes:**
- **This doesn't make them more true.** They were picked to match the same data. It turns two chosen rules into consequences of a meaning, which is the kind of progress attempt 3 was looking for, but it's consistency of form, not new evidence.
- **Self-blocking is unresolved.** Does a body's own on-ness block its own ticking? The picture has to say no, and O2 doesn't yet say how.
- **No published derivation of the exponential metric this way turned up.** The Poisson arithmetic itself is standard.

## 5. What "full" means now, and black holes (C39)

**What gets capped changes.**
- **In note 5,** the gravity field U itself was capped at 1. That produced the saturated core with only a factor-e redshift, and it failed the horizon evidence (C33).
- **In the on/off picture,** what can't exceed 1 is **occupancy**: how often a locus is on, 1 − e^(−Φ). That approaches 1 near a dense mass but never passes it. **The field Φ itself has no cap.**

So a full locus (D2) is kept, **but there's no saturated core.**
- **Redshift grows without limit toward the centre,** the case note 5 said could hide energy (C31).
- **For Sgr A*,** loci are literally on every tick only inside a Planck-density region about 7 × 10⁻²¹ m across, where Φ is about 10³⁰. The slowing there is e^(−10³⁰), effectively frozen.

**The pokes:**
- **This came after the strong-field line closed.** Allen's picture came first (D4), but reading "full" as occupancy instead of the field is exactly one of note 5's "what would have to give" items (the meaning of D2). **It can't reopen that line; only a new line with its own exit rule can.**
- **Outside, it's still the exponential metric, so the shadow is still 4.6% larger** (C30): a specific number, now from derived rules, still 1–1.4 standard deviations from Sgr A*.
- **The exponential metric has a contested history** (C35). Yilmaz's theory, which uses it, was sharply criticised as ill-defined and as describing wormholes rather than black holes. Its radiation rate for binary pulsars was never computed. Some authors argue exponential-metric objects are compatible with X-ray nova evidence. That's a proponent claim, not checked here.
- **Whether an uncapped exponential object hides accreted energy well enough isn't computed here.**

## 6. The wall it runs into: what counts as mass (C40)

**The hardest poke comes from attempt 1's own record.**
- **A linear, counting budget fails the post-Newtonian tests whatever it counts** (A1 C207, C208).
- **General relativity needs gravity to feed back on itself** with specific weights: 4 for how sources move, +4 for gravitational energy, 6 for pressure. Simple counting gives 1, −1 and 0.
- **The Moon's orbit shows it.** The Earth–Moon distance would wobble by about 40 m under simple counting. Lunar laser ranging allows about 1 part in 10⁴ of that.
- **Attempt 1 fixed this by adopting GR's weights by hand** (A1 RD37).

**On/off counting is exactly simple counting of sources.** So it explains the *response* side (how things slow, section 4) but **not the *sourcing* side** (what counts toward Φ).

**Unless** on/off supplies gravity's self-feedback. For example, influence passing through loci that are already often on could itself be slowed, which is a built-in nonlinearity. Whether that gives GR's weights is **open**, and it's the question that decides whether this picture is viable.

## What it means (C41)

**Does it throw us off course? No.** It stays on the specificity question, and it gives the most concrete progress of attempt 3:
- **Allen's on/off picture turns two of attempt 1's matched gravity rules into consequences.**
- **It fits attempt 1's mass normalization** when "on" is a tick.
- **It reads "full locus" in a way that avoids the saturated core.**

**But it runs into the same wall attempt 1 hit:**
- **Counting doesn't give gravity's self-feedback,** so the Moon's orbit fails unless GR's weights are added.
- **The floor survives only as graininess** or at an unmeasurably deep level.
- **The black-hole reading stays unchecked,** and has a contested literature.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(u)** | **The deciding question, on paper:** does on/off exclusion (influence slowed by passing through often-on loci) give gravity's self-feedback weights? Work out what it gives for the Nordtvedt combination, with expected results written first | If it can't, the picture explains but isn't viable; if it can, it's the first derived piece of ED's gravity |
| **(v)** | **Record and pause:** add this to the attempt 3 write-up and close the attempt | The picture's value and its wall are both clear |
| **(w)** | **Open a new strong-field line** on the occupancy reading, with its own exit rule | Only after (u); otherwise it risks the rescue the exit rules exist to prevent |

**Proposal: (u).** It decides whether the picture is worth anything more.

**Update:** (u) is done ([Self_Feedback_Question.md](Self_Feedback_Question.md), note 7). On paper, exclusion does not give gravity's self-feedback: it explains the response side, not the sourcing side.

## Correction: a particle is many loci (D5, C45)

**Allen:** "are we making particles on one loci? sounds like that. a particle is many loci."

**He's right; section 1 slipped.** It treated an electron's mass as the on-rate of a single locus, using a point-source number from attempt 1. Attempt 1's patterns spread over many loci.

**With a particle as many loci that are on:**
- **Section 1's "on must be a rare tick" doesn't hold.** Instead, the tie between a locus being on and a full budget in gravity's units (attempt 1's convention) has to break. Each on-locus carries only a tiny share of the particle's gravity: its mass split over all its loci.
- **Section 5's reading of "full" as gravity's occupancy cap doesn't hold.** If every locus inside every body is on, a full locus is ordinary. It reads instead as **matter excluding matter**: something else can't pass through a locus that's already on. That's an impenetrability idea, not a gravity idea, and it's untested.
- **Section 4 mixed two meanings of "on",** and they have to be kept apart:
  - on because a body is there (lasting);
  - on as gravity's influence (small chances from distant sources).

  The e^(−Φ) and square-for-motion result can stand for the second meaning only.

**Unaffected:**
- **Note 5's black-hole conflict:** outside a body, gravity doesn't depend on how the mass is spread.
- **Section 3's floor argument:** it uses the field per locus, not particle size.
- **Note 7's self-feedback result:** it uses smooth densities, and exclusion subtracts either way.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C35 | Criticism of the Yilmaz theory (ill-defined; no black holes; a traversable wormhole instead; radiation rate for binary pulsars not computed), as described in "Is exponential metric a natural space-time metric of Newtonian gravity?" (arXiv:1009.6017) and listings on Yilmaz cosmology; proponent view: "X-ray novae, event horizons and the exponential metric" (arXiv:astro-ph/9710048) | Search listings; original critiques (Misner; Fackerell) not read |
| — | Attempt 1's record: RD23, RD24, RD35–RD37; C61, C84–C87, C104, C200–C208 | Read directly |
| — | Arithmetic: Planck mass 2.18 × 10⁻⁸ kg; electron 4.19 × 10⁻²³ Planck masses; Earth-surface GM/(Rc²) = 6.96 × 10⁻¹⁰; Planck ticks per Hubble time 8.1 × 10⁶⁰; Sgr A* 3.9 × 10⁴⁴ Planck masses, Planck-density radius 7.3 × 10⁻²¹ m, GM/(Rc²) there 8.6 × 10²⁹ | Computed in a scratch script |
