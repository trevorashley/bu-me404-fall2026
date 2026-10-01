"""Run each Chapter 5 demonstration and regenerate SVG/PNG figures."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
failed = []
for script in sorted(HERE.glob("l*_demo*.py")):
    print(f"\n>>> {script.name}", flush=True)
    result = subprocess.run([sys.executable, str(script)], cwd=HERE)
    if result.returncode:
        failed.append(script.name)
if failed:
    raise SystemExit("Failed: " + ", ".join(failed))
print("All seven Chapter 5 demos completed.")
