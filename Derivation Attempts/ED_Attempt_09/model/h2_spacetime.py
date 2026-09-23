"""H2 step 1: the grown spacetime of H1's conditions-only slices (note 5; D8; A7 D40).

Attempt 7 decided (D40) that the grown spacetime is what gets judged, not the slice alone. H1 judged
slices. This re-grows H1's slices at n = 24 and 32 exactly (the port's generator is seeded), keeps
the last KEEP ticks, builds the spacetime - in-slice links plus each event's link forward to its
children and to whatever absorbed it - and reads its mass dimension by ball growth, the same reading
attempts 7 and 8 used.

CALIBRATION, run first: a flat spacetime - KEEP + 1 copies of the flat slice, each event linked only
to itself in the next copy ("nothing happened"). Ball growth under-reads (a flat slice reads 2.66,
not 3), so the flat spacetime's own reading, not the ideal 4, is the reference.

Expected results, written down before this run:
  S-0  the flat spacetime reads a defined mass dimension at both sizes, with at least three radii.
  S-1  every re-grown slice matches its H1 run exactly (events and links).
  S-2  THE HONEST EXPECTATION: the shortcuts in the slices carry into the spacetime, so the
       conditions-only spacetime reads at least 1.0 above the flat spacetime at the same size.
Fixed from the calibration before any grown spacetime is read:
  a grown spacetime READS 3+1 if its mass dimension is within 0.5 of the flat spacetime's at that
  size; otherwise it does not.
For comparison, already on record at n = 24/32: attempt 7 C3g 5.5-6.4; attempt 8 E4 with the veto
5.68-6.42, without it 6.65-6.94.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ED_Attempt_08", "model"))

from p3 import Slice3P                                        # noqa: E402
from p3_core import SIGMA, FLAT_LINKS_PER_EVENT, CEILING      # noqa: E402

SIZES = (24, 32)
SEEDS = (0, 1)
T = 150
KEEP = 20
OUT = "h2_runs"
MARGIN = 0.5


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    os.replace(tmp, path)


def calibrate(n):
    path = os.path.join(OUT, "cal_flat_n%d.json" % n)
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    from p3_readings import spacetime_readings
    M = Slice3P(n)
    e = M.edges()
    ids = M.vertices()
    kids = np.stack([ids, ids], axis=1).astype(np.int32)
    empty = np.zeros((0, 2), np.int32)
    snaps = [(e, kids, empty) for _ in range(KEEP)] + [(e, empty, empty)]
    t0 = time.perf_counter()
    st = spacetime_readings(snaps, 4000)
    st["seconds"] = time.perf_counter() - t0
    dump(path, st)
    return st


def do_job(job):
    n, s = job
    path = os.path.join(OUT, "n%d_s%d.json" % (n, s))
    if os.path.exists(path):
        return path, 0.0
    from p3_readings import spacetime_readings
    t0 = time.perf_counter()
    M = Slice3P(n)
    M.seed(s)
    V0 = M.V
    rng = np.random.default_rng(s)
    M.S.b[:V0] = 1.0
    M.S.omega[:V0] = 1.0 + SIGMA * rng.standard_normal(V0)
    M.S.phi[:V0] = 0.0
    pool = round(FLAT_LINKS_PER_EVENT * V0) - M.E
    snaps = []
    for t in range(1, T + 1):
        e = M.edges() if t > T - KEEP else None
        r, pool, kids, absd = M.tick(0.0, 0.0, pool, s_max=None, cap=CEILING)
        if e is not None:
            snaps.append((e, kids.copy(), absd.copy()))
    snaps.append((M.edges(), np.zeros((0, 2), np.int32), np.zeros((0, 2), np.int32)))
    ref = json.load(open(os.path.join("h1_runs", "n%d_s%d.json" % (n, s)), encoding="utf-8"))
    same = (M.V == ref["events"] and M.E == ref["links"])
    st = spacetime_readings(snaps, 4000 + s)
    res = dict(n=n, seed=s, matches_h1=bool(same), events=M.V, links=M.E, spacetime=st,
               seconds=time.perf_counter() - t0)
    dump(path, res)
    return path, res["seconds"]


def main():
    os.makedirs(OUT, exist_ok=True)
    cal = {}
    for n in SIZES:
        c = calibrate(n)
        cal[n] = c
        print("flat spacetime n=%d: d_H %s radii %s-%s events %s (%.0f s)"
              % (n, c.get("d_H"), c.get("r_lo"), c.get("r_max"), c.get("events"), c.get("seconds", 0)), flush=True)
    t0 = time.perf_counter()
    with Pool(2) as pool:
        for path, sec in pool.imap_unordered(do_job, [(n, s) for n in SIZES for s in SEEDS]):
            print("  %s %.0f s (elapsed %.2f h)" % (os.path.basename(path), sec, (time.perf_counter() - t0) / 3600), flush=True)
    L = ["H2 step 1: the grown spacetime of H1's conditions-only slices", ""]
    for n in SIZES:
        f = cal[n].get("d_H")
        L.append("  n=%d flat spacetime d_H %s (radii %s-%s) -> reads 3+1 if within %.1f of it"
                 % (n, "%.3f" % f if f else None, cal[n].get("r_lo"), cal[n].get("r_max"), MARGIN))
        for s in SEEDS:
            r = json.load(open(os.path.join(OUT, "n%d_s%d.json" % (n, s)), encoding="utf-8"))
            d = r["spacetime"].get("d_H")
            verdict = "-" if (d is None or f is None) else ("READS 3+1" if abs(d - f) <= MARGIN else "does not (%+.2f)" % (d - f))
            L.append("    seed %d: matches H1 %s | events %s | d_H %s radii %s-%s | %s"
                     % (s, r["matches_h1"], r["spacetime"].get("events"), "%.3f" % d if d else None,
                        r["spacetime"].get("r_lo"), r["spacetime"].get("r_max"), verdict))
    L.append("")
    L.append("  on record for comparison: A7 C3g 5.5-6.4; A8 E4 veto 5.68-6.42, no veto 6.65-6.94")
    text = "\n".join(L)
    print(text)
    with open("h2_spacetime.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
