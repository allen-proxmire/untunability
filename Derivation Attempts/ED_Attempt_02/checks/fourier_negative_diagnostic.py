"""Diagnostic (not pre-registered; follows C45): does the unsteady Fourier g -0.9 state carry a net flow on average?

Same rule and settings as lasting_states_check.py. For starts 0, 2 and 4 (two with alternating local displacement, one
without, per C45): 4,000 steps, then 4,000 more watched. Reports the mean and spread of v over the watched steps, the
strongest period in v (from its Fourier spectrum), and the mean of |v|.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
from discrete_hand_test import D, step  # noqa: E402
from lasting_states_check import CHI, L, starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402

STEPS, WATCH, G = 4000, 4000, -0.9


def main():
    W, Cf = fp.walk_matrix(L, fp.FOURIER), fp.coin_full(L, fp.FOURIER)
    lane, dest = lane_channels(L, D)
    V0 = abs(0.9 * CHI["Fourier"]) / 3
    st = starts()
    for i in (0, 2, 4):
        rho = st[i].copy()
        for _ in range(STEPS):
            rho, _ = step(rho, W, Cf, lane, dest, L, G, V0)
        vs = []
        for _ in range(WATCH):
            rho, _ = step(rho, W, Cf, lane, dest, L, G, V0)
            vs.append(fp.displacement(rho, Cf, L))
        vs = np.array(vs)
        spec = np.abs(np.fft.rfft(vs - vs.mean()))
        k = int(np.argmax(spec[1:]) + 1)
        top = np.argsort(spec[1:])[::-1][:3] + 1
        print("start %d: mean v %+.3e, standard deviation %.3e, mean |v| %.3e, min %+.3e, max %+.3e; strongest period %.2f steps "
              "(next %.2f, %.2f); strongest peak holds %.0f%% of spectral weight"
              % (i, vs.mean(), vs.std(), np.abs(vs).mean(), vs.min(), vs.max(), WATCH / k, WATCH / top[1], WATCH / top[2],
                 100 * spec[k] ** 2 / np.sum(spec[1:] ** 2)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
