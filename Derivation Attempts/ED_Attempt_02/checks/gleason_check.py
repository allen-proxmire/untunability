"""Gleason for ED (RD2): does ED's own structure force the draw probabilities (the amount-squared rule)?

Alternatives tested: 'p-rules', where the chance of a record is proportional to (amount in it)^(p/2), i.e. ||P psi||^p,
normalized over the record's values. p = 2 is the usual rule (Born). Four checks:

  G1 (grouping, Gleason's non-contextuality). In 3 dimensions, a fixed 2-dimensional outcome S is split into two
     orthonormal directions in two different ways. The chance assigned to S, summed over its directions with weight
     |<v|psi>|^p, should not depend on the split.
  G2 (signalling, ED's RD22). A pattern shared by A (4 states) and B (3 states), entangled at random. A's draw fixes a
     record, fine ({0},{1},{2},{3}), coarse ({0,1},{2,3}), or none; then B's record is drawn. With a p-rule applied at
     each draw (post-draw state = normalized projection, as in the rebuilt draw), B's chances should not depend on what
     A did, or A could signal to B.
  G3 (the dimension condition). The 'closest direction gets chance 1' rule is non-Born. In 2 dimensions it is additive
     on every orthonormal basis (so Gleason's theorem needs dimension 3 or more); in 3 dimensions it fails additivity.
  G4 (ED's meetings). ED's meeting (the rebuilt draw's meet, A1-ledger C291) is linear and conserves the amount (the
     2-norm). A p-norm with p != 2 is not conserved by it, so a p-rule's total chance would change under ED's own
     meetings (Aaronson's point, C8 here).

Expected results, written down before the first run (2026-09-14):
  E1 G1: p = 2 gives the same chance for both splits to 1e-12; each of p = 1, 1.5, 3, 4 differs by more than 1e-3.
  E2 G2: p = 2 gives B the same chances whether A drew fine, coarse or not at all, to 1e-12; each p != 2 differs by more
     than 1e-3 somewhere.
  E3 G3: in 2 dimensions the closest-direction rule sums to 1 on all 1,000 random orthonormal bases and differs from
     Born by more than 0.1 somewhere; in 3 dimensions it fails to sum to 1 on at least one of 1,000 bases.
  E4 G4: the meeting keeps the 2-norm to 1e-12 and changes the 1-norm and 3-norm by more than 1e-3.
Reading: if E1-E4 hold, then within ED's structure (complex amplitudes with amount = |a|^2, P04 and P09; outcomes as
records, i.e. subspaces, A1-ledger RD28, RD50, C291; state space of dimension 3 or more; no signalling, RD22), only the
amount-squared rule survives among these alternatives, and Gleason's theorem (and Busch's extension) says no other
non-contextual rule exists at all. Still assumed: non-contextuality for a single isolated pattern.
Exit code: all four expected results.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_01", "04_Ways_Forward", "Commitment_Rule", "v3_draw"))

PS = (1.0, 1.5, 3.0, 4.0)
rng = np.random.default_rng(2026)


def rand_state(n):
    v = rng.normal(size=n) + 1j * rng.normal(size=n)
    return v / np.linalg.norm(v)


def rand_unitary(n):
    q, r = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))
    return q * (np.diag(r) / np.abs(np.diag(r)))


def g1():
    psi = rand_state(3)
    U = rand_unitary(3)
    e0, e1 = U[:, 0], U[:, 1]
    c, s = np.cos(0.7), np.sin(0.7) * np.exp(0.4j)
    f0, f1 = c * e0 + s * e1, -np.conj(s) * e0 + c * e1
    out = {}
    for p in (2.0,) + PS:
        w1 = abs(np.vdot(e0, psi)) ** p + abs(np.vdot(e1, psi)) ** p
        w2 = abs(np.vdot(f0, psi)) ** p + abs(np.vdot(f1, psi)) ** p
        out[p] = abs(w1 - w2)
    return out


def draw(psi_mat, partition, axis, p):
    """psi_mat has shape (dA, dB). Returns [(chance, normalized post-draw pattern)] for a record on `axis`."""
    weights, posts = [], []
    for block in partition:
        part = np.zeros_like(psi_mat)
        if axis == 0:
            part[block, :] = psi_mat[block, :]
        else:
            part[:, block] = psi_mat[:, block]
        n = np.linalg.norm(part)
        weights.append(n ** p)
        posts.append(part / n if n > 0 else part)
    weights = np.array(weights)
    return list(zip(weights / weights.sum(), posts))


def b_chances(psi_mat, a_partition, p):
    dB = psi_mat.shape[1]
    b_part = [[j] for j in range(dB)]
    if a_partition is None:
        return np.array([ch for ch, _ in draw(psi_mat, b_part, 1, p)])
    total = np.zeros(dB)
    for ca, post in draw(psi_mat, a_partition, 0, p):
        total += ca * np.array([ch for ch, _ in draw(post, b_part, 1, p)])
    return total


def g2():
    psi = rand_state(12).reshape(4, 3)
    fine = [[0], [1], [2], [3]]
    coarse = [[0, 1], [2, 3]]
    out = {}
    for p in (2.0,) + PS:
        b0, bf, bc = b_chances(psi, None, p), b_chances(psi, fine, p), b_chances(psi, coarse, p)
        out[p] = float(max(np.max(np.abs(b0 - bf)), np.max(np.abs(b0 - bc)), np.max(np.abs(bf - bc))))
    return out


def closest_rule(U, psi):
    ov = np.abs(U.conj().T @ psi) ** 2
    return np.where(ov > 0.5, 1.0, 0.0), ov


def g3():
    ok2, maxdiff2 = True, 0.0
    for _ in range(1000):
        psi, U = rand_state(2), rand_unitary(2)
        f, ov = closest_rule(U, psi)
        ok2 &= abs(f.sum() - 1) < 1e-12
        maxdiff2 = max(maxdiff2, float(np.max(np.abs(f - ov))))
    fail3 = 0
    for _ in range(1000):
        psi, U = rand_state(3), rand_unitary(3)
        f, _ = closest_rule(U, psi)
        fail3 += abs(f.sum() - 1) > 1e-12
    return ok2, maxdiff2, fail3


def g4():
    import rule_draw as d
    a = rand_state(31 * 3).reshape(31, 3)
    psi = d.start(a, 2)
    x = psi.copy()
    x[..., 0, 1] = 0.4 * psi[..., 0, 0]
    x /= np.sqrt(d.amount(x))
    y, _ = d.meet(x, [10, 11, 12], 0, 0.7)
    y, _ = d.meet(y, [12, 13], 1, 1.1)

    def pnorm(z, p):
        return float(np.sum(np.abs(z) ** p) ** (1 / p))

    return {p: abs(pnorm(y, p) - pnorm(x, p)) for p in (2.0, 1.0, 3.0)}


def main():
    r1, r2, (ok2, maxdiff2, fail3), r4 = g1(), g2(), g3(), g4()
    print("G1 grouping: difference between splits: %s" % ", ".join("p %.1f: %.2e" % (p, v) for p, v in r1.items()))
    print("G2 signalling: largest change in B's chances: %s" % ", ".join("p %.1f: %.2e" % (p, v) for p, v in r2.items()))
    print("G3 closest-direction rule: 2D additive on all bases %s (largest difference from Born %.3f); 3D bases where it fails %d of 1000"
          % (ok2, maxdiff2, fail3))
    print("G4 ED meeting: change in 2-norm %.2e, 1-norm %.2e, 3-norm %.2e" % (r4[2.0], r4[1.0], r4[3.0]))
    e1 = r1[2.0] < 1e-12 and all(r1[p] > 1e-3 for p in PS)
    e2 = r2[2.0] < 1e-12 and all(r2[p] > 1e-3 for p in PS)
    e3 = ok2 and maxdiff2 > 0.1 and fail3 >= 1
    e4 = r4[2.0] < 1e-12 and r4[1.0] > 1e-3 and r4[3.0] > 1e-3
    print("\nExpected results:")
    for name, ok in (("E1 grouping: only p = 2 is split-independent", e1), ("E2 signalling: only p = 2 keeps B's chances fixed", e2),
                     ("E3 dimension condition: loophole in 2D, closed in 3D", e3), ("E4 ED's meetings keep only the 2-norm", e4)):
        print("  %-8s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", name))
    return e1 and e2 and e3 and e4


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
