"""E4 (note 5, C26-C28; D7): does the branched reading survive at size?

Sizes n = 24, 32, 52 at f = 0.45, three seeds, T = 150, with a no-sync control at n = 32 and n = 52
(n = 24's control is tier 3's eight setting-A runs). Threshold s_max = f x median flat strain over
eight reading seeds at that size (C16).

Expected results, written down before this run (note 5):
  E4-0  the gate: at every size the flat calibration reads d_H within 0.3 of its n = 24 value 2.657
        and d_s within 0.4 of 3.05, and the randomised one reads d_H undefined with mean degree > 26.
  E4-1  structure, budgets, ceiling and flip neutrality exact; all runs survive and none is strangled.
  E4-2  at n = 52 the slice readings are defined: at least six usable radii and diameter >= 20.
  E4-3  THE ONE THAT MATTERS: d_s stays at or below 2 at all three sizes and does not trend upward.
  E4-4  mean degree stays <= 13.40 x (V0/V) and max degree stays pinned at the ceiling, every run.
  E4-5  the grown spacetime's mass dimension reported at each size with its usable radii.
Exit rule: note 5's table. The gate is checked BEFORE any growth run; if flat does not read flat at
n = 52, nothing downstream means anything and road E closes as a failed instrument.

Resumable: one JSON per finished job in e4_runs/. Memory is the binding constraint at n = 52, so
that size runs with fewer workers (C25).
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool
from p3 import Slice3P
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING, FLAT_VALENCE

SIZES = (24, 32, 52)
F = 0.45
SEEDS = (0, 1, 2)
CTRL_SEEDS = (0, 1)
T = 150
KEEP = 20
CAL_SEEDS = 8
CAL_REPS = 5            # seeds per calibration (D8, C29); was one, which gave no spread
TETS_PER_EVENT_CAP = 20
FLAT_MEAN_DEGREE = 2 * FLAT_LINKS_PER_EVENT      # 13.398
OUT = "e4_runs"
WORKERS = {24: 3, 32: 4, 52: 2}
SPACETIME_MAX_N = 32    # above this a spacetime reading needs about 6.5 GB (D9); see e4_spacetime52.py
SNAP_SEED = 0           # the one n = 52 seed whose slices are kept, for a single reading afterwards


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def cal_job(job):
    kind, n, rep = job
    path = os.path.join(OUT, "cal_%s_n%d_r%d.json" % (kind, n, rep))
    if os.path.exists(path):
        return path, 0.0
    from p3_readings import slice_readings
    from c3b import sync_steady_state
    t0 = time.perf_counter()
    if kind == "RC":
        # RC ignores the link budget, so it needs far more room than flat: measured at about
        # 14.5 links and 13.5 tetrahedra per starting event. The first run silently overran the
        # default caps and read mean degree exactly 20.0 = 2 x (10 V0)/V, the edge array's edge.
        M = Slice3P(n, t_cap=24 * n ** 3, e_cap=24 * n ** 3)
        M.seed(7 + rep)
        M.flip_randomize(50)
    else:
        M = Slice3P(n)
    res = dict(job="cal", kind=kind, n=n, rep=rep, structure_notes=M.check(),
               readings=slice_readings(M, 100 * rep + SIZES.index(n)))
    if kind == "FC" and rep == 0:
        A, ids, pos, ei, ej = M.adjacency()
        vals = [float(sync_steady_state(A, s)["max_link_diff"]) for s in range(CAL_SEEDS)]
        res["strain_values"] = vals
        res["strain_median"] = float(np.median(vals))
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def do_job(job):
    n, s, s_max = job
    tag = "grow_n%d_s%d%s" % (n, s, "" if s_max else "_ctrl")
    path = os.path.join(OUT, tag + ".json")
    if os.path.exists(path):
        return path, 0.0
    t0 = time.perf_counter()
    M = Slice3P(n)
    M.seed(s)
    V0 = M.V
    rng = np.random.default_rng(s)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    BL = round(FLAT_LINKS_PER_EVENT * V0)
    pool = BL - M.E
    ok = dict(structure=True, budget=True, link=True, cap=True, flips=True)
    cap_claim = True                      # E4-4: mean degree <= 13.40 * V0/V, max degree <= ceiling
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
        md = 2 * M.E / max(M.V, 1)
        mx = max(M.degree(v) for v in M.vertices())
        if mx > CEILING:
            ok["cap"] = False
        if md > FLAT_MEAN_DEGREE * V0 / max(M.V, 1) + 1e-9 or mx > CEILING:
            cap_claim = False
        if not (V0 / 10 <= r["size"] <= 10 * V0):
            status = "died" if r["size"] < V0 / 10 else "ran away"
            break
    ra = np.array(ref) if ref else np.zeros((1, 7))
    res = dict(job="grow", n=n, seed=s, f=(F if s_max else None), s_max=s_max, sync=bool(s_max),
               V0=V0, BL=BL, status=status, ticks=len(sizes), ok=ok, cap_claim_held=cap_claim,
               events=M.V, links=M.E, tets=M.T, events_vs_start=M.V / V0,
               links_per_event=M.E / max(M.V, 1), tets_per_event=M.T / max(M.V, 1),
               mean_degree=2 * M.E / max(M.V, 1),
               mean_degree_bound=FLAT_MEAN_DEGREE * V0 / max(M.V, 1),
               refused_budget_per_tick=float(ra[:, 0].mean()), refused_cap_per_tick=float(ra[:, 1].mean()),
               refused_sync_per_tick=float(ra[:, 2].mean()), split_refused_per_tick=float(ra[:, 3].mean()),
               merges_per_tick=float(ra[:, 4].mean()), splits_per_tick=float(ra[:, 5].mean()),
               forced_per_tick=float(ra[:, 6].mean()))
    res["strangled"] = bool(res["split_refused_per_tick"] > 10 or res["events_vs_start"] > 1.20)
    if status == "survived":
        from p3_readings import slice_readings, spacetime_readings
        res["slice"] = slice_readings(M, s)
        snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
        if n <= SPACETIME_MAX_N:
            t1 = time.perf_counter()
            res["spacetime"] = spacetime_readings(snaps, 4000 + s)
            res["spacetime_seconds"] = time.perf_counter() - t1
        else:
            # One reading over 3.26 million events needs 200 x 3.26e6 x 8 bytes = 5.2 GB for the
            # distance array alone, plus about 1.25 GB of slice and matrix: about 6.5 GB on a
            # machine with 8.4 GB. Two workers cannot both do it and one is marginal (D9).
            res["spacetime_skipped"] = "memory: about 6.5 GB per reading"
            if s == SNAP_SEED and s_max is not None:
                np.savez_compressed(os.path.join(OUT, "snaps_n%d_s%d.npz" % (n, s)),
                                    n_snaps=len(snaps),
                                    **{("e%d" % i): snaps[i][0] for i in range(len(snaps))},
                                    **{("k%d" % i): snaps[i][1] for i in range(len(snaps))},
                                    **{("a%d" % i): snaps[i][2] for i in range(len(snaps))})
                res["snapshots_saved"] = True
    res["seconds"] = time.perf_counter() - t0
    dump(path, res)
    return path, res["seconds"]


def cal_rows(kind, n):
    out = []
    for rep in range(CAL_REPS):
        p = os.path.join(OUT, "cal_%s_n%d_r%d.json" % (kind, n, rep))
        if os.path.exists(p):
            out.append(json.load(open(p, encoding="utf-8"))["readings"])
    return out


def gate():
    """E4-0a/b/c as replaced in note 5's addendum (C29), declared before these runs existed.

    E4-0a gates: flat resolves geometry at every size. E4-0b and E4-0c are recorded, not gating.
    """
    lines = []
    ok = True
    for n in SIZES:
        fc = cal_rows("FC", n)
        rc = cal_rows("RC", n)
        fds = [r["d_s"] for r in fc if r.get("d_s") is not None]
        fdh = [r["d_H"] for r in fc if r.get("d_H") is not None]
        rds = [r["d_s"] for r in rc if r.get("d_s") is not None]
        rdh = [r["d_H"] for r in rc if r.get("d_H") is not None]
        radii = [r["r_max"] - r["r_lo"] + 1 for r in fc if r.get("r_lo") is not None]
        a1 = len(fds) == CAL_REPS and all(abs(x - 3.0) <= 0.4 for x in fds)
        a2 = len(fdh) == CAL_REPS
        a3 = (n != 52) or (len(radii) == CAL_REPS and min(radii) >= 6)
        a4 = len(fds) > 1 and (max(fds) - min(fds)) < 0.5
        a = a1 and a2 and a3 and a4
        ok = ok and a
        sep = []
        for nm, fv, rv in (("d_H", fdh, rdh), ("d_s", fds, rds)):
            if fv and rv and (min(fv) > max(rv) or min(rv) > max(fv)):
                sep.append(nm)
        lines.append("  n=%-3d FC d_s %.3f-%.3f (spread %.3f) d_H %.3f-%.3f radii>=%s | RC d_s %s d_H %s | E4-0a %s | E4-0b separates on: %s"
                     % (n, min(fds), max(fds), max(fds) - min(fds), min(fdh), max(fdh),
                        (min(radii) if radii else "-"),
                        ("%.3f-%.3f" % (min(rds), max(rds))) if rds else "undefined",
                        ("%.3f-%.3f" % (min(rdh), max(rdh))) if rdh else "undefined",
                        "PASS" if a else "FAIL", ", ".join(sep) if sep else "NOTHING (limitation carried, C28/C29)"))
    return ok, "E4-0a gate: %s" % ("PASS" if ok else "FAIL") + chr(10) + chr(10).join(lines)


def report():
    L = ["E4: does the branched reading survive at size? f = %.2f, T = %d, seeds %s" % (F, T, SEEDS), ""]
    L.append("%-5s %-6s %7s %9s %8s %8s %8s %8s %9s %9s %8s" %
             ("n", "seed", "status", "ev/V0", "meandeg", "bound", "maxdeg", "diam", "slice d_H", "d_s", "st d_H"))
    for n in SIZES:
        for tag in ["grow_n%d_s%d" % (n, s) for s in SEEDS] + ["grow_n%d_s%d_ctrl" % (n, s) for s in CTRL_SEEDS]:
            p = os.path.join(OUT, tag + ".json")
            if not os.path.exists(p):
                continue
            r = json.load(open(p, encoding="utf-8"))
            sl = r.get("slice") or {}
            st = r.get("spacetime") or {}
            f = lambda x, d=2: ("%.*f" % (d, x)) if isinstance(x, (int, float)) else "-"
            L.append("%-5d %-6s %7s %9s %8.2f %8.2f %8s %8s %9s %9s %8s%s" % (
                n, ("ctrl" if not r["sync"] else r["seed"]),
                ("strangl" if r.get("strangled") else r["status"])[:7],
                f(r["events_vs_start"], 3), r["mean_degree"], r["mean_degree_bound"],
                sl.get("max_degree"), sl.get("diameter"), f(sl.get("d_H")), f(sl.get("d_s")), f(st.get("d_H")),
                "" if all(r["ok"].values()) and r["cap_claim_held"] else "  CHECK FAILED"))
    text = "\n".join(L)
    with open("e4_run.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return text


def main(stage):
    os.makedirs(OUT, exist_ok=True)
    if stage in ("cal", "all"):
        jobs = [(k, n, r) for n in SIZES for k in ("FC", "RC") for r in range(CAL_REPS)]
        with Pool(3) as pool:
            for path, sec in pool.imap_unordered(cal_job, jobs):
                print("cal %s %.0f s" % (os.path.basename(path), sec), flush=True)
        ok, text = gate()
        print(text, flush=True)
        with open("e4_gate.txt", "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        if not ok:
            print("GATE FAILED - no growth run starts (note 5's exit rule).", flush=True)
            return 1
    if stage in ("grow", "all"):
        t0 = time.perf_counter()
        for n in SIZES:
            base = json.load(open(os.path.join(OUT, "cal_FC_n%d_r0.json" % n), encoding="utf-8"))["strain_median"]
            s_max = F * base
            jobs = [(n, s, s_max) for s in SEEDS]
            if n != 24:
                jobs += [(n, s, None) for s in CTRL_SEEDS]
            print("n=%d: strain median %.4f -> s_max %.4f, %d runs on %d workers"
                  % (n, base, s_max, len(jobs), WORKERS[n]), flush=True)
            with Pool(WORKERS[n]) as pool:
                for path, sec in pool.imap_unordered(do_job, jobs):
                    print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec,
                                                            (time.perf_counter() - t0) / 3600), flush=True)
        print(report(), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "all"))
