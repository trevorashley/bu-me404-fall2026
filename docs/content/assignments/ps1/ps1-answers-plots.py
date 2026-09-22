"""Regenerate the figures and numerically check the PS1 answer key.

Requires NumPy, SciPy, and Matplotlib. Run: python ps1-answers-plots.py
"""

import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ps1-mpl"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import residue

OUT = Path(__file__).resolve().parent / "ps1-answers-figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 170})
t = np.linspace(0, 30, 6001)


def simulate(initial, b=0.5, m2=1.0, force=0.0, times=t):
    def rhs(_, z):
        x1, x2, v1, v2 = z
        coupling = 5 * (x2 - x1) + b * (v2 - v1)
        return [v1, v2, force - 10 * x1 + coupling,
                (-10 * x2 - coupling) / m2]

    sol = solve_ivp(rhs, (0, times[-1]), [*initial, 0, 0],
                    t_eval=times, rtol=1e-10, atol=1e-12)
    assert sol.success
    return sol.y


def differential_response(b):
    if b < np.sqrt(20):
        wd = np.sqrt(20 - b*b)
        return np.exp(-b*t) * (np.cos(wd*t) + b/wd*np.sin(wd*t))
    if b == np.sqrt(20):
        return np.exp(-b*t) * (1 + b*t)
    d = np.sqrt(b*b - 20)
    r1, r2 = -b + d, -b - d
    return (-r2*np.exp(r1*t) + r1*np.exp(r2*t)) / (r1-r2)


def panel(ax, times, values, title, ylim=(-1.2, 1.2)):
    ax.plot(times, values[0], color="#1769aa", lw=1.3, label=r"$x_1$")
    ax.plot(times, values[1], color="#c45118", lw=1.3, ls="--", label=r"$x_2$")
    ax.set(title=title, xlabel="Time (s)", ylabel="Displacement (m)",
           xlim=(times[0], times[-1]), ylim=ylim)
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right", ncol=2)


common = np.cos(np.sqrt(10)*t)
diff = differential_response(0.5)
closed = [np.array([common, common]), np.array([diff, -diff]),
          np.array([(common+diff)/2, (common-diff)/2])]
initials = [(1, 1), (1, -1), (1, 0)]
fig, axes = plt.subplots(3, 1, figsize=(10, 8.2), constrained_layout=True)
max_error = 0
for i, (ax, initial, exact) in enumerate(zip(axes, initials, closed), 1):
    numerical = simulate(initial)[:2]
    max_error = max(max_error, np.max(np.abs(numerical-exact)))
    np.testing.assert_allclose(numerical, exact, atol=2e-8, rtol=0)
    panel(ax, t, exact, f"Case {i}: initial displacements {initial} m")
fig.savefig(OUT / "part-3e.png")
plt.close(fig)

fig, axes = plt.subplots(3, 2, figsize=(12, 9), constrained_layout=True)
for row, b in enumerate([0, 2, 10]):
    diff_b = differential_response(b)
    for col, (case, initial) in enumerate([(1, (1, 1)), (3, (1, 0))]):
        exact = (np.array([common, common]) if case == 1 else
                 np.array([(common+diff_b)/2, (common-diff_b)/2]))
        numerical = simulate(initial, b=b)[:2]
        np.testing.assert_allclose(numerical, exact, atol=2e-8, rtol=0)
        panel(axes[row, col], t, exact, f"Case {case}, b = {b} N s/m")
fig.savefig(OUT / "part-3f-damping.png")
plt.close(fig)

den = [3, 2, 60, 10, 200]
poles = np.roots(den)
assert np.all(poles.real < 0)
print("Asymmetric-system poles:", poles)
fig, axes = plt.subplots(2, 1, figsize=(10, 6.3), constrained_layout=True)
for ax, case, initial, nums in zip(
        axes, [1, 3], [(1, 1), (1, 0)],
        [([3, 2, 30, 0], [3, 2, 50, 0]),
         ([3, 2, 15, 5], [5, -5])]):
    values = simulate(initial, m2=3)
    for i, num in enumerate(nums):
        residues, roots, direct = residue(num, den)
        assert len(direct) == 0
        exact = np.sum(residues[:, None] * np.exp(roots[:, None]*t), axis=0)
        np.testing.assert_allclose(values[i], exact.real, atol=2e-8, rtol=0)
    panel(ax, t, values, f"Case {case}, m2 = 3 kg, b = 0.5 N s/m")
fig.savefig(OUT / "part-3f-asymmetric.png")
plt.close(fig)

step_t = np.linspace(0, 600, 60001)
step = simulate((0, 0), m2=3, force=1, times=step_t)
np.testing.assert_allclose(step[:2, -1], [0.075, 0.025], atol=1e-6, rtol=0)
print("Step response at 600 s:", step[:2, -1])
print("Maximum baseline closed-form / numerical discrepancy:", max_error)
fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
for ax, end, title in zip(axes, [30, 600], ["Initial transient", "Convergence to static equilibrium"]):
    use = step_t <= end
    panel(ax, step_t[use], step[:, use], title, ylim=(-0.005, 0.145))
    ax.axhline(0.075, color="#1769aa", lw=0.9, ls=":")
    ax.axhline(0.025, color="#c45118", lw=0.9, ls=":")
fig.savefig(OUT / "part-3g-step.png")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), constrained_layout=True)
for i, ax in enumerate(axes, 1):
    ax.set(xlim=(-2.5, 2.5), ylim=(-1.8, 1.8), aspect="equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-0.55, -0.45), 1.1, 0.9, fill=False, lw=1.5))
    ax.text(0, 0, f"Cart {i}", ha="center", va="center")

    def arrow(start, end, label, text_xy):
        ax.annotate("", xy=end, xytext=start,
                    arrowprops={"arrowstyle": "->", "lw": 1.4})
        ax.text(*text_xy, label, ha="center", va="center")

    arrow((0, 0.45), (0, 1.25), rf"$N_{i}$", (0.35, 1.15))
    arrow((0, -0.45), (0, -1.25), rf"$m_{i}g$", (0.45, -1.2))
    if i == 1:
        arrow((0.55, 0.25), (2, 0.25), "$u$", (1.5, 0.55))
        arrow((0.55, -0.25), (2, -0.25), "$F_c$", (1.5, -0.6))
        arrow((-0.55, 0), (-2, 0), "$k_1x_1$", (-1.5, 0.35))
    else:
        arrow((-0.55, 0.25), (-2, 0.25), "$F_c$", (-1.5, 0.6))
        arrow((-0.55, -0.25), (-2, -0.25), "$k_3x_2$", (-1.5, -0.6))
fig.savefig(OUT / "part-3a-fbd.png")
plt.close(fig)
print("All response checks passed; figures saved to", OUT)
