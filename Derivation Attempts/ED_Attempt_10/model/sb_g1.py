"""Gate G1 (note 14, C24): rings of 4 events, T = 3, cap 2. Sampler frequencies over distinct histories against the
exact target (every valid history, weighted by 1/|Aut|), enumerated independently tick by tick with closure.
Pass (written before running): every history visited; every frequency within 3 standard errors (batch means);
chi-square reported. Replay check (G2's ring form) run every 1,000 steps.
REVISION after the first run (13 of 49 visited): parent-swap move added to sb_core (which end of a link is the
parent or absorber is part of a history but no bundle could change it)."""
import json
import os
import sys
import time
import numpy as np
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sb_core import History, RingOps, ring, inverse  # noqa: E402

L0, T, CAP = 6, 3, 2   # REVISION: 4 events admit no bundle (a split plus a merge touch 5 events)
ops = RingOps()


def walk(S, start, forward=True):
    out = [start]
    x = S[start][1 if forward else 0]
    while x != start:
        out.append(x)
        x = S[x][1 if forward else 0]
    return out


def canon(slices, taus):
    """Canonical representation (min over the 8 dihedral relabelings of S_0) and |Aut|."""
    Tn = len(slices)
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for t, S in enumerate(slices):
        for v in S:
            parent[(t, v)] = (t, v)
    for t, S in enumerate(slices):
        N = slices[(t + 1) % Tn]
        for v in S:
            if v in N:
                ra, rb = find((t, v)), find(((t + 1) % Tn, v))
                if ra != rb:
                    parent[ra] = rb
    s0 = walk(slices[0], min(slices[0]))
    reps = []
    for fwd in (True, False):
        base = s0 if fwd else [s0[0]] + s0[1:][::-1]
        for r in range(len(base)):
            order = base[r:] + base[:r]
            name = {}
            for i, v in enumerate(order):
                name[find((0, v))] = i
            nxt = len(order)
            rep_s = []
            for t, S in enumerate(slices):
                named = [v for v in S if find((t, v)) in name]
                st = min(named, key=lambda v: name[find((t, v))])
                w = walk(S, st, fwd)
                for v in w:
                    sg = find((t, v))
                    if sg not in name:
                        name[sg] = nxt
                        nxt += 1
                rep_s.append(tuple(name[find((t, v))] for v in w))
            rep_t = []
            for t, tau in enumerate(taus):
                N = (t + 1) % Tn
                ks = []
                for k in tau:
                    if k[0] == "S":
                        ks.append(("S", name[find((t, k[1]))], name[find((t, k[2]))], name[find((N, k[3]))]))
                    else:
                        ks.append(("M", name[find((t, k[1]))], name[find((t, k[2]))], name[find((t, k[3]))]))
                rep_t.append(tuple(sorted(ks)))
            reps.append((tuple(rep_s), tuple(rep_t)))
    m = min(reps)
    return m, sum(1 for r in reps if r == m)


def enumerate_exact():
    S0 = ring(L0)
    classes = {}

    def ticks_from(S, allowed_new):
        yield ()
        for bundle, _ in ops.sites(S):
            (_, x, u), mk = bundle
            for y in allowed_new(S):
                k1 = ("S", x, u, y)
                s1 = ops.support(S, k1)
                s2 = ops.support(S, mk)
                if s1 & s2:
                    continue
                if not ops.valid(S, mk):
                    continue
                yield (k1, mk)

    def rec(t, slices, taus):
        S = slices[-1]
        last = t == T - 1
        def allowed_new(S_):
            if last:
                return [v for v in S0 if v not in S_]
            return [v for v in S0 if v not in S_] + [100 + t]
        seen = set()
        for tau in ticks_from(S, allowed_new):
            key = tuple(sorted(tau))
            if key in seen:
                continue
            seen.add(key)
            C = ops.copy(S)
            ok = all(ops.valid(C, k) for k in tau)
            if not ok:
                continue
            for k in tau:
                ops.apply(C, k)
            if len(tau) > CAP:
                continue
            if last:
                if C == S0:
                    rep, aut = canon(slices, taus + [tau])
                    classes[rep] = aut
            else:
                rec(t + 1, slices + [C], taus + [tau])
    rec(0, [S0], [])
    return classes


def sample(steps, seed, every=10, replay_every=1000):
    H = History([ring(L0) for _ in range(T)], ops, CAP, seed)
    counts = {}
    batches = []
    cur = {}
    bad = 0
    for i in range(1, steps + 1):
        H.step()
        if i % every == 0:
            rep, _ = canon(H.S, [list(tau) for tau in H.tau])
            counts[rep] = counts.get(rep, 0) + 1
            cur[rep] = cur.get(rep, 0) + 1
        if i % (steps // 20) == 0:
            batches.append(cur)
            cur = {}
        if i % replay_every == 0:
            ok, t, why = H.replay_ok()
            if not ok:
                bad += 1
    return H, counts, batches, bad


def main():
    t0 = time.perf_counter()
    exact = enumerate_exact()
    w = {k: 1.0 / a for k, a in exact.items()}
    Z = sum(w.values())
    p = {k: v / Z for k, v in w.items()}
    H, counts, batches, bad = sample(2_000_000, 1)
    n = sum(counts.values())
    extra = [k for k in counts if k not in p]
    missing = [k for k in p if k not in counts]
    nb = len(batches)
    zs = []
    chi2 = 0.0
    for k, pk in p.items():
        fr = [b.get(k, 0) / max(sum(b.values()), 1) for b in batches]
        se = np.std(fr, ddof=1) / np.sqrt(nb)
        f = counts.get(k, 0) / n
        z = (f - pk) / se if se > 0 else (0.0 if f == pk else float("inf"))
        zs.append(z)
        chi2 += (counts.get(k, 0) - n * pk) ** 2 / (n * pk)
    res = dict(classes=len(p), aut_counts={str(a): sum(1 for v in exact.values() if v == a) for a in set(exact.values())},
               samples=n, visited=len(counts), missing=len(missing), extra=len(extra), replay_failures=bad,
               max_abs_z=float(np.max(np.abs(zs))), n_z_over_3=int(np.sum(np.abs(zs) > 3)), chi2=chi2, dof=len(p) - 1,
               acceptance=H.acc / H.tried, why=H.why, seconds=time.perf_counter() - t0)
    json.dump(res, open(os.path.join(HERE, "sb_g1.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
