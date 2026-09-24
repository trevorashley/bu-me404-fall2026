# Dynamic Response II — Block Diagrams and the Effect of Pole Locations

**Student lecture notes — FPE 8th ed., Sections 3.2 and 3.3**

A block diagram is a set of simultaneous equations. Eliminating its internal signals gives a transfer function; the poles of that function describe the rates and oscillations visible in the response. This lecture connects block reduction to the geometry of the complex $s$-plane.

**Prerequisites:** [L1: Convolution and transfer functions](convolution-impulse-response_student.md).

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed. Example and equation numbers follow the textbook. Numbered sections and § references refer to these notes unless labelled as textbook sections.

## Learning objectives

After studying this lecture, you should be able to:

1. Write the equations a block diagram represents, and recover the diagram from the equations.
2. Reduce series, parallel and feedback connections, and state the single-loop rule: forward gain over one plus loop gain.
3. Move a pickoff point or a summing junction without changing the relationships, and convert a loop to unity feedback.
4. Reduce a multi-loop diagram with a nested positive-feedback loop (Example 3.23).
5. Use `series`, `parallel` and `feedback` (or their equivalents) to do the same job numerically, and say where Mason's rule fits.
6. Explain how an impulse excites natural modes, and read the time constant $\tau=1/\sigma$ off a first-order pole.
7. Explain what the numerator contributes to a partial-fraction expansion, and what the denominator contributes (Example 3.25).
8. Relate location in the $s$-plane $\rightarrow$ shape of the natural response.
9. Convert between $(\sigma,\omega_d)$ and $(\zeta,\omega_n)$, and place a pole by radius and angle.
10. Write down the impulse and step responses of the standard second-order system, and sketch the exponential envelope (Example 3.26).

## Notation and assumptions

| Symbol | Meaning |
|---|---|
| $R(s),\ Y(s)$ | reference (input) and output transforms |
| $G_i(s)$ | transfer function of one block |
| $T(s)$ | closed-loop transfer function $Y/R$ |
| $\sigma$ | **minus** the real part of a pole: a stable pole is $s=-\sigma\pm j\omega_d$ with $\sigma>0$ |
| $\tau=1/\sigma$ | time constant of a first-order pole |
| $\zeta,\ \omega_n$ | damping ratio and undamped natural frequency |
| $\omega_d=\omega_n\sqrt{1-\zeta^2}$ | damped natural frequency |
| $\theta=\sin^{-1}\zeta$ | angle of the pole from the imaginary axis |

Unless stated otherwise, transfer functions describe causal LTI systems from zero initial state. Add the zero-input response for nonzero initial conditions. LHP and RHP mean the left and right half planes.

The decay rate $\sigma$ is positive for a stable pole: $s=-\sigma\pm j\omega_d$. It is the negative of the pole’s real part.

---

## 1. From components to response {#section-1}

Real feedback systems contain several components: controller, actuator, plant, and sensor. Block reduction combines their equations into one input-output transfer function. The resulting pole locations then show whether its visible modes decay, oscillate, or grow.

---

## 2. Block diagrams {#section-2}

### 2.1 Three elementary connections {#section-2-1}

| Connection | Diagram | Transfer function |
|---|---|---|
| Series | $G_1$ then $G_2$ | $G_2G_1$ |
| Parallel | $G_1$ and $G_2$ share the same input; outputs added | $G_1+G_2$ |
| Feedback | $G_1$ forward, $G_2$ returned and subtracted | $\dfrac{G_1}{1+G_1G_2}$ |

The first two need only one line each. Write $U$ for the input and $Y$ for the output.

- **Series.** The intermediate signal is $V=G_1U$, and $Y=G_2V=G_2G_1U$. For scalar transfer functions the order does not matter, but writing $G_2G_1$ keeps the signal-flow order, which matters for matrices later.
- **Parallel.** $Y=G_1U+G_2U=(G_1+G_2)U$.

### 2.2 Deriving the feedback rule {#section-2-2}

Assume zero initial conditions and a well-posed scalar interconnection. These algebraic identities compute input-output transfer functions; they do not establish internal stability.

Eliminate the internal signals to derive the feedback formula.

The diagram says three things:

$$
U_1(s)=R(s)-Y_2(s),
\qquad
Y_2(s)=G_2(s)G_1(s)U_1(s),
\qquad
Y_1(s)=G_1(s)U_1(s).
$$

Here $U_1$ is the error signal leaving the summing junction and $Y_2$ is the signal fed back.

*Step 1: eliminate $Y_2$.* Substitute the second equation into the first:

