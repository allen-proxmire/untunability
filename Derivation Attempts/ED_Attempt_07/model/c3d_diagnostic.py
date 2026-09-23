"""C3d follow-up diagnostic (NOT pre-registered; D34).

C3d's runs all ended pinned at the ceiling of 30 links per event, with splits refused in bulk, the
event balance broken and slices shrunk (C79). This repeats two settings at one size with a shorter
run and three ceilings, to see whether the ceiling alone caused it.

Settings: S0 (0,0,0) and S4 (1,1,1); V = 8,000; T = 100; seed 0; ceilings 30 (as run), 60, none.
C3d run 1's verdict stands; nothing here is pre-registered.
"""
import json, time
import numpy as np
from c3c import Slice3, SIGMA
from c3d import tick, slice_readings, FLAT_LINKS_PER_EVENT

T = 100
rows = []
for cap_name, cap in (("30 (as run)", 30), ("60", 60), ("none", 10 ** 9)):
    for name, setting in (("S0", (0, 0, 0)), ("S4", (1, 1, 1))):
        M = Slice3(20)
        V0 = len(M.vt)
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        pool = BL - len(M.val)
        rng = np.random.default_rng(0)
        b = {v: 1.0 for v in M.vt}
        omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
        phi = {v: 0.0 for v in M.vt}
        t0 = time.perf_counter()
        ref_cap = ref_bud = split_ref = 0
        for t in range(T):
            r, pool = tick(M, b, omega, phi, rng, *setting, pool, cap=cap)
            ref_cap += r["refused_cap"]; ref_bud += r["refused_budget"]; split_ref += r["split_refused"]
            if not (V0 / 10 <= r["size"] <= 10 * V0):
                break
        rd = slice_readings(M, 0, with_walk=True)
        rows.append(dict(cap=cap_name, setting=name, events=len(M.vt) / V0, links_per_event=rd["links_per_event"],
                         tets_per_event=rd["tets_per_event"], mean_degree=rd["mean_degree"], max_degree=rd["max_degree"],
                         diameter=rd["diameter"], d_H=rd["d_H"], d_s=rd["d_s"], small_world=rd["small_world"],
                         neck=rd["neck_strain"], ref_cap=ref_cap / T, ref_bud=ref_bud / T, split_ref=split_ref / T,
                         secs=time.perf_counter() - t0))
        x = rows[-1]
        print(f"ceiling {cap_name:11s} {name}: events {x['events']:.3f}x | links/event {x['links_per_event']:.3f} (flat 6.699) | "
              f"tets/event {x['tets_per_event']:.2f} | mean degree {x['mean_degree']:.2f}, largest {x['max_degree']} | "
              f"diameter {x['diameter']:.0f} (flat start 15) | d_H {x['d_H']} | d_s {x['d_s']} | growth flag {x['small_world']} | "
              f"neck strain {x['neck']:.2f} | refused cap/budget/splits per tick {x['ref_cap']:.0f}/{x['ref_bud']:.0f}/{x['split_ref']:.1f} | "
              f"{x['secs']/60:.1f} min", flush=True)
json.dump(rows, open("c3d_diagnostic.json", "w"), default=str)
open("c3d_diagnostic.txt", "w", encoding="utf-8").write("\n".join(
    f"ceiling {x['cap']} {x['setting']}: events {x['events']:.3f}x, links/event {x['links_per_event']:.3f}, tets/event {x['tets_per_event']:.2f}, "
    f"mean degree {x['mean_degree']:.2f}, largest {x['max_degree']}, diameter {x['diameter']:.0f}, d_H {x['d_H']}, d_s {x['d_s']}, "
    f"growth flag {x['small_world']}, neck strain {x['neck']:.2f}, refused cap/budget/splits per tick "
    f"{x['ref_cap']:.0f}/{x['ref_bud']:.0f}/{x['split_ref']:.1f}" for x in rows) + "\n")
