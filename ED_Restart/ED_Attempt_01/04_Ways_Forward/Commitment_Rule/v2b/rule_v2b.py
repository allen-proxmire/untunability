"""Rule version 2b: version 2 plus flow-set lane phases and draws that carry the mark away (RD47). See Spec.md.

Population density matrix rho over (locus u, channel K), index 3u + K. Spreading: the real rule with, on each bond b,
Right-lane hops times e^{i theta_b} and Left-lane hops times e^{-i theta_b}, theta_b = theta0 tanh(|v_b| / V0).
Draws at committed loci x (every D-th): jump operators sqrt(gamma) |x, INTERNAL><x, K| for K in (RIGHT, LEFT), with
gamma[x, RIGHT] = Gamma (1 - g tanh(v_x / V0)), gamma[x, LEFT] = Gamma (1 + g tanh(v_x / V0)).
  d rho / dt = -i [H(theta), rho] + sum_jumps (J rho J^dagger - {J^dagger J, rho} / 2).
"""
import os
import sys

import numpy as np
import scipy.sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v2"))
sys.path.insert(0, os.path.join(HERE, "..", "v1_budget"))
from rule_budget import INTERNAL, LEFT, RIGHT  # noqa: E402
from rule_v2 import max_winding, mirror_perm, pure, purity, real_rule  # noqa: E402,F401


class RuleB:
    def __init__(self, L, D, Gamma, g, theta0, V0=0.05, phase_mode="flow", m=4.0):
        self.L, self.n = L, 3 * L
        self.Gamma, self.g, self.theta0, self.V0, self.mode = Gamma, g, theta0, V0, phase_mode
        H0 = real_rule(L, None, m)
        rows, cols = np.nonzero(np.abs(H0) > 0)
        self.rows, self.cols, self.vals0 = rows, cols, H0[rows, cols]
        ur, uc, Kr, Kc = rows // 3, cols // 3, rows % 3, cols % 3
        fwd = ((ur - uc) % L == 1) & (Kr == Kc)
        bwd = ((uc - ur) % L == 1) & (Kr == Kc)
        self.bond = np.where(fwd, uc, np.where(bwd, ur, 0))
        sgn = np.zeros(len(rows))
        sgn[fwd & (Kr == RIGHT)] = 1.0
        sgn[fwd & (Kr == LEFT)] = -1.0
        sgn[bwd & (Kr == RIGHT)] = -1.0
        sgn[bwd & (Kr == LEFT)] = 1.0
        self.sgn = sgn
        ub = np.arange(L)
        self.aR, self.bR = 3 * ub + RIGHT, 3 * ((ub + 1) % L) + RIGHT
        self.aL, self.bL = 3 * ub + LEFT, 3 * ((ub + 1) % L) + LEFT
        self.hR, self.hL = H0[self.bR, self.aR], H0[self.bL, self.aL]
        self.committed = np.arange(0, L, D)
        x = self.committed
        self.src = np.concatenate([3 * x + RIGHT, 3 * x + LEFT])
        self.dst = np.concatenate([3 * x + INTERNAL, 3 * x + INTERNAL])
        self.theta = np.zeros(L)
        self.d = np.zeros(self.n)

    def currents(self, rho, theta):
        """j_b: amount per unit time from locus b to b + 1 = sum of 2 Im(H_ba rho_ab) over the two lanes."""
        zR = self.hR * np.exp(1j * theta) * rho[self.aR, self.bR]
        zL = self.hL * np.exp(-1j * theta) * rho[self.aL, self.bL]
        return 2 * np.imag(zR + zL)

    def amounts(self, rho):
        return np.real(np.diag(rho)).reshape(self.L, 3).sum(axis=1)

    def settings(self, rho):
        L, x = self.L, self.committed
        j = self.currents(rho, self.theta)
        n = self.amounts(rho)
        nb = 0.5 * (n + np.roll(n, -1))
        vb = np.divide(j, nb, out=np.zeros(L), where=nb > 0)
        if self.mode == "flow":
            theta = self.theta0 * np.tanh(np.abs(vb) / self.V0)
        else:
            theta = np.full(L, float(self.theta0))
        jx = 0.5 * (j[(x - 1) % L] + j[x])
        vx = np.divide(jx, n[x], out=np.zeros(len(x)), where=n[x] > 0)
        s = np.tanh(vx / self.V0)
        d = np.zeros(self.n)
        d[3 * x + RIGHT] = self.Gamma * (1 - self.g * s)
        d[3 * x + LEFT] = self.Gamma * (1 + self.g * s)
        return theta, d

    def hamiltonian(self, theta, dense=False):
        vals = self.vals0 * np.exp(1j * self.sgn * theta[self.bond])
        if dense:
            H = np.zeros((self.n, self.n), dtype=complex)
            H[self.rows, self.cols] = vals
            return H
        return sp.csr_matrix((vals, (self.rows, self.cols)), shape=(self.n, self.n))

    def rhs(self, rho, Hs, d):
        Hr = Hs @ rho
        out = -1j * (Hr - Hr.conj().T) - 0.5 * (d[:, None] + d[None, :]) * rho
        gain = np.zeros(self.n)
        np.add.at(gain, self.dst, d[self.src] * np.real(np.diag(rho))[self.src])
        out[np.diag_indices(self.n)] += gain
        return out

    def step(self, rho, dt):
        theta, d = self.settings(rho)
        self.theta, self.d = theta, d
        Hs = self.hamiltonian(theta)
        k1 = self.rhs(rho, Hs, d); k2 = self.rhs(rho + 0.5 * dt * k1, Hs, d)
        k3 = self.rhs(rho + 0.5 * dt * k2, Hs, d); k4 = self.rhs(rho + dt * k3, Hs, d)
        return rho + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def evolve(self, rho, t, dt=0.01, every=100):
        steps = int(round(t / dt))
        pur = [purity(rho)]
        for i in range(1, steps + 1):
            rho = self.step(rho, dt)
            if i % every == 0:
                pur.append(purity(rho))
        return rho, np.array(pur)

    def total_current(self, rho):
        return float(np.sum(self.currents(rho, self.theta)))

    def final_winding(self, rng, nphi=300, npts=15):
        return max_winding(self.hamiltonian(self.theta, dense=True), self.d, self.L, rng, nphi=nphi, npts=npts)
