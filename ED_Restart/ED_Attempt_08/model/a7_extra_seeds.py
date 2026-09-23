"""Six more seeds of attempt 7's own C3g model, to give tier 3 eight seeds on both sides (D4).

Tier 3 (C11) found the port refusing about 19 per cent fewer moves on sync than attempt 7 at n = 24,
with every other quantity inside. Attempt 7 has only two seeds there, and the refusal count is a tail
statistic that varies by a factor of 1.8 across seeds (C12), so two values cannot define its range.
This runs attempt 7's code unchanged - imported, never edited - at n = 24, setting B, seeds 2 to 7,
with the same knobs, the same threshold read from attempt 7's own calibration file, the same tick
count and the same readings. Results are written here, in attempt 8, not into the closed record.

Expected results, written down before this run:
  X1  all six seeds survive with structure, budgets, ceiling and flip neutrality clean, as seeds 0
      and 1 did.
  X2  the eight-seed range of attempt 7's sync refusals per tick either does or does not contain the
      port's range 1,033-1,289. Both outcomes are recorded; neither is the one being hoped for.
Exit rule: if the two eight-seed ranges overlap, tier 3's one failure was a two-seed artefact and the
port passes tier 3, recorded as such. If they stay apart, the port is a different model in its sync
behaviour: said plainly, the difference named and carried into every later claim, and not used to
reinterpret attempt 7.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
A7 = os.path.join(HERE, "..", "..", "ED_Attempt_07", "model")
sys.path.insert(0, A7)

N = 24
T = 150
KEEP = 20
SEEDS = (2, 3, 4, 5, 6, 7)
ALPHA, LAM = 1.0, 1.0
CHECKS = (T // 2, (3 * T) // 4, T)
TETS_PER_EVENT_CAP = 20
OUT = "a7_extra_runs"


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def threshold():
    """1.5 x the flat calibration's largest link strain, read from attempt 7's own calibration."""
    cal = json.load(open(os.path.join(A7, "c3g_runs", "cal_FC_n24.json"), encoding="utf-8"))
    return 1.5 * float(cal["readings"]["neck_strain"])


def do_job(job):
    s, s_max = job
    path = os.path.join(OUT, "grow_B_n24_s%d.json" % s)
    if os.path.exists(path):
        return path, 0.0
    from c3c import Slice3, SIGMA
    from c3d import slice_readings, FLAT_LINKS_PER_EVENT
    from c3e import CEILING
    from c3f import tick, slice_edges, spacetime_readings
    t0 = time.perf_counter()
    M = Slice3(N)
    rng = np.random.default_rng(s)
    V0 = len(M.vt)
    b = {v: 1.0 for v in M.vt}
    omega = {v: 1.0 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))}
    phi = {v: 0.0 for v in M.vt}
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - len(M.val)
    keep_from = T - KEEP
    sizes, forced, flips, ref = [], [], [], []
    flips_ok = budget_ok = link_ok = cap_ok = True
    status = "survived"
    first_fail = None
    snaps = []
    checkpoints = {}
    for t in range(1, T + 1):
        if len(M.tets) / max(len(M.vt), 1) > TETS_PER_EVENT_CAP:
            status = "densified"
            break
        rec = {} if t > keep_from else None
        edges = slice_edges(M) if rec is not None else None
        r, pool = tick(M, b, omega, phi, rng, ALPHA, LAM, pool, s_max=s_max, cap=CEILING, record=rec)
        if rec is not None:
            snaps.append((edges, rec))
        sizes.append(r["size"])
        forced.append(r["forced"])
        flips.append(r["flips_accepted"])
        ref.append((r["refused_budget"], r["refused_cap"], r["refused_sync"], r["split_refused"],
                    r["merges"], r["splits"]))
        if not r["flips_link_neutral"]:
            flips_ok = False
        notes = M.check()
        if notes:
            first_fail = [t, notes[:3]]
            status = "structure failure"
            break
        if abs(sum(b.values()) - V0) > 1e-9 * V0:
            budget_ok = False
        if len(M.val) + pool != BL:
            link_ok = False
        if max(len(x) for x in M.nbrs.values()) > CEILING:
            cap_ok = False
        if not (V0 / 10 <= r["size"] <= 10 * V0):
            status = "died" if r["size"] < V0 / 10 else "ran away"
            break
        if t in CHECKS:
            checkpoints[str(t)] = slice_readings(M, 10 * s + 1, with_walk=True)
    late = sizes[T // 2 - 1:] if len(sizes) >= T else []
    ra = np.array(ref) if ref else np.zeros((1, 6))
    res = dict(job="grow", setting="B", alpha=ALPHA, lam=LAM, sync=True, s_max=s_max, n=N, V0=V0,
               BL=BL, seed=s, status=status, ticks_done=len(sizes), first_structure_fail=first_fail,
               budget_ok=budget_ok, link_budget_ok=link_ok, cap_ok=cap_ok, flips_ok=flips_ok,
               mean_size_late=float(np.mean(late)) if late else None,
               forced_per_tick=float(np.mean(forced)) if forced else None,
               flips_accepted_per_tick=float(np.mean(flips)) if flips else None,
               refused_budget_per_tick=float(ra[:, 0].mean()), refused_cap_per_tick=float(ra[:, 1].mean()),
               refused_sync_per_tick=float(ra[:, 2].mean()), split_refused_per_tick=float(ra[:, 3].mean()),
               merges_per_tick=float(ra[:, 4].mean()), splits_per_tick=float(ra[:, 5].mean()),
               events=len(M.vt), tets=len(M.tets), links=len(M.val),
               links_per_event=len(M.val) / max(len(M.vt), 1),
               tets_per_event=len(M.tets) / max(len(M.vt), 1),
               mean_degree=2 * len(M.val) / max(len(M.vt), 1),
               max_degree=max((len(x) for x in M.nbrs.values()), default=0),
               checkpoints=checkpoints)
    if status == "survived" and snaps:
        snaps.append((slice_edges(M), {"children": {}, "absorbed": {}}))
        sr = spacetime_readings(snaps, 4000 + s)
        res["spacetime"] = {k: (float(sr[k]) if isinstance(sr.get(k), (int, float, np.floating)) and sr.get(k) is not None else sr.get(k))
                            for k in ("d_H", "r_lo", "r_max", "small_world", "events", "links")}
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def main(workers):
    os.makedirs(OUT, exist_ok=True)
    s_max = threshold()
    print("attempt 7 code, n=%d, setting B, seeds %s, threshold %.3f" % (N, SEEDS, s_max), flush=True)
    jobs = [(s, s_max) for s in SEEDS]
    t0 = time.perf_counter()
    with Pool(workers) as pool:
        for i, (path, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print("[%d/%d] %s %.0f s (elapsed %.2f h)" % (i, len(jobs), os.path.basename(path), sec,
                                                          (time.perf_counter() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
