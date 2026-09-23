"""The reach: does the sync filter destroy a shape because of how FAR it repairs, not how much?

Road P (C5) ran the filter with a reach of three relations and every shape was destroyed. The balance scan (C7)
showed that inheritance, which reaches ONE relation - children of neighbouring parents - preserves a shape perfectly
at any rate, from a line to a 3D grid. The difference between the two is reach, so this tests it directly.

Road P's model, unchanged in every other respect (note 3, D2). Only the filter's reach varies: when the clocks fail
and relations are added where the strain is worst, the partner must lie within REACH relations of the strained
event. Reach 1 is degenerate - the only events within one relation are the ones already related - so the scan is 2,
3 (road P's setting, which should reproduce road P) and 4.

EXPECTATIONS, fixed before this file was run:
  R1  MAIN: at reach 2 the starts KEEP their shapes - the ring stays a line, the 3D grid stays 3D - while the
      clocks still hold                                                                            about 45%
  R2  at reach 3 they do not, reproducing road P (a check on the rerun as much as an expectation)   high
  R3  reported, no expectation: relations added at each reach; whether a short reach leaves the filter unable to
      make a pattern hold at all, which would be destruction of a different kind (recorded as destroyed)
What each outcome means:
  R1 holds            -> the filter's REACH is the whole story. ED's sync requirement does not destroy space; a
                         filter allowed to reach too far does. What ED would then need to say is how far passing
                         on reaches - and A11 D4 already says "a neighbourhood".
  R1 fails, shapes die at every reach -> the sync requirement itself destroys shape, and road P's negative stands
                         as it is.
  patterns destroyed at reach 2 -> a filter that cannot reach cannot repair, so ED would be choosing between
                         keeping a shape and keeping its clocks: a genuine tension, and a real finding.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_11", "model"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
import n2_grow as G                                         # noqa: E402
import p_persist as P                                       # noqa: E402

OUT = os.path.join(HERE, "p_runs")
REACHES = (2, 3, 4)
SEEDS = (1, 2)
from scipy.sparse.csgraph import breadth_first_order       # noqa: E402


def _ball_exact(A, i, hops):
    """Events between two and `hops` relations away - near, but NOT already related to i.

    Recorded before the scan: road P used attempt 11's ball, which includes the events already related to i. At a
    reach of 2 most of that ball is already-related events, so the filter spent its additions on relations that
    already existed and the reach knob would not have meant what it says.
    """
    order, pred = breadth_first_order(A, i, directed=False, return_predecessors=True)
    d = np.full(A.shape[0], -1, dtype=np.int64)
    d[i] = 0
    for v in order[1:]:
        dv = d[pred[v]] + 1
        d[v] = dv if dv <= hops else -1
    return np.flatnonzero(d >= 2)


def set_reach(h):
    """The filter may only partner a strained event with one between two and h relations away."""
    G._ball = lambda A, i, hops=h: _ball_exact(A, i, hops)


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in ("ring", "grid3D"):
        for reach in REACHES:
            set_reach(reach)
            for seed in SEEDS:
                t0 = time.time()
                r = P.run(name, seed, True)
                r["reach"] = reach
                res.append(r)
                print("%-6s reach %d seed %d | n %5d -> %5d | reading %s -> %s (a real one reads %s) | kept %s | "
                      "destroyed %s | relations/event %.2f -> %.2f | repairs %d | %.0fs"
                      % (name, reach, seed, r["n0"], r["n"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"],
                         r["kept"], r["destroyed"], r["start"]["per_event"], r["final"]["per_event"],
                         sum(r["repairs"]), time.time() - t0), flush=True)
                json.dump(res, open(os.path.join(OUT, "reach.json"), "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s reach %d seed %d | %s -> %s (a real one reads %s) | md %.1f -> %.1f | kept %s | "
                     "destroyed %s | clocks held %s | relations/event %.2f -> %.2f | repairs %d"
                     % (r["start_name"], r["reach"], r["seed"], r["start"]["d_H"], r["final"]["d_H"], r["ref_d_H"],
                        r["start"]["md"], r["final"]["md"], r["kept"], r["destroyed"], r["held_every"],
                        r["start"]["per_event"], r["final"]["per_event"], sum(r["repairs"])))
    for reach in REACHES:
        at = [r for r in res if r["reach"] == reach]
        lines.append("reach %d | kept its shape: %s | destroyed: %s | relations per event: %s | repairs: %s"
                     % (reach, {r["start_name"] + str(r["seed"]): r["kept"] for r in at},
                        [r["start_name"] for r in at if r["destroyed"]],
                        {r["start_name"]: round(float(np.mean([x["final"]["per_event"] for x in at
                                                               if x["start_name"] == r["start_name"]])), 2)
                         for r in at},
                        {r["start_name"]: int(np.mean([sum(x["repairs"]) for x in at
                                                       if x["start_name"] == r["start_name"]])) for r in at}))
    r1 = all(r["kept"] and r["held_every"] for r in res if r["reach"] == 2)
    r2 = all(not r["kept"] for r in res if r["reach"] == 3)
    lines.append("R1 (at reach 2 the shapes are kept and the clocks hold) %s" % r1)
    lines.append("R2 (at reach 3 they are not - road P reproduced) %s" % r2)
    text = "\n".join(lines)
    open(os.path.join(HERE, "b_reach.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
