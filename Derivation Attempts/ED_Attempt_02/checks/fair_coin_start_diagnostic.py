"""Diagnostic (not pre-registered; follows C55): why did family B at phi not match family A at -phi (Q4)?

Suspected reason: conjugating the whole dynamics maps coin B(phi) to A(-phi) only together with the momentum gauge k = pi, so the
start rho0 of a B run corresponds to the start G rho0* G^dagger of an A run, with G = (-1)^x on every channel. The near-uniform
starts of the A runs are therefore not the images of the near-uniform starts of the B runs: they correspond to staggered starts.

  E1 the mapping is exact: after 50 steps, G rho_B* G^dagger equals rho_A (B210 from start 0; A150 from the mapped start);
  E2 A150 (which died from all 3 near-uniform starts in C55) from the mapped starts 0 and 1, 4,000 steps, g +0.9: final v and
     the largest change per step over the last 50 steps.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixed_point_check as fp  # noqa: E402
from discrete_hand_test import D, step  # noqa: E402
from fair_coin_family_check import V0, coin  # noqa: E402
from lasting_states_check import L, starts  # noqa: E402
from rule_v4 import lane_channels  # noqa: E402


def main():
    G = np.repeat((-1.0) ** np.arange(L), 3)
    lane, dest = lane_channels(L, D)
    CA, CB = coin(("A", 150, 0.0)), coin(("B", 210, 0.0))
    WA, CfA = fp.walk_matrix(L, CA), fp.coin_full(L, CA)
    WB, CfB = fp.walk_matrix(L, CB), fp.coin_full(L, CB)
    st = starts()
    rb = st[0].copy()
    ra = G[:, None] * rb.conj() * G[None, :]
    for _ in range(50):
        rb, _ = step(rb, WB, CfB, lane, dest, L, 0.9, V0)
        ra, _ = step(ra, WA, CfA, lane, dest, L, 0.9, V0)
    e1 = float(np.max(np.abs(G[:, None] * rb.conj() * G[None, :] - ra)))
    print("E1 after 50 steps, |G rho_B* G - rho_A|: %.1e" % e1, flush=True)
    for i in (0, 1):
        rho = G[:, None] * st[i].conj() * G[None, :]
        change = 0.0
        for t in range(4000):
            new, _ = step(rho, WA, CfA, lane, dest, L, 0.9, V0)
            if t >= 3950:
                change = max(change, float(np.max(np.abs(new - rho))))
            rho = new
        print("E2 A150 from mapped start %d: v %+.5e, largest change per step over last 50 steps %.1e"
              % (i, fp.displacement(rho, CfA, L), change), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
