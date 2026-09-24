# Dynamic Response III — Time-Domain Specifications and the Effects of Zeros
## FPE 8th ed., Sections 3.4 and 3.5

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404)

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §§3.4–3.5. Worked examples and figure numbers are the book's. Additions of my own are marked **[beyond the book]**.

**Prerequisites:** L2 of this series (§3.3: pole locations, $\zeta$, $\omega_n$, $\sigma$, $\omega_d$, the Fig. 3.18 geometry). The physical origin of zeros is in [From Physical Models to the Laplace Transform](modeling-and-dynamics_instructor.md), cited as *(0.0.8 §n)*.

**Earlier-lecture shorthand:** “0.0.8 §n” below refers to section n of the linked prerequisite, whose current filename is `modeling-and-dynamics_instructor.md`.

**Duration:** 75 minutes.

**Book figures:** figure numbers refer to the source chapter at

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./3 - Dynamic Response.pdf
```

Page cues below use the PDF viewer's 1-based page numbers (202 pages). Project the figures directly from this PDF; extracted image files are not supplied. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index lists the scripts.

**Notation:**

| Symbol | Meaning |
|---|---|
| $t_r$ | rise time, from 10% to 90% of the final value |
| $t_p$ | peak time |
| $M_p$ | overshoot, as a fraction of the final value |
| $t_s$ | settling time, to within 1% here (2% and 5% are also used) |
| $\sigma=\zeta\omega_n$ | distance of the pole from the imaginary axis; positive for a stable pole |
| $\alpha$ | normalised zero (or extra-pole) location: the zero sits at $s=-\alpha\zeta\omega_n=-\alpha\sigma$ |

---

# Part 0 — Planning

## 1. Teaching strategy

Last lecture ended with a picture and no numbers. Today supplies the numbers, and then immediately tells the truth about them.

The lecture has a clean two-act shape:

**Act I (§3.4).** Three formulas connect a step response to a pole location:

$$
t_r\simeq\frac{1.8}{\omega_n},
\qquad
M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}},
\qquad
t_s\simeq\frac{4.6}{\sigma} .
$$

Inverted, they turn a specification into a *region* of the $s$-plane. That is the single most useful thing in the chapter for design.

**Act II (§3.5).** Every one of those formulas assumed two poles and no zeros. Real systems have zeros and extra poles. So: what do they change, by how much, and when can you ignore them?

The through-line to say out loud:

> **Act I gives you somewhere to put the poles. Act II tells you why the answer will not be quite what you asked for, and by how much.**

Three moments to protect:

1. **§6** — Example 3.27, a specification drawn as a region. Everything in Chapter 5 lands in this picture.
2. **§9** — the derivative decomposition, $y=y_0+\frac{1}{\alpha\zeta}\dot y_0$. It explains a LHP zero and a RHP zero with one equation.
3. **§11** — the Boeing 747 going down before it goes up. This is the moment nonminimum phase stops being vocabulary.

---

## 2. Learning objectives

By the end of this lecture students should be able to:

1. Define $t_r$, $t_p$, $M_p$ and $t_s$ off a step-response plot, and state the convention each definition depends on.
2. Derive $t_p=\pi/\omega_d$ and $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ from the second-order step response.
3. Explain why $t_s\simeq4.6/\sigma$ is an approximate decay-time rule, distinguish it from a conservative envelope bound, and explain why $t_r\simeq1.8/\omega_n$ is a fit.
4. Convert a set of specifications into $\omega_n$, $\zeta$ and $\sigma$ bounds, and shade the allowable region of the $s$-plane (Example 3.27).
5. Give the first-order results: $M_p=0$, $t_r=2.2/\sigma$, $t_s=4.6/\sigma$.
6. Explain how a zero near a pole reduces that mode's coefficient, using the cover-up formula (Eqs. 3.78–3.79).
7. Decompose the step response of a system with a zero into $y_0+\frac{1}{\alpha\zeta}\dot y_0$, and use it to predict increased overshoot for a LHP zero and initial undershoot for a RHP zero.
8. State the factor-of-four rule for both zeros and extra poles, and the direction of each effect.
9. Recognise nonminimum-phase behaviour in a physical system and explain the mechanism (Example 3.30).
10. Judge when the second-order estimates may be used on a higher-order plant, and verify the judgement by simulation.

---

## 3. Suggested lecture flow (75 minutes)

| Time | Topic | Section |
|---:|---|---|
| 0–4 min | Recap; today's question: how much overshoot, settled by when? | §4 |
| 4–10 min | The four definitions (Fig. 3.23) | §5.1 |
| 10–16 min | Rise time, and why 1.8 | §5.2 |
| 16–26 min | Overshoot and peak time, derived | §5.3 |
| 26–32 min | Settling time and the envelope; the first-order case | §5.4–§5.5 |
| 32–42 min | Design synthesis; Example 3.27; the region | §6 |
| 42–52 min | Zeros: coefficient modification, the normalised family, Fig. 3.29 | §7–§8 |
| 52–60 min | The derivative decomposition; RHP zeros | §9–§10 |
| 60–68 min | Example 3.28, Example 3.29; the Boeing 747 | §10.2–§11 |
| 68–75 min | Extra poles; the four conclusions; closing | §12–§13 |

**Prepare as slides:** Figs. 3.23, 3.24, 3.25, 3.26 (definitions and regions) and Figs. 3.27–3.38 (the zero and extra-pole families). There are many figures in §3.5 and almost no algebra; resist deriving what a picture already settles. Reserve the board for the $M_p$ derivation (§5.3), the Example 3.27 arithmetic (§6), and Eq. (3.81) (§9).

**If you are short of time,** drop Example 3.29 (complex zeros near lightly damped poles) and cover the extra-pole material from the summary box alone. Protect §6 and §11.

### Runnable demonstrations

```
cd demos
uv run python ch3/l3_demo2_spec_regions.py --show
uv run python ch3/l3_demo4_extra_pole_aircraft.py --show
```

**Run Demo 2 and Demo 4 live.** Demo 2 shows a pole pair placed exactly on the specification boundary and then failing the specification, which is the honest version of §3.4. Demo 4 is the aeroplane. Demos 1 and 3 are prepared figures.


### Teaching scope

Use the demos for the selected live examples; the accompanying checks also work on the board. For a 75-minute session, select the protected examples in §1; assign the remaining worked examples and optional computations as follow-up reading. Do not try to present every figure and derivation live.

---

# Part I — The lecture

## 4. Opening

### Instructor script

> Last time we learned to look at a pole and say "fast", "slow", "rings", "unstable". That is a real skill, and it is not enough to design with.
>
> A customer does not ask for a well-damped pair. They ask for: reaches the new setpoint in under half a second, overshoots by no more than ten percent, and is settled within three.
>
> So today has two jobs. First, convert those three numbers into a place to put the poles. Second — and this is the part the book is unusually honest about — find out how much to trust the conversion.

---

## 5. The four specifications (§3.4)

### 5.1 Definitions

> **[ FIG 3.23 ]** — PDF p. 106 *(slide; leave it up for the whole of §5)*

| Quantity | Definition |
|---|---|
| **Rise time** $t_r$ | time to get to the vicinity of the new setpoint; the book uses 10% to 90% |
| **Settling time** $t_s$ | time for the transient to decay and stay inside a band; 1% here |
| **Overshoot** $M_p$ | for the positive unit-step responses here, the maximum excess over the final value, divided by the final value |
| **Peak time** $t_p$ | time at which that maximum occurs |

#### Say out loud

> Two of these depend on a convention someone chose. Rise time could be 0% to 100%, or 5% to 95%. Settling could be to 1%, 2% or 5%. When you read a specification from a customer or a datasheet, **find out which convention it uses** before you compare it with anything.

### 5.2 Rise time

The book's argument is a fit, not a derivation: look at the family of step responses in Fig. 3.19(b), take $\zeta=0.5$ as an average, measure, and get $\omega_nt_r\approx1.8$. Hence

$$
\boxed{
t_r\simeq\frac{1.8}{\omega_n}
\tag{3.68}
}
$$

> **[ DEMO 1 ]** — `ch3/l3_demo1_step_specs.py` *(slide)*
>
> **Teaching check [beyond the book]:** Compute the 10% and 90% crossings of the standard step response. The products $\omega_nt_r$ are approximately 1.10, 1.64, 2.13, and 3.36 at $\zeta=0.1,0.5,0.7,1$, respectively. The value 1.8 is attained near $\zeta=0.58$; it is a rough fit, not a bound.

**[beyond the book]** That last sentence has a consequence students should hear now rather than discover in a lab: a pole pair placed exactly on the $\omega_n$ boundary can *fail* the rise-time requirement if its damping is high. Demo 2 shows exactly that case.

### 5.3 Overshoot and peak time — derive this one

For zero initial state, unit DC gain, $\omega_n>0$, and $0<\zeta<1$, the step response of the standard second-order system is

$$
y(t)=1-e^{-\sigma t}\left(\cos\omega_dt+\frac{\sigma}{\omega_d}\sin\omega_dt\right)
\tag{3.69}
$$

(derived by partial fractions in L2 §10.2). The identity $A\sin\alpha+B\cos\alpha=C\cos(\alpha-\beta)$ compresses it. Here the bracket has $B=1$ and $A=\sigma/\omega_d=\zeta/\sqrt{1-\zeta^2}$, so

$$
C=\sqrt{1+\frac{\zeta^2}{1-\zeta^2}}=\frac{1}{\sqrt{1-\zeta^2}},
\qquad
\cos\beta=\frac BC=\sqrt{1-\zeta^2},
\qquad
\sin\beta=\frac AC=\zeta .
$$

Hence $\beta=\sin^{-1}\zeta$, the same angle $\theta$ as in the Fig. 3.18 pole geometry, and

$$
\boxed{
y(t)=1-\frac{e^{-\sigma t}}{\sqrt{1-\zeta^2}}\cos(\omega_dt-\beta),
\qquad
\beta=\sin^{-1}\zeta
\tag{3.70}
}
$$

**Source correction [beyond the book]:** Eq. (3.70) on PDF p. 108 prints $\sqrt{1-\zeta}$ in the denominator; it should be $\sqrt{1-\zeta^2}$, as used here and in the envelope bound in §5.4.

Differentiate Eq. (3.69) with the product rule. The derivative of $-e^{-\sigma t}$ is $+\sigma e^{-\sigma t}$, and the bracket differentiates to $-\omega_d\sin\omega_dt+\sigma\cos\omega_dt$:

$$
\dot y(t)=\sigma e^{-\sigma t}\left(\cos\omega_dt+\frac{\sigma}{\omega_d}\sin\omega_dt\right)
-e^{-\sigma t}\left(-\omega_d\sin\omega_dt+\sigma\cos\omega_dt\right).
$$

The two cosine terms, $+\sigma\cos$ and $-\sigma\cos$, cancel. That is the collapse. What remains is

$$
\dot y(t)=e^{-\sigma t}\left(\frac{\sigma^2}{\omega_d}+\omega_d\right)\sin\omega_dt
=\frac{\omega_n^2}{\omega_d}e^{-\sigma t}\sin\omega_dt ,
$$

using $\sigma^2+\omega_d^2=\omega_n^2$. This is the impulse response, Eq. (3.66), as it must be.

**Everything except $\sin\omega_dt$ is strictly positive**, so nonzero-time extrema occur at $\omega_dt=k\pi$. Odd $k$ give maxima and even $k$ minima. The first peak is at $\omega_dt_p=\pi$:

$$
\boxed{
t_p=\frac{\pi}{\omega_d}
\tag{3.71}
}
$$

Substituting $\omega_dt_p=\pi$ into Eq. (3.69), $\cos\pi=-1$ and $\sin\pi=0$:

$$
y(t_p)=1-e^{-\sigma\pi/\omega_d}(-1+0)=1+e^{-\sigma\pi/\omega_d} .
$$

The final value is 1, so the overshoot is $M_p=e^{-\sigma\pi/\omega_d}$. Finally, $\sigma/\omega_d=\zeta\omega_n/(\omega_n\sqrt{1-\zeta^2})=\zeta/\sqrt{1-\zeta^2}$:

$$
\boxed{
M_p=e^{-\zeta\pi/\sqrt{1-\zeta^2}},
\qquad 0<\zeta<1
\tag{3.72}
}
$$

> **[ FIG 3.24 ]** — PDF p. 110 *(slide)*

At $\zeta=0$, the same peak formula gives a 100% excursion above the equilibrium value, but the response never settles and has no final-value limit. For $\zeta\ge1$, the zero-free standard step response is monotone: $M_p=0$ and there is no finite overshoot peak time.

Two values to memorise, and they should be memorised. At $\zeta=0.5$ the exponent is $\pi(0.5)/0.866=1.814$, and $e^{-1.814}=0.163$. At $\zeta=0.7$ it is $\pi(0.7)/0.714=3.079$, and $e^{-3.079}=0.046$:

$$
\boxed{
\zeta=0.5 \Rightarrow M_p=16\%
\qquad\qquad
\zeta=0.7 \Rightarrow M_p=5\%
}
$$

#### Ask the class

> $M_p$ depends on $\zeta$ alone. Not on $\omega_n$. Why should that be?

Because $\omega_n$ only scales time. Two systems with the same $\zeta$ have the same step response shape, one played faster than the other. Overshoot is a property of the shape.

Algebraically, $\sigma t=\zeta(\omega_nt)$ and $\omega_dt=\sqrt{1-\zeta^2}(\omega_nt)$. Eq. (3.69) is therefore a function of $\zeta$ and the normalised time $\omega_nt$ only. The peak *height* depends on $\zeta$ alone, and the peak *time* scales as $1/\omega_n$.

### 5.4 Settling time

The textbook uses the exponential decay rate to estimate the 1% settling time. Dropping the oscillatory phase and the envelope prefactor gives

$$
e^{-\sigma t_s}=0.01
\quad\Longrightarrow\quad
\sigma t_s=-\ln0.01=\ln100=4.605
\quad\Longrightarrow\quad
\boxed{
t_s\simeq\frac{4.6}{\zeta\omega_n}=\frac{4.6}{\sigma}
\tag{3.73}
}
$$

**Qualification [beyond the book]:** Eq. (3.70) gives the full bound

$$
|y(t)-1|\le\frac{e^{-\sigma t}}{\sqrt{1-\zeta^2}},\qquad
t_{s,\mathrm{env}}=\frac{-\ln\!\left(\epsilon\sqrt{1-\zeta^2}\right)}{\sigma},
\qquad 0<\zeta<1.
$$

The bound follows from Eq. (3.70) because $|\cos(\cdot)|\le1$. To get $t_{s,\mathrm{env}}$, set the bound equal to $\epsilon$ and take logs: $e^{-\sigma t}=\epsilon\sqrt{1-\zeta^2}$, so $\sigma t=-\ln(\epsilon\sqrt{1-\zeta^2})$. For a tolerance $\epsilon=0.01$, the response stays in the band once $t\ge t_{s,\mathrm{env}}$. The actual settling time is the last band crossing and can be earlier. The shorter rule $4.6/\sigma$ is **not a guaranteed upper bound**. Near critical damping the sinusoidal envelope bound is very loose; use the actual response. At $\zeta=1$, the step response is $1-(1+\omega_nt)e^{-\omega_nt}$ (L2 §10.2), which approaches 1 monotonically from below. Setting the error $(1+x)e^{-x}=0.01$ with $x=\omega_nt$ gives a transcendental equation. Its root is $x\approx6.64$ (Newton's method from $x=6$ gives 6.49, 6.63, 6.64; or use `fsolve`), so $t_s\approx6.64/\omega_n$, not $4.6/\omega_n$. The factor $(1+x)$ is what the pure-exponential rule misses.

> **[ FIG 3.21 ]** — PDF p. 99 *(recall from L2: the envelope)*

> **[ DEMO 1, continued ]** — right-hand panel
>
> **Teaching check [beyond the book]:** At $\zeta=0.7$, $\omega_n=4$ rad/s, the actual 1% settling time is approximately 1.644 s, slightly later than $4.6/\sigma=1.643$ s. The corrected envelope bound above is approximately 1.765 s. Arithmetic: $\sigma=0.7\times4=2.8$ s$^{-1}$, $4.6/2.8=1.643$ s, $\sqrt{1-0.49}=0.714$, and $-\ln(0.00714)/2.8=4.942/2.8=1.765$ s. Thus the textbook estimate is not guaranteed conservative.

### 5.5 The first-order case

For $H(s)=\dfrac{\sigma}{s+\sigma}$ the step response is

$$
y(t)=\left(1-e^{-\sigma t}\right)1(t)
\tag{3.77}
$$

(the step response of L2 §8.2, scaled to unit DC gain). Each specification follows by solving $y(t)=$ level:

- **Overshoot.** $\dot y=\sigma e^{-\sigma t}>0$, so $y$ rises monotonically to 1 and never exceeds it: $M_p=0$.
- **Rise time.** $1-e^{-\sigma t}=p$ gives $t=-\ln(1-p)/\sigma$. So $t_{10}=-\ln0.9/\sigma=0.105/\sigma$ and $t_{90}=-\ln0.1/\sigma=2.303/\sigma$. The difference is $t_r=(\ln10-\ln\tfrac{10}{9})/\sigma=\ln9/\sigma=2.197/\sigma$.
- **Settling time.** The error is $e^{-\sigma t}$ exactly, with no oscillation and no prefactor. It reaches 0.01 at $t_s=\ln100/\sigma=4.605/\sigma$.

$$
\boxed{
M_p=0,
\qquad
t_r=\frac{\ln9}{\sigma}\approx\frac{2.2}{\sigma},
\qquad
t_s=\frac{\ln100}{\sigma}\approx\frac{4.6}{\sigma},
\qquad
\tau=\frac1\sigma
}
$$

Note that $t_r$ here is *derived exactly*, unlike the second-order 1.8. Point that out; it explains why the second-order constant is different and approximate.

---

## 6. Design synthesis: specifications become a region

Invert the three formulas to obtain an **approximate design region**. Here $t_r,t_s,M_p$ denote the specified upper limits; only the overshoot constraint is exact for the standard underdamped pair:

$$
\boxed{
\omega_n\ge\frac{1.8}{t_r}
\qquad
\zeta\ge\zeta(M_p)
\qquad
\sigma\ge\frac{4.6}{t_s}
\tag{3.74–3.76}
}
$$

Each is a geometric constraint:

For $0<M_p<1$, the exact damping bound is

$$
\zeta\ge\frac{-\ln M_p}{\sqrt{\pi^2+(\ln M_p)^2}}.
$$

**Derivation.** Take logs of Eq. (3.72) and write $L=-\ln M_p>0$:

$$
\frac{\pi\zeta}{\sqrt{1-\zeta^2}}=L
\quad\Longrightarrow\quad
\pi^2\zeta^2=L^2(1-\zeta^2)
\quad\Longrightarrow\quad
\zeta^2(\pi^2+L^2)=L^2
\quad\Longrightarrow\quad
\zeta=\frac{L}{\sqrt{\pi^2+L^2}} .
$$

Squaring is safe because both sides are positive for $0<\zeta<1$. $M_p$ decreases as $\zeta$ increases, so "$M_p\le$ spec" becomes "$\zeta\ge$ this value".

**The other two bounds** follow directly from Eqs. (3.68) and (3.73). $t_r\simeq1.8/\omega_n\le t_r^{\rm spec}$ gives $\omega_n\ge1.8/t_r^{\rm spec}$, and $t_s\simeq4.6/\sigma\le t_s^{\rm spec}$ gives $\sigma\ge4.6/t_s^{\rm spec}$.

**Why each is the stated shape (the L2 §10.1 geometry).** $\omega_n$ is the pole's distance from the origin, so a lower bound on it excludes a disc. $\zeta=\sin\theta$ with $\theta$ measured from the imaginary axis, so a lower bound on $\zeta$ is a lower bound on $\theta$: a wedge about the negative real axis. $\sigma$ is the distance from the imaginary axis, so a lower bound on it is a half-plane to the left of a vertical line.

| Bound | Region in the $s$-plane |
|---|---|
| $\omega_n\ge$ | outside a circle of that radius |
| $\zeta\ge$ | inside a wedge, measured by the angle $\theta=\sin^{-1}\zeta$ from the imaginary axis |
| $\sigma\ge$ | to the left of a vertical line |

> **[ FIG 3.25 ]** — PDF p. 113, PDF p. 113, PDF p. 114, PDF p. 114 *(slide: the three regions and their intersection)*

### 6.1 Example 3.27

Requirements: $t_r\le0.6$ s, $M_p\le10\%$, $t_s\le3$ s. On the board:

$$
\omega_n\ge\frac{1.8}{0.6}=3\ \text{rad/s},
\qquad
\zeta\ge0.6,
\qquad
\sigma\ge\frac{4.6}{3}=1.53\ \text{s}^{-1} .
$$

> **[ FIG 3.26 ]** — PDF p. 117 *(slide)*
>
> **Careful:** the shading in the book's Fig. 3.26 covers the region that is **excluded**; the allowable set is to the left of the solid boundary, as the text says. Say which is which before a student copies the picture into an exam answer.

The book's closing observation is worth the extra thirty seconds: any pole meeting the $\omega_n$ and $\zeta$ bounds automatically satisfies the $\sigma$ bound, since $\sigma=\zeta\omega_n\ge0.6\times3=1.8>1.53$. **The settling requirement is not binding here.** Recognising which specification is actually driving the design is a skill worth naming.

**Two small corrections to make in passing [beyond the book]:**

- Inverting $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ at 10% gives $\zeta=0.591$: $L=-\ln0.1=2.303$, so $\zeta=2.303/\sqrt{9.870+5.302}=2.303/3.895=0.591$. The corresponding wedge half-angle is $\theta=\sin^{-1}0.591=36.2^\circ$. The book reads 0.6 off Fig. 3.24, which is the same number rounded, but students should know the bound is exact and computable.
- The book prints "$\sigma\ge4.6/3=1.5$ sec". The value is right and the unit is not: $\sigma$ is a rate, in inverse seconds.

> **[ DEMO 2 ]** — `ch3/l3_demo2_spec_regions.py` *(live, ~10 s — the most important demo of this lecture)*
>
> **Teaching check [beyond the book]:** Place the poles at $\zeta=0.7$, $\omega_n=3$ rad/s. They satisfy the approximate design region: $\omega_n=3\ge3$, $\zeta=0.7\ge0.591$, and $\sigma=2.1\ge1.53$. Yet the actual 10–90% rise time is about 0.709 s, which is $\omega_nt_r\approx2.13$ from §5.2 divided by $\omega_n=3$, exceeding 0.6 s. The overshoot constraint is exact for the standard pair; the rise-time circle and settling-time line require verification.

---

## 7. Zeros, first pass: they reweight the modes (§3.5)

### Instructor script

> Everything so far assumed two poles and no zeros. Now let us add a zero and see what breaks.
>
> Start with the cover-up formula from Lecture 1. The coefficient of the mode at $p_1$ is the whole transfer function, with the $(s-p_1)$ factor removed, evaluated at $s=p_1$.
>
> So: if there is a zero *near* $p_1$, that evaluation is near zero, and the coefficient is small. A zero near a pole switches that mode off.

The book's pair of examples, normalised to the same DC gain:

$$
H_1(s)=\frac{2}{(s+1)(s+2)}=\frac{2}{s+1}-\frac{2}{s+2}
\tag{3.78}
$$

$$
H_2(s)=\frac{2(s+1.1)}{1.1(s+1)(s+2)}=\frac{2/11}{s+1}+\frac{18/11}{s+2}
\tag{3.79}
$$

**The residues, by cover-up.** Both transfer functions have $H(0)=1$: $2/(1\cdot2)=1$ and $2(1.1)/(1.1\cdot1\cdot2)=1$. The 1.1 in the denominator of $H_2$ is there to make that true.

$$
H_1:\quad
\left.\frac{2}{s+2}\right|_{s=-1}=\frac{2}{1}=2,
\qquad
\left.\frac{2}{s+1}\right|_{s=-2}=\frac{2}{-1}=-2 .
$$

$$
H_2:\quad
\left.\frac{2(s+1.1)}{1.1(s+2)}\right|_{s=-1}=\frac{2(0.1)}{1.1(1)}=\frac{0.2}{1.1}=\frac{2}{11},
\qquad
\left.\frac{2(s+1.1)}{1.1(s+1)}\right|_{s=-2}=\frac{2(-0.9)}{1.1(-1)}=\frac{1.8}{1.1}=\frac{18}{11} .
$$

The factor $(s+1.1)$ evaluated at the pole $s=-1$ is $0.1$. That small number is the whole effect.

$$
\boxed{
\text{the coefficient of }e^{-t}\text{ fell from }2\text{ to }2/11\approx0.18
}
$$

because the zero at $-1.1$ nearly cancels the pole at $-1$. Put the zero exactly at $-1$ and the term vanishes entirely.

#### Ask the class

> If a zero can switch a mode off, is a pole-zero cancellation a good way to get rid of a mode you dislike?

Hold the answer. It is Example 3.29 in twenty minutes, and Lecture 4 in a week. The short version: it removes the mode from *this* transfer function only.

---

## 8. The normalised family

To study zeros systematically, put the zero at $s=-\alpha\zeta\omega_n=-\alpha\sigma$ and normalise:

$$
\boxed{
H(s)=\frac{(s/\alpha\zeta\omega_n)+1}{(s/\omega_n)^2+2\zeta(s/\omega_n)+1}
\tag{3.80}
}
$$

For $\alpha>0$, **read $\alpha$ as the ratio of the zero's distance from the imaginary axis to the pair's distance $\sigma$**. Large $\alpha$ means a relatively distant LHP zero. $\alpha=1$ means equal real parts, not coincidence with either complex pole. Negative $\alpha$ puts the zero in the RHP. Assume $0<\zeta<1$ in this family.

> **[ FIG 3.27 ]** — PDF p. 120 ($\zeta=0.5$)
> **[ FIG 3.28 ]** — PDF p. 121 ($\zeta=0.707$)
> **[ FIG 3.29 ]** — PDF p. 122 (overshoot versus $\alpha$)
>
> **Show:** Fig. 3.27, then Fig. 3.29 immediately after.
> **Say:** "In this family the LHP zero raises overshoot and quickens the rise. It leaves the pole decay rates unchanged, but changing modal amplitudes can still change settling time. Its effect diminishes with distance; decide whether it is negligible using the actual specification."

> **[ DEMO 3 ]** — `ch3/l3_demo3_zeros.py` *(slide)*
>
> **Teaching check [beyond the book]:** For $\zeta=0.5$, compare the zero-free overshoot (16.3%) with $\alpha=4,2,1,0.5$: approximately 19.1%, 29.8%, 69.9%, and 171%. A nearby zero can change the response substantially even though the poles are fixed.

**The factor-of-four rule** is the book's heuristic for when a real LHP zero is likely to matter. It is not an error bound: at $\alpha=4$, overshoot still rises from 16.3% to 19.1% in this example.

---

## 9. Why: the derivative decomposition

This is the explanation that makes both the LHP and the RHP case obvious, so give it the board.

Set $\omega_n=1$. Eq. (3.80) becomes

$$
H(s)=\frac{\dfrac{s}{\alpha\zeta}+1}{s^2+2\zeta s+1} .
$$

The numerator is a sum of two terms, so split the fraction into two terms over the same denominator:

$$
\boxed{
H(s)=\underbrace{\frac{1}{s^2+2\zeta s+1}}_{H_0(s)}
+\frac{1}{\alpha\zeta}\underbrace{\frac{s}{s^2+2\zeta s+1}}_{sH_0(s)}
\tag{3.81}
}
$$

The second term is a constant times $s$ times the first. With a step input, $Y=H/s$, so $Y=Y_0+\frac1{\alpha\zeta}sY_0$ with $Y_0=H_0/s$. By property 5 of L1 §9, $\mathcal L\{\dot y_0\}=sY_0-y_0(0^-)=sY_0$, because the system starts at rest. Multiplication by $s$ is differentiation. Therefore, in the time domain,

$$
\boxed{
y(t)=y_0(t)+\frac{1}{\alpha\zeta}\,\dot y_0(t)
}
$$

where $y_0$ is the step response of the zero-free system.

With physical time and arbitrary $\omega_n$, the coefficient is $1/(\alpha\zeta\omega_n)=1/(\alpha\sigma)$. The displayed $1/(\alpha\zeta)$ form uses $\omega_n=1$ (or differentiation with respect to normalised time). The zero initial value of $y_0$ is what permits $sY_0=\mathcal L\{\dot y_0\}$ without an initial-condition term.

> **[ FIG 3.30 ]** — PDF p. 124 *(slide: $y$, $y_0$ and the derivative term)*
>
> **Say:** "The derivative has a large hump early, while $y_0$ is still climbing. Adding that hump lifts the early response — which is exactly what more overshoot and a quicker rise look like."

> **[ DEMO 3, continued ]** — the decomposition table
>
> **Teaching check [beyond the book]:** Use the analytical derivative $\dot y_0=h_0$ to check $y=y_0+\dot y_0/(\alpha\zeta)$ when $\omega_n=1$. This avoids mistaking finite-difference error for failure of the identity.

---

## 10. Right half-plane zeros

Now let $\alpha<0$, so the zero sits at $s=+|\alpha|\sigma$. The numerator becomes $1-s/(|\alpha|\zeta)$ and

$$
\boxed{
y(t)=y_0(t)-\frac{1}{|\alpha|\zeta}\dot y_0(t)
}
$$

**The hump is subtracted.** Early on, when $\dot y_0$ is largest, the response is pushed *down* — often below zero.

> **[ FIG 3.31 ]** — PDF p. 125 *(slide)*

$$
\boxed{
\text{One real RHP zero added to this standard pair}
\ \Rightarrow\
\text{the step response starts out in the wrong direction}
}
$$

This is **nonminimum-phase** behaviour. Here $\dot y(0^+)=1/(\alpha\zeta)<0$ in normalised units, which proves the initial reversal.

*Derivation of the initial slope.* Differentiate the decomposition: $\dot y=\dot y_0+\frac1{\alpha\zeta}\ddot y_0$. For the zero-free pair, $\dot y_0=h_0$, which has $h_0(0^+)=0$ by Eq. (3.66) because $\sin0=0$. Its derivative at $0^+$ is $\ddot y_0(0^+)=\omega_n^2=1$, from differentiating Eq. (3.66) or from the initial value theorem, $\lim_{s\to\infty}s^2H_0(s)=1$. So $\dot y(0^+)=0+\frac1{\alpha\zeta}\cdot1=1/(\alpha\zeta)$, which is negative for $\alpha<0$. In general, having RHP zeros does not always mean the step response's first motion is backwards; other zeros and the relative degree matter. For example, two real RHP zeros can give an initially positive response followed by an inverse excursion. The unstable zero-dynamics interpretation is developed in *(0.0.8 §31–§34)*.

> **[ DEMO 3, continued ]** — the RHP table
>
> **Teaching check [beyond the book]:** For $\zeta=0.5$, $\omega_n=1$ and $\alpha=-1,-2,-4$, the minimum step-response values are approximately $-0.752,-0.280,-0.091$. The early negative excursion grows as the positive real zero approaches the origin.

### 10.1 A correction worth making [beyond the book]

The book's summary says a RHP zero "will depress the overshoot". Read carefully, because the comparison matters:

| Comparison | Result |
|---|---|
| RHP zero at $\alpha=-2$ versus LHP zero at $\alpha=+2$ | 20.9% versus 29.8% — **depressed** |
| RHP zero at $\alpha=-2$ versus no zero at all | 20.9% versus 16.3% — **raised** |

For this family, against the same-distance LHP zero the statement holds. Against the zero-free system it does not: subtracting the derivative term *after* the peak, where $\dot y_0<0$, pushes the response up. The reliable lesson here is inverse response and a performance limitation, not a universal decrease in overshoot. Demo 3 prints all three numbers.

### 10.2 Example 3.28: the zero moving through the poles

$$
H(s)=\frac{24}{z}\cdot\frac{s+z}{(s+4)(s+6)},
\qquad z=1,\dots,6
$$

The factor $24/z$ makes the DC gain unity: $H(0)=\frac{24}{z}\cdot\frac{z}{4\cdot6}=1$. For a unit step,

$$
Y(s)=\frac{24}{z}\cdot\frac{s+z}{s(s+4)(s+6)}=\frac{C_0}{s}+\frac{C_4}{s+4}+\frac{C_6}{s+6} .
$$

Cover up each factor:

$$
C_0=\frac{24}{z}\cdot\frac{z}{(4)(6)}=1,
\qquad
C_4=\frac{24}{z}\cdot\frac{z-4}{(-4)(2)}=-\frac{3(z-4)}{z}=\frac{12}{z}-3,
\qquad
C_6=\frac{24}{z}\cdot\frac{z-6}{(-6)(-2)}=\frac{2(z-6)}{z}=2-\frac{12}{z} .
$$

So the step response is

$$
y(t)=1+\left(\frac{12}{z}-3\right)e^{-4t}+\left(2-\frac{12}{z}\right)e^{-6t} .
$$

*Check:* $y(0)=1+\frac{12}{z}-3+2-\frac{12}{z}=0$ for every $z$ ✓.

> **[ FIG 3.32 ]** — PDF p. 127 *(slide)*

Read the coefficients as $z$ moves, from Demo 3's table:

| $z$ | coeff. of $e^{-4t}$ | coeff. of $e^{-6t}$ | overshoot |
|---:|---:|---:|---:|
| 1 | $+9.000$ | $-10.000$ | 108% |
| 2 | $+3.000$ | $-4.000$ | 25% |
| 3 | $+1.000$ | $-2.000$ | 3.7% |
| 4 | $0$ | $-1.000$ | 0 |
| 5 | $-0.600$ | $-0.400$ | 0 |
| 6 | $-1.000$ | $0$ | 0 |

**The overshoot column, by hand [beyond the book].** Write $c_4$ and $c_6$ for the two coefficients. A peak needs $\dot y=-4c_4e^{-4t}-6c_6e^{-6t}=0$. Dividing by $e^{-6t}$ gives $e^{2t_p}=-\dfrac{6c_6}{4c_4}$. This has a positive solution only when $c_4>0>c_6$ and $-6c_6>4c_4$, which is the case $z<4$. Let $r=e^{-2t_p}=-\dfrac{2c_4}{3c_6}$. Then $e^{-4t_p}=r^2$, $e^{-6t_p}=r^3$, and $y(t_p)=1+c_4r^2+c_6r^3$:

| $z$ | $c_4,\ c_6$ | $r$ | $t_p=-\tfrac12\ln r$ | $y(t_p)$ |
|---:|---|---:|---:|---|
| 1 | $9,\ -10$ | $\tfrac35$ | 0.255 s | $1+9(0.36)-10(0.216)=2.08$ |
| 2 | $3,\ -4$ | $\tfrac12$ | 0.347 s | $1+\tfrac34-\tfrac48=1.25$ |
| 3 | $1,\ -2$ | $\tfrac13$ | 0.549 s | $1+\tfrac19-\tfrac2{27}=1.037$ |

These reproduce 108%, 25% and 3.7%. For $4\le z\le6$ both coefficients are $\le0$, so $y<1$ for all $t>0$ and there is no overshoot.

Three things to point at:

1. **$z=4$ and $z=6$:** a common factor cancels, its residue is *exactly* zero, and the input-output response is first order. If a physical second-order realisation retains that mode, it is hidden from this transfer function; the reduced transfer function alone does not establish its internal presence.
2. **$z=5$, between the poles:** both coefficients are negative, the response approaches its final value from below, and there is no overshoot at all.
3. **$z\le3$:** the zero is nearer the origin than either pole, the coefficients grow and take opposite signs, and the overshoot runs away.

### 10.3 Example 3.29: complex zeros near lightly damped poles

$$
H(s)=\frac{(s+\alpha)^2+\beta^2}{(s+1)\left[(s+0.1)^2+1\right]}
$$

with the poles at $-0.1\pm j$ and the zeros placed at $-\alpha\pm j\beta$ for $(\alpha,\beta)=(0.1,1.0)$, $(0.25,1.0)$ and $(0.5,1.0)$.

> **[ FIG 3.33 ]** — PDF p. 128 *(the three zero locations)*
> **[ FIG 3.34 ]** — PDF p. 130 *(the three step responses)*
>
> **Show:** Fig. 3.33 first and ask the class to predict; then Fig. 3.34.
> **Point at:** the $(0.1,1.0)$ trace, where the zeros land exactly on the poles and the oscillation disappears completely, and the $(0.5,1.0)$ trace, where they do not and it does not.

Then read the book's warning, which is the whole lesson of the example:

> *In practice, the locations of the lightly damped poles are not known precisely, and exact cancellation is not really possible.*

**[beyond the book]** The stated transfer function has DC gain $H(0)=\dfrac{\alpha^2+\beta^2}{1\cdot(0.1^2+1)}=\dfrac{\alpha^2+\beta^2}{1.01}$. For the three cases this is $1.01/1.01=1.00$, $1.0625/1.01=1.052$ and $1.25/1.01=1.238$. Fig. 3.34 is drawn about a common final value of 1, suggesting an unstated normalisation or a plotting inconsistency. To reproduce that comparison explicitly, plot $H(s)/H(0)$ and label it normalised. The source does not state the normalisation. Placing compensator zeros near a resonance can attenuate its response, but exact cancellation is sensitive to modelling error. L4 treats unstable cancellations.

---

## 11. Example 3.30: an aeroplane that descends when you pull up

$$
\boxed{
\frac{h(s)}{\delta_e(s)}=\frac{30(s-6)}{s(s^2+4s+13)}
}
$$

Altitude $h$ from elevator angle $\delta_e$, for a Boeing 747. A zero at $s=+6$, from $s-6=0$. Poles at $s=0$ and at the roots of $s^2+4s+13$, which are $s=\frac{-4\pm\sqrt{16-52}}{2}=-2\pm3j$.

> **[ FIG 3.35 ]** — PDF p. 132 *(slide)*

### 11.1 The physics, which is the point

#### Instructor script

> By convention a negative elevator deflection is upward. Deflect the elevators up and you push the tail *down*, which rotates the nose up.
>
> But rotation takes time. In the first instant, all you have done is add a downward force at the tail. The aeroplane sinks.
>
> Then the nose comes up, the wings meet the air at a larger angle of attack, lift increases, and the aircraft climbs to a new altitude.
>
> Down, then up. That is the right half-plane zero, and notice what it is not: it is not a modelling error, not a delay, and not something a better controller removes. It is the physics of where the control surface sits relative to the centre of mass. Compare the flexible-structure and quadrotor examples of the earlier lecture *(0.0.8 §28–§30)*: the same geometry, the same conclusion.

### 11.2 The numbers

Final value, for the negative unit impulse $\delta_e(t)=-\delta(t)$, whose transform is $\Delta_e(s)=-1$:

$$
h(\infty)=\lim_{s\to0}s\cdot\frac{30(s-6)(-1)}{s(s^2+4s+13)}=\frac{30\times(-6)\times(-1)}{13}=+13.8 .
$$

The $s$ in front cancels the integrator pole, leaving $\dfrac{-30(s-6)}{s^2+4s+13}$ evaluated at $s=0$: $\dfrac{-30(-6)}{13}=\dfrac{180}{13}=13.85$.

**The initial dip, from the transform [beyond the book].** The altitude transform is $H_{\rm alt}(s)=\dfrac{-30(s-6)}{s(s^2+4s+13)}$, which has relative degree 2. The initial value theorem gives $h(0^+)=\lim_{s\to\infty}sH_{\rm alt}=0$ and $\dot h(0^+)=\lim_{s\to\infty}s^2H_{\rm alt}=-30$. The aircraft starts at the reference altitude and moves **down** at first, as the physics said.

**Note why an impulse gives a finite final value:** the pole at the origin integrates, and the integral of an impulse is a constant. A step input would give an altitude that increases forever.

Here $sH_{\rm altitude}(s)$ has poles $-2\pm3j$, so the Final Value Theorem applies to this impulse response even though the altitude plant itself has an integrator and is not BIBO stable. After scaling, the altitude impulse response equals the step response of a second-order pair with a RHP zero (see Demo 4 below). Match $s^2+4s+13$ to $s^2+2\zeta\omega_ns+\omega_n^2$. This gives $\omega_n=\sqrt{13}=3.61$ rad/s, $2\zeta\omega_n=4$ so $\zeta=2/\sqrt{13}=0.555$, and $\sigma=\zeta\omega_n=2$, agreeing with the real part of the roots.

The estimates in the table follow:

- $t_r\simeq1.8/3.606=0.50$ s.
- For overshoot, $\sqrt{1-\zeta^2}=\sqrt{9/13}=3/\sqrt{13}$, so the exponent is $\pi\zeta/\sqrt{1-\zeta^2}=\pi\cdot\tfrac{2}{3}=2.094$ and $M_p=e^{-2.094}=0.123$.
- $t_s\simeq4.6/2=2.30$ s.

| Quantity | Estimate | Source | Recomputed from the model (Demo 4) |
|---|---|---|---|
| $t_r$ | 0.50 s | $1.8/\omega_n$ | 0.43 s |
| $M_p$ | 12.3% | Eq. (3.72), using $\zeta=2/\sqrt{13}$ | 13.8% |
| $t_s$ | 2.30 s | $4.6/\sigma$ | 2.54 s |

**Attribution [beyond the book]:** PDF p. 133 gives a coarse zero-free overshoot estimate of 14% from Fig. 3.24; the table instead evaluates Eq. (3.72), giving 12.3%. The book reports the aircraft response as approximately 0.43 s, 14%, and 2.6 s; our recomputation gives 0.429 s, 13.805%, and 2.535 s, rounded in the last column.

> **[ DEMO 4 ]** — `ch3/l3_demo4_extra_pole_aircraft.py` *(live, ~10 s)*
>
> **Teaching check [beyond the book]:** For the negative unit elevator impulse, verify $h(\infty)=180/13\approx13.846$ and an initial minimum near $-1.68$. The altitude transform is $\frac{180}{13}\frac{1-s/6}{s}\frac{13}{s^2+4s+13}$. To see this, factor $-30(s-6)=180(1-s/6)$ and split $180=\frac{180}{13}\cdot13$. After scaling, this impulse response is exactly the step response of the second-order pair with a RHP zero: $1/s$ is the step, and the rest is a unit-DC-gain pair with the zero at $+6$. This explains why the second-order estimates are useful here.

---

## 12. Extra poles

Add a real pole at $-\alpha\zeta\omega_n$ to the standard pair:

$$
\boxed{
H(s)=\frac{1}{\left(\dfrac{s}{\alpha\zeta\omega_n}+1\right)\left[\left(\dfrac{s}{\omega_n}\right)^2+2\zeta\dfrac{s}{\omega_n}+1\right]}
\tag{3.82}
}
$$

> **[ FIG 3.36 ]** — PDF p. 134 ($\zeta=0.5$)
> **[ FIG 3.37 ]** — PDF p. 135 ($\zeta=0.707$)
> **[ FIG 3.38 ]** — PDF p. 136 (normalised rise time versus $\alpha$)

$$
\boxed{
\text{an extra LHP pole increases the rise time; a LHP zero decreases it}
}
$$

> **[ DEMO 4, continued ]** — left and middle panels
>
> **Teaching check [beyond the book]:** For $\zeta=0.5$, the normalised 10–90% rise times with an added pole at $-\alpha\sigma$ are approximately 1.87, 2.29, 3.46, and 8.49 for $\alpha=4,2,1,0.5$, compared with 1.64 without the extra pole. Even $\alpha=4$ changes rise time by about 14%.

Use the same factor-of-four heuristic to identify extra poles worth checking, not to certify that more distant poles have no effect. Approximation accuracy depends on modal residues, zeros, and the required tolerance as well as pole separation.

---

## 13. The summary box and closing

The book gathers §3.5 into four statements. Use this qualified summary so it agrees with the worked examples:

**Source precision note [beyond the book]:** the summary on PDF p. 137 gives approximately 35% overshoot at $\zeta=0.3$; Eq. (3.72) gives 37.23%, rounded to 37% below.

$$
\boxed{
\begin{array}{l}
\textbf{1.}\ \text{Second order, no zeros: }
t_r\simeq1.8/\omega_n,\quad
M_p\approx5\%,16\%,37\%\ \text{at }\zeta=0.7,0.5,0.3,\quad
t_s\simeq4.6/\sigma\\[6pt]
\textbf{2.}\ \text{A nearby real LHP zero increases overshoot in the standard family}\\[6pt]
\textbf{3.}\ \text{A real RHP zero in that family causes inverse response; compare peaks explicitly}\\[6pt]
\textbf{4.}\ \text{An extra real LHP pole slows the rise; factor 4 is a heuristic, not a bound}
\end{array}}
$$

### Closing script

> We turned three customer requirements into three numbers: a radius, an angle, and a distance from the imaginary axis. Their intersection is a region of the $s$-plane, and every design method in the rest of this course is a way of moving poles into that region.
>
> Then we checked the limits of that region. Nearby zeros change modal amplitudes, and an extra pole can slow the rise. The single real RHP zero in our example sends the response backwards first. Cancelling a plant's unstable zero with an unstable controller pole is not a route to internal stability.
>
> Notice what none of this changed: the poles. A zero reweights the modes; it does not move them. That is why we can design with poles and then check with a simulation, rather than the other way around.
>
> One question is still open, and it is the one that makes control engineering harder than it looks. Everything today assumed the response settles at all. Next time: how do we know it does, and how much gain can we use before it does not?

---

# Part II — Materials

## 14. One-board summary

```text
   SECOND ORDER, NO ZEROS         (this is the reference case, and only this one)

     t_r  ~  1.8 / wn        <- a FIT; exact value of wn*t_r is 1.64 at zeta=0.5,
                                2.13 at zeta=0.7.  Calibrated near zeta = 0.6.
     t_p  =  pi / omega_d    <- exact
     M_p  =  exp(-pi zeta / sqrt(1 - zeta^2))   <- exact.  16% at 0.5, 5% at 0.7
     t_s  ~  4.6 / sigma     <- approximate 1% rule, NOT a guaranteed bound
     envelope bound = -ln(0.01*sqrt(1-zeta^2))/sigma,  0 < zeta < 1

   SPECIFICATIONS -> REGION

     t_r <= T   ->  wn    >= 1.8/T      outside a circle
     M_p <= M   ->  zeta  >= zeta(M)    inside a wedge, theta = asin(zeta)
     t_s <= S   ->  sigma >= 4.6/S      left of a vertical line

     ... then SIMULATE.  The circle is a fit; a boundary pole pair can fail.

   ZEROS AND EXTRA POLES        zero at -alpha*sigma

     y(t) = y0(t) + (1/(alpha sigma)) * y0'(t)        <- physical time
     for wn = 1: sigma = zeta, giving the normalised formula

       alpha > 0 (LHP zero) : add the derivative hump  -> more overshoot, faster rise
       alpha < 0 (RHP zero) : subtract it              -> starts BACKWARDS, sluggish
       extra LHP pole                                  -> slower rise

     factor-of-4 rule: a screening heuristic; check error against the specification
     exact cancellation: no contribution in this transfer; inspect internal modes
