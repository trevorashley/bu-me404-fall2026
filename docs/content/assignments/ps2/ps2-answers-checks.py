"""Symbolic checks for the PS2 answer key. Requires SymPy.

Run: python ps2-answers-checks.py
An assertion failure indicates a mismatch; a successful run prints a summary.
"""

import sympy as sp


def equal(left, right):
    assert sp.simplify(sp.expand_complex(left - right)) == 0, (left, right)


t = sp.symbols("t", real=True)
s = sp.symbols("s", positive=True)
k = sp.symbols("k", integer=True, nonzero=True)
alpha = sp.symbols("alpha", real=True, nonzero=True)
j = sp.I

# Problem 1: Integrate the original signals, independently of their formulas.
c_saw = sp.integrate(t*sp.exp(-j*k*sp.pi*t), (t, -1, 1))/2
equal(c_saw, j*(-1)**k/(sp.pi*k))
equal(sp.integrate(t, (t, -1, 1))/2, 0)
c_trap = (sp.integrate(sp.cos(alpha*t), (t, 0, 1))
          + sp.integrate((2-t)*sp.cos(alpha*t), (t, 1, 2)))/3
equal(c_trap, (sp.cos(alpha)-sp.cos(2*alpha))/(3*alpha**2))
equal((sp.integrate(1, (t, 0, 1))
       + sp.integrate(2-t, (t, 1, 2)))/3, sp.Rational(1, 2))
rc = t-sp.Rational(1, 2)+2*sp.exp(-2*(t+1))/(1-sp.exp(-4))
equal(sp.diff(rc, t)/2+rc, t)
equal(rc.subs(t, -1), rc.subs(t, 1))

# Problem 2: Initial values, ODE residuals, and unilateral transforms.
b = sp.sqrt(11)/2
ya = sp.exp(-t/2)*(sp.cos(b*t)+5/sp.sqrt(11)*sp.sin(b*t))
yb = 4-sp.Rational(5, 2)*sp.exp(-t)-sp.cos(t)/2-sp.sin(t)/2
yc = t+sp.cos(t)-2*sp.sin(t)
cases = [
    (ya, 1, 2, 1, 3, 0, (s+3)/(s**2+s+3)),
    (yb, 1, 2, 1, 0, sp.sin(t), (s+3+1/(s**2+1))/(s*(s+1))),
    (yc, 1, -1, 0, 1, t, (s-1+1/s**2)/(s**2+1)),
]
for y, initial, velocity, damping, stiffness, forcing, transform in cases:
    equal(y.subs(t, 0), initial)
    equal(sp.diff(y, t).subs(t, 0), velocity)
    equal(sp.diff(y, t, 2)+damping*sp.diff(y, t)+stiffness*y, forcing)
    equal(sp.laplace_transform(y, t, s, noconds=True), transform)
equal(cases[1][-1], 4/s-sp.Rational(5, 2)/(s+1)-(s+1)/(2*(s**2+1)))
equal(cases[2][-1], 1/s**2+(s-2)/(s**2+1))

# Problem 3: Transform the piecewise step response directly.
H = sp.integrate(sp.exp(-s*t), (t, 0, 2))
equal(H, (1-sp.exp(-2*s))/s)
equal(sp.limit(H, s, 0), 2)
Y = sp.integrate(t*sp.exp(-s*t), (t, 0, 2)) + sp.integrate(2*sp.exp(-s*t), (t, 2, sp.oo))
equal(Y, H/s)

# Problem 4: Solve signal equations with R=1, then compare reductions.
G1, G2, G3, G4, G5, G6, G7 = sp.symbols("G1:8", real=True)
V, W, Ysignal = sp.symbols("V W Y", real=True)
sol = sp.solve([V-G1*(1-V), Ysignal-V-G2], [V, Ysignal])
equal(sol[Ysignal], G1/(1+G1)+G2)
sol = sp.solve([V-G1*(1-G2*V), W-G4*(G3*V-G5*W),
                Ysignal-G6*W-G7], [V, W, Ysignal])
equal(sol[Ysignal], G1*G3*G4*G6/((1+G1*G2)*(1+G4*G5))+G7)
equal(sol[Ysignal].subs(G7, 0), G1*G3*G4*G6/((1+G1*G2)*(1+G4*G5)))
sol = sp.solve([V-G2*(G1-V), W-G4*(G3*V+G6-W),
                Ysignal-G5*W-G7], [V, W, Ysignal])
equal(sol[Ysignal], G5*G4/(1+G4)*(G1*G2*G3/(1+G2)+G6)+G7)
equal(sol[Ysignal].subs(G3, 0), G4*G5*G6/(1+G4)+G7)

# Problem 5: Derive the loop transfer and verify the exact step response.
K, a = sp.symbols("K a", positive=True)
L = 100*K/((s+a)*(s+25))
T = 100*K/(s**2+(a+25)*s+25*a+100*K)
equal(L/(1+L), T)
y5 = sp.Rational(61, 80)*(1-sp.exp(-60*t)*(sp.cos(80*t)+sp.Rational(3, 4)*sp.sin(80*t)))
equal(y5.subs(t, 0), 0)
equal(sp.diff(y5, t).subs(t, 0), 0)
equal(sp.diff(y5, t, 2)+120*sp.diff(y5, t)+10000*y5, 7625)
equal(sp.laplace_transform(y5, t, s, noconds=True), T.subs({K: sp.Rational(305, 4), a: 95})/s)
print("All symbolic checks passed: Fourier integrals, RC solution, IVPs, convolution, block diagrams, and controller response.")
