"""
Feedback properties Demo 2  --  A perfect tracker with a lightly hidden disturbance response
                                                     (FPE §4.1.2 exercise)

The tracking exercise of §4.1.2: plant G = 1/(s^2 + 3s + 9), controller
D_cl = (c2 s^2 + c1 s + c0)/[s(s + d1)], closed-loop characteristic equation
(s + 6)(s + 3)(s^2 + 3s + 9) = 0. The book's answer is c2 = 18, c1 = 54,
c0 = 162, d1 = 9 -- and c2 s^2 + c1 s + c0 = 18(s^2 + 3s + 9). The controller
zeros cancel the plant poles exactly. So

    T   = 18/[(s+3)(s+6)]                       no overshoot, zero step error
    GS  = s(s+9)/[(s+3)(s+6)(s^2+3s+9)]         the plant's zeta = 0.5 pair
    D S = 18(s^2+3s+9)/[(s+3)(s+6)]             u(0+) = 18, u(inf) = 9

Tracking looks ideal, but the cancelled plant poles are still closed-loop
poles and they show up in the response to a load disturbance.

Run:  uv run python ch4/l1_demo2_hidden_poles.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk


def peak(t, y):
    i = int(np.argmax(np.abs(y)))
    return t[i], y[i]


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("Feedback properties Demo 2 -- the four transfer functions of one pole-placement design")

    plant_den = [1.0, 3.0, 9.0]
    target = np.polymul(np.polymul([1, 6], [1, 3]), plant_den)
    print("  target characteristic polynomial (s+6)(s+3)(s^2+3s+9) = "
          + " ".join(f"{c:+g}" for c in target))
    # s(s+d1)(s^2+3s+9) + c2 s^2 + c1 s + c0 = target, solved for d1, c2, c1, c0
    # the s^3 coefficient gives d1 + 3 = 12
    d1 = target[1] - 3.0
    lhs = np.polymul(np.polymul([1, 0], [1, d1]), plant_den)
    c = np.polysub(target, lhs)[-3:]
    print(f"  d1 = {d1:g},  (c2, c1, c0) = ({c[0]:g}, {c[1]:g}, {c[2]:g})"
          f"  = {c[0]:g} x (1, 3, 9)")

    t = np.linspace(0, 5, 5001)
    T = lti([18.0], np.polymul([1, 3], [1, 6]))
    GS = lti(np.polymul([1, 0], [1, 9]), target)
    DS = lti(18 * np.array(plant_den), np.polymul([1, 3], [1, 6]))
    _, yT = step(T, T=t)
    _, yW = step(GS, T=t)
    _, uR = step(DS, T=t)

    dk.section("responses to unit steps")
    tpk, ypk = peak(t, yW)
    under = float(np.min(yW))
    rows = [
        ["y from r  (T)", f"{np.max(yT):.4f}", f"{yT[-1]:.4f}", "none: poles -3, -6"],
        ["y from w  (GS)", f"{ypk:.4f} at {tpk:.3f} s", f"{yW[-1]:.4f}",
         f"undershoots to {under:.4f}"],
        ["u from r  (D S)", f"{uR[0]:.2f} at 0+", f"{uR[-1]:.4f}", "starts at 2x its final value"],
    ]
    dk.table(["response", "peak", "value at 5 s", "remark"], rows)
    pair = np.sort_complex(np.roots(plant_den))
    zeta = -pair[0].real / abs(pair[0])
    print(f"\n  plant poles, still closed-loop poles: "
          + ", ".join(dk.fmt_root(p, 3) for p in pair) + f"   (zeta = {zeta:.2f})")
    dk.note("T has only the two poles we asked for. The two we cancelled have not "
            "gone anywhere: they are in the characteristic equation, and the "
            "disturbance response G S rings at the plant's own damping. The "
            "integrator in D_cl does drive the step-disturbance error to zero, "
            "as the §4.1.3 exercise says it should.")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.9))
    ax0, ax1, ax2 = axes

    allp = np.roots(target)
    dk.splane(ax0, poles=allp, xlim=(-7, 1), ylim=(-3.6, 3.6),
              label_poles="closed-loop poles", title_text="Characteristic roots")
    ax0.plot(pair.real, pair.imag, "o", ms=20, mfc="none", mew=1.6,
             color=dk.C["orange"], label="cancelled in $T$")
    ax0.legend(fontsize=10, loc="lower left")

    ax1.plot(t, yT, color=dk.C["blue"], label=r"$y$ from $r$: $\mathcal{T}$")
    ax1.plot(t, yW, color=dk.C["red"], label=r"$y$ from $w$: $GS$")
    ax1.axhline(0, color="k", lw=0.8)
    ax1.axhline(1, color="k", lw=0.8, ls=":")
    ax1.set_xlabel("time [s]")
    ax1.set_title("Output")
    ax1.legend(fontsize=10.5)

    ax2.plot(t, uR, color=dk.C["green"], label=r"$u$ from $r$: $D_{cl}S$")
    ax2.axhline(9, color="k", lw=0.8, ls=":")
    ax2.set_xlabel("time [s]")
    ax2.set_title("Control effort")
    ax2.legend(fontsize=10.5)

    fig.suptitle(r"$G=1/(s^2+3s+9)$, $D_{cl}=18(s^2+3s+9)/[s(s+9)]$: "
                 "ideal tracking, plant dynamics in the disturbance response",
                 fontsize=14)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo2_hidden_poles", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
