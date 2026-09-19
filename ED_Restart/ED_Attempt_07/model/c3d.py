"""C3d model (note 21, C76; D31, D32; IMPLEMENTATION_NOTES.md, C3d section).

C3c's 3-torus slice and moves, plus:
  * a conserved link budget held as a pool (total links pinned at round(6.699 * V0)),
  * a ceiling on links per event (no infinities),
  * repaired readings: ball growth, the walk-based spectral dimension, diameter and mean distance.
Moves that would overdraw the pool or break the ceiling are refused, and refusals are counted.
"""
import math
import numpy as np
from c3c import Slice3, edges_of, weighted_choice, FLAT_VALENCE, SIGMA, K, K_RESPONSE
from readings import bfs_distances, N_CENTRES
from readings_v2 import all_readings

FLAT_LINKS_PER_EVENT = 1 + FLAT_VALENCE / (6 - FLAT_VALENCE)  # E/V = 6.699
DEGREE_CAP = 30


def move_effect(M, remove, add):
    """Links born and dying, and the degree change per affected event, for a proposed move."""
    dv = {}
    for tid in remove:
        for e in edges_of(M.tets[tid]):
            dv[e] = dv.get(e, 0) - 1
    for t in add:
        for e in edges_of(tuple(sorted(t))):
            dv[e] = dv.get(e, 0) + 1
    born = dies = 0
    ddeg = {}
    for e, d in dv.items():
        if d == 0:
            continue
        old = M.val.get(e, 0)
        new = old + d
        if old == 0 and new > 0:
            born += 1
            ddeg[e[0]] = ddeg.get(e[0], 0) + 1
            ddeg[e[1]] = ddeg.get(e[1], 0) + 1
        elif old > 0 and new == 0:
            dies += 1
            ddeg[e[0]] = ddeg.get(e[0], 0) - 1
            ddeg[e[1]] = ddeg.get(e[1], 0) - 1
    return born, dies, ddeg


def allowed(M, plan, pool, gone=(), cap=DEGREE_CAP):
    """(ok, born, dies, reason). gone: events removed by the move (their degree is not checked)."""
    born, dies, ddeg = move_effect(M, plan[0], plan[1])
    # A move may always give links back or leave the count alone; only net additions need free budget.
    # (The cube-grid start sits slightly above the budget, so the pool begins negative and is paid down.)
    if born - dies > max(pool, 0):
        return False, born, dies, "budget"
    for v, d in ddeg.items():
        if d <= 0 or v in gone:
            continue
        base = len(M.nbrs[v]) if v in M.nbrs else 0
        if base + d > cap:
            return False, born, dies, "cap"
    return True, born, dies, ""


