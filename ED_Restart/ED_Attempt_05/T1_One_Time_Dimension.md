# Road T, part 1: why exactly one time dimension? (on paper)

*ED_Attempt_05, note 9. 2026-09-15 (RD14). Ledger: C33–C36. Literature and reasoning; nothing computed. **Meaning questions T-Q1 and T-Q2 and the draft exit rule are for Allen.***

## The question

- **Physics assumes spacetime has three space dimensions and one time dimension.**
- **ED has a reason for the three** (A4 E-C, kept by road P).
- **The inputs table lists the one time dimension as a candidate** (item 7): ED says time is the order of relations (A4 D11), and an order runs one way.
- **Does that force exactly one time dimension?**

## What's known (C33)

| | what it says | source |
|---|---|---|
| **Future and past split only with one time** | Take a spacetime interval with t time directions and s space directions. The "timelike" directions form **two separate pieces (future and past) exactly when t = 1.** With two or more time directions they form **one connected piece.** With none, there are no timelike directions at all | Standard geometry of quadratic forms |
| **Order gives the geometry** | The causal order of events fixes a spacetime's geometry, the kind with one time dimension, up to scale; counting fixes the scale | Malament; Hawking, King and McCarthy; causal sets (A4 C26) |
| **More times means no prediction** | With other numbers of time dimensions, physics' equations lose the property that lets the present fix the future | Tegmark 1997 (A4 C54) |
| **More times is possible with a catch** | Wave equations with several time dimensions have well-posed initial data only under **nonlocal constraints** | Craig and Weinstein, *Proc. R. Soc. A* 465 (2009); Weinstein, "Multiple time dimensions" |
| **A formal counterexample** | Bars' "two-time physics" works in 4 + 2 dimensions, but a gauge symmetry makes the extra time unphysical. Ordinary one-time physics comes out as its "shadows" | Bars |
| **An old argument** | Dorling (1970) argued that with more than one time dimension, particles would lose their stability | Dorling, *Am. J. Phys.* 38, 539 |

## The chain (C34)

1. **Time is the order of relations** (A4 D11).
2. **What happened stays happened** (D10, P-Q1). So the order has a direction:
   - if a came before b, then b never came before a;
   - if a came before b and b before c, then a came before c.

   That's a strict order (T-Q1).
3. **Where a smooth description applies, the order comes with an interval** (T-Q2, a labelled assumption):
   - a quadratic form like the pairings count (D29) generalized, **with the number of time directions left open;**
   - its sign says whether two events can be ordered at all.
4. **The geometry fact:** future and past are separate pieces only when there's exactly one time direction.
   - **With two or more,** the timelike directions form one connected piece. Any "later" direction can be turned smoothly into an "earlier" one without ever stopping being timelike, so "later" can't be defined consistently, and step 2's "never both ways" fails.
   - **With none,** there are no timelike directions, so there's no order at all, contradicting step 1.
5. **So ED's time has exactly one dimension.**

**What would be ED's own:** in physics, "one time dimension" is part of the assumed signature. **In ED it would follow from a meaning ED already has, an order that runs one way,** plus the quadratic form of the interval, which physics assumes too.

## Pokes (C35)

| | poke | what it means |
|---|---|---|
| **T1** | **The quadratic interval (Q) is assumed.** ED's pairings count has that form, but it was chosen knowing special relativity (C78 in A4) | "One time" follows from order *given* Q. Q stays inherited, as it is in physics |
| **T2** | **The argument is known.** Tegmark, Dorling, and the causal-set programme all tie one time to predictability or order | At best: **a reason from ED's meanings, not new physics** |
| **T3** | **Bars' two-time physics is consistent,** but only because the extra time is gauge, not physical | Not a counterexample to ED's meaning: there's still one physical order |
| **T4** | **With general light-cone shapes** (not quadratic), "number of time dimensions" isn't defined, but "one future cone per event" still is, and an order gives exactly that | The conclusion survives in weaker form without Q |
| **T5** | **ED is discrete.** The order comes first, and the smooth interval appears only approximately at large scales | The argument applies where the smooth description does. The rest frame (wall 1) is a separate issue |

## Meaning questions (Allen decides)

| | question | proposed default | why |
|---|---|---|---|
| **T-Q1** | **Is ED's order of relations a strict order** (never both ways; before-before gives before), **as a reading** of "time is the order of relations" plus "what happened stays happened"? | **Yes, as a reading** | Both parts are already in D11 and D10 |
| **T-Q2** | **Where a smooth description applies, is ED's interval a quadratic form** (the pairings count generalized), **with the number of time directions left open,** as a labelled assumption? | **Yes, labelled** | It's what "number of time dimensions" means, and physics assumes the quadratic form too |

## Draft exit rule (Allen to confirm)

- **If exactly one time dimension follows from T-Q1 (a reading), T-Q2 (labelled) and the geometry fact:** record **"one time dimension: a reason from ED's meanings; a reduction by one input (the number of time dimensions), conditional on reading T-Q1 and assumption Q"**. Q itself stays inherited.
- **If T-Q1 is a new meaning rather than a reading:** record **"consistent, not derived; no reduction"**.
- **If Allen rejects T-Q2:** record **"one future cone per event"** (T4) as a consistency, with no count of time dimensions and no reduction.
- **Bars' two-time physics is noted,** not treated as a conflict.
- **No model is built at this step.**

## Next steps (Allen decides)

| | step | why |
|---|---|---|
| **(a)** | **Decide T-Q1 and T-Q2** and confirm the exit rule | A short step that could add a third supplied input |
| **(b)** | **Then the frontier:** waves on a direction-free random pattern, or a growth rule (note 8's options c and d) | The walls everything else waits on |

**Proposal: (a).**

## Sources checked

| ledger | source | how checked |
|---|---|---|
| C33 | Connectivity of timelike and spacelike sets for signature (p, q): arc-connected if the relevant count exceeds 1, two components if it equals 1 (as described in MathWorld "Timelike", arXiv:2301.13625, arXiv:1209.5665); Malament, Hawking–King–McCarthy, causal sets (A4-ledger C26); Tegmark, *Class. Quantum Grav.* 14, L69 (1997), arXiv:gr-qc/9702052 (A4-ledger C54); Craig and Weinstein, "On determinism and well-posedness in multiple time dimensions", *Proc. R. Soc. A* 465, 3023 (2009), arXiv:0812.0210; Weinstein, "Multiple time dimensions", arXiv:0812.3869; Bars, two-time physics (arXiv:hep-th/0606045, arXiv:1008.1540; USC two-time physics page); Dorling, "The dimensionality of time", *Am. J. Phys.* 38, 539 (1970); "Is time one-dimensional?", arXiv:2407.06218 (listing); closed cone structures (Minguzzi, arXiv:1709.06494) | Listings and abstracts |
| — | A4-ledger C26, C54, C78, D11, D29; D10 (this ledger) | Earlier ledgers |

**Update (D11):** Allen accepted T-Q1 and T-Q2 and confirmed the exit rule. **Verdict: one time dimension, a reason from ED's meanings; a reduction by one input (the number of time dimensions), conditional on reading T-Q1 and assumption Q** (C37). Q stays inherited. Road T closed (RD15).
