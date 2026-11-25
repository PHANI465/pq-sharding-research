"""Run every week-1 solver test in order. Usage (from repo root): python src/run_all.py"""
import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
tests = ["record_versions", "test_metis_smoke", "test_exact_cpsat", "test_qubo_sa", "test_known_answer",
         "test_worked_example", "test_control", "test_fair_balance"]   # test_exact_scaling is slow (about 2.5 min)
failed = []
for t in tests:
    print(f"\n=== {t}")
    r = subprocess.run([sys.executable, str(here / f"{t}.py")])
    if r.returncode: failed.append(t)
print("\nFAILED:" if failed else "\nALL PASSED", failed or "")
sys.exit(1 if failed else 0)
