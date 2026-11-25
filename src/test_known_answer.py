"""M6: planted 2x10 graph. METIS, exact and annealing must all recover the two groups."""
from common import *
for seed in range(5):
    n, edges, truth = planted_two_groups(10, seed=seed)
    m = metis_partition(n, edges, 2, seed=0)
    e = exact_partition(n, edges, 2)
    ss = anneal(qubo_two_shard(n, edges, lam=20), num_reads=200, seed=0)
    bf = best_feasible_two_shard(ss, n, edges)
    ok = [same_partition(m[0], truth), same_partition(e[0], truth), bf is not None and same_partition(bf[0], truth)]
    print(f"seed {seed}: cuts metis={m[1]} exact={e[1]} sa={bf[1] if bf else None} | recovered truth: {ok}")
    assert all(ok) and m[1] == e[1] == bf[1]
print("M6 OK")
