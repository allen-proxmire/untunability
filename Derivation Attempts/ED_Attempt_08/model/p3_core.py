"""Port of attempt 7's C3c-C3f slice onto flat arrays with a Numba inner loop (E2; note 2 C6; D3).

Containers (IMPLEMENTATION_NOTES.md, "The port"):
  * tetrahedra as rows of `tv` (sorted int32 4-tuples) with an alive flag and an index-swap pool;
  * a tetrahedron-key hash (64-bit mix, collisions resolved by comparing `tv` rows);
  * per-vertex tetrahedron lists and neighbour lists in a power-of-two arena with free lists;
  * an edge hash (min*2^32+max -> slot) with `e_a`, `e_b`, `e_val` and an index-swap pool of valence-3 edges;
  * a scratch open-addressing table, cleared by a stamp counter, for the per-move edge delta.

Nothing here decides the model; it is attempt 7's model in a different representation.
"""
import numpy as np
from numba import njit, int32, int64, float64, uint64

FLAT_VALENCE = 2 * np.pi / np.arccos(1 / 3)          # 5.1043
SIGMA = 0.0005
K = 0.5
K_RESPONSE = 1.0
FLAT_LINKS_PER_EVENT = 1 + FLAT_VALENCE / (6 - FLAT_VALENCE)   # 6.699
CEILING = 60

EMPTY = -1
NCLASS = 12                    # size classes 8, 16, ... 16384
MINCLASS = 3                   # 2**3 = 8


# ---------------------------------------------------------------- randomness
@njit(cache=True, inline="always")
def _rotl(x, k):
    return (x << uint64(k)) | (x >> uint64(64 - k))


@njit(cache=True)
def rng_seed(seed):
    """splitmix64 expansion into a xoshiro256** state."""
    s = np.empty(4, dtype=np.uint64)
    z = uint64(seed)
    for i in range(4):
        z = z + uint64(0x9E3779B97F4A7C15)
        y = z
        y = (y ^ (y >> uint64(30))) * uint64(0xBF58476D1CE4E5B9)
        y = (y ^ (y >> uint64(27))) * uint64(0x94D049BB133111EB)
        s[i] = y ^ (y >> uint64(31))
    return s


@njit(cache=True, inline="always")
def rng_next(s):
    result = _rotl(s[1] * uint64(5), 7) * uint64(9)
    t = s[1] << uint64(17)
    s[2] ^= s[0]
    s[3] ^= s[1]
    s[1] ^= s[2]
    s[0] ^= s[3]
    s[2] ^= t
    s[3] = _rotl(s[3], 45)
    return result


@njit(cache=True, inline="always")
def rng_float(s):
    return (rng_next(s) >> uint64(11)) * (1.0 / 9007199254740992.0)


@njit(cache=True, inline="always")
def rng_below(s, n):
    """Uniform integer in [0, n), by rejection so the result is exactly uniform."""
    if n <= 1:
        return 0
    lim = uint64(0xFFFFFFFFFFFFFFFF) - (uint64(0xFFFFFFFFFFFFFFFF) % uint64(n)) - uint64(n) + uint64(1)
    while True:
        r = rng_next(s)
        if r <= lim:
            return int64(r % uint64(n))


@njit(cache=True)
def rng_geometric(s, p):
    """Trials until the first success, support >= 1 (numpy's `geometric`)."""
    if p >= 1.0:
        return 1
    u = rng_float(s)
    if u <= 0.0:
        u = 1e-300
    return int64(np.floor(np.log(u) / np.log1p(-p))) + 1


@njit(cache=True)
def rng_shuffle(s, a, n):
    for i in range(n - 1, 0, -1):
        j = rng_below(s, i + 1)
        a[i], a[j] = a[j], a[i]


# ---------------------------------------------------------------- hashing
@njit(cache=True, inline="always")
def mix64(x):
    x = uint64(x)
    x = (x ^ (x >> uint64(33))) * uint64(0xFF51AFD7ED558CCD)
    x = (x ^ (x >> uint64(33))) * uint64(0xC4CEB9FE1A85EC53)
    return x ^ (x >> uint64(33))


@njit(cache=True, inline="always")
def ekey(a, b):
    if a < b:
        return (int64(a) << int64(32)) | int64(b)
    return (int64(b) << int64(32)) | int64(a)


# ---- edge table: open addressing, keys in ek_key, payload = edge slot -------
@njit(cache=True)
def etab_find(ek_key, ek_slot, mask, key):
    """Return (probe index, slot or -1)."""
    i = int64(mix64(key) & uint64(mask))
    while True:
        k = ek_key[i]
        if k == key:
            return i, ek_slot[i]
        if k == int64(0):
            return i, int64(-1)
        i = (i + 1) & mask


@njit(cache=True)
def etab_insert(ek_key, ek_slot, mask, key, slot):
    i = int64(mix64(key) & uint64(mask))
    while ek_key[i] != int64(0) and ek_key[i] != key:
        i = (i + 1) & mask
    ek_key[i] = key
    ek_slot[i] = slot


@njit(cache=True)
def etab_delete(ek_key, ek_slot, mask, key):
    """Backward-shift deletion, so linear probing stays correct."""
    i, slot = etab_find(ek_key, ek_slot, mask, key)
    if slot < 0:
        return
    ek_key[i] = int64(0)
    ek_slot[i] = int64(-1)
    j = (i + 1) & mask
    while ek_key[j] != int64(0):
        k = ek_key[j]
        h = int64(mix64(k) & uint64(mask))
        # can k live at i?
        move = False
        if j > i:
            move = h <= i or h > j
        else:
            move = h <= i and h > j
        if move:
            ek_key[i] = k
            ek_slot[i] = ek_slot[j]
            ek_key[j] = int64(0)
            ek_slot[j] = int64(-1)
            i = j
        j = (j + 1) & mask


# ---------------------------------------------------------------- arena
@njit(cache=True)
def arena_class(n):
    c = MINCLASS
    while (1 << c) < n:
        c += 1
    return c - MINCLASS


@njit(cache=True)
def arena_alloc(ar_data, ar_free_head, ar_next, ar_top, cls):
    """Take a block of size 2**(cls+MINCLASS); returns (start, new top)."""
    h = ar_free_head[cls]
    if h >= 0:
        ar_free_head[cls] = ar_next[h]
        return h, ar_top
    start = ar_top
    return start, ar_top + (1 << (cls + MINCLASS))


@njit(cache=True)
def arena_release(ar_free_head, ar_next, start, cls):
    ar_next[start] = ar_free_head[cls]
    ar_free_head[cls] = start
