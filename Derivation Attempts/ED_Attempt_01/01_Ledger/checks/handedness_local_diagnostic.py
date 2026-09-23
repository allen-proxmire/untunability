"""Diagnostic after C263 run 1 (not pre-registered): how do domains form and merge over time, and does a seed's
takeover depend on the ring being small? Same rule as handedness_local_toy.py (g 0.5, V0 0.05, NB 8, RK4 dt 0.02).
  S  L = 512, 3 noise starts (1e-3): domains at t = 2.5, 5, 10, 20, 50.
  N  L = 4096, 1 noise start (1e-3): domains and share of hand +1 at t = 5 ... 800.
  Q  L = 4096, noise 1e-3 plus the C263 seed at the centre: share of the seed's hand (+1) and domains at t = 5 ... 800."""
import math

import numpy as np

G_FB, V0, NB, DT = 0.5, 0.05, 8, 0.02


def hops(psi):
    a = np.roll(psi, -1)
    den = np.abs(psi) ** 2 + np.abs(a) ** 2
    v = np.divide(2 * np.imag(np.conj(psi) * a), den, out=np.zeros(len(psi)), where=den > 0)
    for _ in range(NB):
        v = 0.25 * np.roll(v, 1) + 0.5 * v + 0.25 * np.roll(v, -1)
    d = G_FB * np.tanh(v / V0)
    return 1 - d, 1 + d


def step(psi):
    tf, tb = hops(psi)
    tfp = np.roll(tf, 1)

    def rhs(p):
        return -1j * (tfp * np.roll(p, 1) + tb * np.roll(p, -1))

    k1 = rhs(psi); k2 = rhs(psi + 0.5 * DT * k1); k3 = rhs(psi + 0.5 * DT * k2); k4 = rhs(psi + DT * k3)
    psi = psi + DT * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return psi / np.linalg.norm(psi)


def hands(psi):
    tf, tb = hops(psi)
    d = tb - tf
    return np.where(np.abs(d) > 0.1, np.sign(d), 0).astype(int)


def domains(h):
    nz = h[h != 0]
    if len(nz) == 0:
        return 0
    return max(int(np.sum(nz != np.roll(nz, 1))), 1)


def track(psi, times):
    psi = psi / np.linalg.norm(psi)
    marks = {int(round(t / DT)): t for t in times}
    out = []
    for i in range(1, max(marks) + 1):
        psi = step(psi)
        if i in marks:
            h = hands(psi)
            out.append((marks[i], domains(h), float(np.mean(h == 1)), float(np.mean(h == 0))))
    return out


def noise(rng, n, eps):
    return eps * (rng.standard_normal(n) + 1j * rng.standard_normal(n)) / math.sqrt(2)


rng = np.random.default_rng(4242)
for r in range(3):
    res = track(1 + noise(rng, 512, 1e-3), (2.5, 5, 10, 20, 50))
    print("S L 512 run %d: " % r + "; ".join("t %g: %d domains (unhanded %.2f)" % (t, d, u) for t, d, _, u in res), flush=True)

times = (5, 10, 20, 50, 100, 200, 400, 800)
res = track(1 + noise(rng, 4096, 1e-3), times)
print("N L 4096 noise: " + "; ".join("t %g: %d domains, +1 share %.2f" % (t, d, p) for t, d, p, _ in res), flush=True)

X = np.arange(4096)
seed = 0.5 * np.exp(-((X - 2048) / 32.0) ** 2) * np.exp(1j * 0.3 * X)
res = track(1 + seed + noise(rng, 4096, 1e-3), times)
print("Q L 4096 seed + noise: " + "; ".join("t %g: seed hand %.3f, %d domains" % (t, p, d) for t, d, p, _ in res), flush=True)
