"""C2a timing (note 6, running order step 1). Timing only: values are not results."""
import time
import numpy as np
from c2a import grow_budget
from c1 import build
from readings_v2 import all_readings

t0 = time.perf_counter()
for s in range(5):
    grow_budget(400, 200, 1.0, 900 + s, "B")
tb = (time.perf_counter() - t0) / 5
t1 = time.perf_counter()
g = grow_budget(200, 200, 1.0, 999, "B", keep_offspring=True)
A, ok, notes = build(g["lengths"], g["offspring"])
all_readings(A, np.random.default_rng(1))
tg = time.perf_counter() - t1
print(f"one balance run (T=400, L*=200): {tb:.2f} s; 200 balance runs: about {200*tb/60:.1f} min")
print(f"one geometry run with readings ({A.shape[0]} events, status {g['status']}): {tg:.0f} s; 9 runs: about {9*tg/60:.1f} min")
print(f"estimated c2a_run.py total: about {(200*tb + 9*tg)/60:.1f} min")
