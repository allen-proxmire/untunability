"""C3g runs: C3f rerun with the sync condition's units fixed (D43; note 27 with its D41 threshold).

C3f run 1's sync condition never fired because the threshold was in the calibration's normalized units
(its solver uses rate spread and pull of 1) while the check compared the run's raw tick differences
(scale sigma/K = 0.001). The comparison is now scaled. Nothing else changes: same model, same settings,
same sizes, same seeds, same T, same readings, same classification, same exit rule, and the same
threshold s_max = 1.5 x the flat calibration's largest link strain, which the created-link diagnostic
(C97) puts at about the 99th percentile of the strain that created links actually carry.

Expected results, written down before this run:
  As note 27 (E0-E5), unchanged, with one addition:
  E6  the sync condition fires: settings B and C record more than zero sync refusals per tick, and B is
      no longer identical to A.
Exit rule: as note 27, with E6 reported; if E6 fails the condition is still toothless and that is
recorded, with sync in growth returned to Allen.
Resumable: one JSON per finished job in c3g_runs/; state saved every 10 ticks, except during the window
whose slices are kept for the spacetime pattern.
"""
import json
import os
import pickle
import sys
import time
import numpy as np
from multiprocessing import Pool
from c3c import Slice3, flip_randomize, SIGMA
from c3d import slice_readings, FLAT_LINKS_PER_EVENT
from c3e import CEILING
from c3f import tick, slice_edges, spacetime_readings

