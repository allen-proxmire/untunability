"""C3e model (note 23, C81; D34, D35; IMPLEMENTATION_NOTES.md, C3e section).

C3d's slice, budgets, ceiling and readings, with one change: cut-and-rejoin is done strictly in pairs
(A6 D5, D8). A flip attempt is one 2-3 and one 3-2 at disjoint places, accepted or refused as a single
move, so the link and tetrahedron counts do not change and rewiring no longer draws on the link pool.
"""
import math
import numpy as np
from c3c import n3_after_exact, weighted_choice, K, K_RESPONSE
from c3d import allowed, slice_readings, FLAT_LINKS_PER_EVENT, DEGREE_CAP  # noqa: F401 (re-exported)

CEILING = 60


def paired_flip_plan(M, rng):
    """One 2-3 and one 3-2 at disjoint places, as a single link-neutral move."""
    a = M.flip23_plan(M.tid_set.choice(rng), int(rng.integers(4)))
    if a is None or len(M.val3) == 0:
        return None
    b = M.flip32_plan(M.val3.choice(rng))
    if b is None or (set(a[0]) & set(b[0])):
        return None
    tri = set(b[1][0]) & set(b[1][1])          # the triangle the 3-2 needs absent beforehand
    for t in a[1]:                              # the 2-3 must not create it
        if tri <= set(t):
            return None
    return [a[0] + b[0], a[1] + b[1]]


def tick(M, b, omega, phi, rng, alpha, lam, gamma, pool, cap=CEILING):
    """One growth tick with the link budget, the ceiling and paired flips. Returns counts and the pool."""
    none = alpha == 0 and lam == 0 and gamma == 0
    ids = list(M.vt)
    bb = np.array([b[v] for v in ids])
    mu = np.maximum(0.0, 1.0 + K_RESPONSE * (bb - 1.0))
    c = rng.geometric(1.0 / (1.0 + mu)) - 1
    cnt = dict(zip(ids, c.tolist()))
    forced = merges = splits = f_acc = f_try = 0
    ref_budget = ref_cap = split_refused = 0
    links_before_flips = None

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

    links_before_flips = len(M.val)
    for _ in range(len(M.vt) // 2):
        f_try += 1
        plan = paired_flip_plan(M, rng)
        if plan is None:
            continue
        ok, born, dies, why = allowed(M, plan, pool, gone=(), cap=cap)
        if not ok:
            ref_budget += why == "budget"
            ref_cap += why == "cap"
            continue
        n3_now = len(M.val3)
        corr = n3_now / max(n3_after_exact(M, plan), 1)   # tetrahedron count is unchanged, so F cancels
        dS = 0.0 if none else M.delta_S(plan[0], plan[1], alpha, lam, gamma, phi)
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
    return dict(forced=forced, merges=merges, splits=splits, flips_accepted=f_acc, flips_tried=f_try,
                size=len(M.vt), refused_budget=ref_budget, refused_cap=ref_cap, split_refused=split_refused,
                links=len(M.val), pool=pool, flips_link_neutral=flips_link_neutral), pool
