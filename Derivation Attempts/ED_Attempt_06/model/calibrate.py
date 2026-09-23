"""Calibrations for the readings (note 11, E0; choices in IMPLEMENTATION_NOTES.md).

Expected results, written down before the first run (note 11, E0):
  3D periodic random geometric graph and 3D periodic cubic grid:
      d_H and d_s in [2.6, 3.4], d_w in [1.8, 2.2], beta in [0.55, 0.78].
  2D periodic random geometric graph: d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2].
  Random 12-regular graph: small-world flag raised.
"""
import json
import time
import numpy as np
import scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from readings import all_readings


def to_csr(n, pairs):
    pairs = np.asarray(pairs, dtype=np.int64)
    r = np.concatenate([pairs[:, 0], pairs[:, 1]])
    c = np.concatenate([pairs[:, 1], pairs[:, 0]])
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
    A.data[:] = 1.0
    return A


def largest_component(A):
    _, lab = connected_components(A, directed=False)
    big = np.argmax(np.bincount(lab))
    keep = np.where(lab == big)[0]
    return A[keep][:, keep].tocsr(), len(keep)


def rgg(n, dim, mean_deg, rng):
    pts = rng.random((n, dim))
    if dim == 3:
        r = (mean_deg / (n * 4.0 / 3.0 * np.pi)) ** (1 / 3)
    else:
        r = (mean_deg / (n * np.pi)) ** 0.5
    pairs = cKDTree(pts, boxsize=1.0).query_pairs(r, output_type="ndarray")
    return largest_component(to_csr(n, pairs))


def cubic_grid(L):
    idx = np.arange(L ** 3).reshape(L, L, L)
    pairs = []
    for ax in range(3):
        pairs.append(np.stack([idx.ravel(), np.roll(idx, -1, axis=ax).ravel()], axis=1))
    return to_csr(L ** 3, np.concatenate(pairs)), L ** 3


def random_regular(n, d, rng):
    stubs = np.repeat(np.arange(n), d)
    rng.shuffle(stubs)
    edges = [tuple(sorted((int(stubs[2 * i]), int(stubs[2 * i + 1])))) for i in range(len(stubs) // 2)]
    from collections import Counter
    cnt = Counter(edges)
    good = []
    bad = []
    seen = set()
    for e in edges:
        if e[0] == e[1] or cnt[e] > 1 and e in seen:
            bad.append(e)
        else:
            good.append(e)
            seen.add(e)
    eset = set(good)
    while bad:
        u, v = bad.pop()
        while True:
            k = rng.integers(len(good))
            x, y = good[k]
            if rng.random() < 0.5:
                x, y = y, x
            e1 = tuple(sorted((u, x)))
            e2 = tuple(sorted((v, y)))
            if u != x and v != y and e1 != e2 and e1 not in eset and e2 not in eset:
                eset.discard(good[k])
                good[k] = e1
                good.append(e2)
                eset.add(e1)
                eset.add(e2)
                break
    return largest_component(to_csr(n, good))


def within(x, lo, hi):
    return bool(np.isfinite(x) and lo <= x <= hi)


def main():
    rng_build = np.random.default_rng(1)
    rng_read = np.random.default_rng(2)
    results = {}
    lines = []
    ok_all = True
    builds = [
        ("3D random geometric (mean 12)", lambda: rgg(16000, 3, 12, rng_build), "3d"),
        ("3D cubic grid 25^3", lambda: cubic_grid(25), "3d"),
        ("2D random geometric (mean 8)", lambda: rgg(16000, 2, 8, rng_build), "2d"),
        ("random 12-regular", lambda: random_regular(16000, 12, rng_build), "rr"),
    ]
    for name, build, kind in builds:
        t0 = time.perf_counter()
        A, size = build()
        r = all_readings(A, rng_read)
        r["component_size"] = size
        r["seconds"] = round(time.perf_counter() - t0, 1)
        if kind == "3d":
            ok = (within(r["d_H"], 2.6, 3.4) and within(r["d_s"], 2.6, 3.4)
                  and within(r["d_w"], 1.8, 2.2) and within(r["beta"], 0.55, 0.78))
        elif kind == "2d":
            ok = within(r["d_H"], 1.7, 2.3) and within(r["d_s"], 1.7, 2.3) and within(r["d_w"], 1.8, 2.2)
        else:
            ok = bool(r["small_world"])
        ok_all &= ok
        results[name] = {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in r.items()}
        line = (f"{name}: {'AS EXPECTED' if ok else 'NOT AS EXPECTED'}  N={r['N']} (component {size}), "
                f"mean degree={r['mean_degree']:.3f}, r_max={r['r_max']}, d_H={r['d_H']:.3f}, beta={r['beta']:.3f}, "
                f"d_s={r['d_s']:.3f}, d_w={r['d_w']:.3f}, R5={r['R5']:.3f}, small_world={r['small_world']}, "
                f"R2 power/exp={r['r2_power']:.4f}/{r['r2_exp']:.4f}, cv_mid={r['cv_mid']:.3f}, "
                f"t_end={r['t_end']} (capped {r['t_capped']}), {r['seconds']} s")
        print(line, flush=True)
        lines.append(line)
    verdict = "E0: ALL AS EXPECTED" if ok_all else "E0: SOME NOT AS EXPECTED (exit rule X0 applies)"
    print(verdict)
    lines.append(verdict)
    with open("calibration_run1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open("calibration_run1.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == "__main__":
    main()
