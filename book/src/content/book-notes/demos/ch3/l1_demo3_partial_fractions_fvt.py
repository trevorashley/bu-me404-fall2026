"""
L1 Demo 3  --  Cover-up residues, and misuse of the Final Value Theorem
                                          (Examples 3.11, 3.12, 3.13, 3.14)

Three things at once, because they are the same idea seen from three sides:

  1. the cover-up method computes the residues of Y(s) = (s+2)(s+4)/(s(s+1)(s+3)),
     and Matlab's `residue` agrees -- so does scipy;
  2. the Final Value Theorem reads the residue at the pole s = 0 straight off,
     which is why it works;
  3. why the finite-final-value hypothesis must be checked first.

Run:  uv run python ch3/l1_demo3_partial_fractions_fvt.py
"""

import numpy as np
from scipy.signal import residue

import kit as dk


def cover_up(num_roots, den_roots, gain, pole):
    """Residue at `pole` by covering up its factor and evaluating the rest."""
    value = gain
    for z in num_roots:
        value *= (pole - z)
    for p in den_roots:
        if p != pole:
            value /= (pole - p)
    return value


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L1 Demo 3 -- partial fractions by cover-up, and the FVT's fine print")

    # ---------------------------------------------------------- Example 3.11
    dk.section("Example 3.11: Y(s) = (s+2)(s+4) / [s(s+1)(s+3)]")
    zeros = [-2.0, -4.0]
    poles = [0.0, -1.0, -3.0]
    hand = {"8/3": 8 / 3, "-3/2": -3 / 2, "-1/6": -1 / 6}

    num = np.polynomial.polynomial.polyfromroots(zeros)[::-1]
    den = np.polynomial.polynomial.polyfromroots(poles)[::-1]
    r, p, _ = residue(num, den)
    order = np.argsort(-p.real)                      # 0, -1, -3

    rows = []
    for (name, exact_val), pole, idx in zip(hand.items(), poles, order):
        cu = cover_up(zeros, poles, 1.0, pole)
        rows.append([f"{pole:+.0f}", name, f"{exact_val:+.6f}",
                     f"{cu:+.6f}", f"{r[idx].real:+.6f}"])
    dk.table(["pole", "book", "book value", "cover-up here", "scipy residue"], rows)

    dk.note(
        "y(t) = 8/3 - (3/2) e^-t - (1/6) e^-3t for t >= 0. The three numbers are not "
        "three separate calculations: each one is the whole function with a single "
        "factor covered up and s set to that pole.")

    t = np.linspace(0, 6, 1200)
    y = 8 / 3 - 1.5 * np.exp(-t) - (1 / 6) * np.exp(-3 * t)

    # ---------------------------------------------------- Examples 3.12, 3.14
    dk.section("Examples 3.12 and 3.14: the FVT used correctly")
    dk.note(
        "Y(s) = 3(s+2) / [s(s^2 + 2s + 10)]. Every pole of sY(s) is in the LHP, at "
        "-1 +/- 3j, so the theorem applies: y(inf) = lim s Y(s) = 3*2/10 = 0.6. The "
        "same arithmetic read as a DC gain says G(s) = 3(s+2)/(s^2+2s+10) has DC gain "
        "G(0) = 0.6, which is Example 3.14.")

    t2 = np.linspace(0, 12, 4000)
    # y(t) for Y = 3(s+2)/(s(s^2+2s+10)) by residues, computed not quoted
    num2 = np.array([3.0, 6.0])
    den2 = np.polynomial.polynomial.polyfromroots([0.0, -1 + 3j, -1 - 3j])[::-1].real
    r2, p2, _ = residue(num2, den2)
    y2 = np.real(sum(ri * np.exp(pi * t2) for ri, pi in zip(r2, p2)))
    print(f"\n  simulated y(12 s)            = {y2[-1]:.6f}")
    print(f"  final value theorem          = {0.6:.6f}")
    print(f"  residue at the pole s = 0    = {r2[np.argmin(abs(p2))].real:.6f}")

    # ---------------------------------------------------------- Example 3.13
    dk.section("Example 3.13: the same formula applied where it does not hold")
    dk.note(
        "Y(s) = 3 / [s(s-2)] has a pole at s = +2, so sY(s) is not LHP-stable. "
        "Applying the formula anyway returns the constant term of the expansion and "
        "quietly discards the growing one.")
    t3 = np.linspace(0, 6, 1200)
    y3 = -1.5 + 1.5 * np.exp(2 * t3)
    dk.table(["t [s]", "y(t) = -3/2 + (3/2)e^{2t}"],
             [[f"{tt:g}", f"{-1.5 + 1.5*np.exp(2*tt):,.1f}"] for tt in [0, 1, 2, 3, 6]])
    print(f"\n  naive lim s->0 of sY(s)      = {-1.5:.4f}")
    print(f"  actual behaviour             = unbounded "
          f"(y(6 s) = {y3[-1]:.3e})")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.0))

    axes[0].plot(t, y, color=dk.C["blue"], lw=2.4, label="$y(t)$")
    axes[0].plot(t, np.full_like(t, 8 / 3), "--", color=dk.C["grey"],
                 label="residue at $s=0$: $8/3$")
    axes[0].plot(t, -1.5 * np.exp(-t), color=dk.C["orange"], lw=1.4,
                 label=r"$-\frac{3}{2}e^{-t}$")
    axes[0].plot(t, -(1 / 6) * np.exp(-3 * t), color=dk.C["green"], lw=1.4,
                 label=r"$-\frac{1}{6}e^{-3t}$")
    axes[0].set_title("Example 3.11: one term per pole")
    axes[0].set_xlabel("time [s]")
    axes[0].legend(fontsize=10, loc="center right")

    axes[1].plot(t2, y2, color=dk.C["blue"], lw=2.4)
    axes[1].axhline(0.6, ls="--", color=dk.C["red"])
    axes[1].text(6.2, 0.63, "FVT: 0.6", color=dk.C["red"], fontsize=11)
    axes[1].set_title("Example 3.12: the FVT is right")
    axes[1].set_xlabel("time [s]")

    axes[2].plot(t3, y3, color=dk.C["blue"], lw=2.4)
    axes[2].axhline(-1.5, ls="--", color=dk.C["red"])
    axes[2].text(0.3, -1.5e4, "Invalid use gives $-3/2$", color=dk.C["red"], fontsize=11)
    axes[2].set_yscale("symlog", linthresh=1.0)
    axes[2].set_title("Example 3.13: FVT hypothesis violated")
    axes[2].set_xlabel("time [s]")

    fig.suptitle("Residues, final values, and the pole that invalidates them",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l1_demo3_partial_fractions_fvt", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
