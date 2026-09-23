"""The one n = 52 spacetime reading, run alone after the growth runs (D9).

E4-5 asked for the grown spacetime's mass dimension at every size. At n = 52 a single reading needs
about 6.5 GB - 200 centres x 3.26 million events x 8 bytes for the distance array, plus the slice and
the sparse matrix - on a machine with 8.4 GB, so it cannot run alongside anything. This reads the one
saved seed, alone. If it still runs out of memory, that is recorded as the answer: E4-5 is not
measurable at n = 52 on this machine, and the slice readings (E4-3) stand on their own.
"""
import json
import os
import time
import numpy as np
from p3_readings import spacetime_readings

OUT = "e4_runs"
N, SEED = 52, 0


def main():
    p = os.path.join(OUT, "snaps_n%d_s%d.npz" % (N, SEED))
    if not os.path.exists(p):
        print("no saved slices at %s" % p)
        return 2
    z = np.load(p)
    k = int(z["n_snaps"])
    snaps = [(z["e%d" % i], z["k%d" % i], z["a%d" % i]) for i in range(k)]
    print("%d slices loaded" % k, flush=True)
    t0 = time.perf_counter()
    try:
        st = spacetime_readings(snaps, 4000 + SEED)
    except MemoryError as e:
        print("MemoryError: %s" % e)
        with open("e4_spacetime52.txt", "w", encoding="utf-8") as f:
            f.write("not measurable at n=52 on this machine: %s\n" % e)
        return 1
    st["seconds"] = time.perf_counter() - t0
    print(json.dumps(st, indent=1, default=str))
    with open("e4_spacetime52.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(st, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
