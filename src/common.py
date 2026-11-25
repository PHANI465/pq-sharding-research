"""Shared helpers for the three solvers (METIS, exact CP-SAT, QUBO + simulated annealing).

Graph format: n accounts numbered 0..n-1; `edges` is {(i, j): w} with i < j and integer w > 0.
All three solvers must see the SAME integer weights (METIS and CP-SAT both need integers).
"""
import time

import numpy as np
import pymetis
from ortools.sat.python import cp_model
from dwave.samplers import SimulatedAnnealingSampler


# ---------- weights ----------
def scale_to_int(real_weights, scale):
    """Round real-valued weights to positive integers after multiplying by `scale`.
    Rounding can hide small differences: pick one `scale` and use it for every solver."""
    return {e: max(1, int(round(w * scale))) for e, w in real_weights.items()}


# ---------- evaluation ----------
def cut_cost(edges, assign):
    return sum(w for (i, j), w in edges.items() if assign[i] != assign[j])


def shard_sizes(assign, k):
    return [sum(1 for a in assign if a == s) for s in range(k)]


def is_balanced(assign, k):
    n = len(assign)
    lo, hi = n // k, -(-n // k)  # floor, ceil
    return all(lo <= c <= hi for c in shard_sizes(assign, k))


def same_partition(a, b):
    """True if two assignments give the same grouping (shard labels may be swapped)."""
    mapping = {}
    for x, y in zip(a, b):
        if mapping.setdefault(x, y) != y:
            return False
    return len(set(mapping.values())) == len(mapping)


def normalise(assign):
    """Relabel shards in order of first appearance so equal groupings compare equal."""
    m, out = {}, []
    for a in assign:
        m.setdefault(a, len(m))
        out.append(m[a])
    return out


# ---------- METIS ----------
def metis_partition(n, edges, k, seed=0, ufactor=None):
    """Weighted METIS k-way partition. Returns (assignment, cut_cost_under_given_weights).
    ufactor = allowed imbalance in 1/1000 (30 = 3%); None keeps the METIS default."""
    nbrs = [[] for _ in range(n)]
    for (i, j), w in edges.items():
        nbrs[i].append((j, w))
        nbrs[j].append((i, w))
    xadj, adjncy, eweights = [0], [], []
    for lst in nbrs:
        for j, w in sorted(lst):
            adjncy.append(j)
            eweights.append(int(w))
        xadj.append(len(adjncy))
    opts = pymetis.Options()
    opts.seed = seed
    if ufactor is not None:
        opts.ufactor = ufactor
    _, membership = pymetis.part_graph(
        k, adjacency=pymetis.CSRAdjacency(xadj, adjncy), eweights=eweights, options=opts
    )
    return list(membership), cut_cost(edges, membership)


