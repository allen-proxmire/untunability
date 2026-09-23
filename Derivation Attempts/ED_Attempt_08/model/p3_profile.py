"""Where the port's tick time goes (diagnostic, not a pre-registered result)."""
import time
import numpy as np
from numba import njit
from p3 import Slice3P, link_condition, merge_plan
from p3_ops import allowed, delta_S


@njit(cache=True)
def bench_lc(S, ids, reps):
    c = 0
    for r in range(reps):
        for i in range(ids.shape[0]):
            v = ids[i]
            sn = S.v_ns[v]
            for j in range(S.v_nl[v]):
                if link_condition(S, v, S.an_data[sn + j]):
                    c += 1
    return c


@njit(cache=True)
def bench_plan(S, ids, reps):
    c = 0
    for r in range(reps):
        for i in range(ids.shape[0]):
            v = ids[i]
            sn = S.v_ns[v]
            for j in range(S.v_nl[v]):
                nr, na = merge_plan(S, v, S.an_data[sn + j], 0)
                c += nr
    return c


@njit(cache=True)
def bench_allowed(S, ids, reps):
    c = 0
    for r in range(reps):
        for i in range(ids.shape[0]):
            v = ids[i]
            sn = S.v_ns[v]
            for j in range(S.v_nl[v]):
                nr, na = merge_plan(S, v, S.an_data[sn + j], 0)
                ok, b, d, w = allowed(S, 0, nr, na, 1000, -1.0, v, 60)
                c += b
    return c


@njit(cache=True)
def bench_both(S, ids, reps):
    c = 0.0
    for r in range(reps):
        for i in range(ids.shape[0]):
            v = ids[i]
            sn = S.v_ns[v]
            for j in range(S.v_nl[v]):
                nr, na = merge_plan(S, v, S.an_data[sn + j], 0)
                ok, b, d, w = allowed(S, 0, nr, na, 1000, -1.0, v, 60)
                c += delta_S(S, 0, nr, na, 1.0, 1.0)
    return c


def main():
    n = 16
    M = Slice3P(n)
    ids = M.vertices()[:400].astype(np.int32)
    npairs = int(sum(M.degree(v) for v in ids))
    prev = 0.0
    for name, fn in (("link_condition", bench_lc), ("+ merge_plan", bench_plan),
                     ("+ allowed", bench_allowed), ("+ delta_S", bench_both)):
        fn(M.S, ids[:5], 1)
        t0 = time.perf_counter()
        fn(M.S, ids, 3)
        dt = (time.perf_counter() - t0) / 3
        us = dt / npairs * 1e6
        print("%-16s %7.2f us/pair  (step +%.2f)" % (name, us, us - prev))
        prev = us
    print("candidate pairs per tick at V=%d: about %d" % (M.V, 0.5 * M.V * 14))


if __name__ == "__main__":
    main()
