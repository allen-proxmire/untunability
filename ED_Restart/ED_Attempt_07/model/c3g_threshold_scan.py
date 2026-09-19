"""C3g threshold scan (NOT pre-registered; D44). Does a tighter sync condition push further toward flat?

Setting B (commitment, curvature, sync as a condition) at V = 13,824, seed 0, T = 150, with the sync
threshold at 6, 3 and 1.5 in the calibration's normalized units, against C3g's run at about 10 (which
gave slice diameter 15.0 and spacetime d_H 6.33; the flat slice reads diameter 18, and flat 3+1 space
should read about 4). Readings: slice readings at T and the grown spacetime over the last 20 ticks.
C3g run 1's verdict stands; nothing here is pre-registered.
"""
import json, time
import numpy as np
from c3c import Slice3, SIGMA
from c3d import slice_readings
from c3e import CEILING
from c3f import tick, slice_edges, spacetime_readings, FLAT_LINKS_PER_EVENT

n, T, KEEP, seed = 24, 150, 20, 0
rows = []
for s_max in (6.0, 3.0, 1.5):
    M = Slice3(n); rng = np.random.default_rng(seed)
    V0 = len(M.vt)
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - len(M.val)
    b = {v: 1.0 for v in M.vt}
    omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
    phi = {v: 0.0 for v in M.vt}
    snaps, ref_sync, forced, split_ref = [], 0, 0, 0
    t0 = time.perf_counter()
    for t in range(1, T + 1):
        rec = {} if t > T - KEEP else None
        edges = slice_edges(M) if rec is not None else None
        r, pool = tick(M, b, omega, phi, rng, 1.0, 1.0, pool, s_max=s_max, cap=CEILING, record=rec)
        if rec is not None:
            snaps.append((edges, rec))
        ref_sync += r["refused_sync"]; forced += r["forced"]; split_ref += r["split_refused"]
        if not (V0 / 10 <= r["size"] <= 10 * V0):
            break
    sl = slice_readings(M, 99, with_walk=True)
    snaps.append((slice_edges(M), {"children": {}, "absorbed": {}}))
    st = spacetime_readings(snaps, 99)
    rows.append(dict(s_max=s_max, events=len(M.vt) / V0, diameter=sl["diameter"], d_H=sl["d_H"], d_s=sl["d_s"],
                     links_per_event=sl["links_per_event"], strain=sl["neck_strain"], st_d_H=st["d_H"],
                     st_events=st["events"], sync_per_tick=ref_sync / T, forced_per_tick=forced / T,
                     split_refused_per_tick=split_ref / T, minutes=(time.perf_counter() - t0) / 60))
    x = rows[-1]
    print(f"threshold {s_max:>4}: events {x['events']:.3f}x | slice diameter {x['diameter']:.1f} (flat 18) | "
          f"slice d_H {x['d_H']} , d_s {x['d_s']} | links/event {x['links_per_event']:.3f} | strain {x['strain']:.1f} | "
          f"SPACETIME d_H {x['st_d_H']:.3f} over {x['st_events']} events | sync refusals/tick {x['sync_per_tick']:.0f} | "
          f"forced/tick {x['forced_per_tick']:.0f} | splits abandoned/tick {x['split_refused_per_tick']:.1f} | {x['minutes']:.0f} min", flush=True)
json.dump(rows, open("c3g_threshold_scan.json", "w"), default=str)
open("c3g_threshold_scan.txt", "w", encoding="utf-8").write("\n".join(
    f"threshold {x['s_max']}: events {x['events']:.3f}x, diameter {x['diameter']:.1f}, slice d_H {x['d_H']}, d_s {x['d_s']}, "
    f"links/event {x['links_per_event']:.3f}, strain {x['strain']:.1f}, spacetime d_H {x['st_d_H']:.3f}, "
    f"sync refusals/tick {x['sync_per_tick']:.0f}, forced/tick {x['forced_per_tick']:.0f}, splits abandoned/tick {x['split_refused_per_tick']:.1f}"
    for x in rows) + "\n")
