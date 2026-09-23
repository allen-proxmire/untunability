"""Time one n = 52 spacetime reading (note 3, C19; D6). The one unmeasured number in E3b's plan.

Note 3's rule, inherited from E2: the campaign is not planned until a single n = 52 spacetime
reading has been timed. At n = 24 the pattern is about 292,000 events and ball growth took 16 s;
at n = 52 it is about 1.5 million.

This grows KEEP + 1 ticks at n = 52 from the flat start, builds the spacetime pattern and times the
reading. It is a timing run, not a result: 21 ticks is nowhere near the 150 a real run takes, so the
pattern's shape means nothing - only its size and the reading's cost do.
"""
import json
import time
import numpy as np
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING
from p3_readings import spacetime_readings

N = 52
KEEP = 20


def main():
    t0 = time.perf_counter()
    M = Slice3P(N)
    M.seed(0)
    V0 = M.V
    rng = np.random.default_rng(0)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = round(FLAT_LINKS_PER_EVENT * V0) - M.E
    build = time.perf_counter() - t0
    snaps = []
    tt = []
    for t in range(1, KEEP + 2):
        a = time.perf_counter()
        edges = M.edges()
        r, pool, kids, absd = M.tick(1.0, 1.0, pool, s_max=None, cap=CEILING)
        snaps.append((edges, kids.copy(), absd.copy()))
        tt.append(time.perf_counter() - a)
        print("tick %2d  %.1f s  V %d" % (t, tt[-1], M.V), flush=True)
    snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
    t1 = time.perf_counter()
    st = spacetime_readings(snaps, 4000)
    read = time.perf_counter() - t1
    res = dict(n=N, V0=V0, build_seconds=build, mean_tick_seconds=float(np.mean(tt[2:])),
               spacetime_events=st.get("events"), spacetime_links=st.get("links"),
               spacetime_seconds=read, d_H=st.get("d_H"), r_lo=st.get("r_lo"), r_max=st.get("r_max"))
    print(json.dumps(res, indent=1, default=str))
    txt = ("n=%d: torus build %.0f s, tick %.1f s, spacetime pattern %s events / %s links from %d "
           "slices, reading %.0f s (d_H %s, radii %s-%s)"
           % (N, build, res["mean_tick_seconds"], res["spacetime_events"], res["spacetime_links"],
              KEEP + 2, read, res["d_H"], res["r_lo"], res["r_max"]))
    print(txt)
    with open("e3_spacetime_timing.txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n" + json.dumps(res, default=str) + "\n")


if __name__ == "__main__":
    main()
