"""E3a, the pilot (note 3, C17; D6). EXPLORATORY AND LABELLED - its output is not a result.

Its job is to locate ED's crumpled-to-branched crossing in the sync control f and to find which
quantity moves cleanly through it. The order parameter, the crossing's location and the campaign's
ladder are fixed FROM this and written down as a decision BEFORE any campaign run (C17). The pilot
is also allowed to stop the campaign: if no quantity moves monotonically across the crossing, E3b
does not run.

Threshold (C16): s_max = f x median over 8 reading seeds of the flat slice's largest link strain at
that size, replacing attempt 7's single-seed value and its 10 per cent reading-seed wobble.

Nothing here is pre-registered except the two checks note 3 fixed:
  E3-7  the ladder brackets the crossing: the chosen quantity at the loosest and tightest f differ
        by more than three times the seed-to-seed spread known from tier 3.
  E3-8  the no-sync control sits with the loosest f.
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
SEED = 0
FS = (2.0, 1.5, 1.2, 0.9, 0.7, 0.55, 0.45, 0.3, 0.22)
CAL_SEEDS = 8
TETS_PER_EVENT_CAP = 20
OUT = "e3_pilot_runs"


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def flat_strain_median(n, k=CAL_SEEDS):
    """The flat slice's largest link strain, median over k reading seeds (C16)."""
    from c3b import sync_steady_state
    path = os.path.join(OUT, "cal_n%d.json" % n)
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))["median"]
    M = Slice3P(n)
    A, ids, pos, ei, ej = M.adjacency()
    vals = [float(sync_steady_state(A, s)["max_link_diff"]) for s in range(k)]
    res = dict(n=n, seeds=k, values=vals, median=float(np.median(vals)),
               lo=float(min(vals)), hi=float(max(vals)))
    dump(path, res)
    return res["median"]


def do_job(job):
    tag, f, s_max = job
    path = os.path.join(OUT, "pilot_%s.json" % tag)
    if os.path.exists(path):
        return path, 0.0
    use_sync = s_max is not None
    t0 = time.perf_counter()
    M = Slice3P(N)
    M.seed(SEED)
    V0 = M.V
    rng = np.random.default_rng(SEED)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - M.E
    ok = dict(structure=True, budget=True, link=True, cap=True, flips=True)
    status = "survived"
    sizes, ref = [], []
    snaps = []
    keep_from = T - KEEP
    for t in range(1, T + 1):
        if M.T / max(M.V, 1) > TETS_PER_EVENT_CAP:
            status = "densified"
            break
        edges = M.edges() if t > keep_from else None
        r, pool, kids, absd = M.tick(1.0, 1.0, pool, s_max=s_max, cap=CEILING)
        if t > keep_from:
            snaps.append((edges, kids.copy(), absd.copy()))
        sizes.append(r["size"])
        ref.append((r["refused_budget"], r["refused_cap"], r["refused_sync"], r["split_refused"],
                    r["merges"], r["splits"], r["forced"]))
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
    ra = np.array(ref) if ref else np.zeros((1, 7))
    res = dict(tag=tag, f=f, s_max=s_max, sync=use_sync, n=N, V0=V0, BL=BL, seed=SEED,
               status=status, ticks=len(sizes), ok=ok,
               events=M.V, links=M.E, tets=M.T,
               events_vs_start=M.V / V0,
               links_per_event=M.E / max(M.V, 1), tets_per_event=M.T / max(M.V, 1),
               mean_degree=2 * M.E / max(M.V, 1),
               refused_budget_per_tick=float(ra[:, 0].mean()), refused_cap_per_tick=float(ra[:, 1].mean()),
               refused_sync_per_tick=float(ra[:, 2].mean()), split_refused_per_tick=float(ra[:, 3].mean()),
               merges_per_tick=float(ra[:, 4].mean()), splits_per_tick=float(ra[:, 5].mean()),
               forced_per_tick=float(ra[:, 6].mean()))
    # E3-6: strangled growth is its own outcome and gets no shape
    res["strangled"] = bool(res["split_refused_per_tick"] > 10 or res["events_vs_start"] > 1.20)
    if status == "survived":
        from p3_readings import slice_readings, spacetime_readings
        sl = slice_readings(M, SEED)
        res["slice"] = sl
        res["R"] = (sl["diameter"] / M.V ** (1.0 / 3.0)) if sl.get("diameter") else None
        snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
        t1 = time.perf_counter()
        res["spacetime"] = spacetime_readings(snaps, 4000 + SEED)
        res["spacetime_seconds"] = time.perf_counter() - t1
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def report():
    rows = []
    for tag in ["control"] + ["f%s" % str(f).replace(".", "p") for f in FS]:
        p = os.path.join(OUT, "pilot_%s.json" % tag)
        if os.path.exists(p):
            rows.append(json.load(open(p, encoding="utf-8")))
    if not rows:
        return "no runs"
    L = ["E3a pilot, n=%d, seed %d, T=%d. EXPLORATORY - not a result." % (N, SEED, T), ""]
    L.append("%-9s %8s %7s %8s %7s %7s %7s %8s %8s %9s %7s" %
             ("f", "s_max", "status", "ev/V0", "lpe", "R", "d_H", "d_s", "st d_H", "sync/tick", "abandon"))
    for r in rows:
        sl = r.get("slice") or {}
        st = r.get("spacetime") or {}
        fmt = lambda x, d=2: ("%.*f" % (d, x)) if isinstance(x, (int, float)) else "-"
        L.append("%-9s %8s %7s %8s %7s %7s %7s %8s %8s %9.0f %7.2f%s" % (
            ("control" if not r["sync"] else fmt(r["f"], 2)),
            fmt(r["s_max"], 2) if r["s_max"] else "-",
            ("strangled" if r.get("strangled") else r["status"])[:7],
            fmt(r["events_vs_start"], 3), fmt(r["links_per_event"]), fmt(r.get("R"), 3),
            fmt(sl.get("d_H")), fmt(sl.get("d_s")), fmt(st.get("d_H")),
            r["refused_sync_per_tick"], r["split_refused_per_tick"],
            "" if all(r["ok"].values()) else "  CHECKS FAILED"))
    text = "\n".join(L)
    with open("e3_pilot.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return text


def main(workers):
    os.makedirs(OUT, exist_ok=True)
    base = flat_strain_median(N)
    print("flat strain median over %d reading seeds: %.4f" % (CAL_SEEDS, base), flush=True)
    jobs = [("control", None, None)]
    jobs += [("f%s" % str(f).replace(".", "p"), f, f * base) for f in FS]
    t0 = time.perf_counter()
    with Pool(workers) as pool:
        for i, (path, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print("[%d/%d] %s %.0f s (elapsed %.2f h)" % (i, len(jobs), os.path.basename(path), sec,
                                                          (time.perf_counter() - t0) / 3600), flush=True)
    print(report())


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
