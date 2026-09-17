"""Check C188: pre-registered scan of P12 settings. Does 3D appear across a clear region? (RD33, C187)

Allen's decision, recorded before running (2026-09-13): "run the scan. if it doesn't work, we will impose P06."

Model: as in p12_growth.py (seeded growth 4 -> 1,728 loci, even births, P12-driven rewiring and phase
settling, 10 rewiring + 10 phase moves per birth, then 15 sweeps of each). Fixed: Str weight 1,
Grad weight 1, coherence in the "sum" reading (Wilson made no difference, C186), comfortable load 6.

The grid (27 cells), fixed before running:
  coherence weight  c in {0.25, 1, 4}
  temperature       T in {0.1, 0.3, 1.0}
  birth rule        B1: new locus links to a random locus v and 2 random loci within 2 steps of v
                    B2: new locus links to v and 2 random neighbours of v
                    B3: split: the new locus takes half of v's links (moved, phases kept), links to v,
                        and links to 2 random loci within 2 steps of v
  Every birth adds 3 links, so the average stays 6 links per locus.
Seed for cell k: 1000 + k. A cell that is 3D-like is rerun with seed 2000 + k.

3D-like (as in p12_growth.py, plus not a crystal): largest piece > 90%; d_s within 0.5 of the
12^3 lattice; mean distance within 30% of the lattice; growth dimension within 0.7 of 3;
perfect-lattice share below 0.9.

PASS RULE (fixed before running): keep the cells that are 3D-like on both seeds. Two cells are
neighbours if they differ in exactly one setting, by one step in c or T, or in birth rule (any two
rules count as neighbours). The scan PASSES if some connected group of kept cells has at least
3 cells. Otherwise it FAILS, and by Allen's prior decision P06 is imposed.

Claude's predictions, frozen before running:
  S1  The scan FAILS (no clear 3D region). Medium-high confidence.
  S2  At least 20 of the 27 cells have growth dimension above 3.7. Medium.
  S3  Within each (T, birth rule) pair, squares per locus rise with c in at least 7 of the 9 pairs. Medium.
  S4  The T = 1.0 cells have higher average d_s than the T = 0.1 cells. Medium.
All cells are printed and saved to p12_scan_results.json.

Changes after freezing (2026-09-13):
  First run (p12_scan_run1.txt): every cell printed; no cell 3D-like; SCAN FAILS; S1-S4 all RIGHT.
  The script then crashed while saving the JSON file (a numpy bool is not JSON-serialisable), after
  all results had been printed; the JSON file was not written and the text output is the record.
  Fixed: values are converted before saving. Added: `--spot` reruns cells 0, 10 and 26 with their
  original seeds and checks they reproduce the recorded first-run values (used by run_checks,
  because the full scan takes about 10 minutes). Nothing about the scan or pass rule changed.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components, shortest_path

sys.stdout.reconfigure(encoding="utf-8")
N_FINAL, SNAP = 1728, 216
MOVES_PER_BIRTH, RELAX_SWEEPS = 10, 15
CS = (0.25, 1.0, 4.0)
TS = (0.1, 0.3, 1.0)
BS = ("B1", "B2", "B3")


class World:
    def __init__(self, rng, c_weight, T, birth_rule):
        self.rng, self.cw, self.T, self.rule = rng, c_weight, T, birth_rule
        self.adj, self.d, self.q, self.phase = [], [], [], {}
        for _ in range(4):
            self.adj.append(set()); self.d.append(0); self.q.append(0)
        for a in range(4):
            for b in range(a + 1, 4):
                self.add_link(a, b, rng.uniform(-math.pi, math.pi))
        self.acc = [0, 0]; self.tries = [0, 0]

    def ph(self, a, b):
        return self.phase[(a, b)] if a < b else -self.phase[(b, a)]

    def set_ph(self, a, b, x):
        if a < b:
            self.phase[(a, b)] = x
        else:
            self.phase[(b, a)] = -x

    def squares(self, u, v):
        out = []
        Nv = self.adj[v]
        for a in self.adj[u]:
            if a == v:
                continue
            for b in self.adj[a] & Nv:
                if b != u:
                    out.append((a, b))
        return out

    def add_link(self, x, y, phi):
        self.adj[x].add(y); self.adj[y].add(x)
        self.set_ph(x, y, phi)
        self.d[x] += 1; self.d[y] += 1
        for a, b in self.squares(x, y):
            for z in (x, y, a, b):
                self.q[z] += 1

    def remove_link(self, x, y):
        for a, b in self.squares(x, y):
            for z in (x, y, a, b):
                self.q[z] -= 1
        phi = self.ph(x, y)
        self.adj[x].discard(y); self.adj[y].discard(x)
        del self.phase[(min(x, y), max(x, y))]
        self.d[x] -= 1; self.d[y] -= 1
        return phi

    def within2(self, v, exclude):
        cand = set(self.adj[v])
        for x in self.adj[v]:
            cand |= self.adj[x]
        return [x for x in cand if x not in exclude]

    def birth(self):
        rng = self.rng
        v = int(rng.integers(len(self.adj)))
        w = len(self.adj)
        self.adj.append(set()); self.d.append(0); self.q.append(0)
        if self.rule == "B1":
            cand = self.within2(v, {v, w})
            pick = [int(x) for x in rng.choice(cand, size=min(2, len(cand)), replace=False)] if cand else []
            for y in [v] + pick:
                self.add_link(w, y, rng.uniform(-math.pi, math.pi))
        elif self.rule == "B2":
            cand = [x for x in self.adj[v] if x != w]
            pick = [int(x) for x in rng.choice(cand, size=min(2, len(cand)), replace=False)] if cand else []
            for y in [v] + pick:
                self.add_link(w, y, rng.uniform(-math.pi, math.pi))
        else:  # B3 split
            nb = list(self.adj[v])
            rng.shuffle(nb)
            for x in nb[: len(nb) // 2]:
                phi = self.remove_link(v, x)
                self.add_link(w, x, phi)
            self.add_link(w, v, rng.uniform(-math.pi, math.pi))
            cand = self.within2(v, {v, w} | self.adj[w])
            pick = [int(x) for x in rng.choice(cand, size=min(2, len(cand)), replace=False)] if cand else []
            for y in pick:
                self.add_link(w, y, rng.uniform(-math.pi, math.pi))

    def grad_term(self, x, y, dd, dq):
        dx = self.d[x] + dd.get(x, 0); dy = self.d[y] + dd.get(y, 0)
        qx = self.q[x] + dq.get(x, 0); qy = self.q[y] + dq.get(y, 0)
        return (dx - dy) ** 2 + 0.1 * (qx - qy) ** 2

    def accept(self, dE):
        return dE <= 0 or self.rng.random() < math.exp(-dE / self.T)

    def rewire(self):
        rng, adj = self.rng, self.adj
        u = int(rng.integers(len(adj)))
        if len(adj[u]) < 2:
            return
        nb = list(adj[u])
        v = nb[int(rng.integers(len(nb)))]
        x = nb[int(rng.integers(len(nb)))]
        xn = list(adj[x])
        w = xn[int(rng.integers(len(xn)))]
        if w == u or w in adj[u] or len(adj[v]) < 2:
            return
        self.tries[0] += 1
        phi = rng.uniform(-math.pi, math.pi)
        old = self.squares(u, v)
        new = [(a, b) for a in adj[u] if a != v for b in adj[a] & adj[w] if b != u]
        dq = {}
        for a, b in old:
            for z in (u, v, a, b):
                dq[z] = dq.get(z, 0) - 1
        for a, b in new:
            for z in (u, w, a, b):
                dq[z] = dq.get(z, 0) + 1
        dd = {v: -1, w: 1}
        dE = sum((self.d[z] + c - 6) ** 2 - (self.d[z] - 6) ** 2 for z, c in dd.items())
        aff = {u, v, w} | set(dq)
        before = {(min(z, y), max(z, y)) for z in aff for y in adj[z]}
        after = (before - {(min(u, v), max(u, v))}) | {(min(u, w), max(u, w))}
        dE += sum(self.grad_term(a, b, dd, dq) for a, b in after) - sum(self.grad_term(a, b, {}, {}) for a, b in before)
        c_old = sum(math.cos(self.ph(u, a) + self.ph(a, b) + self.ph(b, v) + self.ph(v, u)) for a, b in old)
        c_new = sum(math.cos(self.ph(u, a) + self.ph(a, b) + self.ph(b, w) - phi) for a, b in new)
        dE -= self.cw * (c_new - c_old)
        if self.accept(dE):
            self.acc[0] += 1
            adj[u].discard(v); adj[v].discard(u)
            del self.phase[(min(u, v), max(u, v))]
            adj[u].add(w); adj[w].add(u)
            self.set_ph(u, w, phi)
            for z, c in dd.items():
                self.d[z] += c
            for z, c in dq.items():
                self.q[z] += c

    def phase_move(self):
        rng, adj = self.rng, self.adj
        u = int(rng.integers(len(adj)))
        if not adj[u]:
            return
        nb = list(adj[u])
        v = nb[int(rng.integers(len(nb)))]
        self.tries[1] += 1
        old = self.ph(u, v)
        new = old + rng.uniform(-math.pi / 2, math.pi / 2)
        dC = 0.0
        for a, b in self.squares(u, v):
            base = self.ph(u, a) + self.ph(a, b) + self.ph(b, v)
            dC += math.cos(base - new) - math.cos(base - old)
        if self.accept(-self.cw * dC):
            self.acc[1] += 1
            self.set_ph(u, v, new)

    def run(self):
        snap = None
        while len(self.adj) < N_FINAL:
            self.birth()
            for _ in range(MOVES_PER_BIRTH):
                self.rewire()
                self.phase_move()
            if len(self.adj) == SNAP:
                snap = exact_mean_distance(self.adj)[0]
        links = sum(self.d) // 2
        for _ in range(RELAX_SWEEPS * links):
            self.rewire()
            self.phase_move()
        return snap


def to_csr(adj):
    n = len(adj)
    rows = np.repeat(np.arange(n), [len(s) for s in adj])
    cols = np.fromiter((u for s in adj for u in s), dtype=np.int64, count=len(rows))
    return csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))


def exact_mean_distance(adj):
    A = to_csr(adj)
    ncomp, labels = connected_components(A, directed=False)
    big = np.bincount(labels).argmax()
    keep = np.flatnonzero(labels == big)
    Ak = A[keep][:, keep]
    nk = len(keep)
    if nk < 2:
        return float("nan"), Ak, ncomp, nk
    D = shortest_path(Ak, method="D", unweighted=True)
    return D.sum() / (nk * nk - nk), Ak, ncomp, nk


def lattice(n):
    adj = []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                nb = set()
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    nb.add(((x + dx) % n) * n * n + ((y + dy) % n) * n + (z + dz) % n)
                adj.append(nb)
    return adj


def measure(adj, rng, snap_dist):
    n = len(adj)
    mean_dist, Ak, ncomp, nk = exact_mean_distance(adj)
    d_s = float("nan")
    if nk >= 2:
        S = min(40, nk)
        src = rng.choice(nk, size=S, replace=False)
        deg = np.asarray(Ak.sum(axis=1)).ravel()
        M = (0.5 * (diags(1.0 / deg) @ Ak)).T.tocsr()
        p = np.zeros((nk, S))
        p[src, np.arange(S)] = 1.0
        ret = {}
        for t in range(1, 65):
            p = 0.5 * p + M @ p
            if t in (16, 64):
                ret[t] = p[src, np.arange(S)].mean()
        d_s = -2 * math.log(ret[64] / ret[16]) / math.log(4)
    q = np.zeros(n)
    for u in range(n):
        Nu = list(adj[u])
        for i in range(len(Nu)):
            for j in range(i + 1, len(Nu)):
                q[u] += len(adj[Nu[i]] & adj[Nu[j]]) - 1
    degs = np.array([len(s) for s in adj])
    tri = np.array([sum(len(adj[a] & adj[u]) for a in adj[u]) // 2 for u in range(n)])
    perfect = float(np.mean((degs == 6) & (q == 12) & (tri == 0)))
    D_g = float("nan")
    if snap_dist and mean_dist == mean_dist and mean_dist > 1.01 * snap_dist:
        D_g = math.log(8) / math.log(mean_dist / snap_dist)
    return {"pieces": int(ncomp), "largest": nk / n, "distance": mean_dist, "d_s": d_s,
            "squares": float(q.mean()), "perfect": perfect, "spread": float(degs.std()), "D_g": D_g}


def main():
    rng_m = np.random.default_rng(31)
    control = measure(lattice(12), rng_m, exact_mean_distance(lattice(6))[0])

    def three_d(m):
        return (m["largest"] > 0.9 and abs(m["d_s"] - control["d_s"]) < 0.5
                and abs(m["distance"] - control["distance"]) < 0.3 * control["distance"]
                and abs(m["D_g"] - 3) < 0.7 and m["perfect"] < 0.9)

    cells = [(ci, ti, bi) for ci in range(3) for ti in range(3) for bi in range(3)]
    results = {}
    print("control: distance %.4f  d_s %.4f  D_g %.4f" % (control["distance"], control["d_s"], control["D_g"]))
    print("%-4s %5s %4s %3s %7s %8s %9s %7s %8s %8s %7s %6s" % ("cell", "c", "T", "B", "pieces", "largest", "distance",
                                                                "d_s", "squares", "perfect", "D_g", "3D"))
    for k, (ci, ti, bi) in enumerate(cells):
        w = World(np.random.default_rng(1000 + k), CS[ci], TS[ti], BS[bi])
        snap = w.run()
        m = measure(w.adj, np.random.default_rng(3000 + k), snap)
        m["three_d"] = three_d(m)
        m["accept"] = w.acc[0] / max(1, w.tries[0])
        results[k] = m
        print("%-4d %5.2f %4.1f %3s %7d %8.4f %9.4f %7.3f %8.3f %8.4f %7.3f %6s" % (
            k, CS[ci], TS[ti], BS[bi], m["pieces"], m["largest"], m["distance"], m["d_s"], m["squares"],
            m["perfect"], m["D_g"], m["three_d"]), flush=True)

    kept = []
    for k, (ci, ti, bi) in enumerate(cells):
        if results[k]["three_d"]:
            w = World(np.random.default_rng(2000 + k), CS[ci], TS[ti], BS[bi])
            snap = w.run()
            m2 = measure(w.adj, np.random.default_rng(4000 + k), snap)
            results[k]["seed2"] = m2
            results[k]["seed2_three_d"] = three_d(m2)
            print("seed 2, cell %d: D_g %.3f, d_s %.3f, distance %.4f, 3D-like %s" % (k, m2["D_g"], m2["d_s"], m2["distance"], three_d(m2)))
            if three_d(m2):
                kept.append(k)

    def neighbours(a, b):
        (c1, t1, b1), (c2, t2, b2) = cells[a], cells[b]
        diffs = [c1 != c2, t1 != t2, b1 != b2]
        if sum(diffs) != 1:
            return False
        if c1 != c2:
            return abs(c1 - c2) == 1
        if t1 != t2:
            return abs(t1 - t2) == 1
        return True

    groups, seen = [], set()
    for k in kept:
        if k in seen:
            continue
        stack, group = [k], []
        seen.add(k)
        while stack:
            x = stack.pop()
            group.append(x)
            for y in kept:
                if y not in seen and neighbours(x, y):
                    seen.add(y)
                    stack.append(y)
        groups.append(sorted(group))
    passed = any(len(g) >= 3 for g in groups)

    n_high = sum(1 for k in results if results[k]["D_g"] == results[k]["D_g"] and results[k]["D_g"] > 3.7)
    rising = 0
    for ti in range(3):
        for bi in range(3):
            sq = [results[cells.index((ci, ti, bi))]["squares"] for ci in range(3)]
            rising += sq[0] < sq[1] < sq[2]
    ds_hot = np.nanmean([results[k]["d_s"] for k, (ci, ti, bi) in enumerate(cells) if ti == 2])
    ds_cold = np.nanmean([results[k]["d_s"] for k, (ci, ti, bi) in enumerate(cells) if ti == 0])

    print("\n3D-like on seed 1: %s" % [k for k in results if results[k]["three_d"]])
    print("3D-like on both seeds: %s; connected groups: %s" % (kept, groups))
    print("SCAN %s" % ("PASSES: a clear 3D region exists" if passed else "FAILS: no clear 3D region -> impose P06 (Allen's prior decision)"))
    print("\nClaude's frozen predictions:")
    print("  %-6s S1 scan fails" % ("RIGHT" if not passed else "WRONG"))
    print("  %-6s S2 at least 20 of 27 cells with D_g > 3.7 (got %d)" % ("RIGHT" if n_high >= 20 else "WRONG", n_high))
    print("  %-6s S3 squares rise with c in at least 7 of 9 (T, B) pairs (got %d)" % ("RIGHT" if rising >= 7 else "WRONG", rising))
    print("  %-6s S4 T = 1.0 cells have higher mean d_s than T = 0.1 cells (%.3f vs %.3f)" % ("RIGHT" if ds_hot > ds_cold else "WRONG", ds_hot, ds_cold))

    out = {"control": control, "cells": {str(k): {"c": CS[cells[k][0]], "T": TS[cells[k][1]], "B": BS[cells[k][2]], **results[k]}
                                         for k in results},
           "kept": kept, "groups": groups, "passed": passed}
    Path(__file__).with_name("p12_scan_results.json").write_text(
        json.dumps(out, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding="utf-8")


RECORDED = {  # first-run values (p12_scan_run1.txt): distance (4 d.p.), d_s, squares, D_g (3 d.p.)
    0: (5.3627, 4.310, 4.690, 4.777),
    10: (6.3301, 2.218, 7.743, 3.895),
    26: (5.5454, 3.931, 5.632, 4.755),
}


def spot():
    cells = [(ci, ti, bi) for ci in range(3) for ti in range(3) for bi in range(3)]
    ok = True
    for k, (dist, d_s, sq, D_g) in RECORDED.items():
        ci, ti, bi = cells[k]
        w = World(np.random.default_rng(1000 + k), CS[ci], TS[ti], BS[bi])
        snap = w.run()
        m = measure(w.adj, np.random.default_rng(3000 + k), snap)
        good = (abs(m["distance"] - dist) < 1e-4 and abs(m["d_s"] - d_s) < 1e-3
                and abs(m["squares"] - sq) < 1e-3 and abs(m["D_g"] - D_g) < 1e-3)
        ok &= good
        print("%-4s cell %d (c %.2f, T %.1f, %s): distance %.4f, d_s %.3f, squares %.3f, D_g %.3f" % (
            "PASS" if good else "FAIL", k, CS[ci], TS[ti], BS[bi], m["distance"], m["d_s"], m["squares"], m["D_g"]))
    print("ALL PASS" if ok else "SOME FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if "--spot" in sys.argv:
        spot()
    else:
        main()
