"""The budget slows spreading (V0-L1, RD16), on a 1D ring test bed. See Spec.md.

A pattern is a vector over (locus u, channel K), K in (INTERNAL, LEFT, RIGHT), index 3u + K.
H is a local Hermitian spreading generator; m is the positive rest term (D7);
the budget slows everything at a locus by s(u) = 1 - U(u):  H_s = sqrt(S) (H + m) sqrt(S).
"""
import numpy as np

INTERNAL, LEFT, RIGHT = 0, 1, 2
G = (2.0 / 3.0) * np.ones((3, 3)) - np.eye(3)  # Hermitian lane mixing (continuous-time counterpart of V0-D1)


def idx(u, K, L):
    return 3 * (u % L) + K


def generator(L, g=1.0):
    """Local Hermitian spreading generator on a ring of L loci (no rest term)."""
    H = np.zeros((3 * L, 3 * L), dtype=complex)
    for u in range(L):
        for K1 in range(3):
            for K2 in range(3):
                H[idx(u, K1, L), idx(u, K2, L)] += g * G[K1, K2]
        # Right lane: +i (T - T^dagger), T|u> = |u+1>
        H[idx(u + 1, RIGHT, L), idx(u, RIGHT, L)] += 1j
        H[idx(u, RIGHT, L), idx(u + 1, RIGHT, L)] += -1j
        # Left lane: -i (T - T^dagger)
        H[idx(u + 1, LEFT, L), idx(u, LEFT, L)] += -1j
        H[idx(u, LEFT, L), idx(u + 1, LEFT, L)] += 1j
    return H


def slowed(H, U, m):
    """RD16: everything at a locus slows by s = 1 - U, placed symmetrically so H_s stays Hermitian."""
    L = len(U)
    root_s = np.repeat(np.sqrt(np.maximum(0.0, 1.0 - np.asarray(U, dtype=float))), 3)
    return (root_s[:, None] * (H + m * np.eye(3 * L))) * root_s[None, :]


def split_parts(H):
    """Split a generator into its on-locus part (lane mixing) and its moving part (hops between loci)."""
    n = H.shape[0]
    onsite = np.zeros_like(H)
    for b in range(0, n, 3):
        onsite[b:b + 3, b:b + 3] = H[b:b + 3, b:b + 3]
    return onsite, H - onsite


def slowed_rd35(H, U, m):
    """RD35: ticking and internal change at a locus slow by s (rest term and lane mixing, placed as
    sqrt(S) ... sqrt(S)); moving between loci slows by s^2 (each hop u-v weighted by s(u) s(v))."""
    L = len(U)
    s = np.repeat(np.maximum(0.0, 1.0 - np.asarray(U, dtype=float)), 3)
    onsite, hop = split_parts(H)
    root = np.sqrt(s)
    return (root[:, None] * (onsite + m * np.eye(3 * L))) * root[None, :] + (s[:, None] * hop) * s[None, :]


def slowed_rd36(H, U, m):
    """RD36: as RD35, but the rate is s = e^(-U) (used budget removes a share of what's left):
    ticking and internal change slow by e^(-U), moving between loci by e^(-2U)."""
    L = len(U)
    s = np.repeat(np.exp(-np.asarray(U, dtype=float)), 3)
    onsite, hop = split_parts(H)
    root = np.sqrt(s)
    return (root[:, None] * (onsite + m * np.eye(3 * L))) * root[None, :] + (s[:, None] * hop) * s[None, :]


def evolve(Hs, psi, t):
    w, V = np.linalg.eigh(Hs)
    return V @ (np.exp(-1j * w * t) * (V.conj().T @ psi))


def mirror_state(psi, L):
    """Locus u -> -u (mod L), Left <-> Right."""
    a = psi.reshape(L, 3)
    b = a[(-np.arange(L)) % L][:, [INTERNAL, RIGHT, LEFT]]
    return b.reshape(-1)


def mirror_profile(U):
    L = len(U)
    return np.asarray(U)[(-np.arange(L)) % L]


def shares(psi, L):
    return (np.abs(psi.reshape(L, 3)) ** 2).sum(axis=1)


def mass_profile(L, center, U0, a=5.0):
    u = np.arange(L)
    d = np.minimum(np.abs(u - center), L - np.abs(u - center))
    return U0 * a / np.sqrt(d ** 2 + a ** 2)