$$
U_1=R-G_2G_1U_1 .
$$

*Step 2: solve for the error.* Collect the $U_1$ terms:

$$
(1+G_1G_2)U_1=R
\qquad\Longrightarrow\qquad
U_1=\frac{R}{1+G_1G_2} .
$$

*Step 3: substitute into the output equation.* $Y_1=G_1U_1$, so

$$
\boxed{
Y_1(s)=\frac{G_1(s)}{1+G_1(s)G_2(s)}\,R(s)
\tag{3.58}
}
$$

For negative feedback,

$$
\boxed{
\text{closed-loop gain}=\frac{\text{forward gain}}{1+\text{loop gain}}
}
$$

For **positive** feedback the first equation becomes $U_1=R+Y_2$. Step 2 then gives $(1-G_1G_2)U_1=R$, so the denominator is $1-\text{loop gain}$.

#### Check your understanding

> If the loop gain is very large, what is the closed-loop gain?

Divide the numerator and denominator by $G_1G_2$:

$$
\frac{G_1}{1+G_1G_2}=\frac{1/G_2}{1/(G_1G_2)+1}\ \longrightarrow\ \frac{1}{G_2}
\qquad\text{when } |G_1G_2|\gg1 .
$$

At frequencies where $|G_1G_2|\gg1$, the closed-loop transfer is approximately $1/G_2$ and becomes less sensitive to the forward path. This is useful only when the interconnection is stable; increasing gain does not by itself guarantee stability or good transients.

### 2.3 Moving things around {#section-2-3}

The governing principle, in the book's words: *block-diagram reduction is a pictorial way to solve equations by eliminating variables.* Everything in this section is legal because the underlying equations are unchanged.

**Signal identities:** if $v=Gu$, taking off $u$ after the block requires $v/G$, while taking off $v$ before it requires $Gu$. Likewise, $G(u+d)=Gu+Gd$: moving an input-side sum to the output multiplies its side input by $G$. These are algebraic rearrangements for nonzero $G$; $1/G$ may be unstable or improper and need not be physically implementable.

For nonzero $G_2$, a nonunity feedback loop has $Y/R=(1/G_2)[G_1G_2/(1+G_1G_2)]$. In the original diagram the error is $e=R-G_2Y$. In the equivalent diagram of Fig. 3.10(c), a prefilter $1/G_2$ precedes a unity-feedback loop around $G_1G_2$: its error is $e'=R/G_2-Y=e/G_2$, and $Y=G_1G_2e'=G_1e$. Thus $Y/R$ is unchanged, but the signal at the summing junction is rescaled. Canceling $G_2$ in the overall transfer function recovers Eq. (3.58).

---

## 3. Two worked reductions {#section-3}

### 3.1 Example 3.22 {#section-3-1}

The forward path is a gain of 2 in parallel with $4/s$, followed by an integrator $1/s$, all inside unity negative feedback. Reduce in two steps:

$$
\text{parallel: } 2+\frac4s=\frac{2s+4}{s},
\qquad
\text{series: } \frac{2s+4}{s}\cdot\frac1s=\frac{2s+4}{s^2},
$$

then the feedback rule with $G_1=(2s+4)/s^2$ and unity feedback, $G_2=1$. Multiply the numerator and denominator by $s^2$ to clear the inner fractions:

$$
\boxed{
T(s)=\frac{Y(s)}{R(s)}
=\frac{(2s+4)/s^2}{1+(2s+4)/s^2}
=\frac{2s+4}{s^2+(2s+4)}
=\frac{2s+4}{s^2+2s+4}
}
$$

For unity feedback this is $G/(1+G)$, which is the numerator of $G$ over its numerator plus its denominator. That is a useful shortcut.

#### Check your understanding

> Where are the closed-loop poles, and what were the poles of the forward path?

The forward path had a double pole at the origin, from $s^2=0$. For the closed loop, solve $s^2+2s+4=0$:

$$
s=\frac{-2\pm\sqrt{4-16}}{2}=-1\pm j\frac{\sqrt{12}}{2}=-1\pm j\sqrt3 .
$$

**Feedback moved the poles.** In the second-order notation of §7, match $s^2+2s+4$ to $s^2+2\zeta\omega_ns+\omega_n^2$. This gives $\omega_n^2=4$, so $\omega_n=2$ rad/s, and $2\zeta\omega_n=2$, so $\zeta=0.5$. Check: $\sigma=\zeta\omega_n=1$ and $\omega_d=2\sqrt{1-0.25}=\sqrt3$, matching the roots. The zero at $-2$ means that L3’s zero-free overshoot formula does not apply directly.

