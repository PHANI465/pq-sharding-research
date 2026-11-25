"""M2: METIS on the PyMetis README example graph (7 nodes, 2 parts). README reports 3 cut edges."""
import numpy as np, pymetis
adjacency_list = [np.array([4, 2, 1]), np.array([0, 2, 3]),
                  np.array([4, 3, 1, 0]), np.array([1, 2, 5, 6]),
                  np.array([0, 2, 5]), np.array([4, 3, 6]), np.array([5, 3])]
n_cuts, membership = pymetis.part_graph(2, adjacency=adjacency_list)
print("pymetis version:", getattr(pymetis, "version", "unknown"))
print("cuts:", n_cuts, "membership:", membership)
assert n_cuts == 3, "expected 3 cut edges (PyMetis README)"
print("M2 OK")
