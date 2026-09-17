"""
L4 Demo 1  --  The Routh array, built and believed              (Example 3.32)

Routh's test claims to count right half-plane roots without finding any roots.
Here the array is built from the coefficients, its first column is read for
sign changes, and the count is checked against the roots that numpy finds.

The book's Example 3.32 polynomial is

    a(s) = s^6 + 4s^5 + 3s^4 + 2s^3 + s^2 + 4s + 4,

all coefficients positive -- so the easy necessary condition tells us nothing,
and the array has to do the work.

Run:  uv run python ch3/l4_demo1_routh.py
"""

import numpy as np

import kit as dk


def routh_array(coeffs):
    """Rows of the Routh array for a monic-or-not polynomial in descending powers.

    Only the ordinary case is handled here. A zero in the first column or an
    entirely zero row needs the special treatment of Appendix W3.6.3, and this
    function says so rather than dividing by zero.
    """
    a = np.asarray(coeffs, dtype=float)
    if a.ndim != 1 or len(a) < 2 or not np.all(np.isfinite(a)) or a[0] == 0:
        raise ValueError("supply a finite polynomial of degree at least one with nonzero leading coefficient")
    a = a / a[0]
    n = len(a) - 1
    width = (n + 2) // 2
    rows = np.zeros((n + 1, width))
    rows[0, :len(a[0::2])] = a[0::2]
    rows[1, :len(a[1::2])] = a[1::2]
    for i in range(2, n + 1):
        pivot = rows[i - 1, 0]
        if abs(pivot) < 1e-12:
            raise ValueError("zero in the first column: special case, see Appendix W3.6.3")
        for j in range(width - 1):
            rows[i, j] = (rows[i - 1, 0] * rows[i - 2, j + 1]
                          - rows[i - 2, 0] * rows[i - 1, j + 1]) / pivot
    if np.any(np.abs(rows[:, 0]) < 1e-12):
        raise ValueError("zero in the first column: special case, see Appendix W3.6.3")
    return rows


def sign_changes(column):
    column = np.asarray(column)
    if np.any(np.abs(column) < 1e-12):
        raise ValueError("resolve zero pivots and zero rows before counting signs")
    signs = np.sign(column)
    return int(np.sum(signs[1:] * signs[:-1] < 0))


def report(name, coeffs):
    dk.section(name)
    rows = routh_array(coeffs)
    n = len(coeffs) - 1
    labels = [f"s^{n-i}" for i in range(n + 1)]
    dk.table(["row"] + [f"c{j+1}" for j in range(rows.shape[1])],
             [[labels[i]] + [f"{v:.4f}" for v in rows[i]] for i in range(n + 1)])

    first = rows[:, 0]
    changes = sign_changes(first)
    roots = np.roots(coeffs)
    rhp = int(np.sum(roots.real > 1e-9))
    print(f"\n  first column          : {[f'{v:+.4f}' for v in first]}")
    print(f"  sign changes          : {changes}")
    print(f"  RHP roots from numpy  : {rhp}")
    print(f"  verdict               : "
          f"{'stable' if changes == 0 else f'unstable, {changes} RHP root(s)'}")
    return roots


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 1 -- Routh's test counts RHP roots without computing them")

    dk.note(
        "The necessary condition is free: if any coefficient is missing or negative, "
        "there is a root outside the LHP and you are done. It is not sufficient, and "
        "Example 3.32 is the standard counterexample -- every coefficient positive, "
        "two roots in the RHP.")

    roots = report("Example 3.32:  s^6 + 4s^5 + 3s^4 + 2s^3 + s^2 + 4s + 4",
                   [1, 4, 3, 2, 1, 4, 4])
    print("\n  roots, for comparison only:")
    for r in np.sort_complex(roots):
        print(f"      {dk.fmt_root(r)}")
    dk.note(
        "Two of those roots sit at +0.6797 +/- 0.7488j. The book's footnote prints "
        "+0.7797 +/- 0.7488j, which cannot be right: the coefficient of s^5 is 4, so "
        "the six roots must sum to -4, and they only do with 0.6797. It is a typo, and "
        "a good one to hand the class -- the conclusion, two RHP roots, is unaffected.")

    report("a stable comparison:  s^4 + 6s^3 + 13s^2 + 12s + 4", [1, 6, 13, 12, 4])
    report("one negative coefficient:  s^3 + s^2 - 2s + 8", [1, 1, -2, 8])

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.2, 5.8),
                                   gridspec_kw={"width_ratios": [1.15, 1]})

    dk.splane(axL, poles=roots, xlim=(-4.0, 1.6), ylim=(-1.6, 1.6),
              title_text="Example 3.32: the roots Routh never computes")
    axL.annotate("the two the array finds", (0.6797, 0.7488),
                 textcoords="offset points", xytext=(-140, 26), fontsize=11,
                 color=dk.C["red"],
                 arrowprops=dict(arrowstyle="->", color=dk.C["red"]))

    t = np.linspace(0, 8, 2000)
    unstable = np.exp(0.6797 * t) * np.cos(0.7488 * t)
    stable = np.exp(-0.8858 * t)
    axR.plot(t, unstable, color=dk.C["red"], lw=2.2,
             label=r"mode at $+0.68 \pm 0.75j$")
    axR.plot(t, stable, color=dk.C["blue"], lw=2.2, label=r"mode at $-0.886$")
    axR.set_yscale("symlog", linthresh=1.0)
    axR.axhline(0, color="k", lw=0.8)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("natural response (symlog scale)")
    axR.set_title("One sign change is one growing motion")
    axR.legend(fontsize=10.5)

    fig.suptitle("Routh's criterion: a table of determinants that replaces root finding",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo1_routh", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
