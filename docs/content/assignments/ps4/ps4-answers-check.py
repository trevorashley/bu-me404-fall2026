"""Verify the PS4 answer key and regenerate its figures.

Run with Python 3, NumPy, SciPy, SymPy, and Matplotlib installed:
    python ps4-answers-check.py

An assertion failure indicates a mismatch with the key; a successful run
prints the measured quantities and writes the figures to ps4-answers-figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.signal import step

OUT = Path(__file__).resolve().parent / "ps4-answers-figures"
s = sp.symbols("s")
R = sp.Rational


def equal(left, right):
    assert sp.simplify(sp.cancel(left - right)) == 0, (left, right)


def metrics(num, den, end, n=400001, final=None):
    """Overshoot (%), peak time, and 1% settling time of a unit-step response."""
    t = np.linspace(0, end, n)
    _, y = step((num, den), T=t)
    if final is None:
        final = num[-1] / den[-1]
    outside = np.flatnonzero(np.abs(y - final) > 0.01 * abs(final))
    # A response that never enters the band has no settling time.
    settling = np.inf if outside[-1] == len(t) - 1 else t[outside[-1] + 1]
    return t, y, 100 * (y.max() - final) / abs(final), t[np.argmax(y)], settling


# ---------------------------------------------------------------- Problem 1
K, a, b, zeta = sp.symbols("K a b zeta", positive=True)
G = 1 / (s**2 + 2 * zeta * s + 1)
Dc = K * (s + a) / (s + b)
L = G * Dc
equal(sp.limit(s * L.subs(b, 0), s, 0), K * a)                      # K_v = K a
poly = sp.Poly(sp.expand(s * (s**2 + 2 * zeta * s + 1) + K * (s + a)), s)
c3, c2, c1, c0 = poly.all_coeffs()
assert (c3, c2, c1, c0) == (1, 2 * zeta, K + 1, K * a)
equal(c2 * c1 - c0, 2 * zeta * (1 + K) - K * a)                      # Routh s^1 entry numerator
roots = np.roots([1, 1, 3, 1])                                       # zeta=.5, a=.5, K=2
assert np.all(roots.real < 0)
np.testing.assert_allclose(sorted(roots.real), sorted([-0.3611, -0.3194, -0.3194]), atol=2e-4)

G = 1 / s**2
Dc = 10 * (s + 2) / (s + 5)
L = G * Dc
charpoly = sp.expand(sp.numer(sp.together(1 + L)))
equal(charpoly, s**3 + 5 * s**2 + 10 * s + 20)
roots = np.roots([1, 5, 10, 20])
assert np.all(roots.real < 0)
np.testing.assert_allclose(sorted(roots.real)[0], -3.7553, atol=1e-4)
assert sp.limit(s**2 * L, s, 0) == 4                                 # K_a
Tw = sp.cancel(-G / (1 + L))
equal(Tw, -(s + 5) / (s**3 + 5 * s**2 + 10 * s + 20))
assert Tw.subs(s, 0) == R(-1, 4)
ER = sp.cancel(1 / (1 + L))
equal(ER, s**2 * (s + 5) / (s**3 + 5 * s**2 + 10 * s + 20))
assert sp.limit(ER / s**2, s, 0) == R(1, 4)                           # parabola error 1/K_a

# ---------------------------------------------------------------- Problem 2
K0, K1, K2, K3 = sp.symbols("K0 K1 K2 K3", positive=True)
plant = K0 / (4 * s + 1)
Ea = sp.cancel(1 / (1 + K1 / s * plant))
equal(Ea, s * (4 * s + 1) / (4 * s**2 + s + K1 * K0))
assert sp.limit(Ea, s, 0) == 0
equal(sp.limit(Ea / s, s, 0), 1 / (K1 * K0))
Eb = sp.cancel(1 - K2 * K3 * plant / (1 + K3 * plant))
equal(Eb, (4 * s + 1 + K3 * K0 - K2 * K3 * K0) / (4 * s + 1 + K3 * K0))
K2sol = sp.solve(sp.limit(Eb, s, 0), K2)[0]
equal(K2sol, 1 + 1 / (K3 * K0))
Eb0 = sp.cancel(Eb.subs(K2, K2sol))
equal(sp.limit(Eb0 / s, s, 0), 4 / (1 + K3 * K0))
assert sp.solve(sp.Eq((4 / (1 + K3 * K0)).subs(K0, 1), 1), K3) == [3]
assert K2sol.subs({K0: 1, K3: 3}) == R(4, 3)
dK = sp.symbols("deltaK0")
step_b = sp.simplify(sp.limit(Eb.subs({K2: R(4, 3), K3: 3, K0: 1 + dK}), s, 0))
equal(step_b, -dK / (1 + 3 * (1 + dK)))
assert step_b.subs(dK, R(1, 10)) == R(-1, 43)
ta, ya, os_a, _, ts_a = metrics([1.0], [4.0, 1.0, 1.0], 60, 600001)
tb, yb, os_b, _, ts_b = metrics([4.0], [4.0, 4.0], 60, 600001)
assert abs(os_a - 44.43) < 0.1 and abs(ts_a - 34.54) < 0.05 and os_b < 1e-6 and abs(ts_b - 4.605) < 0.01
_, ya_p, *_ = metrics([1.1], [4.0, 1.0, 1.1], 60, 600001)
_, yb_p, *_ = metrics([4.0 * 1.1], [4.0, 1.0 + 3.3], 60, 600001, final=1.0)
np.testing.assert_allclose(ya_p[-1], 1.0, atol=1e-3)   # slow pole at -0.125: e^(-7.5) after 60 s
np.testing.assert_allclose(yb_p[-1], 1 + 1 / 43, atol=1e-6)
print(f"Problem 2: (a) overshoot {os_a:.2f}%, settling {ts_a:.2f} s; (b) settling {ts_b:.3f} s; "
      f"perturbed final outputs {ya_p[-1]:.6f} and {yb_p[-1]:.6f}")

# ---------------------------------------------------------------- Problem 3
a1, b0, c0 = 65, 200, 10
assert abs(b0 * 100 / a1 * 60 / (2 * np.pi) - 2938.2) < 0.1
zeta_min = np.log(1 / 0.17) / np.sqrt(np.pi**2 + np.log(1 / 0.17) ** 2)
assert abs(zeta_min - 0.4913) < 1e-4
Kc, TD = 200.0, 0.003375
den2 = [1.0, a1 + b0 * Kc * TD, b0 * Kc]
assert den2 == [1.0, 200.0, 40000.0]
np.testing.assert_allclose(np.roots(den2), [-100 + 100 * np.sqrt(3) * 1j, -100 - 100 * np.sqrt(3) * 1j])
predicted_os = 100 * np.exp(-np.pi / np.sqrt(3))
envelope = np.log(100 / np.sqrt(0.75)) / 100
t3, y3, os3, tp3, ts3 = metrics([b0 * Kc], den2, 0.2)
assert abs(os3 - predicted_os) < 1e-3 and ts3 < 0.05 and ts3 < envelope
assert abs(b0 * Kc / (a1 + b0 * Kc * TD) - 200) < 1e-9                # K_v
e_step_torque = -c0 / (b0 * Kc)
_, yw, *_ = metrics([c0], den2, 0.2)
np.testing.assert_allclose(-yw[-1], e_step_torque, rtol=1e-6)
kI = sp.symbols("k_I", positive=True)
Kc_s, TD_s = sp.Integer(200), R(27, 8000)
cubic = s**3 + (a1 + b0 * Kc_s * TD_s) * s**2 + b0 * Kc_s * s + b0 * kI
equal(cubic, s**3 + 200 * s**2 + 40000 * s + 200 * kI)
# Routh s^1 entry: (200*40000 - 200 kI)/200
equal((200 * 40000 - 200 * kI) / 200, 40000 - kI)
EW = -c0 * s / cubic
equal(sp.limit(s * EW / s**2, s, 0), -c0 / (b0 * kI))                 # ramp-torque error
ER3 = sp.cancel(1 - b0 * (Kc_s * s + kI) / cubic)
equal(ER3, s**2 * (s + 200) / cubic)
assert sp.limit(ER3 / s**2, s, 0).subs(kI, 4000) == R(200, 800000) * 1 and sp.limit(ER3 / s**2, s, 0) == 200 / (200 * kI) * 1
den3 = [1.0, 200.0, 40000.0, 800000.0]
roots3 = np.roots(den3)
np.testing.assert_allclose(sorted(roots3.real), sorted([-88.9057, -88.9057, -22.1886]), atol=1e-3)
tI = np.linspace(0, 0.5, 200001)
_, ywI = step(([c0, 0.0], den3), T=tI)
assert abs(ywI[-1]) < 1e-7 and abs(ywI.max() - 2.685e-4) < 2e-6
print(f"Problem 3: overshoot {os3:.4f}% (predicted {predicted_os:.4f}%), peak time {tp3:.5f} s, "
      f"1% settling {ts3:.5f} s (bound {envelope:.5f} s); step-torque error {-yw[-1]:.3e} rad; "
      f"with k_I: peak {ywI.max():.3e} rad at {tI[np.argmax(ywI)]:.4f} s")
print("All symbolic and numerical checks passed.")

# ---------------------------------------------------------------- Figures
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.25, "lines.linewidth": 1.7})
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
for ax, nominal, perturbed, title in [
    (axes[0], ya, ya_p, "System (a): integral control"),
    (axes[1], yb, yb_p, "System (b): input gain and proportional control"),
]:
    ax.plot(ta, nominal, color="#0072B2", label="nominal, $K_0 = 1$")
    ax.plot(ta, perturbed, color="#D55E00", ls="--", label="perturbed, $K_0 = 1.1$")
    ax.axhline(1, color="0.3", lw=0.9, ls=":")
    ax.set(xlabel="Time (s)", ylabel="Output y(t)", title=title, xlim=(0, 40), ylim=(0, 1.6))
    ax.legend(loc="lower right")
fig.savefig(OUT / "problem-2-step.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
ax.plot(t3, y3, color="#0072B2", label=r"$\theta_m(t)$")
ax.axhline(1, color="0.3", ls="--", lw=0.9, label="final value 1 rad")
ax.axhspan(0.99, 1.01, color="#009E73", alpha=0.2, label="1% band")
ax.plot(tp3, y3.max(), "o", color="#D55E00", label=f"peak {y3.max():.4f} at {tp3*1e3:.1f} ms")
ax.axvline(ts3, color="#6C54A3", ls=":", label=f"1% settling {ts3*1e3:.1f} ms")
ax.set(xlabel="Time (s)", ylabel="Shaft angle (rad)", xlim=(0, 0.08), ylim=(0, 1.3),
       title="Unit-step reference, K = 200 V/rad, T_D = 3.375 ms")
ax.legend(loc="lower right", fontsize=9)
fig.savefig(OUT / "problem-3-reference.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
ax.plot(t3 * 1e3, yw * 1e3, color="#0072B2", label="P + rate feedback")
ax.plot(tI * 1e3, ywI * 1e3, color="#D55E00", label="with integral action, $k_I$ = 4000")
ax.axhline(0.25, color="0.3", ls="--", lw=0.9, label="predicted offset 0.25 mrad")
ax.axhline(0, color="0.3", lw=0.8)
ax.set(xlabel="Time (ms)", ylabel="Shaft angle (mrad)", xlim=(0, 200), title="Unit-step load torque, 1 N·m")
ax.legend(loc="upper right")
fig.savefig(OUT / "problem-3-disturbance.png", dpi=180)
plt.close(fig)
print(f"Figures written to {OUT}")
