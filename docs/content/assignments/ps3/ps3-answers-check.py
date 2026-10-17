"""Verify PS3 calculations and regenerate the answer-key figures.

Run with Python 3, NumPy, SymPy, and Matplotlib installed:
    python ps3-answers-check.py

This instructor utility uses polynomial partial fractions, bracketed root
finding, and an independent Runge-Kutta integration of each transfer function.
The student-facing equivalent is ps3_answers.m (MATLAB Control System Toolbox).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def bisect(f, left, right):
    """Refine a bracketed scalar root without a numerical-library dependency."""
    fl, fr = f(left), f(right)
    if fl == 0:
        return left
    if fr == 0:
        return right
    assert fl * fr < 0, (left, right, fl, fr)
    for _ in range(55):
        mid = (left + right) / 2
        fm = f(mid)
        if fm * fl > 0:
            left, fl = mid, fm
        else:
            right = mid
    return (left + right) / 2


class StepResponse:
    """Simple-pole partial fractions of G(s)/s; all models here have G(0)=1."""

    def __init__(self, transfer, s):
        num, den = sp.fraction(sp.cancel(transfer))
        self.num = np.array(sp.Poly(num, s).all_coeffs(), dtype=float)
        self.den = np.array(sp.Poly(den, s).all_coeffs(), dtype=float)
        self.num, self.den = self.num / self.den[0], self.den / self.den[0]
        step_den = np.r_[self.den, 0.0]
        self.poles = np.roots(step_den)
        self.residues = np.polyval(self.num, self.poles) / np.polyval(
            np.polyder(step_den), self.poles
        )
        assert np.isclose(self.num[-1] / self.den[-1], 1)
        assert np.all(np.roots(self.den).real < 0)

    def value(self, time, derivative=0):
        values = np.real(
            np.exp(np.outer(np.atleast_1d(time), self.poles))
            @ (self.residues * self.poles**derivative)
        )
        return float(values[0]) if np.ndim(time) == 0 else values

    def tail_bound(self, time):
        transient = self.poles.real < 0
        return np.sum(
            np.abs(self.residues[transient])
            * np.exp(self.poles[transient].real * time)
        )

    def metrics(self, end, dt):
        grid = np.linspace(0, end, round(end / dt) + 1)

        def crossings(level, derivative=0):
            f = self.value(grid, derivative) - level
            indices = np.flatnonzero(f[:-1] * f[1:] < 0)
            return [
                bisect(lambda t: self.value(t, derivative) - level, grid[i], grid[i + 1])
                for i in indices
            ]

        t10, t90 = crossings(0.1)[0], crossings(0.9)[0]
        extrema = crossings(0, derivative=1)
        peak = max([1.0] + [self.value(t) for t in extrema])
        # The monotone modal envelope certifies no later 1% band exits.
        assert self.tail_bound(end) < 0.01
        settling = max(crossings(0.99) + crossings(1.01))
        return np.array([t10, t90, t90 - t10, 100 * (peak - 1), settling])

    def check_by_integration(self, end=10, dt=0.001):
        """Independently integrate a phase-variable state model using RK4."""
        n = len(self.den) - 1
        A = np.zeros((n, n))
        A[:-1, 1:] = np.eye(n - 1)
        A[-1, :] = -self.den[:0:-1]
        B = np.zeros(n)
        B[-1] = 1
        C = np.pad(self.num, (n - len(self.num), 0))[::-1]
        x = np.zeros(n)
        samples = [0.0]
        grid = np.linspace(0, end, round(end / dt) + 1)
        for _ in grid[1:]:
            k1 = A @ x + B
            k2 = A @ (x + dt * k1 / 2) + B
            k3 = A @ (x + dt * k2 / 2) + B
            k4 = A @ (x + dt * k3) + B
            x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            samples.append(C @ x)
        error = np.max(np.abs(np.array(samples) - self.value(grid)))
        assert error < 2e-7, error
        return error


def motor_rise(K):
    wd = np.sqrt(0.2 * K - 0.052**2)
    def response(t):
        return 1 - np.exp(-0.052 * t) * (
            np.cos(wd * t) + 0.052 / wd * np.sin(wd * t)
        )
    crossings = [bisect(lambda t: response(t) - level, 0, np.pi / wd)
                 for level in (0.1, 0.9)]
    return crossings[1] - crossings[0]


def verify_symbolic(s, transfers):
    R = sp.Rational
    b_eff = R(1, 1000) + R(2, 100) ** 2 / 10
    speed = (R(2, 100) / 10) / (R(1, 100) * s + b_eff)
    assert sp.cancel(speed - R(1, 5) / (s + R(13, 125))) == 0
    assert speed.subs(s, 0) * 10 == R(250, 13)

    t = sp.symbols("t", nonnegative=True)
    q = s**2 + 4 * s + 40
    # These are the exact partial-fraction expressions used in the key.
    decompositions = [
        1/s - (s+4)/q,
        1/s - 40/(37*(s+1)) + (3*s-28)/(37*q),
        1/s - 40/(37*(s+3)) + (3*s-108)/(37*q),
        1/s - 20/(37*(s+1)) - (17*s+88)/(37*q),
        1/s - 901*(105171*s+440684)/(100519071*q)
        - 20000*(288*s-613)/(100519071*(s**2+s+901)),
    ]
    for G, Y in zip(transfers, decompositions):
        assert sp.cancel(G/s - Y) == 0
    # Check the real time-domain forms, including the high-frequency mode.
    N = sp.Integer(100519071)
    nu = sp.sqrt(3603)/2
    responses = [
        1-sp.exp(-2*t)*(sp.cos(6*t)+sp.sin(6*t)/3),
        1-R(40,37)*sp.exp(-t)+sp.exp(-2*t)*(R(3,37)*sp.cos(6*t)-R(17,111)*sp.sin(6*t)),
        1-R(40,37)*sp.exp(-3*t)+sp.exp(-2*t)*(R(3,37)*sp.cos(6*t)-R(19,37)*sp.sin(6*t)),
        1-R(20,37)*sp.exp(-t)-sp.exp(-2*t)*(R(17,37)*sp.cos(6*t)+R(9,37)*sp.sin(6*t)),
        1+sp.exp(-2*t)*(-901*105171/N*sp.cos(6*t)-901*230342/(6*N)*sp.sin(6*t))
        +sp.exp(-t/2)*(-5760000/N*sp.cos(nu*t)+15140000/(N*nu)*sp.sin(nu*t)),
    ]
    for G, y in zip(transfers, responses):
        assert sp.cancel(sp.laplace_transform(y, t, s, noconds=True)-G/s) == 0

    a, p, z, qgain = sp.symbols("a p z q", real=True)
    characteristic = sp.expand((s+p)*(s**2-a**2)+qgain*(s+z))
    assert sp.expand(characteristic-(s**3+p*s**2+(qgain-a**2)*s+qgain*z-p*a**2)) == 0
    assert sp.expand(p*(qgain-a**2)-(qgain*z-p*a**2)-qgain*(p-z)) == 0
    # Retain the controller state: its characteristic determinant is the cubic.
    K, K0 = sp.symbols("K K0", real=True)
    A = sp.Matrix([[0, 1, 0], [a*a-K*K0, 0, K*K0*(z-p)], [-1, 0, -p]])
    assert sp.expand((s*sp.eye(3)-A).det()-characteristic.subs(qgain,K*K0)) == 0
    beta = sp.symbols("beta", positive=True)
    gains = [-beta*K**3, -K**3/(1+beta*K)**3, -K**3/(1+beta*K**3)]
    expected_K = [3, 3/(1+beta*K), 3/(1+beta*K**3)]
    expected_beta = [1, -3*beta*K/(1+beta*K), -beta*K**3/(1+beta*K**3)]
    for G, SK, Sb in zip(gains, expected_K, expected_beta):
        assert sp.simplify(K/G*sp.diff(G,K)-SK) == 0
        assert sp.simplify(beta/G*sp.diff(G,beta)-Sb) == 0
    beta_values = [R(1,100), 10**(-R(1,3))-R(1,10), R(99,1000)]
    for G, b in zip(gains, beta_values):
        assert sp.simplify(G.subs({K:10, beta:b})+10) == 0


def main():
    s = sp.symbols("s")
    q = s*s+4*s+40
    transfers = [40/q, 40/((s+1)*q), 120/((s+3)*q),
                 20*(s+2)/((s+1)*q),
                 sp.Rational(36040,401)*(s*s+s+401)/(q*(s*s+s+901))]
    verify_symbolic(s, transfers)
    systems = [StepResponse(G,s) for G in transfers]
    metrics = np.array([G.metrics(30,0.0005) for G in systems])
    # Halving the grid must preserve all crossings and peaks, including G5.
    refined = np.array([G.metrics(30,0.00025) for G in systems])
    np.testing.assert_allclose(metrics,refined,atol=1e-9,rtol=0)
    error = max(G.check_by_integration() for G in systems)
    print("Problem 2: t10, t90, rise (s), overshoot (%), settling (s)")
    for i,row in enumerate(metrics,1):
        print(f"G{i}: " + ", ".join(f"{v:.9f}" for v in row))
    assert np.array_equal(metrics[:,3]<=5,[False,True,True,True,False])
    assert np.array_equal(metrics[:,2]<=0.5,[True,False,True,False,True])
    assert np.array_equal(metrics[:,4]<=2.5,[True,False,True,False,False])
    zeta_min = -np.log(0.2)/np.sqrt(np.pi**2+np.log(0.2)**2)
    Kmax = 0.052**2/(0.2*zeta_min**2)
    Krise = bisect(lambda K:motor_rise(K)-4,0.02,2)
    print(f"Problem 1: zeta_min={zeta_min:.12f}, Kmax={Kmax:.12f}, Krise={Krise:.12f}")
    # Numerically check the decreasing rise time on the underdamped branch.
    gains = np.geomspace(0.013521,1e5,400)
    assert np.all(np.diff([motor_rise(K) for K in gains])<0)
    motors = [StepResponse(sp.Rational(1,5)*K/(s*s+sp.Rational(13,125)*s+sp.Rational(1,5)*K),s)
              for K in (sp.Rational(1,2),sp.Integer(1),sp.Integer(2))]
    for K,G in zip((0.5,1,2),motors):
        row = G.metrics(200,0.002)
        np.testing.assert_allclose(row[2],motor_rise(K),atol=1e-10)
        error = max(error,G.check_by_integration())
        print(f"K={K}: rise={row[2]:.9f} s, overshoot={row[3]:.9f}%")
    print(f"Symbolic checks passed; maximum independent integration error: {error:.3g}")

    out = Path(__file__).resolve().parent / "ps3-answers-figures"
    out.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size":11, "axes.grid":True, "grid.alpha":0.25,
                         "lines.linewidth":1.7, "svg.fonttype":"none"})
    colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#6C54A3"]
    fig,axes = plt.subplots(1,2,figsize=(11,4),layout="constrained")
    for ax,end in zip(axes,(16,100)):
        time = np.linspace(0,end,8001)
        for K,G,color in zip((0.5,1,2),motors,colors):
            ax.plot(time,G.value(time),color=color,label=f"K = {K:g}")
        ax.axhline(1,color="0.3",lw=0.9,ls="--")
        ax.set(xlabel="Time (s)",ylabel="Shaft angle (rad)",xlim=(0,end),ylim=(0,1.85))
    axes[0].axhline(0.1,color="0.55",lw=0.8,ls=":")
    axes[0].axhline(0.9,color="0.55",lw=0.8,ls=":")
    axes[0].set_title("First rise and overshoot")
    axes[1].set_title("Slow decay at every gain")
    axes[0].legend(loc="lower right")
    fig.savefig(out/"problem-1-step.png",dpi=180)
    plt.close(fig)

    fig,axes = plt.subplots(5,2,figsize=(11,12),layout="constrained")
    for i,(G,color) in enumerate(zip(systems,colors)):
        for j,end in enumerate((3,8)):
            ax=axes[i,j]
            time=np.linspace(0,end,8001)
            ax.axhspan(0.99,1.01,color="0.87",label="1% band")
            ax.axhline(1,color="0.4",lw=0.8,ls="--")
            ax.plot(time,G.value(time),color=color)
            ax.set(xlim=(0,end),ylabel=f"$y_{i+1}(t)$")
            if j==0:
                ax.set_ylim(0,1.45)
                ax.axhline(0.1,color="0.55",lw=0.7,ls=":")
                ax.axhline(0.9,color="0.55",lw=0.7,ls=":")
            else:
                ax.set_ylim(0.965,1.035)
                ax.axvline(metrics[i,4],color=color,ls=":",lw=1.1)
                ax.text(0.97,0.90,f"$t_s$ = {metrics[i,4]:.3f} s",
                        transform=ax.transAxes,ha="right",va="top",
                        bbox={"facecolor":"white","edgecolor":"none","alpha":0.9})
    axes[0,0].set_title("Unit-step responses (10% and 90% guides)")
    axes[0,1].set_title("Settling detail (gray band: 0.99 to 1.01)")
    for ax in axes[-1,:]:
        ax.set_xlabel("Time (s)")
    fig.savefig(out/"problem-2-step.png",dpi=180)
    plt.close(fig)
    print(f"Figures written to {out}")


if __name__ == "__main__":
    main()
