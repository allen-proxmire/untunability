"""The draw rebuilt (RD50). See Spec.md.

A pattern is an array psi[uS, KS, e_0, ..., e_{F-1}]: the system on a ring of loci with channels (INTERNAL, LEFT,
RIGHT), spreading with version 0's walk_step, and F environment fragments of committed matter, each with two channels,
UNMARKED (0) and MARKED (1). The environment has a state, so the mark stays in it.

Meeting (RD27): where the system is at one of a set of loci, a fragment turns from UNMARKED toward MARKED by an angle.
Linear, conserving, never draws. The set of loci is the distinction the record is about (its family).
Draw (RD50 working stand-in): once a family has R_STAR fragments with near-perfect records (sin theta >= 1 - DELTA),
the record value (all UNMARKED or all MARKED) is fixed, with probability equal to the amount in it. Only the record is
fixed; everything inside it stays coherent. R_STAR and DELTA are modelling choices, not part of ED.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v0"))
import rule_v0 as v0  # noqa: E402

INTERNAL, LEFT, RIGHT = v0.INTERNAL, v0.LEFT, v0.RIGHT
UNMARKED, MARKED = 0, 1
R_STAR, DELTA = 3, 0.01


def start(a_system, F):
    psi = np.zeros(a_system.shape + (2,) * F, dtype=complex)
    psi[(slice(None), slice(None)) + (UNMARKED,) * F] = a_system
    return psi


def amount(psi):
    return float((np.abs(psi) ** 2).sum())


def _per_config(psi, fn):
    L = psi.shape[0]
    flat = psi.reshape(L, 3, -1)
    out = np.empty_like(flat)
    for j in range(flat.shape[2]):
        out[:, :, j] = fn(flat[:, :, j])
    return out.reshape(psi.shape)


def walk(psi):
    """One spreading step of the system in every environment configuration."""
    return _per_config(psi, v0.walk_step)


def mirror(psi):
    """System locus u -> -u and Left <-> Right, in every environment configuration; fragments unchanged."""
    return _per_config(psi, v0.mirror)


def meet(psi, loci, frag, theta):
    """Where the system is at one of `loci`, fragment `frag` turns toward MARKED by theta. Returns (pattern, record)."""
    loci = sorted(loci)
    out = psi.copy()
    ax = 2 + frag
    sub = np.moveaxis(psi[loci], ax, -1)
    x0, x1 = sub[..., UNMARKED], sub[..., MARKED]
    c, s = np.cos(theta), np.sin(theta)
    new = np.stack([c * x0 - s * x1, s * x0 + c * x1], axis=-1)
    out[loci] = np.moveaxis(new, -1, ax)
    return out, {"family": tuple(loci), "frag": frag, "theta": theta}


def perfect_fragments(marks, family, delta=DELTA):
    return sorted({m["frag"] for m in marks if m["family"] == family and np.sin(m["theta"]) >= 1 - delta})


def draw_outcomes(psi, frags):
    """Fix only which record the fragments hold. Returns ([(probability, pattern)], weight of disagreeing records)."""
    total = amount(psi)
    res = []
    for c in (UNMARKED, MARKED):
        idx = [slice(None)] * psi.ndim
        for f in frags:
            idx[2 + f] = c
        out = np.zeros_like(psi)
        out[tuple(idx)] = psi[tuple(idx)]
        w = amount(out)
        if w > 0:
            res.append((w / total, out * np.sqrt(total / w)))
    return res, 1.0 - sum(p for p, _ in res)


def run(psi, events, r_star=R_STAR, delta=DELTA):
    """Apply events: ("walk",) or ("meet", loci, frag, theta). After each meeting, a family that reaches r_star
    near-perfect fragments and hasn't been drawn is drawn. Returns ([(probability, pattern, drawn families)], marks,
    largest disagreeing weight)."""
    branches = [(1.0, psi, frozenset())]
    marks, worst = [], 0.0
    for ev in events:
        if ev[0] == "walk":
            branches = [(p, walk(b), d) for p, b, d in branches]
            continue
        new = []
        rec = None
        for p, b, d in branches:
            b2, rec = meet(b, ev[1], ev[2], ev[3])
            new.append((p, b2, d))
        marks.append(rec)
        branches = new
        fam = rec["family"]
        frags = perfect_fragments(marks, fam, delta)
        if len(frags) >= r_star:
            out = []
            for p, b, d in branches:
                if fam in d:
                    out.append((p, b, d))
                    continue
                res, dis = draw_outcomes(b, frags)
                worst = max(worst, abs(dis))
                out += [(p * q, bb, d | {fam}) for q, bb in res]
            branches = out
    return branches, marks, worst


def erase(psi, frags, signs):
    """Measure fragments in the (UNMARKED + s MARKED)/sqrt 2 basis and keep outcome s for each. Returns
    (weight relative to the pattern's amount, unnormalized kept part)."""
    out = psi.copy()
    for f, s in zip(frags, signs):
        ax = 2 + f
        sub = np.moveaxis(out, ax, -1)
        kept = (sub[..., UNMARKED] + s * sub[..., MARKED]) / np.sqrt(2)
        new = np.stack([kept, np.zeros_like(kept)], axis=-1)
        out = np.moveaxis(new, -1, ax)
    return amount(out) / amount(psi), out


def screen(psi, steps):
    b = psi
    for _ in range(steps):
        b = walk(b)
    s = (np.abs(b) ** 2).sum(axis=tuple(range(1, b.ndim)))
    return s


def reduced(psi, ax):
    m = np.moveaxis(psi, ax, 0).reshape(psi.shape[ax], -1)
    return m @ m.conj().T
