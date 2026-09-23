"""Stage B runs (notes 7, 14, 16; Allen D16: 'a, build the crowded start then run it').

History sampler (sb_core + sb_3d, gates G1 and G2 passed), narrow moves, T = 32 periodic slices, every slice exactly the
start's event and link counts, cap round(0.1 V) changes per tick. Runs: n = 12 and 16, starts 'flat' (flat reference at
ED's density) and 'crowded' (crowded_grown: an A9-style small world at the same exact counts). Sweep = V x T proposals.

Recorded revisions before this run (from G3, note 16 and after): the crowded start is crowded_grown (G3 run 2: growth-rate
gap 0.210, spacetime gap at 16 = 1.278); at n = 12 the crowded stack's spacetime reading is undefined (too small across), so
the spacetime reading is judged at n = 16 only, and n = 12 serves the growth rate; readings every 10 sweeps (note 7 said
50, too sparse for the sweep budget); sweep budget fixed here: 300 at n = 12 (about 2.3 h), 200 at n = 16 (about 3.6 h).

Readings every 10 sweeps: slice mean distance averaged over 8 slices (every 4th), degree sd, max degree, tick sizes.
At the end: growth rate ln(md16/md12)/ln(V16/V12) per start, from the mean of the last third's readings; spacetime reading
(A9's ball growth) on 16 consecutive slices with the recorded parent links, at n = 16.
Settled: over the last third of readings, (max - min) / mean of the slice mean distance <= 0.05.
Checks throughout (G2 continued): counts every sweep; structure of all slices and full replay every 10 sweeps.

Pass (note 7, unchanged): growth rate within 0.05 of the flat stack's (0.327); spacetime (n = 16) within 0.5 of the flat
stack's (3.562); both starts agree (growth rates within 0.05, spacetime within 0.3).
Other outcomes (note 7): both starts end as small worlds -> 'counting whole histories with ED's rules gives small worlds',
take stock; starts disagree -> 'not settled, or the sampler does not reach every history', longer runs then take stock;
both between -> reported as it reads, take stock. Any check failure -> code problem, stop.
Expectation (Claude, low confidence): near a coin toss, leaning flat.
"""
import json
import math
import os
import sys
import time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "sb_runs")
T = 32
BUDGET = {12: 300, 16: 200}
EVERY = 10
JOBS = [(12, "flat"), (12, "crowded"), (16, "flat"), (16, "crowded")]


def readings(H, seed):
    import sa_count as sc
    mds, sds, mx = [], [], []
    for t in range(0, H.T, 4):
        M = H.S[t]
        mds.append(sc.mean_distance(M.adjacency()[0], seed + t))
        d = [int(M.S.v_nl[v]) for v in M.vertices()]
        sds.append(float(np.std(d)))
        mx.append(int(max(d)))
    return dict(md=float(np.mean(mds)), md_slices=mds, deg_sd=float(np.mean(sds)), deg_max=int(max(mx)),
                ticks=[len(x) for x in H.tau])


def spacetime(H, start=0, span=16, seed=7):
    from p3_readings import spacetime_readings
    snaps = []
    for i in range(span):
        t = (start + i) % H.T
        M = H.S[t]
        kids, absd = [], []
        merged = set()
        for k in H.tau[t]:
            if k[0] == "S":
                kids.append((k[1], k[3]))
            elif k[0] == "M":
                absd.append((k[1], k[2]))
                merged.add(k[1])
        for v in M.vertices():
            v = int(v)
            if v not in merged:
                kids.append((v, v))
        snaps.append((M.edges(), np.array(kids, dtype=np.int32), np.array(absd, dtype=np.int32).reshape(-1, 2)))
    return spacetime_readings(snaps, seed).get("d_H")


