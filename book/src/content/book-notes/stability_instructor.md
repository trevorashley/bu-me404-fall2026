# Dynamic Response IV — Stability, Routh's Criterion, and Closing the Chapter
## FPE 8th ed., Sections 3.6 through 3.9

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404)

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §§3.6–3.9 and the chapter Summary. Worked examples and figure numbers are the book's. Additions of my own are marked **[beyond the book]**.

**Prerequisites:** L1–L3 of this series. The physical reading of a right half-plane pole is in [From Physical Models to the Laplace Transform](modeling-and-dynamics_instructor.md), cited as *(0.0.8 §n)*.

**Earlier-lecture shorthand:** “0.0.8 §n” below refers to section n of the linked prerequisite, whose current filename is `modeling-and-dynamics_instructor.md`.

**Duration:** 75 minutes, including the chapter wrap-up.

**Book figures:** figure numbers refer to the source chapter at

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./3 - Dynamic Response.pdf
```

Page cues below use the PDF viewer's 1-based page numbers (202 pages). Project the figures directly from this PDF; extracted image files are not supplied. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index lists the scripts.

**Notation:**

| Symbol | Meaning |
|---|---|
| $a(s)$ | characteristic polynomial, $s^n+a_1s^{n-1}+\cdots+a_n$ |
| $p_i$ | roots of the full characteristic polynomial (internal modes), before transfer-function cancellation |
| $h(t)$ | impulse response |
| BIBO | bounded input, bounded output |
| $K,\ K_I$ | proportional and integral controller gains |

---

# Part 0 — Planning

## 1. Teaching strategy

Three lectures have described responses on the assumption that they settle. This one asks when they do.

The section is short on new mathematics and heavy on distinctions, and the distinctions are what students get wrong. The book uses "stable" for three different things:

| Kind | Question | Test |
|---|---|---|
| **BIBO** | From zero initial state, does every bounded input give a bounded output? | For a causal proper rational transfer function, every pole of the reduced transfer function lies strictly in the LHP |
| **Internal** | Do the natural modes of the *system* decay? | every root of $a(s)$ in the LHP, **before** cancellation |
| **Neutral** | Is every free motion bounded, with some nondecaying modes? | Imaginary-axis modes are simple in the scalar ODE setting; every other mode is strictly in the LHP |

Then Routh's criterion arrives as a labour-saving device with one genuinely modern use: **it answers the question with a parameter left as a symbol.** A numerical root finder cannot do that, and that is the argument for teaching a 150-year-old test in a world with `roots()`.

The framing line:

> **Every design method in the rest of this course moves poles. Today we find out which side of the line they have to stay on, and how to check it without solving for them.**

Three moments to protect:

1. **§5.2** — the capacitor. A bounded input, an unbounded output, and a pole that is not in the right half plane.
2. **§6.3** — the cancelled unstable pole. A perfectly stable transfer function sitting on top of a system that explodes.
3. **§8** — Example 3.33: Routh with $K$ as a symbol, giving $K>7.5$ in three lines.

---

## 2. Learning objectives

By the end of this lecture students should be able to:

1. State the stability condition for an LTI system in terms of the roots of its characteristic polynomial.
2. Define BIBO stability, prove the sufficiency of $\int|h|<\infty$, and explain the sign-matching input argument for necessity.
3. Show that a capacitor driven by a current source is not BIBO stable, and connect that to its pole at the origin.
4. Distinguish asymptotic stability, neutral stability and instability, including the case of repeated imaginary-axis poles.
5. Explain why a pole-zero cancellation can hide an unstable mode, and where that mode reappears.
6. Apply the necessary condition on the coefficients of $a(s)$, and say why it is not sufficient.
7. Build a Routh array and count right half-plane roots from the sign changes in its first column.
8. Use Routh's criterion to find the range of a single gain that stabilises a loop (Example 3.33).
9. Use it with two parameters to find a stable region in a parameter plane (Example 3.34).
10. Say what system identification and amplitude/time scaling are for, and where the book puts them.

---

## 3. Suggested lecture flow (75 minutes)

| Time | Topic | Section |
|---:|---|---|
| 0–4 min | Recap of L1–L3; the question left open | §4 |
| 4–8 min | The LTI stability statement; back to Fig. 3.16 | §5.1 |
| 8–18 min | BIBO stability; the capacitor; resonant forcing | §5.2–§5.3 |
| 18–28 min | Internal stability; repeated $j\omega$ poles; the cancellation trap | §6 |
| 28–34 min | The necessary condition, and why it is not enough | §7.1 |
| 34–44 min | The Routh array; Example 3.32 | §7.2–§7.3 |
| 44–54 min | Example 3.33: a range of gain | §8 |
| 54–62 min | Example 3.34: a region in two parameters | §9 |
| 62–68 min | Special cases, Kharitonov; §3.7 and §3.8 in brief | §10 |
| 68–75 min | Historical perspective; chapter summary; what Chapter 4 does with it | §11–§13 |

**Prepare as slides:** Fig. 3.39 (the capacitor), Fig. 3.40 and 3.41 (Example 3.33), Fig. 3.43 and 3.44 (Example 3.34), and the chapter summary. The Routh array construction belongs on the board, written out slowly once.

**If you are short of time,** compress §9 to the boxed inequalities and the region picture, and fold §10 into a single "where to read more" slide. Do not compress §6.3.

### Runnable demonstrations

```
cd demos
uv run python ch3/l4_demo1_routh.py --show
uv run python ch3/l4_demo4_bibo_internal.py --show
```

**Run Demo 1 and Demo 4 live.** Demo 1 builds the array for Example 3.32 and checks the RHP count against a root finder. Demo 4 is the cancellation trap, and it is the one students remember. Demos 2 and 3 work as slides.


### Teaching scope

Use the demos for the selected live examples; the accompanying checks also work on the board. For a 75-minute session, select the protected examples in §1; assign the remaining worked examples and optional computations as follow-up reading. Do not try to present every figure and derivation live.

---

# Part I — The lecture

## 4. Opening

### Instructor script

> Three lectures of machinery, and all of it assumed something we never checked.
>
> We computed final values with a theorem whose hypothesis was that all the poles of $sY(s)$ are in the left half plane. We converted specifications into a region and put poles inside it. We approximated higher-order systems by a dominant pair and ignored what we dropped.
>
> Every one of those steps assumed the transients decay.
>
> Today: when do they? And here is why it matters more in this course than in a differential-equations course. In Chapter 4 we start closing loops, and closing a loop *moves the poles* — you saw it happen in Example 3.22. A perfectly well-behaved plant, wrapped in a loop with too much gain, oscillates or runs away. So we need not just a test, but a test we can run with the gain left as an unknown.

---

## 5. Stability, and the first version of the test (§3.6)

### 5.1 The statement

$$
\boxed{
\begin{array}{c}
\text{A finite-dimensional LTI realisation is asymptotically stable}\\
\text{if and only if all roots of its full characteristic polynomial}\\
\text{have strictly negative real parts.}
\end{array}}
$$

> **[ FIG 3.16 ]** — PDF p. 88 *(recall from L2)*
>
> **Say:** "We drew this two lectures ago and read it as shapes of motion. Read it again as a verdict: everything on the left decays, everything on the right grows, and the imaginary axis is the boundary where the argument needs more care."

Three cases:

| Poles | Free response | Name |
|---|---|---|
| All strictly in the LHP | decays to zero | asymptotically stable |
| Any in the RHP | grows | unstable |
| Simple $j\omega$ modes, all remaining modes strictly in the LHP | bounded, with persistent constants or oscillations | neutrally stable |

Failure of asymptotic stability does not necessarily mean growing free motion. Neutral systems have bounded free responses but need not have bounded forced responses. In the RHP case, some initial conditions may fail to excite the growing mode; instability means that not every small initial perturbation remains bounded.

### 5.2 BIBO stability (§3.6.1)

A different question, asked from zero initial state: *does every bounded input produce a bounded output?* First assume a causal, strictly proper rational system so that its impulse response is an ordinary function.

Start from convolution. If $|u|\le M$ then

$$
|y(t)|=\left|\int h(\tau)u(t-\tau)\,d\tau\right|
\le M\int_{-\infty}^{\infty}|h(\tau)|\,d\tau ,
$$

so the output is bounded whenever $\int|h|$ is. For necessity, fix a finite observation time $T$ and choose one bounded causal test input

$$
u_T(t)=
\begin{cases}
\operatorname{sgn}h(T-t),&0\le t\le T\\
0,&\text{otherwise}.
\end{cases}
$$

Then at that observation time

$$
y_T(T)=\int_0^T|h(\tau)|\,d\tau.
$$

If the absolute integral diverges, these outputs can be made arbitrarily large with inputs bounded by 1: no uniform bounded-input gain exists. This is the finite-horizon version of the book's sign-matching argument in Eq. (3.84). Do not let the input definition depend on a changing observation time while claiming it is one fixed waveform. The resulting criterion is

$$
\boxed{
\text{BIBO stable}
\iff
\int_{-\infty}^{\infty}|h(\tau)|\,d\tau<\infty
\tag{3.85}
}
$$

#### Say out loud

> Matching the input to the sign of the reversed impulse response maximises the output at a chosen time. The next two examples give fixed bounded waveforms that produce unbounded responses.

For a proper model with direct feedthrough, $h(t)=D\delta(t)+h_r(t)$; use finite $D$ and $\int_0^\infty|h_r|<\infty$, rather than treating $|\delta|$ as an ordinary function. For causal proper rational systems the criterion is equivalent to all **uncancelled transfer-function poles** lying strictly in the LHP.

### 5.3 Example 3.31: the capacitor

> **[ FIG 3.39 ]** — PDF p. 142 *(slide: capacitor driven by a current source)*

Current in, voltage out. Since $C\dot v=i$, the transfer function is $1/(Cs)$ and $h(t)=1(t)/C$. The book uses the normalised case $C=1$, giving

$$
\int_{-\infty}^{\infty}|h(\tau)|\,d\tau=\int_0^\infty d\tau=\infty .
$$

Not BIBO stable. Physically obvious: hold a constant current into a capacitor and the voltage climbs forever. The transfer function is $1/s$ — one pole, on the imaginary axis, at the origin.

$$
\boxed{
\text{BIBO stability requires }\textbf{every}\text{ pole strictly inside the LHP}
}
$$

> **[ DEMO 4 ]** — `ch3/l4_demo4_bibo_internal.py` *(live, ~10 s; the first two panels here, the third in §6.3)*
>
> **Teaching check [beyond the book]:** For a 1 F capacitor at rest, a 1 A constant current gives $v(t)=t$ volts. For $H(s)=1/(s^2+1)$ and $u(t)=\sin t\,1(t)$, verify $y(t)=(\sin t-t\cos t)/2$. Both bounded inputs produce unbounded outputs, despite the absence of RHP poles.

---

## 6. Internal stability (§3.6.2)

### 6.1 The characteristic equation, before any cancellation

$$
a(s)=s^n+a_1s^{n-1}+\cdots+a_n=0
\tag{3.86}
$$

For distinct roots the free response is

$$
y(t)=\sum_{i=1}^{n}K_ie^{p_it}
\tag{3.88}
$$

and it decays for every set of initial conditions if and only if

$$
\boxed{
\Re\{p_i\}<0\quad\text{for all }i
\tag{3.89}
}
$$

This is **internal asymptotic stability**, provided $a(s)$ represents the full physical realisation or interconnection. In state-space language it is $\det(sI-A)$. An arbitrarily unreduced fraction is not enough: multiplying a transfer function by $(s-1)/(s-1)$ does not establish that a physical unstable state exists. The book's “before cancellation” warning means retain actual internal dynamics when deriving the characteristic equation.

### 6.2 The imaginary axis, carefully

| Poles on the axis | Free response |
|---|---|
| One simple pole at the origin | a constant that never decays |
| A simple conjugate pair at $\pm j\omega_1$ | constant-amplitude oscillation |
| **Repeated** poles on the axis | $te^{\pm j\omega_1t}$ terms: **unbounded** |

A double integrator is the example to give: two poles at the origin, and a free response containing a ramp. Students met it as the drifting satellite in L1 §13, and as the free mass of *(0.0.8 §10)*.

$$
\boxed{
\text{simple on the axis} \Rightarrow \text{neutrally stable}
\qquad
\text{repeated on the axis} \Rightarrow \text{unstable}
}
$$

**Scope [beyond the book]:** the repeated-pole statement above applies to the scalar ODE/transfer-pole setting. For a general state-space realisation, repeated imaginary-axis eigenvalues can still give bounded free motion if they are semisimple (no nontrivial Jordan blocks). For example, $A=0_{2\times2}$ gives two constant states; a double integrator has a Jordan block and gives a ramp. Neutrality also requires no RHP modes.

### 6.3 The cancellation trap [beyond the book: worked example]

The book's sentence is easy to read past:

> *If a zero were to cancel a pole in the RHP for the transfer function, the corresponding $K_i$ would equal zero in the output, but the unstable transient would appear in some internal variable.*

Make it concrete on the board. Plant and controller:

$$
G(s)=\frac{1}{s-1}
\qquad\qquad
C(s)=\frac{s-1}{s+3}
$$

The controller's zero cancels the plant's unstable pole. Loop gain $CG=1/(s+3)$; with unity feedback,

$$
T(s)=\frac{CG}{1+CG}=\frac{1}{s+4} .
$$

A stable first-order input-output transfer function. It does not certify the internal stability of the interconnection.

Realise the loop with states and look at the eigenvalues. With $x_p$ the plant state ($y=x_p$) and $x_c$ the controller state, using $C(s)=1-\dfrac{4}{s+3}$:

$$
\dot x_p=r-4x_c,
\qquad
\dot x_c=-3x_c+r-x_p,
\qquad
A=\begin{bmatrix}0&-4\\-1&-3\end{bmatrix}
$$

$$
\boxed{
\text{eigenvalues of }A: \quad -4 \quad\text{and}\quad +1
}
$$

The mode at $+1$ is not in $T(s)$. It is in the system.

> **[ DEMO 4, continued ]** — right-hand panel *(this is the moment of the lecture)*
>
> **Teaching check [beyond the book]:** With a unit reference step and zero initial state, $y(t)=(1-e^{-4t})/4$. With $x_p(0)=\epsilon$, $x_c(0)=0$, add $\epsilon(4e^t+e^{-4t})/5$. For $\epsilon=10^{-6}$ this gives about 0.268 at 10 s and 388.38 at 20 s. The growing mode is observable at $y$ but cannot be excited by $r$ from rest.

**[beyond the book]** Chapter 7 gives this its proper names — the cancelled mode is uncontrollable from $r$ while remaining observable at $y$ — and the earlier lecture's discussion of hidden internal motion *(0.0.8 §14, §34)* is the same phenomenon approached from the zero-dynamics side.

---

## 7. Routh's criterion (§3.6.3)

### 7.1 The free half of the test

$$
\boxed{
\text{A necessary condition for stability: every coefficient of }a(s)\text{ is present and positive.}
}
$$

The reason is one line: a stable polynomial factors into terms $(s+\sigma)$ and $(s^2+2\zeta\omega_ns+\omega_n^2)$ with all coefficients positive, and a product of polynomials with positive coefficients has positive coefficients.

**A missing or negative coefficient rules out all roots being strictly in the LHP**, for this monic real polynomial. A missing coefficient alone does not prove a RHP root: $s^2+1$ has only imaginary-axis roots. Check whether the result is neutral or growing before calling its free response unstable.

It is *not* sufficient. Example 3.32 is the counterexample, and it is next.

### 7.2 The array

For $a(s)=s^n+a_1s^{n-1}+\cdots+a_n$, write two rows by taking alternate coefficients:

```text
   s^n  |   1     a2     a4    ...
 s^(n-1)|   a1    a3     a5    ...
 s^(n-2)|   b1    b2     b3    ...
 s^(n-3)|   c1    c2     c3    ...
   ...
   s^0  |   *
