# Road C5: what form should sync take in growth? (on paper)

*ED_Attempt_07, note 26. 2026-09-18 (RD45). Ledger: C87–C90. Literature and reasoning; nothing computed. **Meaning questions C5-Q1–C5-Q4 and the draft exit rule are for Allen.***

## The question

C3e's runs collapsed wherever sync was switched on (C84). Before scanning its strength, ask whether its **form** is right.

> **Sync earned its place in C2b by deciding which slice dimensions can hold a common "now." Does it also belong in the cost that picks each growth move, and if so, in what form?**

## What's known (C87)

| | what it says | source |
|---|---|---|
| **Sync-driven rewiring makes small worlds, not geometry** | Oscillator networks rewired by phase differences, under a limited connection budget, organize into **modular small-world** structure | Gutiérrez et al., *PRL* 107, 234103 (2011) (C54) |
| **Shortcuts are what kill distance** | A few long links turn a lattice-like network into a small world, with distances falling to logarithmic | Watts–Strogatz; Barthélemy, *Spatial Networks*, *Phys. Rep.* (2011) |
| **Cost per link length suppresses shortcuts** | In spatial networks, a cost that grows with a link's length keeps distances lattice-like; without it, shortcuts dominate | Barthélemy (2011) ([arXiv:1010.0302](https://arxiv.org/pdf/1010.0302)) |
| **Entropy favours crumpled geometry** | Random triangulations with no weight on the building-block count crumple, with diameters far below the flat value | A7 C42, C54, C72 |
| **CDT's own slices are not flat** | In 4D CDT's de Sitter phase, a single spatial slice has Hausdorff dimension about 3 but spectral dimension about 1.5: **fractal slices inside a good phase** | A7 C20 |

## On paper

### 1. Why C3e's sync collapses the slice (C88)

**The cost as specced rewards a link in proportion to the tick difference it carries.**
- **The largest differences sit between regions far apart,** because the tick field varies smoothly and accumulates with distance.
- **So the move cost pays most for exactly the links that shorten distances.** That's the shortcut mechanism, and it's the same behaviour the adaptive-sync literature reports: rewiring by phase difference builds small worlds.
- **The evidence matches:** with sync on, links per event rose to 14–21, diameters fell to 8, and event counts fell by half. With sync off, sizes held.

**And it isn't the strength.** Turning γ down weakens the pull but keeps its direction. That's why a strength scan alone would answer the wrong question.

### 2. The deeper problem: local weights against entropy (C88)

- **Every weight in C3c–C3e is local:** links, valences, tick differences across single links.
- **The number of rough configurations vastly exceeds the number of smooth ones.** Local weights have to fight that entropy, and in every run they lost.
- **The one quantity ED has that isn't local is the tick field** (C57). Its value at a place depends on the whole region. That's why sync looked like the answer.
- **But rewarding the relief of strain flattens the field,** and a flat field is exactly what an expander-like, small-diameter slice gives you. **The cost as written asks for the shape we don't want.**

### 3. The target may be wrong, not just the term (C89)

**This is the part worth pausing on.**
- **C3c–C3e demanded that a grown slice read flat 3D.**
- **CDT's own good phase doesn't satisfy that.** Its spatial slices are fractal (Hausdorff about 3, spectral about 1.5). What is smooth in CDT is the **spacetime**, not the slice.
- **C1 judged ED the same way CDT is judged:** it measured the spacetime pattern (slices plus forward links), and got 2D as it should.
- **So road C3 has been holding ED to a stricter standard than the theory it's being compared with.**

**The fix is available and cheap:** measure the **spacetime** pattern grown by C3e's machinery, not the slice. The runs already build it; only the reading changes.

### 4. Four readings of sync's form (C89)

