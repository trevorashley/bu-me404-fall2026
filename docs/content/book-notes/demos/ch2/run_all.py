#!/usr/bin/env python3
"""Run every demo in order and regenerate all figures.

    uv run python run_all.py
"""

import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).parent
DEMOS = sorted(p.name for p in HERE.glob("demo?_*.py"))


def main() -> int:
    failed = []
    for name in DEMOS:
        print(f"\n>>> {name}")
        t0 = time.time()
        r = subprocess.run([sys.executable, str(HERE / name)],
                           capture_output=True, text=True)
        if r.returncode:
            failed.append(name)
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
            print(f"    FAILED after {time.time()-t0:.1f}s")
        else:
            print(f"    ok  ({time.time()-t0:.1f}s)")

    print("\n" + "=" * 60)
    if failed:
        print("FAILED:", ", ".join(failed))
        return 1
    print(f"All {len(DEMOS)} demos ran. Figures are in figures/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
