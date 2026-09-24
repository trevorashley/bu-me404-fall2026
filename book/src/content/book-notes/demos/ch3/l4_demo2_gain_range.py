"""
L4 Demo 2  --  Routh with a symbol in it: the range of stabilising gain
                                                            (Example 3.33)

The plant (s+1)/[s(s-1)(s+6)] is open-loop unstable. Close a proportional loop
around it and the characteristic equation is

    s^3 + 5 s^2 + (K - 6) s + K = 0,

whose Routh array gives K > 7.5 (and K > 0). The claim is checked here by
sweeping K, computing the closed-loop roots, and marking where they cross the
imaginary axis. The three gains the book simulates, K = 7.5, 13 and 25, are
then run as step responses.

Run:  uv run python ch3/l4_demo2_gain_range.py
"""

import numpy as np
from scipy.signal import lti, step

import kit as dk


def closed_loop_den(K):
    return [1.0, 5.0, K - 6.0, K]


def routh_first_column(K):
    """[1, 5, (4K-30)/5, K] -- the array of Example 3.33, in symbols."""
    return np.array([1.0, 5.0, (4 * K - 30) / 5.0, K])


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 2 -- the stabilising range of a gain, found without root finding")

    dk.note(
        "Routh's array for s^3 + 5s^2 + (K-6)s + K has first column "
        "[1, 5, (4K-30)/5, K]. Both of the K-dependent entries must be positive, so "
        "K > 7.5 and K > 0; the binding condition is K > 7.5. Below is the same "
        "question answered by computing roots, for comparison.")

    dk.section("the boundary, from both directions")
    rows = []
    for K in [5.0, 7.0, 7.4, 7.5, 7.6, 13.0, 25.0, 100.0]:
        roots = np.roots(closed_loop_den(K))
        col = routh_first_column(K)
        changes = ("zero row: boundary" if np.any(np.abs(col) < 1e-12) else
                   str(int(np.sum(np.sign(col[1:]) * np.sign(col[:-1]) < 0))))
        rows.append([f"{K:g}", f"{col[2]:+.3f}", f"{changes}",
                     f"{int(np.sum(roots.real > 1e-9))}",
                     f"{max(roots.real):+.4f}"])
    dk.table(["K", "(4K-30)/5", "Routh sign changes", "RHP roots", "max Re(root)"], rows)

    # locate the crossing numerically
    Ks = np.linspace(6.0, 9.0, 3001)
    maxre = np.array([max(np.roots(closed_loop_den(K)).real) for K in Ks])
    idx = int(np.argmin(np.abs(maxre)))
    print(f"\n  imaginary-axis crossing found by root sweep : K = {Ks[idx]:.4f}")
    print(f"  Routh's prediction                          : K = 7.5000")
    roots_at = np.roots(closed_loop_den(7.5))
    print(f"  roots at K = 7.5                            : "
          + ", ".join(dk.fmt_root(r) for r in np.sort_complex(roots_at)))
    print("  so the neutrally stable loop rings at 1.2247 rad/s and never decays")

    dk.section("the three gains of Fig. 3.41")
    t = np.linspace(0, 12, 6000)
    traces, rows = {}, []
    for K in [7.5, 13.0, 25.0]:
        sys = lti([K, K], closed_loop_den(K))
        _, y = step(sys, T=t)
        traces[K] = y
        roots = np.sort_complex(np.roots(closed_loop_den(K)))
        rows.append([f"{K:g}", ", ".join(dk.fmt_root(r, 3) for r in roots),
                     f"{y[-1]:.4f}"])
    dk.table(["K", "closed-loop roots", "output at t = 12 s"], rows)

    dk.note(
        "At K = 7.5 the response oscillates forever: that is the pair sitting exactly "
        "on the imaginary axis. Increase K and the pair moves left, the ringing "
        "decays, and the loop becomes usable. Routh answered the question in three "
        "lines of algebra with K left as a symbol, which is the point -- a numerical "
        "root search has to be repeated for every value of K.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.6, 5.8))

    Ksweep = np.linspace(0.2, 40, 600)
    allroots = np.array([np.sort_complex(np.roots(closed_loop_den(K)))
                         for K in Ksweep])
    for k in range(3):
        axL.plot(allroots[:, k].real, allroots[:, k].imag, ".", ms=2.0,
                 color=dk.C["grey"])
    for K, colour in [(7.5, dk.C["red"]), (13.0, dk.C["orange"]),
                      (25.0, dk.C["green"])]:
        r = np.roots(closed_loop_den(K))
        axL.plot(r.real, r.imag, "x", ms=12, mew=3, color=colour, label=f"K = {K:g}")
    axL.axvline(0, color="k", lw=1.6)
    axL.axhline(0, color="k", lw=1.0)
    axL.axvspan(-6.5, 0, color=dk.C["green"], alpha=0.06)
    axL.set_xlim(-6.5, 1.5)
    axL.set_ylim(-4.5, 4.5)
    axL.set_xlabel(r"$\Re(s)$")
    axL.set_ylabel(r"$\Im(s)$")
    axL.set_title("Closed-loop roots as $K$ runs from 0.2 to 40")
    axL.legend(fontsize=10.5, loc="upper left")

    for K, colour in [(7.5, dk.C["red"]), (13.0, dk.C["orange"]),
                      (25.0, dk.C["green"])]:
        axR.plot(t, traces[K], color=colour, lw=2.0, label=f"K = {K:g}")
    axR.axhline(1.0, ls=":", color="k", lw=1.0)
    axR.set_xlabel("time [s]")
    axR.set_ylabel("step response")
    axR.set_title("Fig. 3.41: neutrally stable, then stable")
    axR.legend(fontsize=10.5)

    fig.suptitle("Example 3.33: Routh's criterion as a design tool", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo2_gain_range", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
