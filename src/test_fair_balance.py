"""M3/M8 finding: METIS and the exact solver must use the SAME size tolerance.
Observed (n=20, k=2, unit vertex weights): METIS returns 11/9 even with ufactor=1; the exact solver
defaults to 10/10. Comparing them directly makes METIS look better than 'optimal'. Fix: give the exact
solver METIS's observed size range."""
import numpy as np
from common import *
rng = np.random.default_rng(0)
n, k = 20, 2
edges = {(i, j): int(rng.pareto(1.5) * 100) + 1 for i in range(n) for j in range(i + 1, n) if rng.random() < 0.25}
m = min((metis_partition(n, edges, k, seed=s, ufactor=1) for s in range(10)), key=lambda r: r[1])
sizes = shard_sizes(m[0], k)
strict = exact_partition(n, edges, k)
loose = exact_partition(n, edges, k, min_size=min(sizes), max_size=max(sizes))
print("METIS sizes", sizes, "cut", m[1])
print("exact strict 10/10 cut", strict[1], "| exact with METIS's size range cut", loose[1], loose[2])
assert loose[1] <= m[1] <= strict[1]
print("fair comparison: exact(same tolerance) <= metis <= exact(strict)")
