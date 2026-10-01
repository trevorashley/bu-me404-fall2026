"""Symbolic derivations and independent numerical checks for all four lectures.

Requires SymPy as well as the demo dependencies. This is an instructor check,
not a prerequisite for students running the demonstrations.
"""
import numpy as np
import sympy as sp
from scipy import signal

import kit

s, K, a, p, z = sp.symbols("s K a p z", real=True)
q = sp.Rational


def equal(left, right):
    assert sp.simplify(left-right) == 0, (left, right)


def main():
    # Construction, repeated roots, and gain selection.
    cubic = s*(s+2)*(s+4)+K
    equal(cubic.subs(K, 48), (s+6)*(s*s+8))
    sb = -2+2*sp.sqrt(3)/3
    equal(sp.diff(cubic, s).subs(s, sb), 0)
    equal((-s*(s+2)*(s+4)).subs(s, sb), 16*sp.sqrt(3)/9)
    equal(cubic.subs(K, q(224, 27)), (s+q(14, 3))*(s*s+q(4, 3)*s+q(16, 9)))
    sd = -2+2*sp.I
    equal(3*(sd+q(8, 3))/(sd*(sd+1)), -1)
    equal(20*(sd+2)/(sd*(sd+1)*(sd+8)), -1)
    equal(s*(s+1)+3*s+8, s*s+4*s+8)
    equal(s*(s+1)*(s+8)+20*(s+2), (s+5)*(s*s+4*s+8))
    # Alternate lead zero z=11/5.
    equal(s*(s+1)*(s+q(76, 7))+q(200, 7)*(s+q(11, 5)),
          (s+q(55, 7))*(s*s+4*s+8))
    # A zero beyond the PD zero cannot supply enough angle for this target.
    required_angle = np.arctan(3)
    np.testing.assert_allclose(np.angle(complex(sd+q(8, 3))), required_angle)
    assert np.angle(complex(sd+3)) < required_angle
    # Independent partial-fraction identities underlying all analytic responses.
    equal((3*s+8)/(s*(s*s+4*s+8)), 1/s+(-s-1)/(s*s+4*s+8))
    equal(20*(s+2)/(s*(s+5)*(s*s+4*s+8)),
          1/s+q(12, 13)/(s+5)+(-q(25, 13)*s-q(40, 13))/(s*s+4*s+8))
    equal(q(224, 27)/(s*cubic.subs(K, q(224, 27))),
          1/s-q(4, 39)/(s+q(14, 3))
          +(-q(35, 39)*s-q(196, 117))/(s*s+q(4, 3)*s+q(16, 9)))
    # General lag/PI characteristic and error constants.
    char = s*(s+a)*(s+p)+K*(s+z)
    equal(char, s**3+(a+p)*s*s+(a*p+K)*s+K*z)
    equal(sp.limit((s+a)*(s+p)/char, s, 0), a*p/(K*z))
    equal(sp.limit((s+p)/char, s, 0), p/(K*z))
    equal(char.subs({p: 0, z: a}), (s+a)*(s*s+K))
    char_pi = char.subs(p, 0)
    equal(sp.limit(s*(s+a)/char_pi, s, 0), 0)
    equal(sp.limit((s+a)/char_pi, s, 0), a/(K*z))
    leadlag = s*(s+1)*(s+13)*(s+q(1, 100))+91*(s+2)*(s+q(1, 20))
    equal(leadlag, s**4+q(1401, 100)*s**3+q(5207, 50)*s*s+q(4667, 25)*s+q(91, 10))
    equal(sp.limit(s*91*(s+2)*(s+q(1, 20))/(s*(s+1)*(s+13)*(s+q(1, 100))), s, 0), 70)
    equal(K*(s+z)/(s+p), K*z/p + (K*(p-z)/p**2)*s/(1+s/p))
    print("Symbolic identities: construction, pole placement, partial fractions, lag/PI, lead-lag, filtering passed.")

    # Compare time-domain formulas against independent scipy state-space step responses.
    t = np.linspace(0, 20, 20001)
    cases = [
        ([3, 8], [1, 4, 8], 1-np.exp(-2*t)*np.cos(2*t)+.5*np.exp(-2*t)*np.sin(2*t)),
        ([20, 40], [1, 9, 28, 40], 1+12/13*np.exp(-5*t)-25/13*np.exp(-2*t)*np.cos(2*t)
         +5/13*np.exp(-2*t)*np.sin(2*t)),
        ([224/27], [1, 6, 8, 224/27], 1-4/39*np.exp(-14*t/3)
         -35/39*np.exp(-2*t/3)*np.cos(2*np.sqrt(3)*t/3)
         -7*np.sqrt(3)/13*np.exp(-2*t/3)*np.sin(2*np.sqrt(3)*t/3)),
    ]
    for num, den, expected in cases:
        _, measured = signal.step(signal.TransferFunction(num, den), T=t)
        np.testing.assert_allclose(measured, expected, atol=2e-11)
    # The course uses 1% settling: check against the exact first-order result.
    first_order = signal.TransferFunction([1], [1, 1])
    _, first_metrics = kit.metrics(first_order, t)
    assert 0 <= first_metrics[2]-np.log(100) <= t[1]-t[0]
    # Compare full responses, keeping rough design formulas out of this table.
    pair = signal.TransferFunction([16/9], [1, 4/3, 16/9])
    cubic_selected = signal.TransferFunction([224/27], [1, 6, 8, 224/27])
    _, pair_metrics = kit.metrics(pair, t)
    _, cubic_metrics = kit.metrics(cubic_selected, t)
    assert cubic_metrics[1] > pair_metrics[1]
    assert cubic_metrics[2] > pair_metrics[2]
    np.testing.assert_allclose(pair_metrics[1:], [1.228, 6.586], atol=.001)
    np.testing.assert_allclose(cubic_metrics[1:], [1.296, 6.803], atol=.001)
    # Verify complete specs for the final Franklin design, not just pole damping.
    final = kit.closed_loop([91, 182], [1, 14, 13, 0])
    _, (overshoot, rise, settling) = kit.metrics(final, np.linspace(0, 8, 32001))
    assert overshoot < 20 and rise < .3
    np.testing.assert_allclose([overshoot, rise, settling], [16.8562, .1895, 1.3945], atol=.0003)
    initial = kit.closed_loop([70, 140], [1, 11, 10, 0])
    _, initial_metrics = kit.metrics(initial, np.linspace(0, 8, 32001))
    assert settling < initial_metrics[2]  # The comparison uses the same 1% band.
    # Check the Routh interval numerically on both sides and verify full poles.
    for gain, unstable in [(1, 0), (40, 0), (60, 2)]:
        assert np.count_nonzero(np.roots([1, 6, 8, gain]).real > 0) == unstable
    for label, zero, pole in [("lag initial", .05, .01), ("lag final", .01, .002), ("PI", .01, 0)]:
        den = [1, 1+pole, 1+pole, zero]
        roots = np.roots(den)
        assert np.all(roots.real < 0)
        residues, poles, _ = signal.residue([1, zero], np.polymul(den, [1, 0]))
        slow = min((x for x in roots if abs(x.imag) < 1e-8), key=abs)
        rr = residues[np.argmin(abs(poles-slow))].real
        print(f"{label}: poles {roots}, slow reference-step residue {rr:.8f}")
        # Analytic ramp error: E(s)= (s+1)(s+p)/(s P(s)), with p=0 for PI.
        er = signal.TransferFunction(np.polymul([1, 1], [1, pole]), np.polymul([1, 0], den))
        # impulse_response here inverts E(s), which already includes R=1/s^2.
        tl = np.linspace(0, 1800, 18001)
        _, error = signal.impulse(er, T=tl)
        np.testing.assert_allclose(error[-1], pole/zero, atol=2e-6)
        print(f"  ramp error at 1800 s: {error[-1]:.8f}; final-value prediction {pole/zero:.8f}")
    coeff = np.array([1, 14.01, 104.14, 186.68, 9.1])
    assert np.all(np.roots(coeff).real < 0)
    b1 = (coeff[1]*coeff[2]-coeff[3])/coeff[1]
    c1 = (b1*coeff[3]-coeff[1]*coeff[4])/b1
    print("Lead-lag roots:", np.roots(coeff), "Routh:", b1, c1)
    print("Independent numerical checks passed.")


if __name__ == "__main__":
    main()
