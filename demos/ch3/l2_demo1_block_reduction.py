"""
L2 Demo 1  --  Block-diagram reduction is Gaussian elimination
                                                   (Examples 3.22, 3.23, 3.24)

Block-diagram algebra feels like a set of tricks to memorise. It is not: the
diagram is a set of simultaneous linear equations in the transformed signals,
and every reduction rule is one step of eliminating a variable.

This script checks that claim numerically. For the six-block system of Fig.
3.12 it solves the node equations at random complex values of s and compares
the answer with the book's reduced formula

    T = (G1 G2 G5 + G1 G6) / (1 - G1 G3 + G1 G2 G4).

If the reduction were wrong, random s would expose it immediately.

Run:  uv run python ch3/l2_demo1_block_reduction.py
"""

import numpy as np

import kit as dk

rng = np.random.default_rng(3)


# Arbitrary but fixed component transfer functions for the Fig. 3.12 system.
def G1(s): return 2.0 / (s + 3.0)
def G2(s): return (s + 5.0) / (s**2 + 2.0 * s + 8.0)
def G3(s): return 0.5 / (s + 1.0)
def G4(s): return 3.0 / (s + 4.0)
def G5(s): return 1.5
def G6(s): return 0.25 / (s + 2.0)


def solve_nodes(s):
    """Solve the diagram as written: three unknowns a, b, Y, one equation each.

        a = G1 [ (R - G4 b) + G3 a ]      b = G2 a      Y = G5 b + G6 a
    """
    g1, g2, g3, g4, g5, g6 = (f(s) for f in (G1, G2, G3, G4, G5, G6))
    A = np.array([[1.0 - g1 * g3, g1 * g4, 0.0],
                  [-g2, 1.0, 0.0],
                  [-g6, -g5, 1.0]], dtype=complex)
    rhs = np.array([g1, 0.0, 0.0], dtype=complex)   # unit R
    return np.linalg.solve(A, rhs)[2]


def reduced(s):
    g1, g2, g3, g4, g5, g6 = (f(s) for f in (G1, G2, G3, G4, G5, G6))
    return (g1 * g2 * g5 + g1 * g6) / (1.0 - g1 * g3 + g1 * g2 * g4)


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L2 Demo 1 -- the reduced transfer function is the solved linear system")

    # ---------------------------------------------------------- Example 3.22
    dk.section("Example 3.22: the simple loop, done both ways")
    dk.note(
        "Forward path: a gain of 2 in parallel with 4/s, then an integrator, inside "
        "unity negative feedback. Parallel gives 2 + 4/s; series gives (2s+4)/s^2; "
        "the feedback rule gives T = (2s+4)/(s^2+2s+4).")

    def T22_nodes(s):
        forward = (2.0 + 4.0 / s) * (1.0 / s)
        return forward / (1.0 + forward)

    rows = []
    for s in [0.5 + 0.0j, 1.0 + 1.0j, -0.3 + 2.0j, 4.0 - 1.5j]:
        direct = (2 * s + 4) / (s**2 + 2 * s + 4)
        rows.append([f"{s.real:+.2f}{s.imag:+.2f}j",
                     f"{T22_nodes(s):.10f}", f"{direct:.10f}"])
    dk.table(["s", "diagram solved", "(2s+4)/(s^2+2s+4)"], rows)

    poles22 = np.roots([1, 2, 4])
    wn = float(abs(poles22[0]))
    zeta = float(-poles22[0].real / wn)
    print(f"\n  closed-loop poles : {dk.fmt_root(poles22[0])}, {dk.fmt_root(poles22[1])}")
    print(f"  omega_n = {wn:.4f} rad/s,  zeta = {zeta:.4f},  DC gain = "
          f"{(4/4):.4f}")

    # ---------------------------------------------------------- Example 3.23
    dk.section("Example 3.23: six blocks, two loops, one pickoff point moved")
    errs, rows = [], []
    for _ in range(6):
        s = rng.uniform(-2, 5) + 1j * rng.uniform(-5, 5)
        a, b = solve_nodes(s), reduced(s)
        errs.append(abs(a - b))
        rows.append([f"{s.real:+.3f}{s.imag:+.3f}j", f"{a.real:+.8f}{a.imag:+.8f}j",
                     f"{abs(a - b):.2e}"])
    dk.table(["random s", "solved from the diagram", "|difference from formula|"], rows)
    print(f"\n  worst disagreement over 2000 random points in the s-plane: "
          f"{max(abs(solve_nodes(s) - reduced(s)) for s in (rng.uniform(-3, 6, 2000) + 1j*rng.uniform(-8, 8, 2000))):.2e}")

    dk.note(
        "The matrix inverted at each s is the diagram: row 1 is the two summers and "
        "G1, row 2 is G2, row 3 is the output summer with G5 and G6. Reducing the "
        "diagram by hand eliminates the same three unknowns in the same order. "
        "Matlab's series/parallel/feedback commands (Example 3.24) do the same thing "
        "one connection at a time.")

    # ------------------------------------------------------------------ figure
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 5.6))

    w = np.logspace(-1, 1.6, 500)
    axL.loglog(w, [abs(solve_nodes(1j * ww)) for ww in w], color=dk.C["blue"], lw=3.2,
               alpha=0.45, label="diagram solved at each $j\\omega$")
    axL.loglog(w, [abs(reduced(1j * ww)) for ww in w], "--", color=dk.C["red"], lw=1.8,
               label="reduced formula")
    axL.set_xlabel("$\\omega$ [rad/s]")
    axL.set_ylabel("$|T(j\\omega)|$")
    axL.set_title("Fig. 3.12 system: two routes, one curve")
    axL.legend(fontsize=10.5)

    t = np.linspace(0, 8, 800)
    wd = float(abs(poles22[0].imag))
    sig = float(-poles22[0].real)
    # step response of (2s+4)/(s^2+2s+4) = 1 - e^{-t}(cos(wd t) - (1/wd) sin(wd t))
    y = 1 - np.exp(-sig * t) * (np.cos(wd * t) - (1.0 / wd) * np.sin(wd * t))
    axR.plot(t, y, color=dk.C["blue"], lw=2.4)
    axR.axhline(1.0, ls="--", color=dk.C["grey"])
    axR.set_xlabel("time [s]")
    axR.set_ylabel("step response")
    axR.set_title(f"Example 3.22 closed loop: $\\zeta$ = {zeta:.2f}, "
                  f"$\\omega_n$ = {wn:.1f} rad/s")

    fig.suptitle("Block-diagram algebra, checked against the equations it stands for",
                 fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l2_demo1_block_reduction", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
