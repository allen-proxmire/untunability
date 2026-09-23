"""ED's own readings: dimension as independent directions, distance as participation resistance.

Every reading used in thirteen attempts has been borrowed - ball growth, hop-count distance, a small-world flag
taken from the network literature. Paper 10 (February 2026, 'Event Density and the Emergence of Spacetime') defines
both quantities in ED's own terms, and they are not the same things:

    S3.5  "The number of effective dimensions is the number of INDEPENDENT PARTICIPATION DIRECTIONS available
          at scale."
    S3.2  "Distance as Participation Resistance" - two regions feel distant when participation bandwidth between
          them is low; distance is "the macroscopic measure of participation resistance".

Both have exact counterparts on a pattern of events and relations:

  DIRECTIONS  the pattern's slowest modes come in groups. On a ring the lowest non-trivial group has two members,
              on a flat torus four, on a cubic torus six - two per independent direction. The size of that group,
              halved, is the number of independent directions available at scale. A pattern with no such grouping
              has no definite number of directions.
  RESISTANCE  the effective resistance between two events, which is exactly "participation bandwidth" read as a
              network quantity: many short paths means low resistance, few or long paths means high. How resistance
              grows with separation gives a dimension: on a line it grows in proportion to separation, on a flat
              sheet like its logarithm, and in three dimensions it stops growing at all.

THE GATE, fixed before this file was run. Allen's caveat, recorded: these definitions are early work and are being
tried, not assumed.
  I0  On shapes we already know, ED's own readings must give: ring 1, flat torus 2, cubic torus 3, and no definite
      answer for a random web. **If I0 fails, these instruments are not usable and nothing measured with them
      counts.** No result from them will be reported unless this passes.
  I1  On ED's own grown patterns, the two ED readings agree with each other (within 0.5)
  I2  They agree with ball growth about whether there is a definite dimension at all
  I3  Reported: the values, for every start already run
If I2 fails - if ED's own readings find a definite dimension where ball growth found none - that is the single most
important result this project could produce, and it would need repeating at more sizes and seeds before being said
aloud.
"""
import io
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh, cg
from scipy.sparse.csgraph import breadth_first_order, shortest_path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import l_local as L                                         # noqa: E402
import l_local2 as L2                                       # noqa: E402
import g_grad as G                                          # noqa: E402

OUT = os.path.join(HERE, "e_runs")
NMODES = 24
CLUSTER_TOL = 0.25    # two modes count as the same group if they differ by less than this, relatively


def laplacian(A):
    d = np.asarray(A.sum(axis=1)).ravel()
    return (sp.diags(d) - A).tocsc()


def directions(A, nmodes=NMODES, tol=CLUSTER_TOL):
    """S3.5: the number of independent participation directions available at scale.

    The slowest modes come in groups; the lowest non-trivial group has two members per direction.
    Returns (directions, group size, the modes themselves).
    """
    Lap = laplacian(A)
    k = min(nmodes, A.shape[0] - 2)
    try:
        vals = eigsh(Lap, k=k, sigma=-1e-6, which="LM", return_eigenvectors=False, maxiter=5000)
    except Exception:
        return None, None, None
    vals = np.sort(np.real(vals))
    vals = vals[vals > 1e-8]
    if len(vals) < 3:
        return None, None, None
    first = vals[0]
    group = int(np.sum(vals <= first * (1.0 + tol)))
    if group >= len(vals):                                   # no gap found within the modes we looked at
        return None, group, vals[:8]
    return group / 2.0, group, vals[:8]


def resistance_dim(A, rng, pairs=60):
    """S3.2: distance as participation resistance, and how it grows with separation.

    Effective resistance R(u,v) between sampled pairs against their separation r.
    Slope s of log R against log r gives the dimension: d = 2 - s (s = 1 in one dimension, 0 in three).
    """
    n = A.shape[0]
    Lap = laplacian(A).tocsr()
    src = int(rng.integers(n))
    order, pred = breadth_first_order(A, src, directed=False, return_predecessors=True)
    d = np.full(n, -1)
    d[src] = 0
    for v in order[1:]:
        d[v] = d[pred[v]] + 1
    reach = np.flatnonzero(d > 0)
    if len(reach) < 20:
        return None, None, None
    rs, Rs = [], []
    for _ in range(pairs):
        v = int(reach[int(rng.integers(len(reach)))])
        b = np.zeros(n)
        b[src] = 1.0
        b[v] = -1.0
        x, info = cg(Lap, b, rtol=1e-8, maxiter=3000)
        rs.append(float(d[v]))
        Rs.append(float(x[src] - x[v]))
    rs, Rs = np.asarray(rs), np.asarray(Rs)
    ok = (rs > 1) & (Rs > 0)
    if ok.sum() < 8:
        return None, None, None
    s = float(np.polyfit(np.log(rs[ok]), np.log(Rs[ok]), 1)[0])
    return 2.0 - s, s, float(Rs[ok].mean())