def tick(M, b, omega, phi, rng, alpha, lam, gamma, pool, cap=DEGREE_CAP):
    """One growth tick with the link budget and the ceiling. Returns counts and the new pool."""
    none = alpha == 0 and lam == 0 and gamma == 0
    ids = list(M.vt)
    bb = np.array([b[v] for v in ids])
    mu = np.maximum(0.0, 1.0 + K_RESPONSE * (bb - 1.0))
    c = rng.geometric(1.0 / (1.0 + mu)) - 1
    cnt = dict(zip(ids, c.tolist()))
    forced = merges = splits = f_acc = 0
    ref_budget = ref_cap = split_refused = 0
    order = [v for v in ids if cnt[v] == 0]
    rng.shuffle(order)
    for v in order:
        cands, plans, dS = [], [], []
        for a in list(M.nbrs[v]):
            if not M.link_condition(v, a):
                continue
            plan = M.merge_plan(v, a)
            ok, born, dies, why = allowed(M, plan, pool, gone=(v,), cap=cap)
            if not ok:
                ref_budget += why == "budget"
                ref_cap += why == "cap"
                continue
            cands.append((a, born, dies)); plans.append(plan)
            if not none:
                dS.append(M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi))
        if not cands:
            cnt[v] = 1
            forced += 1
            continue
        k = int(rng.integers(len(cands))) if none else weighted_choice(rng, dS)
        a, born, dies = cands[k]
        M.merge(v, a, plans[k])
        pool += dies - born
        b[a] += b.pop(v)
        del phi[v], omega[v]
        merges += 1
    order = [v for v in ids if v in M.vt and cnt[v] >= 1]
    rng.shuffle(order)
    for v in order:
        kids = [v]
        for _ in range(cnt[v] - 1):
            x = kids[-1]
            y = M.next_id
            opts, plans, dS = [], [], []
            for u in sorted(M.nbrs[x]):
                plan = M.split_plan(x, u, y)
                ok, born, dies, why = allowed(M, plan, pool, gone=(), cap=cap)
                if not ok:
                    ref_budget += why == "budget"
                    ref_cap += why == "cap"
                    continue
                opts.append((u, born, dies)); plans.append(plan)
                if not none:
                    dS.append(M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi, {y: phi[x]}))
            if not opts:
                split_refused += 1
                break
            k = int(rng.integers(len(opts))) if none else weighted_choice(rng, dS)
            u, born, dies = opts[k]
            y = M.split(x, u, plans[k])
            pool += dies - born
            phi[y] = phi[x]
            omega[y] = omega[x]
            kids.append(y)
            splits += 1
        share = b[v] / len(kids)
        for x in kids:
            b[x] = share
    from c3c import n3_after_exact
    for _ in range(len(M.vt)):
        if rng.random() < 0.5:
            plan = M.flip23_plan(M.tid_set.choice(rng), int(rng.integers(4)))
            if plan is None:
                continue
            corr = 2 * len(M.tets) / max(n3_after_exact(M, plan), 1)
        else:
            if len(M.val3) == 0:
                continue
            plan = M.flip32_plan(M.val3.choice(rng))
            if plan is None:
                continue
            corr = len(M.val3) / (2 * (len(M.tets) - 1))
        ok, born, dies, why = allowed(M, plan, pool, gone=(), cap=cap)
        if not ok:
            ref_budget += why == "budget"
            ref_cap += why == "cap"
            continue
        dS = 0.0 if none else M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi)
        acc = corr * math.exp(-dS) if dS > -700 else float("inf")
        if acc >= 1 or rng.random() < acc:
            M.apply(plan[0], plan[1])
            pool += dies - born
            f_acc += 1
    A, idsA, pos, ei, ej = M.adjacency()
    ph = np.array([phi[v] for v in idsA])
    om = np.array([omega[v] for v in idsA])
    deg = np.bincount(np.concatenate([ei, ej]), minlength=len(idsA)).astype(float)
    t_ = np.tanh(ph[ej] - ph[ei])
    pull = np.bincount(ei, weights=t_, minlength=len(idsA)) - np.bincount(ej, weights=t_, minlength=len(idsA))
    ph = ph + om + (K / deg) * pull
    for i, v in enumerate(idsA):
        phi[v] = ph[i]
    return dict(forced=forced, merges=merges, splits=splits, flips_accepted=f_acc, size=len(M.vt),
                refused_budget=ref_budget, refused_cap=ref_cap, split_refused=split_refused,
                links=len(M.val), pool=pool), pool


def slice_readings(M, seed, with_walk=True):
    """Ball growth, the walk-based spectral dimension, diameter and mean distance, counts and neck strain."""
    from c3b import sync_steady_state
    A, ids, pos, ei, ej = M.adjacency()
    rng = np.random.default_rng(3000 + seed)
    N = A.shape[0]
    centres = rng.choice(N, size=min(N_CENTRES, N), replace=False)
    dist = bfs_distances(A, centres)
    if with_walk:
        r = all_readings(A, np.random.default_rng(3000 + seed))
        d_H, d_s, sw, r_lo, r_max = r["d_H"], r["d_s"], bool(r["small_world"]), r["r_lo"], r["r_max"]
    else:
        from readings_v2 import mass_and_cut
        r = mass_and_cut(A, dist)
        d_H, d_s, sw, r_lo, r_max = r["d_H"], np.nan, bool(r["small_world"]), r["r_lo"], r["r_max"]
    deg = np.asarray(A.sum(axis=1)).ravel()
    vals = np.fromiter(M.val.values(), dtype=float, count=len(M.val))
    s = sync_steady_state(A, seed)
    f = lambda x: (float(x) if x is not None and np.isfinite(x) else None)
    return dict(d_H=f(d_H), d_s=f(d_s), small_world=sw, r_lo=f(r_lo), r_max=f(r_max),
                diameter=float(dist.max()), mean_distance=float(dist.mean()),
                mean_degree=float(deg.mean()), max_degree=int(deg.max()),
                links_per_event=len(M.val) / len(M.vt), tets_per_event=len(M.tets) / len(M.vt),
                valence_mean=float(vals.mean()), valence_sd=float(vals.std()),
                curv2=float(np.mean((vals - FLAT_VALENCE) ** 2)),
                neck_strain=float(s["max_link_diff"]), solve_residual=float(s["residual"]),
                V=len(M.vt), T=len(M.tets), E=len(M.val))