### 3.2 Example 3.23 {#section-3-2}

Six blocks, a nested **positive** feedback loop through $G_3$, an outer loop through $G_4$, and a feedforward path through $G_6$ that takes off before $G_2$.

**Step 1: the inner loop (Fig. 3.12a → b).** The loop runs from the inner summing junction through $G_1$, then back through $G_3$, and enters the junction with a $+$ sign. Let $e$ be the signal arriving at the inner junction from the outer one. Then $a=G_1(e+G_3a)$, so $(1-G_1G_3)a=G_1e$. This is the positive-feedback form of Eq. (3.58):

$$
\frac{a}{e}=\frac{G_1}{1-G_1G_3}.
$$

**Step 2: move the pickoff (Fig. 3.12b → c).** $G_6$ takes its input from $a$, before $G_2$. After the move it takes its input from $b=G_2a$. To deliver the same signal $G_6a$, the block must become $G_6/G_2$, because $(G_6/G_2)\,b=(G_6/G_2)G_2a=G_6a$. The output is now two parallel blocks acting on $b$:

$$
\frac{Y}{b}=G_5+\frac{G_6}{G_2}.
$$

**Step 3: the outer loop, then the series connection.** The outer loop has forward path $\dfrac{G_1}{1-G_1G_3}\cdot G_2$ from the outer error to $b$, and feedback $G_4$ from $b$ with a $-$ sign. By Eq. (3.58),

$$
\frac{b}{R}=\frac{\dfrac{G_1G_2}{1-G_1G_3}}{1+\dfrac{G_1G_2}{1-G_1G_3}G_4} .
$$

Multiply the numerator and denominator by $1-G_1G_3$ to clear the nested fraction:

$$
\frac{b}{R}=\frac{G_1G_2}{(1-G_1G_3)+G_1G_2G_4} .
$$

The parallel pair from Step 2 is in series with this loop:

$$
T(s)=\frac{Y}{R}=\frac{b}{R}\cdot\frac{Y}{b}
=\frac{G_1G_2}{1-G_1G_3+G_1G_2G_4}\left(G_5+\frac{G_6}{G_2}\right) .
$$

Distribute $G_1G_2$ over the bracket. The $G_2$ cancels in the second term: $G_1G_2\cdot G_6/G_2=G_1G_6$. So

$$
\boxed{
T(s)=\frac{G_1G_2G_5+G_1G_6}{1-G_1G_3+G_1G_2G_4}
}
$$

**Reading the answer.** The numerator lists the two forward paths from $R$ to $Y$, which are $G_1G_2G_5$ and $G_1G_6$. The denominator is $1$ minus the positive loop gain $G_1G_3$, plus the negative loop gain $G_1G_2G_4$. Both loops pass through $G_1$, so they touch and no product of loop gains appears. This is Mason's rule in miniature; see §4.

### The same thing as equations

The same reduction follows from three node equations. Let $a$ be the output of $G_1$ and $b$ the output of $G_2$:

$$
a=G_1\left[(R-G_4b)+G_3a\right],
\qquad
b=G_2a,
\qquad
Y=G_5b+G_6a .
$$

The first equation is the outer junction ($R-G_4b$), then the inner junction ($+G_3a$), then $G_1$. Eliminate in three moves:

1. Substitute $b=G_2a$ into the first equation: $a=G_1R-G_1G_2G_4a+G_1G_3a$.
2. Collect the $a$ terms: $a(1-G_1G_3+G_1G_2G_4)=G_1R$, so $a=\dfrac{G_1R}{1-G_1G_3+G_1G_2G_4}$.
3. Substitute into the output equation: $Y=G_5G_2a+G_6a=(G_2G_5+G_6)a$, which gives
   $$
   \frac YR=\frac{G_1(G_2G_5+G_6)}{1-G_1G_3+G_1G_2G_4},
   $$
   which is the boxed result exactly.

**The three reduction steps are three eliminations.** Collecting the $G_3a$ term is the inner loop, writing $G_6a$ in terms of $b$ is the pickoff move, and collecting the $G_4b$ term is the outer loop.

**Worked check:** Choose nonzero numerical values for the six blocks and solve the three node equations. Compare $Y/R$ with the reduced formula, then reverse the inner-feedback sign and repeat. Agreement at sample points is a useful error check; the symbolic elimination establishes the identity.

---

## 4. Doing it by computer {#section-4}

Example 3.24 repeats Example 3.22 with three Matlab commands:

