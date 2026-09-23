"""Commitment rule, version 1, on 1D rings of loci.

Built on version 0 (../v0/rule_v0.py) with ledger decisions RD22 and RD26-RD28. See Spec.md.

What changed from version 0:
- No spontaneous draws. The thinness trigger (RD19) is retired (RD26); nothing here uses it.
- Meetings hinge (RD27). `meet` is a linear, conserving step on two parts. It never draws.
- Draws happen only where a mark can't be brought back (RD28). Version 1 models that with a
  detector: a part that reaches a detector is drawn, with the local draw (RD22). What makes a
  mark unrecoverable in general is open (G36); the detector stands in for it.

A two-part pattern is an array A[uS, KS, uM, KM]: part 0 (the system) and part 1 (the marker),
each on its own ring.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v0"))
import rule_v0 as v0  # noqa: E402

INTERNAL, LEFT, RIGHT = v0.INTERNAL, v0.LEFT, v0.RIGHT
walk_step = v0.walk_step
mirror = v0.mirror
shares = v0.shares
walk_step_part = v0.walk_step_part
part_shares = v0.part_shares
draw_local = v0.draw_entangled  # RD22
budget_step, budget_steady, rate, clock_ticks_per_step = (
    v0.budget_step, v0.budget_steady, v0.rate, v0.clock_ticks_per_step)


def joint(a_system, a_marker):
    """Two separate patterns, not yet hinged: A[uS, KS, uM, KM] = a_system[uS, KS] * a_marker[uM, KM]."""
    return np.einsum("uk,vl->ukvl", a_system, a_marker)


def swap_lanes(a):
    """A test interaction (input, V1-L2): Left and Right lanes exchange at every locus; loci don't move.
    It is its own inverse."""
    return a[:, [INTERNAL, RIGHT, LEFT]]


def meet(A, x, op):
    """RD27: where the system part is at locus x, in any channel, the marker part is changed by op.
    The two parts are then hinged. Linear and conserving whenever op is. Never draws."""
    out = A.copy()
    for K in range(3):
        out[x, K] = op(A[x, K])
    return out


def detector_outcomes(A, part):
    """RD28 as modelled in version 1: a detector draws the part that reaches it, with the local draw (RD22).
    Returns every possible outcome as (probability, pattern after the draw). This is the exact
    distribution that draw_local samples from."""
    total = (np.abs(A) ** 2).sum()
    B = A if part == 0 else A.transpose(2, 3, 0, 1)
    result = []
    for u in range(B.shape[0]):
        for K in range(3):
            rest = B[u, K]
            w = (np.abs(rest) ** 2).sum()
            if w == 0:
                continue
            out = np.zeros_like(B)
            out[u, K] = rest / np.sqrt(w) * np.sqrt(total)
            result.append((w / total, out if part == 0 else out.transpose(2, 3, 0, 1)))
    return result


def run(A, events, rng):
    """Apply events in order and count draws. Events: ("walk", part), ("meet", x, op), ("detect", part).
    Draws happen only at "detect" events (RD26, RD28)."""
    draws = 0
    for event in events:
        kind = event[0]
        if kind == "walk":
            A = walk_step_part(A, event[1])
        elif kind == "meet":
            A = meet(A, event[1], event[2])
        elif kind == "detect":
            A = draw_local(A, event[1], rng)
            draws += 1
        else:
            raise ValueError("unknown event %r" % (event,))
    return A, draws
