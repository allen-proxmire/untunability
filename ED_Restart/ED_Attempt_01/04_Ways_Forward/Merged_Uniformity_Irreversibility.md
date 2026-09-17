# Way forward 3: merged — uniformity plus irreversibility

> **Status 2026-09-13.** Both simulation questions built on this program are already answered in the literature, and each answer depends on a law ED doesn't state: reinforcement ([Sim_Spontaneous_Direction/Literature_Gate.md](Sim_Spontaneous_Direction/Literature_Gate.md)) or feedback ([Phases_Interference/Literature_Gate.md](Phases_Interference/Literature_Gate.md)). The program's real first step is writing the commitment rule ([Reinforcement_Rule.md](Reinforcement_Rule.md)).

## Why the two ways are one

The two approaches run into the same principle from opposite ends:

- **Maximum uniformity:** a symmetric rule on a uniform state stays uniform. A first difference needs chance, a lopsided rule, or a non-uniform start ([MaxUniformity_ZeroContrast.md](MaxUniformity_ZeroContrast.md)).
- **The handedness result:** a mirror-symmetric rule can't carry a preferred direction. A preferred direction must come from the state ([Handedness_Irreversibility.md](Handedness_Irreversibility.md)).

Both say: **symmetric rules don't create asymmetry. Asymmetry comes from the state or from chance.**

ED's commitments are symmetric rules plus an arrow. If both are kept, the only engine left is chance, and irreversibility is what lets chance leave a lasting mark.

## The program

> Start perfectly uniform. Use a rule that is symmetric and irreversible, and whose only source of difference is chance. See what structure appears, and whether it lasts.

The questions, in order. Don't move to the next until the current one has an answer.

1. **Does a difference appear and persist?** Irreversibility should lock in chance events. Check that it does, and that it doesn't just wash out.
2. **Does a preferred direction appear? If so, is it global or in patches?** This is the first question the handedness result makes precise. See [Sim_Spontaneous_Direction/Spec.md](Sim_Spontaneous_Direction/Spec.md). **Status 2026-09-13:** the literature gate showed this is already answered for reinforced random walks, and that the answer depends on the reinforcement law, which ED doesn't fix. Suspended; see [Sim_Spontaneous_Direction/Literature_Gate.md](Sim_Spontaneous_Direction/Literature_Gate.md).
3. **If only patches form, what would it take to get a global direction?** Longer-range coupling, more dimensions, or something else. One change at a time.
4. **Only then: do stable patterns form**, beyond spreading and patches? Each one gets compared against a null model before it counts.

## How the result fits into the program

The theorem does real work in the simulation:

- **At the start** the world is uniform, so its transport is mirror-symmetric and the winding is guaranteed to be zero.
- **In the reversible control** the winding must stay zero at all times. If it doesn't, the code is wrong.
- **Anything nonzero** that appears in the main run is therefore a symmetry broken by chance, which is exactly what the program is looking for.

## Rules that apply most

From [the rules](../00_Rules/README.md):

- **Rule 1.** The rule is written as code before any interpretation.
- **Rule 3.** Every run is repeated on a deliberately different rule.
- **Rule 4.** Reinforcement leading to lock-in is generic, so a lock-in means nothing on its own.
- **Rule 7.** Predictions and pass/fail criteria are written down before the first run.
- **Rule 16.** One question at a time.

## Honest expectations

- **In one dimension, patches are more likely than global order.** Local rules in 1D tend to form domains. Irreversible, out-of-equilibrium rules can behave differently, which is why it's worth testing.
- **A "no" is a result.** If chance plus irreversibility gives only patches, that says what else a world like this needs.
- **None of this is physics yet.** It is a test of whether the logic of the commitments does what the philosophy says it should. Any link to nature comes later, and only through a calculation.
