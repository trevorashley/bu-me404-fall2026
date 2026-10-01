# The Root-Locus Design Method I — From a Gain to a Family of Poles

**Student lecture notes — FPE 8th ed., Sections 5.1–5.2; selected examples from §5.3**

A gain changes every closed-loop pole at once. The root locus puts those changes on one picture, so that we can ask which responses feedback can produce before choosing a gain.

**Prerequisites:** [Pole locations and response](time-domain-specs_student.md), [Routh's criterion](stability_student.md), and [feedback equations](feedback-properties_student.md). We use complex numbers as vectors; no complex integration is needed.

**Sources:** Franklin, Powell & Emami-Naeini (FPE), *Feedback Control of Dynamic Systems*, 8th ed., §§5.1–5.3, checked against the corresponding sections of the 7th ed. The motor gain locus is FPE Example 5.1; the damping-parameter locus in §8 is Example 5.2. Nise, *Control Systems Engineering*, 7th ed., §§8.2–8.5, supplements the construction procedure. Åström & Murray, *Feedback Systems*, 2nd ed., §12.5, supplies the repeated-root viewpoint. Examples labelled **[course example]** are our own, not numbered textbook examples. Figures are recomputed from the stated models.

## Learning objectives

1. Put a characteristic equation in the form $a(s)+Kb(s)=0$.
2. Derive and use the angle and magnitude conditions, keeping the sign of the gain explicit.
3. Sketch real-axis segments, endpoints, asymptotes, breakaway points, and departure directions.
4. Find imaginary-axis crossings and the stable gain interval.
5. Explain what a root-locus plot does and does not say about a closed loop.

## Notation and assumptions

| Symbol | Meaning |
|---|---|
| $G(s),D_c(s),H(s)$ | plant, controller, sensor |
| $L(s)=D_c(s)G(s)H(s)=K L_0(s)$ | full loop transfer function; $L_0$ excludes the varied gain |
| $L_0=b/a$ | fixed rational part of the loop |
| $p_i,z_i$ | signed open-loop pole and zero locations |
| $n,m$ | number of poles and zeros, including multiplicity |
| $K$ | real gain, varied from zero toward positive infinity unless stated otherwise |

Negative feedback gives $1+L=0$. In the core rules, $a$ and $b$ are real, monic polynomials with no common factor, $n>m$, and any **positive** fixed scale factor has been absorbed into $K$. Monic means that the highest-power coefficient is one. A negative scale factor must remain explicit (§8). Unity feedback means $H=1$. Signals and motor gains are normalized; time is in seconds and pole coordinates are in $\mathrm{s}^{-1}$.

**Notation bridge:** FPE writes $1+KL(s)=0$ with the gain omitted from its $L$. Our $L_0$ is FPE's $L$; our $L$ retains the meaning used in the earlier course notes.

---

## 1. Why plot a family of roots? {#section-1}

With $H=1$,

$$
\mathcal T(s)=\frac{Y}{R}=\frac{D_cG}{1+D_cG},\qquad
1+KL_0(s)=0\quad\Longleftrightarrow\quad a(s)+Kb(s)=0.
$$

The **root locus** is the set of roots of this polynomial for all permitted $K$. A plotted point is a possible closed-loop pole. A particular gain selects **all $n$ roots together**, not one independently chosen point on each branch.

At $K=0$ the roots are those of $a$; these are the branch starting points. With $D_c=K$, the reference-to-output transfer function vanishes identically at $K=0$, so endpoints are best understood as characteristic roots or limits as $K\to0^+$. More generally, cancelling a factor in $Y/R$ can hide a mode. Check the physical interconnection and internal stability before discarding it.

### Motor position: FPE Example 5.1

The normalized motor model is $G=A/[s(s+c)]$. Set $c=1$ and vary $A=K$, with unit controller and sensor. Equivalently, use $G=1/[s(s+1)]$, $D_c=K$:

$$
s(s+1)+K=0,\qquad
s_{1,2}=-\frac12\pm\sqrt{\frac14-K}.
$$

| Gain | Closed-loop poles | Response character |
|---|---|---|
| $K\to0^+$ | approach $0,-1$ | one very slow mode |
| $0<K<1/4$ | two distinct negative real roots | overdamped |
| $K=1/4$ | repeated root at $-1/2$ | critically damped |
| $K>1/4$ | $-1/2\pm j\sqrt{K-1/4}$ | underdamped |

Increasing gain beyond $1/4$ raises the oscillation frequency but leaves the exponential decay rate at $0.5\ \mathrm{s}^{-1}$. This is the geometric version of the limitation of proportional control from Chapter 4.

![Motor root locus and cubic root locus with breakaway and imaginary-axis crossings](demos/ch5/figures/l1_demo1_motor_cubic.svg)

## 2. The angle test decides where; the magnitude test decides the gain {#section-2}

For $K>0$ and a point away from poles and zeros,

$$
KL_0(s)=-1
\quad\Longrightarrow\quad
\boxed{\arg L_0(s)=(2\ell+1)180^\circ},\qquad
\boxed{K=\frac1{|L_0(s)|}}.
$$

Factoring $a$ and $b$ gives

$$
\sum_{i=1}^m\arg(s-z_i)-\sum_{i=1}^n\arg(s-p_i)
=(2\ell+1)180^\circ,
\qquad
K=\frac{\prod_i|s-p_i|}{\prod_i|s-z_i|}.
$$

The vector runs **from a pole or zero to the trial point**. Its angle is measured counterclockwise from the positive real axis. Use a quadrant-aware angle: the vector $-1+j$ has angle $135^\circ$, not $-45^\circ$. Angles differing by $360^\circ$ represent the same direction.

For the motor at $s_d=-1/2+j\sqrt3/2$, the two pole-vector angles are $120^\circ$ and $60^\circ$. Their negative sum is $-180^\circ$, so the point is on the locus. Both distances are one, giving $K=1$.

**Check:** Substituting this $s_d$ into $s_d(s_d+1)$ gives $-1$. A magnitude calculation alone would assign a positive number to any trial point, even one that fails the angle test.

## 3. Rules for a positive-gain locus {#section-3}

| Feature | Construction rule |
|---|---|
| Branch count | $n$ branches, counting repeated roots |
| Symmetry | reflection about the real axis, because coefficients are real |
| Starting points | poles $p_i$ as $K\to0^+$ |
| Ending points | $m$ branches approach finite zeros; $n-m$ go to infinity |
| Real-axis segments | a real point is on the locus if an odd number of real poles and zeros lie to its right, counting multiplicity |
| Asymptote angles | $\theta_q=(2q+1)180^\circ/(n-m)$, $q=0,\ldots,n-m-1$ |
| Asymptote intersection | $\displaystyle\sigma_a=\frac{\sum p_i-\sum z_i}{n-m}$ |

Why odd? A real pole or zero to the right contributes a $180^\circ$ vector angle; one to the left contributes $0^\circ$. Complex conjugate pairs contribute zero modulo $360^\circ$. For parity, subtracting a pole angle and adding a zero angle have the same effect.

Asymptotes describe the far-away branches, not necessarily the locus near the plant poles. They intersect at $\sigma_a$, which need not itself be a point on the locus.

## 4. Breakaway and break-in points {#section-4}

On the real axis,

$$
K(s)=-\frac{a(s)}{b(s)}.
$$

A multiple closed-loop root satisfies both $a+Kb=0$ and $a'+Kb'=0$. Eliminating $K$ gives

$$
\boxed{a'b-ab'=0}\qquad\text{or}\qquad \frac{dK}{ds}=0,
$$

provided $b(s)\ne0$. These are **candidates**. Keep only real candidates on an allowed real-axis segment with $K>0$. At a real double root with $P_{ss}\ne0$, a two-branch breakaway leaves the real axis at $\pm90^\circ$. If $P_{ss}=0$, the root has higher multiplicity and requires its own angle calculation.

For the motor, $K=-s^2-s$, so $dK/ds=-2s-1=0$ gives $s=-1/2$, $K=1/4$.

## 5. A complete cubic sketch [course example] {#section-5}

Let

$$
L_0(s)=\frac1{s(s+2)(s+4)},\qquad
P(s,K)=s^3+6s^2+8s+K.
$$

The poles are $0,-2,-4$; there are no finite zeros. Real-axis segments are $(-\infty,-4)$ and $(-2,0)$. All three branches go to infinity, with

$$
\sigma_a=-2,\qquad \theta=60^\circ,180^\circ,300^\circ.
$$

The stationary-gain equation is

$$
3s^2+12s+8=0
\quad\Longrightarrow\quad s=-2\pm\frac{2\sqrt3}{3}.
$$

Only $s=-0.8453$ lies on a positive-gain segment. It gives $K=16\sqrt3/9\approx3.0792$. The other candidate gives negative gain and is rejected.

For stability, use the Routh array:

$$
\begin{array}{c|cc}
s^3&1&8\\
s^2&6&K\\
s^1&(48-K)/6&0\\
s^0&K&0
\end{array}
\qquad\Longrightarrow\qquad \boxed{0<K<48}.
$$

At $K=48$, the auxiliary polynomial is $6s^2+48$, giving $s=\pm j\sqrt8$; the remaining root is $-6$. Indeed,

$$
s^3+6s^2+8s+48=(s+6)(s^2+8).
$$

The imaginary roots describe sustained oscillations in the zero-input linear model. This boundary is not BIBO stable. Above it two branches enter the RHP. Thus more gain eventually destabilizes this plant, even though more gain always keeps the earlier motor model stable.

## 6. Departure and arrival directions {#section-6}

Near a simple complex pole $p_k$, the vector $s-p_k$ is the only vector whose angle is still unknown. The angle condition gives

$$
\theta_{\mathrm{dep}}=180^\circ+\sum_i\arg(p_k-z_i)
-\sum_{i\ne k}\arg(p_k-p_i)\pmod{360^\circ}.
$$

**Optional reference: arrival at a zero.** Near a simple zero $z_k$,

$$
\theta_{\mathrm{arr}}=180^\circ-\sum_{i\ne k}\arg(z_k-z_i)
+\sum_i\arg(z_k-p_i)\pmod{360^\circ}.
$$

The arrival angle here is the angle of $s-z_k$, pointing **from the zero to nearby locus points**. The direction of motion toward the zero is opposite that ray.

**[Course example]** For $L_0=1/[(s+4)(s^2+2s+5)]$, the upper pole is $-1+2j$. Vectors from the other poles have angles $90^\circ$ and $\tan^{-1}(2/3)=33.69^\circ$, so

$$
\theta_{\mathrm{dep}}=180^\circ-90^\circ-33.69^\circ=56.31^\circ.
$$

Its branch initially moves rightward: an LHP open-loop pole need not initially move deeper into the LHP under feedback.

### Repeated poles

If $L_0(s)=b(s)/[(s-p)^q\widetilde a(s)]$, then near $p$,

$$
(s-p)^q\approx-K\frac{b(p)}{\widetilde a(p)}.
$$

There are $q$ departure rays separated by $360^\circ/q$. For the rigid satellite model $L_0=1/s^2$, $s^2=-K$ gives $\pm90^\circ$: proportional control creates oscillation, but no damping. This connects FPE's satellite examples in §5.3 to the local repeated-root argument in Åström–Murray §12.5.

![Complex-pole departure, repeated origin poles, and a right-half-plane-zero example](demos/ch5/figures/l1_demo2_departure.svg)

## 7. Sketch first, compute second {#section-7}

1. Derive the characteristic polynomial and identify the varied parameter.
2. Mark poles and zeros; determine real-axis segments and asymptotes.
3. Find relevant breakaway points and departure angles.
4. Use Routh or $s=j\omega$ to locate crossings.
5. Compute roots at a few gains, including every root at each gain.
6. Add arrows for increasing gain. Verify any proposed design in the time domain.

A numerical plot fills in the curves. It does not replace the sign, stability, or cancellation checks.

```matlab
s = tf('s');                      % Control System Toolbox
L0 = 1/(s*(s+2)*(s+4));
rlocus(L0); grid on
K = 48;
roots([1 6 8 K])                  % Characteristic roots at this gain
```

## 8. Extensions: another parameter or another sign {#section-8}

FPE Example 5.2 (both editions) varies a plant pole rather than controller gain. For $s^2+cs+A=0$, fixed $A>0$ and variable $c\ge0$ give

$$
1+c\frac{s}{s^2+A}=0.
$$

That is a different locus, with starting poles $\pm j\sqrt A$ and a zero at zero. It describes increasing physical damping, not increasing motor gain.

For negative $K$, or positive feedback written $1-KL_0=0$, the angle condition is $0^\circ$ modulo $360^\circ$. Re-derive the real-axis and asymptote rules for that sign.

**[Course example]** $L_0=(1-s)/[s(s+2)]$ has a positive DC-direction numerator but a **negative leading coefficient**. Do not replace $1-s$ by $s-1$ without retaining the minus sign. The closed-loop polynomial is

$$
s^2+(2-K)s+K,
$$

stable only for $0<K<2$. As $K\to\infty$, one root approaches the RHP zero at $+1$. Endpoint reasoning identifies a high-gain limitation before detailed design.

## Review questions

1. For the motor at $s=-1+j$, why does the magnitude condition alone give a misleading candidate gain?
2. Why does the cubic's breakaway equation have a real solution that is not on the positive-gain locus?
3. Does an asymptote at $60^\circ$ imply that the system is unstable at every gain?
4. For a double pole at the origin, why are departure angles not found by inserting the other coincident pole into the simple-pole formula?
5. Sketch the real-axis segments for poles $0,-1,-3$ and a zero at $-2$.

## Optional practice and demonstrations

Work FPE §5.2's construction rules on one new pole-zero pattern, then check it numerically. Nise 7th ed. §8.5 provides additional breakaway and departure practice. Run `l1_demo1_motor_cubic.py` and `l1_demo2_departure.py`; instructions and a MATLAB alternative are in the [demo guide](demos/ch5/guide.md).

**Next:** [II — Reading the locus and selecting gain](root-locus-gain-design_student.md).
