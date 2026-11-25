"""M9: print versions for docs/setup-solvers.md."""
import sys, platform, importlib.metadata as md
print("python", sys.version.split()[0], "|", platform.platform())
for p in ("pymetis", "ortools", "dwave-ocean-sdk", "dwave-samplers", "dimod", "networkx", "numpy"):
    try: print(p, md.version(p))
    except Exception as ex: print(p, "NOT INSTALLED", ex)
