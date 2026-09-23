# Locus birth and dark energy

*2026-09-14. Ledger: C209–C214. Follows [Locus_Birth.md](Locus_Birth.md) (RD29) and [Nordtvedt_Check.md](Nordtvedt_Check.md). G39 was decided as RD37: ED's gravity is GR in budget language, so the effort moves here.*

## 1. What ED's current rule predicts (C211)

**RD29: every locus has the same tiny birth chance per step.** Assume each step is one Planck time and each locus one Planck volume:

| quantity | value | what it means |
|---|---|---|
| **Birth chance needed** for today's dark energy | **about 2.9 × 10⁻⁶¹ per step** | One birth per locus every 10⁶⁰ steps or so |
| **The cosmological constant that gives** | Λ ≈ 2.85 × 10⁻¹²² (Planck units) | The measured value, by construction |
| **How much the number of births jitters** in a Hubble volume over a Hubble time | **about 10⁻⁹²** | Far too small to see |

Checked with `checks/birth_rate_lambda.py`; predictions were frozen before running, and all came out as predicted.

**So the current rule predicts:**
- **Dark energy exactly constant,** with no change over time (w = −1).
- **One unexplained number:** 2.9 × 10⁻⁶¹. That is the old "why is the cosmological constant so small?" problem, restated.
- **If surveys confirm dark energy changing over time,** RD29 as it stands is ruled out. DESI's hint is 2.8–4.2σ (C139). Other analyses of supernovae alone still find it consistent with constant (C212).

## 2. The published route that avoids the tiny number: Everpresent Λ (C209, C210)

**Sorkin's idea** (causal sets):
- **The cosmological constant isn't a fixed number.** It fluctuates, with a size of about 1 divided by the square root of the amount of spacetime so far.
- **Today that is about 1.4 × 10⁻¹²²,** within a factor of 2 of the measured value (C211), **with no tuning.** It was predicted before dark energy was discovered.
- **Its sign flips** roughly once per Hubble time, and its size tracks whatever else dominates the universe at the time.

**How it has fared against data:**
- **Zwane, Afshordi and Sorkin (2018):** a version fits current observations about as well as the standard model.
- **Das, Nasiri and Yazdi (2023–24):** simulations can produce today's values, but only in uncommon runs. Some runs fit supernovae better than the standard model, but most do worse against the CMB.
- **Barrow (2007):** the isotropy of the CMB limits fluctuations that vary from place to place.

**Mixed, not dead, and actively tested.**

## 3. ED's twist: births can't be negative (C213)

**In ED, dark energy is births:** new loci being added.
- **Loci persist** (RD20, space is the record). Nothing removes them.
- **So in ED the birth rate can fluctuate, but never below zero.**
- **ED's version of Everpresent Λ would be one-sided:** dark energy that jitters and changes, **but is never negative.**

**That is a genuine difference from the causal-set version,** where Λ goes negative about half the time.
- **It could matter.** Some DESI analyses weakly prefer a negative cosmological constant hiding underneath evolving dark energy (above 68% only, C212). If data ever clearly needed negative dark energy at some epoch, ED's one-sided version would be ruled out and the two-sided one wouldn't.
- **Honest caveats:**
  - This is my reading of RD20 applied to births. Nobody has published a one-sided version that I've checked.
  - The mechanism (why the birth chance would fluctuate like 1/√volume) would be *borrowed* from causal sets, not derived in ED.
  - One-sided fluctuations have a positive average, which changes the model's statistics. They need their own test against data.

---

## G40: which birth rule?

| | option | what it predicts | cost |
|---|---|---|---|
| **(a)** | **Keep a constant birth chance** (RD29 as is) | Dark energy exactly constant | One unexplained tiny number (2.9 × 10⁻⁶¹). Ruled out if evolving dark energy is confirmed |
| **(b)** | **Everpresent-style births, one-sided:** the birth chance fluctuates with size about 1/√(amount of record so far), and never goes below zero | Dark energy that changes over time, stays near the density of everything else, and is **never negative** | No tiny number, just an order-1 factor. The mechanism is borrowed from causal sets. Must survive CMB and isotropy tests |
| **(c)** | **Births tied to commitment activity** | Dark energy following the history of interactions and structure | More structure, and a coupling number |

**Proposal: (b).** It removes ED's only unexplained number. It is the one place so far where ED might say something testable that isn't already standard: **dark energy that fluctuates but is never negative.**

