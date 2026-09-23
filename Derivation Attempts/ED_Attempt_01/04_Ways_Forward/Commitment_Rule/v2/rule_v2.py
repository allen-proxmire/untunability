"""Rule version 2: spreading and draws on one ring, with feedback at commitment (RD46). See Spec.md.

A population of identical patterns is described by its one-pattern density matrix rho over (locus u, channel K),
index 3u + K as in v1_budget. Between draws it spreads with the real rule's generator (v1_budget: three lanes, Grover
mixing, budget slowing RD36). Committed loci (every D-th locus) draw: a part in channel K at committed locus x is drawn
at rate gamma[x, K] and collapses onto that single channel (P11, RD28). Averaged over draws:
  d rho / dt = -i [H, rho] + sum_a gamma_a (P_a rho P_a - {P_a, rho} / 2),  P_a = |a><a|,
so coherence between channels a and b decays at rate (gamma_a + gamma_b) / 2.
Feedback at commitment: gamma[x, RIGHT] = Gamma (1 - g tanh(v_x / V0)), gamma[x, LEFT] = Gamma (1 + g tanh(v_x / V0)),
gamma[x, INTERNAL] = Gamma, with v_x the population's local velocity at that moment (present state only, D1).
"""
import os
import sys

import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v1_budget"))
from rule_budget import INTERNAL, LEFT, RIGHT, generator, slowed_rd36  # noqa: E402


def real_rule(L, U=None, m=4.0, theta=0.0):
    """The real rule's spreading generator (RD36 slowing). theta != 0 multiplies Right-lane hops by e^{i theta}
    and Left-lane hops by e^{-i theta} (used only for the contrast test V2-P6)."""
    U = np.zeros(L) if U is None else np.asarray(U, dtype=float)
    H = slowed_rd36(generator(L), U, m)
    if theta:
        for u in range(L):
            v = (u + 1) % L
            for K, sgn in ((RIGHT, 1), (LEFT, -1)):
                a, b = 3 * u + K, 3 * v + K
                H[b, a] *= np.exp(1j * sgn * theta)
                H[a, b] *= np.exp(-1j * sgn * theta)
    return H


class Rule:
    def __init__(self, L, D, Gamma, g, V0=0.05, U=None, m=4.0):
        self.L, self.n, self.Gamma, self.g, self.V0 = L, 3 * L, Gamma, g, V0
        self.H = real_rule(L, U, m)
        self.Hs = sp.csr_matrix(self.H)
        u = np.arange(L)
        self.A = 3 * u[:, None] + np.arange(3)[None, :]
        self.B = 3 * ((u + 1) % L)[:, None] + np.arange(3)[None, :]
        self.Hba = self.H[self.B[:, :, None], self.A[:, None, :]]
        self.committed = np.arange(0, L, D)

    def currents(self, rho):
        """j_u: amount per unit time crossing from locus u to u + 1 = sum over a at u, b at u+1 of 2 Im(H_ba rho_ab)."""
        rab = rho[self.A[:, :, None], self.B[:, None, :]]
        return 2 * np.sum(np.imag(self.Hba * np.transpose(rab, (0, 2, 1))), axis=(1, 2))

    def amounts(self, rho):
        return np.real(np.diag(rho)).reshape(self.L, 3).sum(axis=1)

    def rates(self, rho):
        L, x = self.L, self.committed
        j = self.currents(rho)
        n = self.amounts(rho)
        jx = 0.5 * (j[(x - 1) % L] + j[x])
        vx = np.divide(jx, n[x], out=np.zeros(len(x)), where=n[x] > 0)
        s = np.tanh(vx / self.V0)
        gam = np.zeros(self.n)
        gam[3 * x + INTERNAL] = self.Gamma
        gam[3 * x + RIGHT] = self.Gamma * (1 - self.g * s)
        gam[3 * x + LEFT] = self.Gamma * (1 + self.g * s)
        return gam

    def rhs(self, rho, G):
        Hr = self.Hs @ rho
        return -1j * (Hr - Hr.conj().T) - G * rho

    def step(self, rho, dt):
        gam = self.rates(rho)
        G = 0.5 * (gam[:, None] + gam[None, :])
        np.fill_diagonal(G, 0.0)
        k1 = self.rhs(rho, G); k2 = self.rhs(rho + 0.5 * dt * k1, G)
        k3 = self.rhs(rho + 0.5 * dt * k2, G); k4 = self.rhs(rho + dt * k3, G)
        return rho + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def evolve(self, rho, t, dt=0.01, every=100):
        """Returns the final rho and the purity recorded every `every` steps (including the start)."""
        steps = int(round(t / dt))
        pur = [purity(rho)]
        for i in range(1, steps + 1):
            rho = self.step(rho, dt)
            if i % every == 0:
                pur.append(purity(rho))
        return rho, np.array(pur)


def purity(rho):
    return float(np.sum(np.abs(rho) ** 2))


def pure(psi):
    psi = psi / np.linalg.norm(psi)
    return np.outer(psi, psi.conj())


def mirror_perm(L):
    """p[new index] = old index for locus u -> -u, Left <-> Right."""
    p = np.zeros(3 * L, dtype=int)
    swap = {INTERNAL: INTERNAL, LEFT: RIGHT, RIGHT: LEFT}
    for u in range(L):
        for K in range(3):
            p[3 * ((-u) % L) + swap[K]] = 3 * u + K
    return p


def twisted(H, L, phi):
    """Multiply hops from locus L-1 to locus 0 by e^{i phi} (and the reverse by e^{-i phi})."""
    Ht = H.copy()
    a0, a1 = slice(0, 3), slice(3 * (L - 1), 3 * L)
    Ht[a0, a1] *= np.exp(1j * phi)
    Ht[a1, a0] *= np.exp(-1j * phi)
    return Ht


def max_winding(H, gam, L, rng, nphi=600, npts=30):
    """Largest |winding| of det(H_eff(phi) - E0) over the centroid and npts random E0 in the spectrum's bounding box."""
    Heff = H - 0.5j * np.diag(gam)
    phis = np.linspace(0, 2 * np.pi, nphi + 1)
    eigs = np.array([np.linalg.eigvals(twisted(Heff, L, ph)) for ph in phis])
    flat = eigs.ravel()
    lo_r, hi_r = flat.real.min(), flat.real.max()
    lo_i, hi_i = flat.imag.min(), flat.imag.max()
    pts = [flat.mean()] + list(rng.uniform(lo_r, hi_r, npts) + 1j * rng.uniform(lo_i, hi_i, npts))
    best = 0
    for E0 in pts:
        if np.min(np.abs(eigs - E0)) < 1e-3:
            continue
        total = np.sum(np.angle(eigs - E0), axis=1)
        steps = np.angle(np.exp(1j * np.diff(total)))
        best = max(best, abs(int(round(steps.sum() / (2 * np.pi)))))
    return best
