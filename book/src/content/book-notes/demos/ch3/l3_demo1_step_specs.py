"""
L3 Demo 1  --  How good are t_r = 1.8/wn, M_p = e^..., t_s = 4.6/sigma?
                                                              (FPE §3.4)

The three design formulas of Section 3.4 are stated for a second-order system
with no zeros. Overshoot is exact under the stated assumptions; rise and settling
times are approximations. This script measures all three straight off simulated step responses
and puts the measurements beside the formulas.

    rise time    t_r ~ 1.8 / omega_n            (a fit, exact near zeta = 0.6)
    peak time    t_p = pi / omega_d             (exact)
    overshoot    M_p = e^{-pi zeta/sqrt(1-zeta^2)}   (exact)
    settling     t_s = 4.6 / sigma              (approximate decay-rate rule, not a guaranteed bound)

Run:  uv run python ch3/l3_demo1_step_specs.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk


def measure(zeta, wn, t_end=None, n=60000):
    """Rise, peak, overshoot and 1% settling time measured from the response."""
    sigma = zeta * wn
    t_end = t_end if t_end is not None else 12.0 / sigma
    t = np.linspace(0, t_end, n)
    _, y = step(lti([wn**2], [1.0, 2 * zeta * wn, wn**2]), T=t)

    t10 = t[np.argmax(y >= 0.1)]
    t90 = t[np.argmax(y >= 0.9)]
    tr = t90 - t10
    tp = t[np.argmax(y)]
    mp = max(0.0, y.max() - 1.0)
    outside = np.where(np.abs(y - 1.0) > 0.01)[0]
    ts = t[outside[-1] + 1] if len(outside) and outside[-1] + 1 < len(t) else (np.inf if len(outside) else 0.0)
    return tr, tp, mp, ts


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 1 -- the three time-domain formulas, measured")

    dk.section("rise time: the 1.8 is a fit, and here is its error")
    rows = []
    zetas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    wn_tr = []
    for z in zetas:
        tr, _, _, _ = measure(z, 1.0)
        wn_tr.append(tr)
        rows.append([f"{z:.1f}", f"{tr:.4f}", f"{1.8:.4f}",
                     f"{100*(1.8 - tr)/tr:+.1f}%"])
    dk.table(["zeta", "measured omega_n t_r", "formula 1.8", "formula error"], rows)
    from scipy.optimize import brentq
    z_match = brentq(lambda z: measure(z, 1.0)[0] - 1.8, 0.5, 0.7, xtol=1e-4)
    dk.note(
        f"The measured product omega_n t_r rises steadily with damping and passes "
        f"through 1.8 at zeta = {z_match:.2f}. So the book's constant is calibrated "
        "near zeta = 0.6, it over-estimates the rise time of a lightly damped system "
        "and under-estimates a heavily damped one. Use it to place omega_n, then "
        "simulate.")

    dk.section("peak time and overshoot: these two are exact")
    rows = []
    for z in [0.1, 0.3, 0.5, 0.7, 0.9]:
        wn = 4.0
        tr, tp, mp, ts = measure(z, wn)
        wd = wn * np.sqrt(1 - z**2)
        mp_f = np.exp(-z * np.pi / np.sqrt(1 - z**2))
        rows.append([f"{z:.1f}", f"{tp:.5f}", f"{np.pi/wd:.5f}",
                     f"{100*mp:.3f}%", f"{100*mp_f:.3f}%"])
    dk.table(["zeta", "t_p measured [s]", "pi/omega_d [s]",
              "M_p measured", "formula"], rows)
    print("\n  the two familiar rules of thumb: 16% overshoot at zeta = 0.5, "
          "5% at zeta = 0.7")

    dk.section("settling time: distinguish the 4.6/sigma estimate from the envelope bound")
    rows = []
    for z in [0.1, 0.3, 0.5, 0.7]:
        wn = 4.0
        _, _, _, ts = measure(z, wn)
        sigma = z * wn
        rows.append([f"{z:.1f}", f"{sigma:.2f}", f"{ts:.4f}", f"{4.6/sigma:.4f}",
                     f"{-np.log(0.01*np.sqrt(1-z*z))/sigma:.4f}"])
    dk.table(["zeta", "sigma [1/s]", "t_s measured (1%) [s]", "4.6/sigma [s]", "full envelope bound [s]"], rows)
    dk.note(
        "The measured settling time steps down in jumps as zeta changes, because the "
        "response leaves the 1% band at whichever oscillation peak happens to be the "
        "last one outside it. The 4.6/sigma rule drops the envelope prefactor and "
        "can underestimate settling time. The conservative underdamped envelope "
        "bound is -ln(0.01*sqrt(1-zeta^2))/sigma; compare the last two columns.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.2))

    zfine = np.linspace(0.05, 1.0, 36)
    trs = [measure(z, 1.0, n=40000)[0] for z in zfine]
    axes[0].plot(zfine, trs, color=dk.C["blue"], lw=2.4, label="measured")
    axes[0].axhline(1.8, ls="--", color=dk.C["red"], label="$1.8$")
    axes[0].set_xlabel(r"$\zeta$")
    axes[0].set_ylabel(r"$\omega_n t_r$")
    axes[0].set_title("Rise time: the fit and the truth")
    axes[0].legend(fontsize=10.5)

    zz = np.linspace(0.01, 0.99, 300)
    axes[1].plot(zz, 100 * np.exp(-zz * np.pi / np.sqrt(1 - zz**2)),
                 color=dk.C["blue"], lw=2.4)
    for z, mk in [(0.5, "16%"), (0.7, "5%")]:
        mp = 100 * np.exp(-z * np.pi / np.sqrt(1 - z**2))
        axes[1].plot([z], [mp], "o", color=dk.C["red"], ms=9)
        axes[1].annotate(f"$\\zeta$={z}: {mp:.0f}%", (z, mp),
                         textcoords="offset points", xytext=(8, 8), fontsize=10.5)
    axes[1].set_xlabel(r"$\zeta$")
    axes[1].set_ylabel("$M_p$ [%]")
    axes[1].set_title("Fig. 3.24: overshoot versus damping")

    t = np.linspace(0, 6, 4000)
    z, wn = 0.3, 4.0
    _, y = step(lti([wn**2], [1.0, 2 * z * wn, wn**2]), T=t)
    sigma = z * wn
    axes[2].plot(t, y, color=dk.C["blue"], lw=2.2, label="step response")
    axes[2].plot(t, 1 + np.exp(-sigma * t) / np.sqrt(1 - z**2), "--",
                 color=dk.C["red"], lw=1.3, label="envelope (Fig. 3.21)")
    axes[2].plot(t, 1 - np.exp(-sigma * t) / np.sqrt(1 - z**2), "--",
                 color=dk.C["red"], lw=1.3)
    axes[2].axhspan(0.99, 1.01, color=dk.C["green"], alpha=0.18)
    axes[2].axvline(4.6 / sigma, color=dk.C["grey"], lw=1.2)
    axes[2].text(4.6 / sigma + 0.08, 0.35, "$4.6/\\sigma$", fontsize=11,
                 color=dk.C["grey"])
    envelope_time = -np.log(0.01 * np.sqrt(1-z*z)) / sigma
    axes[2].axvline(envelope_time, color=dk.C["green"], ls=":",
                    label="full envelope bound")
    axes[2].set_ylim(0, 1.6)
    axes[2].set_xlabel("time [s]")
    axes[2].set_title(f"$\\zeta$ = {z}, $\\omega_n$ = {wn:g}: the 1% band")
    axes[2].legend(fontsize=10, loc="lower right")

    fig.suptitle("Time-domain specifications: exact peaks, approximate rise and settling",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo1_step_specs", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
