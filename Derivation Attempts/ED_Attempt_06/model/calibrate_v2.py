"""Calibration run 2, with readings v2 (Allen D14; fix and held-out patterns set in note 12 / C65).

Expected results, written down before the first run (note 11's E0 ranges by
dimension class; the two held-out patterns were not used in choosing the fix):
  3D class (3D periodic random geometric graph mean 12; 3D periodic cubic grid
  25^3; HELD-OUT 3D periodic random geometric graph mean 8, construction seed 11):
      d_H and d_s in [2.6, 3.4], d_w in [1.8, 2.2], beta in [0.55, 0.78].
  2D class (2D periodic random geometric graph mean 8; HELD-OUT 2D periodic
  square grid 126 x 126): d_H and d_s in [1.7, 2.3], d_w in [1.8, 2.2].
  Small world (random 12-regular graph): small-world flag raised.
  All six must be as expected for E0 to be met.
Flag recorded before the run (note 12): by the diagnostic's local slopes the
3D random pattern (mean 12) walk dimension may sit at the 2.2 edge.
The first four patterns are built with the same seeds and order as run 1.
"""
import json
import time
import numpy as np
import scipy.sparse as sp
from calibrate import rgg, cubic_grid, random_regular, to_csr, within
from readings_v2 import all_readings


def square_grid(L):
    idx = np.arange(L * L).reshape(L, L)
    pairs = [np.stack([idx.ravel(), np.roll(idx, -1, axis=ax).ravel()], axis=1) for ax in range(2)]
    return to_csr(L * L, np.concatenate(pairs)), L * L


def main():
    rng_build = np.random.default_rng(1)
    rng_hold = np.random.default_rng(11)
    rng_read = np.random.default_rng(2)
    builds = [
        ("3D random geometric (mean 12)", lambda: rgg(16000, 3, 12, rng_build), "3d"),
        ("3D cubic grid 25^3", lambda: cubic_grid(25), "3d"),
        ("2D random geometric (mean 8)", lambda: rgg(16000, 2, 8, rng_build), "2d"),
        ("random 12-regular", lambda: random_regular(16000, 12, rng_build), "rr"),
        ("HELD-OUT 3D random geometric (mean 8, seed 11)", lambda: rgg(16000, 3, 8, rng_hold), "3d"),
        ("HELD-OUT 2D square grid 126^2", lambda: square_grid(126), "2d"),
    ]
    results, lines, ok_all = {}, [], True
    for name, build, kind in builds:
        t0 = time.perf_counter()
        A, size = build()
        r = all_readings(A, rng_read)
        r["component_size"] = size
        r["seconds"] = round(time.perf_counter() - t0, 1)
        if kind == "3d":
            ok = (within(r["d_H"], 2.6, 3.4) and within(r["d_s"], 2.6, 3.4)
                  and within(r["d_w"], 1.8, 2.2) and within(r["beta"], 0.55, 0.78))
        elif kind == "2d":
            ok = within(r["d_H"], 1.7, 2.3) and within(r["d_s"], 1.7, 2.3) and within(r["d_w"], 1.8, 2.2)
        else:
            ok = bool(r["small_world"])
        ok_all &= ok
        results[name] = {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in r.items()}
        line = (f"{name}: {'AS EXPECTED' if ok else 'NOT AS EXPECTED'}  N={r['N']} (component {size}), "
                f"mean degree={r['mean_degree']:.3f}, radii {r['r_lo']}..{r['r_max']}, d_H={r['d_H']:.3f}, "
                f"beta={r['beta']:.3f}, d_s={r['d_s']:.3f}, d_w={r['d_w']:.3f}, R5={r['R5']:.3f}, "
                f"small_world={r['small_world']}, walk window t={r['t_start']}..{r['t_end']} "
                f"(capped {r['t_capped']}), {r['seconds']} s")
        print(line, flush=True)
        lines.append(line)
    verdict = "E0 (run 2): ALL AS EXPECTED" if ok_all else "E0 (run 2): SOME NOT AS EXPECTED (exit rule X0 still applies)"
    print(verdict)
    lines.append(verdict)
    with open("calibration_run2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open("calibration_run2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == "__main__":
    main()
