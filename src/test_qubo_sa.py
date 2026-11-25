"""M5: same problem as a QUBO, solved with local simulated annealing. Sweeps the balance penalty."""
from common import *
n, edges, truth = planted_two_groups(10, seed=1)
exact_cut = exact_partition(n, edges, 2)[1]
print("exact cut:", exact_cut, " max edge weight:", max(edges.values()))
print("lam   best-sample cut  balanced?  lowest-energy balanced?")
for lam in (0.1, 1, 5, 20, 100, 1000):
    ss = anneal(qubo_two_shard(n, edges, lam), num_reads=200, seed=0)
    low = decode_two_shard(ss.first.sample, n)
    bf = best_feasible_two_shard(ss, n, edges)
    print(f"{lam:<6}{cut_cost(edges, low):<17}{str(is_balanced(low,2)):<11}{bf[1] if bf else None}")
# k-shard one-hot formulation: 4 groups of 5
import numpy as np
rng = np.random.default_rng(3); k=4; per=5; n4=k*per; e4={}
for g in range(k):
    for a in range(per):
        for b in range(a+1, per): e4[(g*per+a, g*per+b)] = 10
for _ in range(6):
    a, b = rng.integers(0, n4, 2)
    if a//per != b//per: e4[(int(min(a,b)), int(max(a,b)))] = 1
ex4 = exact_partition(n4, e4, k, time_limit=120)
Q = qubo_k_shard(n4, e4, k, lam_onehot=50, lam_balance=20)
ss = anneal(Q, num_reads=500, seed=0)
dec = decode_k_shard(ss.first.sample, n4, k)
print("k=4: exact cut", ex4[1], "| SA lowest-energy valid one-hot:", dec is not None,
      "cut:", cut_cost(e4, dec) if dec else None, "balanced:", is_balanced(dec, k) if dec else None)
print("M5 done (inspect sweep: too small lam -> unbalanced, too large -> cut ignored)")
