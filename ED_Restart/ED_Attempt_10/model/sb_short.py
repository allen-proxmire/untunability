"""Short-loop diagnostic (note 17 option (a); Allen: 'a, run the short-loop test').

Same sampler and rules as sb_run.py, with T = 4 slices instead of 32, n = 12, both starts (flat reference; crowded_grown),
1,000 sweeps each (sweep = V x T proposals, about 3.3 s), readings every 20 sweeps: mean slice distance over all 4 slices,
degree sd, max degree. Checks: counts every sweep, structure and full replay every 20 sweeps.

Written before running. Start values: flat 5.85, crowded 3.63.
  MEET     last-fifth means of the two starts within 5 per cent of each other -> 'the starts meet with short loops';
           then where: mean >= 5.0 'near flat', <= 4.2 'near crowded', else 'between'.
  MOVING   not met, but the gap between them shrank by >= 50 per cent -> 'moving toward each other, not yet met'.
  PARTIAL  gap shrank by 10-50 per cent -> 'slow movement'.
  FROZEN   gap shrank by < 10 per cent -> 'frozen even with short loops: the moves themselves cannot reshape a history at
           this rate'; take stock.
  Any check failure -> code problem.
RERUN (D18): with PG = 0.3, the whole-history move (the same bundle applied to every slice; exact on rings with it) is
added; same outcome rules; outputs in sb_short_runs_global/ and sb_short_global.txt. Rerun expectation (Claude, low
confidence): PARTIAL at most - global moves get through only a few per sweep at n = 12.
Original expectation (Claude, low confidence): MOVING or MEET, because a 4-slice loop can shift as a whole far faster; where they
meet, no expectation stronger than a coin toss.
"""
import json
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PG = float(os.environ.get("PG", "0"))
OUT = os.path.join(HERE, "sb_short_runs" + ("_global" if PG > 0 else ""))
T = 4
SWEEPS = 1000
EVERY = 20


def readings(H, seed):
    import sa_count as sc
    mds, sds, mx = [], [], []
    for t in range(H.T):
        M = H.S[t]
        mds.append(sc.mean_distance(M.adjacency()[0], seed + t))
        d = [int(M.S.v_nl[v]) for v in M.vertices()]
        sds.append(float(np.std(d)))
        mx.append(int(max(d)))
    return dict(md=float(np.mean(mds)), deg_sd=float(np.mean(sds)), deg_max=int(max(mx)), ticks=[len(x) for x in H.tau])


def do_job(start):
    path = os.path.join(OUT, "%s.json" % start)
    import sb_build as b
    from sb_core import History
    from sb_3d import Ops3D
    t0 = time.perf_counter()
    F = b.flat_reference(12)
    base = F if start == "flat" else b.crowded_grown(F)
    ops = Ops3D()
    H = History([ops.copy(base) for _ in range(T)], ops, int(round(0.1 * base.V)), 77)
    H.p_global = PG
    V0, E0 = base.V, base.E
    rec = dict(start=start, V=V0, E=E0, T=T, readings=[dict(sweep=0, **readings(H, 0))], fails=[])
    for sw in range(1, SWEEPS + 1):
        for _ in range(V0 * T):
            H.step()
        if any(S.V != V0 or S.E != E0 for S in H.S):
            rec["fails"].append((sw, "counts"))
        if sw % EVERY == 0:
            if any(S.check() for S in H.S):
                rec["fails"].append((sw, "structure"))
            ok, t, why = H.replay_ok()
            if not ok:
                rec["fails"].append((sw, "replay", t, str(why)))
            r = readings(H, sw)
            r.update(sweep=sw, acceptance=H.acc / H.tried, hours=(time.perf_counter() - t0) / 3600,
                     global_accepted=getattr(H, "acc_global", 0))
            rec["readings"].append(r)
            json.dump(rec, open(path, "w"))
        if rec["fails"]:
            break
    rec["done"] = True
    json.dump(rec, open(path, "w"))
    return path


def report():
    R = {s: json.load(open(os.path.join(OUT, "%s.json" % s))) for s in ("flat", "crowded")}
    L = []
    tail = {}
    for s, r in R.items():
        rd = r["readings"]
        k = max(1, (len(rd) - 1) // 5)
        tail[s] = float(np.mean([x["md"] for x in rd[-k:]]))
        L.append("%-7s md %.3f -> last-fifth %.3f | deg sd %.2f -> %.2f | max deg %d | acc %.3f | fails %s" % (
            s, rd[0]["md"], tail[s], rd[0]["deg_sd"], rd[-1]["deg_sd"], rd[-1]["deg_max"], rd[-1].get("acceptance", 0),
            r["fails"]))
        L.append("    md: " + " ".join("%d:%.2f" % (x["sweep"], x["md"]) for x in rd[::5]))
    g0 = R["flat"]["readings"][0]["md"] - R["crowded"]["readings"][0]["md"]
    g1 = tail["flat"] - tail["crowded"]
    shrink = 1 - g1 / g0
    mean = (tail["flat"] + tail["crowded"]) / 2
    L.append("gap %.3f -> %.3f (shrank %.1f per cent)" % (g0, g1, 100 * shrink))
    if any(r["fails"] for r in R.values()):
        v = "a check failed - code problem"
    elif abs(g1) / mean <= 0.05:
        v = "MEET: the starts meet with short loops, %s (mean %.2f)" % (
            "near flat" if mean >= 5.0 else "near crowded" if mean <= 4.2 else "between", mean)
    elif shrink >= 0.5:
        v = "MOVING: toward each other, not yet met"
    elif shrink >= 0.1:
        v = "PARTIAL: slow movement"
    else:
        v = "FROZEN: even with short loops, the moves cannot reshape a history at this rate"
    L.append("VERDICT: " + v)
    text = "\n".join(L)
    open(os.path.join(HERE, "sb_short%s.txt" % ("_global" if PG > 0 else "")), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    with Pool(2) as p:
        for path in p.imap_unordered(do_job, ["flat", "crowded"]):
            print("  done", path, flush=True)
    report()
