"""M2 (note 13): CGP with one change, births inside a relation (a-b becomes a-z-b)."""
from cgp import CGP


class M2(CGP):
    def _birth(self):
        p = self.rng.integers(self.m)
        a, b = int(self.ei[p]), int(self.ej[p])
        self._remove_edge(a, b)
        z = self._new_locus()
        self._add_edge(a, z)
        self._add_edge(z, b)
        if self.curvature_ok([z, a, b]):
            self.counts["births"] += 1
            self._consec_birth_fail = 0
        else:
            self._remove_edge(a, z)
            self._remove_edge(z, b)
            self.n -= 1
            self._add_edge(a, b)
            self.counts["birth_fail"] += 1
            self._consec_birth_fail += 1
            if self._consec_birth_fail >= 10000:
                self.stalled = True
