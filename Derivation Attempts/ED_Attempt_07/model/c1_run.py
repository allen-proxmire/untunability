"""C1 runs (note 3, D3; IMPLEMENTATION_NOTES.md).

Expected results, written down before the first run (note 3):
  F0  flat calibration: d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2].
  E1  structure exact in every tree run and every slice.
  E2  slice length: least-squares slope of mean L_t (1,000 seeds) against t for t = 10..199 in [1.8, 2.2].
  E3  median d_H over 10 tree seeds in [1.7, 2.3].
  E4  median d_s over 10 tree seeds <= 2.3.
  E5  d_w reported; median >= 1.8.
Exit rule (note 2/3, confirmed D3): pass records "C1: ED's causal growth with no
splitting reproduces 2D CDT: the causal half checked"; E1 failure = code bug;
F0 failure = fix readings for this pattern type; F0 pass with E2-E4 miss =
"C1 not reproduced"; the growth rule is not changed after results.

Usage: python c1_run.py
"""
import json
import time
import numpy as np
from c1 import grow, slice_lengths, build
from readings_v2 import all_readings

T = 200


def within(x, lo, hi):
    return bool(np.isfinite(x) and lo <= x <= hi)


def main():
    out = {}
    lines = []
    t0 = time.perf_counter()

    # F0: flat calibration (structure of the flat strip: in-slice cycles and forward identity only)
    lengths, offspring = grow(T, seed=0, flat_L=200)
    A, ok_flat, notes_flat = build(lengths, offspring)
    notes_flat = [n for n in notes_flat if not n.startswith("parent links")]
    rf = all_readings(A, np.random.default_rng(999))
    f0 = within(rf["d_H"], 1.7, 2.3) and within(rf["d_s"], 1.7, 2.3) and within(rf["d_w"], 1.8, 2.2)
    lines.append(f"F0 flat strip ({A.shape[0]} events): {'AS EXPECTED' if f0 else 'NOT AS EXPECTED'}  d_H={rf['d_H']:.3f}, d_s={rf['d_s']:.3f}, d_w={rf['d_w']:.3f}, beta={rf['beta']:.3f}, radii {rf['r_lo']}..{rf['r_max']}, structure notes: {notes_flat or 'none'}  ({time.perf_counter()-t0:.0f} s)")
    out["F0"] = {k: (v if not isinstance(v, np.floating) else float(v)) for k, v in rf.items()}
    print(lines[-1], flush=True)

    # E2: slice length over 1,000 seeds
    t1 = time.perf_counter()
    Ls = np.array([slice_lengths(T, s) for s in range(1000)], dtype=float)
    meanL = Ls.mean(axis=0)
    tt = np.arange(T)
    sel = tt >= 10
    slope, intercept = np.polyfit(tt[sel], meanL[sel], 1)
    e2 = 1.8 <= slope <= 2.2
    lines.append(f"E2 slice length (1,000 seeds): {'AS EXPECTED' if e2 else 'NOT AS EXPECTED'}  slope={slope:.3f}, intercept={intercept:.2f}; mean L at t=50,100,199: {meanL[50]:.1f}, {meanL[100]:.1f}, {meanL[199]:.1f} (1+2t: 101, 201, 399)  ({time.perf_counter()-t1:.0f} s)")
    out["E2"] = dict(slope=float(slope), intercept=float(intercept), meanL=meanL.tolist())
    print(lines[-1], flush=True)

    # E1, E3-E5: ten seeds with readings
    runs = []
    all_ok = True
    for s in range(10):
        t2 = time.perf_counter()
        lengths, offspring = grow(T, seed=s)
        A, ok, notes = build(lengths, offspring)
        all_ok &= ok
        r = all_readings(A, np.random.default_rng(1000 + s))
        runs.append(dict(seed=s, events=int(A.shape[0]), structure_ok=bool(ok), notes=notes,
                         d_H=float(r["d_H"]), d_s=float(r["d_s"]), d_w=float(r["d_w"]), beta=float(r["beta"]),
                         R5=float(r["R5"]), r_lo=r["r_lo"], r_max=r["r_max"], small_world=bool(r["small_world"]),
                         t_capped=bool(r["t_capped"])))
        print(f"  seed {s}: {A.shape[0]} events, structure {'exact' if ok else 'FAILED ' + str(notes)}, d_H={r['d_H']:.3f}, d_s={r['d_s']:.3f}, d_w={r['d_w']:.3f}, radii {r['r_lo']}..{r['r_max']}  ({time.perf_counter()-t2:.0f} s)", flush=True)
    out["runs"] = runs
    med = lambda k: float(np.nanmedian([x[k] for x in runs]))
    e1 = all_ok
    e3 = within(med("d_H"), 1.7, 2.3)
    e4 = np.isfinite(med("d_s")) and med("d_s") <= 2.3
    e5 = np.isfinite(med("d_w")) and med("d_w") >= 1.8
    lines.append(f"E1 structure exact in all 10 runs: {'AS EXPECTED' if e1 else 'NOT AS EXPECTED'}")
    lines.append(f"E3 median d_H = {med('d_H'):.3f}: {'AS EXPECTED' if e3 else 'NOT AS EXPECTED'}")
    lines.append(f"E4 median d_s = {med('d_s'):.3f}: {'AS EXPECTED' if e4 else 'NOT AS EXPECTED'}")
    lines.append(f"E5 median d_w = {med('d_w'):.3f} (reported; >= 1.8): {'AS EXPECTED' if e5 else 'NOT AS EXPECTED'}")

    if not e1:
        verdict = "E1 failed: code bug; fix and rerun (recorded)."
    elif not f0:
        verdict = "F0 failed: readings do not suit this pattern type; fix readings, rerun calibration then tree (recorded)."
    elif e2 and e3 and e4:
        verdict = "PASS: C1: ED's causal growth with no splitting reproduces 2D CDT: the causal half checked."
    else:
        verdict = "C1 not reproduced (F0 passed, E2-E4 missed): examine why; growth rule unchanged."
    lines.append("EXIT: " + verdict)
    lines.append(f"total {time.perf_counter()-t0:.0f} s")
    text = "\n".join(lines)
    print(text)
    with open("c1_run1.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    with open("c1_run1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, default=str)


if __name__ == "__main__":
    main()