```matlab
s = tf('s');
sysG1 = 2;                       % the gain path
sysG2 = 4/s;                     % the integral path
sysG3 = parallel(sysG1,sysG2);
sysG4 = 1/s;
sysG5 = series(sysG3,sysG4);
sysG6 = 1;
sysCL = feedback(sysG5,sysG6,-1);
```

which returns $(2s+4)/(s^2+2s+4)$, as before.

**Mason’s rule** computes a transfer function directly from a signal-flow graph and can be useful for complicated interconnections. The textbook gives it in online Appendix W3.2.3.

For Example 3.23, the feedback-dependent factor is $1-G_1G_3+G_1G_2G_4$. Substitute the block transfer functions into the full expression for $T(s)$, combine the fractions, and check for cancellations before identifying its input-output poles. Dynamic blocks $G_5$ and $G_6$ can contribute additional poles even though they lie outside the loops. Internal modes can also be hidden by cancellations; the reduced $Y/R$ alone does not establish internal stability. The opposite signs of the two loop terms do not imply that increasing those gains moves every pole in opposite directions.

---

## 5. The natural response, and first-order poles {#section-5}

### 5.1 The impulse response is the natural response {#section-5-1}

For $H(s)=b(s)/a(s)$ with no common factors, the roots of $a$ are the poles and the roots of $b$ the zeros. Since the impulse response is the inverse transform of $H$ itself, the book gives it a name:

$$
\boxed{\text{the impulse response is the }\textbf{natural response}\text{ of the system}}
$$

The poles say which exponentials appear; the numerator says how much of each.

Here “natural response” follows the book's terminology and means the modes excited by an impulse. More generally, natural (or zero-input) response means motion due to initial conditions with the input set to zero. For a strictly proper system, the motion after the impulse is unforced, but its modal coefficients need not match an arbitrary initial-state response. Modes hidden from the input-output transfer function need not appear in the impulse response at all. A proper system with direct feedthrough also has an impulse at $t=0$.

### 5.2 One pole, one exponential {#section-5-2}

$$
H(s)=\frac1{s+\sigma}
\qquad\Longrightarrow\qquad
h(t)=e^{-\sigma t}1(t)
$$

with

$$
\boxed{\tau=\frac1\sigma}
\tag{3.59}
$$

the **time constant**, for $\sigma>0$: the time at which the response has fallen to $1/e$ of its initial value, since $h(\tau)=e^{-\sigma/\sigma}=e^{-1}$.

**The step response, derived.** With $U=1/s$, cover-up gives

$$
Y(s)=\frac{1}{s(s+\sigma)}=\frac{1/\sigma}{s}-\frac{1/\sigma}{s+\sigma}
\qquad\Longrightarrow\qquad
y(t)=\frac1\sigma\left(1-e^{-\sigma t}\right),\quad t\ge0 .
$$

The residues are $\left.\frac1{s+\sigma}\right|_{s=0}=\frac1\sigma$ and $\left.\frac1s\right|_{s=-\sigma}=-\frac1\sigma$. The final value is $1/\sigma$, so the percentages below are fractions of $1/\sigma$. Multiplying $H$ by $\sigma$ makes that final value unity: $\sigma/(s+\sigma)$ has DC gain 1.

**The tangent-line construction.** The unit-DC-gain step response $1-e^{-t/\tau}$ has initial slope $\frac{d}{dt}(1-e^{-t/\tau})\big|_{t=0}=1/\tau$. A line with that slope starting from 0 reaches the final value 1 at $t=\tau$. For the decaying impulse response $e^{-t/\tau}$, the tangent at the origin, $1-t/\tau$, reaches zero at the same time (textbook Fig. 3.14).

The percentages follow by evaluating $1-e^{-t/\tau}$. For example, $e^{-1}=0.368$, so $1-0.368=0.632$:

| $t/\tau$ | $1-e^{-t/\tau}$ |
|---:|---:|
| 1 | 63.2% |
| 2 | 86.5% |
| 3 | 95.0% |
| 4 | 98.2% |
| 5 | 99.3% |

The response reaches 63% of its final value at one time constant and is within 1% of it by five. “Settled” always needs a tolerance; the final value is approached asymptotically.

**Stability:** If $\sigma>0$ the pole is at $-\sigma$ in the left half plane and the response decays: stable. If $\sigma<0$ the pole is on the right and the response grows: unstable. L4 distinguishes free-response stability from bounded-input stability.

---

## 6. Reading a response off the poles {#section-6}

### 6.1 Example 3.25: two real poles {#section-6-1}

$$
H(s)=\frac{2s+1}{s^2+3s+2}
\tag{3.60}
$$

