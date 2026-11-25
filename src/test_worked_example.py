"""M7: the four-account deck example (our own derivation, not from a paper).
A-B and C-D: 2 contract calls of 1,065 B. A-C and B-D: 10 transfers of 185 B. Two shards of two.
Migration adds 3,244 B per message (3,309 B ML-DSA-65 signature - 65 B ECDSA signature)."""
import itertools
from common import *
A, B, C, D = range(4)
def graph(extra):
    return {(A, B): 2 * (1065 + extra), (C, D): 2 * (1065 + extra),
            (A, C): 10 * (185 + extra),  (B, D): 10 * (185 + extra)}
layouts = {"{A,B}|{C,D} (cuts transfer pairs)": [0, 0, 1, 1],
           "{A,C}|{B,D} (cuts call pairs)":     [0, 1, 0, 1],
           "{A,D}|{B,C} (cuts all four pairs)": [0, 1, 1, 0]}
for label, extra in (("BEFORE (ECDSA)", 0), ("AFTER (ML-DSA-65, +3244 B/msg)", 3244)):
    e = graph(extra)
    print(label)
    for name, a in layouts.items():
        print(f"   {name}: {cut_cost(e, a):>6}")
    a, c, st, _ = exact_partition(4, e, 2)
    mt = metis_partition(4, e, 2, seed=0, ufactor=1)
    print("   exact:", normalise(a), c, st, "| metis:", normalise(mt[0]), mt[1])
    best = min(layouts, key=lambda k: cut_cost(e, layouts[k]))
    print("   best layout:", best)
b, a_ = graph(0), graph(3244)
assert cut_cost(b, [0,0,1,1]) == 3700 and cut_cost(b, [0,1,0,1]) == 4260
assert cut_cost(a_, [0,0,1,1]) == 68580 and cut_cost(a_, [0,1,0,1]) == 17236
assert same_partition(exact_partition(4, b, 2)[0], [0,0,1,1])
assert same_partition(exact_partition(4, a_, 2)[0], [0,1,0,1])
print("M7 OK: best layout flips after migration")
