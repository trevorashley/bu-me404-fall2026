"""
L3 Demo 1  --  Table 4.1, simulated: three loops, three inputs, nine errors
                                                    (FPE §4.2.1, Eqs. 4.33-4.38)

Three unity-feedback loops, one of each type:

    Type 0   L0(s) = 4 / [(s+1)(0.5s+1)]          K_p = 4
    Type 1   L1(s) = 2 / [s(0.5s+1)]              K_v = 2
    Type 2   L2(s) = 2(s+1) / [s^2(0.2s+1)]       K_a = 2

Each is driven by a unit step, a unit ramp and a unit parabola t^2/2. The
steady-state error predicted by Table 4.1 is printed beside the error measured
from simulation, and the nine error histories are drawn as a 3 x 3 grid that
has the same layout as the table.

Run:  uv run python ch4/l3_demo1_type_table.py
"""

import math

import numpy as np
from scipy.signal import lsim, lti

import kit as dk

LOOPS = {
    # name: (numerator, denominator, type n, error constant, symbol)
    "Type 0": ([4.0], np.polymul([1.0, 1.0], [0.5, 1.0]), 0, 4.0, "K_p"),
    "Type 1": ([2.0], np.polymul([1.0, 0.0], [0.5, 1.0]), 1, 2.0, "K_v"),
    "Type 2": (np.polymul([2.0], [1.0, 1.0]),
               np.polymul([1.0, 0.0, 0.0], [0.2, 1.0]), 2, 2.0, "K_a"),
}
INPUTS = ["step", "ramp", "parabola"]


def sensitivity(num, den):
    """S = 1/(1+L) = den/(den+num) for L = num/den."""
    return lti(den, np.polyadd(den, num))


def predicted(n, K, k):
    """Table 4.1: zero if n > k, 1/(1+K_p) or 1/K_n if n = k, infinite if n < k."""
    if n > k:
        return 0.0
    if n < k:
        return math.inf
    return 1.0 / (1.0 + K) if n == 0 else 1.0 / K


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L3 Demo 1 -- system type and the error table, by simulation")
    dk.note(
        "For unity feedback, E = S R with S = 1/(1+L). Write L = L_o(s)/s^n with "
        "L_o(0) = K_n finite. A reference t^k/k! has transform 1/s^(k+1), and the "
        "Final Value Theorem gives e_ss = lim s^n/(s^n + K_n) * 1/s^k. So the error "
        "is zero when n > k, the constant 1/(1+K_p) or 1/K_n when n = k, and grows "
        "without bound when n < k.")

    dk.section("closed-loop poles (the table only means something if these are in the LHP)")
    rows = []
    for name, (num, den, n, K, sym) in LOOPS.items():
        roots = np.roots(np.polyadd(den, num))
        rows.append([name, f"{sym} = {K:g}",
                     ", ".join(dk.fmt_root(r, 3) for r in np.sort_complex(roots))])
    dk.table(["loop", "error constant", "closed-loop poles"], rows)

    t = np.linspace(0, 30, 15001)
    refs = {"step": np.ones_like(t), "ramp": t, "parabola": t**2 / 2}
    errors = {}
    dk.section("predicted versus simulated error at t = 30 s")
    rows = []
    for name, (num, den, n, K, sym) in LOOPS.items():
        S = sensitivity(num, den)
        row = [name]
        for k, inp in enumerate(INPUTS):
            _, e, _ = lsim(S, refs[inp], t)
            errors[(name, inp)] = e
            pred = predicted(n, K, k)
            ptxt = "grows" if math.isinf(pred) else f"{pred:.4f}"
            row.append(f"{ptxt} | {e[-1]:.4f}")
        rows.append(row)
    dk.table(["loop", "step: table | sim", "ramp: table | sim",
              "parabola: table | sim"], rows)

    dk.note(
        "Read the diagonal: each loop tracks the polynomial whose degree equals its "
        "type with a constant error, set by its error constant. Above the diagonal "
        "the error is zero; below it the error grows like t or t^2. The zero entries "
        "come from integrators in the loop, not from large gain.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(3, 3, figsize=(13.6, 9.6), sharex=True)
    colours = {"Type 0": dk.C["red"], "Type 1": dk.C["blue"], "Type 2": dk.C["green"]}
    for i, (name, (num, den, n, K, sym)) in enumerate(LOOPS.items()):
        for j, inp in enumerate(INPUTS):
            ax = axes[i, j]
            e = errors[(name, inp)]
            pred = predicted(n, K, j)
            ax.plot(t, e, color=colours[name])
            ax.axhline(0, color="k", lw=0.8)
            ax.set_xlim(0, 12)
            if math.isinf(pred):
                ax.set_ylim(-0.5, 5)
                label = r"$e_{ss}\to\infty$"
            else:
                ax.axhline(pred, ls="--", color=dk.C["grey"], lw=1.2)
                ax.set_ylim(-0.6, 1.1)
                label = rf"$e_{{ss}} = {pred:.2g}$"
            ax.text(0.97, 0.9, label, transform=ax.transAxes, ha="right",
                    va="top", fontsize=12)
            if i == 0:
                ax.set_title(f"unit {inp}")
            if j == 0:
                ax.set_ylabel(f"{name}\n$e(t)$")
            if i == 2:
                ax.set_xlabel("time [s]")
    fig.suptitle("Table 4.1 by simulation: rows are system type, columns are input degree",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l3_demo1_type_table", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