def do_job(job):
    n, start = job
    path = os.path.join(OUT, "n%d_%s.json" % (n, start))
    if os.path.exists(path) and json.load(open(path)).get("done"):
        return path, 0.0
    import sb_build as b
    from sb_core import History
    from sb_3d import Ops3D
    t0 = time.perf_counter()
    F = b.flat_reference(n)
    base = F if start == "flat" else b.crowded_grown(F)
    ops = Ops3D()
    H = History([ops.copy(base) for _ in range(T)], ops, int(round(0.1 * base.V)), 1000 + n)
    V0, E0 = base.V, base.E
    per = V0 * T
    rec = dict(n=n, start=start, V=V0, E=E0, T=T, budget=BUDGET[n], readings=[], fails=[])
    rec["readings"].append(dict(sweep=0, **readings(H, 0)))
    json.dump(rec, open(path, "w"))
    for sw in range(1, BUDGET[n] + 1):
        for _ in range(per):
            H.step()
        bad = [t for t, S in enumerate(H.S) if S.V != V0 or S.E != E0]
        if bad:
            rec["fails"].append((sw, "counts", bad[:3]))
        if sw % EVERY == 0:
            for t, S in enumerate(H.S):
                if S.check():
                    rec["fails"].append((sw, "structure", t))
                    break
            ok, t, why = H.replay_ok()
            if not ok:
                rec["fails"].append((sw, "replay", t, str(why)))
            r = readings(H, sw)
            r.update(sweep=sw, acceptance=H.acc / H.tried, hours=(time.perf_counter() - t0) / 3600)
            rec["readings"].append(r)
            json.dump(rec, open(path, "w"))
        if rec["fails"]:
            break
    if n == 16 and not rec["fails"]:
        rec["spacetime"] = spacetime(H)
    rec["done"] = True
    rec["hours"] = (time.perf_counter() - t0) / 3600
    json.dump(rec, open(path, "w"))
    return path, rec["hours"]


def verdict():
    R = {}
    for n, st in JOBS:
        p = os.path.join(OUT, "n%d_%s.json" % (n, st))
        if os.path.exists(p):
            R[(n, st)] = json.load(open(p))
    L = []
    last = {}
    for (n, st), r in R.items():
        rd = [x for x in r["readings"] if x["sweep"] > 0]
        k = max(1, len(rd) // 3)
        tail = [x["md"] for x in rd[-k:]]
        m = float(np.mean(tail)) if tail else float("nan")
        settled = bool(tail) and (max(tail) - min(tail)) / m <= 0.05
        last[(n, st)] = (m, settled)
        L.append("n%d %-7s V %d: md start %.3f -> last-third mean %.3f (settled %s) | deg sd %.2f max %d | acc %.3f | "
                 "spacetime %s | fails %s | done %s" % (n, st, r["V"], r["readings"][0]["md"], m, settled,
                                                        rd[-1]["deg_sd"] if rd else float("nan"),
                                                        rd[-1]["deg_max"] if rd else -1,
                                                        rd[-1]["acceptance"] if rd else float("nan"),
                                                        r.get("spacetime"), r["fails"], r.get("done")))
        L.append("    md by sweep: " + " ".join("%d:%.2f" % (x["sweep"], x["md"]) for x in r["readings"]))
    if len(R) == 4 and all(r.get("done") for r in R.values()):
        rate = {}
        for st in ("flat", "crowded"):
            rate[st] = math.log(last[(16, st)][0] / last[(12, st)][0]) / math.log(R[(16, st)]["V"] / R[(12, st)]["V"])
        stt = {st: R[(16, st)].get("spacetime") for st in ("flat", "crowded")}
        L.append("growth rate flat %.3f crowded %.3f (flat stack 0.327; small worlds about 0.12-0.15)"
                 % (rate["flat"], rate["crowded"]))
        L.append("spacetime n16 flat %s crowded %s (flat stack 3.562)" % (stt["flat"], stt["crowded"]))
        settled = all(v[1] for v in last.values())
        fails = any(r["fails"] for r in R.values())
        ok_rate = all(abs(rate[s] - 0.327) <= 0.05 for s in rate)
        ok_st = all(stt[s] is not None and abs(stt[s] - 3.562) <= 0.5 for s in stt)
        agree = (abs(rate["flat"] - rate["crowded"]) <= 0.05 and stt["flat"] is not None
                 and stt["crowded"] is not None and abs(stt["flat"] - stt["crowded"]) <= 0.3)
        if fails:
            v = "a check failed - code problem"
        elif ok_rate and ok_st and agree:
            v = "PASS: counting whole histories gives extended 3D space from both starts"
        elif not agree:
            v = "starts disagree: not settled, or the sampler does not reach every history (settled flags: %s)" % settled
        elif all(rate[s] < 0.2 for s in rate):
            v = "both starts end as small worlds: counting whole histories with ED's rules gives small worlds"
        else:
            v = "both between flat and small world: reported as it reads"
        L.append("VERDICT: " + v)
    text = "\n".join(L)
    open(os.path.join(HERE, "sb_run.txt"), "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    if "--report" in sys.argv:
        verdict()
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p:
        for path, h in p.imap_unordered(do_job, JOBS):
            print("  %s %.2f h" % (os.path.basename(path), h), flush=True)
    verdict()