*Poles and zero.* The denominator factors as $s^2+3s+2=(s+1)(s+2)$, since $1\cdot2=2$ and $1+2=3$. This gives poles at $s=-1$ and $s=-2$. The numerator $2s+1=0$ gives one finite zero at $s=-\tfrac12$.

*Expand.* The numerator has degree 1 and the denominator has degree 2, so $H$ is strictly proper with distinct poles:

$$
H(s)=\frac{2s+1}{(s+1)(s+2)}=\frac{C_1}{s+1}+\frac{C_2}{s+2} .
$$

Cover up each factor:

$$
C_1=\left.\frac{2s+1}{s+2}\right|_{s=-1}=\frac{-2+1}{-1+2}=-1,
\qquad
C_2=\left.\frac{2s+1}{s+1}\right|_{s=-2}=\frac{-4+1}{-2+1}=3 .
$$

*Check:* $\dfrac{-1}{s+1}+\dfrac{3}{s+2}=\dfrac{-(s+2)+3(s+1)}{(s+1)(s+2)}=\dfrac{2s+1}{(s+1)(s+2)}$ ✓.

*Invert* with $1/(s+a)\leftrightarrow e^{-at}$:

$$
\boxed{
h(t)=-e^{-t}+3e^{-2t},\qquad t\ge0
\tag{3.61}
}
$$

The denominator supplies the rates $-1$ and $-2$, while the numerator sets the coefficients $-1$ and $3$. With the denominator fixed, moving the zero changes the coefficients without changing the rates. If the zero lands exactly on a pole, that term disappears from the input-output response through cancellation. A farther-left pole decays faster; a higher imaginary part instead means a higher oscillation frequency.

**Worked check:** The two modal contributions have equal magnitude when $3e^{-2t}=e^{-t}$. Dividing by $e^{-2t}$ gives $e^{t}=3$, so $t=\ln3\approx1.10$ s. At this time the contributions cancel and the impulse response crosses zero. This separates fast initial motion from the slow tail. Separately, $h(0^+)=-1+3=2$, as the initial-value theorem $h(0^+)=\lim_{s\to\infty}sH(s)=2$ requires. This equals the leading numerator coefficient here because the denominator is monic and its degree is exactly one greater than the numerator's.

### 6.2 Pole locations and modal shapes {#section-6-2}

![Decaying, sustained, and growing modal responses for different pole locations](images/ch3/pole-locations.png)

*Modal shapes:* the real part sets decay or growth; the imaginary part sets oscillation frequency. These curves illustrate simple free modes, not boundedness under every possible input.

For simple modes, pole locations give the following response shapes:

| Location | Natural response | Interpretation |
|---|---|---|
| Far left, real axis | Fast decay, no ringing | "small time constant" |
| Near the origin, negative real axis | Slow decay, no ringing | "large time constant" |
| Left half plane, complex pair | Decaying oscillation | "rings, then settles" |
| On the imaginary axis, simple pair | Constant-amplitude oscillation | "neutrally stable" |
| Right half plane, complex pair | Growing oscillation | "unstable" |
| Right, real axis | Pure growth | "runs away" |
| At the origin | Constant | "an integrator remembers" |

This table describes simple modes. Repeated poles add polynomial factors in time: a double pole at zero gives a ramp, and a repeated imaginary-axis pole can give growing oscillations. “Neutral” describes bounded free motion with all other modes decaying; it does not mean BIBO stable (L4).

**Worked check:** Compare poles at $-3$ and $-0.6$: their decay time constants are $1/3$ s and $5/3$ s. Then sketch poles at $\pm j$ and $+0.5\pm j$: equal oscillation frequency, different amplitude evolution. These are modal shapes, not claims about arbitrary-input boundedness.

---

## 7. Complex poles: the standard second-order form {#section-7}

A conjugate pair at $s=-\sigma\pm j\omega_d$ has denominator

$$
a(s)=(s+\sigma-j\omega_d)(s+\sigma+j\omega_d)=(s+\sigma)^2+\omega_d^2 .
\tag{3.62}
$$

The product is a difference of squares, $(x-jy)(x+jy)=x^2-(jy)^2=x^2+y^2$, with $x=s+\sigma$ and $y=\omega_d$.

The book's standard form, which recurs for the rest of the course:

$$
\boxed{
H(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_ns+\omega_n^2}
\tag{3.63}
}
$$

Expand Eq. (3.62) and match it to the denominator of Eq. (3.63) coefficient by coefficient:

$$
s^2+2\sigma s+(\sigma^2+\omega_d^2)\ \equiv\ s^2+2\zeta\omega_ns+\omega_n^2 .
$$

