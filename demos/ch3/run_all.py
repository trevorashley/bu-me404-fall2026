"""Run every Chapter 3 demo and regenerate its figure.

    uv run python ch3/run_all.py
"""

import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).parent


def main() -> None:
    scripts = sorted(p for p in HERE.glob("l*_demo*.py"))
    t0 = time.time()
    failed = []
    for script in scripts:
        print(f"\n>>> {script.name}")
        result = subprocess.run([sys.executable, str(script)],
                                cwd=HERE, capture_output=True, text=True)
        if result.returncode != 0:
            failed.append(script.name)
            print(result.stdout[-2000:])
            print(result.stderr[-2000:])
        else:
            print(result.stdout.strip().splitlines()[-1])
    print(f"\n{len(scripts) - len(failed)}/{len(scripts)} demos ran in "
          f"{time.time() - t0:.1f} s")
    if failed:
        print("failed: " + ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
