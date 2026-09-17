"""
L4 Demo 3  --  Two gains at once: the stable region in a parameter plane
                                                            (Example 3.34)

PI control of 1/[(s+1)(s+2)] gives the characteristic equation

    s^3 + 3 s^2 + (2 + K) s + K_I = 0,

and Routh's array turns stability into two inequalities in the two gains:

    K_I > 0        and        K > K_I/3 - 2.

This is where the symbolic method earns its keep: the answer is a region, and
no amount of root finding at sample points draws a region. To check the derived inequalities numerically, the script also computes closed-loop
roots on a grid and shades where they are all in the LHP -- the two pictures
have to agree.

Run:  uv run python ch3/l4_demo3_pi_region.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk


def den(K, KI):
    return [1.0, 3.0, 2.0 + K, KI]


def stable(K, KI):
    return bool(np.all(np.roots(den(K, KI)).real < -1e-9))


def routh_says(K, KI):
    return (KI > 0.0) and (K > KI / 3.0 - 2.0)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 3 -- a stability region in the gain plane, two ways")

    dk.note(
        "The Routh array is [1, 2+K], [3, K_I], [(6 + 3K - K_I)/3], [K_I]. Positive "
        "first column means K_I > 0 and 6 + 3K - K_I > 0. Everything below tests those "
        "two inequalities against actual closed-loop roots.")

    dk.section("spot checks")
    rows = []
    for K, KI in [(1.0, 0.0), (1.0, 1.0), (10.0, 5.0), (0.0, 5.0), (0.0, 7.0),
                  (-1.5, 1.0), (2.0, 20.0)]:
        roots = np.sort_complex(np.roots(den(K, KI)))
        rows.append([f"{K:g}", f"{KI:g}",
                     "yes" if routh_says(K, KI) else "no",
                     "yes" if stable(K, KI) else "no",
                     ", ".join(dk.fmt_root(r, 2) for r in roots)])
    dk.table(["K", "K_I", "Routh says stable", "roots say stable",
              "closed-loop roots"], rows)

    dk.section("agreement over a grid of 40401 gain pairs")
    Kg = np.linspace(-3.0, 12.0, 201)
    KIg = np.linspace(0.0, 30.0, 201)
    disagreements = 0
    grid = np.zeros((len(KIg), len(Kg)), dtype=bool)
    for i, KI in enumerate(KIg):
        for j, K in enumerate(Kg):
            s_roots = stable(K, KI)
            grid[i, j] = s_roots
            if s_roots != routh_says(K, KI) and abs(6 + 3 * K - KI) > 1e-9 and KI > 1e-9:
                disagreements += 1
    print(f"\n  grid points where the two verdicts differ (off the boundary): "
          f"{disagreements}")
    print("  K_I = 0 leaves an origin root in the retained-state cubic; "
          "a pure proportional implementation has only the quadratic dynamics")

    dk.note(
        "The line K = K_I/3 - 2 is not a rule of thumb. Cross it and a complex pair "
        "steps across the imaginary axis; on it the loop rings forever. Notice that "
        "raising integral gain K_I always demands more proportional gain K -- integral "
        "action buys steady-state accuracy and spends stability margin, which is the "
        "trade Chapter 4 formalises.")

    dk.section("the three gain sets of Fig. 3.44")
    t = np.linspace(0, 10, 4000)
    traces, rows = {}, []
    for K, KI in [(1.0, 0.0), (1.0, 1.0), (10.0, 5.0)]:
        sys = lti([K, KI], den(K, KI))
        _, y = step(sys, T=t)
        traces[(K, KI)] = y
        zero = "origin factor cancels" if KI == 0 else f"{-KI/K:+.2f}"
        rows.append([f"{K:g}", f"{KI:g}", zero, f"{y[-1]:.4f}"])
    dk.table(["K", "K_I", "closed-loop zero at -K_I/K", "output at t = 10 s"], rows)
    print("\n  at K=1, K_I=0 the reduced transfer is 1/(s^2+3s+3), with final "
          "value 1/3.\n  Retaining an unused integrator leaves a neutral state; removing "
          "it gives a stable pure-P loop.\n  For the two stable PI examples, integral "
          "action gives zero steady-state step error.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.8))

    axL.contourf(KIg, Kg, grid.T.astype(float), levels=[0.5, 1.5],
                 colors=[dk.C["green"]], alpha=0.22)
    axL.plot(KIg, KIg / 3.0 - 2.0, color=dk.C["blue"], lw=2.4,
             label=r"$K = K_I/3 - 2$")
    axL.axvline(0.0, color=dk.C["red"], lw=2.4, label=r"$K_I = 0$")
    for K, KI in [(1.0, 0.0), (1.0, 1.0), (10.0, 5.0), (0.0, 7.0)]:
        axL.plot([KI], [K], "o", ms=9,
                 color=dk.C["green"] if stable(K, KI) else dk.C["red"])
        offset = (8, -22) if KI == 0 else (8, 8)
        axL.annotate(f"({K:g}, {KI:g})", (KI, K), textcoords="offset points",
                     xytext=offset, fontsize=9.5)
    axL.set_xlim(-1, 30)
    axL.set_ylim(-3, 12)
    axL.set_xlabel("$K_I$")
    axL.set_ylabel("$K$")
    axL.set_title("Fig. 3.43: cubic stability; labels $(K, K_I)$")
    axL.legend(fontsize=10.5, loc="lower right")

    for (K, KI), colour in zip(traces, [dk.C["red"], dk.C["orange"], dk.C["green"]]):
        axR.plot(t, traces[(K, KI)], color=colour, lw=2.0,
                 label=f"$K$ = {K:g}, $K_I$ = {KI:g}")
    axR.axhline(1.0, ls=":", color="k", lw=1.0)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("step response")
    axR.set_title("Fig. 3.44: integral action removes the offset")
    axR.legend(fontsize=10.5)

    fig.suptitle("Example 3.34: stability as a region, not a number", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo3_pi_region", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
