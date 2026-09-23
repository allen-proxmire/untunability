"""Scale-resolved spectral dimension of a grown slice (diagnostic, not pre-registered).

The runs report one fitted d_s over the ball-growth window, which for grown slices is radii 2-4 at
every size while flat's window grows 3-6, 4-8, 7-14. So every d_s in hand describes a two-hop span
at short range. This re-grows a slice exactly - the port's generator is seeded, so the same seed
gives the same slice - and reads the spectral dimension as a function of walk radius instead.
"""
import json
import os
import sys
import time
import numpy as np
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING
from p3_dscurve import d_s_curve

T = 150
OUT = "e4_runs"


def regrow(n, seed, s_max):
    M = Slice3P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = round(FLAT_LINKS_PER_EVENT * V0) - M.E
    for t in range(T):
        r, pool, kids, absd = M.tick(1.0, 1.0, pool, s_max=s_max, cap=CEILING)
    return M


def main(n, seed, t_cap):
    base = json.load(open(os.path.join(OUT, "cal_FC_n%d_r0.json" % n), encoding="utf-8"))["strain_median"]
    s_max = 0.45 * base
    t0 = time.perf_counter()
    M = regrow(n, seed, s_max)
    ref = json.load(open(os.path.join(OUT, "grow_n%d_s%d.json" % (n, seed)), encoding="utf-8"))
    same = (M.V == ref["events"] and M.E == ref["links"])
    print("regrown n=%d seed %d in %.0f s: V %d E %d | matches the run: %s"
          % (n, seed, time.perf_counter() - t0, M.V, M.E, same), flush=True)
    if not same:
        print("  the re-grown slice is NOT the run's slice; the curve below is a different slice.")
    A, ids, pos, ei, ej = M.adjacency()
    c = d_s_curve(A, seed, t_cap=t_cap)
    c["n"] = n
    c["seed"] = seed
    c["matches_run"] = bool(same)
    c["run_d_s"] = (ref.get("slice") or {}).get("d_s")
    c["run_r_lo"] = (ref.get("slice") or {}).get("r_lo")
    c["run_r_max"] = (ref.get("slice") or {}).get("r_max")
    c["diameter"] = (ref.get("slice") or {}).get("diameter")
    path = os.path.join(OUT, "dscurve_n%d_s%d.json" % (n, seed))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, default=str)
    print("  the run fitted d_s = %s over radii %s-%s; diameter %s"
          % (c["run_d_s"], c["run_r_lo"], c["run_r_max"], c["diameter"]))
    print("  %8s %10s %9s" % ("t", "radius", "d_s"))
    for i in range(len(c["t"])):
        print("  %8d %10.2f %9.3f" % (c["t"][i], c["radius"][i], c["d_s"][i]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]), int(sys.argv[2]),
                          int(sys.argv[3]) if len(sys.argv) > 3 else 4000))