$$
s^1:\ 2\sigma=2\zeta\omega_n\ \Rightarrow\ \sigma=\zeta\omega_n;
\qquad
s^0:\ \sigma^2+\omega_d^2=\omega_n^2\ \Rightarrow\ \omega_d^2=\omega_n^2-\zeta^2\omega_n^2=\omega_n^2(1-\zeta^2).
$$

Therefore

$$
\boxed{
\sigma=\zeta\omega_n,
\qquad
\omega_d=\omega_n\sqrt{1-\zeta^2}
\tag{3.64}
}
$$

The real-frequency geometry and sinusoidal formulas below apply to $0\le\zeta<1$ with $\omega_n>0$. At $\zeta=1$ use the limiting critically damped formulas; for $\zeta>1$, the poles are real and unequal.

### 7.1 Pole geometry {#section-7-1}

$$
\boxed{
\begin{array}{ll}
\omega_n & \text{distance from the origin to the pole (a radius)}\\[3pt]
\sigma=\zeta\omega_n & \text{distance from the imaginary axis}\\[3pt]
\omega_d & \text{height above the real axis}\\[3pt]
\theta=\sin^{-1}\zeta & \text{angle measured from the imaginary axis}
\end{array}}
$$

**Why each entry holds.** The upper pole sits at horizontal distance $\sigma$ from the imaginary axis and height $\omega_d$ above the real axis. Draw the right triangle from the origin to that pole (textbook Fig. 3.18).

- *Radius:* by Pythagoras, the distance from the origin is $\sqrt{\sigma^2+\omega_d^2}=\sqrt{\omega_n^2}=\omega_n$, using the $s^0$ match above. The pole's magnitude is $\omega_n$.
- *Angle:* measured from the imaginary axis, the side opposite $\theta$ is the horizontal leg $\sigma$ and the hypotenuse is $\omega_n$. So $\sin\theta=\sigma/\omega_n=\zeta\omega_n/\omega_n=\zeta$.
- *Height:* similarly, $\cos\theta=\omega_d/\omega_n=\sqrt{1-\zeta^2}$, consistent with $\sin^2\theta+\cos^2\theta=1$.

#### Check your understanding

> Where do the poles go as $\zeta$ runs from 0 to 1, with $\omega_n$ held fixed?

Around a circle of radius $\omega_n$, from the imaginary axis to the negative real axis, where the two poles meet at $\zeta=1$. For the upper pole, $\sin\theta=\sigma/\omega_n=\zeta$. Conversely,

$$
\omega_n=\sqrt{\sigma^2+\omega_d^2},
\qquad
\zeta=\frac{\sigma}{\sqrt{\sigma^2+\omega_d^2}}.
$$

$$
\zeta=0 \ \Rightarrow\ \theta=0,\ \omega_d=\omega_n
\qquad\qquad
\zeta=1 \ \Rightarrow\ \theta=90^\circ,\ \omega_d=0
$$

Another common notation is the quality factor $Q=1/(2\zeta)$ for $\zeta>0$.

### 7.2 The response families {#section-7-2}

Rewriting Eq. (3.63) so the table can be used directly,

$$
H(s)=\frac{\omega_n^2}{(s+\zeta\omega_n)^2+\omega_n^2(1-\zeta^2)},
\tag{3.65}
$$

which is Eq. (3.62) with $\sigma=\zeta\omega_n$ and $\omega_d^2=\omega_n^2(1-\zeta^2)$ substituted. The table pair needed is

$$
\mathcal L\{e^{-\sigma t}\sin\omega_dt\,1(t)\}=\frac{\omega_d}{(s+\sigma)^2+\omega_d^2},
$$

which is the sine transform of L1 §5.2 with the frequency shift $s\to s+\sigma$ (property 4 in L1 §6). The numerator of $H$ is $\omega_n^2$, not $\omega_d$, so multiply and divide by $\omega_d$:

$$
H(s)=\frac{\omega_n^2}{\omega_d}\cdot\frac{\omega_d}{(s+\sigma)^2+\omega_d^2}
\qquad\Longrightarrow\qquad
h(t)=\frac{\omega_n^2}{\omega_d}e^{-\sigma t}\sin\omega_dt .
$$

Finally, $\omega_n^2/\omega_d=\omega_n^2/(\omega_n\sqrt{1-\zeta^2})=\omega_n/\sqrt{1-\zeta^2}$, so the impulse response is

