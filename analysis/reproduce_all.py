"""Run the complete release pipeline from repository root or any directory."""
from pathlib import Path
import os,subprocess,sys
base=Path(__file__).resolve().parents[1]
env=os.environ.copy()
env.setdefault("MPLCONFIGDIR",str(base/".mplcache"))
for name in ["count_taxonomy.py","run_analysis.py","verify_release.py","sensitivity.py","permutation_check.py","cluster_analysis.py","model_sensitivity.py","make_figures.py"]:
    print(f"Running {name}",flush=True)
    subprocess.run([sys.executable,str(base/"analysis"/name)],cwd=base,env=env,check=True)
print("All release calculations and figures regenerated successfully.")
