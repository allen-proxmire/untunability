"""Stage B core (note 14, C24): a sampler over whole periodic ED histories, generic over the slice type.

A history is T slices S_0..S_{T-1} (periodic) and, for each tick t, a set tau_t of changes taking S_t to S_{t+1}.
Changes are keyed canonically; each has a support (the events whose stars it changes). Changes in one tick have disjoint
supports (B-Q2), at most `cap` of them (C-Q3). An update picks t, proposes a balanced bundle c valid in S_t, sets
S_t' = c(S_t), and composes c into the neighbouring ticks: each part e of c cancels a change d in tau_{t-1} with d^-1 = e
or joins tau_{t-1} (support disjoint); and cancels an identical change in tau_t or joins tau_t as e^-1. Acceptance
min(1, q_rev / q_fwd): the bundle is applied, the slice type computes the reverse bundle's proposal probability in the new
slice, and a rejected bundle is undone exactly by its inverse changes in reverse order. Target: uniform over valid histories (C-Q1, D3).

Change keys:  ('S', x, u, y)  x splits along link xu, child y       inverse ('M', y, x, u)
              ('M', v, a, u)  v merges into a, other pole u          inverse ('S', a, u, v)
              ('F23', ring, apex)  ring, apex: frozensets             inverse ('F32', apex, ring)
              ('F32', edge, ring)                                     inverse ('F23', ring, edge)
"""
import numpy as np


def inverse(key):
    k = key[0]
    if k == "S":
        return ("M", key[3], key[1], key[2])
    if k == "M":
        return ("S", key[2], key[3], key[1])
    if k == "F23":
        return ("F32", key[2], key[1])
    return ("F23", key[2], key[1])


