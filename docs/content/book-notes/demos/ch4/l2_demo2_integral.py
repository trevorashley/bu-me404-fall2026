"""
PID control Demo 2  --  Integral control: zero error whatever the plant
                                        (Section 4.3.2, Eqs. 4.64-4.69, Figs. 4.8, 4.9)

Pure integral control D_c = k_I / s around the same plant
G(s) = A / (s^2 + a1 s + a2). Three claims are checked by simulation:

  1. a unit step in r gives e(inf) = 0 and u(inf) = 1/G(0);
  2. a unit step disturbance at the plant input gives y(inf) = 0 and
     u(inf) = -1, cancelling it exactly (Fig. 4.9);
  3. both results survive large changes in the plant, as long as the loop
     stays stable; the Routh condition for that is k_I A < a1 a2.

Run:  uv run python ch4/l2_demo2_integral.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk

KI = 0.5
PLANTS = [  # (label, A, a1, a2)
    ("nominal  A=1, a1=1.4, a2=1", 1.0, 1.4, 1.0),
    ("A=2, a1=2.5, a2=3", 2.0, 2.5, 3.0),
    ("A=0.6, a1=2.0, a2=1.5", 0.6, 2.0, 1.5),
]


def char_poly(A, a1, a2, kI):
    return [1.0, a1, a2, kI * A]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("PID control Demo 2 -- integral control, D_c = k_I / s")

    t = np.linspace(0, 40, 8001)

    dk.section("reference and disturbance steps, three different plants")
    rows, ref, dist, uref = [], {}, {}, {}
    for label, A, a1, a2 in PLANTS:
        den = char_poly(A, a1, a2, KI)
        _, yr = step(lti([KI * A], den), T=t)             # Y/R
        _, ur = step(lti([KI, KI * a1, KI * a2], den), T=t)  # U/R
        _, yw = step(lti([A, 0.0], den), T=t)             # Y/W = sG/(s + k_I G)
        _, uw = step(lti([-KI * A], den), T=t)            # U/W
        ref[label], dist[label], uref[label] = yr, (yw, uw), ur
        rows.append([label, f"{1 - yr[-1]:+.4f}", f"{ur[-1]:.4f}",
                     f"{a2 / A:.4f}", f"{yw[-1]:+.4f}", f"{uw[-1]:+.4f}",
                     "yes" if KI * A < a1 * a2 else "NO"])
    dk.table(["plant", "e(40) ref", "u(40) ref", "1/G(0)", "y(40) dist",
              "u(40) dist", "k_I A < a1 a2"], rows)

    dk.note(
        "Every plant ends with zero error, and the steady control is exactly the inverse "
        "DC gain of whichever plant is in the loop. The integrator does not know the "
        "plant; it keeps pushing until the error it integrates is zero.")

    dk.section("nominal plant: peaks quoted in Figs. 4.8 and 4.9")
    yr = ref[PLANTS[0][0]]
    yw, uw = dist[PLANTS[0][0]]
    print(f"  reference: error minimum {1 - yr.max():+.3f} at t = {t[yr.argmax()]:.2f} s")
    print(f"  disturbance: y peak {yw.max():.3f} at t = {t[yw.argmax()]:.2f} s, "
          f"u minimum {uw.min():.3f} at t = {t[uw.argmin()]:.2f} s")

    dk.section("how far can k_I go?  s^3 + 1.4 s^2 + s + k_I")
    rows = []
    for kI in [0.5, 1.0, 1.4, 1.5]:
        r = np.roots(char_poly(1.0, 1.4, 1.0, kI))
        rows.append([f"{kI:g}", ", ".join(dk.fmt_root(z, 3) for z in np.sort_complex(r)),
                     f"{max(r.real):+.4f}"])
    dk.table(["k_I", "closed-loop roots", "max Re"], rows)
    dk.note("Routh: first column 1, 1.4, (1.4 - k_I)/1.4, k_I, so 0 < k_I < 1.4. At the "
            "boundary the pair sits at +/- j, the plant's own natural frequency.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.2))
    colours = [dk.C["blue"], dk.C["orange"], dk.C["green"]]
    for (label, *_), c in zip(PLANTS, colours):
        axes[0].plot(t, ref[label], color=c, label=label)
        axes[1].plot(t, dist[label][0], color=c, label=label)
        axes[2].plot(t, dist[label][1], color=c, label=label)
    axes[0].axhline(1.0, color="k", ls="--", lw=1.0)
    axes[0].set_title("Reference step: $y(t)$")
    axes[1].axhline(0.0, color="k", ls="--", lw=1.0)
    axes[1].set_title("Disturbance step: $y(t)$")
    axes[2].axhline(-1.0, color="k", ls="--", lw=1.0)
    axes[2].set_title("Disturbance step: $u(t)$")
    for ax in axes:
        ax.set_xlabel("time [s]")
    axes[0].legend(fontsize=9.5, loc="lower right")
    fig.suptitle(rf"Integral control, $k_I$ = {KI}: zero steady error for every plant",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo2_integral", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
