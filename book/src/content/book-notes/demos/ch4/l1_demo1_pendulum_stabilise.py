"""
Feedback properties Demo 1  --  Open loop cannot stabilise; feedback can           (FPE §4.1.1)

The inverted pendulum of §4.1.1 has G(s) = 1/(s^2 - 1), with a pole at +1.

  Open loop.  Try to "fix" the plant with D_ol = (s - 1)/(s + 2), whose zero
  cancels the unstable pole. The reference path G D_ol = 1/[(s+1)(s+2)] looks
  perfectly stable. But a disturbance W enters at the plant input and never
  passes through D_ol: a bias of one-thousandth of a unit produces
  0.001 (cosh t - 1), which is 11 by t = 10 s.

  Feedback.  D_cl = K (s + gamma)/(s + delta) with gamma = 1 cancels the
  *stable* pole at -1. The book's exercise asks for K and delta that put the
  remaining pair at zeta, omega_n; the answer is delta = 1 + 2 zeta omega_n and
  K = omega_n^2 + 2 zeta omega_n + 1. With zeta = 0.5, omega_n = 2: delta = 3,
  K = 7, and the same disturbance bias now settles at 3/4000 = 0.00075.

Run:  uv run python ch4/l1_demo1_pendulum_stabilise.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

W0 = 1e-3       # disturbance bias at the plant input


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("Feedback properties Demo 1 -- the inverted pendulum, open loop and closed loop")

    # ------------------------------------------------ the exercise, solved
    dk.section("the book's exercise: place the pair at zeta, omega_n")
    zeta, wn = 0.5, 2.0
    delta = 1 + 2 * zeta * wn
    K = wn**2 + 2 * zeta * wn + 1
    print(f"  (s-1)(s+delta) + K = s^2 + (delta-1)s + (K-delta)")
    print(f"  match s^2 + 2 zeta wn s + wn^2  ->  delta = 1 + 2 zeta wn = {delta:g}")
    print(f"                                    K     = wn^2 + delta     = {K:g}")
    full = np.polyadd(np.polymul(np.polymul([1, 1], [1, -1]), [1, delta]),
                      K * np.array([1, 1.0]))
    roots = np.sort_complex(np.roots(full))
    print("  full characteristic polynomial (s+1)(s-1)(s+3) + 7(s+1), roots: "
          + ", ".join(dk.fmt_root(r, 4) for r in roots))
    dk.note("The root at -1 is the cancelled plant pole. It is still a pole of "
            "the system -- Eq. (4.16) keeps it -- but it is stable, so the "
            "cancellation is harmless.")

    # ------------------------------------------------ open loop
    t = np.linspace(0, 10, 4001)
    _, y_ol_r = step(lti([1], [1, 3, 2]), T=t)              # G D_ol R
    _, y_ol_w = step(lti([W0], [1, 0, -1]), T=t)            # G W
    y_ol = y_ol_r + y_ol_w

    # ------------------------------------------------ closed loop
    # T = 7/(s^2+2s+4) after the (s+1) cancellation;
    # G S = (s+3)/[(s+1)(s^2+2s+4)]
    _, y_cl_r = step(lti([K], [1, 2, 4]), T=t)
    den_w = np.polymul([1, 1], [1, 2, 4])
    _, y_cl_w = step(lti([W0, 3 * W0], den_w), T=t)
    y_cl = y_cl_r + y_cl_w

    dk.section(f"unit reference step plus a disturbance bias w = {W0:g}")
    rows = []
    for tt in [2, 5, 8, 10]:
        i = np.searchsorted(t, tt)
        rows.append([f"{tt:g}", f"{y_ol_w[i]:.4f}", f"{y_ol[i]:.4f}",
                     f"{y_cl_w[i]:.6f}", f"{y_cl[i]:.4f}"])
    dk.table(["t [s]", "open: y from w", "open: total y",
              "closed: y from w", "closed: total y"], rows)
    print(f"\n  open loop,   y from w = 0.001 (cosh t - 1): at 10 s "
          f"{W0 * (np.cosh(10) - 1):.3f}")
    print(f"  closed loop, y from w -> 3/4 x 0.001 = {0.75 * W0:.5f}")
    print(f"  closed loop, y from r -> T(0) = 7/4 = {K / 4:.3f}  "
          "(stabilised, not yet a good tracker)")

    dk.note("The open-loop cancellation removed the unstable pole from the "
            "reference path only. The disturbance path is G itself, and no "
            "open-loop controller can touch it. Feedback moves the pole.")

    # ------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.4))

    axL.plot(t, y_ol_r, color=dk.C["blue"], label=r"from $r$ only: $1/[(s+1)(s+2)]$")
    axL.plot(t, y_ol, color=dk.C["red"], label=rf"with $w={W0:g}$ at the plant input")
    axL.set_ylim(-0.2, 3.0)
    axL.set_xlabel("time [s]")
    axL.set_ylabel(r"output $y$")
    axL.set_title(r"Open loop, $D_{ol}=(s-1)/(s+2)$")
    axL.legend(fontsize=10.5, loc="upper left")

    axR.plot(t, y_cl_r, color=dk.C["blue"], label=r"from $r$ only: $7/(s^2+2s+4)$")
    axR.plot(t, y_cl, "--", color=dk.C["red"], label=rf"with $w={W0:g}$")
    axR.axhline(1.75, ls=":", color="k", lw=1.0)
    axR.set_ylim(-0.2, 3.0)
    axR.set_xlabel("time [s]")
    axR.set_title(r"Feedback, $D_{cl}=7(s+1)/(s+3)$")
    axR.legend(fontsize=10.5, loc="upper left")

    fig.suptitle(r"Inverted pendulum $G=1/(s^2-1)$: cancellation fails open loop, "
                 "feedback stabilises", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo1_pendulum_stabilise", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
