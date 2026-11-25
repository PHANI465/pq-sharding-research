"""M4: exact CP-SAT on a 20-account graph; also a 30- and 40-account timing for T10 planning."""
from common import planted_two_groups, exact_partition, metis_partition
for npg in (10, 15, 20):
    n, edges, truth = planted_two_groups(npg, seed=1)
    a, c, st, secs = exact_partition(n, edges, 2, time_limit=120)
    mc = metis_partition(n, edges, 2, seed=0)[1]
    print(f"n={n:>2} edges={len(edges):>3} exact cut={c} status={st} time={secs:.2f}s  metis cut={mc}")
    assert st == "OPTIMAL"
print("M4 OK")
