# Can on/off loci make gravity feed back on itself?

*ED_Attempt_03, note 7. 2026-09-15 (RD9). Ledger: C42–C44. On paper: reasoning and algebra, with a small script only to double-check the arithmetic (`checks/feedback_weights_check.py`, expected results written first). Nothing about ED was simulated.*

## The question (from note 6)

Allen's on/off picture explains **how things slow down** near mass: two of attempt 1's matched rules follow from it (C38).

**But gravity also has to feed back on itself.** In general relativity, three things make gravity slightly stronger than plain mass alone, with specific weights:
- a source's **motion**;
- its **pressure**;
- the **energy of gravity itself**.

Attempt 1 showed that simple counting misses these weights, and the Moon's orbit then fails the Nordtvedt test by more than 10,000 times (A1 C207, C208). **Can on/off exclusion supply the weights instead of adding them by hand?**

## What exclusion can do

In the on/off picture, a process can only happen at a locus that's off. That gives exactly two natural ways for gravity to act back on itself.

| channel | what it means | effect |
|---|---|---|
| **F1** | Influence spreading through loci gets slowed, the way motion does | Changes how gravity falls off with distance |
| **F2** | A source's own on-ticks get slowed: by its own gravity, and by its motion (moving clocks tick slower) | Changes how much a source counts |

## What the algebra gives (C42)

*All six expected results held.*

**F1: slowing the spread breaks Mercury.**

| how influence spreads | β (Mercury parameter) | Mercury's perihelion vs GR |
|---|---|---|
| Slowed like motion (e^(−2Φ)) | **0** | **4/3** |
| Slowed once (e^(−Φ)) | **½** | **7/6** |
| Not slowed | **1** | 1 |

- **Mercury needs β = 1,** to better than 1 part in 10,000 (A1 C200).
- **On/off already gets β = 1 from how things slow down** (note 6), but only if the influence itself spreads unslowed. Slow the spread too, and the same picture breaks the result it just explained.
- **So F1 is out.**

**F2: slowing a source's on-ticks makes things worse.**

| case | how gravity's energy counts (ζ2) | how motion counts (ζ1) | Nordtvedt number |
|---|---|---|---|
| General relativity | 0 | 0 | **0** |
| Attempt 1, rest mass only | −2 | −4 | 10/3 |
| Attempt 1, all commitment counted | −2.5 | −3 | 17/6 |
| **On/off, on-ticks slowed** | **−3** | **−5** | **13/3** |

- **F2 moves every number further from general relativity.** The Moon's orbit allows the Nordtvedt number to be about 0 ± 0.0005.
- **The script reproduces attempt 1's two earlier cases exactly,** so the bookkeeping matches.

## Why it fails (C43)

- **Exclusion blocks; general relativity's feedback adds.** Everything on/off exclusion does is *subtractive*: fewer ticks, slower spread, less counted. In general relativity a source's motion, its pressure and gravity's own energy all make gravity *stronger*. **A blocking mechanism can't produce an adding effect.**
- **The one channel not ruled out.** Allen's picture has a second half: on-loci **commit to other on-loci of the same body.** If those relations count as sources, they're relational by nature, as motion, pressure and binding are. Relations could in principle *add*.
  - **Nothing here works that out.** It isn't obvious which sign or size the weights would come out with.
  - **The hazard:** for it to work, the weights would have to come out exactly as general relativity's. Choosing a counting rule to hit them would be matching again, not deriving.

## What it means (C44)

**On paper, on/off exclusion doesn't give gravity its self-feedback.**
- **Slowing the spread** breaks Mercury.
- **Slowing the sources** pushes the Moon test further from passing.

**So the on/off picture is half a success:**
- **It explains the response side:** how clocks and motion slow, and why "full" is occupancy.
- **It doesn't explain the sourcing side:** what makes gravity. For that, ED still needs general relativity's weights added by hand, as attempt 1 did.

**For the specificity search, the pattern holds.** ED's own meanings can turn some matched rules into consequences, but they haven't produced the numbers physics needs on their own.

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(v)** | **Close attempt 3:** update the write-up with notes 6–7 and conclude, as attempts 1 and 2 were | The specificity search and the on/off picture both have clear answers |
| **(x)** | **Relations as sources, on paper:** work out what counting a body's commitments between its on-loci gives for the weights, with expected results written first, and a stated rule that choosing the counting to hit GR's weights doesn't count | The one channel not ruled out; high risk of matching |

**Proposal: (v).** (x) stays recorded as open, but chasing it now risks turning a clean negative into another round of fitting.