**Proposed next step if (b):**
1. A literature check on how Everpresent Λ is implemented in simulations (Das, Nasiri and Yazdi's model equations).
2. A frozen toy comparison of one-sided and two-sided versions: how often each gives today's values, and how their dark-energy histories differ.

## Questions for Allen

1. **G40:** (a) constant births, (b) one-sided fluctuating births, or (c) births tied to activity?
2. **Does "births jitter but can never go negative" match your picture** of loci being born and persisting?

## Decided (2026-09-14): G40 = (b), RD38. The comparison

**What was compared** (`checks/everpresent_onesided.py`, predictions frozen before running): a simple one-number-in-time model of the universe, using the published Everpresent Λ rule, in three versions, 400 runs each:

| version | rule |
|---|---|
| **Two-sided** (causal sets) | Dark energy fluctuates and can go negative |
| **One-sided, clipped** (ED) | Same fluctuations, but dark energy is set to zero whenever it would be negative |
| **One-sided, reflecting** (ED) | The fluctuations themselves bounce off zero |

Both the strength used by Das et al. and the weaker strength in the original 2004 paper were run.

**Two mistakes of mine, both recorded:**
- **The first run was invalid.** My code started counting spacetime from zero partway through the early universe, which made the first fluctuations huge, so every two-sided run crashed at once. After fixing it I reran with the predictions unchanged.
- **I predicted about 53% of two-sided runs would survive, from a misread summary.** The paper actually says 535 out of 10,000, which is 5%.

### Results (run 2)

| | two-sided | one-sided, clipped | one-sided, reflecting |
|---|---|---|---|
| **Runs that survive** (Das strength) | **0%** (all crash) | 100% | 100% |
| **Runs that look like today** (Hubble rate within 10%, dark energy 60–80%) | 0 | **7%** | **10%** |
| **Weaker 2004 strength** | Survive, but dark energy today is only about 0–3%. No run looks like today | Same | Same |

**Among the runs that look like today** (a diagnostic added after the run):

| | one-sided, clipped | one-sided, reflecting |
|---|---|---|
| **Dark energy at the time of the CMB** | **Zero in about half the runs.** 52% are below about 0.7%, the level Planck-era limits allow (search listing, C218) | **Always large:** at least 4%, median 58% |
| **How much dark energy changed since z = 1** (about 8 billion years ago) | **Median factor of about 2.** Only 14% changed by less than 30% | Median factor of about 3 |

### What it means

- **The reflecting version is ruled out.** Every run that looks like today has far too much dark energy early on for the CMB.
- **The clipped version is the live one.**
  - It never crashes.
  - It produces universes like ours when the two-sided version can't, at the same strength.
  - Half of those have no early dark energy problem.
- **Its problem is change.** In most runs like ours, dark energy changed by a factor of about 2 since z = 1. Current data allow only modest change: DESI hints at some, and a supernova reconstruction finds none (C212). So most, but not all, clipped runs are probably ruled out. **That needs a proper comparison with real distance measurements, not just this toy.**
- **Limits:**
  - one number describing the whole universe, with no clumping, so the CMB can't really be tested;
  - one step size;
  - the clipped and reflecting rules are my two readings of "never negative".
- **The strength that matters in the published model** crashes the two-sided version almost every time. Das et al. get 5%, and my toy 0 of 400. So the toy isn't an exact copy of theirs.

## G41: what next for ED's dark energy?

| | option | what it means |
|---|---|---|
| **(a)** | **Keep one-sided, clipped births** as ED's form, drop reflecting, and **test the clipped runs that look like today against real distance data** (supernovae and BAO) | The first real data test of something ED-specific. It may rule the clipped form out |
| **(b)** | Go back to constant births (RD29) | Matches current data; brings back the tiny unexplained number |
| **(c)** | Everpresent births with fluctuations damped at late times | Das et al.'s data test hinted that good runs have small late fluctuations. More structure, and a risk of fitting |

**Proposal: (a).**

## Decided (2026-09-14): G41 = (a), RD39. The distance-data test

**Allen:** "it's possible that it's (b). but do (a) now."

**The test** (`checks/bao_distance_test.py`, predictions frozen before running):
- **Data:** DESI's second data release of baryon acoustic oscillation distances. That is 13 measured distances out to redshift 2.3, about 11 billion years back, with their full error matrix, copied verbatim from the published data files.
- **Candidates:** 2,000 clipped one-sided universes. 93 of them look like today.
- **Fit:** each universe, and constant dark energy, gets one overall scale fitted, nothing else.

### Result

| model | how well it fits (χ², 13 distances; lower is better) |
|---|---|
| **Constant dark energy** (same matter density) | **14.3** (good) |
| Constant dark energy, matter density also free | 10.3 |
| **Best of the 93 clipped universes like today** | **91**, worse by 77 |
| **Typical clipped universe like today** | worse by about **830** |

**None of the 93 comes close.** A difference of 77 is overwhelming. The clipped one-sided form is **ruled out by DESI's distances alone.**

**Why** (diagnostic on the best run): in these universes dark energy follows the total density back in time, the signature of the everpresent mechanism.

| redshift | dark energy share, best clipped run | dark energy share, constant |
|---|---|---|
| 0 (today) | 71% | 69% |
| 0.5 | **79%** | 39% |
| 1 | **66%** | 21% |
| 2 | **64%** | 7.5% |

Today looks right, but the past is badly wrong, and distances measure the past. The best run also needs a distance scale about 50% off, which would clash with the sound-horizon size the CMB gives. That is a further failure this test didn't count.

**Predictions: 5 of 7 right.** Two were wrong:
- I expected at least 5% of runs to fit acceptably; none did.
- I expected runs with little change since z = 1 to fit better. Only 2 such runs existed, and they fit badly too.

**Limits:**
- distances only, with no supernovae or CMB;
- one fluctuation strength and one matter density;
- my "clipped" reading of never-negative;
- a toy model without clumping.

**None of these limits is likely to turn a difference of 77 into a fit.**

## G42: what now?

| | option | what it means |
|---|---|---|
| **(a)** | **Go back to constant births (RD29): your "(b)"** | Dark energy is exactly constant and fits the distances well. It brings back the tiny unexplained number. ED says nothing new about dark energy |
| **(b)** | Everpresent births with late-time fluctuations damped | Could be tuned to fit. Without an ED reason for the damping it's fitting, and Das et al.'s data tests already point that way |
| **(c)** | Abandon everpresent fluctuations but keep "never negative" | With constant births, "never negative" is automatic and says nothing extra |

**Proposal: (a).**

**The honest bigger picture.** On both sides where ED had a chance to be different from standard physics, it has come back to standard physics:
- **Gravity:** it is GR in budget language (RD37).
- **Dark energy:** the distinctive version is ruled out, and the survivor is a plain cosmological constant.

**What remains distinctive is interpretation and structure,** not a testable prediction:
- commitments as irreversible steps;
- space as the record;
- draws when a mark can't be brought back;
- exact draws as a point of principle.

**That is worth saying plainly before choosing what to do next.**

## Decided (2026-09-14): G42 = (a), RD40. Then: horizon-set births tested

**The idea (Allen's "flow meets boundary", D14):** the birth rate is set by the horizon, the edge of what we can ever see. Published as holographic dark energy (Li 2004): dark energy density = 3c² M_P² / L², with L the future event horizon and c an order-1 number. **As an ED birth rule it replaces the tiny birth chance (2.9 × 10⁻⁶¹) with c.**

**The test** (`checks/hde_bao_test.py`, predictions frozen before running): the same DESI DR2 distances and pipeline as before. Holographic dark energy has matter density and c free; constant dark energy has matter density free. Each gets one fitted overall scale.

| model | best fit (χ², 13 distances) | settings |
|---|---|---|
| **Constant dark energy** | 10.28 | matter 0.298 |
| **Horizon-set births** | **10.05** | matter 0.272, **c = 0.93**, dark energy today w = −0.945 (slowly thinning) |

**In plain words:**
- **Horizon-set births fit DESI's distances as well as constant dark energy,** marginally better in raw fit.
- **Not better once the extra number is paid for.** The model-comparison score, which penalises each extra number, is 1.8 *worse*.
- This matches a published 2026 analysis (C227).
- **The number that sets it, c ≈ 0.93, is order 1.** That's the point: no 10⁻⁶¹.
- **It predicts dark energy thinning slightly over time** (w a little above −1), the direction DESI hints at.

**Predictions: 4 of 5 right.** One was my error: I assumed large c would turn it into constant dark energy. It doesn't; large c gives w = −1/3. The code was checked another way and is correct.

**Limits:**
- **Distances only.** The best-fit matter density (0.272) is lower than Planck's CMB value (0.315), so adding the CMB could hurt it.
- **It's Li's model in ED words,** not derived from ED.
- **It relies on counting by horizon area, which competes with exact draws** (C143).

**G44:** adopt horizon-set births as ED's birth rule (c ≈ 1 instead of a tiny number), or keep constant births? Next test either way: add the supernova and CMB distance data.

## Decided (2026-09-14): G44 = adopt provisionally (RD42). Then: supernovae and the CMB

**The test** (`checks/hde_combined_test.py`, predictions frozen before running). Three kinds of data, each model with one fitted scale for BAO and one for supernovae:
- **BAO:** the same DESI distances as before.
- **Supernovae:** Union3, compressed to 22 points with their full error matrix, downloaded verbatim.
- **CMB:** Planck's "shift parameter" R = 1.7502 ± 0.0046, which measures the distance to the CMB in a way that pins the matter density.

| model | BAO + supernovae + CMB | matter density |
|---|---|---|
| **Constant dark energy** | **40.1** | 0.310 |
| **Horizon-set births** | **72.8**, worse by 33 | 0.306 (c = 0.67) |

**With the CMB included, horizon-set births fit much worse:** a difference of 33 is decisive.

**Where it breaks** (diagnostic after the test, `checks/hde_combined_diagnostic.txt`):

| data used | horizon-set births compared with constant dark energy |
|---|---|
| BAO only | about equal (−0.3) |
| Supernovae only | slightly better (−1.7) |
| BAO + supernovae | **better (−4.9)** |
| Supernovae + CMB | about equal (−0.3) |
| **BAO + CMB** | **worse (+15.3)** |
| **All three** | **worse (+32.8)** |

**In plain words:**
- **Horizon-set births need a low matter density (about 0.27) to match the BAO distances,** but the CMB needs about 0.31.
- **Constant dark energy satisfies both at 0.30–0.31.** Horizon-set births can't satisfy both.
- **Without the CMB, horizon-set births would even be mildly preferred,** which is why the late-time-only published analysis found them comparable (C227).
- **This isn't about early dark energy.** Horizon-set births have almost none when the CMB formed (0.007%).
- **The code was checked:** the BAO-only fit reproduces the earlier test (10.03 at c = 0.93).

**Predictions: 6 of 7 right.** I predicted "comparable, within 6", and the real gap was 33.

**Limits:**
- the CMB is used only through R, a compressed number derived assuming constant dark energy;
- the Hubble constant is fixed where it enters radiation and the CMB redshift;
- the supernovae are compressed.

A full CMB analysis could move the numbers, but a gap of 15 from BAO + CMB alone is hard to erase.

## G45: what now for births?

| | option | what it means |
|---|---|---|
| **(a)** | **Back to constant births** (RD40 again) | Fits everything tested. The tiny number returns |
| **(b)** | **A different horizon** (Barrow, Tsallis or "fractional" holographic dark energy) | Published variants with extra numbers. One published analysis found a future-horizon fractional version close to constant dark energy with CMB priors. More numbers; risk of fitting |
| **(c)** | Keep testing horizon-set births with the full CMB | Unlikely to overturn a gap of 33 |

**Proposal: (a).** Dark energy returns to a plain cosmological constant, and the tiny number is back.

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C209 | Sorkin, "Is the cosmological 'constant' a nonlocal quantum residue of discreteness of the causal set type?", *AIP Conf. Proc.* 957, 142 (2007), arXiv:0710.1675 | Abstract |
| C210 | Das, Nasiri, Yazdi, "Aspects of Everpresent Λ (I)", *JCAP* 10 (2023) 047, arXiv:2304.03819 | Abstract |
| C210 | Das, Nasiri, Yazdi, "Aspects of Everpresent Λ (II)", arXiv:2307.13743 | Abstract |
| C210 | Zwane, Afshordi, Sorkin, "Cosmological tests of Everpresent Λ", *Class. Quantum Grav.* 35, 194002 (2018), arXiv:1703.06265 | Abstract |
| C210 | Barrow, "A strong constraint on ever-present Lambda", *Phys. Rev. D* 75, 067301 (2007), arXiv:gr-qc/0612128 | Abstract |
| C212 | Wang, Peng, Piao, "Can recent DESI BAO measurements accommodate a negative cosmological constant?", arXiv:2406.03395 | Abstract |
| C212 | Blanco, Cárdenas, Campuzano, "Revealing evolution of dark energy density from observations", arXiv:2510.12881 | Abstract |