$$
\boxed{
h(t)=\frac{\omega_n}{\sqrt{1-\zeta^2}}\,e^{-\sigma t}\sin(\omega_dt)\,1(t)
\tag{3.66}
}
$$

For the same zero-free standard pair, integrating $h(t)$ gives

$$
y_{\rm step}(t)=1-e^{-\sigma t}\left(\cos\omega_dt+\frac{\sigma}{\omega_d}\sin\omega_dt\right),\qquad t\ge0.
$$

**Derivation.** In $s$ this is $Y=H/s$. The residue at the origin is $H(0)=\omega_n^2/\omega_n^2=1$. Subtract it and simplify the remainder using $\sigma^2+\omega_d^2=\omega_n^2$:

$$
\frac{\omega_n^2}{s[(s+\sigma)^2+\omega_d^2]}-\frac1s
=\frac{\omega_n^2-(s^2+2\sigma s+\omega_n^2)}{s[(s+\sigma)^2+\omega_d^2]}
=-\frac{s+2\sigma}{(s+\sigma)^2+\omega_d^2} .
$$

Split $s+2\sigma=(s+\sigma)+\sigma$ to match the shifted cosine and shifted sine entries:

$$
Y(s)=\frac1s-\frac{s+\sigma}{(s+\sigma)^2+\omega_d^2}-\frac{\sigma}{\omega_d}\cdot\frac{\omega_d}{(s+\sigma)^2+\omega_d^2},
$$

which inverts term by term to the formula above. *Checks:* $y(0)=1-1=0$. Differentiating gives $\dot y=h$ from Eq. (3.66); the cosine and sine terms combine using $\sigma^2+\omega_d^2=\omega_n^2$.

For $0<\zeta<1$, the step response tends to 1. At $\zeta=0$, the same formula gives $y_{\rm step}(t)=1-\cos\omega_nt$, which oscillates indefinitely and has no final value despite $H(0)=1$.

At critical damping, $\zeta=1$, the denominator is $(s+\omega_n)^2$. Then $H=\omega_n^2/(s+\omega_n)^2$, and the repeated-pole pair $1/(s+a)^2\leftrightarrow te^{-at}$ gives $h(t)=\omega_n^2t e^{-\omega_nt}$. For the step, $\dfrac{\omega_n^2}{s(s+\omega_n)^2}=\dfrac1s-\dfrac1{s+\omega_n}-\dfrac{\omega_n}{(s+\omega_n)^2}$, so $y_{\rm step}(t)=1-(1+\omega_nt)e^{-\omega_nt}$. To check the expansion, recombine over a common denominator: $(s+\omega_n)^2-s(s+\omega_n)-\omega_ns=\omega_n^2$ ✓. The underdamped formulas with $\sqrt{1-\zeta^2}$ in a denominator must not be used directly at $\zeta=1$.

**Worked check:** For the zero-free standard pair, the overshoot formula in L3 gives 72.92% at $\zeta=0.1$, 16.30% at 0.5, and 4.60% at 0.7. The formula is $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$, from evaluating $y_{\rm step}$ at the first peak, $\omega_dt=\pi$. The exponents are $\pi(0.1)/0.99499=0.3157$, $\pi(0.5)/0.86603=1.8138$, and $\pi(0.7)/0.71414=3.0794$. Keep the numerator fixed when comparing this family.

### 7.3 Example 3.26 {#section-7-3}

$$
H(s)=\frac{2s+1}{s^2+2s+5}
\tag{3.67}
$$

Read the parameters off the denominator first:

$$
\omega_n^2=5 \Rightarrow \omega_n=\sqrt5=2.24\ \text{rad/s},
\qquad
2\zeta\omega_n=2 \Rightarrow \zeta=\frac{1}{\omega_n}=\frac1{\sqrt5}=0.447,
$$

$$
\sigma=\zeta\omega_n=1,
\qquad
\omega_d=\omega_n\sqrt{1-\zeta^2}=\sqrt5\sqrt{1-\tfrac15}=\sqrt4=2 .
$$

*Check with the quadratic formula:* $s=\dfrac{-2\pm\sqrt{4-20}}{2}=-1\pm2j$, so $\sigma=1$ and $\omega_d=2$ ✓. The zero is at $s=-\tfrac12$, as in Example 3.25.

*Predict before computing:* moderately damped, so expect a brief oscillatory transient near 2 rad/s with decay rate $e^{-t}$.

Now invert. The poles are complex, so rather than using complex residues, match table entries 19 and 20:

