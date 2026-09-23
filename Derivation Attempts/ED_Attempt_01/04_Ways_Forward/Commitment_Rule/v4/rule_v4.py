"""Rule version 4: the tuned handedness test on the rebuilt draw (RD51). See Spec.md.

Transfer meetings at committed loci: where a pattern is in the Right or Left lane at committed locus x, part of it moves
into x's Internal channel, and committed matter records that the transfer happened in R identical fragments. Per step
dt the transfer probability is p = gamma dt. Under the rebuilt draw (RD50) a record with R >= R_STAR is drawn: only the
record (transferred or not) is fixed.

Explicit description: pattern plus records, draws branching. The R fragments of one record are always all unmarked or
all marked, so they are stored as one two-level record carrying its count R (exact for this meeting type).
Population description: one-pattern density matrix, rho -> U rho U^dagger, then for each committed lane channel
a = (x, K): K0 = 1 - (1 - sqrt(1 - p)) P_a, K1 = sqrt(p) |x, INTERNAL><x, K|.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("v2b", "v2", "v1_budget"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
from rule_v2b import INTERNAL, LEFT, RIGHT, RuleB, mirror_perm, pure, purity  # noqa: E402,F401

R_STAR = 3


def unitary(H, dt):
    w, V = np.linalg.eigh(H)
    return (V * np.exp(-1j * w * dt)) @ V.conj().T


def lane_channels(L, D):
    x = np.arange(0, L, D)
    return np.concatenate([3 * x + RIGHT, 3 * x + LEFT]), np.concatenate([3 * x + INTERNAL, 3 * x + INTERNAL])


def kraus(rho, lane, dest, p):
    """Population map for transfer meetings with drawn (or traced) records."""
    n = rho.shape[0]
    scale = np.ones(n)
    scale[lane] = np.sqrt(1 - p)
    old = np.real(np.diag(rho))[lane]
    out = scale[:, None] * rho * scale[None, :]
    add = np.zeros(n)
    np.add.at(add, dest, p * old)
    out[np.diag_indices(n)] += add
    return out


def explicit_average(H, dt, lane, dest, p, psi0, steps, R, r_star=R_STAR):
    """Pattern plus records; the system density matrix averaged over draws and traced over records."""
    U = unitary(H, dt)
    n = len(psi0)
    branches = [(1.0, psi0.reshape(n, 1).astype(complex))]
    for _ in range(steps):
        branches = [(w, U @ b) for w, b in branches]
        for a, i_dest, pa in zip(lane, dest, p):
            s, c = np.sqrt(pa), np.sqrt(1 - pa)
            new = []
            for w, b in branches:
                m = b.shape[1]
                out = np.zeros((n, m, 2), dtype=complex)
                out[:, :, 0] = b
                out[a, :, 0] = c * b[a]
                out[i_dest, :, 1] = s * b[a]
                if R >= r_star:
                    for rec in (0, 1):
                        part = out[:, :, rec]
                        wt = float((np.abs(part) ** 2).sum())
                        if wt > 1e-300:
                            new.append((w * wt, part / np.sqrt(wt)))
                else:
                    new.append((w, out.reshape(n, 2 * m)))
            branches = new
    return sum(w * (b @ b.conj().T) for w, b in branches)


class PopulationV4:
    """The tuned test's settings with transfer meetings and the rebuilt draw, in population form."""

    def __init__(self, L, D, Gamma, g, theta, V0, dt):
        self.rule = RuleB(L, D, Gamma, g, theta, V0, phase_mode="const")
        self.rule.theta = np.full(L, float(theta))
        self.H = self.rule.hamiltonian(self.rule.theta, dense=True)
        self.U = unitary(self.H, dt)
        self.dt = dt
        self.lane, self.dest = lane_channels(L, D)

    def step(self, rho):
        _, d = self.rule.settings(rho)
        self.rule.d = d
        rho = self.U @ rho @ self.U.conj().T
        return kraus(rho, self.lane, self.dest, d[self.lane] * self.dt)

    def evolve(self, rho, t):
        for _ in range(int(round(t / self.dt))):
            rho = self.step(rho)
        return rho

    def current(self, rho):
        return float(np.sum(self.rule.currents(rho, self.rule.theta)))
