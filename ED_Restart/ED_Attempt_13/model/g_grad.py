"""Road E with gradients (D2, C4): rates that pass on and rates that diffuse.

The local-sync model (A12 C9, C11, C12) unchanged in every respect - pass on once and be spent, neighbourhoods
inherited, every patch able to shed its surplus through its own edge (exact max-flow, no shared now), relations
added across the minimum cut, a relation persisting once it has carried anything - with exactly two changes, both
from Allen's January 2026 paper:

    S4   a child's rate is its PARENT'S plus a small variation, so a gradient can persist;
    S26  each tick an event's rate moves a little TOWARD ITS NEIGHBOURS', so gradients soften.
         ("The natural flow of becoming is from concentrated ED toward diffuse ED" - the arrow of time.)

Until now every rate was drawn independently from a bell curve, and in the generation models redrawn every tick:
noise with no memory. There was no such thing as a fast region. Now there is.

PRE-REGISTERED VOID CONDITION (note 4, before any code): a flat pattern satisfies every sync condition trivially.
    If the spread of rates falls below a tenth of its starting value, the run is VOID and is reported as
    "the pattern flattened", NEVER as "the pattern held together".
The paper's S16 and S29 say a universe does end that way, so flattening is a real outcome - just not a success.

EXPECTATIONS, fixed in note 4 before this file was written:
  G0  THE GATE: gradients survive long enough to matter (the void check above passes)          about 55%
  G1  patterns hold on FEWER relations than with noise - under 4.15 per event                   about 70%
  G2  MAIN: the end state is no longer the same from every start                                about 40%
  G3  readings lower than the noise model's 3.9, small-world flag clearing on at least one start about 20%
  G4  reported: the paper's OWN distance (shortest path weighted by rate difference) against hop distance; the
      size of the gradients at the end; what the rate spread does over the run
Claude's two new numbers, labelled: SIGMA_PASS (variation when a rate passes on) and ALPHA (diffusion speed), set
to the smallest values that let a gradient exist, and varied by a factor of three afterwards as the pull was in C11.
Under the census guard this makes ED's input list LONGER, not shorter.
"""
import io
import json
import os
import sys
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components, dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for rel in (("..", "..", "ED_Attempt_12", "model"), ("..", "..", "ED_Attempt_11", "model"),
            ("..", "..", "ED_Attempt_08", "model")):
    sys.path.insert(0, os.path.join(HERE, *rel))
import n1_sync as N1                                        # noqa: E402
import p_persist as P                                       # noqa: E402
import l_local as L                                         # noqa: E402
import l_local2 as L2                                       # noqa: E402

OUT = os.path.join(HERE, "e_runs")
SEEDS = (1, 2, 3)
GROW = 4.0
SIGMA_PASS = 0.1      # Claude's: variation when a rate passes on, as a share of the starting spread
ALPHA = 0.1           # Claude's: how far a rate moves toward its neighbours' each tick
VOID_AT = 0.1         # the pre-registered void threshold, as a share of the starting spread


def inherit_rates(adj, committed, omega, rng, sigma_pass):
    """One generation: neighbourhoods inherited as before, and each child takes its parent's rate (S4)."""
    n_old = len(adj)
    r_old = sum(len(s) for s in adj)
    kids, m = [], 0
    for _ in range(n_old):
        c = 2 if rng.random() < P.Q else 1
        kids.append(list(range(m, m + c)))
        m += c
    new = [set() for _ in range(m)]
    mark = set()

    def link(a, b, src=None):
        if a != b and b not in new[a] and len(new[a]) < P.CEIL and len(new[b]) < P.CEIL:
            new[a].add(b)
            new[b].add(a)
            if src is not None and src in committed:
                mark.add(L2.key(a, b))
            return 1
        return 0

    count, extras, base = 0, [], []
    for p in range(n_old):
        ks = kids[p]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                base.append((ks[i], ks[j], None))
        for qn in adj[p]:
            if qn <= p:
                continue
            kq = kids[qn]
            mm = max(len(ks), len(kq))
            base.append((ks[int(rng.integers(len(ks)))], kq[int(rng.integers(len(kq)))], L2.key(p, qn)))
            for i in range(mm):
                extras.append((ks[i % len(ks)], kq[i % len(kq)], L2.key(p, qn)))
    target = int(round(r_old / 2.0 * m / n_old))
    for a, b, src in base:
        if count >= target:
            break
        count += link(a, b, src)
    if extras and count < target:
        for k in rng.permutation(len(extras)):
            if count >= target:
                break
            a, b, src = extras[int(k)]
            count += link(a, b, src)
    child_omega = np.empty(m)
    for p in range(n_old):
        for a in kids[p]:
            child_omega[a] = omega[p] + rng.normal(0, sigma_pass)   # S4: the parent's rate, plus a little
    return new, mark, child_omega


