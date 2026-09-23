"""CGP, the constrained growth process (note 11, M1_Model_Spec.md; choices in IMPLEMENTATION_NOTES.md)."""
import time
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


class CGP:
    def __init__(self, K_over_sigma, c, k_max, kappa_min, N_final, seed,
                 sigma=0.05, W=50, tau_frac=0.2, B=10):
        self.rng = np.random.default_rng(seed)
        self.sigma, self.K = sigma, K_over_sigma * sigma
        self.c, self.k_max, self.kappa_min = c, k_max, kappa_min
        self.N_final, self.W, self.tau, self.B = N_final, W, tau_frac * sigma, B
        cap = N_final
        self.theta = np.zeros(cap)
        self.theta_birth = np.zeros(cap)
        self.omega = np.zeros(cap)
        self.birth_tick = np.zeros(cap, dtype=np.int64)
        self.hist = np.zeros((W, cap))
        self.Omega = np.zeros(cap)
        self.adj = [set() for _ in range(cap)]
        maxE = cap * k_max // 2 + 8
        self.ei = np.zeros(maxE, dtype=np.int64)
        self.ej = np.zeros(maxE, dtype=np.int64)
        self.epos = {}
        self.m = 0
        self.n = 0
        self.t = 0
        self.timers = dict(clock=0.0, moves=0.0, curvature=0.0, connect=0.0)
        self.counts = dict(births=0, birth_fail=0, pull_prop=0, pull_acc=0,
                           rew_att=0, rew_cand=0, rew_acc=0, lp=0)
        self.stalled = False
        self._consec_birth_fail = 0
        for _ in range(3):
            self._new_locus()
        self._add_edge(0, 1)
        self._add_edge(1, 2)
        self._add_edge(0, 2)

    # ---- structure ----
    def _new_locus(self):
        z = self.n
        self.omega[z] = self.rng.normal(0.0, self.sigma)
        th = self.rng.uniform(0.0, 2 * np.pi)
        self.theta[z] = th
        self.theta_birth[z] = th
        self.hist[:, z] = th
        self.birth_tick[z] = self.t
        self.n += 1
        return z

    def _add_edge(self, u, v):
        key = (u, v) if u < v else (v, u)
        self.ei[self.m], self.ej[self.m] = key
        self.epos[key] = self.m
        self.m += 1
        self.adj[u].add(v)
        self.adj[v].add(u)

    def _remove_edge(self, u, v):
        key = (u, v) if u < v else (v, u)
        p = self.epos.pop(key)
        last = self.m - 1
        if p != last:
            k2 = (int(self.ei[last]), int(self.ej[last]))
            self.ei[p], self.ej[p] = k2
            self.epos[k2] = p
        self.m -= 1
        self.adj[u].discard(v)
        self.adj[v].discard(u)

    # ---- curvature ----
    def _transport(self, u, v):
        """Masses (after cancelling common mass) and hop costs for Ollivier W1, laziness 1/2."""
        adj = self.adj
        Nu, Nv = adj[u], adj[v]
        A = {u: 0.5}
        for x in Nu:
            A[x] = A.get(x, 0.0) + 0.5 / len(Nu)
        Bm = {v: 0.5}
        for y in Nv:
            Bm[y] = Bm.get(y, 0.0) + 0.5 / len(Nv)
        for x in set(A) & set(Bm):
            cm = min(A[x], Bm[x])
            A[x] -= cm
            Bm[x] -= cm
        P = [x for x in A if A[x] > 1e-15]
        Q = [y for y in Bm if Bm[y] > 1e-15]
        a = np.array([A[x] for x in P])
        b = np.array([Bm[y] for y in Q])
        cost = np.empty((len(P), len(Q)))
        for i, x in enumerate(P):
            ax = adj[x]
            for j, y in enumerate(Q):
                if y in ax:
                    cost[i, j] = 1.0
                elif ax & adj[y]:
                    cost[i, j] = 2.0
                else:
                    cost[i, j] = 3.0
        return a, b, cost

    @staticmethod
    def _greedy_cost(a, b, cost):
        """A feasible plan filling cheapest pairs first: an upper bound on W1."""
        a = a.copy()
        b = b.copy()
        total = 0.0
        order = np.argsort(cost, axis=None, kind="stable")
        nQ = cost.shape[1]
        for k in order:
            i, j = divmod(int(k), nQ)
            f = min(a[i], b[j])
            if f > 0:
                total += f * cost[i, j]
                a[i] -= f
                b[j] -= f
        return total

    def _exact_w1(self, a, b, cost):
        nP, nQ = cost.shape
        A_eq = np.zeros((nP + nQ, nP * nQ))
        for i in range(nP):
            A_eq[i, i * nQ:(i + 1) * nQ] = 1.0
        for j in range(nQ):
            A_eq[nP + j, j::nQ] = 1.0
        t0 = time.perf_counter()
        res = linprog(cost.ravel(), A_eq=A_eq, b_eq=np.concatenate([a, b]), bounds=(0, None), method="highs")
        self.timers["curvature"] += time.perf_counter() - t0
        self.counts["lp"] += 1
        return res.fun

    def curvature(self, u, v):
        """Exact Ollivier curvature (laziness 1/2)."""
        a, b, cost = self._transport(u, v)
        if len(a) == 0:
            return 1.0
        return 1.0 - self._exact_w1(a, b, cost)

    def curvature_ok(self, loci):
        """Exact decision kappa >= kappa_min on every relation touching the loci.

        Screens: kappa <= 1 - (mass to move) always (every cost >= 1), and
        kappa >= 1 - greedy cost always (greedy is a feasible plan). The exact
        linear program runs only when the screens can't decide.
        """
        if not np.isfinite(self.kappa_min):
            return True
        t0 = time.perf_counter()
        seen = set()
        ok = True
        for u in loci:
            for v in self.adj[u]:
                key = (u, v) if u < v else (v, u)
                if key in seen:
                    continue
                seen.add(key)
                a, b, cost = self._transport(u, v)
                if len(a) == 0:
                    continue
                if 1.0 - a.sum() < self.kappa_min:
                    ok = False
                    break
                if 1.0 - self._greedy_cost(a, b, cost) >= self.kappa_min:
                    continue
                if 1.0 - self._exact_w1(a, b, cost) < self.kappa_min:
                    ok = False
                    break
            if not ok:
                break
        self.timers["curvature"] += time.perf_counter() - t0
        return ok

    def _reaches_all(self, a, targets):
        t0 = time.perf_counter()
        need = set(targets) - {a}
        seen = {a}
        frontier = [a]
        while frontier and need:
            nxt = []
            for x in frontier:
                for y in self.adj[x]:
                    if y not in seen:
                        seen.add(y)
                        need.discard(y)
                        nxt.append(y)
            frontier = nxt
        self.timers["connect"] += time.perf_counter() - t0
        return not need

    # ---- one tick ----
    def tick(self, births=True):
        n, m, W, t = self.n, self.m, self.W, self.t
        t0 = time.perf_counter()
        th = self.theta[:n]
        ei, ej = self.ei[:m], self.ej[:m]
        s = np.sin(th[ej] - th[ei])
        acc = np.bincount(ei, s, n) - np.bincount(ej, s, n)
        old = self.hist[t % W, :n].copy()
        self.theta[:n] = th + self.omega[:n] + (self.K / self.k_max) * acc
        self.hist[t % W, :n] = self.theta[:n]
        age = t + 1 - self.birth_tick[:n]
        Om = (self.theta[:n] - old) / W
        young = age < W
        Om[young] = (self.theta[:n][young] - self.theta_birth[:n][young]) / np.maximum(age[young], 1)
        self.Omega[:n] = Om
        deg = np.bincount(ei, minlength=n) + np.bincount(ej, minlength=n)
        sumO = np.bincount(ei, Om[ej], n) + np.bincount(ej, Om[ei], n)
        mis = np.abs(Om - sumO / np.maximum(deg, 1))
        out = np.where((mis > self.tau) & (~young) & (deg < self.k_max) & (deg > 0))[0]
        self.timers["clock"] += time.perf_counter() - t0

        t1 = time.perf_counter()
        if births and t % self.B == 0 and self.n < self.N_final:
            self._birth()
        self._sync_pull(out)
        self._rewire()
        self.timers["moves"] += time.perf_counter() - t1
        self.t += 1

    def _birth(self):
        p = self.rng.integers(self.m)
        a, b = int(self.ei[p]), int(self.ej[p])
        if len(self.adj[a]) >= self.k_max or len(self.adj[b]) >= self.k_max:
            self.counts["birth_fail"] += 1
            self._consec_birth_fail += 1
            if self._consec_birth_fail >= 10000:
                self.stalled = True
            return
        z = self._new_locus()
        self._add_edge(z, a)
        self._add_edge(z, b)
        if self.curvature_ok([z, a, b]):
            self.counts["births"] += 1
            self._consec_birth_fail = 0
        else:
            self._remove_edge(z, a)
            self._remove_edge(z, b)
            self.n -= 1
            self.counts["birth_fail"] += 1
            self._consec_birth_fail += 1
            if self._consec_birth_fail >= 10000:
                self.stalled = True

    def _sync_pull(self, out):
        if len(out) == 0:
            return
        x = int(out[self.rng.integers(len(out))])
        ax = self.adj[x]
        two = set()
        for y in ax:
            two |= self.adj[y]
        two -= ax
        two.discard(x)
        cands = [y for y in two if len(self.adj[y]) < self.k_max]
        if not cands:
            return
        y = cands[self.rng.integers(len(cands))]
        self.counts["pull_prop"] += 1
        if self.rng.random() >= np.exp(-self.c):
            return
        self._add_edge(x, y)
        if self.curvature_ok([x, y]):
            self.counts["pull_acc"] += 1
        else:
            self._remove_edge(x, y)

    def _ball2(self, a):
        b = {a} | self.adj[a]
        for y in self.adj[a]:
            b |= self.adj[y]
        return b

    def _rewire(self):
        self.counts["rew_att"] += 1
        p = self.rng.integers(self.m)
        u, v = int(self.ei[p]), int(self.ej[p])
        a, b = (u, v) if self.rng.random() < 0.5 else (v, u)
        B2a, B2b = self._ball2(a), self._ball2(b)
        cands = []
        for cc in B2a:
            if cc == a or cc == b:
                continue
            for dd in self.adj[cc]:
                if dd in B2b and dd != a and dd != b:
                    cands.append((cc, dd))
        if not cands:
            return
        cc, dd = cands[self.rng.integers(len(cands))]
        self.counts["rew_cand"] += 1
        if cc in self.adj[a] or dd in self.adj[b]:
            return
        O = self.Omega
        if abs(O[a] - O[cc]) + abs(O[b] - O[dd]) >= abs(O[a] - O[b]) + abs(O[cc] - O[dd]):
            return
        self._remove_edge(a, b)
        self._remove_edge(cc, dd)
        self._add_edge(a, cc)
        self._add_edge(b, dd)
        if self.curvature_ok([a, b, cc, dd]) and self._reaches_all(a, [b, cc, dd]):
            self.counts["rew_acc"] += 1
        else:
            self._remove_edge(a, cc)
            self._remove_edge(b, dd)
            self._add_edge(a, b)
            self._add_edge(cc, dd)

    # ---- run ----
    def to_csr(self):
        n, m = self.n, self.m
        r = np.concatenate([self.ei[:m], self.ej[:m]])
        c = np.concatenate([self.ej[:m], self.ei[:m]])
        return sp.csr_matrix((np.ones(2 * m), (r, c)), shape=(n, n))

    def run(self, on_checkpoint=None):
        tg = time.perf_counter()
        while self.n < self.N_final and not self.stalled:
            self.tick(births=True)
        self.growth_time = time.perf_counter() - tg
        self.growth_ticks = self.t
        tr = time.perf_counter()
        E0 = self.m
        target = 20 * E0
        start_att = self.counts["rew_att"]
        marks = [int(round(f * target)) for f in (0.0, 0.25, 0.5, 0.75, 1.0)]
        mi = 0
        if self.stalled:
            self.rest_time = 0.0
            return
        while True:
            done = self.counts["rew_att"] - start_att
            while mi < len(marks) and done >= marks[mi]:
                if on_checkpoint is not None:
                    on_checkpoint(self, mi)
                mi += 1
            if done >= target:
                break
            self.tick(births=False)
        self.rest_time = time.perf_counter() - tr
        self.rest_ticks = self.t - self.growth_ticks
