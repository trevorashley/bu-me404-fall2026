"""
Demo 9  --  A square wave is a sum of exponentials                (Addendum A)

A 0/1 square-wave force is built from its Fourier series, then used to drive
the spring-mass-damper of lecture §8. Each harmonic passes through G(jw) on its
own, so the steady-state motion is the sum of the scaled harmonics. The period
is chosen so the THIRD harmonic sits on the natural frequency: it becomes the
largest component of the motion, which still repeats with period T.

The last panel shows why a long pulse (a step, in the limit) needs the
e^{-sigma t} weight: without it, the integral of e^{-j w t} over 0 < t < L
never settles as L grows.

Plant: m = 1 kg, c = 1 N s/m, k = 25 N/m  (wn = 5 rad/s, zeta = 0.1).
Force: 0/1 N square wave, w0 = 5/3 rad/s.

Run:  uv run python demo9_square_wave_harmonics.py
"""

import numpy as np
from scipy.integrate import quad, solve_ivp

import demokit as dk

M, CD, K = 1.0, 1.0, 25.0
W0 = 5.0 / 3.0                  # fundamental, rad/s; 3*W0 = wn
T = 2 * np.pi / W0              # period, s
KMAX = 399                      # highest harmonic kept in the series


def G(s):
    return 1.0 / (M * s**2 + CD * s + K)


def coeff(k):
    """Complex Fourier coefficient of the 0/1 square wave (on for 0 < t < T/2)."""
    k = np.asarray(k)
    out = np.where(k % 2 == 1, 1.0 / (1j * np.pi * np.where(k == 0, 1, k)), 0.0)
    return np.where(k == 0, 0.5, out)


def square(t):
    return (np.mod(t, T) < T / 2).astype(float)


def partial_sum(t, N):
    """Square wave rebuilt from harmonics |k| <= N."""
    u = np.full_like(t, 0.5, dtype=float)
    for k in range(1, N + 1, 2):
        u += 2.0 / (np.pi * k) * np.sin(k * W0 * t)
    return u


def response_series(t, kmax=KMAX, only=None):
    """Steady-state displacement as the sum of scaled harmonics."""
    ks = [0] + list(range(1, kmax + 1, 2)) if only is None else list(only)
    x = np.zeros_like(t, dtype=float)
    for k in ks:
        if k == 0:
            x += 0.5 * G(0.0).real
        else:
            g = G(1j * k * W0)
            x += 2.0 / (np.pi * k) * abs(g) * np.sin(k * W0 * t + np.angle(g))
    return x


