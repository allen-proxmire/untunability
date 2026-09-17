"""Follow-up diagnostic (NOT pre-registered): what does a floor -0.2 job spend its time on?

The reduced plan has finished 16 control and 10 central jobs but no floor -0.2
job in 77 minutes (C75, C76 context). Running jobs write nothing until they
finish, so this runs one -0.2 job at the central knobs with readings OFF, at
N = 1,000 (a quarter of the scan's size), printing progress as it goes.

Timing and structure only: no readings are taken, nothing here is scored, and
the output is not a process result. It uses one core alongside the eight
workers, and stops itself at the cap below.
"""
import time
import numpy as np
from m2 import M2

CAP_MIN = 25.0


def main():
    g = M2(K_over_sigma=10, c=1.0, k_max=12, kappa_min=-0.2, N_final=1000, seed=0)
    t0 = time.perf_counter()
    last = 0
    phase = "growth"
    while True:
        el = (time.perf_counter() - t0) / 60
        if el > CAP_MIN:
            print(f"[{el:5.1f} min] CAP reached in {phase}: loci {g.n}, relations {g.m}, "
                  f"mean degree {2*g.m/max(g.n,1):.2f}, counts {g.counts}", flush=True)
            break
        if g.n < g.N_final and not g.stalled:
            g.tick(births=True)
        else:
            if phase == "growth":
                print(f"[{el:5.1f} min] growth done: loci {g.n}, relations {g.m}, mean degree {2*g.m/g.n:.2f}, "
                      f"stalled {g.stalled}, ticks {g.t}, counts {g.counts}, "
                      f"curvature {g.timers['curvature']:.0f} s of {time.perf_counter()-t0:.0f} s", flush=True)
                if g.stalled:
                    break
                phase = "rest"
                E0 = g.m
                target = 20 * E0
                start = g.counts["rew_att"]
                print(f"[{el:5.1f} min] rest: {target} rewire attempts to go", flush=True)
            done = g.counts["rew_att"] - start
            if done >= target:
                print(f"[{el:5.1f} min] rest done: loci {g.n}, relations {g.m}, mean degree {2*g.m/g.n:.2f}, "
                      f"counts {g.counts}, curvature {g.timers['curvature']:.0f} s", flush=True)
                break
            g.tick(births=False)
        if g.t - last >= 2000:
            last = g.t
            tot = time.perf_counter() - t0
            print(f"[{el:5.1f} min] {phase}: ticks {g.t}, loci {g.n}, relations {g.m}, "
                  f"mean degree {2*g.m/max(g.n,1):.2f}, births {g.counts['births']} (failed {g.counts['birth_fail']}), "
                  f"pulls accepted {g.counts['pull_acc']}, rewires accepted {g.counts['rew_acc']}, "
                  f"exact LPs {g.counts['lp']}, curvature {g.timers['curvature']:.0f} s "
                  f"({100*g.timers['curvature']/max(tot,1e-9):.0f}% of wall)", flush=True)


if __name__ == "__main__":
    main()
