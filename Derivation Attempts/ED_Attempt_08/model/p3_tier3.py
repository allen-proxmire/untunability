"""Tier 3 of note 2's ladder (C5): whole runs, compared statistically with attempt 7.

Attempt 7 has two seeds per setting; two values cannot define a spread, so the port supplies it.
This runs the port at n = 24 for SEEDS seeds at settings A and B, T = 150, exactly C3g's model and
knobs, and reports whether attempt 7's C3g values fall inside the port's seed-to-seed range.

Expected results, written down before this run:
  T1  structure clean every tick, event budget conserved, links + pool = BL, flips link-neutral,
      and no event count outside a tenth or ten times the start, in every seed.
  T2  attempt 7's C3g value for setting A at n = 24 lies inside the port's 8-seed range for each of
      links per event, slice diameter, and the grown spacetime's mass dimension; the same for B.
  T3  setting B records more sync refusals per tick than zero, and differs from A, as C3g found.
Exit rule: T1 failing is a port bug. T2 failing means the port is a different model - said plainly,
with the difference named, and not used to reinterpret attempt 7. T3 failing means the condition is
inert in the port and that is a port bug, since C3g's was not.

Resumable: one JSON per finished job in p3_tier3_runs/.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING

N = 24
T = 150
KEEP = 20
SEEDS = tuple(range(8))
SETTINGS = {"A": (1.0, 1.0, False), "B": (1.0, 1.0, True)}
SYNC_FACTOR = 1.5
READING_SEED = 1        # attempt 7 used SIZES.index(n); 1 at n = 24
TETS_PER_EVENT_CAP = 20
OUT = "p3_tier3_runs"

# attempt 7, C3g, n = 24 (note 29): the values the port's spread must contain
A7 = {"A": dict(links_per_event=5.15, diameter=12.5, spacetime_d_H=6.44, refused_sync_per_tick=0.0),
      "B": dict(links_per_event=5.12, diameter=15.0, spacetime_d_H=6.33, refused_sync_per_tick=1403.0)}


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def flat_threshold(n):
    """The threshold attempt 7's C3g actually used, not a freshly chosen one.

    C3g set s_max = 1.5 x the flat calibration's neck strain, and that calibration's reading seed was
    `SIZES.index(n)` - 0 for n = 20, 1 for n = 24. The first version of this runner passed seed 0 at
    n = 24 and so ran at 10.956 where attempt 7 ran at 9.985, a 9.7 per cent higher threshold; that,
    and not the model, is why the port refused fewer moves on sync (C13). The value is now read from
    attempt 7's own calibration file, so the two cannot drift apart again.
    """
    import json
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "ED_Attempt_07", "model", "c3g_runs", "cal_FC_n%d.json" % n)
    if os.path.exists(p):
        return SYNC_FACTOR * float(json.load(open(p, encoding="utf-8"))["readings"]["neck_strain"])
    from c3b import sync_steady_state
    M = Slice3P(n)
    A, ids, pos, ei, ej = M.adjacency()
    return SYNC_FACTOR * float(sync_steady_state(A, READING_SEED)["max_link_diff"])


def do_job(job):
    name, s, s_max = job
    path = os.path.join(OUT, "grow_%s_s%d.json" % (name, s))
    if os.path.exists(path):
        return path, 0.0
    alpha, lam, use_sync = SETTINGS[name]
    sm = s_max if use_sync else None
    t0 = time.perf_counter()
    M = Slice3P(N)
    M.seed(s)
    V0 = M.V
    rng = np.random.default_rng(s)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - M.E
    ok = dict(structure=True, budget=True, link=True, cap=True, flips=True)
    status = "survived"
    sizes = []
    ref = []
    snaps = []
    keep_from = T - KEEP
    for t in range(1, T + 1):
        if M.T / max(M.V, 1) > TETS_PER_EVENT_CAP:
            status = "densified"
            break
        edges = M.edges() if t > keep_from else None
        r, pool, kids, absd = M.tick(alpha, lam, pool, s_max=sm, cap=CEILING)
        if t > keep_from:
            snaps.append((edges, kids.copy(), absd.copy()))
        sizes.append(r["size"])
        ref.append((r["refused_budget"], r["refused_cap"], r["refused_sync"], r["split_refused"],
                    r["merges"], r["splits"]))
        if not r["flips_link_neutral"]:
            ok["flips"] = False
        if M.check():
            ok["structure"] = False
            status = "structure failure"
            break
        if abs(float(M.S.b[M.vertices()].sum()) - V0) > 1e-9 * V0:
            ok["budget"] = False
        if M.E + pool != BL:
            ok["link"] = False
        if max(M.degree(v) for v in M.vertices()) > CEILING:
            ok["cap"] = False
        if not (V0 / 10 <= r["size"] <= 10 * V0):
            status = "died" if r["size"] < V0 / 10 else "ran away"
            break
    ref = np.array(ref) if ref else np.zeros((1, 6))
    res = dict(setting=name, seed=s, n=N, V0=V0, BL=BL, status=status, ticks=len(sizes), ok=ok,
               s_max=(s_max if use_sync else None),
               mean_size_late=float(np.mean(sizes[T // 2 - 1:])) if len(sizes) >= T else None,
               events=M.V, links=M.E, tets=M.T,
               links_per_event=M.E / max(M.V, 1), tets_per_event=M.T / max(M.V, 1),
               refused_budget_per_tick=float(ref[:, 0].mean()), refused_cap_per_tick=float(ref[:, 1].mean()),
               refused_sync_per_tick=float(ref[:, 2].mean()), split_refused_per_tick=float(ref[:, 3].mean()),
               merges_per_tick=float(ref[:, 4].mean()), splits_per_tick=float(ref[:, 5].mean()))
    if status == "survived":
        from p3_readings import slice_readings, spacetime_readings
        res["slice"] = slice_readings(M, s)
        snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
        res["spacetime"] = spacetime_readings(snaps, 4000 + s)
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def report():
    lines = []
    got = {}
    for name in SETTINGS:
        rows = []
        for s in SEEDS:
            p = os.path.join(OUT, "grow_%s_s%d.json" % (name, s))
            if os.path.exists(p):
                rows.append(json.load(open(p, encoding="utf-8")))
        got[name] = rows
        if not rows:
            continue
        lines.append("setting %s: %d seeds, statuses %s" % (name, len(rows), sorted({r["status"] for r in rows})))
        bad = [k for r in rows for k, v in r["ok"].items() if not v]
        lines.append("  T1 structure/budgets/ceiling/flips: %s" % ("clean" if not bad else "FAILED: " + str(sorted(set(bad)))))
        for key, path in (("links_per_event", ("links_per_event",)), ("diameter", ("slice", "diameter")),
                          ("spacetime_d_H", ("spacetime", "d_H")), ("refused_sync_per_tick", ("refused_sync_per_tick",))):
            vals = []
            for r in rows:
                x = r
                for k in path:
                    x = (x or {}).get(k) if isinstance(x, dict) else None
                if isinstance(x, (int, float)):
                    vals.append(float(x))
            if not vals:
                lines.append("  %-22s no values" % key)
                continue
            lo, hi = min(vals), max(vals)
            ref = A7[name][key]
            inside = lo <= ref <= hi
            lines.append("  %-22s port %.3f - %.3f (mean %.3f, n=%d) | A7 %.3f | %s"
                         % (key, lo, hi, float(np.mean(vals)), len(vals), ref,
                            "INSIDE" if inside else "OUTSIDE"))
    return "\n".join(lines)


def main(workers):
    os.makedirs(OUT, exist_ok=True)
    s_max = flat_threshold(N)
    print("sync threshold %.3f" % s_max, flush=True)
    only = os.environ.get("P3_SETTINGS", "BA")
    jobs = [(name, s, s_max) for name in ("B", "A") if name in only for s in SEEDS]
    t0 = time.perf_counter()
    with Pool(workers) as pool:
        for i, (path, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print("[%d/%d] %s %.0f s (elapsed %.2f h)" % (i, len(jobs), os.path.basename(path), sec,
                                                          (time.perf_counter() - t0) / 3600), flush=True)
    text = report()
    print(text)
    with open("p3_tier3.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
