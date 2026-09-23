"""M2 timing trial (note 13, running order step 1; IMPLEMENTATION_NOTES.md, M2 section).

Central setting (K/sigma = 10, c = 1, k_max = 12), N_final = 1,000, seed 0,
readings off. Two runs: constrained (kappa_min = -0.1) and control
(kappa_min = -inf). Timing only: no readings are taken or recorded, and there
are no expected results for timing. Plan estimates are reported only for runs
that reach N_final and finish the resting phase; a stalled run gets none.

Usage: python m2_timing_trial.py constrained|control
"""
import json
import sys
import time
import numpy as np
from m2 import M2


def main(which):
    kappa = -0.1 if which == "constrained" else -np.inf
    t0 = time.perf_counter()
    g = M2(K_over_sigma=10, c=1.0, k_max=12, kappa_min=kappa, N_final=1000, seed=0)
    g.run(on_checkpoint=None)
    total = time.perf_counter() - t0
    rep = dict(which=which, total_s=total, growth_s=g.growth_time, rest_s=getattr(g, "rest_time", 0.0),
               growth_ticks=g.growth_ticks, rest_ticks=getattr(g, "rest_ticks", 0),
               loci=g.n, relations=g.m, mean_degree=2 * g.m / g.n, stalled=g.stalled,
               timers=g.timers, counts=g.counts)
    lines = [json.dumps(rep, indent=2)]
    if g.stalled or g.n < 1000:
        lines.append("STALLED or short of N_final: no plan estimate (it would scale from a run that did not happen).")
    else:
        tm = g.timers
        other = total - tm["clock"] - tm["moves"]
        moves_ex_conn = tm["moves"] - tm["connect"]

        def est(N):
            s = N / 1000.0
            return tm["clock"] * s ** 2 + moves_ex_conn * s + tm["connect"] * s ** 2 + other * s

        for largest in (16000, 8000, 4000):
            central = sum(5 * est(N) for N in (1000, 4000, largest))
            scan = 108 * 3 * est(4000)
            lines.append(f"{which}, largest size {largest}: central {central/3600:.1f} core-h, scan {scan/3600:.1f} core-h; "
                         f"subtotal {(central+scan)/3600:.1f} core-h")
        lines.append(f"{which}: one run at 4,000 estimated {est(4000)/60:.1f} min; at 16,000 {est(16000)/3600:.2f} h")
    out = "\n".join(lines)
    print(out)
    with open(f"m2_timing_trial_{which}_run1.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