# ---------- exact (CP-SAT) ----------
def exact_partition(n, edges, k, time_limit=60.0, workers=8, min_size=None, max_size=None):
    """Exact minimum-cut k-way partition. Shard sizes default to floor(n/k)..ceil(n/k);
    pass min_size/max_size to give the exact solver the SAME tolerance METIS used (fair comparison).
    Account 0 is fixed to shard 0 to remove mirror-image solutions.
    Returns (assignment, cut_cost, status_name, seconds)."""
    m = cp_model.CpModel()
    x = [[m.NewBoolVar(f"x_{i}_{s}") for s in range(k)] for i in range(n)]
    for i in range(n):
        m.AddExactlyOne(x[i])
    lo = n // k if min_size is None else min_size
    hi = -(-n // k) if max_size is None else max_size
    for s in range(k):
        m.Add(sum(x[i][s] for i in range(n)) >= lo)
        m.Add(sum(x[i][s] for i in range(n)) <= hi)
    cut_vars = {}
    for (i, j) in edges:
        c = m.NewBoolVar(f"cut_{i}_{j}")
        for s in range(k):
            m.Add(c >= x[i][s] - x[j][s])
            m.Add(c >= x[j][s] - x[i][s])
        cut_vars[(i, j)] = c
    m.Add(x[0][0] == 1)
    m.Minimize(sum(int(w) * cut_vars[e] for e, w in edges.items()))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = workers
    solver.parameters.random_seed = 0
    t0 = time.time()
    status = solver.Solve(m)
    secs = time.time() - t0
    name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, name, secs
    assign = [next(s for s in range(k) if solver.Value(x[i][s])) for i in range(n)]
    return assign, cut_cost(edges, assign), name, secs


# ---------- QUBO ----------
def qubo_two_shard(n, edges, lam):
    """Two shards, one 0/1 variable per account (x_i = shard of i).
    cut = sum w (x_i + x_j - 2 x_i x_j);  balance penalty = lam * (sum x_i - n/2)^2 (constant dropped)."""
    Q = {}

    def add(a, b, v):
        key = (a, b) if a <= b else (b, a)
        Q[key] = Q.get(key, 0.0) + v

    for (i, j), w in edges.items():
        add(i, i, w)
        add(j, j, w)
        add(i, j, -2 * w)
    for i in range(n):
        add(i, i, lam * (1 - n))      # x^2 = x, so linear part of (sum x - n/2)^2
        for j in range(i + 1, n):
            add(i, j, 2 * lam)
    return Q


def qubo_k_shard(n, edges, k, lam_onehot, lam_balance):
    """One 0/1 variable per (account, shard), index i*k+s.
    cut = sum w (1 - sum_s x_is x_js); one-shard-per-account penalty; equal-size penalty."""
    Q = {}

    def add(a, b, v):
        key = (a, b) if a <= b else (b, a)
        Q[key] = Q.get(key, 0.0) + v

    idx = lambda i, s: i * k + s
    for (i, j), w in edges.items():
        for s in range(k):
            add(idx(i, s), idx(j, s), -w)
    for i in range(n):                                   # (sum_s x_is - 1)^2
        for s in range(k):
            add(idx(i, s), idx(i, s), -lam_onehot)
            for t in range(s + 1, k):
                add(idx(i, s), idx(i, t), 2 * lam_onehot)
    for s in range(k):                                   # (sum_i x_is - n/k)^2
        for i in range(n):
            add(idx(i, s), idx(i, s), lam_balance * (1 - 2 * n / k))
            for j in range(i + 1, n):
                add(idx(i, s), idx(j, s), 2 * lam_balance)
    return Q


def anneal(Q, num_reads=100, seed=0):
    ss = SimulatedAnnealingSampler().sample_qubo(Q, num_reads=num_reads, seed=seed)
    return ss


def decode_two_shard(sample, n):
    return [int(sample[i]) for i in range(n)]


def decode_k_shard(sample, n, k):
    """Returns assignment, or None if some account does not have exactly one shard."""
    out = []
    for i in range(n):
        on = [s for s in range(k) if sample[i * k + s] == 1]
        if len(on) != 1:
            return None
        out.append(on[0])
    return out


def best_feasible_two_shard(sampleset, n, edges):
    """Lowest-cut balanced assignment among all samples; None if none is balanced."""
    best = None
    for rec in sampleset.data(fields=["sample"]):
        a = decode_two_shard(rec.sample, n)
        if is_balanced(a, 2):
            c = cut_cost(edges, a)
            if best is None or c < best[1]:
                best = (a, c)
    return best


# ---------- test graphs ----------
def planted_two_groups(n_per_group=10, heavy=10, light=1, n_cross=4, seed=0):
    """Two groups of n_per_group accounts: heavy edges inside each group (ring + chords),
    a few light edges between groups. Known answer: the two groups."""
    rng = np.random.default_rng(seed)
    n = 2 * n_per_group
    edges = {}
    for g in range(2):
        base = g * n_per_group
        for a in range(n_per_group):
            for b in range(a + 1, n_per_group):
                if b == a + 1 or rng.random() < 0.5:       # ring plus random chords
                    edges[(base + a, base + b)] = heavy
    placed = 0
    while placed < n_cross:
        a, b = int(rng.integers(0, n_per_group)), int(rng.integers(n_per_group, n))
        if (a, b) not in edges:
            edges[(a, b)] = light
            placed += 1
    truth = [0] * n_per_group + [1] * n_per_group
    return n, edges, truth
