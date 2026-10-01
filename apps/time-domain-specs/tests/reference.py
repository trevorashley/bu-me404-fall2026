"""Cross-check the JavaScript simulator against scipy.signal on random systems.

Requires Node.js and a Python with NumPy/SciPy, e.g. the demos environment:

    book/src/content/book-notes/demos/.venv/bin/python apps/time-domain-specs/tests/reference.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess

import numpy as np
from scipy import signal

HERE = pathlib.Path(__file__).resolve().parent
LTI = (HERE.parent / "static" / "js" / "lti.js").as_uri()

rng = np.random.default_rng(404)


def random_system():
    poles, zeros = [], []
    for _ in range(rng.integers(1, 4)):
        if rng.random() < 0.5:
            poles.append({"re": -rng.uniform(0.2, 15), "im": 0.0})
        else:
            poles.append({"re": -rng.uniform(0.1, 8), "im": rng.uniform(0.3, 12)})
    order = sum(2 if p["im"] > 0 else 1 for p in poles)
    for _ in range(rng.integers(0, order + 1)):
        zorder = sum(2 if z["im"] > 0 else 1 for z in zeros)
        if zorder + 2 <= order and rng.random() < 0.3:
            zeros.append({"re": rng.uniform(-10, 10), "im": rng.uniform(0.3, 8)})
        elif zorder + 1 <= order:
            zeros.append({"re": rng.uniform(-12, 12), "im": 0.0})
    return {"poles": poles, "zeros": zeros, "gain": float(rng.uniform(0.5, 5))}


def expand(lst):
    out = []
    for r in lst:
        if r["im"] > 0:
            out += [complex(r["re"], r["im"]), complex(r["re"], -r["im"])]
        else:
            out.append(complex(r["re"], 0))
    return out


def main() -> None:
    systems = [random_system() for _ in range(40)]
    T, N = 6.0, 1201
    script = f"""
import {{ simulate }} from {json.dumps(LTI)};
const systems = {json.dumps(systems)};
const out = systems.map((s) => {{
  const r = {{ step: Array.from(simulate(s, {{ input: "step", T: {T}, N: {N} }}).y) }};
  const strictly = s.zeros.reduce((n, z) => n + (z.im > 0 ? 2 : 1), 0) < s.poles.reduce((n, p) => n + (p.im > 0 ? 2 : 1), 0);
  if (strictly) r.impulse = Array.from(simulate(s, {{ input: "impulse", T: {T}, N: {N} }}).y);
  return r;
}});
console.log(JSON.stringify(out));
"""
    js = json.loads(subprocess.run(["node", "--input-type=module", "-e", script],
                                   capture_output=True, text=True, check=True).stdout)
    t = np.linspace(0, T, N)
    worst = 0.0
    for sys_, res in zip(systems, js):
        z, p, k = expand(sys_["zeros"]), expand(sys_["poles"]), sys_["gain"]
        lti = signal.ZerosPolesGain(z, p, k).to_tf()
        _, ys = signal.step(lti, T=t)
        scale = max(1.0, np.max(np.abs(ys)))
        worst = max(worst, np.max(np.abs(ys - res["step"])) / scale)
        if "impulse" in res:
            _, yi = signal.impulse(lti, T=t)
            scale = max(1.0, np.max(np.abs(yi)))
            worst = max(worst, np.max(np.abs(yi - res["impulse"])) / scale)
    print(f"{len(systems)} random systems: worst relative deviation from scipy = {worst:.2e}")
    assert worst < 1e-6, "JavaScript and SciPy responses disagree"


if __name__ == "__main__":
    main()