```

with

$$
b_1=\frac{a_1a_2-a_3}{a_1},
\qquad
b_2=\frac{a_1a_4-a_5}{a_1},
\qquad
c_1=\frac{b_1a_3-a_1b_2}{b_1},
\qquad\dots
$$

Each entry is a $2\times2$ determinant of the two rows above, divided by the first element of the row immediately above, with a sign flip. Then:

$$
\boxed{
\begin{array}{c}
\text{All roots are strictly in the LHP iff the ordinary array has a positive first column.}\\[4pt]
\text{The number of RHP roots equals the number of \textbf{sign changes} in that column.}
\end{array}}
$$

A pattern $+,-,+$ counts as **two** sign changes.

These statements assume the ordinary array is defined, with no zero pivots or zero rows. Handle those cases as in §10 before counting signs; an auxiliary-polynomial replacement alone must not be used to certify strict stability of the original polynomial.

**Practical note from the book:** any row may be multiplied or divided by a positive constant to keep the arithmetic clean.

### 7.3 Example 3.32

$$
a(s)=s^6+4s^5+3s^4+2s^3+s^2+4s+4
$$

Every coefficient is present and positive, so the free test tells us nothing. Build the array — Demo 1 prints it:

| row | | | | |
|---|---:|---:|---:|---:|
| $s^6$ | 1 | 3 | 1 | 4 |
| $s^5$ | 4 | 2 | 4 | 0 |
| $s^4$ | 2.5 | 0 | 4 | |
| $s^3$ | 2 | $-2.4$ | 0 | |
| $s^2$ | 3 | 4 | | |
| $s^1$ | $-5.0667$ | 0 | | |
| $s^0$ | 4 | | | |

First column: $1,\ 4,\ 2.5,\ 2,\ 3,\ -5.0667,\ 4$. **Two sign changes**, so two roots in the right half plane.

> **[ DEMO 1 ]** — `ch3/l4_demo1_routh.py` *(live, ~10 s)*
>
> **Teaching check [beyond the book]:** Numerical roots of Example 3.32 are approximately $-3.2644,-0.8858,-0.6046\pm0.9935j,+0.6797\pm0.7488j$. Their sum is $-4$, and there are two RHP roots. **Source correction [beyond the book]:** the footnote on PDF p. 150 prints $+0.7797$ instead of $+0.6797$.

#### Ask the class

> Routh gives a count, not locations. When is a count enough?

Whenever the question is a yes-or-no about stability, or a *boundary* in a parameter. That is the next two examples.

---

## 8. Example 3.33: the range of stabilising gain

> **[ FIG 3.40 ]** — PDF p. 151 *(slide)*

**Source correction [beyond the book]:** Fig. 3.40 prints the plant denominator as $s(s+1)(s+6)$; the worked solution uses $s(s-1)(s+6)$. Use the latter to obtain the characteristic equation and gain range below.

Proportional gain $K$ around the plant $\dfrac{s+1}{s(s-1)(s+6)}$. Note the plant is already unstable, with a pole at $+1$.

The characteristic equation is

$$
1+K\frac{s+1}{s(s-1)(s+6)}=0
\qquad\Longrightarrow\qquad
\boxed{s^3+5s^2+(K-6)s+K=0}
$$

The array:

$$
\begin{array}{c|cc}
s^3 & 1 & K-6\\
s^2 & 5 & K\\
s^1 & \dfrac{4K-30}{5} & \\
s^0 & K &
\end{array}
$$

Both $K$-dependent entries must be positive:

$$
\frac{4K-30}{5}>0
\quad\text{and}\quad
K>0
\qquad\Longrightarrow\qquad
\boxed{K>7.5}
$$

### Instructor script

> Look at what we just did. We asked a question about an infinite family of systems — one for every value of $K$ — and answered it in four lines with $K$ left as a letter.
>
> `roots()` cannot do that. It answers for one $K$ at a time. If you want the boundary, you either derive it symbolically or you go hunting numerically and hope you did not step over a narrow region.
>
> That is the reason a test from 1874 is still in the book.

> **[ DEMO 2 ]** — `ch3/l4_demo2_gain_range.py` *(slide)*
>
> **Teaching check [beyond the book]:** At $K=7.5$, factor the polynomial as $(s+5)(s^2+1.5)$: the imaginary poles are $\pm j\sqrt{1.5}$, so the free response is neutral and the system is not BIBO stable. At $K=13$ the roots are approximately $-4.065,-0.468\pm1.726j$; at $K=25$, $-1.908,-1.546\pm3.273j$. The pair's damping ratio increases from about 0.261 to 0.427. Still, the zero and third pole mean that damping ratio alone does not determine overshoot; compare the full responses in Fig. 3.41.

> **[ FIG 3.41 ]** — PDF p. 154

---

## 9. Example 3.34: two parameters, and a region

> **[ FIG 3.42 ]** — PDF p. 155; the PI feedback system is $C(s)=K+K_I/s$ around $\dfrac{1}{(s+1)(s+2)}$

$$
1+\left(K+\frac{K_I}{s}\right)\frac{1}{(s+1)(s+2)}=0
\qquad\Longrightarrow\qquad
\boxed{s^3+3s^2+(2+K)s+K_I=0}
$$

Array:

$$
\begin{array}{c|cc}
s^3 & 1 & 2+K\\
s^2 & 3 & K_I\\
s^1 & \dfrac{6+3K-K_I}{3} & \\
s^0 & K_I &
\end{array}
$$

**Source correction [beyond the book]:** the Routh array on PDF p. 156 labels its third row $s^2$; the correct label is $s^1$, as shown here.

$$
\boxed{
K_I>0
\qquad\text{and}\qquad
K>\frac{K_I}{3}-2
}
$$

> **[ FIG 3.43 ]** — PDF p. 158 *(slide: the allowable region)*

> **[ DEMO 3 ]** — `ch3/l4_demo3_pi_region.py` *(slide)*
>
> **Teaching check [beyond the book]:** At $K=K_I=1$, $T(s)=(s+1)/(s+1)^3=1/(s+1)^2$, with unit final value. At $K=10,K_I=5$, the roots are approximately $-0.462,-1.269\pm3.036j$, and the zero is at $-0.5$. **Source correction [beyond the book]:** PDF p. 159 prints an imaginary part near 3.3; substitution or numerical roots gives 3.036. Treat $K_I=0$ separately, as explained below.

**Boundary case $K_I=0$ [beyond the book].** The cubic becomes $s[s^2+3s+(2+K)]$. If the PI integrator state is retained, it has a neutral mode and the full realisation is not asymptotically stable. If the integral term is removed and the controller is implemented as a pure gain, the physical closed loop is second order and is stable for $K>-2$. At $K=1$, $T=1/(s^2+3s+3)$ has final value $1/3$. The zero at the origin cancels in that input-output transfer; it is not an uncancelled transfer pole. Distinguish controller implementation from an algebraic factor introduced by multiplying through by $s$.

#### Ask the class

> Could you have found that straight line by computing roots?

You could confirm points on it. You could not *derive* it. This is the book's own argument for why Routh is "superior to the numerical approaches" here, and it is the honest version of that claim.

---

## 10. Loose ends (§3.6.3 special cases, §3.7, §3.8)

Keep this section brisk; it is signposting.

**Special cases [procedures beyond the chapter's printed treatment].** Appendix W3.6.3 gives the full treatment. Two rules are useful now:

- If the first element is zero but the row is not all zero, replace that element by $\epsilon>0$, continue, and count signs as $\epsilon\to0^+$.
- If an entire row is zero, form an auxiliary polynomial from the row immediately above, replace the zero row by its derivative's coefficients, and continue. Also examine the auxiliary roots: symmetry about the origin can mean imaginary-axis pairs **or** real pairs $\pm a$, so a zero row does not by itself imply neutrality.

At the $K=7.5$ boundary of Example 3.33, the $s^1$ row vanishes. The row above gives $A(s)=5s^2+7.5$, with roots $\pm j\sqrt{1.5}$. Its derivative is $10s$. The remaining root is $-5$, confirming bounded free oscillation but neither asymptotic nor BIBO stability.

**Kharitonov's theorem (1978).** For a real fixed-degree polynomial family whose coefficients vary independently within specified intervals (with a leading coefficient bounded away from zero), robust strict stability can be checked using four particular endpoint polynomials. This is a pointer to robust control, not a recipe for arbitrary correlated or changing-order uncertainty.

**§3.7 System identification.** Building a model from measured data rather than from first principles. The frequency-response measurement of L1 §7 is the simplest version: drive with sinusoids, record amplitude ratio and phase, and you have $H(j\omega)$ without ever writing an equation of motion. Details in Appendix W3.7.

**§3.8 Amplitude and time scaling.** When model quantities span many orders of magnitude, rescale both signal amplitudes and time, then translate results back to physical units. For example, $\hat y=y/y_{\rm ref}$ is amplitude scaling and $\hat t=t/t_{\rm ref}$ is time scaling. The one-sided transform rule is $\mathcal L\{f(at)\}=F(s/a)/a$ for $a>0$. The printed chapter points to Appendix W3.8 for the details; time scaling alone is not the whole topic.

---

## 11. Historical perspective (§3.9)

Five minutes, and worth it — students remember the chapter better when the names have people attached.

**Oliver Heaviside (1850–1925).** Self-taught, left school at sixteen, worked as a telegraph operator, and did his research outside a scientific community that was hostile to him. He reformulated Maxwell's equations into the four we use today, predicted the ionosphere, and invented an operational calculus for solving differential equations that was wildly popular with electrical engineers in the 1920s and 1930s — and which turned out to be equivalent to the Laplace transform.

**Pierre-Simon Laplace (1749–1827).** Astronomer and mathematician, sometimes called the Newton of France, author of the five-volume *Mécanique céleste* on the stability of the solar system. Asked by Napoleon why God did not appear in it, he is said to have replied, "Sir, there was no need for that hypothesis." He was also Napoleon's Interior Minister, briefly, and an opportunist who changed sides as the politics shifted.

**Joseph Fourier (1768–1830).** Laplace's student, went to Egypt with Napoleon as a science adviser, and is credited with identifying the greenhouse effect. Fourier series and transforms represent signals in terms of exponentials; Laplace transforms extend that to transients and to closed-loop behaviour.

**And the book that made it standard practice:** Gardner and Barnes, 1942, which popularised the Laplace transform among American engineers.

#### Say out loud

> There is a moral in the Heaviside story for this course. He had a working method that got right answers and could not prove it was legitimate; the mathematicians who could prove it arrived decades later. Every technique in this chapter has that shape — a physical intuition first, a rigorous justification afterwards. Do not wait for the second one before using the first.

---

## 12. Chapter summary

The book's summary, with the qualifications developed in these lectures. Here $Y=GU$ assumes zero initial state; the time specifications assume the unit-gain zero-free standard pair with $0<\zeta<1$, and $t_s$ uses a 1% band:

$$
\boxed{
\mathcal L\{f\}=\int_{0^-}^{\infty}f(t)e^{-st}\,dt
\qquad
\mathcal L\{\dot f\}=sF(s)-f(0^-)
\qquad
Y(s)=G(s)U(s)
}
$$

$$
\boxed{
\text{final value } \lim_{t\to\infty}y=\lim_{s\to0}sY(s)
\ \ \text{(all poles of }sY\text{ in the LHP)}
\qquad
\text{feedback } \frac{G_1}{1+G_1G_2}
}
$$

$$
\boxed{
t_r\simeq\frac{1.8}{\omega_n}
\qquad
M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}
\qquad
t_s\simeq\frac{4.6}{\zeta\omega_n}
}
$$

$$
\boxed{
\begin{array}{l}
\text{Single real LHP zero in the standard family} \rightarrow \text{more overshoot}\\
\text{Single real RHP zero in that family} \rightarrow \text{initial inverse response}\\
\text{Extra real LHP pole in that family} \rightarrow \text{slower rise}\\
\text{Internal asymptotic stability} \rightarrow \text{all internal modes strictly in the LHP}
\end{array}}
$$

> **[ SUMMARY FIG ]** — PDF p. 168

### The book's review questions (§ Review Questions 3.1–3.12)

Use three or four as a closing quiz, with hands up rather than written answers:

- What is a transfer function, and what must be true of a system for one to exist?
- State the Final Value Theorem. What is its most common use in control?
- Given $\zeta$ and $\omega_n$, estimate the rise time, the overshoot and the settling time.
- What is the most noticeable effect of a right half-plane zero on a step response?
- What is the main use of Routh's criterion?

---

## 13. Closing script

> Four lectures ago we had a differential equation and a table of transforms. Here is what the chapter actually did.
>
> It said that the zero-state input-output behaviour of a linear time-invariant system is described by its impulse response, and that convolution can be replaced by multiplication in $s$. That gave us the transfer function.
>
> Its poles tell us the visible natural rates: fast or slow, oscillatory or not, growing or decaying. Modal amplitudes and hidden internal states require additional information.
>
> It gave us three numbers connecting that geometry to what a customer asks for, and then told us honestly how far to trust them.
>
> It showed how zeros reweight modes, and how a single real RHP zero in our examples causes an initial inverse response. The response later reverses direction; the design limitation remains.
>
> And today it drew the line: all poles strictly in the left half plane, checked without solving for them, with the design parameter left as a symbol.
>
> Chapter 4 starts moving poles on purpose. Everything from here — root locus, frequency response, state feedback — is a different way of answering the same question: where do I want them, and what do I have to build to put them there?

---

# Part II — Materials

## 14. One-board summary

```text
   THREE KINDS OF STABLE

     BIBO        zero state: every bounded input -> bounded output
                 <=>  INTEGRAL |h| dt < infinity (strictly proper case)
                 <=>  every reduced transfer pole STRICTLY in the LHP

     internal    every root of the PHYSICAL characteristic polynomial in the LHP
                 (this is the one that matters when you close a loop)

     neutral     simple axis modes, all other modes in the LHP: bounded free motion
                 repeated scalar axis poles give t*e^{jwt}: growing free motion
                 general state models: check Jordan blocks (see section 6.2)

   THE CANCELLATION TRAP

     G = 1/(s-1),  C = (s-1)/(s+3)   ->   T = 1/(s+4)      looks perfect
     eigenvalues of the interconnection: -4 and +1          is not
     10^-6 of initial state -> 388 by twenty seconds

   ROUTH

     free test   : missing or negative coefficient -> NOT strictly LHP
                   a missing coefficient need not mean a RHP root
                   all positive -> NECESSARY only, keep going

     array       : two rows of alternating coefficients, then 2x2 determinants

     verdict     : ordinary array, first column positive <=> strictly LHP
                   number of sign changes     =   number of RHP roots
                   zero pivots/rows require special treatment

     the point   : it works with a parameter left as a SYMBOL
                   K > 7.5      (one gain)
                   K_I > 0 and K > K_I/3 - 2      (a region)
