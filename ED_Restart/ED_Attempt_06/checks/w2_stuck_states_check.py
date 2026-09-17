"""Road W part 2: arithmetic (linear-algebra) check of the stuck-state bound (note 3, C12).

No simulation: nothing is evolved in time. Only the eigenvalues of one-step
matrices are counted.

On-paper claim being checked. A coined walk whose state sits on (locus,
neighbour) pairs ("arcs"), with no stored directions (W-Q2), uses the
flip-flop shift S (arc u->v becomes v->u) and, at every locus, the same coin
that treats all neighbours alike:
    C = a (I + (e^{i theta} - 1) P),
where P projects onto the all-equal state at each locus and |a| = 1.
Any arc state psi with P psi = 0 and P S psi = 0 obeys U psi = a S psi and
U S psi = a psi, so it only flips between psi and S psi (eigenvalues +a and -a).
Such states form a space of dimension at least 2|E| - 2|V|. So at least a
share 1 - 2/(mean degree) of all states never move.

Expected results, written down before the first run:
  S0  U is unitary to within 1e-10 in every case.
  S1  For each of 3 random geometric graphs (80 random points in the unit
      cube, seeds 1, 2, 3, reach 0.3, largest connected piece) and each of
      3 coins (a, theta) = (-1, pi) [Grover], (1, pi/2), (e^{0.7i}, 2.1),
      the number of eigenvalues of U = S C within 1e-8 of +a or -a is at
      least 2(|E| - |V|).
  S2  Grover coin: eigenvalue +1 has multiplicity |E| - |V| + 1, and
      eigenvalue -1 has |E| - |V| + (1 if the graph is bipartite, else 0)
      (spectral mapping theorem, Higuchi-Konno-Sato-Segawa, as quoted in
      Kubota-Saito-Yoshie arXiv:2103.05235, Theorem 2.1).
  S3  The stuck share 2(|E| - |V|) / (2|E|) equals 1 - 2/(mean degree) to
      1e-12, and exceeds 0.5 for every graph (mean degree above 4).
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix

ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= ok
    print(f"{name}: {'AS EXPECTED' if ok else 'NOT AS EXPECTED'}  {detail}")


def graph(seed, n=80, reach=0.3):
    pts = np.random.default_rng(seed).random((n, 3))
    pairs = cKDTree(pts).query_pairs(reach, output_type="ndarray")
    A = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
    _, lab = connected_components(A + A.T, directed=False)
    big = np.argmax(np.bincount(lab))
    keep = np.where(lab == big)[0]
    idx = {v: i for i, v in enumerate(keep)}
    edges = [(idx[u], idx[v]) for u, v in pairs if u in idx and v in idx]
    return len(keep), edges


def bipartite(nv, edges):
    adj = [[] for _ in range(nv)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    col = [-1] * nv
    col[0] = 0
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if col[w] < 0:
                col[w] = 1 - col[u]
                stack.append(w)
            elif col[w] == col[u]:
                return False
    return True


def walk(nv, edges, a, theta):
    arcs = [(u, v) for u, v in edges] + [(v, u) for u, v in edges]
    k = {arc: i for i, arc in enumerate(arcs)}
    M = len(arcs)
    S = np.zeros((M, M))
    for (u, v), i in k.items():
        S[k[(v, u)], i] = 1
    P = np.zeros((M, M))
    for x in range(nv):
        out = [i for (u, v), i in k.items() if u == x]
        for i in out:
            for j in out:
                P[i, j] = 1 / len(out)
    C = a * (np.eye(M) + (np.exp(1j * theta) - 1) * P)
    return S @ C, M


coins = [(-1.0 + 0j, np.pi, "Grover"), (1.0 + 0j, np.pi / 2, "a=1, theta=pi/2"), (np.exp(0.7j), 2.1, "a=e^0.7i, theta=2.1")]
for seed in (1, 2, 3):
    nv, edges = graph(seed)
    ne = len(edges)
    dbar = 2 * ne / nv
    bip = bipartite(nv, edges)
    share = 2 * (ne - nv) / (2 * ne)
    report(f"S3 seed {seed}", abs(share - (1 - 2 / dbar)) < 1e-12 and share > 0.5,
           f"|V| = {nv}, |E| = {ne}, mean degree = {dbar:.3f}, bipartite = {bip}, stuck share bound = {share:.4f}")
    for a, th, name in coins:
        U, M = walk(nv, edges, a, th)
        uni = np.abs(U.conj().T @ U - np.eye(M)).max()
        report(f"S0 seed {seed} {name}", uni < 1e-10, f"unitarity error = {uni:.2e}")
        ev = np.linalg.eigvals(U)
        n_plus = int(np.sum(np.abs(ev - a) < 1e-8))
        n_minus = int(np.sum(np.abs(ev + a) < 1e-8))
        report(f"S1 seed {seed} {name}", n_plus + n_minus >= 2 * (ne - nv),
               f"at +a: {n_plus}, at -a: {n_minus}, total {n_plus + n_minus} of {M}; bound 2(|E|-|V|) = {2*(ne-nv)}")
        if name == "Grover":
            ok = n_plus == ne - nv + 1 and n_minus == ne - nv + (1 if bip else 0)
            report(f"S2 seed {seed}", ok, f"+1: {n_plus} (expected {ne-nv+1}), -1: {n_minus} (expected {ne-nv+(1 if bip else 0)})")

print("ALL AS EXPECTED" if ok_all else "SOME NOT AS EXPECTED")
