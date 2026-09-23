"""Diagnostic (not pre-registered): does the relations-per-event the filter settles on depend on the pull?

Road P's run left every start carrying 6.2-7.0 relations per event, which is close to ED's link budget of 6.699.
That budget was derived from flat geometry (A7 C4), and nothing in this model was told it. But the pull K0 = 1 is
Claude's setting (D13 fixes only the units), so the match means nothing until we know whether the settled number
moves when the pull moves. If it scales with K0, the match is a coincidence of one setting.
"""
import sys
import time
sys.path.insert(0, ".")
import p_persist as P

for k0 in (0.5, 1.0, 2.0):
    P.K0 = k0
    t = time.time()
    r = P.run("ring", 1, True)
    print("pull %.2f | n %d -> %d | d_H %s | relations per event %.2f | repairs %d | %.0fs"
          % (k0, r["n0"], r["n"], r["final"]["d_H"], r["final"]["per_event"], sum(r["repairs"]), time.time() - t),
          flush=True)
