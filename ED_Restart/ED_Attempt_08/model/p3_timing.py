"""Timing for the port (E2). Per-tick cost with the structure check timed separately.

Note 2's rule: no per-tick time is quoted as a result until tiers 1 and 2 of the ladder pass.
This script only measures; `p3_verify.py` is what licenses quoting it.

Settings follow C3g: A = commitment and curvature (alpha = lam = 1, no sync), B = the same with the
sync condition, D = no pressure. The sync threshold is 1.5 x the flat calibration's largest link
strain at that size, as in C3f/C3g (D41).
"""
import sys
import time
import numpy as np
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING

SETTINGS = {"A": (1.0, 1.0, False), "B": (1.0, 1.0, True), "D": (0.0, 0.0, False)}
WARM = 2


def setup(n, seed):
    M = Slice3P(n)
    M.seed(seed)
    V0 = M.V
    rng = np.random.default_rng(seed)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    return M, BL, BL - M.E


def flat_strain(n, seed):
    """The flat calibration's largest link strain, as C3f sets the threshold from."""
    from c3b import sync_steady_state
    M = Slice3P(n)
    A, ids, pos, ei, ej = M.adjacency()
    return float(sync_steady_state(A, seed)["max_link_diff"])


def main(sizes, ticks):
    out = []
    for n in sizes:
        t0 = time.perf_counter()
        s_max = 1.5 * flat_strain(n, 0)
        cal_s = time.perf_counter() - t0
        out.append("n=%d (V=%d): flat calibration largest link strain %.3f -> sync threshold %.3f (%.1f s)"
                   % (n, n ** 3, s_max / 1.5, s_max, cal_s))
        for name, (alpha, lam, use_sync) in SETTINGS.items():
            M, BL, pool = setup(n, 0)
            sm = s_max if use_sync else None
            tt = []
            ct = []
            last = None
            for t in range(WARM + ticks):
                a = time.perf_counter()
                r, pool, kids, absd = M.tick(alpha, lam, pool, s_max=sm, cap=CEILING)
                b = time.perf_counter()
                notes = M.check()
                c = time.perf_counter()
                if notes:
                    out.append("  %s: STRUCTURE FAIL at tick %d: %s" % (name, t + 1, notes[:2]))
                    break
                if t >= WARM:
                    tt.append(b - a)
                    ct.append(c - b)
                last = r
            if not tt:
                continue
            out.append("  %s: tick %.3f s, check %.3f s, total %.3f s; V %d, E %d, E+pool %d/%d; "
                       "refusals per tick budget/cap/sync/splits %d/%d/%d/%d"
                       % (name, float(np.mean(tt)), float(np.mean(ct)), float(np.mean(tt)) + float(np.mean(ct)),
                          last["size"], last["links"], last["links"] + pool, BL,
                          last["refused_budget"], last["refused_cap"], last["refused_sync"],
                          last["split_refused"]))
        print("\n".join(out[-4:]), flush=True)
    text = "\n".join(out)
    with open("p3_timing.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return text


if __name__ == "__main__":
    sizes = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [20, 24]
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    main(sizes, ticks)
