"""
L1 Demo 3  --  Disturbance against noise: the regulation dilemma  (FPE §4.1.3)

Plant G = 1/(s + 1), proportional control D_cl = K, reference r = 0. Two
unwanted inputs arrive together:

  a constant load bias  w = 1           (all of it at zero frequency)
  a sensor noise        v = 0.1 sin 50t (all of it at 50 rad/s)

From Eq. (4.9) and (4.10) with r = 0:

    y = G S w - T v,     u = -T w - D S v

    G S(0)   = 1/(1 + K)                  bias left in the output
    |T(j50)| = K/|j50 + 1 + K|            noise passed to the output
    |DS(j50)| = K|j50 + 1|/|j50 + 1 + K|  noise passed to the actuator

Raising K fixes the first and worsens the other two. S + T = 1 is why the same
gain cannot make both small at the same frequency.

Run:  uv run python ch4/l1_demo3_regulation_tradeoff.py
"""

import numpy as np
from scipy.signal import lsim, lti

import kit as dk

W_BIAS = 1.0
V_AMP, V_W = 0.1, 50.0
GAINS = [1.0, 10.0, 100.0]
COLOURS = [dk.C["blue"], dk.C["orange"], dk.C["red"]]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L1 Demo 3 -- more gain rejects the bias and admits the noise")

    rows = []
    for K in GAINS:
        jw = 1j * V_W
        T = K / (jw + 1 + K)
        DS = K * (jw + 1) / (jw + 1 + K)
        rows.append([f"{K:g}", f"{1 / (1 + K):.4f}", f"{abs(T):.4f}",
                     f"{V_AMP * abs(T):.4f}", f"{V_AMP * abs(DS):.3f}",
                     f"{1 + K:g}"])
    dk.table(["K", "bias in y = 1/(1+K)", "|T(j50)|", "noise in y",
              "noise in u", "bandwidth 1+K [rad/s]"], rows)
    dk.note("At K = 100 the bias is down to 1% -- and 89% of the 50 rad/s sensor "
            "noise reaches the output, while the actuator is driven with a 4.4 "
            "amplitude sinusoid it did not need. That last number is the cost of "
            "feedback that the output plot does not show.")

    # ------------------------------------------------------ simulation
    t = np.linspace(0, 6, 60001)
    w = W_BIAS * np.ones_like(t)
    v = V_AMP * np.sin(V_W * t)
    sims = {}
    for K in GAINS:
        # x' = -x + u + w,  u = -K (x + v),  y = x
        A, B = [[-(1 + K)]], [[1.0, -K]]
        C, D = [[1.0], [-K]], [[0.0, 0.0], [0.0, -K]]
        _, out, _ = lsim((A, B, C, D), U=np.column_stack([w, v]), T=t)
        sims[K] = out
    dk.section("steady state: last ten noise periods of the simulation")
    tail = t >= t[-1] - 10 * 2 * np.pi / V_W
    rows = []
    for K in GAINS:
        y, u = sims[K][tail, 0], sims[K][tail, 1]
        rows.append([f"{K:g}", f"{y.mean():.4f}", f"{(y.max() - y.min()) / 2:.4f}",
                     f"{u.mean():+.4f}", f"{(u.max() - u.min()) / 2:.3f}"])
    dk.table(["K", "mean y", "y ripple amplitude", "mean u", "u ripple amplitude"], rows)

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0))
    ax0, ax1, ax2 = axes
    wgrid = np.logspace(-1, 3, 800)
    for K, col in zip(GAINS, COLOURS):
        L = K / (1j * wgrid + 1)
        S, T = 1 / (1 + L), L / (1 + L)
        ax0.loglog(wgrid, np.abs(S), color=col, label=rf"$|S|$, $K={K:g}$")
        ax0.loglog(wgrid, np.abs(T), "--", color=col, label=rf"$|\mathcal{{T}}|$, $K={K:g}$")
    ax0.axvline(V_W, color=dk.C["grey"], lw=1.0, ls=":")
    ax0.text(V_W * 1.08, 1.5e-3, "noise\n50 rad/s", fontsize=10, color=dk.C["grey"])
    ax0.set_ylim(1e-3, 2)
    ax0.set_xlabel(r"$\omega$ [rad/s]")
    ax0.set_title(r"$|S(j\omega)|$ solid, $|\mathcal{T}(j\omega)|$ dashed")
    ax0.legend(fontsize=8.5, ncol=2, loc="lower left")

    for K, col in zip(GAINS, COLOURS):
        ax1.plot(t, sims[K][:, 0], color=col, lw=1.4, label=f"K = {K:g}")
        ax2.plot(t, sims[K][:, 1], color=col, lw=1.2, label=f"K = {K:g}")
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_xlim(0, 3)
    ax1.set_xlabel("time [s]")
    ax1.set_title(r"Output $y$ (want 0)")
    ax1.legend(fontsize=10)
    ax2.set_xlim(0, 3)
    ax2.set_xlabel("time [s]")
    ax2.set_title(r"Control $u$")
    ax2.set_ylim(-6, 4)
    ax2.legend(fontsize=10, loc="upper right", ncol=3)

    fig.suptitle(r"$G=1/(s+1)$, $D_{cl}=K$: load bias $w=1$ and sensor noise "
                 r"$v=0.1\sin 50t$", fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo3_regulation_tradeoff", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
