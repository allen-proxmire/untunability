"""C2a run 2: fresh-seed retest of the revised balance check (D9, D10; note 7, C19).

Revision (recorded, revise-and-retest): E2's offspring measure is the telescoped
(geometric-mean) ratio exp[(ln L_(T-1) - ln L_(T/2)) / (T - 1 - T/2)], replacing
run 1's average of L_(t+1)/L_t, which fluctuations bias upward (C17). Nothing
else changes: same rule, settings, sizes, readings and exit rule as run 1.
Fresh seeds: balance runs 20-39 per setting (run 1 used 0-19); geometry runs
seeds 103-105 (run 1 used 100-102).

Expected results, written down before the first run:
  E1  structure exact and budget conserved (to 1e-9 relative) in every run.
  E2  reading B, k = 0.5, 1, 1.5, both L* (100, 200): >= 19 of 20 seeds survive;
      median telescoped offspring (slices T/2..T-1) in [0.98, 1.02]; median mean
      slice length within +-10% of L*.
  E3  reading B, k = 2.5: fails E2 in a majority of seeds at both L* (a seed
      fails if it dies, runs away, or its mean slice length is outside +-10%).
  E4  reading A, k = 0.5 and 1, L* = 200: a majority of seeds die or run away.
  E5  reading B geometry, k = 0.5, 1, 1.5, L* = 200, T = 200, 3 seeds: median
      d_H in [1.7, 2.3], median d_s <= 2.3, structure exact.
Exit rule (note 6, D7, with D9's revised E2): pass on E1, E2, E5 confirms C19's
record "the balance self-organizes from ED's budget passed forward and conserved:
consistent, not derived; k and L* are knobs; space settles as a fixed-size tube,
and growth would need budget creation (the cosmic excess, inherited)"; E3/E4 not
as expected are stability findings, not blocking; E2 or E5 failing means the
revised check does not hold on fresh seeds, recorded, and C19 goes back to Allen;
E1 failing is a code bug.
"""
import json
import time
import numpy as np
from c2a import grow_budget, balance_stats
from c1 import build
from readings_v2 import all_readings


