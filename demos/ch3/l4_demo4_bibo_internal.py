"""
L4 Demo 4  --  Three ways to be unstable                     (FPE §3.6.1, §3.6.2)

Section 3.6 uses the word "stable" for three different things, and this script
separates them.

  1. BIBO: the capacitor of Example 3.31 has h(t) = 1(t), whose integral is
     unbounded, so a bounded current gives an unbounded voltage.
  2. A pole pair exactly on the imaginary axis is not BIBO stable either: drive
     an undamped oscillator at its own frequency and the output grows like t.
  3. Internal stability is stronger than a stable transfer function. Cancel a
     plant's RHP pole with a controller zero and the closed-loop transfer
     function from r to y is a clean first-order lag -- while a hidden mode
     grows as e^t and appears the moment anything but r disturbs the loop.

Run:  uv run python ch3/l4_demo4_bibo_internal.py
"""

import numpy as np
from scipy.integrate import solve_ivp

import kit as dk


def main() -> None:
    args = dk.parse_args(__doc__)
    plt = dk.setup(args)

    dk.title("L4 Demo 4 -- BIBO stability, neutral stability, internal stability")

    # -------------------------------------------------- 1. the capacitor
    dk.section("Example 3.31: a capacitor is not BIBO stable")
    t = np.linspace(0, 10, 2000)
    i_in = np.ones_like(t)                     # 1 A, thoroughly bounded
    v = t.copy()                              # C = 1 F, v(0) = 0
    dk.table(["t [s]", "input current [A]", "capacitor voltage [V]"],
             [[f"{tt:g}", "1", f"{vv:.2f}"]
              for tt, vv in zip([0, 2, 5, 10], np.interp([0, 2, 5, 10], t, v))])
    print("\n  h(t) = 1(t), so integral |h| dt diverges: the BIBO test fails")
    print("  transfer function 1/s -- one pole on the imaginary axis, at the origin")

    # -------------------------------------------------- 2. resonance
    dk.section("A j-omega pair is no better: resonant forcing of 1/(s^2 + 1)")
    t2 = np.linspace(0, 60, 20000)
    sol = solve_ivp(lambda tt, x: [x[1], -x[0] + np.sin(tt)], (0, t2[-1]), [0, 0],
                    t_eval=t2, rtol=1e-10, atol=1e-12)
    y_res = sol.y[0]
    y_exact = 0.5 * (np.sin(t2) - t2 * np.cos(t2))
    print(f"\n  max |simulated - (sin t - t cos t)/2| = "
          f"{np.max(np.abs(y_res - y_exact)):.2e}")
    dk.table(["t [s]", "peak so far"],
             [[f"{tt:g}", f"{np.max(np.abs(y_res[t2 <= tt])):.2f}"]
              for tt in [10, 20, 40, 60]])
    dk.note(
        "The input never exceeds 1 and the output grows without bound, linearly in "
        "time. So 'no poles in the RHP' is not the stability condition for BIBO: the "
        "condition is that every pole be strictly inside the LHP. Poles exactly on the "
        "axis are the boundary case the book calls neutrally stable, and this is why "
        "that is not good enough.")

    # -------------------------------------------------- 3. hidden mode
    dk.section("The cancellation trap: G = 1/(s-1) with C = (s-1)/(s+3)")
    dk.note(
        "On paper the loop gain is CG = 1/(s+3) and the closed loop is "
        "T = 1/(s+4): stable, well damped, unremarkable. But the controller zero "
        "cancelled the plant's unstable pole, and the state matrix of the "
        "interconnection still has an eigenvalue at +1.")

    # states: x[0] = plant state (y), x[1] = controller state
    A = np.array([[0.0, -4.0], [-1.0, -3.0]])
    B = np.array([1.0, 1.0])
    eig = np.linalg.eigvals(A)
    print(f"\n  closed-loop transfer function poles : -4")
    print(f"  eigenvalues of the interconnection  : "
          + ", ".join(dk.fmt_root(e) for e in np.sort_complex(eig)))

    t3 = np.linspace(0, 20, 8000)

    def run(x0, disturbance=0.0):
        f = lambda tt, x: A @ x + B * 1.0 + np.array([disturbance, 0.0])
        return solve_ivp(f, (0, t3[-1]), x0, t_eval=t3,
                         rtol=1e-10, atol=1e-12).y

    clean = run([0.0, 0.0])
    nudged = run([1e-6, 0.0])
    disturbed = run([0.0, 0.0], disturbance=1e-5)

    dk.table(["scenario", "y at t = 10 s", "y at t = 20 s"],
             [["step in r only, exact zero state",
               f"{np.interp(10, t3, clean[0]):.6f}", f"{clean[0][-1]:.6f}"],
              ["same, plant state off by 1e-6",
               f"{np.interp(10, t3, nudged[0]):.4f}", f"{nudged[0][-1]:.3e}"],
              ["same, 1e-5 input disturbance",
               f"{np.interp(10, t3, disturbed[0]):.4f}", f"{disturbed[0][-1]:.3e}"]])

    dk.note(
        f"From the reference alone the cancelled mode is never excited, so the "
        f"response is exactly what T = 1/(s+4) predicts and settles at "
        f"{clean[0][-1]:.3f}. Move the plant state by one part in a million and e^t "
        f"takes over: barely visible at ten seconds, {nudged[0][-1]:.0f} at twenty. A "
        f"disturbance of 1e-5 at the plant input does the same thing, reaching "
        f"{disturbed[0][-1]:.0f}. Cancelling an unstable pole does not remove it, it "
        "only removes it from one transfer function. That is the difference between a "
        "stable transfer function and an internally stable system, and it is why "
        "Section 3.6.2 insists on the roots of the characteristic equation before any "
        "cancellation.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.2))

    axes[0].plot(t, i_in, color=dk.C["grey"], lw=2.0, label="current in [A]")
    axes[0].plot(t, v, color=dk.C["blue"], lw=2.4, label="voltage out [V]")
    axes[0].set_xlabel("time [s]")
    axes[0].set_title("Example 3.31: bounded in, unbounded out")
    axes[0].legend(fontsize=10.5)

    axes[1].plot(t2, np.sin(t2), color=dk.C["grey"], lw=1.0, alpha=0.7,
                 label="input $\\sin t$")
    axes[1].plot(t2, y_res, color=dk.C["blue"], lw=1.6, label="output")
    axes[1].set_xlabel("time [s]")
    axes[1].set_title("$1/(s^2+1)$ driven at $\\omega = 1$")
    axes[1].legend(fontsize=10.5, loc="upper left")

    axes[2].plot(t3, clean[0], color=dk.C["green"], lw=2.4,
                 label="zero state: matches $1/(s+4)$")
    axes[2].plot(t3, nudged[0], color=dk.C["red"], lw=2.0,
                 label="plant state off by $10^{-6}$")
    axes[2].plot(t3, disturbed[0], color=dk.C["orange"], lw=2.0, ls="--",
                 label="$10^{-5}$ input disturbance")
    axes[2].set_yscale("symlog", linthresh=1.0)
    axes[2].set_xlabel("time [s]")
    axes[2].set_ylabel("output $y$ (symlog scale)")
    axes[2].set_title("A stable transfer function over an unstable system")
    axes[2].legend(fontsize=9.5, loc="upper left")

    fig.suptitle("Stability of what, exactly?", fontsize=15)
    fig.tight_layout()
    dk.finish(plt, fig, "l4_demo4_bibo_internal", args)


if __name__ == "__main__":
    dk.require_venv()
    main()
