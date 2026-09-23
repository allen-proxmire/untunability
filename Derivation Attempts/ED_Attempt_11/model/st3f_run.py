"""Wrapper for the compiled sampler: builds with st3.Spacetime, runs with st3f.sweep."""
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))
from st3 import Spacetime, random_torus_tris          # noqa: E402
import st3f                                           # noqa: E402


class Fast:
    def __init__(self, L, T, mode="ed", eps=0.1, k0=0.0, epsv=0.0005, seed=0, slice_tris=None):
        self.X = Spacetime(L, T, eps=eps, seed=seed, slice_tris=slice_tris)
        self.X.M.seed(seed)          # FIX: the compiled sampler draws from the engine's stream, which must be seeded too
        X = self.X
        self.W = np.zeros(9)
        if mode == "cdt":
            self.W[0], self.W[6], self.W[7], self.W[8] = 1.0, k0, epsv, X.N3()
        else:
            self.W[3], self.W[4], self.W[5] = eps, X.N0s, X.N22s
        self.cnt = np.zeros(32, dtype=np.int64)
        self.cnt[2] = X.N22()
        self.scratch = np.zeros(256, dtype=np.int64)
        self.T = T

    def sweeps(self, n):
        X = self.X
        for _ in range(n):
            st3f.sweep(X.S, X.time, self.T, self.W, self.cnt, self.scratch, X.N3())
        X.N22_cur = int(self.cnt[2])
        return self.cnt

    def tau(self):
        return self.cnt[2] / self.X.N3()

    def check(self):
        self.X.N22_cur = int(self.cnt[2])
        return self.X.check()