class History:
    def __init__(self, slices, ops, cap, seed):
        self.S = slices
        self.T = len(slices)
        self.ops = ops
        self.cap = cap
        self.rng = np.random.default_rng(seed)
        self.tau = [dict() for _ in range(self.T)]          # key -> support (frozenset)
        self.occ = [dict() for _ in range(self.T)]          # event -> key holding it
        self.acc = 0
        self.tried = 0
        self.why = {}
        self.p_swap = 0.2
        self.p_global = 0.0            # whole-history move (note 18 option (a), D18); 0 keeps G1-G2 behaviour

    # ---- whole-history move (D18): the same bundle applied to every slice ------------------------
    def global_bundle(self, parts):
        """Deterministic part: keys, or a reason. Valid only if the bundle's support avoids every tick's supports (so it
        commutes with every tick, which stays unchanged) and it is valid in every slice."""
        keys = []
        for p in parts:
            if p[0] == "S":
                keys.append(("S", p[1], p[2], self.ops.fresh(self.S)))
            else:
                keys.append(p)
        supps = [self.ops.support(self.S[0], k) for k in keys]
        for i in range(len(supps)):
            for j in range(i + 1, len(supps)):
                if supps[i] & supps[j]:
                    return "global bundle overlap"
        for t in range(self.T):
            occ = self.occ[t]
            for sp in supps:
                if any(w in occ for w in sp):
                    return "global tick overlap"
        for t in range(self.T):
            for k in keys:
                if not self.ops.valid(self.S[t], k):
                    return "global invalid"
                if self.ops.support(self.S[t], k) != self.ops.support(self.S[0], k):
                    return "global support differs"
        return keys

    def global_step(self):
        prop = self.ops.propose(self.S[0], self.rng)
        if prop is None:
            return self._no("global proposal")
        parts, q_fwd = prop
        keys = self.global_bundle(parts)
        if isinstance(keys, str):
            return self._no(keys)
        for S in self.S:
            for k in keys:
                self.ops.apply(S, k)
        q_rev = self.ops.reverse_q(self.S[0], keys)
        if q_rev < q_fwd and self.rng.random() >= q_rev / q_fwd:
            for S in self.S:
                for k in reversed(keys):
                    self.ops.apply(S, inverse(k))
            return self._no("global hastings")
        self.acc += 1
        self.acc_global = getattr(self, "acc_global", 0) + 1
        return True

    # ---- parent swap (G1 revision): which end of the link is the parent / absorber ---------------
    def swap_step(self):
        """Pick a tick and one of its changes uniformly; swap the child's parent (S(x,u,y) <-> S(u,x,y)) or the
        absorbing neighbour (M(v,a,u) <-> M(v,u,a)). Slices unchanged; support unchanged; self-inverse and symmetric."""
        t = int(self.rng.integers(self.T))
        if not self.tau[t]:
            return self._no("swap empty")
        ks = sorted(self.tau[t], key=repr)
        k = ks[int(self.rng.integers(len(ks)))]
        if k[0] == "S":
            nk = ("S", k[2], k[1], k[3])
        elif k[0] == "M":
            nk = ("M", k[1], k[3], k[2])
        else:
            return self._no("swap flip")
        if not self.ops.swap_valid(self.S[t], nk):
            return self._no("swap invalid")
        sp = self.tau[t].pop(k)
        self.tau[t][nk] = sp
        for w in sp:
            self.occ[t][w] = nk
        self.acc += 1
        return True

    # ---- labels -----------------------------------------------------------------------------
    def _new_label(self, t, x, u):
        L, R = (t - 1) % self.T, t
        for k in self.tau[L]:
            if k[0] == "M" and k[2] == x and k[3] == u:
                return k[1], "L"
        for k in self.tau[R]:
            if k[0] == "S" and k[1] == x and k[2] == u:
                return k[3], "R"
        return self.ops.fresh([self.S[L], self.S[t], self.S[(t + 1) % self.T]]), None

    # ---- one update -------------------------------------------------------------------------
    def step(self):
        self.tried += 1
        r = self.rng.random()
        if r < self.p_swap:
            return self.swap_step()
        if r < self.p_swap + self.p_global:
            return self.global_step()
        t = int(self.rng.integers(self.T))
        prop = self.ops.propose(self.S[t], self.rng)
        if prop is None:
            return self._no("proposal")
        parts, q_fwd = prop
        res = self.try_bundle(t, parts)
        if isinstance(res, str):
            return self._no(res)
        keys, tL, oL, tR, oR, L, R = res
        for k in keys:
            self.ops.apply(self.S[t], k)
        q_rev = self.ops.reverse_q(self.S[t], keys)
        if q_rev < q_fwd and self.rng.random() >= q_rev / q_fwd:
            for k in reversed(keys):                           # undo exactly
                self.ops.apply(self.S[t], inverse(k))
            return self._no("hastings")
        self.tau[L], self.occ[L], self.tau[R], self.occ[R] = tL, oL, tR, oR
        self.acc += 1
        return True

    def try_bundle(self, t, parts):
        """Deterministic part of a bundle update. Returns a reason string, or (keys, tL, oL, tR, oR, L, R)."""
        keys = []
        for p in parts:
            if p[0] == "S":
                y, _ = self._new_label(t, p[1], p[2])
                keys.append(("S", p[1], p[2], y))
            else:
                keys.append(p)
        supps = [self.ops.support(self.S[t], k) for k in keys]
        for i in range(len(supps)):
            for j in range(i + 1, len(supps)):
                if supps[i] & supps[j]:
                    return "bundle overlap"
        L, R = (t - 1) % self.T, t
        tL, oL = dict(self.tau[L]), dict(self.occ[L])
        tR, oR = dict(self.tau[R]), dict(self.occ[R])
        SL, SN = self.S[L], self.S[(t + 1) % self.T]
        for k, sp in zip(keys, supps):
            ik = inverse(k)
            if k[0] == "S":                                    # a new child's label must be free where it is new
                if ik not in tL and self.ops.has(SL, k[3]):
                    return "label left"
                if k not in tR and self.ops.has(SN, k[3]):
                    return "label right"
            if ik in tL:                                       # left: cancels
                for w in tL.pop(ik):
                    oL.pop(w, None)
            else:
                if any(w in oL for w in sp):
                    return "left overlap"
                tL[k] = sp
                for w in sp:
                    oL[w] = k
            if k in tR:                                        # right: cancels
                for w in tR.pop(k):
                    oR.pop(w, None)
            else:
                if any(w in oR for w in sp):
                    return "right overlap"
                tR[ik] = sp
                for w in sp:
                    oR[w] = ik
        if len(tL) > self.cap or len(tR) > self.cap:
            return "cap"
        return keys, tL, oL, tR, oR, L, R

    def _no(self, why):
        self.why[why] = self.why.get(why, 0) + 1
        return False

    # ---- G2: replay every tick ---------------------------------------------------------------
    def replay_ok(self):
        for t in range(self.T):
            C = self.ops.copy(self.S[t])
            for k in self.tau[t]:
                if not self.ops.valid(C, k):
                    return False, t, ("invalid", k)
            for k in self.tau[t]:
                self.ops.apply(C, k)
            if not self.ops.same(C, self.S[(t + 1) % self.T]):
                return False, t, "mismatch"
        return True, None, None


