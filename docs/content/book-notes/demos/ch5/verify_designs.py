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
    # FPE Section 5.2 examples: Eq. (5.18) trial point, Eq. (5.20) locus, and Section 5.2.3 gain.
    s0 = -1+2*sp.I
    phase = sum(sp.arg(s0-zz) for zz in [-1]) - sum(sp.arg(s0-pp) for pp in [0, -5, -2+2*sp.I, -2-2*sp.I])
    np.testing.assert_allclose(float(sp.deg(phase)), -129.0939, atol=1e-3)
    fpe = s*(s*s+8*s+32)+K
    equal(fpe.subs(K, 64), (s+4)*(s*s+4*s+16))
    equal(fpe.subs(K, 256), (s+8)*(s*s+32))
    pk = -4+4*sp.I
    equal(sp.diff(fpe, s).subs(s, pk), -32-32*sp.I)      # ds/dK = -1/a'(p) has angle -45 degrees
    np.testing.assert_allclose(np.degrees(np.angle(complex(-1/(-32-32*sp.I)))), -45.0)
    s0 = -2+2*sp.sqrt(3)*sp.I
    equal(sp.simplify(sp.Abs(s0)*sp.Abs(s0-pk)*sp.Abs(s0-sp.conjugate(pk))), 64)
    theta = sp.symbols("theta", real=True)
    # FPE Fig. 5.22 (Lecture III, section 1): PD K(s+z) on the motor gives a circle of radius sqrt(z(z-1)) about -z.
    rr = sp.symbols("r", positive=True)
    pt = -z+rr*sp.exp(sp.I*theta)
    Kpd = sp.expand_complex(-pt*(pt+1)/(pt+z))
    equal(sp.simplify(sp.im(Kpd).subs(rr, sp.sqrt(z*z-z))), 0)
    equal(sp.simplify(sp.re(Kpd).subs(rr, sp.sqrt(z*z-z))), 2*z-1-2*sp.sqrt(z*z-z)*sp.cos(theta))
    equal(sp.expand(s*(s+1)+4), s*s+s+4)            # proportional at wn=2: zeta=1/4
    equal(sp.expand(s*(s+1)+2*(s+2)), s*s+3*s+4)    # PD K(s+2) at wn=2: zeta=3/4
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
    # FPE Section 5.3 examples (Lecture II, sections 1-4).
    spt = -1+sp.exp(sp.I*theta)
    equal(sp.simplify(sp.expand_complex(-spt**2/(spt+1))), 2-2*sp.cos(theta))     # Ex. 5.3 circle
    equal(s*s+4*(s+1), (s+2)**2)
    equal(sp.expand(sp.diff(s*s*(s+p), s)*(s+1)-s*s*(s+p)), sp.expand(s*(2*s*s+(3+p)*s+2*p)))
    equal(sp.expand((3+p)**2-16*p), sp.expand((p-1)*(p-9)))                       # Ex. 5.4-5.6 discriminant
    equal(s*s*(s+9)+27*(s+1), (s+3)**3)                                           # Ex. 5.6 triple root
    ex10 = s*(s+2)*((s+1)**2+4)+K
    equal(ex10.subs(K, 4), (s+1)**2*(s*s+2*s+4))                                  # Ex. 5.10
    equal(ex10.subs(K, q(25, 4)), (s*s+2*s+q(5, 2))**2)
    flex_pole = -0.1+6.6j
    others = [0, 0, -12, -0.1-6.6j]
    def dep(zeros):
        total = sum(np.degrees(np.angle(flex_pole-zz)) for zz in zeros)
        total -= sum(np.degrees(np.angle(flex_pole-pp)) for pp in others) + 180
        return (total+180) % 360-180
    np.testing.assert_allclose(dep([-1, -0.1+6j, -0.1-6j]), 141.485, atol=1e-2)  # Ex. 5.8 (FPE: 142.6)
    np.testing.assert_allclose(dep([-1]), -38.515, atol=1e-2)                     # Ex. 5.9 (FPE: -37.4)
    flex_den = np.polymul([1, 12], np.polymul([1, 0.2, 0.01+6.6**2], [1, 0, 0]))
    assert max(np.roots(np.polyadd(flex_den, 144.437*np.array([1., 1.]))).real) < 1e-3
    assert max(np.roots(np.polyadd(flex_den, 145*np.array([1., 1.]))).real) > 0
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
    # Lecture III, section 4: general lead construction reproduces p=8 for z=2, and the feasibility limit z=8/3.
    phi_c = np.degrees(np.angle(complex(sd*(sd+1))))-180+360   # 71.565 degrees
    theta_z = np.degrees(np.arctan2(2, 2-2)); theta_p = theta_z-phi_c
    np.testing.assert_allclose(2+2/np.tan(np.radians(theta_p)), 8)
    np.testing.assert_allclose(2/np.tan(np.radians(phi_c)), 2/3)                 # theta_p -> 0 at z = 8/3
    # Lecture IV, section 9: FPE Example 5.15 tachometer numbers and the course rate-feedback design.
    equal(sp.expand(s*s+s+4+1*s), sp.expand((s+1-sp.sqrt(3)*sp.I)*(s+1+sp.sqrt(3)*sp.I)))
    equal(sp.expand(s*(s+1)+3*s+8), s*s+4*s+8)
    # Lecture IV, section 8: FPE Eqs. (5.74)-(5.76). The notch flips the flexible mode's departure angle.
    flex = complex(-q(1, 2)+sp.sqrt(q(9999, 4))*sp.I)
    def departure(zeros, poles):
        total = sum(np.degrees(np.angle(flex-zz)) for zz in zeros)
        total -= sum(np.degrees(np.angle(flex-pp)) for pp in poles if abs(pp-flex) > 1e-9)+180
        return (total+180) % 360-180
    base_z, base_p = [-2, -.05], [0, -1, -13, -.01, flex, flex.conjugate()]
    notch_z = list(np.roots([1, .8, 3600]))
    np.testing.assert_allclose(departure(base_z, base_p), -77.73, atol=.01)
    np.testing.assert_allclose(departure(base_z+notch_z, base_p+[-60, -60]), -158.33, atol=.01)
    loop_num = 2500*91*np.polymul([1, 2], [1, .05])
    loop_den = np.polymul(np.polymul([1, 1, 0], [1, 1, 2500]), np.polymul([1, 13], [1, .01]))
    no_notch = np.roots(np.polyadd(loop_den, loop_num))
    with_notch = np.roots(np.polyadd(np.polymul(loop_den, np.polymul([1, 60], [1, 60])), np.polymul(loop_num, [1, .8, 3600])))
    flex_no = max((x for x in no_notch if x.imag > 40), key=lambda x: x.imag)
    flex_yes = max((x for x in with_notch if x.imag > 40), key=lambda x: x.imag)
    np.testing.assert_allclose([flex_no.real, flex_yes.real], [-0.2913, -0.6527], atol=5e-4)
    assert np.all(no_notch.real < 0) and np.all(with_notch.real < 0)
    print("Symbolic identities: construction, FPE 5.2-5.4 examples, pole placement, partial fractions, lag/PI, lead-lag, notch, filtering passed.")

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
