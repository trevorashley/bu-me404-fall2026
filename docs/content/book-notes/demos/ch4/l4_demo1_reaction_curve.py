"""
L4 Demo 1  --  Ziegler-Nichols from a process reaction curve   (Example 4.9)

Take the open-loop step response of the heat exchanger, draw the tangent at the
inflection point, read off its slope R and its time-axis intercept L, and apply
the Ziegler-Nichols quarter-decay rules (FPE Table 4.2):

    P   : k_P = 1/(RL)
    PI  : k_P = 0.9/(RL),  T_I = L/0.3
    PID : k_P = 1.2/(RL),  T_I = 2L,  T_D = 0.5L

The book reads R ~ 1/90 and L ~ 13 s off its measured curve (Fig. 4.23). Here
the same construction is done on the model G(s) = e^{-5s}/[(10s+1)(60s+1)], and
the closed-loop responses are compared for the book's gains, and for the same
gains halved (Fig. 4.24).

Run:  uv run python ch4/l4_demo1_reaction_curve.py
"""

import numpy as np

import heatx as hx
import kit as dk


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 1 -- tuning a heat exchanger from one open-loop step test")

    t, y = hx.open_loop_step(400.0)
    dy = np.gradient(y, t)
    i = int(np.argmax(dy))
    R = dy[i]
    L = t[i] - y[i] / R
    dk.section("the tangent construction on the model")
    dk.table(["quantity", "model", "book (read from Fig. 4.23)"], [
        ["inflection time [s]", f"{t[i]:.2f}", "--"],
        ["max slope R [1/s]", f"1/{1 / R:.1f}", "1/90"],
        ["apparent lag L [s]", f"{L:.2f}", "13"],
        ["RL", f"{R * L:.4f}", f"{13 / 90:.4f}"],
    ])
    dk.note(
        "The model's L is 10.6 s, not 13 s, and R is 1/85.9 rather than 1/90. A "
        "tangent drawn by eye on a printed curve moves by this much easily; the "
        "true transport delay is only 5 s, and the rest of L is the lag of the "
        "two thermal time constants disguised as dead time.")

    dk.section("Table 4.2 gains: the book's readings and the model's")
    rows = []
    for name, RL, Lval in [("book", 13 / 90, 13.0), ("model", R * L, L)]:
        rows.append([name, "P", f"{1 / RL:.3f}", "--", "--"])
        rows.append([name, "PI", f"{0.9 / RL:.3f}", f"{Lval / 0.3:.2f}", "--"])
        rows.append([name, "PID", f"{1.2 / RL:.3f}", f"{2 * Lval:.2f}", f"{0.5 * Lval:.2f}"])
    dk.table(["from", "law", "k_P", "T_I [s]", "T_D [s]"], rows)

    dk.section("closed-loop step responses with the book's gains (Fig. 4.24)")
    cases = [("P", 6.92, np.inf), ("PI", 6.22, 43.3)]
    runs = {}
    rows = []
    for scale in (1.0, 0.5):
        for name, kP, TI in cases:
            tt, yy, uu = hx.closed_loop(scale * kP, TI, T=400.0)
            pk = hx.peaks(tt, yy)
            yfin = (scale * kP) / (1 + scale * kP) if not np.isfinite(TI) else 1.0
            dr = ((yy[pk[1]] - yfin) / (yy[pk[0]] - yfin)) if len(pk) > 1 else float("nan")
            runs[(name, scale)] = (tt, yy)
            rows.append([f"{name}", f"{scale * kP:.3f}", f"{yy.max():.3f}",
                         f"{tt[np.argmax(yy)]:.1f}", f"{yfin:.4f}", f"{dr:.3f}"])
    dk.table(["law", "k_P", "peak y", "t_peak [s]", "final y", "decay ratio"], rows)
    dk.note(
        "With the full Ziegler-Nichols gains, the decay ratio of successive peaks is "
        "0.20 for P and 0.27 for PI: close to the quarter-decay target the rules were "
        "built for. Proportional control leaves the Type 0 offset 1/(1+k_P); the "
        "integrator removes it. Halving k_P, as the book does in Fig. 4.24(b), "
        "cuts the decay ratio to a few percent at the cost of a slower rise. "
        "The quarter-decay target is aggressive by modern standards.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.6))
    axL.plot(t, y, color=dk.C["blue"], label="plant step response")
    tl = np.linspace(L, L + 1.15 / R, 50)
    axL.plot(tl, R * (tl - L), "--", color=dk.C["red"], lw=1.6,
             label=f"tangent: slope $R$ = 1/{1 / R:.1f}")
    axL.plot(t[i], y[i], "o", color=dk.C["red"])
    axL.axvline(hx.TD_DELAY, color=dk.C["grey"], lw=1.0, ls=":")
    axL.annotate(f"$L$ = {L:.1f} s", xy=(L, 0), xytext=(L + 25, 0.12),
                 arrowprops=dict(arrowstyle="->", color="k"), fontsize=12)
    axL.text(hx.TD_DELAY + 2, 0.95, "true delay 5 s", color=dk.C["grey"], fontsize=10.5)
    axL.set_xlim(0, 400)
    axL.set_ylim(-0.05, 1.15)
    axL.set_xlabel("time [s]")
    axL.set_ylabel("output temperature (normalised)")
    axL.set_title("Process reaction curve (cf. Fig. 4.23)")
    axL.legend(fontsize=10.5, loc="lower right")

    for (name, scale), colour in [(("P", 1.0), dk.C["orange"]), (("PI", 1.0), dk.C["blue"]),
                                  (("P", 0.5), dk.C["orange"]), (("PI", 0.5), dk.C["blue"])]:
        tt, yy = runs[(name, scale)]
        ls = "-" if scale == 1.0 else "--"
        axR.plot(tt, yy, ls, color=colour,
                 label=f"{name}, {'Z-N gains' if scale == 1 else 'k_P halved'}")
    axR.axhline(1.0, ls=":", color="k", lw=1.0)
    axR.set_xlim(0, 400)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("output")
    axR.set_title("Closed loop with Table 4.2 gains (cf. Fig. 4.24)")
    axR.legend(fontsize=10.5)

    fig.suptitle("Example 4.9: Ziegler-Nichols tuning from a step test", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo1_reaction_curve", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
