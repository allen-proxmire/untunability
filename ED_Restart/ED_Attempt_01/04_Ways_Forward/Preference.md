# What would links prefer? Looking inside ED for a preference

*2026-09-13. Follows [Edge_And_Rewiring.md](Edge_And_Rewiring.md). Ledger: D12, D13, RD29, C179–C184.*

## Settled first: births stay even everywhere (RD29)

Allen meant an edge in space. After talking it through, he finds births spread evenly everywhere the better fit. **RD29 stands**, with its one free number, the birth chance.

---

## The problem

**Allen (D13):** "ED doesn't have a preference that I know of."

**That matters, because option (C) needs one.**
- **If links let go and re-grab with no preference at all,** they just wander.
- **A network whose links wander at random ends up a random tangle.** Random networks where every locus has the same number of links are known to be "expanders": everything is a few steps from everything else (C180). That is the opposite of space.
- **So "no preference" gives no geometry** (C182).

## What ED already has that could act as a preference

Going back through the 13 primitives turned up more than expected (C183).

| ED piece | what it says | could it steer links? |
|---|---|---|
| **P06** | Space has three dimensions, plus one of time | **Directly.** Links could settle toward whatever looks 3D. But that *imposes* 3D rather than explaining it, much as causal dynamical triangulations impose their time layering |
| **P12** | Each chain carries a stability score, **Σ = Coh − Str − Grad** (coherence minus strain minus gradient) | **The only score in ED.** It is already the one place where the state steers motion (C34). Its three parts were never fully defined, and it is written for chains, not links |
| **P03, P13, and Way forward 1 (maximum uniformity, zero contrast)** | The rules are the same at every locus and every time; start from no differences | **"No locus special."** It narrows things down but doesn't pick 3 (see below) |
| **P04 and the per-locus bandwidth bound** (C40) | Each locus has a limited bandwidth | **Could cap how many links a locus carries** |
| **P09** | Each channel carries a phase | **Could say which loops are "good":** loops whose phases fit together |

### Uniformity alone doesn't pick 3 (C179)

There is a known mathematical result (Gromov 1981; Trofimov 1984) about networks in which **every locus looks exactly the same:**
- if such a network's size grows like a power of distance, that power is **a whole number**, so it is lattice-like in 1, 2, 3, 4… dimensions;
- otherwise it grows faster, like a tree or a tangle.

So perfect uniformity allows 3D, but it allows every other whole-number dimension too. And perfect uniformity *is* a crystal, which has built-in directions (T6). Uniformity helps, but it isn't enough on its own.

---

## A proposal: read P12 as the preference for links (C184)

**P12's three parts line up with the three things space needs.** This is my proposal for what they could mean when applied to links; Allen decides.

| P12 part | proposed meaning for links | plain words | where it comes from |
|---|---|---|---|
| **Str (strain)** | How far a locus's number of links is from what its bandwidth comfortably carries | Not too many links, not too few | P04, the bandwidth bound |
| **Grad (gradient)** | How different a locus's surroundings are from its neighbours' | No locus sticks out; zero contrast | P03, P13, maximum uniformity |
| **Coh (coherence)** | How well the phases fit together around small loops | Loops that "close up" nicely count as good | P09, phases |

**Why "coherence around loops" isn't made up from nothing.** Physics already has exactly this for phases on a lattice. Wilson's 1974 lattice gauge theory gives each smallest loop a cost for how badly the phases around it fail to fit (C181). It is the standard way electromagnetism-like forces are put on a grid. Quantum graphity also found a U(1) force emerging in its settled phase (C164).

So reading Coh this way would tie space's shape to the same phase structure (P09) that could carry a force. That loosely echoes your "each force gets a dimension" thought (D11). It's a resemblance, not a result.

**What this proposal buys:**
- **Nothing new is added to ED:** P12, P04, P09, P03 and P13 are already primitives.
- **If it settles into 3D by itself, P06 stops being an assumption and becomes a result.** That would be real progress.
- **If it doesn't,** ED can fall back to imposing P06 openly.

**What it costs, and the risks:**
- **P12 is written for chains.** Applying it to links is an extension, and it needs your OK.
- **Each part still needs a precise form and a weight.** The weights are probably numbers.
- **Nothing guarantees it lands on 3.** Every earlier rule missed, and this one might too.
- **Coh ties geometry to phases.** That may be deep, or it may be a coincidence of words.

---

## Questions for Allen

1. **Is P12 the right place to look?** What did Coh, Str and Grad mean to you when you wrote them?
2. **Does the proposed reading fit your picture?**
   - strain = link load against the bandwidth bound;
   - gradient = difference from neighbours;
   - coherence = phases fitting around small loops.
3. **Fallback:** if nothing in ED produces 3D, is it acceptable to impose P06 openly?

## Proposed next test (after your answers)

**Setup:** seeded growth with even births (RD29) plus local rewiring driven by the P12 reading, with predictions frozen before running. It would be run four times: once with all three parts, and once each with one part left out, to see which part does what.

**Pass condition:** 3D, glass-like, not a crystal.

## Decided and tested (2026-09-13)

**Allen accepted the P12 reading (RD33)** and asked for the test.

