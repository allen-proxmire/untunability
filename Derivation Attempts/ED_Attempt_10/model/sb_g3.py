"""Gate G3 (notes 7, 14): can the readings tell the flat start from the crowded start at the run sizes?
Readings: slice mean distance at n = 12 and 16 and its growth rate ln(md16/md12)/ln(V16/V12); spacetime ball-growth
reading (A9's method) on a stack of the slice copied T_READ times with the identity parent map.
Pass (written in note 7 before any code): the two starts differ by >= 0.1 in growth rate and >= 1.0 in the spacetime
reading, at both sizes; else sizes rise (recorded)."""
import json
import math
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sb_build as b  # noqa: E402
import sa_count as sc  # noqa: E402

T_READ = 16


def stack_reading(M, seed):
    from p3_readings import spacetime_readings
    e = M.edges()
    vs = [int(v) for v in M.vertices()]
    kids = np.array([(v, v) for v in vs], dtype=np.int32)
    snaps = [(e, kids, np.zeros((0, 2), np.int32)) for _ in range(T_READ)]
    return spacetime_readings(snaps, seed).get("d_H")


def main():
    out = {}
    for n in (12, 16):
        F = b.flat_reference(n)
        C = b.crowded_grown(F)   # REVISION (D16): strongly crowded start at exact counts; run 1 kept in sb_g3_run1.json
        for tag, M in (("flat", F), ("crowded", C)):
            d = [len(M.neighbours(int(v))) for v in M.vertices()]
            out["%s_%d" % (tag, n)] = dict(V=M.V, E=M.E, md=sc.mean_distance(M.adjacency()[0], 0),
                                           deg_sd=float(np.std(d)), deg_max=int(max(d)), spacetime=stack_reading(M, 7))
            print(tag, n, out["%s_%d" % (tag, n)], flush=True)
    for tag in ("flat", "crowded"):
        a, c = out["%s_12" % tag], out["%s_16" % tag]
        out["rate_" + tag] = math.log(c["md"] / a["md"]) / math.log(c["V"] / a["V"])
    out["rate_gap"] = out["rate_flat"] - out["rate_crowded"]
    out["st_gap_12"] = (out["crowded_12"]["spacetime"] or 0) - (out["flat_12"]["spacetime"] or 0)
    out["st_gap_16"] = (out["crowded_16"]["spacetime"] or 0) - (out["flat_16"]["spacetime"] or 0)
    out["G3_pass"] = out["rate_gap"] >= 0.1 and out["st_gap_12"] >= 1.0 and out["st_gap_16"] >= 1.0
    json.dump(out, open(os.path.join(HERE, "sb_g3.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("rate_flat", "rate_crowded", "rate_gap", "st_gap_12", "st_gap_16", "G3_pass")}))


if __name__ == "__main__":
    main()
