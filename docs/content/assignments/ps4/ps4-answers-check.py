"""Verify the PS4 answer key and regenerate its figures.

Run with the repository virtual environment (NumPy, SymPy, Matplotlib only):
    python ps4-answers-check.py

The closed-form results for Problems 2-10 quoted in ps4-answers.md are rederived
symbolically here (Problem 1 and the explanatory prose are not checked), and the
time-domain specifications are measured using a fourth-order Runge-Kutta integration
of a phase-variable state model, so that no result depends on a control-systems
library. The student-facing MATLAB equivalent is ps4_answers.m, which was run in
MATLAB R2026a and agrees with these results.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

OUT = Path(__file__).resolve().parent / "ps4-answers-figures"
INK, REF, GRID, ACCENT, ACCENT2 = "#1f2430", "#8a8f99", "#d9dce3", "#b4552d", "#2d6fb4"
s = sp.symbols("s")


# --------------------------------------------------------------------------- #
# Numerical helpers
# --------------------------------------------------------------------------- #
def simulate(num, den, t, u):
    """Response of num(s)/den(s) to the sampled input u(t) from rest, by RK4."""
    num = np.atleast_1d(np.asarray(num, float))
    den = np.atleast_1d(np.asarray(den, float))
    num, den = num / den[0], den / den[0]
    n = len(den) - 1
    num = np.concatenate([np.zeros(n + 1 - len(num)), num])
    A = np.zeros((n, n))
    A[0, :] = -den[1:]
    A[1:, :-1] = np.eye(n - 1)
    B = np.zeros(n)
    B[0] = 1.0
    D = num[0]
    C = num[1:] - num[0] * den[1:]
    x = np.zeros(n)
    y = np.empty_like(t)
    dt = t[1] - t[0]
    for k in range(len(t)):
        y[k] = C @ x + D * u[k]
        uk, uh, u1 = u[k], 0.5 * (u[k] + u[min(k + 1, len(t) - 1)]), u[min(k + 1, len(t) - 1)]
        k1 = A @ x + B * uk
        k2 = A @ (x + dt / 2 * k1) + B * uh
        k3 = A @ (x + dt / 2 * k2) + B * uh
        k4 = A @ (x + dt * k3) + B * u1
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


def step(num, den, t):
    return simulate(num, den, t, np.ones_like(t))


def specs(num, den, tend=None, n=40001):
    """10-90% rise time, overshoot, peak time, 1% settling time, final value, minimum."""
    poles = np.roots(den)
    if tend is None:
        tend = 12 / min(abs(poles.real))
    t = np.linspace(0, tend, n)
    y = step(num, den, t)
    yf = num[-1] / den[-1]
    i10, i90 = np.argmax(y >= 0.1 * yf), np.argmax(y >= 0.9 * yf)
    outside = np.abs(y - yf) > 0.01 * abs(yf)
    ts = t[np.max(np.nonzero(outside)[0])] if outside.any() else 0.0
    return dict(tr=t[i90] - t[i10], Mp=(y.max() - yf) / yf, tp=t[np.argmax(y)], ts=ts, yf=yf, ymin=y.min())


def coeffs(expr):
    return [float(c) for c in sp.Poly(sp.expand(expr), s).all_coeffs()]


def closed_loop(L):
    """Numerator and denominator coefficient lists of L/(1+L)."""
    num, den = sp.fraction(sp.together(L))
    return coeffs(num), coeffs(sp.expand(num + den))


def routh(poly):
    """Routh array (list of rows) of a polynomial in s."""
    c = sp.Poly(sp.expand(poly), s).all_coeffs()
    n = len(c)
    width = (n + 1) // 2
    rows = [list(c[0::2]), list(c[1::2])]
    for r in rows:
        r.extend([0] * (width - len(r)))
    for i in range(2, n):
        prev, prev2 = rows[i - 1], rows[i - 2]
        row = [sp.simplify((prev[0] * prev2[j + 1] - prev2[0] * prev[j + 1]) / prev[0]) for j in range(width - 1)]
        row.append(0)
        rows.append(row)
    return rows


def axes_style(ax):
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


# --------------------------------------------------------------------------- #
# Problem 2: magnetic levitation
# --------------------------------------------------------------------------- #
def problem2():
    m, g, k, x, i, KP, KD = sp.symbols("m g k x i K_P K_D", positive=True)
    f = g - k * i**2 / (m * x**2)
    vals = {m: sp.Rational(1, 10), g: 10, k: sp.Rational(1, 10000)}
    x0 = sp.Rational(1, 20)
    i0 = sp.solve(f.subs(vals).subs(x, x0), i)[0]
    fx = sp.diff(f, x).subs(vals).subs({x: x0, i: i0})
    fi = sp.diff(f, i).subs(vals).subs({x: x0, i: i0})
    assert (i0, fx, fi) == (5, 400, -4)
    assert sp.simplify(sp.diff(f, x).subs(k * i**2, m * g * x**2) - 2 * g / x) == 0
    assert sp.simplify(sp.diff(f, i).subs(k * i, m * g * x**2 / i) + 2 * g / i) == 0
    G = sp.simplify(fi / (s**2 - fx))
    assert sp.simplify(G + 4 / (s**2 - 400)) == 0
    doubling = sp.log(2) / 20  # asymptotic doubling time of the unstable mode
    first_doubling = sp.acosh(2) / 20  # released from rest: cosh(20 t) = 2
    # P control: s^2 - 400 + 4 K_P has no s term
    cp_pd = sp.expand(s**2 + 4 * KD * s + 4 * KP - 400)
    target = sp.expand((s + 20 + 20 * sp.I) * (s + 20 - 20 * sp.I))
    sol = sp.solve(sp.Poly(cp_pd - target, s).all_coeffs(), [KP, KD], dict=True)[0]
    assert sol == {KP: 300, KD: 10}
    print(f"Problem 2: i0 = {i0} A, delta-xdd = {fx} dx {fi} di, G = {G}, first doubling (from rest) = {float(first_doubling):.4f} s, later doublings = {float(doubling):.4f} s, PD gains {sol}")


# --------------------------------------------------------------------------- #
# Problem 3: six step responses
# --------------------------------------------------------------------------- #
PS4_SET = {
    "H1": ([25], [1, 6, 25]),
    "H2": ([25], [1, 2, 25]),
    "H3": ([100], list(np.polymul([1, 4], [1, 6, 25]))),
    "H4": ([-25 / 4, 25], [1, 6, 25]),
    "H5": ([12.5, 25], [1, 6, 25]),
    "H6": ([5], [1, 5]),
}
PANELS = dict(A="H4", B="H1", C="H6", D="H5", E="H3", F="H2")


def problem3():
    print("Problem 3: measured 10-90% rise, overshoot, 1% settling (s)")
    results = {}
    for name, (num, den) in PS4_SET.items():
        r = specs(num, den)
        results[name] = r
        print(f"   {name}: tr={r['tr']:.3f}  Mp={100 * r['Mp']:.1f}%  tp={r['tp']:.3f}  ts={r['ts']:.3f}  ymin={r['ymin']:.3f}")
    meets = {n: (r["Mp"] <= 0.10, r["tr"] <= 0.4, r["ts"] <= 1.5) for n, r in results.items()}
    print("   meets (Mp<=10%, tr<=0.4, ts<=1.5):", meets)
    assert [n for n, m in meets.items() if all(m)] == ["H1"]
    assert abs(results["H6"]["tr"] - np.log(9) / 5) < 2e-3
    assert abs(results["H1"]["Mp"] - np.exp(-0.6 * np.pi / np.sqrt(1 - 0.36))) < 1e-3
    assert abs(results["H2"]["Mp"] - np.exp(-0.2 * np.pi / np.sqrt(1 - 0.04))) < 1e-3
    return results


# --------------------------------------------------------------------------- #
# Problem 4: initial-value problems
# --------------------------------------------------------------------------- #
def problem4():
    t = sp.symbols("t", positive=True)
    y = sp.Function("y")
    cases = [
        (sp.Eq(y(t).diff(t, 2) + 3 * y(t).diff(t) + 2 * y(t), 4), {y(0): 1, y(t).diff(t).subs(t, 0): 0},
         2 - 2 * sp.exp(-t) + sp.exp(-2 * t), (s**2 + 3 * s + 4) / (s * (s + 1) * (s + 2))),
        (sp.Eq(y(t).diff(t, 2) + 4 * y(t), 8), {y(0): 0, y(t).diff(t).subs(t, 0): 2},
         2 - 2 * sp.cos(2 * t) + sp.sin(2 * t), (2 * s + 8) / (s * (s**2 + 4))),
        (sp.Eq(y(t).diff(t) + 2 * y(t), 2 * t), {y(0): 1},
         t - sp.Rational(1, 2) + sp.Rational(3, 2) * sp.exp(-2 * t), (s**2 + 2) / (s**2 * (s + 2))),
    ]
    for ode, ics, expected, Y in cases:
        sol = sp.dsolve(ode, y(t), ics=ics).rhs
        assert sp.simplify(sol - expected) == 0
        assert sp.simplify(sp.inverse_laplace_transform(Y, s, t) - expected) == 0
        print(f"   {sp.pretty(ode.lhs, use_unicode=False)} -> y(t) = {expected};  Y(s) = {sp.apart(Y, s)}")
    print("   (b) formal limit sY ->", sp.limit(s * cases[1][3], s, 0), "(not a final value)")
    print("   (c) lim [y - t] =", sp.limit(cases[2][2] - t, t, sp.oo))


# --------------------------------------------------------------------------- #
# Problem 5: two-loop block diagram
# --------------------------------------------------------------------------- #
def problem5():
    G1, G2, G3, H1, R, W, Y, K, kt = sp.symbols("G1 G2 G3 H1 R W Y K k_t")
    Ysol = sp.solve(sp.Eq(Y, G2 * (G1 * (R - Y) + G3 * R + W - H1 * Y)), Y)[0]
    YR, YW = sp.factor(sp.diff(Ysol, R)), sp.factor(sp.diff(Ysol, W))
    assert sp.simplify(YR - G2 * (G1 + G3) / (1 + G1 * G2 + G2 * H1)) == 0
    assert sp.simplify(YW - G2 / (1 + G1 * G2 + G2 * H1)) == 0
    ER = sp.simplify(1 - YR)
    assert sp.simplify(ER - (1 + G2 * H1 - G2 * G3) / (1 + G1 * G2 + G2 * H1)) == 0
    sub = {G1: K, G2: 1 / (s * (s + 2)), H1: kt * s, G3: 0}
    cp = sp.expand(sp.fraction(sp.together(YR.subs(sub)))[1])
    assert sp.expand(cp - (s**2 + (2 + kt) * s + K)) == 0
    cpn = cp.subs({K: 25, kt: 3})
    poles = sp.Poly(cpn, s).nroots()
    zeta = sp.Rational(5, 10)
    Mp = float(sp.exp(-zeta * sp.pi / sp.sqrt(1 - zeta**2)))
    ess = -sp.limit(YW.subs(sub).subs({K: 25, kt: 3}), s, 0)
    r = specs([25], [1, 5, 25])
    assert abs(r["Mp"] - Mp) < 1e-3 and ess == -sp.Rational(1, 25)
    G3_exact = sp.solve(sp.Eq(YR.subs({G1: K, G2: 1 / (s * (s + 2)), H1: kt * s}), 1), G3)[0]
    assert sp.expand(G3_exact - (s * (s + 2) + kt * s)) == 0
    print(f"Problem 5: Y/R = {YR}; Y/W = {YW}; poles(K=25,kt=3) = {[complex(p) for p in poles]}; zeta={float(zeta):.4f}; Mp={100 * Mp:.1f}%; e_ss(step W)={ess}; exact G3 = {sp.expand(G3_exact)}")


# --------------------------------------------------------------------------- #
# Problem 6: DC motor with rate feedback and integral action
# --------------------------------------------------------------------------- #
def problem6():
    a1, b0, c0 = 50, 100, 5
    K, TD, kI = sp.symbols("K T_D k_I", positive=True)
    cp = sp.expand(s**2 + (a1 + b0 * K * TD) * s + b0 * K)
    target = sp.expand((s + 50 + 50 * sp.I) * (s + 50 - 50 * sp.I))
    sol = sp.solve(sp.Poly(cp - target, s).all_coeffs(), [K, TD], dict=True)[0]
    assert sol == {K: 50, TD: sp.Rational(1, 100)}
    Kv = sp.Rational(b0 * 50, a1 + b0 * 50 * sp.Rational(1, 100))
    assert Kv == 50
    rpm = b0 * 100 / a1 * 60 / (2 * np.pi)
    den = [1, 100, 5000]
    r = specs([5000], den)
    assert r["Mp"] <= 0.05 and r["ts"] <= 0.1
    ess_w = -sp.Rational(c0, b0 * 50)
    cp3 = s**3 + 100 * s**2 + 5000 * s + b0 * kI
    rt = routh(cp3)
    kImax = sp.solve(rt[2][0], kI)[0]
    assert kImax == 5000
    poles3 = sp.Poly(cp3.subs(kI, 500), s).nroots()
    ramp_w = -sp.Rational(c0, b0) / 500
    print(f"Problem 6: K={sol[K]}, T_D={sol[TD]}, K_v={Kv}, 100 V -> {rpm:.0f} rpm; measured Mp={100 * r['Mp']:.2f}% ts={r['ts']:.4f} s tr={r['tr']:.4f} s; e_ss(step w)={ess_w} rad; Routh s^1 entry {rt[2][0]} -> k_I<{kImax}; poles(k_I=500)={[complex(p) for p in poles3]}; e_ss(ramp w)={ramp_w}")

    t = np.linspace(0, 0.15, 6001)
    y = step([5000], den, t)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.axhspan(0.99, 1.01, color=GRID, alpha=0.6, lw=0)
    ax.axhline(1, color=REF, ls="--", lw=1.2)
    ax.plot(t, y, color=INK, lw=2)
    ax.axvline(r["ts"], color=ACCENT, lw=1.2, ls=":")
    ax.annotate(f"1% settling at {r['ts']:.3f} s", (r["ts"], 0.3), xytext=(r["ts"] + 0.01, 0.3), color=ACCENT)
    ax.annotate(f"overshoot {100 * r['Mp']:.1f}%", (r["tp"], 1 + r["Mp"]), xytext=(r["tp"] + 0.015, 1.06), color=INK,
                arrowprops=dict(arrowstyle="-", color=REF))
    ax.set_xlabel("time (s)")
    ax.set_ylabel(r"$\theta_m$ (rad)")
    ax.set_title("Problem 6(g): unit-step reference response, K = 50, T_D = 0.01 s", loc="left")
    axes_style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "problem-6-reference.png", dpi=160)
    plt.close(fig)

    t = np.linspace(0, 0.5, 20001)
    y_no = step([c0], den, t)
    y_int = step([c0, 0], coeffs(cp3.subs(kI, 500)), t)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.axhline(c0 / 5000, color=REF, ls="--", lw=1.2)
    ax.plot(t, y_no, color=INK, lw=2, label="without integral action")
    ax.plot(t, y_int, color=ACCENT2, lw=2, label=r"with $k_I = 500$")
    ax.text(0.36, c0 / 5000 * 1.08, r"$c_0/(b_0K) = 0.001$ rad", color=REF)
    ax.set_xlabel("time (s)")
    ax.set_ylabel(r"$\theta_m$ (rad)")
    ax.set_title("Problem 6(g): response to a unit-step load torque", loc="left")
    ax.legend(frameon=False)
    axes_style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "problem-6-disturbance.png", dpi=160)
    plt.close(fig)
    assert abs(y_no[-1] - c0 / 5000) < 1e-6 and abs(y_int[-1]) < 2e-5


# --------------------------------------------------------------------------- #
# Problem 7: Routh and Ziegler-Nichols
# --------------------------------------------------------------------------- #
def problem7():
    K = sp.symbols("K", positive=True)
    G = 1 / (s * (s + 1) * (s + 4))
    cp = sp.expand(s * (s + 1) * (s + 4) + K)
    rt = routh(cp)
    Ku = sp.solve(rt[2][0], K)[0]
    wu = sp.sqrt(rt[1][1].subs(K, Ku) / rt[1][0])
    Pu = 2 * sp.pi / wu
    assert (Ku, wu) == (20, 2) and sp.factor(cp.subs(K, Ku)) == (s + 5) * (s**2 + 4)
    gains = {
        "P": (sp.Rational(1, 2) * Ku, None, None),
        "PI": (sp.Rational(45, 100) * Ku, Pu / sp.Rational(12, 10), None),
        "PID": (sp.Rational(6, 10) * Ku, Pu / 2, Pu / 8),
    }
    assert gains["PI"][0] == 9 and gains["PID"][0] == 12
    TI, TD = gains["PID"][1], gains["PID"][2]
    assert sp.factor(TI * TD * s**2 + TI * s + 1) == (sp.pi * s + 4)**2 / 16
    print(f"Problem 7: Routh {rt}; K_u={Ku}, w_u={wu}, P_u={Pu}; PID numerator factor {(sp.pi * s + 4)**2 / 16}, double zero at {-2 / TI}")
    t = np.linspace(0, 40, 40001)
    fig, ax = plt.subplots(figsize=(8, 4.4))
    colors = {"P": INK, "PI": ACCENT, "PID": ACCENT2}
    for name, (kP, TI, TD) in gains.items():
        Dc = kP * (1 + (1 / (TI * s) if TI else 0) + (TD * s if TD else 0))
        num, den = closed_loop(Dc * G)
        poles = np.roots(den)
        r = specs(num, den, tend=200, n=200001)
        Kv = sp.limit(s * Dc * G, s, 0)
        print(f"   {name}: k_P={kP}, T_I={TI}, T_D={TD}; char poly {np.round(den, 4)}; poles {np.round(poles, 3)}; K_v={Kv}; Mp={100 * r['Mp']:.1f}% ts={r['ts']:.1f} s")
        assert np.all(poles.real < 0)
        ax.plot(t, step(num, den, t), color=colors[name], lw=2, label=f"{name}: overshoot {100 * r['Mp']:.0f}%")
    ax.axhline(1, color=REF, ls="--", lw=1.2)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("y(t)")
    ax.set_title("Problem 7(f): Ziegler-Nichols designs for G = 1/(s(s+1)(s+4))", loc="left")
    ax.legend(frameon=False)
    axes_style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "problem-7-zn-steps.png", dpi=160)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Problem 8: system type
# --------------------------------------------------------------------------- #
def problem8():
    K, a, b = sp.symbols("K a b", positive=True)
    G = 1 / ((s + 1) * (s + 2))
    Dc = K * (s + a) / s
    assert sp.limit(s * Dc * G, s, 0) == K * a / 2
    cp = sp.expand(s * (s + 1) * (s + 2) + K * (s + a))
    rt = routh(cp)
    assert sp.simplify(rt[2][0] - (K + 2 - K * a / 3)) == 0
    assert sp.factor(cp.subs({a: 1, K: 4})) == (s + 1) * (s**2 + 2 * s + 4)
    print(f"Problem 8A: char poly {cp}; Routh {rt}; a=1,K=4 -> {sp.factor(cp.subs({a: 1, K: 4}))}, K_v=2, ramp error 1/2")
    Dc = 8 * (s + 1) / (s + 4)
    G = 1 / s**2
    cp = sp.expand(s**2 * (s + 4) + 8 * (s + 1))
    assert sp.factor(cp) == (s + 2) * (s**2 + 2 * s + 4)
    Ka = sp.limit(s**2 * Dc * G, s, 0)
    YW = sp.factor(sp.simplify(G / (1 + Dc * G)))
    YW_out = sp.factor(sp.simplify(1 / (1 + Dc * G)))
    assert Ka == 2 and sp.limit(YW, s, 0) == sp.Rational(1, 2) and sp.limit(YW_out / s**2, s, 0) == sp.Rational(1, 2)
    print(f"Problem 8B: {sp.factor(cp)}; Routh {routh(cp)}; K_a={Ka}; Y/W(input)={YW}, e_ss=-1/2; Y/W(output)={YW_out}, Type 2 wrt W")


# --------------------------------------------------------------------------- #
# Problem 9: robustness of type and sensitivity
# --------------------------------------------------------------------------- #
def problem9():
    K0, K1, K2, K3, d = sp.symbols("K0 K1 K2 K3 delta", positive=True)
    P = K0 / (2 * s + 1)
    Ta = (K1 / s) * P / (1 + (K1 / s) * P)
    Tb = K2 * K3 * P / (1 + K3 * P)
    Ea, Eb = sp.simplify(1 - Ta), sp.simplify(1 - Tb)
    assert sp.simplify(Ea - s * (2 * s + 1) / (2 * s**2 + s + K0 * K1)) == 0
    assert sp.limit(Ea, s, 0) == 0 and sp.simplify(sp.limit(Ea / s, s, 0) - 1 / (K0 * K1)) == 0
    K2sol = sp.solve(sp.limit(Eb, s, 0), K2)[0]
    assert sp.simplify(K2sol - (1 + K0 * K3) / (K0 * K3)) == 0
    assert sp.simplify(sp.limit((Eb / s).subs(K2, K2sol), s, 0) - 2 / (1 + K0 * K3)) == 0
    nom = {K1: 2, K3: 3, K2: sp.Rational(4, 3)}
    pert = {**nom, K0: 1 + d}
    ramp_a = sp.simplify(sp.limit((Ea / s).subs(pert), s, 0))
    step_b = sp.simplify(sp.limit(Eb.subs(pert), s, 0))
    assert ramp_a.subs(d, sp.Rational(1, 10)) == sp.Rational(5, 11)
    assert step_b.subs(d, sp.Rational(1, 10)) == -sp.Rational(1, 43)
    Sa = sp.simplify(sp.limit(K0 / Ta * sp.diff(Ta, K0), s, 0))
    Sb = sp.simplify((K0 / Tb * sp.diff(Tb, K0)).subs(s, 0)).subs({K0: 1, K3: 3})
    SK2 = sp.simplify(K2 / Tb * sp.diff(Tb, K2))
    assert (Sa, Sb, SK2) == (0, sp.Rational(1, 4), 1)
    ra = specs([2], [2, 1, 2], tend=40)
    rb = specs([4], [2, 4])
    zeta = 0.25
    assert abs(ra["Mp"] - np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2))) < 1e-3
    print(f"Problem 9: ramp_a(d)={ramp_a}, step_b(d)={step_b}; sensitivities S_K0: a={Sa}, b={Sb}; S_K2={SK2}; specs a: Mp={100 * ra['Mp']:.1f}% ts={ra['ts']:.2f} s; b: Mp={100 * rb['Mp']:.1f}% ts={rb['ts']:.2f} s")
    t = np.linspace(0, 25, 25001)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axhline(1, color=REF, ls="--", lw=1.2)
    ax.plot(t, step([2], [2, 1, 2], t), color=INK, lw=2, label="(a) integral control, K_1 = 2")
    ax.plot(t, step([4], [2, 4], t), color=ACCENT2, lw=2, label="(b) input gain 4/3 and K_3 = 3")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("y(t)")
    ax.set_title("Problem 9(c): unit-step responses of the two nominal designs", loc="left")
    ax.legend(frameon=False)
    axes_style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "problem-9-steps.png", dpi=160)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Problem 10: sinusoids, harmonics and the low-pass filter
# --------------------------------------------------------------------------- #
def problem10():
    w = sp.symbols("omega", positive=True)
    G = 1 / (sp.Rational(1, 10) * s + 1)
    Gj = lambda om: complex(G.subs(s, sp.I * om))
    for om in (10, 30, 50):
        print(f"   |G(j{om})| = {abs(Gj(om)):.4f}, angle = {np.degrees(np.angle(Gj(om))):.2f} deg")
    assert abs(abs(Gj(10)) - 1 / np.sqrt(2)) < 1e-12 and abs(np.degrees(np.angle(Gj(10))) + 45) < 1e-9
    # Fourier coefficients of the +-1 square wave, period T = pi/5
    t, k = sp.symbols("t", positive=True), sp.symbols("k", integer=True)
    T = sp.pi / 5
    w0 = 2 * sp.pi / T
    ck = (1 / T) * (sp.integrate(sp.exp(-sp.I * k * w0 * t), (t, 0, T / 2)) - sp.integrate(sp.exp(-sp.I * k * w0 * t), (t, T / 2, T)))
    for kk in (1, 2, 3, 5):
        val = sp.nsimplify(sp.simplify(ck.subs(k, kk)))
        expected = 2 / (sp.I * kk * sp.pi) if kk % 2 else 0
        assert sp.simplify(val - expected) == 0, (kk, val)
    amps_in = [4 / (kk * np.pi) for kk in (1, 3, 5)]
    amps_out = [4 / (kk * np.pi) * abs(Gj(10 * kk)) for kk in (1, 3, 5)]
    print(f"   input amplitudes {np.round(amps_in, 4)}, output amplitudes {np.round(amps_out, 4)}, ratio 3rd/1st: in {1 / 3:.4f}, out {amps_out[1] / amps_out[0]:.4f}")
    tt = np.linspace(0, 1.5, 15001)
    u = np.where(np.mod(tt, np.pi / 5) < np.pi / 10, 1.0, -1.0)
    y = simulate([1], [0.1, 1], tt, u)
    yss = sum(2 * np.real((2 / (1j * kk * np.pi)) * Gj(10 * kk) * np.exp(1j * 10 * kk * tt)) for kk in (1, 3, 5))
    late = tt > 1.0
    print(f"   max |y - y_ss(harmonics 1, 3, 5)| for t > 1 s: {np.max(np.abs(y[late] - yss[late])):.4f} (truncation only; the exact peak output is tanh(pi/2) = {np.tanh(np.pi/2):.4f})")
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.plot(tt, u, color=GRID, lw=1.5, label="square-wave input")
    ax.plot(tt, y, color=INK, lw=2, label="simulated output (switched on at t = 0)")
    ax.plot(tt, yss, color=ACCENT, lw=1.6, ls="--", label="periodic steady state, harmonics 1, 3, 5")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("u(t), y(t)")
    ax.set_title("Problem 10(e): square wave through 1/(0.1s+1)", loc="left")
    ax.legend(frameon=False, loc="lower right")
    axes_style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "problem-10-square-wave.png", dpi=160)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    problem2()
    problem3()
    print("Problem 4:")
    problem4()
    problem5()
    problem6()
    problem7()
    problem8()
    problem9()
    print("Problem 10:")
    problem10()
    print(f"All checks passed; figures written to {OUT}")


if __name__ == "__main__":
    main()
