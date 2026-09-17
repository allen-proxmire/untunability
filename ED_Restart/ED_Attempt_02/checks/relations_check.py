"""Inputs-and-relations table (RD3): compute the empirical relations from the values in table/inputs.csv, and count
inputs and relations by relation-gradient-boundary class (D1) from table/relations.csv.

Expected results, written down before the first run (2026-09-14):
  X1 Koide: |Q - 2/3| < 2e-5 with PDG 2024 lepton masses.
  X2 Gatto-Sartori-Tonin: |V_us| and sqrt(m_d / m_s) agree to within 0.005 (m_s/m_d from m_s/m_ud and m_u/m_d).
  X3 Quark-lepton complementarity: theta_12(PMNS) + theta_C exceeds 45 degrees by between 1 and 2.5 degrees.
  X4 Top Yukawa sqrt2 m_t / v lies between 0.98 and 1.00.
  X5 Light neutrino species: |2.984 - 3| is less than 2.5 standard deviations.
Reported, not expected in advance (they follow from how the table was sorted): counts of inputs and of relations by
class and type.
Exit code: X1-X5.
"""
import csv
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "..", "table")


def load(name):
    with open(os.path.join(TABLE, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    inputs = {r["id"]: r for r in load("inputs.csv")}
    rels = load("relations.csv")
    val = lambda k: float(inputs[k]["value"])

    me, mmu, mtau = val("S06"), val("S07"), val("S08")
    Q = (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2
    vus, ms_mud, mu_md = val("S15"), val("S20"), val("S21")
    md_over_mud = 2.0 / (1.0 + mu_md)
    ms_md = ms_mud / md_over_mud
    gst = math.sqrt(1.0 / ms_md)
    thC = math.degrees(math.asin(vus))
    qlc = val("N04") + thC - 45.0
    yt = math.sqrt(2) * val("S14") / val("S04")
    nnu, snu = 2.984, 0.008

    print("R02 Koide Q = %.7f (2/3 = %.7f; difference %.1e)" % (Q, 2 / 3, Q - 2 / 3))
    print("R03 GST: |V_us| = %.4f, sqrt(m_d/m_s) = %.4f (m_s/m_d = %.2f); difference %.4f" % (vus, gst, ms_md, vus - gst))
    print("R04 QLC: theta_12 + theta_C = %.2f + %.2f = %.2f deg (45 + %.2f)" % (val("N04"), thC, val("N04") + thC, qlc))
    print("R05 top Yukawa sqrt2 m_t / v = %.4f" % yt)
    print("R08 light neutrino species: %.3f +- %.3f, %.1f sigma from 3" % (nnu, snu, abs(nnu - 3) / snu))

    ci = Counter(r["class"] for r in inputs.values())
    free_like = Counter(r["class"] for r in inputs.values() if r["status"] not in ("measured",))
    print("\ninputs by class: %s; not simply measured (free, bound, unknown, chosen): %s" % (dict(ci), dict(free_like)))
    ct = Counter((r["class"], r["type"]) for r in rels)
    for cls in ("relation", "gradient", "boundary"):
        row = {t: ct[(cls, t)] for t in ("theorem", "measurement", "empirical-unexplained", "ED-internal")}
        print("relations, %-8s: %s" % (cls, row))

    checks = [("X1 Koide within 2e-5 of 2/3", abs(Q - 2 / 3) < 2e-5),
              ("X2 GST agreement within 0.005", abs(vus - gst) < 0.005),
              ("X3 QLC excess between 1 and 2.5 degrees", 1.0 < qlc < 2.5),
              ("X4 top Yukawa between 0.98 and 1.00", 0.98 <= yt <= 1.00),
              ("X5 neutrino species within 2.5 sigma of 3", abs(nnu - 3) / snu < 2.5)]
    print("\nExpected results:")
    for name, ok in checks:
        print("  %-16s %s" % ("AS EXPECTED" if ok else "NOT AS EXPECTED", name))
    return all(ok for _, ok in checks)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