def main():
    t0 = time.perf_counter()
    lines, out = [], {"balance": [], "geometry": []}
    T = 400
    e1 = True
    settings = [("B", k, Ls) for k in (0.5, 1.0, 1.5, 2.5) for Ls in (100, 200)] + [("A", k, 200) for k in (0.5, 1.0)]
    res = {}
    for reading, k, Ls in settings:
        rows = []
        for s in range(20, 40):
            g = grow_budget(T, Ls, k, s, reading)
            if reading == "B" and not g["budget_ok"]:
                e1 = False
            ml = balance_stats(g["lengths"], T)[1]
            Lg = np.array(g["lengths"], float)
            mo = float(np.exp((np.log(Lg[T - 1]) - np.log(Lg[T // 2])) / (T - 1 - T // 2))) if g["status"] == "survived" else float("nan")
            rows.append(dict(seed=s, status=g["status"], mean_offspring=mo, mean_length=ml, final=g["lengths"][-1]))
        res[(reading, k, Ls)] = rows
        out["balance"].append(dict(reading=reading, k=k, Lstar=Ls, runs=rows))
        surv = sum(r["status"] == "survived" for r in rows)
        mo = np.nanmedian([r["mean_offspring"] for r in rows]) if surv else float("nan")
        ml = np.nanmedian([r["mean_length"] for r in rows]) if surv else float("nan")
        lines.append(f"reading {reading} k={k} L*={Ls}: survived {surv}/20 (died {sum(r['status']=='died' for r in rows)}, ran away {sum(r['status']=='ran away' for r in rows)}); median telescoped offspring {mo:.4f}; median mean length {ml:.1f} ({ml/Ls:.3f} of L*)")
        print(lines[-1], flush=True)

    def seed_ok(r, Ls):
        return r["status"] == "survived" and abs(r["mean_length"] / Ls - 1) <= 0.10

    e2 = all(sum(r["status"] == "survived" for r in res[("B", k, Ls)]) >= 19
             and 0.98 <= np.nanmedian([r["mean_offspring"] for r in res[("B", k, Ls)]]) <= 1.02
             and abs(np.nanmedian([r["mean_length"] for r in res[("B", k, Ls)]]) / Ls - 1) <= 0.10
             for k in (0.5, 1.0, 1.5) for Ls in (100, 200))
    e3 = all(sum(not seed_ok(r, Ls) for r in res[("B", 2.5, Ls)]) >= 11 for Ls in (100, 200))
    e4 = all(sum(r["status"] in ("died", "ran away") for r in res[("A", k, 200)]) >= 11 for k in (0.5, 1.0))

    geo = []
    for k in (0.5, 1.0, 1.5):
        for s in range(3, 6):
            t1 = time.perf_counter()
            g = grow_budget(200, 200, k, 100 + s, "B", keep_offspring=True)
            if g["status"] != "survived":
                geo.append(dict(k=k, seed=100 + s, status=g["status"]))
                lines.append(f"  geometry k={k} seed {100+s}: {g['status']} (no readings)")
                print(lines[-1], flush=True)
                continue
            A, ok, notes = build(g["lengths"], g["offspring"])
            notes = [n for n in notes if not n.startswith("parent links")]
            ok_struct = len(notes) == 0
            if not (ok_struct and g["budget_ok"]):
                e1 = False
            r = all_readings(A, np.random.default_rng(2000 + 10 * s + int(k * 10)))
            geo.append(dict(k=k, seed=100 + s, status="survived", events=int(A.shape[0]), structure_ok=ok_struct,
                            d_H=float(r["d_H"]), d_s=float(r["d_s"]), d_w=float(r["d_w"]), r_lo=r["r_lo"], r_max=r["r_max"]))
            lines.append(f"  geometry k={k} seed {100+s}: {A.shape[0]} events, structure {'exact' if ok_struct else notes}, d_H={r['d_H']:.3f}, d_s={r['d_s']:.3f}, d_w={r['d_w']:.3f}, radii {r['r_lo']}..{r['r_max']} ({time.perf_counter()-t1:.0f} s)")
            print(lines[-1], flush=True)
    out["geometry"] = geo
    okg = [x for x in geo if x["status"] == "survived"]
    med = lambda key: float(np.nanmedian([x[key] for x in okg])) if okg else float("nan")
    e5 = (len(okg) == 9 and all(x["structure_ok"] for x in okg)
          and all(1.7 <= np.nanmedian([x["d_H"] for x in okg if x["k"] == k]) <= 2.3
                  and np.nanmedian([x["d_s"] for x in okg if x["k"] == k]) <= 2.3 for k in (0.5, 1.0, 1.5)))
    for name, v in (("E1 structure exact, budget conserved", e1), ("E2 reading B balance (telescoped), k=0.5,1,1.5", e2),
                    ("E3 reading B k=2.5 fails in majority", e3), ("E4 reading A dies or runs away in majority", e4),
                    (f"E5 geometry (overall medians d_H {med('d_H'):.3f}, d_s {med('d_s'):.3f}, d_w {med('d_w'):.3f})", e5)):
        lines.append(f"{name}: {'AS EXPECTED' if v else 'NOT AS EXPECTED'}")
    if not e1:
        verdict = "E1 failed: code bug; fix and rerun (recorded)."
    elif e2 and e5:
        verdict = ("PASS (revised check confirmed on fresh seeds): the balance self-organizes from ED's budget passed forward and conserved: consistent, not derived; "
                   "k and L* are knobs; space settles as a fixed-size tube, and growth would need budget creation (the cosmic excess, inherited).")
    else:
        verdict = "Revised check not confirmed on fresh seeds (E2 or E5 not met); recorded; C19 goes back to Allen."
    lines.append("EXIT: " + verdict)
    lines.append(f"total {time.perf_counter()-t0:.0f} s")
    print("\n".join(lines[-7:]))
    with open("c2a_run2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open("c2a_run2.json", "w", encoding="utf-8") as f:
        json.dump(out, f, default=str)


if __name__ == "__main__":
    main()