```

## 15. Discussion questions

1. $M_p$ depends on $\zeta$ alone while $t_r$ and $t_s$ depend on $\omega_n$ and $\sigma$. What does that say about which specification you should negotiate with a customer first?
2. A pole pair sits exactly on the $\omega_n=1.8/t_r$ circle at $\zeta=0.9$ and fails the rise-time requirement. Has the design method failed?
3. Example 3.28 has the zero exactly on a pole for $z=4$. If you built that system and pushed on it, would the missing mode be gone?
4. Two plants have identical poles. One has a zero at $-1$, the other at $+1$. Which is harder to control, and what in the step response tells you so?
5. The 747 climbs to a finite altitude after an impulsive elevator input but would climb forever after a step. Which pole is responsible, and what does that mean for the pilot?
6. When would you deliberately place a compensator zero near a lightly damped pole, given Example 3.29's warning?

## 16. Homework and follow-up problems

| Problem | Topic | Why this one |
|---|---|---|
| 3.16 | DC gain and final value of a second-order system | Short review before using unit-gain response formulas. |
| 3.30, 3.31 | Feedback parameters and attainable pole regions | Tests which specifications can be met simultaneously. |
| 3.25, 3.26 | Choosing gain and pole location for a unity-feedback system | First taste of design in the region. |
| 3.27 | Peak time requirement | Uses Eq. (3.71) alone; short and clean. |
| 3.28, 3.29 | Dynamics dominated by a complex pair; multiple specifications | The Example 3.27 workflow with new numbers. |
| 3.36 | Initial-condition response and logarithmic decrement | Relates observed decay to damping ratio. |
| 3.37 | Ideal pitch response, aircraft | The Example 3.30 setting as a design problem. |
| 3.38 | Approximating higher-order systems by second-order ones | The judgement §12 asks for. |
| 3.39, 3.42 | Modal response form, settling time, and overshoot estimates | State assumptions before applying the formulas. |
| 3.41 | Sketch a step response, then compare with Matlab | Predict from poles and zeros before computing. |

**Suggested additional exercise [beyond the book]:** compare the altitude impulse responses of $-30(s-6)/[s(s^2+4s+13)]$ and $30(s+6)/[s(s^2+4s+13)]$. They have the same poles and final altitude $180/13$, so the comparison isolates zero location. Report undershoot, rise time, and overshoot.

*Answer key (numerical, 1% settling).*

| Zero | Undershoot | $t_r$ | $M_p$ | $t_s$ |
|---|---:|---:|---:|---:|
| $+6$ (RHP, the 747) | $-1.68$ | 0.43 s | 13.8% | 2.54 s |
| $-6$ (LHP mirror) | none | 0.38 s | 15.8% | 2.24 s |

Both zeros are $6=3\sigma$ from the imaginary axis ($|\alpha|=3$ in the normalised family), so both overshoot a little more than the zero-free 12.3%. Only the RHP zero dips first and rises more slowly.

## 17. Instructor cautions

1. **State the settling-time convention and approximation.** The decay-rate estimates are 4.6/$\sigma$, 3.9/$\sigma$, and 3.0/$\sigma$ for 1%, 2%, and 5%. Use §5.4's prefactor for a conservative underdamped envelope bound.
2. **Fig. 3.26's shading marks the excluded region.** The text says the allowable region is to the left of the boundary. Announce it.
3. **"$\sigma\ge4.6/3=1.5$ sec" in Example 3.27 has the wrong unit.** $\sigma$ is a rate. Correct it in passing; it costs five seconds and prevents a persistent confusion.
4. **The rise-time constant is not accurate at high damping.** $\omega_nt_r$ is 2.13 at $\zeta=0.7$ and 3.36 at $\zeta=1$, not 1.8. Demo 2 shows a boundary case failing because of this.
5. **The RHP-zero overshoot claim needs its comparison stated** (§10.1). Against a same-distance LHP zero it depresses the overshoot; against no zero it does not.
6. **Fig. 3.34 and the written model have different final-value conventions.** Normalisation is an inference, not a stated source fact. Label $H/H(0)$ explicitly if reproducing the plot.
7. **Normalised axes everywhere in §3.5.** Figs. 3.27, 3.28, 3.36 and 3.37 all plot against $\omega_nt$. Numbers read off them must be divided by $\omega_n$.
8. **Nonminimum phase and instability are different properties.** The 747's complex pair is stable, but its altitude integrator makes the full plant non-BIBO-stable. A clearer stable nonminimum-phase example is $(1-s)/(s+1)^2$; its RHP zero coexists with LHP poles.

## 18. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l3_demo1_step_specs.py` | §5 | Exact peak formulas, a rise-time fit, and an approximate settling rule compared with the full envelope bound. | slide |
| 2 | `l3_demo2_spec_regions.py` | §6 | A pole pair on the specification boundary that fails the specification. | **live** |
| 3 | `l3_demo3_zeros.py` | §8–§10 | The derivative decomposition; overshoot versus $\alpha$; Example 3.28's exact cancellations. | slide |
| 4 | `l3_demo4_extra_pole_aircraft.py` | §11–§12 | The 747's undershoot and final value; extra-pole rise times matching Fig. 3.38. | **live** |

## 19. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| L1 | 3.1 | Convolution, transfer functions, frequency response, partial fractions, final value, poles and zeros |
| L2 | 3.2, 3.3 | Block diagrams, effect of pole locations |
| **This lecture (L3)** | **3.4, 3.5** | **Time-domain specifications; effects of zeros and additional poles** |
| L4 | 3.6–3.9 | Stability, Routh's criterion, system identification, scaling, history |
