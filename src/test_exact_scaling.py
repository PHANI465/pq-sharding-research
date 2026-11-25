"""M10(b): how large a graph does the exact solver handle in a few minutes? Random weighted graphs
(no planted structure, heavy-tailed weights) are much harder than the planted test graph."""
import numpy as np
from common import exact_partition, metis_partition
rng = np.random.default_rng(0)
print(" n  k  edges  exact_cut  status    seconds  metis_cut(best of 10 seeds)")
for n, k in ((20, 2), (30, 2), (40, 2), (20, 4), (30, 4), (40, 4)):
    edges = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.25:
                edges[(i, j)] = int(rng.pareto(1.5) * 100) + 1
    a, c, st, secs = exact_partition(n, edges, k, time_limit=120)
    mc = min(metis_partition(n, edges, k, seed=s)[1] for s in range(10))
    print(f"{n:>2} {k:>2} {len(edges):>6} {str(c):>10}  {st:<9} {secs:>7.1f}  {mc}")
