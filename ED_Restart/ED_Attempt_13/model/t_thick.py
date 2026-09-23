"""Road T: does a stable dimension appear once participation is THICK? (C6, paper 11.)

Paper 11 (February 2026) says dimensionality does not exist at the micro-scale and appears only when participation
becomes thick: S1.2 lists "no dimensionality" among what the substrate lacks; S3.1 calls stable dimensionality a
"classical-regime feature, not a micro-event primitive"; S3.5 and S6.7 say that when participation is thin,
"dimensionality fluctuates". Every model in this project has run at about 3.2 relations per event - the thinnest
the rules allow, because of the minimality rule - which is exactly where ED says there is no dimension to find.

So this relaxes minimality and imposes thickness instead. Everything else is the gradient model (C4, C5): events
pass on once and are spent, neighbourhoods are inherited, a child's rate is its parent's plus a variation, and
rates diffuse toward their neighbours each tick. The relations added to reach the target thickness are COUSIN
relations - children of neighbouring parents - so thickness means a bigger local neighbourhood, not shortcuts.

The filter is not used to drive anything here: thickness is imposed, so the sync condition is CHECKED and reported
rather than repaired. That is T0.

THE RULE, fixed before this file was run. "A stable dimension" means:
  T1  the reading at the end differs from the reading early on by no more than 0.4, AND the small-world flag is
      clear at the end UNLESS a genuine 3D lattice of the same thickness also trips it. The 0.4 is not arbitrary:
      a real fixed-dimension object drifts under this instrument - a cubic torus reads 2.36 at about 2,200 events
      and 2.69 at about 8,000 (A12 C7's controls) - so a real dimension must be allowed that much instrument drift.
      INSTRUMENT FIX made at the smoke test and recorded before the run: the reference is matched in THICKNESS as
      well as dimension (a cubic torus widened to the same relations per event), because a real 3D lattice carrying
      25 relations per event trips the small-world flag too, and judging thick patterns against a 6-regular
      reference would penalise thickness itself.
  T2  if a thickness gives a stable reading, what value it takes (reported; between 2.5 and 3.5 would be three).
  T3  reported: whether the sync condition holds unaided at each thickness, and how the readings move with
      thickness overall.

EXPECTATIONS, fixed before running:
  T0  the sync condition holds unaided at every thickness (thick patterns have plenty of edge)        high
  T1  at least one thickness gives a stable reading                                                   about 35%
  T2  if one does, the value is between 2.5 and 3.5                                                   about 15%
  T3  reported, no expectation
If T1 fails at every thickness, then on ED's own account of where dimension lives, ED's rules do not produce one -
and per C6 that is the point at which the sequence of missing pieces becomes the finding.
"""
import io
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import l_local as L                                         # noqa: E402
import b_balance as B                                       # noqa: E402
import g_grad as G                                          # noqa: E402

OUT = os.path.join(HERE, "e_runs")
THICK = (6, 12, 25, 50)
SEEDS = (1, 2)
STARTS = ("grid3D", "ring")
EARLY = 2.0           # first reading at twice the starting size
END = 8.0             # last reading at eight times it - a four-fold span, as in A12 C7


def inherit_thick(adj, omega, rng, rho, sigma_pass):
    """Neighbourhoods inherited at a set thickness, with the child's rate taken from its parent (S4)."""
    n_old = len(adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < P.Q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]

    def link(a, b):
        if a != b and b not in new[a] and len(new[a]) < P.CEIL and len(new[b]) < P.CEIL:
            new[a].add(b)
            new[b].add(a)
            return 1
        return 0

    target = int(round(rho / 2.0 * m))
    count, extras, base = 0, [], []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                base.append((ks[i], ks[j]))
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            base.append((ks[int(rng.integers(len(ks)))], kq[int(rng.integers(len(kq)))]))
            for i in range(mm):
                extras.append((ks[i % len(ks)], kq[i % len(kq)]))
    for a, b in base:
        if count >= target:
            break
        count += link(a, b)
    if extras and count < target:
        for k in rng.permutation(len(extras)):
            if count >= target:
                break
            a, b = extras[int(k)]
            count += link(a, b)
    child = np.empty(m)
    for p in range(n_old):
        for a in kids[p]:
            child[a] = omega[p] + rng.normal(0, sigma_pass)
    return new, child


def thick_lattice(n, rho, rng):
    """A GENUINE 3D lattice at the same thickness: a cubic torus widened to rho relations per event.

    INSTRUMENT FIX, recorded before the run. The first rule failed any pattern whose small-world flag was set at
    the end - but a real cubic torus carrying 25 relations per event trips that flag too, simply because many
    neighbours make distances short. Judging a thick pattern against a 6-regular reference penalises thickness
    itself. So the reference is now matched in thickness as well as dimension: the same cubic torus, widened by
    joining everything within a few steps and thinned at random to exactly rho relations per event.
    """
    side = max(4, int(round(n ** (1 / 3.0))))
    A = N1.torus3(side, rng).tocsr()
    B = A.copy()
    while (B.nnz / B.shape[0]) < rho and B.nnz < 200 * B.shape[0]:
        B = ((B + B.dot(A)) > 0).astype(float)
        B.setdiag(0)
        B.eliminate_zeros()
    r, c = sp.triu(B, 1).nonzero()
    keep = int(round(rho / 2.0 * B.shape[0]))
    if len(r) > keep:
        idx = rng.permutation(len(r))[:keep]
        r, c = r[idx], c[idx]
    W = sp.csr_matrix((np.ones(2 * len(r)), (np.concatenate([r, c]), np.concatenate([c, r]))), shape=B.shape)
    W.data[:] = 1.0
    return P.read(W)


