# What a reinforcement rule is, and how ED could get one

## In plain words

A **reinforcement rule** says how what has already happened changes the odds of what happens next.

- **Ant trails:** every ant that walks a path leaves scent, so the next ant is more likely to take it.
- **Worn footpaths across grass:** each walker makes the path easier, so more people use it.
- **The simulation spec:** every hop a walker takes makes that hop a bit more likely next time.

A reinforcement rule has to say at least three things:

1. **Does the past change the odds at all?** Some processes have no memory.
2. **By how much, and how does it grow?** Adding a fixed amount each time (linear), or multiplying (exponential).
3. **Can it be undone?** Can a later event cancel an earlier one's effect?

The literature gates showed these choices decide the outcome. Linear, never-cancelled reinforcement gives no preferred direction. Exponential, cancellable reinforcement gives one every time. (Ledger C18, C24.)

## Does ED have one?

**Not as it stands, and not the memory kind.**

**What "can't be undone" means in ED (the author's definition, D1, 2026-09-13).** A commitment is a step a chain takes that can't be taken back. It is **not** a record kept anywhere. A chain commits across the graph. The loci it touched are free for other chains, and because everything is moving, no locus or commitment is ever the same one twice. P11's own wording fits this: no operation maps the state after a commitment back to the state before. That is information lost at the step, not a mark left behind.

So:

- **P11 is not reinforcement.** It doesn't say a commitment makes a similar commitment more likely later.
- **P11 is not a permanent record either.** An earlier version of this note called it one, which was wrong.
- **Reinforced walks are not ED-like.** They store memory on edges (ant scent, worn paths), and ED's loci keep none. The simulation spec had modelled irreversibility as hop strengths that never decrease; that assumption (S2) is withdrawn.
- **If ED has feedback, it must come from what is present now:** the chains and their current contents, the way light's present intensity changes how light travels in a nonlinear ring. The primitive where that could live is P12 (ledger C33, C34).

## Three ways ED could get one

| route | what it means | problem |
|---|---|---|
| **Postulate it** | Add a new assumption: "commitments reinforce like this." | The rule becomes a setting. Whatever follows is a property of the choice, not of ED (Rule 5). |
| **Derive it** | Write ED's commitment rule precisely (P02, P04, P09, P11 as a definite update a computer can run), then see whether reinforcement follows, and in what form. | Nobody has written that rule yet. The primitives are prose. This is the real missing piece. |
| **Fit it to data** | Pick the rule that matches observations. | There are no ED-specific observations to fit. |

Only the second route could make a result that belongs to ED.

## Recommended step

Write the commitment rule, following Rule 1:

- **State:** what exists at a locus (channels, bandwidths, phases).
- **Commitment:** exactly what happens when a commitment occurs, as a formula.
- **Consequence:** what that does to the next commitment's odds.

Do this before any interpretation, and without choosing the rule to make a particular behaviour appear. Then log in the ledger which of the three questions above the rule answers, and how.

The worksheet for this is [Commitment_Rule/Worksheet.md](Commitment_Rule/Worksheet.md).
