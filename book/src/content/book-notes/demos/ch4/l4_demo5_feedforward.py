"""
L4 Demo 5  --  Feedforward by plant DC-gain inversion        (Example 4.11)

Plant G(s) = 1/(s^2 + 1.4 s + 1), so G(0) = 1 and G^{-1}(0) = 1; proportional
feedback k_P = 1.5 and 6.

  (a) tracking, Fig. 4.27(a): U = k_P E + G^{-1}(0) R
          Y/R = (1 + k_P) G / (1 + k_P G) = (1 + k_P)/(s^2 + 1.4 s + 1 + k_P)
  (b) measured output disturbance, Fig. 4.27(b): U = k_P E - G^{-1}(0) W
          Y/W = (1 - G)/(1 + k_P G) = (s^2 + 1.4 s)/(s^2 + 1.4 s + 1 + k_P)

Each is compared with pure proportional feedback, and then with a plant whose
true DC gain is 20% higher than the model used for the feedforward.

Run:  uv run python ch4/l4_demo5_feedforward.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 5 -- feedforward: let the model supply the steady effort")

    t = np.linspace(0, 10, 5001)
    runs, rows = {}, []
    for kP in (1.5, 6.0):
        den = [1.0, 1.4, 1.0 + kP]
        _, y_fb = step(lti([kP], den), T=t)
        _, y_ff = step(lti([1.0 + kP], den), T=t)
        _, w_fb = step(lti([1.0, 1.4, 1.0], den), T=t)
        _, w_ff = step(lti([1.0, 1.4, 0.0], den), T=t)
        runs[kP] = (y_fb, y_ff, w_fb, w_ff)
        wn = np.sqrt(1 + kP)
        zeta = 1.4 / (2 * wn)
        Mp = np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))
        rows.append([f"{kP:g}", f"{wn:.3f}", f"{zeta:.3f}", f"{100 * Mp:.1f}%",
                     f"{y_ff.max():.3f}", f"{1 / (1 + kP):.4f}", "0",
                     f"{w_ff.min():+.3f}"])
    dk.table(["k_P", "w_n", "zeta", "M_p", "peak y (FF)", "e_ss FB only",
              "e_ss with FF", "min y after W step"], rows)
    dk.note(
        "Feedforward changes the numerator, not the denominator: the closed-loop poles, "
        "and so zeta and the overshoot, are exactly those of the proportional loop. "
        "Without feedforward the Type 0 loop leaves a step error 1/(1 + k_P): 0.4 at "
        "k_P = 1.5 and 0.143 at k_P = 6. With it the DC gain from R is (1+k_P)/(1+k_P) "
        "= 1 and from W it is 0/(1+k_P) = 0.")

    dk.section("what if the model's DC gain is wrong?")
    rows = []
    for kP in (1.5, 6.0):
        for g0 in (1.0, 1.2, 0.8):
            e_fb = 1 - kP * g0 / (1 + kP * g0)
            e_ff = (1 - g0 / 1.0) / (1 + kP * g0)
            rows.append([f"{kP:g}", f"{g0:.1f}", f"{e_fb:+.4f}", f"{e_ff:+.4f}"])
    dk.table(["k_P", "true G(0)", "e_ss, feedback only", "e_ss, with FF (model G(0)=1)"], rows)
    dk.note(
        "With a 20% model error the residual error is (1 - G(0)/G_model(0)) / "
        "(1 + k_P G(0)): the feedforward removes most of the error and the feedback "
        "divides what is left by 1 + k_P G(0). Feedforward is only as good as the "
        "model; feedback is what makes it forgiving. Integral action is what makes the "
        "residual exactly zero.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.4))
    for kP, colour in [(1.5, dk.C["blue"]), (6.0, dk.C["orange"])]:
        y_fb, y_ff, w_fb, w_ff = runs[kP]
        axL.plot(t, y_ff, color=colour, label=f"$k_P$ = {kP:g}, with feedforward")
        axL.plot(t, y_fb, "--", color=colour, lw=1.6, label=f"$k_P$ = {kP:g}, feedback only")
        axR.plot(t, w_ff, color=colour, label=f"$k_P$ = {kP:g}, with feedforward")
        axR.plot(t, w_fb, "--", color=colour, lw=1.6, label=f"$k_P$ = {kP:g}, feedback only")
    axL.axhline(1.0, ls=":", color="k", lw=1.0)
    axR.axhline(0.0, ls=":", color="k", lw=1.0)
    axL.set_title("Tracking a unit step (cf. Fig. 4.28)")
    axR.set_title("Unit output-disturbance step (cf. Fig. 4.29)")
    for ax in (axL, axR):
        ax.set_xlabel("time [s]")
        ax.set_ylabel("$y$")
        ax.legend(fontsize=9.5, loc="lower right" if ax is axL else "upper right")
    fig.suptitle("Example 4.11: feedforward of the inverse plant DC gain", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo5_feedforward", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
