"""C3f model (note 27, C92; D40, D41; IMPLEMENTATION_NOTES.md, C3f section).

C3e's slice, budgets, ceiling and paired flips, with:
  * sync as a CONDITION: a move is refused if it would leave any new link carrying a tick difference
    above s_max (set from the flat calibration), instead of a reward term in the cost;
  * the cost reduced to commitment and curvature: S = alpha*E + lam*sum (valence - 5.104)^2;
  * per-tick bookkeeping of merges, splits, forced keeps and refusals by cause;
  * an optional record of children and absorptions, so the grown spacetime can be built.
"""
import math
import numpy as np
from c3c import n3_after_exact, weighted_choice, edges_of, SIGMA, K, K_RESPONSE
from c3d import slice_readings, FLAT_LINKS_PER_EVENT  # noqa: F401
from c3e import paired_flip_plan, CEILING


def allowed(M, plan, pool, phi, s_max, gone=(), cap=CEILING):
    """(ok, born, dies, reason). Budget, ceiling and the sync condition in one pass over the move's edges."""
    dv = {}
    for tid in plan[0]:
        for e in edges_of(M.tets[tid]):
            dv[e] = dv.get(e, 0) - 1
    for t in plan[1]:
        for e in edges_of(tuple(sorted(t))):
            dv[e] = dv.get(e, 0) + 1
    born = dies = 0
    ddeg = {}
    born_edges = []
    val = M.val
    for e, d in dv.items():
        if d == 0:
            continue
        old = val.get(e, 0)
        new = old + d
        if old == 0 and new > 0:
            born += 1
            born_edges.append(e)
            ddeg[e[0]] = ddeg.get(e[0], 0) + 1
            ddeg[e[1]] = ddeg.get(e[1], 0) + 1
        elif old > 0 and new == 0:
            dies += 1
            ddeg[e[0]] = ddeg.get(e[0], 0) - 1
            ddeg[e[1]] = ddeg.get(e[1], 0) - 1
    if born - dies > max(pool, 0):
        return False, born, dies, "budget"
    nbrs = M.nbrs
    for v, d in ddeg.items():
        if d > 0 and v not in gone:
            base = len(nbrs[v]) if v in nbrs else 0
            if base + d > cap:
                return False, born, dies, "cap"
    if s_max is not None:
        # s_max is in the calibration's normalized units (its solver uses sigma = K = 1), so the run's
        # raw tick differences must be divided by sigma/K before comparing. C3f run 1 compared raw
        # differences (order 1e-3) against a normalized threshold (order 10) and so never fired (D43).
        scale = SIGMA / K
        for a, b in born_edges:
            pa = phi.get(a)
            pb = phi.get(b)
            if pa is None or pb is None:            # a new child inherits its parent's tick count
                continue
            if abs(pa - pb) / scale > s_max:
                return False, born, dies, "sync"
    return True, born, dies, ""


def tick(M, b, omega, phi, rng, alpha, lam, pool, s_max=None, cap=CEILING, record=None):
    """One growth tick. Cost has no sync term; sync acts only as a condition. Returns counts and the pool."""
    none = alpha == 0 and lam == 0
    ids = list(M.vt)
    bb = np.array([b[v] for v in ids])
    mu = np.maximum(0.0, 1.0 + K_RESPONSE * (bb - 1.0))
    c = rng.geometric(1.0 / (1.0 + mu)) - 1
    cnt = dict(zip(ids, c.tolist()))
    forced = merges = splits = f_acc = 0
    ref = {"budget": 0, "cap": 0, "sync": 0}
    split_refused = 0
    children, absorbed = {}, {}

    order = [v for v in ids if cnt[v] == 0]
    rng.shuffle(order)
    for v in order:
        cands, plans, dS = [], [], []
        for a in list(M.nbrs[v]):
            if not M.link_condition(v, a):
                continue
            plan = M.merge_plan(v, a)
            ok, born, dies, why = allowed(M, plan, pool, phi, s_max, gone=(v,), cap=cap)
            if not ok:
                ref[why] += 1
                continue
            cands.append((a, born, dies)); plans.append(plan)
            if not none:
                dS.append(M.delta_S(plan[0], plan[1], alpha, lam, 0.0, phi))
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
        absorbed[v] = a
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
                ok, born, dies, why = allowed(M, plan, pool, phi, s_max, gone=(), cap=cap)
                if not ok:
                    ref[why] += 1
                    continue
                opts.append((u, born, dies)); plans.append(plan)
                if not none:
                    dS.append(M.delta_S(plan[0], plan[1], alpha, lam, 0.0, phi, {y: phi[x]}))
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
        children[v] = kids

    links_before_flips = len(M.val)
    for _ in range(len(M.vt) // 2):
        plan = paired_flip_plan(M, rng)
        if plan is None:
            continue
        ok, born, dies, why = allowed(M, plan, pool, phi, s_max, gone=(), cap=cap)
        if not ok:
            ref[why] += 1
            continue
        corr = len(M.val3) / max(n3_after_exact(M, plan), 1)
        dS = 0.0 if none else M.delta_S(plan[0], plan[1], alpha, lam, 0.0, phi)
        acc = corr * math.exp(-dS) if dS > -700 else float("inf")
        if acc >= 1 or rng.random() < acc:
            M.apply(plan[0], plan[1])
            pool += dies - born
            f_acc += 1
    flips_link_neutral = (len(M.val) == links_before_flips)

    A, idsA, pos, ei, ej = M.adjacency()
    ph = np.array([phi[v] for v in idsA])
    om = np.array([omega[v] for v in idsA])
    deg = np.bincount(np.concatenate([ei, ej]), minlength=len(idsA)).astype(float)
    t_ = np.tanh(ph[ej] - ph[ei])
    pull = np.bincount(ei, weights=t_, minlength=len(idsA)) - np.bincount(ej, weights=t_, minlength=len(idsA))
    ph = ph + om + (K / deg) * pull
    for i, v in enumerate(idsA):
        phi[v] = ph[i]
    if record is not None:
        record["children"] = children
        record["absorbed"] = absorbed
    return dict(forced=forced, merges=merges, splits=splits, flips_accepted=f_acc, size=len(M.vt),
                refused_budget=ref["budget"], refused_cap=ref["cap"], refused_sync=ref["sync"],
                split_refused=split_refused, links=len(M.val), pool=pool,
                flips_link_neutral=flips_link_neutral), pool


def slice_edges(M):
    return [(a, b) for (a, b) in M.val]


def spacetime_readings(snapshots, seed):
    """Ball-growth readings on the grown spacetime pattern (slices plus forward links)."""
    from c3a import build_spacetime
    from c3b import readings as ball_readings
    A = build_spacetime(snapshots)
    r = ball_readings(A, seed)
    r["events"] = int(A.shape[0])
    r["links"] = int(A.nnz // 2)
    return r
