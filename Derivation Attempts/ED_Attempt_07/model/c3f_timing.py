"""C3f timing trial (note 27 running order; D41). Timing and harness only: no shape values printed.

Per size n = 20, 24 and settings A (1,1,no sync), B (1,1,sync condition), D (0,0): 10 ticks with the
structure check, both budgets, the ceiling and flip neutrality; refusals by cause, so we can see whether
the sync condition ever binds; then the grown spacetime from those 10 ticks, timed, with only whether the
ball reading is defined reported. s_max comes from the flat start's largest link strain, times 3.
"""
import time
import numpy as np
from c3c import Slice3, SIGMA
from c3d import slice_readings
from c3e import CEILING
from c3f import tick, slice_edges, spacetime_readings, FLAT_LINKS_PER_EVENT

lines, per = [], {}
for n in (20, 24):
    M0 = Slice3(n)
    fc = slice_readings(M0, 0, with_walk=False)
    s_max = 3 * fc["neck_strain"]
    V0 = n ** 3
    lines.append(f"n={n} (V={V0}): flat calibration largest link strain {fc['neck_strain']:.3f} -> sync threshold {s_max:.3f}")
    print(lines[-1], flush=True)
    for label, (alpha, lam, use_sync) in (("A", (1, 1, False)), ("B", (1, 1, True)), ("D", (0, 0, False))):
        M = Slice3(n); rng = np.random.default_rng(0)
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        pool = BL - len(M.val)
        b = {v: 1.0 for v in M.vt}
        omega = {v: 1 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
        phi = {v: 0.0 for v in M.vt}
        snaps, ref = [], dict(budget=0, cap=0, sync=0, split=0)
        t0 = time.perf_counter()
        for _ in range(10):
            rec = {}
            e = slice_edges(M)
            r, pool = tick(M, b, omega, phi, rng, alpha, lam, pool, s_max=(s_max if use_sync else None), cap=CEILING, record=rec)
            snaps.append((e, rec))
            assert not M.check(), "structure"
            assert len(M.val) + pool == BL, "link budget"
            assert max(len(x) for x in M.nbrs.values()) <= CEILING, "ceiling"
            assert r["flips_link_neutral"], "flip neutrality"
            ref["budget"] += r["refused_budget"]; ref["cap"] += r["refused_cap"]
            ref["sync"] += r["refused_sync"]; ref["split"] += r["split_refused"]
        t_tick = (time.perf_counter() - t0) / 10
        snaps.append((slice_edges(M), {"children": {}, "absorbed": {}}))
        t0 = time.perf_counter()
        st = spacetime_readings(snaps, 0)
        t_st = time.perf_counter() - t0
        per[(n, label)] = dict(tick=t_tick, st=t_st, st_events=st["events"])
        lines.append(f"  {label}: tick+checks {t_tick:.1f} s; refusals per tick budget/cap/sync/splits "
                     f"{ref['budget']/10:.0f}/{ref['cap']/10:.0f}/{ref['sync']/10:.0f}/{ref['split']/10:.1f}; "
                     f"spacetime over 10 ticks {st['events']} events, reading {t_st:.1f} s, d_H defined "
                     f"{st['d_H'] is not None and np.isfinite(st['d_H'])} (radii {st['r_lo']}-{st['r_max']})")
        print(lines[-1], flush=True)
for T in (150, 100):
    tot = 0.0
    for n in (20, 24):
        ticks_kept = 30 if n == 20 else 20
        for label in ("A", "B", "D"):
            p = per[(n, label)]
            runs = 2 if label != "B" else 2
            st_scaled = p["st"] * (ticks_kept / 10)
            tot += runs * (T * p["tick"] + st_scaled + 3 * 4.0)
        p = per[(n, "B")]
        tot += 2 * (T * p["tick"] + p["st"] * (ticks_kept / 10))   # setting C, sync alone, same cost class
    lines.append(f"T={T}: {tot/3600:.1f} h single process, {tot/3600/3:.1f} h on 3 workers")
print("\n".join(lines[-2:]))
open("c3f_timing.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
