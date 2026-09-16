# Event Density

**Event Density (ED)** is a way of picturing how the world works underneath. It starts from one simple conviction: **time only runs one way.** Once something has really happened, it can't be undone.

This repository holds ED's one proved result, and a note on how ED's ideas connect to Jacobson's derivation of gravity.

## The idea

In ED:

- **The world is a web of places,** called *loci*. The web keeps growing: new places keep being born.
- **Things spread across the web like ripples,** trying out many paths at once.
- **When a ripple meets something already settled,** it leaves a mark. Once that mark can't be brought back, something definite has happened. ED calls this a *commitment*, and the moment it becomes final a *draw*.
- **Commitments use up a kind of budget,** so near a lot of settled matter, clocks and motion slow down.

That's the whole picture. Everything else is working out what it implies.

## What it gets right

The picture was turned into an exact set of rules that a computer can run, and then checked against what's already known.

- **Quantum behavior.** The rules reproduce the strange things quantum experiments show: waves that interfere with themselves, interference that fades when you learn which path was taken, and comes back when that information is erased. They also never let a signal go faster than light.
- **Gravity.** With the budget set up the right way, the rules match Einstein's general relativity: how light bends near the Sun, how Mercury's orbit shifts, how the Moon moves.
- **The expanding universe.** New places being born at a steady rate gives the steady push that makes the universe's expansion speed up, matching astronomers' measurements.

**Matching known physics is a requirement, not a discovery.** Each match was reached by adjusting the rules to fit what's already measured.

## The one result

**Handedness** means a built-in preference for left or right. The laws of nature have one: one of the fundamental forces treats left and right differently.

Picture a highway with several lanes. Traffic hops forward or backward along the road, switching lanes as it goes. Does it drift more one way than the other? ED proved a small theorem about that:

- **If the rules look the same in a mirror,** the drift is exactly zero. Every bit of preference one way is matched the other way. So handedness can't be written into mirror-symmetric rules. If a world has a handedness, the state of the world picked it, the way a magnet picks a direction its laws don't prefer.
- **Handedness is only possible at all because time runs one way.** If hopping forward and back were perfect mirror images in time, there could be no preference whatever the rules.

The theorem is correct, and a script here checks it. Its mathematics is simple, and something close to it is already known.

## What didn't work

A lot, and every failure is written down.

- **Dark energy.** ED's own distinctive versions (births that fluctuate, or births tied to the edge of the visible universe) were ruled out or disfavored by real astronomical data. What fits is the ordinary constant version.
- **Gravity.** Every simpler version of the budget failed a real measurement, and each fix just made ED more like Einstein's theory.
- **Space.** ED couldn't explain why space has three dimensions. That has to be put in by hand.
- **Handedness in ED's own rules.** ED's rules *can* settle into a handed state picked by chance, but only if three extra ingredients are added by hand. Three careful attempts to make ED supply the key ingredient itself all failed.

## Where it stands

- **ED is an interpretation:** a consistent, runnable way of picturing the world that agrees with known physics.
- **It isn't a new theory** that tells us something about nature we didn't already know.
- **Its lasting contributions:**
  - the handedness theorem;
  - a clear, physical account of what makes a measurement final;
  - an unusually complete record of what doesn't work, and why.

## How the work was done

- **Tests set up in advance.** Each test was specified before it was run, so results couldn't be quietly reinterpreted afterwards.
- **Every failure recorded,** including mistakes in the test code itself.
- **Literature first.** Before claiming anything, published physics was checked to see whether someone had already done it.
- **Tuned settings labeled.** Any setting chosen just to make something work is marked as tuned.
- **An exit rule agreed ahead of time.** "If three honest attempts fail, stop and write it up." That's why the write-up exists.

## What's in this repository

| | |
|---|---|
| **The theorem** | [Result.md](Result.md) (one page), [Paper.md](Paper.md) (full proof and limits), [Assumptions.md](Assumptions.md) (what it assumes), [tools/check_result.py](tools/check_result.py) (checks it) |
| **Gravity's area law** | [Jacobson_Area_Law.md](Jacobson_Area_Law.md): how ED's ideas supply the one physical assumption in Jacobson's derivation of Einstein's equations, and exactly what that does and doesn't show |

## Check the theorem yourself

```
python tools/check_result.py
```

This needs Python with numpy. It tests the theorem for up to six lanes, for random mirrors, and for hops reaching several places at once. It also runs the two edge cases: traffic that only hops forward, and traffic without one-way time.

## Further reading

- H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981). The best-known result of this kind about handedness.
- The full reference list is in [Paper.md](Paper.md).
