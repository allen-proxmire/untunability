"""Check C63: how commitment is shared between moving and ticking decides whether
the muon measurement is passed.

Idea (Allen, G25): a moving chain spends commitment on moving, leaving less for its
internal clock. Two ways to share a fixed total:
  linear split:       tick fraction = 1 - v/c
  Pythagorean split:  (tick fraction)^2 + (v/c)^2 = 1, tick fraction = sqrt(1 - v^2/c^2)

Muons in the CERN storage ring (Bailey et al. 1977) had gamma = 29.33 and their
lifetime was dilated by that factor to about 2 parts in 1000. The lifetime dilation
equals 1 / (tick fraction).

The Pythagorean split is special relativity's proper-time formula restated, so it
matches by construction. The check's job is to show the linear split does not.
"""
import math
import sys

GAMMA = 29.33
v = math.sqrt(1 - 1 / GAMMA ** 2)          # speed as a fraction of c
linear = 1 / (1 - v)
pythagorean = 1 / math.sqrt(1 - v ** 2)

print("speed v/c                     %.6f" % v)
print("measured lifetime dilation    %.2f" % GAMMA)
print("linear split predicts         %.1f" % linear)
print("Pythagorean split predicts    %.2f" % pythagorean)

ok = abs(pythagorean - GAMMA) / GAMMA < 2e-3 and abs(linear - GAMMA) / GAMMA > 0.5
print("C63 holds: only the Pythagorean split matches" if ok else "C63 FAILED")
sys.exit(0 if ok else 1)