def diffuse(adj, omega, alpha):
    """S26: each rate moves a little toward its neighbours'. Gradients soften; this is the arrow of time."""
    A = P.to_A(adj)
    deg = np.asarray(A.sum(axis=1)).ravel()
    deg[deg == 0] = 1
    nbr = A.dot(omega) / deg
    return omega + alpha * (nbr - omega)


def rate_distance(A, omega, rng, sources=8):
    """The paper's own distance: shortest path weighted by difference in rate, against hop distance."""
    n = A.shape[0]
    r, c = sp.triu(A, 1).nonzero()
    w = np.abs(omega[r] - omega[c]) + 1e-9
    W = sp.csr_matrix((np.concatenate([w, w]), (np.concatenate([r, c]), np.concatenate([c, r]))), shape=(n, n))
    src = rng.choice(n, size=min(sources, n), replace=False)
    dr = dijkstra(W, directed=False, indices=src)
    dh = dijkstra(A, directed=False, indices=src, unweighted=True)
    ok = np.isfinite(dr) & np.isfinite(dh) & (dh > 0)
    if ok.sum() < 10:
        return None, None
    return float(dr[ok].mean()), float(np.corrcoef(dr[ok], dh[ok])[0, 1])


def run(name, seed, K=L.K0, grow=GROW, sigma_pass=SIGMA_PASS, alpha=ALPHA):
    rng = np.random.default_rng(seed)
    A0 = {"ring": lambda: N1.ring(2000, rng), "grid3D": lambda: N1.torus3(13, rng),
          "web": lambda: N1.rand_regular(2000, rng)}[name]()
    adj = P.to_adj(A0)
    omega = rng.normal(0, 1, len(adj))
    omega -= omega.mean()
    spread0 = float(omega.std())
    sp_pass = sigma_pass * spread0
    committed = set()
    start = P.read(A0)
    target, t0, gen = grow * len(adj), time.time(), 0
    adds, goes, spreads, failed, void = [], [], [spread0], False, False
    while len(adj) < target:
        adj, committed, omega = inherit_rates(adj, committed, omega, rng, sp_pass)
        omega = diffuse(adj, omega, alpha)
        omega -= omega.mean()
        spreads.append(float(omega.std()))
        if spreads[-1] < VOID_AT * spread0:                  # the pre-registered void condition
            void = True
            break
        adj, a, ok = L.repair(adj, omega, rng, K)
        adds.append(a)
        if not ok:
            failed = True
            break
        adj, committed, g = L2.dissolve_uncommitted(adj, committed, omega, rng, K)
        goes.append(g)
        gen += 1
    A = P.to_A(adj)
    k, lab = connected_components(A, directed=False)
    big = np.flatnonzero(lab == np.bincount(lab).argmax()) if k > 1 else None
    whole = 1.0 if k == 1 else float(len(big)) / A.shape[0]
    final = P.read(A if k == 1 else A[big][:, big])
    ref = P.reference(name, A.shape[0], np.random.default_rng(99))
    rd, corr = rate_distance(A, omega, np.random.default_rng(7))
    return dict(start_name=name, seed=seed, K=K, sigma_pass=sigma_pass, alpha=alpha, n0=A0.shape[0], n=len(adj),
                start=start, final=final, ref_d_H=ref, whole=round(whole, 3), void=bool(void), failed=bool(failed),
                added=int(sum(adds)), dissolved=int(sum(goes)), spread0=round(spread0, 3),
                spread_end=round(spreads[-1], 3), spread_ratio=round(spreads[-1] / spread0, 3),
                rate_dist=None if rd is None else round(rd, 3), rate_hop_corr=None if corr is None else round(corr, 3),
                secs=round(time.time() - t0, 1))


