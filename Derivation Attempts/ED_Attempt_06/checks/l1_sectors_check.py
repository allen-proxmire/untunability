"""Loops on paper: linear-algebra check of the sector split (note 10, C49).

No simulation: nothing is evolved in time. Only subspaces, projections and
eigenvalues of one-step matrices are computed, on the same stand-in patterns
as w2_stuck_states_check.py (79 loci, seeds 1-3, reach 0.3).

On-paper claim. With d: C^arcs -> C^loci, (d psi)(x) = sum over arcs leaving x
of psi / sqrt(deg x), so that d d* = I and P = d* d; S the flip-flop shift;
coin C = a (I + (e^{i theta} - 1) P); U = S C:
  * L = span{ d* f, S d* g } (states built from locus values) is U-invariant:
      U d* f = a e^{i theta} S d* f,
      U S d* g = a (d* g + (e^{i theta} - 1) S d* T g),  T = d S d*;
  * L's orthogonal complement is exactly ker d ∩ ker dS, the stuck space;
  * for a connected, non-bipartite pattern, d* f = S d* g only for
    f = g ∝ sqrt(deg), so dim L = 2|V| - 1 and the stuck space has
    dimension 2|E| - 2|V| + 1;
  * for the Grover coin, U on L has eigenvalues e^{±i arccos λ}, λ in σ(T),
    with λ = 1 giving the single eigenvalue 1.

Expected results, written down before the first run:
  L0  For each of the 3 patterns: rank of [d*, S d*] = 2|V| - 1, and the
      dimension of ker P ∩ ker PS = 2|E| - 2|V| + 1 (patterns non-bipartite).
  L1  For each pattern and each of the 3 coins (Grover; a = 1, theta = pi/2;
      a = e^{0.7i}, theta = 2.1): || (I - Q_L) U Q_L || < 1e-10, where Q_L
      projects onto L (L is invariant).
  L2  For each pattern: the largest overlap |<u, v>| between an orthonormal
      basis of L and one of ker P ∩ ker PS is < 1e-10 (they are orthogonal),
      and their dimensions add to 2|E|.
  L3  Grover coin, each pattern: the 2|V| - 1 eigenvalues of U restricted to
      L match, as sorted phases, {±arccos λ : λ in σ(T), λ ≠ 1} ∪ {0}, to
      within 1e-7.
"""
import numpy as np
from scipy.linalg import orth, null_space
import importlib.util, os

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "w2_stuck_states_check.py"), encoding="utf-8").read().split("coins = [")[0]
ns = {}
exec(src, ns)
graph, bipartite = ns["graph"], ns["bipartite"]
ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= ok
    print(f"{name}: {'AS EXPECTED' if ok else 'NOT AS EXPECTED'}  {detail}")


def build(nv, edges):
    arcs = [(u, v) for u, v in edges] + [(v, u) for u, v in edges]
    k = {arc: i for i, arc in enumerate(arcs)}
    M = len(arcs)
    deg = np.zeros(nv)
    for u, v in arcs:
        deg[u] += 1
    S = np.zeros((M, M))
    D = np.zeros((nv, M))
    for (u, v), i in k.items():
        S[k[(v, u)], i] = 1
        D[u, i] = 1 / np.sqrt(deg[u])
    return S, D, M


coins = [(-1.0 + 0j, np.pi, "Grover"), (1.0 + 0j, np.pi / 2, "a=1, theta=pi/2"), (np.exp(0.7j), 2.1, "a=e^0.7i, theta=2.1")]
for seed in (1, 2, 3):
    nv, edges = graph(seed)
    ne = len(edges)
    S, D, M = build(nv, edges)
    P = D.T @ D
    B = np.hstack([D.T, S @ D.T])
    rankL = np.linalg.matrix_rank(B, tol=1e-9)
    stuck = null_space(np.vstack([D, D @ S]), rcond=1e-9)
    report(f"L0 seed {seed}", rankL == 2 * nv - 1 and stuck.shape[1] == 2 * ne - 2 * nv + 1 and not bipartite(nv, edges),
           f"|V|={nv}, |E|={ne}: dim L = {rankL} (expected {2*nv-1}), stuck dim = {stuck.shape[1]} (expected {2*ne-2*nv+1})")
    QL_basis = orth(B, rcond=1e-9)
    QL = QL_basis @ QL_basis.conj().T
    for a, th, name in coins:
        C = a * (np.eye(M) + (np.exp(1j * th) - 1) * P)
        U = S @ C
        err = np.linalg.norm((np.eye(M) - QL) @ U @ QL, 2)
        report(f"L1 seed {seed} {name}", err < 1e-10, f"invariance error = {err:.2e}")
        if name == "Grover":
            R = QL_basis.conj().T @ U @ QL_basis
            ph = np.sort(np.angle(np.linalg.eigvals(R)))
            T = D @ S @ D.T
            lam = np.linalg.eigvalsh((T + T.T) / 2)
            lam = np.sort(lam)[:-1]  # drop the single λ = 1
            target = np.sort(np.concatenate([np.arccos(np.clip(lam, -1, 1)), -np.arccos(np.clip(lam, -1, 1)), [0.0]]))
            dev = np.max(np.abs(ph - target)) if len(ph) == len(target) else np.inf
            report(f"L3 seed {seed}", dev < 1e-7, f"largest phase mismatch = {dev:.2e} over {len(ph)} eigenvalues; top λ of T = {np.max(np.linalg.eigvalsh((T+T.T)/2)):.12f}")
    ov = np.max(np.abs(QL_basis.conj().T @ stuck))
    report(f"L2 seed {seed}", ov < 1e-10 and QL_basis.shape[1] + stuck.shape[1] == M,
           f"largest overlap = {ov:.2e}; dims {QL_basis.shape[1]} + {stuck.shape[1]} = {QL_basis.shape[1] + stuck.shape[1]} of {M}")

print("ALL AS EXPECTED" if ok_all else "SOME NOT AS EXPECTED")
