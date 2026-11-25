# Solver setup note (M3, M9)

STATUS: tests below were run in Claude's workspace and on Phaneendra's device (Python 3.13, Linux). Meet must repeat them on his own
machine and fill the "Meet's machine" block. Phaneendra's Windows machine should also run src/run_all.py.

## Install (Windows, Python 3.11 or later, 64-bit)
```
python -m venv .venv
.venv\Scripts\activate
pip install pymetis ortools dwave-ocean-sdk networkx numpy
pip freeze > requirements.txt
python src/record_versions.py
python src/run_all.py
```
Binary builds of METIS or Ocean can fail on some Python versions or operating systems. Note any workaround here.

## Versions used in the workspace run
pymetis 2025.2.2, ortools 9.15.6755, dwave-ocean-sdk 9.5.0, dwave-samplers 1.8.0, dimod 0.12.22,
networkx 3.7, numpy 2.5.3, Python 3.13.18.

## Meet's machine (fill in)
Python ___, OS ___, pymetis ___, ortools ___, dwave-ocean-sdk ___, run_all result: ___ , problems: ___

## Run on Phaneendra's device, 2026-11-25 (Meet unavailable)
Fact: Python 3.13.18 (installed with uv) in a Linux virtual environment on Phaneendra's device, Ubuntu 22.04,
packages from requirements.txt. Versions: pymetis 2025.2.2, ortools 9.15.6755, dwave-ocean-sdk 9.5.0,
dwave-samplers 1.8.0, dimod 0.12.22, networkx 3.7, numpy 2.5.3. `python src/run_all.py`: ALL PASSED
(record_versions, M2, M4, M5, M6, M7, M8, fair-balance). Full pip freeze saved as requirements-lock.txt.
This is Linux, not Windows: the Windows install above is still to be repeated by whoever uses Windows.
Meet's own-machine block above stays open until he runs it.

## Results so far (Fact: observed in our own test runs; not from a paper)
- M2: PyMetis README example gives 3 cut edges. Pass.
- M4: CP-SAT is optimal in 0.02 s on the planted 20/30/40-account graphs, but those are easy.
  On random heavy-tailed graphs (25% edge density, test_exact_scaling.py): k=2 solves to optimal for n=20/30/40
  in 0.0/0.2/1.0 s; k=4 takes 1.2 s (n=20), 10.2 s (n=30), and n=40 was NOT proved optimal within 120 s.
  Planning figure for T10: 20 to 40 accounts is feasible for 2 shards; 4 shards at 40 accounts needs a longer
  time limit or a smaller graph. Timings depend on the machine.
- M5: QUBO + local simulated annealing recovers the exact cut on the planted graph for balance penalty
  0.1 to 100 and fails at 1000 (cut 84 vs 4: the penalty swamps the cut term). The "too small" failure did
  not show up on that easy graph, so we retested on a harder one (src/explore_penalty.py: random heavy-tailed
  graph, n=20, exact cut 1056, 300 reads). Result: lam=1 gave no balanced sample at all; lam=10 and 50 gave
  cut 1577 (+49%) with an unbalanced lowest-energy sample; lam=100, 500 and 1000 matched the exact cut (1056);
  lam=5000 gave 1367 (+29.5%) and lam=20000 gave 1571 (+48.8%). So the working window is narrow and depends on
  the weight scale (here max edge weight 1286, total 9224). The penalty must be tuned per graph or scaled to
  the weights, and the tuning must be reported. Real-data weights (bytes) are much larger, so lam cannot be
  reused from the toy graphs.
  One-hot formulation with k=4 also matched the exact cut (3) on a planted 4x5 graph.
- M6: METIS, exact and annealing agree on all 5 planted 2x10 graphs (same cut, same grouping).
- M7: four-account example reproduced exactly: before 3,700 B (cut transfer pairs) vs 4,260 B (cut call pairs);
  after 68,580 B vs 17,236 B. The best layout flips. These numbers come from our own derivation.
- M8: multiplying all weights by 10 leaves the METIS partition (5 seeds) and the exact partition unchanged;
  cuts scale exactly x10. Criterion 1 control passes on the toy graph.

## Fairness finding (M3): balance tolerance must match (IMPORTANT)
On a random 20-account graph, METIS returned an 11/9 split even with ufactor=1 (we tried default, 30, 5, 1,
with and without set_defaults and in recursive mode) and a cut of 988. Our exact solver enforced 10/10 and
returned 1056. That made METIS look better than "optimal". With the exact solver given the same size range
(9 to 11) it also returns 988. Why METIS allows 11/9 at ufactor=1 is Unknown (not checked in the manual).
RULE for all comparisons: report each solver's shard sizes, and run the exact solver with the size range
the compared heuristic actually produced (exact_partition(min_size=..., max_size=...)), or enforce the same
hard limit on every solver. See src/test_fair_balance.py.

## Integer scaling (M3)
METIS and CP-SAT need integer weights. Use ONE scale for all solvers (common.scale_to_int). At scale 1,
weights 1.004 and 1.000 both become 1 (the difference vanishes); at scale 1000 they stay distinct.
Uneven growth is a small-difference effect, so choose the scale after P5 fixes the message-size unit.

## Other notes
- pymetis deprecates passing xadj/adjncy; common.py uses pymetis.CSRAdjacency instead.
- Older D-Wave tutorials use `neal`; the current class is dwave.samplers.SimulatedAnnealingSampler.
- Seeds: METIS options.seed and SA seed are fixed in tests; the CP-SAT seed is 0.