**The test** (`checks/p12_growth.py`, predictions frozen before running):
- **Growth:** space grows from 4 linked loci to 1,728, with even births everywhere. Each new locus links to 3 loci nearby.
- **Rewiring:** links rewire by the P12 score, and link phases settle too.
- **Five runs:**
  - all three parts;
  - one run each without coherence, gradient and strain;
  - a run using Wilson's cost as the reading of coherence.
- **Comparison:** a plain 3D lattice of the same size.

| run | pieces | how far apart loci are | random-walk dimension | squares per locus | growth dimension (3D = 3) |
|---|---|---|---|---|---|
| **3D lattice** | 1 | 9.0 | 3.03 | 12 | **3.0** |
| **All three parts** | 1 | 5.4 | 4.09 | 4.5 | **5.0** |
| No coherence | 2 | 5.4 | 3.68 | 4.7 | 4.8 |
| No gradient | 1 | 5.9 | 3.66 | 9.3 | 4.2 |
| No strain | 7 | 5.4 | 4.09 | 4.9 | 5.1 |
| Wilson coherence | 1 | 5.3 | 4.16 | 4.3 | 5.0 |

### What it means, in plain words

- **None came out 3D. All came out with too many dimensions,** about 4 to 5. Space grew connected and glass-like (no perfect lattice loci), but loci ended up too close together for 3D.
- **The three parts barely mattered.**
  - Taking coherence out, or swapping in Wilson's reading, changed almost nothing.
  - Taking gradient out doubled the squares and brought the dimension down to about 4.2, still above 3.
  - So at these settings **P12 isn't what shaped space.** The birth rule (link within 2 steps) and the settings did.
- **My predictions: 5 of 7 were wrong.** I expected either clumps or tangles, and got neither: something in between, a glass with too many dimensions. The one I got right is the one that mattered: none came out 3D.
- **Limits:**
  - one set of weights (1, 1, 0.25);
  - one temperature (0.3);
  - one size, one seed, one birth rule;
  - about 14% of rewiring moves accepted.

### Honest reading (C187)

**This doesn't rule out P12.** The weights and temperature are numbers I chose.

**But tuning them until 3D appears would be fitting, not deriving.** A fair next step is a **pre-registered scan:**
- a small grid of settings (coherence weight, temperature, birth rule), fixed in advance;
- every cell reported;
- a pass only if 3D shows up across a clear region, not in one lucky cell.

**If no setting gives 3D, the fallback is to impose P06 openly.**

## The scan, and P06 imposed (2026-09-13)

**Allen, before running:** "run the scan. if it doesn't work, we will impose P06."

**The scan** (`checks/p12_scan.py`, grid and pass rule fixed before running): 27 combinations, every one run and reported.
- **Coherence weight:** 0.25, 1, 4.
- **Temperature:** 0.1, 0.3, 1.0.
- **Birth rule:**
  - B1: link near v, within 2 steps;
  - B2: link to v's immediate neighbours;
  - B3: split, taking half of v's links.
- **Pass rule:** at least 3 neighbouring combinations come out 3D-like, on two different random seeds.

**Result: the scan fails. Not one of the 27 came out 3D-like** (C188).

| | lowest | highest | 3D lattice |
|---|---|---|---|
| **Growth dimension** | 3.9 | 5.2 | 3.0 |
| **Random-walk dimension** | 2.2 | 4.3 | 3.0 |
| **How far apart loci are** | 5.3 | 6.4 | 9.0 |

**What varied, and what didn't:**
- **Higher coherence weight** gave more square loops every time. It also lowered the dimension a little, never to 3.
- **Higher temperature** raised the random-walk dimension a little.
- **The "neighbours" birth rule (B2)** came closest on growth dimension (3.9), but its random-walk dimension fell to about 2.2. It was lopsided, not 3D.
- **All four predictions I froze were right:** the scan fails; nearly every combination is too high-dimensional; loops rise with coherence weight; hotter means higher random-walk dimension.

**One bookkeeping bug.** After printing every result, the script crashed while saving a data file. The printed output is the record. I fixed the save and added a quick spot-check that reruns three recorded combinations.

### Decided: P06 is imposed (RD34)

**Space has three dimensions, as ED's primitive P06 already says, and it is taken as an assumption, not derived.**
- **Links rewiring (RD32) and P12 as their preference (RD33) stay as ED's picture of how space holds together, but they are parked.** At the sizes and settings tried, they don't produce 3D, and nothing else in ED depends on them.
- **What this costs:** ED doesn't explain why space is 3D. Your pincer idea (D11, C162) stays an intuition.
- **What it frees up:** test beds can now use 3D space directly. The same caution applies as for the 1D ring: a regular lattice is only a stand-in for checking local rules, not a claim about preferred directions (T6).

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C179 | Gromov, "Groups of polynomial growth and expanding maps", *Publ. Math. IHÉS* 53, 53 (1981) | Search listings |
| C179 | Trofimov, "Graphs with polynomial growth", *Math. USSR Sb.* 51, 405 (1985) | Search listings |
| C179 | Tessera and Tointon, "A finitary structure theorem for vertex-transitive graphs of polynomial growth", *Combinatorica* (2021), arXiv:1908.06044 | Search listing |
| C180 | Friedman, "A proof of Alon's second eigenvalue conjecture and related problems", *Mem. AMS* 195, no. 910 (2008) | Search listings |
| C181 | Wilson, "Confinement of quarks", *Phys. Rev. D* 10, 2445 (1974) | Search listings; the loop-cost description is Claude's summary of the standard lattice action |
