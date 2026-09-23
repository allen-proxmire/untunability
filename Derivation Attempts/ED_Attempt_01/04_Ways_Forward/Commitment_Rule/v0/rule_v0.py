"""Commitment rule, version 0, on a 1D ring of loci.

Built from ledger decisions RD1-RD21. See Spec.md for what is and isn't included.

A pattern is an array a[u, K] of complex amplitudes: u = locus (0..L-1),
K = channel (INTERNAL, LEFT, RIGHT). Bandwidth is |a|^2.
An entangled two-part pattern is an array A[uA, KA, uB, KB] over two rings.
"""
import numpy as np

INTERNAL, LEFT, RIGHT = 0, 1, 2
GROVER = (2.0 / 3.0) * np.ones((3, 3)) - np.eye(3)  # V0-D1: parameter-free, channel-symmetric coin


# ---------- single pattern ----------

def walk_step(a):
    """One substrate step of spreading: coin at every locus, then shift. Linear and conserving."""
    b = a @ GROVER.T
    out = np.empty_like(b)
    out[:, INTERNAL] = b[:, INTERNAL]
    out[:, RIGHT] = np.roll(b[:, RIGHT], 1)   # Right content moves u -> u+1
    out[:, LEFT] = np.roll(b[:, LEFT], -1)    # Left content moves u -> u-1
    return out


def mirror(a):
    """Reflection: locus u -> -u (mod L), and Left <-> Right."""
    L = a.shape[0]
    return a[(-np.arange(L)) % L][:, [INTERNAL, RIGHT, LEFT]]


def shares(a):
    """Per-locus bandwidth."""
    return (np.abs(a) ** 2).sum(axis=1)


def too_thin(a, b_min):
    """RD19: a lone pattern draws when its largest per-locus share falls below b_min."""
    s = shares(a)
    return s.max() / s.sum() < b_min


def draw_probabilities(a):
    """RD13 (G7): probability of drawing each (locus, channel) is proportional to bandwidth."""
    p = np.abs(a) ** 2
    return p / p.sum()


def draw(a, rng):
    """RD3, RD11: pick one option, zero the rest, keep the drawn content's phase, keep the total amount."""
    p = draw_probabilities(a).ravel()
    k = rng.choice(p.size, p=p)
    flat = a.ravel()
    out = np.zeros_like(flat)
    total = np.sqrt((np.abs(flat) ** 2).sum())
    out[k] = flat[k] / abs(flat[k]) * total
    return out.reshape(a.shape)


def decohered_step(P):
    """Comparison only (not part of the rule): the same step probabilities with no interference.
    P[u, K] are populations."""
    b = P @ (GROVER ** 2).T
    out = np.empty_like(b)
    out[:, INTERNAL] = b[:, INTERNAL]
    out[:, RIGHT] = np.roll(b[:, RIGHT], 1)
    out[:, LEFT] = np.roll(b[:, LEFT], -1)
    return out


# ---------- budget and clock ticks ----------

def budget_step(U, M, q):
    """RD14: used budget = mass here + q * average of the neighbours' used budget, capped at 1."""
    return np.minimum(1.0, M + q * 0.5 * (np.roll(U, 1) + np.roll(U, -1)))


def budget_steady(M, q, tol=1e-15, max_steps=1_000_000):
    U = np.zeros_like(M, dtype=float)
    for _ in range(max_steps):
        new = budget_step(U, M, q)
        if np.max(np.abs(new - U)) < tol:
            return new
        U = new
    raise RuntimeError("budget did not settle")


def rate(U):
    """RD14, RD16: local rate factor = share of budget left."""
    return np.maximum(0.0, 1.0 - U)


def clock_ticks_per_step(a, U, omega=1.0):
    """RD18: clock ticks gained in one step, bandwidth-weighted over the loci the pattern covers."""
    s = shares(a)
    return omega * (s * rate(U)).sum() / s.sum()