def simulate(n_periods):
    """ODE solve from rest, integrated one half-period at a time so the
    solver never steps across a switching instant."""
    z = np.array([0.0, 0.0])
    ts, xs = [], []
    for i in range(2 * n_periods):
        f = 1.0 if i % 2 == 0 else 0.0
        t0, t1 = i * T / 2, (i + 1) * T / 2
        te = np.linspace(t0, t1, 200, endpoint=(i == 2 * n_periods - 1))
        sol = solve_ivp(lambda tt, y: [y[1], (f - CD * y[1] - K * y[0]) / M],
                        (t0, t1), z, t_eval=te, dense_output=True,
                        rtol=1e-11, atol=1e-13)
        ts.append(sol.t)
        xs.append(sol.y[0])
        z = sol.sol(t1)
    return np.concatenate(ts), np.concatenate(xs)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    wn = np.sqrt(K / M)
    zeta = CD / (2 * np.sqrt(K * M))
    dk.title("Demo 9 -- a square wave is a sum of exponentials, and each one passes on its own")
    dk.note(
        f"Plant m = {M:g}, c = {CD:g}, k = {K:g}: wn = {wn:g} rad/s, zeta = {zeta:g}, "
        f"poles {dk.fmt_root(complex(np.roots([M, CD, K])[0]))} and conjugate. "
        f"Forcing: a 0/1 N square wave with w0 = {W0:.4f} rad/s (T = {T:.4f} s), "
        f"so the 3rd harmonic lands at {3 * W0:g} rad/s = wn.")

    # --------------------------------------------------- Fourier coefficients
    dk.section("coefficients by projection:  U_n = (1/T) * integral of u e^(-jn w0 t)")
    rows = []
    worst = 0.0
    for n in range(0, 8):
        # u = 1 only on the "on" half, so integrate there; quad never sees the jump.
        re = quad(lambda t: np.cos(n * W0 * t), 0, T / 2, epsabs=1e-13)[0] / T
        im = -quad(lambda t: np.sin(n * W0 * t), 0, T / 2, epsabs=1e-13)[0] / T
        exact = complex(coeff(n))
        worst = max(worst, abs(complex(re, im) - exact))
        rows.append([str(n), f"{re:+.5f}{im:+.5f}j",
                     f"{exact.real:+.5f}{exact.imag:+.5f}j"])
    dk.table(["n", "numerical U_n", "formula 1/(j pi n), odd n"], rows)
    print(f"\n  largest |numerical - formula| over n = 0..7: {worst:.1e}")

    # ----------------------------------------------------------------- Gibbs
    dk.section("partial sums near the jump (Gibbs)")
    tg = np.linspace(0, T / 2, 400001)
    rows = []
    for N in (1, 3, 9, 49, 199):
        peak = partial_sum(tg, N).max()
        rows.append([str(N), f"{peak:.4f}", f"{100 * (peak - 1):.2f} %"])
    dk.table(["highest harmonic N", "peak of partial sum", "overshoot of the jump"], rows)
    dk.note("The overshoot does not tend to zero as harmonics are added; it narrows "
            "toward the jump and approaches about 8.95 % of the jump. Away from the jump "
            "the sum converges, and at the jump itself it takes the midpoint value 1/2.")

    # --------------------------------------------------- harmonic-by-harmonic
    dk.section("each harmonic through G(j n w0)")
    rows = []
    for k in (0, 1, 3, 5, 7, 9):
        w = k * W0
        g = G(1j * w) if k else G(0.0)
        u_amp = 0.5 if k == 0 else 2 / (np.pi * k)
        rows.append([str(k), f"{w:.3f}", f"{u_amp:.4f}", f"{abs(g):.5f}",
                     f"{np.degrees(np.angle(g)):+.1f}", f"{u_amp * abs(g):.5f}"])
    dk.table(["n", "w [rad/s]", "force amp [N]", "|G| [m/N]", "phase [deg]",
              "motion amp [m]"], rows)
    a1 = 2 / np.pi * abs(G(1j * W0))
    a3 = 2 / (3 * np.pi) * abs(G(3j * W0))
    dk.note(f"The input's 3rd harmonic is one third the size of its fundamental, but "
            f"the output's 3rd harmonic is {a3 / a1:.2f} times the fundamental, because "
            f"3 w0 sits near the resonance peak. The motion still repeats with period T; "
            f"its largest component is simply not the fundamental.")
    zeta_ = CD / (2 * np.sqrt(K * M))
    wr = np.sqrt(K / M) * np.sqrt(1 - 2 * zeta_**2)
    print(f"\n  gain at wn = {abs(G(1j * np.sqrt(K / M))):.6f} m/N;  "
          f"peak gain = {abs(G(1j * wr)):.6f} m/N at w_r = {wr:.5f} rad/s")

    # ------------------------------------------------------ simulation check
    n_per = 20
    t_sim, x_sim = simulate(n_per)
    last = t_sim >= (n_per - 2) * T
    x_ser = response_series(t_sim[last])
    dk.section("the ODE knows nothing about harmonics; compare anyway")
    print(f"  simulated from rest for {n_per} periods ({n_per * T:.1f} s); "
          f"transient envelope factor e^(-{zeta * wn:g}t) at the window start = "
          f"{np.exp(-zeta * wn * (n_per - 2) * T):.1e}")
    print(f"  max |simulation - harmonic sum (n <= {KMAX})| at the sampled times, last two periods "
          f"= {np.max(np.abs(x_sim[last] - x_ser)):.2e} m")
    print(f"  peak-to-peak motion = {np.ptp(x_sim[last]):.5f} m")

    # --------------------------------------------- the step and e^{-sigma t}
    dk.section("one pulse of length L: the integral of e^(-st) from 0 to L")
    w = 2.0
    rows = []
    for sigma in (0.0, 0.5):
        s = sigma + 1j * w
        vals = [(1 - np.exp(-s * tf)) / s for tf in (5.0, 10.0, 20.0, 40.0)]
        rows.append([f"{sigma:g}"] + [f"{v.real:+.4f}{v.imag:+.4f}j" for v in vals]
                    + [f"{(1 / s).real:+.4f}{(1 / s).imag:+.4f}j" if sigma else "none"])
    dk.table(["sigma", "L = 5", "L = 10", "L = 20", "L = 40", "limit 1/s"], rows)
    dk.note("With sigma = 0 the pulse's transform keeps circling 1/(jw) at radius 1/|w| "
            "as the pulse lengthens toward a step, and never settles. With any sigma > 0 "
            "it spirals into 1/s. That weight is the only change between the Fourier "
            "integral and the Laplace transform.")

    # ------------------------------------------------------------------ figure
    fig, axs = plt.subplots(2, 2, figsize=(13.5, 9.5))
    ax_a, ax_b, ax_c, ax_d = axs.ravel()

    t2 = np.linspace(-0.25 * T, 1.75 * T, 6000)
    ax_a.plot(t2, square(t2), color="k", lw=1.4, label="square wave")
    for N, col in ((1, dk.C["sky"]), (3, dk.C["green"]), (9, dk.C["orange"]),
                   (49, dk.C["red"])):
        ax_a.plot(t2, partial_sum(t2, N), color=col, lw=1.7, label=f"harmonics up to {N}")
    ax_a.set_xlabel("time  [s]")
    ax_a.set_ylabel("force  [N]")
    ax_a.set_title("(a) Adding exponentials rebuilds the square wave")
    ax_a.legend(fontsize=10, ncol=2, loc="lower center")
    ax_a.set_ylim(-0.45, 1.3)

    wf = np.linspace(0.01, 12 * W0, 3000)
    g0 = abs(G(0.0))
    ns = np.arange(1, 12, 2)
    f_rel = 1.0 / ns                                     # force harmonic / force fundamental
    x_rel = f_rel * np.abs(G(1j * ns * W0)) / abs(G(1j * W0))   # motion harmonic / motion fundamental
    ax_b.semilogy(wf, np.abs(G(1j * wf)) / g0, color=dk.C["blue"], lw=2,
                  label=r"$|G(j\omega)|\,/\,|G(0)|$")
    ax_b.vlines(ns * W0 - 0.12, 1e-5, f_rel, color=dk.C["grey"], lw=5,
                label="force harmonic / force fundamental")
    ax_b.vlines(ns * W0 + 0.12, 1e-5, x_rel, color=dk.C["orange"], lw=5,
                label="motion harmonic / motion fundamental")
    ax_b.axhline(1, color="k", lw=0.8)
    ax_b.axvline(wn, color=dk.C["red"], lw=1, ls="--")
    ax_b.text(wn + 0.2, 7, r"$\omega_n = 3\omega_0$", color=dk.C["red"], fontsize=11)
    ax_b.set_ylim(3e-3, 20)
    ax_b.set_xticks(ns * W0)
    ax_b.set_xticklabels([rf"${n}\omega_0$" if n > 1 else r"$\omega_0$" for n in ns])
    ax_b.set_ylabel("ratio (dimensionless)")
    ax_b.set_title("(b) Each harmonic is scaled by G at its own frequency")
    ax_b.legend(fontsize=10, loc="upper right")

    tl = t_sim[last] - (n_per - 2) * T
    ax_c.plot(tl, x_sim[last], color=dk.C["green"], lw=3.4, label="ODE simulation")
    ax_c.plot(tl, x_ser, "--", color="k", lw=1.6, label="sum of scaled harmonics")
    ax_c.plot(tl, response_series(t_sim[last], only=[0, 1]), color=dk.C["sky"], lw=1.4,
              label="mean + fundamental only")
    ax_c.plot(tl, 0.5 * G(0.0).real + response_series(t_sim[last], only=[3]),
              color=dk.C["orange"], lw=1.4, label="mean + 3rd harmonic only")
    ax_c.set_xlabel("time within the last two periods  [s]")
    ax_c.set_ylabel("displacement  [m]")
    ax_c.set_title("(c) Steady state: period $T$, dominated by $3\\omega_0$")
    ax_c.set_ylim(-0.12, 0.1)
    ax_c.legend(fontsize=10, loc="lower center", ncol=2)

    for sigma, col, lab in ((0.0, dk.C["red"], r"$\sigma = 0$: never settles"),
                            (0.5, dk.C["blue"], r"$\sigma = 0.5$: converges to $1/s$")):
        s = sigma + 1j * w
        L = np.linspace(0, 40, 8000)
        I = (1 - np.exp(-s * L)) / s
        ax_d.plot(I.real, I.imag, color=col, lw=1.8, label=lab)
    ax_d.plot([(1 / (0.5 + 2j)).real], [(1 / (0.5 + 2j)).imag], "o", color=dk.C["blue"], ms=9)
    ax_d.plot([0], [-1 / w], "+", color=dk.C["red"], ms=14, mew=2.5)
    ax_d.set_aspect("equal")
    ax_d.set_ylim(-1.45, 0.1)
    ax_d.set_xlabel("real part")
    ax_d.set_ylabel("imaginary part")
    ax_d.set_title(r"(d) $\int_0^{L} e^{-st}dt$ as the pulse length $L$ grows, $\omega = 2$")
    ax_d.legend(fontsize=10, loc="lower center")

    fig.suptitle("Signals are sums of exponentials; LTI systems scale each one separately",
                 fontsize=15, y=0.995)
    fig.tight_layout()
    dk.finish(plt, fig, "demo9_square_wave_harmonics", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