$$
e^{-\sigma t}\cos\omega_dt\ \leftrightarrow\ \frac{s+\sigma}{(s+\sigma)^2+\omega_d^2},
\qquad
e^{-\sigma t}\sin\omega_dt\ \leftrightarrow\ \frac{\omega_d}{(s+\sigma)^2+\omega_d^2} .
$$

*Step 1: complete the square.* $s^2+2s+5=(s^2+2s+1)+4=(s+1)^2+2^2$, so $\sigma=1$ and $\omega_d=2$.

*Step 2: rewrite the numerator in terms of $s+1$.* $2s+1=2(s+1)-1$. The cosine entry needs $s+1$ on top. The sine entry needs $\omega_d=2$ on top, so write $-1=-\tfrac12\cdot2$:

$$
H(s)=\frac{2(s+1)-1}{(s+1)^2+2^2}
=2\,\frac{s+1}{(s+1)^2+2^2}-\frac12\,\frac{2}{(s+1)^2+2^2} .
$$

*Step 3: invert term by term.*

$$
\boxed{
h(t)=\left(2e^{-t}\cos2t-\tfrac12e^{-t}\sin2t\right)1(t)
}
$$

*Checks.* $h(0)=2$, which equals $\lim_{s\to\infty}sH(s)=2$, as in Example 3.25. Combining the two sinusoids, $2\cos2t-\tfrac12\sin2t=\tfrac{\sqrt{17}}{2}\cos(2t+\phi)$ with $\phi=\tan^{-1}(1/4)\approx14.0^\circ$. This is the small phase shift visible in textbook Fig. 3.22, where the $2\cos2t$ term dominates.

Examples 3.25 and 3.26 have the same numerator, $2s+1$. Changing the denominator moved the poles and replaced two real decays with a decaying oscillation. The amplitude envelope here is $\sqrt{4+1/4}\,e^{-t}=\tfrac{\sqrt{17}}{2}e^{-t}\approx2.06e^{-t}$; $e^{-t}$ gives only its decay rate.

---

## 8. What this buys, and what is still missing {#section-8}

$$
\boxed{
\text{denominator} \rightarrow \text{which exponentials}
\qquad
\text{numerator} \rightarrow \text{how much of each}
}
$$

#### Check your understanding

> We can now look at a pole-zero map and describe the response in words: fast or slow, ringing or not, growing or decaying. What can we still not do?

Put numbers on it. *How much* overshoot? Settled by *when*? That is textbook §3.4, and it is the next lecture.

---

## 9. Looking ahead {#section-9}

Block reduction determines the transfer function. Pole locations describe its visible natural rates, while the numerator sets modal amplitudes. L3 attaches quantitative specifications to this geometry: rise time, overshoot, and settling time.

---

## Review questions

1. Example 3.22 has a forward path with a double pole at the origin and a closed loop with a well-damped pair. How does the feedback denominator $D+N$, for $G=N/D$, create new pole locations? Compare this with series and parallel connections of fixed blocks, whose poles come from the component poles, possibly with cancellations.
2. Moving a pickoff point introduced $G_6/G_2$. If $G_2$ has a RHP zero, why can the algebra remain valid while a separate physical realisation of $1/G_2$ is problematic?
3. The impulse response is called the natural response. In what sense is a system's response to being hit "natural" when a step response is not?
4. For $H_1(s)=2/[(s+1)(s+2)]$ and $H_2(s)=200/[(s+10)(s+20)]$, what is the same about their step responses and what differs? Why was specifying the numerators necessary?
5. A pole pair sits at $\omega_n=10$ rad/s with $\zeta=0.05$. Describe the impulse response in one sentence without computing anything.
6. The modal-shape table in §6.2 says nothing about zeros. What would you expect a zero to change, given Example 3.25?

## Optional practice

Optional practice from FPE, 8th edition; these are study suggestions, not an assignment.

| Problem | Topic |
|---|---|
| 3.18 | Transfer function from a block diagram with symbolic coefficients |
| 3.19, 3.20 | Transfer functions of several diagrams |
| 3.21 | $R$ to $Y$ through a multi-loop diagram |
| 3.22, 3.23 | The same diagrams by Mason's rule |
| 3.16 | DC gain and unit-step final value of a second-order system |
| 3.36 | Initial-condition response and logarithmic decrement |
| 3.41 | Sketch a step response from poles and zeros, then compare with Matlab (uses the zero effects from L3) |

## Chapter 3 student notes

- [L1: Convolution and transfer functions](convolution-impulse-response_student.md)
- [L2: Block diagrams and pole locations](block-diagrams_student.md)
- [L3: Specifications and zeros](time-domain-specs_student.md)
- [L4: Stability and Routh’s criterion](stability_student.md)
