"""C3b timing trial (note 16 running order; D23). Timing and harness checks only: no signal values printed.

One seed (0) of each stand-in at each size: construction, sync solve, degree stats and readings,
timed. Harness facts printed: connected, degree conditions (E1), solve residual, redraws, whether
readings were defined. Projection for 45 jobs on 6 workers.
"""
import time
import numpy as np
from c3b import KINDS, SIZES, MAKERS, connected, sync_steady_state, readings, degree_stats

lines, per = [], {}
for kind in KINDS:
    for N in SIZES[kind]:
        t0 = time.perf_counter(); A, info = MAKERS[kind](N, 0); t_make = time.perf_counter() - t0
        t0 = time.perf_counter(); s = sync_steady_state(A, 0); t_solve = time.perf_counter() - t0
        d = degree_stats(A)
        t0 = time.perf_counter(); r = readings(A, 0); t_read = time.perf_counter() - t0
        per[(kind, N)] = t_make + t_solve + t_read
        extra = ""
        if kind == "B":
            extra = f", tree edges {info['tree_edges']} of {info['blocks']} blocks"
        lines.append(f"{kind} N={A.shape[0]}: build {t_make:.1f} s (redraws {info['redraws']}{extra}), solve {t_solve:.1f} s "
                     f"({s['method']}, residual {s['residual']:.1e}), readings {t_read:.1f} s (d_H defined: "
                     f"{r['d_H'] is not None and np.isfinite(r['d_H'])}); connected {connected(A)}; "
                     f"degree mean/min/max {d['mean_degree']:.2f}/{d['min_degree']}/{d['max_degree']}")
        print(lines[-1], flush=True)
tot = 3 * sum(per.values())
lines.append(f"projected 45 jobs: {tot/60:.1f} min single process, {tot/60/6:.1f} min on 6 workers")
print(lines[-1])
open("c3b_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