def line(r):
    return ("%-6s seed %d sig %.2f a %.2f | n %5d -> %5d | reading %s -> %s (a real one reads %s) | md %.1f -> %.1f |"
            " small world %s | relations/event %.2f -> %.2f | rate spread %.3f -> %.3f (x%.2f) | VOID %s | added %d"
            " dissolved %d | rate-distance %s (agrees with hops %s)"
            % (r["start_name"], r["seed"], r["sigma_pass"], r["alpha"], r["n0"], r["n"], r["start"]["d_H"],
               r["final"]["d_H"], r["ref_d_H"], r["start"]["md"], r["final"]["md"], r["final"]["small_world"],
               r["start"]["per_event"], r["final"]["per_event"], r["spread0"], r["spread_end"], r["spread_ratio"],
               r["void"], r["added"], r["dissolved"], r["rate_dist"], r["rate_hop_corr"]))


def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    for name in ("ring", "grid3D", "web"):
        for seed in SEEDS:
            r = run(name, seed)
            res.append(r)
            print(line(r), flush=True)
            json.dump(res, open(os.path.join(OUT, "grad.json"), "w"), indent=1, default=str)
    for sp_, al in ((0.03, 0.1), (0.3, 0.1), (0.1, 0.03), (0.1, 0.3)):     # Claude's two numbers, varied
        r = run("grid3D", 1, sigma_pass=sp_, alpha=al)
        res.append(r)
        print(line(r), flush=True)
        json.dump(res, open(os.path.join(OUT, "grad.json"), "w"), indent=1, default=str)
    lines = [line(r) for r in res]
    main_runs = [r for r in res if r["sigma_pass"] == SIGMA_PASS and r["alpha"] == ALPHA]
    g0 = all(not r["void"] for r in main_runs)
    per = {n: round(float(np.mean([x["final"]["per_event"] for x in main_runs if x["start_name"] == n])), 2)
           for n in ("ring", "grid3D", "web")}
    g1 = g0 and all(v < 4.15 for v in per.values())
    reads = {n: [x["final"]["d_H"] for x in main_runs if x["start_name"] == n] for n in ("ring", "grid3D", "web")}
    defined = {n: [v for v in vs if v is not None] for n, vs in reads.items()}
    means = {n: (None if not vs else round(float(np.mean(vs)), 2)) for n, vs in defined.items()}
    g2 = g0 and len([m for m in means.values() if m is not None]) >= 2 and (
        max([m for m in means.values() if m is not None]) - min([m for m in means.values() if m is not None]) > 0.3)
    g3 = g0 and any((m is not None and m < 3.9) for m in means.values()) and \
        any(not x["final"]["small_world"] for x in main_runs)
    lines.append("G0 (gradients survive - THE GATE) %s%s" % (g0, "" if g0 else "   ** runs VOID: the pattern flattened, NOT held together **"))
    lines.append("G1 (fewer relations than the noise model's 4.15) %s   %s" % (g1, per))
    lines.append("G2 (the end state is no longer the same from every start) %s   readings %s" % (g2, means))
    lines.append("G3 (readings below 3.9 and the small-world flag clearing somewhere) %s" % g3)
    lines.append("G4 rate spread at the end: %s | rate-distance and its agreement with hops: %s"
                 % ({r["start_name"] + str(r["seed"]): r["spread_ratio"] for r in main_runs},
                    {r["start_name"] + str(r["seed"]): (r["rate_dist"], r["rate_hop_corr"]) for r in main_runs}))
    text = "\n".join(lines)
    io.open(os.path.join(HERE, "g_grad.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
