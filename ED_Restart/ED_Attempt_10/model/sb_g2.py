"""Gate G2 (note 14, C24): 3D moves in the history sampler. Every slice valid with exact event and link counts after every
accepted step (structure check every CHECK steps, counts every step), and replaying every tick's recorded changes on its
slice reproduces the next slice exactly (every REPLAY steps). Pass: no failure at all. Also measured: acceptance by
bundle type and cost per step, for the run-time estimate."""
import json
import os
import sys
import time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sb_core import History  # noqa: E402
from sb_3d import Ops3D  # noqa: E402
import sb_build as b  # noqa: E402


def run(n=6, T=4, steps=20000, CHECK=500, REPLAY=2000, start="flat", seed=0):
    F = b.flat_reference(n)
    base = F if start == "flat" else b.crowded(F)
    ops = Ops3D()
    slices = [ops.copy(base) for _ in range(T)]
    V0, E0 = base.V, base.E
    cap = int(round(0.1 * V0))
    H = History(slices, ops, cap, seed)
    fails = []
    t0 = time.perf_counter()
    for i in range(1, steps + 1):
        H.step()
        for t, S in enumerate(H.S):
            if S.V != V0 or S.E != E0:
                fails.append((i, t, "counts", S.V, S.E))
        if i % CHECK == 0:
            for t, S in enumerate(H.S):
                if S.check():
                    fails.append((i, t, "structure"))
        if i % REPLAY == 0:
            ok, t, why = H.replay_ok()
            if not ok:
                fails.append((i, t, "replay", str(why)))
        if fails:
            break
    sec = time.perf_counter() - t0
    return dict(n=n, T=T, start=start, V=V0, E=E0, cap=cap, steps=i, fails=fails[:5], accepted=H.acc,
                acceptance=H.acc / H.tried, tick_sizes=[len(x) for x in H.tau], why=H.why, site_rejects=ops.stats,
                ms_per_step=1000 * sec / i)


if __name__ == "__main__":
    out = [run(6, 4, 20000, start="flat"), run(6, 4, 20000, start="crowded", seed=1)]
    json.dump(out, open(os.path.join(HERE, "sb_g2.json"), "w"), indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))
