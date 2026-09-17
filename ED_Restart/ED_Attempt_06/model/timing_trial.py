"""Timing trial (note 11, running order step 1; IMPLEMENTATION_NOTES.md).

Central setting, N_final = 1,000, seed 0, readings off. Timing only: no
readings are taken or recorded. There are no expected results for timing.
"""
import json
import time
import numpy as np
from cgp import CGP


def main():
    t0 = time.perf_counter()
    g = CGP(K_over_sigma=10, c=1.0, k_max=12, kappa_min=-0.1, N_final=1000, seed=0)
    g.run(on_checkpoint=None)
    total = time.perf_counter() - t0
    tm = g.timers
    rep = dict(total_s=total, growth_s=g.growth_time, rest_s=getattr(g, "rest_time", 0.0),
               growth_ticks=g.growth_ticks, rest_ticks=getattr(g, "rest_ticks", 0),
               loci=g.n, relations=g.m, stalled=g.stalled, timers=tm, counts=g.counts)
    print(json.dumps(rep, indent=2))

    # extrapolation (method fixed in IMPLEMENTATION_NOTES.md)
    other = total - tm["clock"] - tm["moves"]
    moves_ex_conn = tm["moves"] - tm["connect"]

    def est(N, control=False):
        s = N / 1000.0
        mv = moves_ex_conn - (tm["curvature"] if control else 0.0)
        return tm["clock"] * s ** 2 + mv * s + tm["connect"] * s ** 2 + other * s

    def plan(largest):
        sizes = [1000, 4000, largest]
        central = sum(5 * est(N) for N in sizes)
        central_ctrl = sum(5 * est(N, True) for N in sizes)
        scan = 108 * 3 * est(4000)
        scan_ctrl = 108 * 3 * est(4000, True)
        return central, central_ctrl, scan, scan_ctrl

    lines = []
    for largest in (16000, 8000, 4000):
        ce, cc, sc, scc = plan(largest)
        tot = ce + cc + sc + scc
        lines.append(f"largest size {largest}: central {ce/3600:.1f} h, central control {cc/3600:.1f} h, "
                     f"scan {sc/3600:.1f} h, scan control {scc/3600:.1f} h; total {tot/3600:.1f} core-hours "
                     f"= {tot/3600/8:.1f} wall-clock hours on 8 cores")
    for budget in (24, 72, 168):
        chosen = None
        for largest in (16000, 8000, 4000):
            if sum(plan(largest)) / 3600 / 8 <= budget:
                chosen = largest
                break
        lines.append(f"budget {budget} h: halving rule gives largest size {chosen if chosen else 'none (scan at 4,000 alone does not fit)'}")
    lines.append(f"one run at 4,000 (constrained) estimated {est(4000)/60:.1f} min; at 16,000 {est(16000)/3600:.2f} h")
    for l in lines:
        print(l)
    with open("timing_trial_run1.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(rep, indent=2) + "\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