# ======================================================================= rings (gate G1)
class RingOps:
    """Slices are rings {id: [prev, next]}; narrow split inserts a child on a link; narrow merge removes an event
    (every ring event sits between two). Bundle: one split and one merge (V- and E-neutral)."""

    def labels(self, S):
        return set(S)

    def has(self, S, y):
        return y in S

    def fresh(self, slices):
        y = 0
        while any(y in S for S in slices):
            y += 1
        return y

    def copy(self, S):
        return {k: list(v) for k, v in S.items()}

    def same(self, A, B):
        return A == B

    def sites(self, S):
        """All (split, merge) bundles with their proposal probability (used by exact tests)."""
        ids = sorted(S)
        V = len(ids)
        out = []
        for x in ids:
            for j in (0, 1):
                u = S[x][1] if j == 0 else S[x][0]
                for v in ids:
                    for i in (0, 1):
                        a = S[v][1] if i == 0 else S[v][0]
                        uu = S[v][0] if i == 0 else S[v][1]
                        out.append(((("S", x, u), ("M", v, a, uu)), 1.0 / (V * 2 * V * 2)))
        return out

    def reverse_q(self, S, keys):
        return 1.0

    def propose(self, S, rng):
        ids = list(S)
        V = len(ids)
        if V < 4:
            return None
        x = ids[int(rng.integers(V))]
        u = S[x][1] if rng.integers(2) == 0 else S[x][0]
        v = ids[int(rng.integers(V))]
        i = int(rng.integers(2))
        a = S[v][1] if i == 0 else S[v][0]
        uu = S[v][0] if i == 0 else S[v][1]
        return [("S", x, u), ("M", v, a, uu)], 1.0

    def support(self, S, key):
        if key[0] == "S":
            return frozenset((key[1], key[2], key[3]))
        return frozenset((key[1], key[2], key[3]))

    def swap_valid(self, S, key):
        return True

    def valid(self, S, key):
        if key[0] == "S":
            _, x, u, y = key
            return x in S and u in S and u in S[x] and y not in S
        _, v, a, u = key
        return v in S and set(S[v]) == {a, u} and len(S) >= 4

    def apply(self, S, key):
        if key[0] == "S":
            _, x, u, y = key
            if S[x][1] == u:
                S[x][1] = y
                S[y] = [x, u]
                S[u][0] = y
            else:
                S[x][0] = y
                S[y] = [u, x]
                S[u][1] = y
        else:
            _, v, a, u = key
            p, n = S.pop(v)
            S[p][1] = n
            S[n][0] = p


def ring(L):
    return {i: [(i - 1) % L, (i + 1) % L] for i in range(L)}