def read_both(A, rng):
    t0 = time.time()
    dirs, group, modes = directions(A)
    rdim, slope, rmean = resistance_dim(A, rng)
    return dict(directions=None if dirs is None else round(dirs, 2), group=group,
                modes=None if modes is None else [round(float(v), 5) for v in modes[:6]],
                resistance_dim=None if rdim is None else round(rdim, 2),
                resistance_slope=None if slope is None else round(slope, 3),
                mean_resistance=None if rmean is None else round(rmean, 4), secs=round(time.time() - t0, 1))


def grown(name, seed):
    """Regenerate a grown end-state pattern exactly as C5's run produced it, and keep the pattern itself."""
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    omega = rng.normal(0, 1, len(adj))
    omega -= omega.mean()
    sp_pass = G.SIGMA_PASS * float(omega.std())
    committed = set()
    target = G.GROW * len(adj)
    while len(adj) < target:
        adj, committed, omega = G.inherit_rates(adj, committed, omega, rng, sp_pass)
        omega = G.diffuse(adj, omega, G.ALPHA)
        omega -= omega.mean()
        adj, a, ok = L.repair(adj, omega, rng, L.K0)
        if not ok:
            break
        adj, committed, g = L2.dissolve_uncommitted(adj, committed, omega, rng, L.K0)
    return P.to_A(adj)


def main():
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(5)
    res = {"gate": {}, "grown": {}}
    lines = []

    known = (("ring (should read 1)", N1.ring(4096, rng), 1.0),
             ("flat torus (should read 2)", N1.torus2(64, rng), 2.0),
             ("cubic torus (should read 3)", N1.torus3(16, rng), 3.0),
             ("random web (should read nothing definite)", N1.rand_regular(4096, rng), None))
    for label, A, want in known:
        r = read_both(A, np.random.default_rng(1))
        res["gate"][label] = r
        lines.append("%-42s | directions %s (group of %s) | resistance dimension %s (slope %s) | modes %s"
                     % (label, r["directions"], r["group"], r["resistance_dim"], r["resistance_slope"], r["modes"]))
    ok_dirs = []
    for (label, A, want), key in zip(known, res["gate"]):
        r = res["gate"][key]
        if want is None:
            ok_dirs.append(r["directions"] is None or abs(r["directions"]) > 4)
        else:
            ok_dirs.append(r["directions"] is not None and abs(r["directions"] - want) <= 0.5)
    ok_res = []
    for (label, A, want), key in zip(known, res["gate"]):
        r = res["gate"][key]
        if want is not None:
            ok_res.append(r["resistance_dim"] is not None and abs(r["resistance_dim"] - want) <= 0.7)
    i0 = all(ok_dirs) and all(ok_res)
    lines.append("")
    lines.append("I0 THE GATE (ED's own readings reproduce known shapes) %s" % i0)
    if not i0:
        lines.append("   ** GATE FAILED: these instruments are not usable, and nothing below is reported as a "
                     "result. Which part failed is in the table above. **")
    for name in ("ring", "grid3D", "web"):
        for seed in (1, 2):
            A = grown(name, seed)
            r = read_both(A, np.random.default_rng(3))
            res["grown"]["%s_%d" % (name, seed)] = r
            lines.append("grown from %-6s seed %d | n %5d | directions %s (group of %s) | resistance dimension %s"
                         " (slope %s) | modes %s"
                         % (name, seed, A.shape[0], r["directions"], r["group"], r["resistance_dim"],
                            r["resistance_slope"], r["modes"]))
            print(lines[-1], flush=True)
            json.dump(res, open(os.path.join(OUT, "ed_readings.json"), "w"), indent=1, default=str)
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "ed_readings.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