def reading(adj, omega, K=L.K0):
    A = P.to_A(adj)
    r = P.read(A)
    ok, _, _, _ = L.holds_local(adj, omega, K)
    return r, bool(ok)


def run(name, rho, seed):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    n0 = len(adj)
    omega = rng.normal(0, 1, n0)
    omega -= omega.mean()
    spread0 = float(omega.std())
    sp_pass = G.SIGMA_PASS * spread0
    early, end, t0 = None, None, time.time()
    while len(adj) < END * n0:
        adj, omega = inherit_thick(adj, omega, rng, rho, sp_pass)
        omega = G.diffuse(adj, omega, G.ALPHA)
        omega -= omega.mean()
        if early is None and len(adj) >= EARLY * n0:
            early = (len(adj),) + reading(adj, omega)
    end = (len(adj),) + reading(adj, omega)
    # a genuine 3D lattice at the SAME thickness and the same two sizes: drift and flag both calibrated
    rlo = thick_lattice(early[0], rho, np.random.default_rng(99))
    rhi = thick_lattice(end[0], rho, np.random.default_rng(99))
    ref_lo, ref_hi, ref_sw = rlo["d_H"], rhi["d_H"], rhi["small_world"]
    drift = None if (early[1]["d_H"] is None or end[1]["d_H"] is None) else round(end[1]["d_H"] - early[1]["d_H"], 3)
    ref_drift = None if (ref_lo is None or ref_hi is None) else round(ref_hi - ref_lo, 3)
    stable = (drift is not None and abs(drift) <= 0.4 and (ref_sw or not end[1]["small_world"]))
    return dict(start=name, rho=rho, seed=seed, n_early=early[0], n_end=end[0],
                d_early=early[1]["d_H"], d_end=end[1]["d_H"], drift=drift, ref_drift=ref_drift,
                md_early=early[1]["md"], md_end=end[1]["md"], sw_end=end[1]["small_world"], ref_sw=bool(ref_sw),
                ref_d_end=ref_hi,
                per_event=end[1]["per_event"], holds_early=early[2], holds_end=end[2], stable=bool(stable),
                secs=round(time.time() - t0, 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in STARTS:
        for rho in THICK:
            for seed in SEEDS:
                r = run(name, rho, seed)
                res.append(r)
                print("%-6s thickness %2d seed %d | reading %s at %5d -> %s at %5d | drift %s | a real 3D lattice "
                      "of that thickness reads %s, drift %s, small world %s | our small world %s | relations/event"
                      " %.1f | holds unaided %s | STABLE %s | %.0fs"
                      % (name, rho, seed, r["d_early"], r["n_early"], r["d_end"], r["n_end"], r["drift"],
                         r["ref_d_end"], r["ref_drift"], r["ref_sw"], r["sw_end"], r["per_event"], r["holds_end"],
                         r["stable"], r["secs"]),
                      flush=True)
                json.dump(res, open(os.path.join(OUT, "thick.json"), "w"), indent=1, default=str)
    lines = []
    for r in res:
        lines.append("%-6s thickness %2d seed %d | %s at %5d -> %s at %5d | drift %s | a real 3D lattice of that"
                     " thickness: reads %s, drift %s, small world %s | our small world %s | relations/event %.1f |"
                     " holds unaided %s | STABLE %s"
                     % (r["start"], r["rho"], r["seed"], r["d_early"], r["n_early"], r["d_end"], r["n_end"],
                        r["drift"], r["ref_d_end"], r["ref_drift"], r["ref_sw"], r["sw_end"], r["per_event"],
                        r["holds_end"], r["stable"]))
    t0 = all(r["holds_end"] and r["holds_early"] for r in res)
    stable_at = sorted({(r["start"], r["rho"]) for r in res if r["stable"]})
    t1 = len(stable_at) > 0
    vals = [r["d_end"] for r in res if r["stable"] and r["d_end"] is not None]
    t2 = bool(vals) and all(2.5 <= v <= 3.5 for v in vals)
    lines.append("")
    lines.append("T0 (the sync condition holds unaided at every thickness) %s" % t0)
    lines.append("T1 (at least one thickness gives a STABLE reading) %s   %s" % (t1, stable_at))
    lines.append("T2 (a stable reading between 2.5 and 3.5) %s   values %s" % (t2, [round(v, 2) for v in vals]))
    for name in STARTS:
        lines.append("T3 %s: readings at the end by thickness %s"
                     % (name, {rho: [r["d_end"] for r in res if r["start"] == name and r["rho"] == rho]
                               for rho in THICK}))
    if not t1:
        lines.append("** T1 FAILED AT EVERY THICKNESS: on ED's own account of where dimension lives, these rules do "
                     "not produce one. Per C6 this is where the sequence of missing pieces becomes the finding. **")
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "t_thick.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
