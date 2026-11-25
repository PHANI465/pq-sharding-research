"""M8: control test (week-6 criterion 1). Multiply every weight by one constant: partition must not change.
Also shows the METIS integer-rounding risk (M3)."""
from common import *
n, edges, truth = planted_two_groups(10, heavy=10, light=3, n_cross=12, seed=2)
big = {e: w * 10 for e, w in edges.items()}
for seed in range(5):
    p1 = metis_partition(n, edges, 2, seed=seed)
    p2 = metis_partition(n, big, 2, seed=seed)
    print(f"METIS seed {seed}: cut {p1[1]} -> {p2[1]}  same partition: {same_partition(p1[0], p2[0])}")
    assert same_partition(p1[0], p2[0]) and p2[1] == 10 * p1[1]
e1 = exact_partition(n, edges, 2); e2 = exact_partition(n, big, 2)
print("exact cut", e1[1], "->", e2[1], "(x10)  same partition:", same_partition(e1[0], e2[0]))
assert e2[1] == 10 * e1[1] and cut_cost(edges, e2[0]) == e1[1]
# rounding demo: two real weights that differ by 0.4% collapse to the same integer at a coarse scale
real = {(0, 1): 1.004, (1, 2): 1.000}
for sc in (1, 10, 1000):
    print(f"scale {sc:>4}: {scale_to_int(real, sc)}")
print("M8 OK")