| | reading | what it does | verdict on paper |
|---|---|---|---|
| **(i)** | **As specced:** reward links carrying strain | Builds shortcuts; flattens the tick field; small-world slices | **Fails**, by C3e and by the adaptive-sync literature |
| **(ii)** | **Locality-capped:** the same reward, but only for links whose ends were already within a few hops | Keeps the neck-widening it was meant for (a neck's two sides are two hops apart through the neck) and bans shortcuts | **Plausible**, and matches the spatial-network lesson that cost must grow with length |
| **(iii)** | **A condition, not a reward:** a move is refused if it would leave any link's tick difference above the space-like limit | Reads "clocks want to sync" as something the pattern must keep, like the link condition, rather than a force | **Closest to C2b's meaning**, where sync sets a condition that dimensions must satisfy |
| **(iv)** | **Out of growth entirely:** sync selects which slice dimension is viable (C2b) and plays no part in the move cost | Growth is shaped by commitment and curvature; sync stays a selection principle | **Cleanest**, and testable as a contrast |

### 5. What each reading predicts, in one line each (C90)

- **(ii)** should stop diameters collapsing, since no move can shorten distance by more than the cap.
- **(iii)** should leave shapes to commitment and curvature, with sync only vetoing moves that tear "now."
- **(iv)** is the control: if growth without sync gives the same shapes as (iii), then sync in the cost was doing nothing useful either way.

## What it means (C90)

- **Sync's failure in C3e is a failure of form, not of strength.** Rewarding strain relief asks for flat tick fields, and flat tick fields come with collapsed distances.
- **The honest reading of C2b is a condition:** "the pattern keeps a common now" is something to satisfy, not something to maximize.
- **The bigger correction is the target:** slices need not be flat, in ED or in CDT. The thing to measure is the grown **spacetime**.
- **Consistent, not derived.** Nothing computed. Inputs unchanged (3).

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **C5-Q1** | **Is sync in growth a condition** (a move must not leave a link's tick difference above the space-like limit) **rather than a reward?** | **Yes**, reading (iii) | It's what C2b actually established; a reward asks for the opposite shape |
| **C5-Q2** | **If a reward form is kept for comparison, must it be locality-capped** (only links whose ends were within a few hops)? | **Yes**, reading (ii) as a contrast | Matches the spatial-network lesson; keeps neck-widening, bans shortcuts |
| **C5-Q3** | **Should road C3 judge the grown spacetime pattern** (slices plus forward links), not the slice alone? | **Yes** | CDT's slices are fractal in its good phase; C1 already judged ED this way |
| **C5-Q4** | **Keep a no-sync run as the control** (commitment and curvature only)? | **Yes**, reading (iv) | Shows whether sync in the cost earns its place at all |

## Draft exit rule (Allen to confirm)

**Next step: C3f, specified on paper, then run.** It would carry:
- **the label fixes** (crumpled test independent of the ceiling; a diameter floor, below which a run is recorded "too small to measure" rather than given a shape);
- **spacetime readings** as the main result, slice readings reported alongside;
- **four settings:** commitment and curvature only; the same plus sync as a condition; the same plus locality-capped sync; and no pressure as the baseline.

**Recording:**
- **the grown spacetime reads 4-dimensional and smooth in some setting:** "with the link balance, paired cut-and-rejoin and ⟨that sync form⟩, ED's growth gives a four-dimensional pattern at the sizes run: consistent, not derived";
- **no setting does, but the counts hold:** "ED's local weights don't select smooth geometry against entropy; the wall is the ensemble, not the meanings";
- **the counts don't hold:** recorded as a model or code problem.

**Expected results, ranges and a cost plan fixed in the spec before any code.**

## Next steps (Allen decides)

| | step |
|---|---|
| **(a)** | **Decide C5-Q1–C5-Q4 and spec C3f** |
| **(b)** | **Reread the existing C3e runs as spacetime patterns first** (cheap: the saved runs hold the slices, but not the forward links, so this needs a short rerun) |
| **(c)** | **Take stock again** before spending more compute |

**Proposal: (a).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C87 | Gutiérrez et al., *PRL* 107, 234103 (2011) (C54); Barthélemy, *Spatial Networks*, *Phys. Rep.* 499, 1 (2011), [arXiv:1010.0302](https://arxiv.org/pdf/1010.0302) (listing: cost per link length suppresses shortcuts, and shortcut density decides lattice-like against small-world distances); Watts–Strogatz shortcut effect (standard); A7 C20 (4D CDT slices fractal), C42, C54, C72 | 2026-09-18 |
| — | A7 C57, C66, C84, C85; A6 G-Q6, G-Q11 | Ledgers |
