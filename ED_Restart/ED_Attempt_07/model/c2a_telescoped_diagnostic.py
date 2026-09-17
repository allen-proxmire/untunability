"""Follow-up diagnostic for C2a run 1 (NOT pre-registered).

Run 1's E2 missed only on 'median mean offspring in [0.98, 1.02]', where mean
offspring was the arithmetic mean of L_(t+1)/L_t over slices T/2..T. That
average of ratios is biased upward by fluctuations (1.1 x 0.9 = 0.99 while the
ratios average 1). Here, on the same settings and seeds, two measures that do
not carry that bias: the telescoped (geometric-mean) ratio
exp[(ln L_(T-1) - ln L_(T/2)) / (T/2 - 1)], and the ratio of sums
sum L_(t+1) / sum L_t. Run 1's verdict stands.
"""
import numpy as np
from c2a import grow_budget, balance_stats
T = 400
for k in (0.5, 1.0, 1.5, 2.5):
    for Ls in (100, 200):
        ar, tel, ros, surv = [], [], [], 0
        for s in range(20):
            g = grow_budget(T, Ls, k, s, "B")
            if g["status"] != "survived":
                continue
            surv += 1
            L = np.array(g["lengths"], float)
            lo = T // 2
            ar.append(balance_stats(g["lengths"], T)[0])
            tel.append(np.exp((np.log(L[T - 1]) - np.log(L[lo])) / (T - 1 - lo)))
            ros.append(L[lo + 1:T].sum() / L[lo:T - 1].sum())
        print(f"reading B k={k} L*={Ls}: survived {surv}/20; median offspring: average-of-ratios {np.median(ar):.4f}, telescoped {np.median(tel):.4f}, ratio-of-sums {np.median(ros):.4f}")
