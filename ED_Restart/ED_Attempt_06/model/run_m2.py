"""One M2 job: grow, rest, take readings at 5 checkpoints (note 13; IMPLEMENTATION_NOTES.md, M2 runs section)."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import json
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.linalg import lsqr
from m2 import M2
from readings_v2 import all_readings

OUT = "m2_runs"


def job_name(j):
    kap = "none" if not np.isfinite(j["kappa_min"]) else f"{j['kappa_min']:+.1f}"
    return f"{j['kind']}_K{j['K']:g}_c{j['c']:g}_k{j['k_max']}_kap{kap}_N{j['N']}_s{j['seed']}"


def sync_fraction(Om, tau):
    """R7: largest share of loci whose rates fit in a window of width 2 tau (within tau of its centre)."""
    s = np.sort(Om)
    j, best = 0, 0
    for i in range(len(s)):
        while s[i] - s[j] > 2 * tau:
            j += 1
        best = max(best, i - j + 1)
    return best / len(s)


def mean_pair_distance(g, pairs):
    A = g.to_csr()
    src = np.unique(pairs[:, 0])
    D = shortest_path(A, method="D", unweighted=True, indices=src)
    row = {s: i for i, s in enumerate(src)}
    return float(np.mean([D[row[u], v] for u, v in pairs]))


def sample_pairs(rng, n, k=200):
    u = rng.integers(0, n, size=4 * k)
    v = rng.integers(0, n, size=4 * k)
    keep = u != v
    return np.stack([u[keep], v[keep]], axis=1)[:k]


def moving_basis(n, edges, arc_index):
    """Columns spanning the moving sector {d* f, S d* g} on the union arc space."""
    deg = np.bincount(edges.ravel(), minlength=n)
    rows_d, cols_d, vals = [], [], []
    rows_s, cols_s = [], []
    for u, v in edges:
        for a, b in ((u, v), (v, u)):
            i = arc_index[(a, b)]
            rows_d.append(i)
            cols_d.append(a)
            vals.append(1.0 / np.sqrt(deg[a]))
            rows_s.append(arc_index[(b, a)])
            cols_s.append(a)
    M = len(arc_index)
    Dt = sp.csr_matrix((vals, (rows_d, cols_d)), shape=(M, n))       # d*: locus value -> its outgoing arcs
    SDt = sp.csr_matrix((vals, (rows_s, cols_s)), shape=(M, n))      # S d*: onto the reversed arcs
    return sp.hstack([Dt, SDt]).tocsr()


class M2Job(M2):
    """M2 with a leakage probe on accepted rewires during rest (R9, N_final = 1,000 central only)."""
    leak_target = 0
    probing = False

    def _rewire(self):
        if not (self.probing and len(self.leaks) < self.leak_target):
            return super()._rewire()
        old = np.stack([self.ei[: self.m].copy(), self.ej[: self.m].copy()], axis=1)
        before = self.counts["rew_acc"]
        super()._rewire()
        if self.counts["rew_acc"] == before:
            return
        new = np.stack([self.ei[: self.m].copy(), self.ej[: self.m].copy()], axis=1)
        arcs = {}
        for E in (old, new):
            for u, v in E:
                for key in ((int(u), int(v)), (int(v), int(u))):
                    if key not in arcs:
                        arcs[key] = len(arcs)
        Bo = moving_basis(self.n, old, arcs)
        Bn = moving_basis(self.n, new, arcs)
        vals = []
        for _ in range(20):
            psi = Bo @ self.rng_probe.normal(size=Bo.shape[1])
            psi /= np.linalg.norm(psi)
            x = lsqr(Bn, psi, atol=1e-12, btol=1e-12, iter_lim=20000)[0]
            vals.append(float(np.sum((psi - Bn @ x) ** 2)))
        self.leaks.append(float(np.mean(vals)))


def run_job(j):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, job_name(j) + ".json")
    if os.path.exists(path):
        return path
    t0 = time.perf_counter()
    g = M2Job(K_over_sigma=j["K"], c=j["c"], k_max=j["k_max"], kappa_min=j["kappa_min"], N_final=j["N"], seed=j["seed"])
    g.leaks = []
    g.rng_probe = np.random.default_rng(10_000 + j["seed"])
    g.leak_target = 200 if j.get("leak") else 0
    rng_pairs = np.random.default_rng(20_000 + j["seed"])
    N = j["N"]
    marks = [int(round(f * N)) for f in (0.25, 0.5, 0.75, 1.0)]
    growth_pairs, r10_growth, mi = None, [], 0
    while g.n < N and not g.stalled:
        g.tick(births=True)
        while mi < 4 and g.n >= marks[mi]:
            if mi == 0:
                growth_pairs = sample_pairs(rng_pairs, g.n)
            r10_growth.append(mean_pair_distance(g, growth_pairs))
            mi += 1
    res = dict(job=j, name=job_name(j), stalled=bool(g.stalled), loci=int(g.n), relations=int(g.m),
               growth_ticks=int(g.t), r10_growth=r10_growth, checkpoints=[])
    if not g.stalled:
        E0 = g.m
        target = 20 * E0
        start = g.counts["rew_att"]
        rest_pairs = sample_pairs(rng_pairs, g.n)
        cmarks = [int(round(f * target)) for f in (0.0, 0.25, 0.5, 0.75, 1.0)]
        ci = 0
        g.probing = True
        while True:
            done = g.counts["rew_att"] - start
            while ci < 5 and done >= cmarks[ci]:
                A = g.to_csr()
                r = all_readings(A, np.random.default_rng(30_000 + 10 * j["seed"] + ci))
                r["R7"] = sync_fraction(g.Omega[: g.n], g.tau)
                rngk = np.random.default_rng(40_000 + 10 * j["seed"] + ci)
                pick = rngk.choice(g.m, size=min(1000, g.m), replace=False)
                kap = [g.curvature(int(g.ei[p]), int(g.ej[p])) for p in pick]
                r["R8_mean"], r["R8_p5"] = float(np.mean(kap)), float(np.percentile(kap, 5))
                r["R10_rest"] = mean_pair_distance(g, rest_pairs)
                r["checkpoint"] = ci
                res["checkpoints"].append({k: (float(v) if isinstance(v, (np.floating,)) else v) for k, v in r.items()})
                ci += 1
            if done >= target:
                break
            g.tick(births=False)
    res["leakage"] = g.leaks
    res["counts"] = g.counts
    res["seconds"] = time.perf_counter() - t0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, default=lambda o: None if o is None else (bool(o) if isinstance(o, np.bool_) else str(o)))
    os.replace(tmp, path)
    return path
