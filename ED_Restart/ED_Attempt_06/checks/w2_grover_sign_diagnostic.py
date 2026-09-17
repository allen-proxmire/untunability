"""Follow-up diagnostic for w2_stuck_states_check.py (NOT pre-registered).

Run 1 gave S2 NOT AS EXPECTED: for the Grover coin the extra two eigenvalues
sat at -1 (m-n+2) instead of +1 (m-n+1 plus the lifted T-eigenvalue 1).
The verdict stands. This asks only which convention or count is behind it.
Hand counts: triangle Grover walk (d = 2 coin swaps the two out-arcs) is a
pair of 3-cycles on arcs, so eigenvalues 1, w, w^2 twice each (+1 twice,
-1 never). Also reports the dimension of the stuck space ker P ∩ ker PS
and the U-eigenvalues of its vectors.
"""
import numpy as np
import importlib.util, os

spec = importlib.util.spec_from_file_location("chk", os.path.join(os.path.dirname(__file__), "w2_stuck_states_check.py"))
src = open(spec.origin, encoding="utf-8").read().split("coins = [")[0]
ns = {}
exec(src, ns)
walk, graph = ns["walk"], ns["graph"]


def stuck_dim(nv, edges):
    U, M = walk(nv, edges, -1.0 + 0j, np.pi)
    arcs = [(u, v) for u, v in edges] + [(v, u) for u, v in edges]
    k = {arc: i for i, arc in enumerate(arcs)}
    S = np.zeros((M, M))
    for (u, v), i in k.items():
        S[k[(v, u)], i] = 1
    P = np.zeros((M, M))
    for x in range(nv):
        out = [i for (u, v), i in k.items() if u == x]
        for i in out:
            for j in out:
                P[i, j] = 1 / len(out)
    B = np.vstack([P, P @ S])
    sv = np.linalg.svd(B, compute_uv=True)
    null = sv[2][np.sum(sv[1] > 1e-9):].conj().T
    # eigenvalues of U restricted to the stuck space (it is invariant)
    R = null.conj().T @ U @ null
    ev = np.linalg.eigvals(R)
    return null.shape[1], int(np.sum(np.abs(ev - 1) < 1e-8)), int(np.sum(np.abs(ev + 1) < 1e-8))


cases = {
    "triangle": (3, [(0, 1), (1, 2), (0, 2)]),
    "K4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    "path of 3": (3, [(0, 1), (1, 2)]),
    "square (bipartite)": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    "seed 1 graph": graph(1),
}
for name, (nv, edges) in cases.items():
    m = len(edges)
    U, M = walk(nv, edges, -1.0 + 0j, np.pi)
    ev = np.linalg.eigvals(U)
    p, q = int(np.sum(np.abs(ev - 1) < 1e-8)), int(np.sum(np.abs(ev + 1) < 1e-8))
    evCS = np.linalg.eigvals(U.T)  # transpose has the same spectrum; sanity
    d, sp, sm = stuck_dim(nv, edges)
    print(f"{name}: |V|={nv}, |E|={m}, m-n={m-nv}; Grover U=S C: +1 x{p}, -1 x{q} of {M}; "
          f"stuck space dim {d} (U on it: +1 x{sp}, -1 x{sm})")