SIZES = (20, 24)
KEEP = {20: 30, 24: 20}          # ticks kept for the spacetime pattern
SETTINGS = {"A": (1.0, 1.0, False), "B": (1.0, 1.0, True), "C": (0.0, 0.0, True), "D": (0.0, 0.0, False)}
SEEDS = (0, 1)
T = 150
CHECKS = (T // 2, (3 * T) // 4, T)
OUT = "c3g_runs"
CKPT_EVERY = 10
TETS_PER_EVENT_CAP = 20
FLAT_MEAN_DEGREE = 2 * FLAT_LINKS_PER_EVENT      # 13.40
SYNC_FACTOR = 1.5


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def cal_path(kind, n):
    return os.path.join(OUT, f"cal_{kind}_n{n}.json")


def do_job(job):
    if job[0] == "cal":
        _, kind, n = job
        path = cal_path(kind, n)
        if os.path.exists(path):
            return path, 0
        t0 = time.perf_counter()
        M = Slice3(n)
        if kind == "RC":
            flip_randomize(M, 50, np.random.default_rng(7))
        res = dict(job="cal", kind=kind, n=n, structure_notes=M.check(),
                   readings=slice_readings(M, SIZES.index(n), with_walk=True))
        res["seconds"] = time.perf_counter() - t0
        dump(path, res)
        return path, res["seconds"]
    _, name, n, s, s_max = job
    path = os.path.join(OUT, f"grow_{name}_n{n}_s{s}.json")
    if os.path.exists(path):
        return path, 0
    ck = os.path.join(OUT, "ckpt", f"grow_{name}_n{n}_s{s}.pkl")
    alpha, lam, use_sync = SETTINGS[name]
    keep_from = T - KEEP[n]
    if os.path.exists(ck):
        with open(ck, "rb") as f:
            st = pickle.load(f)
    else:
        M = Slice3(n)
        rng = np.random.default_rng(s)
        V0 = len(M.vt)
        BL = round(FLAT_LINKS_PER_EVENT * V0)
        st = dict(M=M, rng=rng, b={v: 1.0 for v in M.vt},
                  omega={v: 1.0 + SIGMA * g for v, g in zip(M.vt, rng.standard_normal(V0))},
                  phi={v: 0.0 for v in M.vt}, t=0, V0=V0, BL=BL, pool=BL - len(M.val),
                  sizes=[], forced=[], flips=[], ref=[], flips_ok=True, first_fail=None,
                  budget_ok=True, link_ok=True, cap_ok=True, status="survived", checkpoints={}, elapsed=0.0)
    M, rng = st["M"], st["rng"]
    snaps = []
    seg0 = time.perf_counter()
    while st["t"] < T and st["status"] == "survived":
        if len(M.tets) / max(len(M.vt), 1) > TETS_PER_EVENT_CAP:
            st["status"] = "densified"
            break
        st["t"] += 1
        t = st["t"]
        rec = {} if t > keep_from else None
        edges = slice_edges(M) if rec is not None else None
        r, st["pool"] = tick(M, st["b"], st["omega"], st["phi"], rng, alpha, lam, st["pool"],
                             s_max=(s_max if use_sync else None), cap=CEILING, record=rec)
        if rec is not None:
            snaps.append((edges, rec))
        st["sizes"].append(r["size"]); st["forced"].append(r["forced"]); st["flips"].append(r["flips_accepted"])
        st["ref"].append((r["refused_budget"], r["refused_cap"], r["refused_sync"], r["split_refused"],
                          r["merges"], r["splits"]))
        if not r["flips_link_neutral"]:
            st["flips_ok"] = False
        notes = M.check()
        if notes:
            st["first_fail"] = [t, notes[:3]]
            st["status"] = "structure failure"
            break
        if abs(sum(st["b"].values()) - st["V0"]) > 1e-9 * st["V0"]:
            st["budget_ok"] = False
        if len(M.val) + st["pool"] != st["BL"]:
            st["link_ok"] = False
        if max(len(x) for x in M.nbrs.values()) > CEILING:
            st["cap_ok"] = False
        if not (st["V0"] / 10 <= r["size"] <= 10 * st["V0"]):
            st["status"] = "died" if r["size"] < st["V0"] / 10 else "ran away"
            break
        if t in CHECKS:
            st["checkpoints"][str(t)] = slice_readings(M, 10 * s + SIZES.index(n), with_walk=True)
        if t % CKPT_EVERY == 0 and t < keep_from:
            st["elapsed"] += time.perf_counter() - seg0
            seg0 = time.perf_counter()
            tmp = ck + ".tmp"
            with open(tmp, "wb") as f:
                pickle.dump(st, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, ck)
    st["elapsed"] += time.perf_counter() - seg0
    late = st["sizes"][T // 2 - 1:] if len(st["sizes"]) >= T else []
    ref = np.array(st["ref"]) if st["ref"] else np.zeros((1, 6))
    res = dict(job="grow", setting=name, alpha=alpha, lam=lam, sync=use_sync, s_max=s_max, n=n, V0=st["V0"],
               BL=st["BL"], seed=s, status=st["status"], ticks_done=st["t"], first_structure_fail=st["first_fail"],
               budget_ok=st["budget_ok"], link_budget_ok=st["link_ok"], cap_ok=st["cap_ok"], flips_ok=st["flips_ok"],
               mean_size_late=float(np.mean(late)) if late else None,
               forced_per_tick=float(np.mean(st["forced"])) if st["forced"] else None,
               flips_accepted_per_tick=float(np.mean(st["flips"])) if st["flips"] else None,
               refused_budget_per_tick=float(ref[:, 0].mean()), refused_cap_per_tick=float(ref[:, 1].mean()),
               refused_sync_per_tick=float(ref[:, 2].mean()), split_refused_per_tick=float(ref[:, 3].mean()),
               merges_per_tick=float(ref[:, 4].mean()), splits_per_tick=float(ref[:, 5].mean()),
               events=len(M.vt), tets=len(M.tets), links=len(M.val),
               links_per_event=len(M.val) / max(len(M.vt), 1), tets_per_event=len(M.tets) / max(len(M.vt), 1),
               mean_degree=2 * len(M.val) / max(len(M.vt), 1),
               max_degree=max((len(x) for x in M.nbrs.values()), default=0),
               checkpoints=st["checkpoints"], seconds=st["elapsed"])
    if st["status"] == "survived" and snaps:
        snaps.append((slice_edges(M), {"children": {}, "absorbed": {}}))
        t0 = time.perf_counter()
        sr = spacetime_readings(snaps, 4000 + s)
        res["spacetime"] = {k: (float(sr[k]) if isinstance(sr.get(k), (int, float, np.floating)) and sr.get(k) is not None else sr.get(k))
                            for k in ("d_H", "r_lo", "r_max", "small_world", "events", "links")}
        res["spacetime_seconds"] = time.perf_counter() - t0
    dump(path, res)
    if os.path.exists(ck):
        os.remove(ck)
    return path, st["elapsed"]


def fin(x):
    return x is not None and np.isfinite(x)


def med(xs):
    xs = [x for x in xs if fin(x)]
    return float(np.median(xs)) if xs else float("nan")


def classify(rds, fc):
    m = lambda k: med([r.get(k) for r in rds])
    dH, ds, diam = m("d_H"), m("d_s"), m("diameter")
    if not fin(dH) or (fin(diam) and diam < 8):
        return "too small to measure", dH, ds
    flags = []
    if m("mean_degree") >= 2 * FLAT_MEAN_DEGREE or m("tets_per_event") >= 2 * 5.699:
        flags.append("crumpled")
    if all(bool(r["small_world"]) for r in rds):
        flags.append("hyperbolic")
    if m("neck_strain") >= 3 * fc["neck_strain"] or dH < 2.3 or (fin(ds) and ds < 2.0):
        flags.append("branched")
    if not flags and 2.5 <= dH <= 3.5 and fin(ds) and 2.3 <= ds <= 3.7:
        return "flat 3D", dH, ds
    return (" + ".join(flags) if flags else "unclassified"), dH, ds


def gate(R):
    lines, FC, ok = [], {}, True
    for n in SIZES:
        fc = R[f"cal_FC_n{n}"]["readings"]
        rc = R[f"cal_RC_n{n}"]["readings"]
        FC[n] = fc
        sf, dHf, dsf = classify([fc], fc)
        sr, dHr, dsr = classify([rc], fc)
        good = sf == "flat 3D" and sr != "flat 3D"
        ok = ok and good
        lines.append(f"calibration V={n**3}: FC {sf} (d_H {dHf:.3f}, d_s {dsf:.3f}, diameter {fc['diameter']:.0f}, "
                     f"largest link strain {fc['neck_strain']:.2f} -> sync threshold {SYNC_FACTOR * fc['neck_strain']:.2f}); "
                     f"RC {sr} (d_H {dHr}, diameter {rc['diameter']:.0f}) -> {'ok' if good else 'NOT ok'}")
    return ok, lines, FC


def analyse():
    R = {}
    for fn in os.listdir(OUT):
        if fn.endswith(".json"):
            R[fn[:-5]] = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
    ok, lines, FC = gate(R)
    e0, e1, e2 = ok, True, True
    shape, settled, st_dH = {}, {}, {}
    for name in SETTINGS:
        for n in SIZES:
            keys = [f"grow_{name}_n{n}_s{s}" for s in SEEDS]
            if not all(k in R for k in keys):
                shape[(name, n)] = "not run"
                continue
            runs = [R[k] for k in keys]
            for r in runs:
                if r["first_structure_fail"] or not r["budget_ok"] or not r["link_budget_ok"] or not r["cap_ok"] or not r["flips_ok"]:
                    e1 = False
                drift = r["status"] == "survived" and (r["mean_size_late"] is None or abs(r["mean_size_late"] / r["V0"] - 1) > 0.10)
                if drift or r["status"] == "structure failure":
                    if name in ("A", "D"):
                        e1 = False
                    else:
                        e2 = False
            good = [r for r in runs if r["status"] == "survived" and str(T) in r["checkpoints"]]
            if len(good) < len(runs):
                shape[(name, n)] = [r["status"] for r in runs]
                settled[(name, n)] = False
                lines.append(f"{name} V={n**3}: statuses {shape[(name, n)]}")
                continue
            rT = [r["checkpoints"][str(T)] for r in good]
            r3 = [r["checkpoints"][str(CHECKS[1])] for r in good]
            shp, dH, ds = classify(rT, FC[n])
            ch = [abs(a["d_H"] - b["d_H"]) for a, b in zip(rT, r3) if fin(a["d_H"]) and fin(b["d_H"])]
            dg = [abs(a["mean_degree"] - b["mean_degree"]) / b["mean_degree"] for a, b in zip(rT, r3)]
            settled[(name, n)] = bool(ch) and med(ch) <= 0.15 and med(dg) <= 0.20
            shape[(name, n)] = shp
            stv = [r.get("spacetime", {}).get("d_H") for r in good]
            st_dH[(name, n)] = med(stv)
            m = lambda k: med([x[k] for x in rT])
            lines.append(f"{name} V={n**3}: slice {shp}; d_H {dH:.3f}, d_s {ds:.3f}, diameter {m('diameter'):.1f} (FC {FC[n]['diameter']:.0f}); "
                         f"SPACETIME d_H {st_dH[(name, n)]:.3f} (radii {[r.get('spacetime', {}).get('r_lo') for r in good]}-"
                         f"{[r.get('spacetime', {}).get('r_max') for r in good]}, events {[r.get('spacetime', {}).get('events') for r in good]}); "
                         f"settled {settled[(name, n)]}; links/event {m('links_per_event'):.3f}, tets/event {m('tets_per_event'):.2f}, "
                         f"mean degree {m('mean_degree'):.2f}, largest {m('max_degree'):.0f}; neck strain {m('neck_strain'):.2f} (FC {FC[n]['neck_strain']:.2f}); "
                         f"late size/V0 {med([r['mean_size_late'] / r['V0'] for r in good]):.3f}; per tick: merges {med([r['merges_per_tick'] for r in good]):.0f}, "
                         f"splits {med([r['splits_per_tick'] for r in good]):.0f}, forced {med([r['forced_per_tick'] for r in good]):.0f}, "
                         f"refused budget/cap/sync/splits {med([r['refused_budget_per_tick'] for r in good]):.0f}/"
                         f"{med([r['refused_cap_per_tick'] for r in good]):.0f}/{med([r['refused_sync_per_tick'] for r in good]):.0f}/"
                         f"{med([r['split_refused_per_tick'] for r in good]):.1f}; flips {med([r['flips_accepted_per_tick'] for r in good]):.0f}")
    big, small = SIZES[-1], SIZES[0]
    inrange = lambda nm, n: fin(st_dH.get((nm, n))) and 3.3 <= st_dH[(nm, n)] <= 4.7
    e3 = inrange("B", small) and inrange("B", big)
    e4 = not inrange("D", big)
    e5 = all(shape.get((nm, n)) != "too small to measure" for nm in SETTINGS for n in SIZES)
    fired = [R[k]["refused_sync_per_tick"] for k in R if k.startswith("grow_") and R[k].get("sync")]
    e6 = bool(fired) and min(fired) > 0
    lines.append(f"sync refusals per tick in B and C: {[round(x, 1) for x in sorted(fired)]}")
    for nm, v in (("E0 calibration gate", e0), ("E1 structure, budgets, ceiling, flips, size (A and D)", e1),
                  ("E2 B and C hold their event counts", e2), ("E3 B's spacetime in [3.3, 4.7]", e3),
                  ("E4 D's spacetime not in range", e4), ("E5 every setting measurable", e5),
                  ("E6 the sync condition fires", e6)):
        lines.append(f"{nm}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if not e0:
        verdict = "E0 failed: readings revision (recorded); growth runs not started."
    elif not e1:
        verdict = "E1 failed: code bug (recorded)."
    elif e3 and not inrange("D", big):
        verdict = ("With the link balance, paired cut-and-rejoin and sync as a condition, ED's growth gives a four-dimensional "
                   "pattern at the sizes run: consistent, not derived; the density, the ceiling, the sync threshold and the "
                   "strengths are knobs." + (" Setting A reads in range as well, so sync is not needed for it."
                                             if inrange("A", small) and inrange("A", big) else ""))
    elif inrange("D", small) and inrange("D", big):
        verdict = "Growth alone gives a four-dimensional pattern at these sizes; the pressures aren't doing the work."
    elif any(shape.get((nm, n)) == "too small to measure" for nm in SETTINGS for n in SIZES):
        verdict = "Too small to measure at these sizes for " + ", ".join(
            f"{nm} V={n**3}" for nm in SETTINGS for n in SIZES if shape.get((nm, n)) == "too small to measure") + "."
    else:
        verdict = ("ED's local weights don't select smooth geometry against entropy; the wall is the ensemble, not the meanings "
                   "(spacetime d_H: " + ", ".join(f"{nm} {st_dH.get((nm, big), float('nan')):.2f}" for nm in SETTINGS) + ").")
    if not e2:
        verdict += " The counts still drift under B or C (bookkeeping above)."
    lines.append("EXIT: " + verdict)
    return lines


def main():
    os.makedirs(os.path.join(OUT, "ckpt"), exist_ok=True)
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t0 = time.perf_counter()
    cals = [("cal", k, n) for n in SIZES for k in ("FC", "RC")]
    with Pool(min(workers, len(cals))) as pool:
        for p, sec in pool.imap_unordered(do_job, cals):
            print(f"calibration {os.path.basename(p)} {sec:.0f} s", flush=True)
    R = {fn[:-5]: json.load(open(os.path.join(OUT, fn), encoding="utf-8")) for fn in os.listdir(OUT) if fn.endswith(".json")}
    ok, lines, FC = gate(R)
    print("\n".join(lines), flush=True)
    if not ok:
        lines.append("EXIT: E0 failed: readings revision (recorded); growth runs not started.")
        print(lines[-1])
        open("c3g_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
        return
    s_max = {n: SYNC_FACTOR * FC[n]["neck_strain"] for n in SIZES}
    jobs = [("grow", nm, n, s, s_max[n]) for n in sorted(SIZES, reverse=True) for nm in ("B", "A", "D", "C") for s in SEEDS]
    with Pool(workers) as pool:
        for i, (p, sec) in enumerate(pool.imap_unordered(do_job, jobs), 1):
            print(f"[{i}/{len(jobs)}] {os.path.basename(p)} {sec:.0f} s (elapsed {time.perf_counter() - t0:.0f} s)", flush=True)
    lines = analyse()
    lines.append(f"total wall time this session {time.perf_counter() - t0:.0f} s")
    print("\n".join(lines))
    open("c3g_run1.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