def hinged_draw_probability(part_probabilities):
    """RD10, RD14: a hinged pattern draws if any part triggers."""
    return 1.0 - np.prod(1.0 - np.asarray(part_probabilities))


# ---------- entangled two-part pattern ----------

def walk_step_part(A, part):
    """Spread one part (0 = A, 1 = B) of a two-part pattern by one step."""
    if part == 1:
        A = A.transpose(2, 3, 0, 1)
    L = A.shape[0]
    flat = A.reshape(L, 3, -1)
    b = np.einsum("ij,ujx->uix", GROVER, flat)
    out = np.empty_like(b)
    out[:, INTERNAL] = b[:, INTERNAL]
    out[:, RIGHT] = np.roll(b[:, RIGHT], 1, axis=0)
    out[:, LEFT] = np.roll(b[:, LEFT], -1, axis=0)
    out = out.reshape(A.shape)
    return out.transpose(2, 3, 0, 1) if part == 1 else out


def part_shares(A, part):
    """Per-locus bandwidth of one part, summed over everything else."""
    P = np.abs(A) ** 2
    return P.sum(axis=(1, 2, 3)) if part == 0 else P.sum(axis=(0, 1, 3))


def part_too_thin(A, part, b_min):
    s = part_shares(A, part)
    return s.max() / s.sum() < b_min


def bob_distribution_no_draw(A):
    return part_shares(A, 1) / part_shares(A, 1).sum()


def draw_entangled(A, part, rng):
    """RD22: the draw fixes only the part that interacts (0 = A, 1 = B). That part's locus and
    channel are drawn in proportion to its bandwidth; the other part keeps the conditional
    pattern that goes with the outcome. Phase kept (RD11); total amount kept."""
    total = np.sqrt((np.abs(A) ** 2).sum())
    B = A if part == 0 else A.transpose(2, 3, 0, 1)
    p = (np.abs(B) ** 2).sum(axis=(2, 3))
    p = (p / p.sum()).ravel()
    k = rng.choice(p.size, p=p)
    u, K = divmod(k, 3)
    out = np.zeros_like(B)
    slice_rest = B[u, K]
    out[u, K] = slice_rest / np.sqrt((np.abs(slice_rest) ** 2).sum()) * total
    return out if part == 0 else out.transpose(2, 3, 0, 1)


def bob_average_after_joint_draw(A, bob_steps):
    """REJECTED OPTION (RD22), kept for comparison only. Joint draw: one draw fixes both parts'
    locus and channel, which allows signalling (C81).
    Returns Bob's per-locus distribution after bob_steps, averaged exactly over outcomes."""
    P = np.abs(A) ** 2
    P = P / P.sum()
    pB = P.sum(axis=(0, 1))                      # probability of each (uB, KB)
    L = A.shape[2]
    avg = np.zeros(L)
    for uB in range(L):
        for KB in range(3):
            if pB[uB, KB] == 0:
                continue
            b = np.zeros((L, 3), dtype=complex)
            b[uB, KB] = 1.0
            for _ in range(bob_steps):
                b = walk_step(b)
            avg += pB[uB, KB] * shares(b)
    return avg


def bob_average_after_local_draw(A, bob_steps):
    """The rule (RD22): the draw fixes only part A's locus and channel; Bob keeps the conditional pattern.
    Returns Bob's per-locus distribution after bob_steps, averaged exactly over outcomes."""
    L = A.shape[2]
    total = (np.abs(A) ** 2).sum()
    avg = np.zeros(L)
    for uA in range(A.shape[0]):
        for KA in range(3):
            slice_b = A[uA, KA]
            w = (np.abs(slice_b) ** 2).sum() / total
            if w == 0:
                continue
            b = slice_b / np.sqrt((np.abs(slice_b) ** 2).sum())
            for _ in range(bob_steps):
                b = walk_step(b)
            avg += w * shares(b)
    return avg