```

## 15. Discussion questions

1. The capacitor is not BIBO stable, yet capacitors are in every circuit you own. In what sense is the analysis useful and in what sense is it beside the point?
2. Give a system that is neutrally stable but harmless, and one that is neutrally stable and dangerous. What distinguishes them?
3. The cancelled unstable mode in §6.3 never appears in $T(s)$. Name three physical events that would excite it in a real machine.
4. Routh's test gives a count of RHP roots, not their locations. Design a situation where the count alone is exactly what you need, and one where it is useless.
5. Example 3.33 required $K>7.5$ to stabilise an already-unstable plant. Is there an upper limit on $K$ here, and is that typical?
6. In Example 3.34, increasing $K_I$ at fixed $K$ eventually loses stability. How does the added integrator alter the dynamics? Why is this not a claim that integral action is always destabilising?
7. Kharitonov's theorem reduces an independent interval-coefficient family to four endpoint polynomials. Which uncertainty assumptions must hold before applying it to measured coefficients?

## 16. Homework and follow-up problems

| Problem | Topic | Why this one |
|---|---|---|
| 3.51 | Time to double for unstable modes | Connects pole location to growth rate. |
| 3.52 | Unity-feedback stability via Routh | Derive the closed-loop polynomial first. |
| 3.53 | Count RHP roots of given polynomials | Core Routh-array practice, including special cases. |
| 3.54, 3.55 | Ranges of a parameter for stability | Symbolic inequalities, followed by numerical checks. |
| 3.56 | Magnetic levitation with feedback | Connects a physical model to stability constraints. |
| 3.58 | Require all poles to lie left of a specified negative real part | Optional extension using a shifted variable. |
| 3.59 | Constraints on two gains and an allowable region | Direct follow-up to Example 3.34. |
| Review Questions 3.10–3.12 | Stability, Routh, system identification | Short written answers; good exam preparation. |

**Suggested additional exercise [beyond the book]:** modify `l4_demo1_routh.py` to accept a polynomial with a zero in the first column, observe the exception it raises, and read Appendix W3.6.3 to find out what the fix is.

## 17. Instructor cautions

1. **Three meanings of "stable" in one section.** Write the three-row table (§1) on the board at the start and refer back to it. Students who merge BIBO with internal stability cannot understand §6.3.
2. **The necessary condition is not sufficient — prove it with Example 3.32.** Some students will otherwise stop at "all coefficients positive" for the rest of their careers.
3. **Sign changes are counted, not just the presence of negatives.** A first column reading $+,-,+$ means two RHP roots, not one. Demo 1's third case makes this concrete.
4. **The book's Example 3.32 footnote has a typo** ($+0.7797$ should be $+0.6797$); the sum-of-roots argument catches it in one line. Use it as a lesson in checking, not as a complaint.
5. **Repeated scalar $j\omega$ poles produce growing free motion.** Use the double integrator, and distinguish it from two independent constant states as in §6.2.
6. **Never cancel an unstable pole.** Say it as a rule, then earn it with Demo 4. A cancellation inside the *stable* region is a legitimate technique with its own caveats (Example 3.29); in the RHP it is never acceptable.
7. **Routh's real value today is symbolic.** If you present it as a way to avoid computing roots, a student with `numpy` will reasonably conclude it is obsolete. Present it as the way to get a *boundary in a parameter*.

## 18. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l4_demo1_routh.py` | §7.3 | The array built from coefficients; sign-change count matches the root finder; the footnote typo. | **live** |
| 2 | `l4_demo2_gain_range.py` | §8 | The imaginary-axis crossing found by sweeping roots is $K=7.5000$, exactly Routh's answer. | slide |
| 3 | `l4_demo3_pi_region.py` | §9 | Routh's two inequalities agree with root computations at 40,401 gain pairs, with zero disagreements. | slide |
| 4 | `l4_demo4_bibo_internal.py` | §5.3, §6.3 | Bounded input, unbounded output; and a stable transfer function over an internally unstable system. | **live** |

## 19. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| L1 | 3.1 | Convolution, transfer functions, frequency response, partial fractions, final value, poles and zeros |
| L2 | 3.2, 3.3 | Block diagrams, effect of pole locations |
| L3 | 3.4, 3.5 | Time-domain specifications; effects of zeros and additional poles |
| **This lecture (L4)** | **3.6–3.9** | **BIBO and internal stability, Routh's criterion, system identification, scaling, historical perspective, chapter summary** |
| Next | Chapter 4 | Feedback: what moving the poles actually buys |
