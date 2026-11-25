"""M5 follow-up: does the QUBO balance penalty (lam) behave on HARDER graphs than the planted one?
Compares simulated annealing with the exact solver on random heavy-tailed graphs, over a sweep of lam."""
import numpy as np
from common import *

rng = np.random.default_rng(0)
n = 20
edges = {(i, j): int(rng.pareto(1.5) * 100) + 1
         for i in range(n) for j in range(i + 1, n) if rng.random() < 0.25}
exact = exact_partition(n, edges, 2)[1]
print(f"n={n} edges={len(edges)} total weight={sum(edges.values())} max edge={max(edges.values())} exact cut={exact}")
print("lam      best balanced cut   gap vs exact   lowest-energy sample balanced?")
for lam in (1, 10, 50, 100, 500, 1000, 5000, 20000):
    ss = anneal(qubo_two_shard(n, edges, lam), num_reads=300, seed=0)
    bf = best_feasible_two_shard(ss, n, edges)
    low = decode_two_shard(ss.first.sample, n)
    cut = bf[1] if bf else None
    gap = f"{100 * (cut - exact) / exact:+.1f}%" if cut else "no balanced sample"
    print(f"{lam:<9}{str(cut):<20}{gap:<22}{is_balanced(low, 2)}")
