# A First Analysis of Feedback I — The Basic Equations of Control
## FPE 8th ed., Chapter 4 opening and Section 4.1

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404)

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., Chapter 4 introduction and §4.1 (4.1.1–4.1.4). Worked examples, exercises and figure numbers are the book's. The web-only §4.6 (sensitivity of the time response to parameter change) is not supplied. The cost of feedback, raised in Review Questions 4.1–4.2, is supplemented from Åström & Murray, 2nd ed., §12.1 and Oppenheim, Willsky & Nawab, 2nd ed., §11.2. Additions of my own are marked **[beyond the book]**.

**Prerequisites:** the four Chapter 3 lectures, especially [Block Diagrams](block-diagrams_instructor.md) (the feedback formula) and [Stability](stability_instructor.md) (Routh, and the cancellation trap).

**Earlier-lecture shorthand:** “3-L2 §n” and “3-L4 §n” below refer to section n of `block-diagrams_instructor.md` and `stability_instructor.md` respectively. “3-L3” is `time-domain-specs_instructor.md`.

**Duration:** 75 minutes.

**Book figures:** figure numbers refer to

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./4 - A First Analysis of Feedback.pdf
```

Page cues use the PDF viewer's 1-based page numbers (120 pages). The figures are extracted to `book-figures/` and embedded below. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index (§16) lists the scripts.

**Notation:**

| Symbol | Meaning |
|---|---|
| $G(s)=b(s)/a(s)$ | plant transfer function; $a$, $b$ its denominator and numerator polynomials |
| $D_{ol}(s)$, $D_{cl}(s)=c(s)/d(s)$ | open-loop and feedback controllers; from L2 on, the feedback controller is written $D_c$, as FPE does from §4.2 |
| $R,\ W,\ V$ | reference, plant-input disturbance, sensor noise |
| $Y,\ U,\ E$ | output, control, error $E=R-Y$ |
| $L=GD_{cl}$ | loop gain (open-loop transfer function around the loop) |
| $S=1/(1+L)$ | sensitivity function, Eq. (4.23) |
| $\mathcal{T}=L/(1+L)$ | complementary sensitivity = closed-loop transfer function, Eq. (4.24) |
| $S^{T}_{G}$ | sensitivity of $T$ to $G$: fractional change in $T$ per fractional change in $G$ |

---

# Part 0 — Planning

## 1. Teaching strategy

Chapter 3 analysed a system that someone handed us. Chapter 4 is the first time we get to choose part of the system, and the first question is the obvious one: **what does closing the loop actually buy, and what does it cost?**

The section is short and consists almost entirely of one block diagram, Fig. 4.2, and three equations read off it. Everything else is interpretation. The book compares open loop and feedback against the four objectives of Chapter 1:

| Objective | Open loop, Fig. 4.1 | Feedback, Fig. 4.2 |
|---|---|---|
| **Stability** | cannot move plant poles; an unstable plant stays unstable | poles are roots of $ad+bc$: they can be moved |
| **Tracking** | possible by inversion, with three caveats | possible; $E=SR$ |
| **Regulation** | controller has no effect on $W$ or $V$ | $W$ attenuated by $GS$, but $V$ passed by $\mathcal T$ |
| **Sensitivity** | $S=1$: a 10% plant error is a 10% output error | multiplied by $S=1/(1+L)$: reduced where $\lvert S\rvert<1$, e.g. at low frequency with large $L$ |

And one identity binds the right-hand column together:

$$
S+\mathcal{T}=1 .
$$

It is the reason feedback is a design problem and not a free lunch.

The framing line:

> **Feedback buys stability, disturbance rejection and insensitivity to the plant. It pays for them with a sensor, with noise, with control effort, and with the possibility of instability. Today we write down the bill.**

Three moments to protect:

1. **§7.2** — the book's pole-placement exercise. Its answer is a controller whose zeros cancel the plant's poles. Tracking is perfect; the disturbance response shows the cancelled poles are still there.
2. **§8.2** — the regulation dilemma. Large $D_{cl}$ kills $W$ and passes $V$. The resolution is frequency, and it is the seed of every loop-shaping idea in Chapter 6.
3. **§9** — the sensitivity derivation. $S=1/(1+L)$: loop gain of 100 makes the system 100 times less sensitive to the plant.

---

## 2. Learning objectives

By the end of this lecture students should be able to:

1. Derive the output, control and error of the unity-feedback loop (Fig. 4.2) as superpositions of the responses to $R$, $W$ and $V$, Eqs. (4.5)–(4.11).
2. Explain why an open-loop controller cannot stabilise an unstable plant or reject disturbances, and why cancelling a RHP pole fails in both structures.
3. Form the closed-loop characteristic equation $a(s)d(s)+b(s)c(s)=0$ and use it to stabilise the inverted pendulum, Eq. (4.17).
4. State the three caveats on open-loop tracking by plant inversion, and solve the book's pole-placement exercise.
5. Explain the conflict between disturbance rejection and noise rejection, and how frequency separation resolves it.
6. Show that an integrator in the controller removes the steady error to a constant disturbance, while one in the plant does not.
7. Derive the sensitivity $S^{T}_{G}=1/(1+GD_{cl})$ and use it to estimate the effect of a plant-gain change.
8. State $S+\mathcal{T}=1$, and use $|E(j\omega)|=|S(j\omega)||R(j\omega)|$ for sinusoidal inputs.
9. List the costs of feedback: a sensor, noise injected into the actuator, larger control effort, and the possibility of instability.

---

## 3. Suggested lecture flow (75 minutes)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | What changes in Chapter 4; open vs closed loop | §4 |
| 5–15 min | The two structures and the basic equations | §5 |
| 15–26 min | Stability: open loop cannot, feedback can; the pendulum | §6 |
| 26–38 min | Tracking; the pole-placement exercise and its hidden poles | §7 |
| 38–50 min | Regulation: disturbance against noise | §8 |
| 50–62 min | Sensitivity: the factor $1/(1+L)$ | §9 |
| 62–71 min | $S+\mathcal T=1$, sinusoids, the cost of feedback | §10 |
| 71–75 min | Closing; what PID does with this | §11 |

**Prepare as slides:** Fig. 4.1 and Fig. 4.2 side by side (leave Fig. 4.2 up for the whole lecture if you have two screens), the comparison table of §1, and the demo figures. Derive Eqs. (4.5)–(4.11) on the board once, slowly.

**If you are short of time,** compress §6.3 (feedback can destabilise) to one sentence pointing back to 3-L4, and cut the audio-amplifier calculation in §10.2. Do not compress §7.2.

### Runnable demonstrations

```
cd demos
uv run python ch4/l1_demo2_hidden_poles.py --show
uv run python ch4/l1_demo4_gain_sensitivity.py --show
```

**Run Demo 2 and Demo 4 live.** Demo 2 is the pole-placement exercise with all four closed-loop transfer functions plotted; Demo 4 puts a ±50% plant-gain error through open-loop and feedback control. Demos 1 and 3 work as slides.

### Teaching scope

Use the demos for the protected examples; the accompanying checks also work on the board. For a 75-minute session, present the protected moments of §1 and assign the remaining exercises as follow-up reading.

---

# Part I — The lecture

## 4. Opening

### Instructor script

> For four lectures we have been handed a transfer function and asked what it does. How fast, how much overshoot, does it settle at all.
>
> From today we get to add something to the system. The simplest thing we can add is a controller in front of the plant, computing the input from what we want. The next simplest is a controller that also looks at what actually happened, through a sensor.
>
> The second one is feedback. Everybody in this room already believes feedback is better. Today we find out exactly *how much* better, in which respects, and what it costs. By the end you should be able to say: "this loop gain buys this much disturbance rejection and this much insensitivity, and it passes this much sensor noise to my motor."

The book's opening assumptions, stated once: the plant and controller are **LTI** and **single-input single-output**, so everything is a scalar transfer function. The four objectives are the ones of Chapter 1: **stability, tracking, regulation, sensitivity**.

---

## 5. Two structures and the basic equations (§4.1)

### 5.1 Open loop

![Fig. 4.1 — Open-loop system](./book-figures/4-1.png)
> **[ FIG 4.1 ]** — PDF p. 3

No signal path from the output back to the control. With the disturbance at the plant input,

$$
Y_{ol}=GD_{ol}R+GW,
\tag{4.1}
$$

$$
E_{ol}=R-Y_{ol}=[1-GD_{ol}]R-GW .
\tag{4.4}
$$

The open-loop transfer function from $R$ to $Y$ is $\mathcal{T}_{ol}=GD_{ol}$. Read the second term before moving on: **the controller does not appear in the disturbance term at all.**

### 5.2 Feedback

![Fig. 4.2 — Closed-loop system with reference, disturbance and sensor noise](./book-figures/4-2.png)
> **[ FIG 4.2 ]** — PDF p. 4 *(leave this up)*

Three external inputs, each with a job:

| Input | Where it enters | What we want |
|---|---|---|
| $R$ | summing junction | the output should **track** it |
| $W$ | plant input | the output should **ignore** it (regulation) |
| $V$ | sensor | the controller should **ignore** it |

Note what the controller actually sees: $R-(Y+V)$, the *measured* error. The book's $E=R-Y$ is the *true* error, which nobody measures.

**Derivation on the board.** Write the loop once, in order:

$$
U=D_{cl}\,[R-(Y+V)],\qquad Y=G\,(U+W).
$$

Substitute the first into the second: $Y=GD_{cl}R-GD_{cl}Y-GD_{cl}V+GW$. Collect $Y$:

$$
(1+GD_{cl})\,Y=GD_{cl}R+GW-GD_{cl}V ,
$$

$$
Y_{cl}=\frac{GD_{cl}}{1+GD_{cl}}R+\frac{G}{1+GD_{cl}}W-\frac{GD_{cl}}{1+GD_{cl}}V .
\tag{4.5}
$$

For the control, substitute $Y=G(U+W)$ into the first equation and collect $U$: $(1+GD_{cl})U=D_{cl}R-GD_{cl}W-D_{cl}V$,

$$
U=\frac{D_{cl}}{1+GD_{cl}}R-\frac{GD_{cl}}{1+GD_{cl}}W-\frac{D_{cl}}{1+GD_{cl}}V .
\tag{4.6}
$$

And the error, $E=R-Y$: the $R$ coefficient is $1-\frac{GD_{cl}}{1+GD_{cl}}=\frac{1}{1+GD_{cl}}$, so

$$
E_{cl}=\frac{1}{1+GD_{cl}}R-\frac{G}{1+GD_{cl}}W+\frac{GD_{cl}}{1+GD_{cl}}V .
\tag{4.8}
$$

Every transfer function has the same denominator $1+GD_{cl}$. Name the two that keep appearing:

$$
\boxed{
S=\frac{1}{1+GD_{cl}},
\qquad
\mathcal{T}=\frac{GD_{cl}}{1+GD_{cl}}
}
\tag{4.12, 4.13}
$$

and the three equations compress to

$$
\boxed{
\begin{aligned}
Y_{cl}&=\mathcal{T}R+GSW-\mathcal{T}V\\
U&=D_{cl}SR-\mathcal{T}W-D_{cl}SV\\
E_{cl}&=SR-GSW+\mathcal{T}V
\end{aligned}}
\tag{4.9–4.11}
$$

**[beyond the book]** Only four distinct transfer functions appear: $S$, $\mathcal T$, $GS$ and $D_{cl}S$. Åström and Murray (§12.1) call them the **Gang of Four**. A design that looks good in one of them can be poor in another, and §7.2 shows that happening. **Caution for students reading AM:** AM writes $P$ and $C$ for plant and controller and swaps FPE's disturbance letters, so $v$ is AM's load disturbance and $w$ its measurement noise. AM's $PS$ and $CS$ are our $GS$ and $D_{cl}S$.

| Transfer function | From → to | Name |
|---|---|---|
| $\mathcal T=L/(1+L)$ | $R\to Y$, $V\to Y$ (with a minus sign) | complementary sensitivity |
| $S=1/(1+L)$ | $R\to E$ | sensitivity |
| $GS$ | $W\to Y$ | load sensitivity |
| $D_{cl}S$ | $R\to U$, $V\to U$ | noise sensitivity |

#### Ask the class

> The noise $V$ reaches $Y$ through $\mathcal T$, which is the *same* transfer function that makes $Y$ follow $R$. Why is that unavoidable?

Because the controller cannot tell $R-Y-V$ apart from $R-Y$. It sees one signal. Whatever it does to follow a change in $R$, it also does to follow an equal and opposite change in $V$. A sensor error *is* a reference error, as far as the loop can tell.

---

## 6. Stability (§4.1.1)

### 6.1 Open loop cannot move a pole

Write $G=b/a$ and $D_{ol}=c/d$. Then $GD_{ol}=bc/(ad)$, and the poles of Eq. (4.1) are the roots of $a(s)$ and $d(s)$. **The plant's poles are poles of the open-loop system, whatever the controller.**

The tempting fix: put a zero of $c(s)$ on the unstable root of $a(s)$. It cancels in $GD_{ol}$, but not in the $GW$ term, and not in the physical plant. The book: *"the slightest noise or disturbance will cause the output to grow until stopped by saturation or system failure."* The same applies to a RHP plant zero cancelled by a controller pole: now the controller itself is unstable.

$$
\boxed{\text{An open-loop structure cannot stabilise an unstable plant.}}
$$

**Qualification [beyond the book]:** "no roots in the RHP" in the book's sentence should be read as *no roots in the closed RHP*: as in 3-L4 §5, roots on the imaginary axis are not acceptable either.

### 6.2 Feedback can

From Eq. (4.8) the poles are the roots of $1+GD_{cl}=0$. Multiply through by $a(s)d(s)$:

$$
1+GD_{cl}=0
\quad\Longrightarrow\quad
1+\frac{b(s)c(s)}{a(s)d(s)}=0
\quad\Longrightarrow\quad
\boxed{a(s)d(s)+b(s)c(s)=0}
\tag{4.14–4.16}
$$

The controller polynomials $c$ and $d$ now enter the characteristic equation *added* to the plant's, not multiplied. That is the freedom. Two warnings survive:

- A RHP root of $a$ cancelled by a root of $c$ is a common factor of both $ad$ and $bc$, so it is a root of Eq. (4.16). **The unstable pole remains a closed-loop pole.** This is exactly the cancellation trap of 3-L4 §6.3.
- A stable cancellation is legitimate; the cancelled pole stays in the characteristic equation but it is stable.

### 6.3 The inverted pendulum, Eq. (4.17)

For simple values the pendulum of Chapter 2 is

$$
G(s)=\frac{1}{s^2-1},\qquad b=1,\quad a=(s+1)(s-1).
$$

Try a lead-type controller $D_{cl}=K\dfrac{s+\gamma}{s+\delta}$. Then Eq. (4.16) gives

$$
(s+1)(s-1)(s+\delta)+K(s+\gamma)=0 .
\tag{4.17}
$$

*"This is the problem that Maxwell faced in his study of governors"* — conditions on the parameters for all roots in the LHP — and Routh solved it (3-L4 §7). Here a shortcut works: choose $\gamma=1$. Then $(s+1)$ is a factor of both terms:

$$
(s+1)\big[(s-1)(s+\delta)+K\big]=0 .
$$

The factor $(s+1)$ is a stable closed-loop pole, so this cancellation is harmless. The bracket is a quadratic we can place anywhere.

**The book's exercise.** Force the bracket to be $s^2+2\zeta\omega_ns+\omega_n^2$. Expand: $(s-1)(s+\delta)+K=s^2+(\delta-1)s+(K-\delta)$. Match coefficients:

$$
\delta-1=2\zeta\omega_n,\qquad K-\delta=\omega_n^2
\qquad\Longrightarrow\qquad
\boxed{\delta=1+2\zeta\omega_n,\qquad K=\omega_n^2+2\zeta\omega_n+1}
$$

> **Teaching check [beyond the book]:** $\zeta=0.5$, $\omega_n=2$ gives $\delta=1+2=3$ and $K=4+2+1=7$, so $D_{cl}=7(s+1)/(s+3)$. The full characteristic polynomial is $(s+1)(s-1)(s+3)+7(s+1)=(s+1)(s^2+2s+4)$, with roots $-1$ and $-1\pm j\sqrt3=-1\pm1.732j$. Check: $s^2+2s+4$ has $\omega_n=2$ and $2\zeta\omega_n=2$, so $\zeta=0.5$ ✓. From $R$ the $(s+1)$ cancels and $\mathcal T=7/(s^2+2s+4)$, whose DC gain is $7/4=1.75$, not 1. The loop is stabilised but is not yet a good tracker, which is what PID (L2) and system type (L3) address. With $\zeta=0.5$ the overshoot is 16.3% (3-L3), so the peak is $1.163\times1.75=2.035$.

> **[ DEMO 1 ]** — `ch4/l1_demo1_pendulum_stabilise.py` *(slide)*
>
> Left: the open-loop "fix" $D_{ol}=(s-1)/(s+2)$. From $R$ alone, $GD_{ol}=1/[(s+1)(s+2)]$ settles at 0.5. Add a disturbance bias $w=0.001$ at the plant input: $Y=GW=0.001/[s(s-1)(s+1)]$, whose inverse transform is $0.001(\cosh t-1)$. That is 0.073 at 5 s and **11.0 at 10 s**. Right: feedback $D_{cl}=7(s+1)/(s+3)$ with the same bias. The disturbance contribution is $GS\,W=\dfrac{(s+3)}{(s+1)(s^2+2s+4)}\cdot\dfrac{0.001}{s}$, whose final value is $3/(1\cdot4)\times0.001=0.00075$.
>
> *Working for $\cosh$.* $\dfrac{1}{s(s-1)(s+1)}=-\dfrac1s+\dfrac{1/2}{s-1}+\dfrac{1/2}{s+1}$ by cover-up (at $s=0$: $1/(-1)$; at $s=1$: $1/(1\cdot2)$; at $s=-1$: $1/((-1)(-2))$). Inverting gives $-1+\tfrac12e^t+\tfrac12e^{-t}=\cosh t-1$. At $t=10$, $\cosh 10=11013.2$.

![Inverted pendulum: open-loop cancellation diverges under a tiny disturbance, feedback stabilises](demos/ch4/figures/l1_demo1_pendulum_stabilise.svg)

### 6.4 Feedback can also destabilise [beyond the book]

The book mentions it in passing (*"a vicious circle"*); make it concrete in one line. The plant $G=1/(s+1)^3$ is stable. Close a loop with $D_{cl}=K$:

$$
(s+1)^3+K=s^3+3s^2+3s+(1+K)=0 .
$$

The Routh $s^1$ entry is $\dfrac{3\cdot3-(1+K)}{3}=\dfrac{8-K}{3}$, so the loop is stable only for $-1<K<8$. At $K=8$, $s^3+3s^2+3s+9=(s+3)(s^2+3)$, with roots $-3$ and $\pm j\sqrt3$. Too much gain around a perfectly good plant produces oscillation. Oppenheim §11.2.6 treats this as one of the basic consequences of feedback.

---

## 7. Tracking (§4.1.2)

### 7.1 Open loop, by inversion, with three caveats

If the plant is stable with no RHP poles or zeros, an open-loop controller can in principle cancel $G$ and substitute any desired transfer function: $D_{ol}=\mathcal T_{\text{desired}}/G$. The book attaches three caveats, and each one returns later in the course:

1. **Properness.** The controller must be buildable: no more zeros than poles. Inverting a strictly proper plant is not proper, so the desired $\mathcal T$ must roll off at least as fast as $G$.
2. **Don't get greedy.** A fast $\mathcal T$ demands large inputs, and a real actuator saturates. The linear analysis stops being true at exactly that point.
3. **Sensitivity.** Cancelling a pole that is barely inside the LHP is risky: the plant drifts, the cancellation becomes imperfect, and a slow, lightly damped residue appears in the response.

#### Say out loud

> Open-loop inversion is not a silly idea. It comes back in L4 as *feedforward*, where it is combined with feedback rather than used instead of it. The three caveats are why it cannot stand alone.

### 7.2 The pole-placement exercise

The book's exercise (PDF p. 12–13): plant and controller

$$
G(s)=\frac{1}{s^2+3s+9},
\qquad
D_{cl}(s)=\frac{c_2s^2+c_1s+c_0}{s(s+d_1)} ,
$$

with the closed-loop characteristic equation required to be $(s+6)(s+3)(s^2+3s+9)=0$. This is "pole placement," which the book develops properly in Chapter 7.

Equation (4.16) with $a=s^2+3s+9$, $b=1$, $d=s(s+d_1)$, $c=c_2s^2+c_1s+c_0$:

$$
s(s+d_1)(s^2+3s+9)+c_2s^2+c_1s+c_0=(s+6)(s+3)(s^2+3s+9).
$$

**Work it smartly.** $(s+6)(s+3)=s^2+9s+18$, so the right side is $(s^2+3s+9)(s^2+9s+18)$. The left side is $(s^2+3s+9)(s^2+d_1s)+(c_2s^2+c_1s+c_0)$. Matching:

$$
d_1=9,
\qquad
c_2s^2+c_1s+c_0=18\,(s^2+3s+9)
\quad\Longrightarrow\quad
\boxed{c_2=18,\ c_1=54,\ c_0=162,\ d_1=9}
$$

which is the book's answer. Now look at what it *is*:

$$
D_{cl}(s)=\frac{18\,(s^2+3s+9)}{s(s+9)} .
$$

**The controller's zeros cancel the plant's poles exactly.** The requested characteristic polynomial contained the plant denominator, so the only way to get it was to cancel. The cancellation is stable ($s^2+3s+9$ has $\omega_n=3$, $\zeta=0.5$, roots $-1.5\pm2.598j$), so it is legal. But compute all four transfer functions:

$$
\begin{aligned}
L=GD_{cl}&=\frac{18}{s(s+9)}, &
\mathcal T&=\frac{18}{s^2+9s+18}=\frac{18}{(s+3)(s+6)},\\[4pt]
S&=\frac{s(s+9)}{(s+3)(s+6)}, &
GS&=\frac{s(s+9)}{(s+3)(s+6)(s^2+3s+9)},\\[4pt]
D_{cl}S&=\frac{18\,(s^2+3s+9)}{(s+3)(s+6)} .
\end{aligned}
$$

Check: $S+\mathcal T=\dfrac{s^2+9s+18}{(s+3)(s+6)}=1$ ✓.

- $\mathcal T$ has only the two poles we asked for: an overdamped, zero-overshoot tracker.
- $GS$ still has the plant's $\zeta=0.5$ pair. **A load disturbance excites the poles the reference cannot.**
- $D_{cl}S$ is biproper: $u(0^+)=18$ for a unit step, twice the final value $u(\infty)=1/G(0)=9$. That is caveat 2 in the flesh.

> **[ DEMO 2 ]** — `ch4/l1_demo2_hidden_poles.py` *(live, ~5 s; this is the moment of the lecture)*
>
> **Teaching check [beyond the book]:** the unit-step response through $\mathcal T$ rises to 1.0000 with no overshoot. Through $GS$, a unit step disturbance produces a bump that peaks at 0.0646 near $t=0.74$ s, undershoots to $-0.0070$, and returns to zero. The control for a unit reference step starts at $D_{cl}S(\infty)=18$, dips to 6.00 at $t=0.37$ s and settles at $D_{cl}S(0)=18\cdot9/18=9$.

![Pole-placement design: characteristic roots, output responses to r and w, and control effort](demos/ch4/figures/l1_demo2_hidden_poles.svg)

### Instructor script

> Look at the middle panel. If all you ever plotted was the step response from the reference, you'd call this a perfect design. No overshoot, no steady-state error, done.
>
> But we placed four poles and $\mathcal T$ only has two. The other two are the plant's own poles, and the controller cancelled them. They haven't gone anywhere. Push on the plant, and there they are.
>
> This is the same lesson as the cancellation trap from the stability lecture, except that this time the cancelled poles are stable, so nothing explodes. It just means one plot is never enough. There are four transfer functions in this loop and you have to look at all of them.

### 7.3 The second exercise: zero steady-state error

*"Show that if the reference input … is a step of amplitude A, the steady-state error will be zero."* From Eq. (4.11) with $W=V=0$, $E=SR$. Using the polynomials,

$$
S=\frac{1}{1+bc/(ad)}=\frac{a\,d}{a\,d+b\,c} .
$$

The controller denominator $d(s)=s(s+9)$ has a root at the origin, so $S(0)=0$. The closed loop is stable, so the Final Value Theorem applies:

$$
e_{ss}=\lim_{s\to0}s\,S(s)\frac{A}{s}=A\,S(0)=0 .
$$

With the numbers, $S(0)=0\cdot9/(3\cdot6)=0$ ✓. **An integrator in the controller makes $S$ vanish at DC.** L3 turns this observation into system type.

---

## 8. Regulation (§4.1.3)

### 8.1 Open loop is useless

Regulation: keep the error small when $R$ is at most a constant and disturbances are present. In Fig. 4.1, $D_{ol}$ is not on any path from $W$ (or from $V$, which does not even exist in an open-loop system) to $Y$. **The open-loop controller has no influence on disturbances at all.**

### 8.2 Feedback, and the dilemma

From Eq. (4.8), the two unwanted terms in the error are

$$
-\frac{G}{1+GD_{cl}}\,W
\qquad\text{and}\qquad
+\frac{GD_{cl}}{1+GD_{cl}}\,V .
$$

- To shrink the first, make $D_{cl}$ **large**: $G/(1+GD_{cl})\approx1/D_{cl}\to0$.
- But then the second tends to $1\cdot V$: **the sensor noise goes straight through.**

*"What are we to do?"* The resolution is that both are functions of frequency, and the two inputs live in different places on the frequency axis:

| Signal | Typical frequency content |
|---|---|
| plant disturbance $W$ | low; the commonest case is a **bias**, all at zero frequency |
| sensor noise $V$ | a good sensor has no bias and little low-frequency noise; its noise is at **high** frequency |

So **make $D_{cl}$ (and hence $L$) large at low frequency and small at high frequency.** Where to put the crossover from one to the other is the central decision of loop shaping (Chapter 6).

> **[ DEMO 3 ]** — `ch4/l1_demo3_regulation_tradeoff.py` *(slide)*
>
> Plant $G=1/(s+1)$, proportional $D_{cl}=K$, $r=0$, a load bias $w=1$ and sensor noise $v=0.1\sin50t$. With $r=0$, $y=GS\,w-\mathcal T v$ and $u=-\mathcal T w-D_{cl}Sv$.
>
> | $K$ | bias left in $y$: $1/(1+K)$ | $\lvert\mathcal T(j50)\rvert$ | noise amplitude in $y$ | noise amplitude in $u$ |
> |---:|---:|---:|---:|---:|
> | 1 | 0.500 | 0.020 | 0.002 | 0.100 |
> | 10 | 0.091 | 0.195 | 0.020 | 0.977 |
> | 100 | 0.0099 | 0.887 | 0.089 | 4.44 |
>
> **Teaching check [beyond the book]:** $\mathcal T=K/(s+1+K)$, so at $K=100$, $|\mathcal T(j50)|=100/|101+50j|=100/112.7=0.887$. $D_{cl}S=K(s+1)/(s+1+K)$, so $|D_{cl}S(j50)|=100\cdot|1+50j|/|101+50j|=100\cdot50.01/112.7=44.4$; times 0.1 gives 4.44. The simulation's steady-state ripple agrees to three figures. Proportional control with a pure gain cannot be large at DC and small at 50 rad/s at the same time, because a gain is the same at every frequency. That is the argument for dynamic controllers.

![Regulation trade-off: sensitivity magnitudes, output and control under bias plus sensor noise](demos/ch4/figures/l1_demo3_regulation_tradeoff.svg)

### 8.3 The bias exercise

*"Show that if $w$ is a constant bias and if $D_{cl}$ has a pole at $s=0$, then the error due to this bias will be zero. However, show that if $G$ has a pole at zero, the error due to this bias will not be zero."*

The disturbance term of the error is $-GS\,W$ with $W=w_0/s$. In polynomials,

$$
GS=\frac{b/a}{1+bc/(ad)}=\frac{b\,d}{a\,d+b\,c} .
$$

With a stable loop, $e_{ss}=-w_0\,GS(0)=-w_0\dfrac{b(0)d(0)}{a(0)d(0)+b(0)c(0)}$.

- **Integrator in the controller**, $d(0)=0$: the numerator vanishes and $e_{ss}=0$.
- **Integrator in the plant**, $a(0)=0$, controller without one ($d(0)\ne0$): $GS(0)=\dfrac{b(0)d(0)}{b(0)c(0)}=\dfrac{d(0)}{c(0)}=\dfrac{1}{D_{cl}(0)}$, so

$$
e_{ss}=-\frac{w_0}{D_{cl}(0)}\neq0 .
$$

**Qualification [beyond the book]:** the second statement assumes the controller has no integrator of its own. If both have one, $d(0)=0$ again and the error is zero. What matters is **where the integrator sits relative to where the disturbance enters**: an integrator *after* the disturbance (in $G$) cannot generate the constant control needed to cancel it. L3 formalises this as system type with respect to disturbances.

> **Teaching check [beyond the book]:** DC motor position, $G=1/[s(\tau s+1)]$, under proportional control $D_{cl}=K$ with a constant load torque $w_0$ at the input: $e_{ss}=-w_0/K$. Doubling $K$ halves the error; only an integrator in $D_{cl}$ removes it. This is the case in which the plant's own integrator removes the step-*reference* error, yet a bias *disturbance* still leaves an error.

---

## 9. Sensitivity (§4.1.4)

### 9.1 The definition

A plant designed with gain $G$ (at some frequency) turns out in service to be $G+\delta G$: a fractional change $\delta G/G$. Temperature, wear, load, a different batch of motors. How much does the overall gain $\mathcal T$ move?

$$
\boxed{
S^{\mathcal T}_{G}=\frac{\delta\mathcal T/\mathcal T}{\delta G/G}=\frac{G}{\mathcal T}\frac{\delta\mathcal T}{\delta G}
}
\tag{4.18, 4.19}
$$

"Percent change out per percent change in." The book works at zero frequency, but nothing below depends on that.

### 9.2 Open loop

$\mathcal T_{ol}=GD_{ol}$ with $D_{ol}$ fixed, so $\delta\mathcal T_{ol}=D_{ol}\,\delta G$ and

$$
\frac{\delta\mathcal T_{ol}}{\mathcal T_{ol}}=\frac{D_{ol}\,\delta G}{D_{ol}\,G}=\frac{\delta G}{G}
\qquad\Longrightarrow\qquad
S^{\mathcal T_{ol}}_{G}=1 .
\tag{4.20}
$$

A 10% plant error is a 10% error in the result. Open-loop control is exactly as accurate as the plant model.

### 9.3 Feedback

$\mathcal T_{cl}=\dfrac{GD_{cl}}{1+GD_{cl}}$. To first order $\delta\mathcal T_{cl}=\dfrac{d\mathcal T_{cl}}{dG}\delta G$, and by the quotient rule

$$
\frac{d\mathcal T_{cl}}{dG}=\frac{(1+GD_{cl})D_{cl}-D_{cl}(GD_{cl})}{(1+GD_{cl})^2}=\frac{D_{cl}}{(1+GD_{cl})^2} .
$$

Multiply by $G/\mathcal T_{cl}=G(1+GD_{cl})/(GD_{cl})=(1+GD_{cl})/D_{cl}$:

$$
\boxed{
S^{\mathcal T_{cl}}_{G}=\frac{1}{1+GD_{cl}}
}
\tag{4.21, 4.22}
$$

**This is the same $S$ as in Eq. (4.12).** The function that carries the reference into the error is also the function that measures sensitivity to the plant, which is why it gets the name.

> **Advantage of feedback (the book's box).** In feedback control, the error in the overall transfer function gain is less sensitive to variations in the plant gain by a factor of $S=1/(1+GD_{cl})$ compared with open-loop control.

With $1+GD_{cl}=100$, a 10% change in $G$ changes the steady-state gain by about $10\%/100=0.1\%$.

**Qualification [beyond the book]:** the book's box is a DC statement. At other frequencies the sensitivity is multiplied by $S(j\omega)$, and it is reduced only where $|S(j\omega)|<1$. A stable loop can amplify it: $L=4/(s+1)^3$ gives the stable closed loop $s^3+3s^2+3s+5$, yet at $\omega=\sqrt3$, $L=-1/2$ and $|S|=2$, so plant variations at that frequency are *doubled*. Part V returns to this trade-off.

**Source clarification [beyond the book]:** PDF p. 18 then says the open-loop controller is 100 times more sensitive than "the closed-loop system with loop gain of 100". The factor 100 is $1+GD_{cl}$, so the loop gain $GD_{cl}$ in the example is 99. The distinction is immaterial at this size but matters for small loop gains, where $1+L$ and $L$ differ appreciably.

Bode, who developed the theory, defined sensitivity as $1+GD_{cl}$, the reciprocal of the book's choice (footnote 2). Some older texts and data sheets use his convention.

### 9.4 Large changes [beyond the book]

The derivative gives a first-order estimate. The exact result for a change $\epsilon=\delta G/G$ of any size is

$$
\frac{\delta\mathcal T}{\mathcal T}=\frac{\epsilon\,S}{1+\mathcal T\epsilon} .
$$

*Derivation.* With $L=GD_{cl}$, the ratio of new to old gain is $\dfrac{(1+\epsilon)L/(1+L+\epsilon L)}{L/(1+L)}=\dfrac{(1+\epsilon)(1+L)}{1+L+\epsilon L}$. Subtract 1: the numerator becomes $(1+\epsilon)(1+L)-(1+L+\epsilon L)=\epsilon$, so $\delta\mathcal T/\mathcal T=\epsilon/(1+L+\epsilon L)$. Divide numerator and denominator by $1+L$ to get $\epsilon S/(1+\mathcal T\epsilon)$.

> **[ DEMO 4 ]** — `ch4/l1_demo4_gain_sensitivity.py` *(live, ~5 s)*
>
> Plant $G=A/(s+1)$, nominally $A=1$ but actually anywhere in $0.5\le A\le1.5$. Open loop: $D_{ol}=1$. Feedback: $D_{cl}=99$, so $1+GD_{cl}(0)=100$ nominally.
>
> | $A$ | $\delta G/G$ | open-loop gain | closed-loop gain $99A/(1+99A)$ | $\delta\mathcal T/\mathcal T$ | first-order $S\,\delta G/G$ |
> |---:|---:|---:|---:|---:|---:|
> | 0.5 | −50% | 0.500 | 0.98020 | −0.990% | −0.50% |
> | 0.75 | −25% | 0.750 | 0.98671 | −0.332% | −0.25% |
> | 1.0 | 0 | 1.000 | 0.99000 | 0 | 0 |
> | 1.25 | +25% | 1.250 | 0.99198 | +0.200% | +0.25% |
> | 1.5 | +50% | 1.500 | 0.99331 | +0.334% | +0.50% |
>
> **Teaching check [beyond the book]:** $\pm10\%$ gives exactly $+0.0910\%$ and $-0.1110\%$ against the first-order $\pm0.1\%$. At $A=0.5$: $\epsilon S/(1+\mathcal T\epsilon)=(-0.5)(0.01)/(1-0.495)=-0.005/0.505=-0.990\%$. The first-order estimate is optimistic by a factor of two for a 50% *loss* of plant gain, because losing gain also reduces the loop gain that is providing the protection.
>
> **Point at the right-hand panel.** The feedback loop's pole is at $-(1+99A)$, about $-100$ rad/s instead of $-1$, and its control starts at $u(0^+)=99$ instead of 1. Insensitivity and speed were both bought with loop gain, and loop gain is actuator effort.

![Plant-gain sensitivity: overall DC gain against plant gain, step responses and control effort, open loop versus feedback](demos/ch4/figures/l1_demo4_gain_sensitivity.svg)

#### Ask the class

> Feedback made the system insensitive to $G$. Is it insensitive to everything?

No. $\mathcal T=GD_{cl}/(1+GD_{cl})$ with large $L$ is approximately 1 because the output is forced to equal *what the sensor says*. A sensor-gain error of $\epsilon$ gives $y/r\to1/(1+\epsilon)$, however large the loop gain: about an equal and opposite output error for small $\epsilon$ (+10% gives −9.09%, −10% gives +11.1%). So feedback trades trust in the actuator and plant for trust in the sensor. Problem 4.2(c) asks students to discover this. This is why a precision machine is built around a precision sensor.

---

## 10. $S+\mathcal T=1$, sinusoids, and the cost of feedback

### 10.1 The fundamental identity

Define, as the book does,

$$
S\triangleq\frac{1}{1+GD_{cl}},
\qquad
\mathcal T\triangleq\frac{GD_{cl}}{1+GD_{cl}}=1-S ,
\tag{4.23, 4.24}
$$

($\mathcal T$ is "a fancy alternative name for the closed-loop transfer function"), so that

$$
\boxed{S(s)+\mathcal T(s)=1}
\tag{4.25}
$$

at every $s$, in particular at every frequency $s=j\omega$. Now reread the regulation dilemma. Disturbance rejection and tracking want $S$ small; noise rejection wants $\mathcal T$ small. **At any single frequency, both cannot be small**, since they sum to one. Feedback design is the art of deciding which one to make small at which frequency.

### 10.2 Sinusoidal inputs, Eq. (4.26)

Everything so far applies at any frequency, not just DC. With the loop stable and a sinusoidal reference at $\omega_o$, the steady-state error amplitude is

$$
|E(j\omega_o)|=|R(j\omega_o)|\,\left|\frac{1}{1+G(j\omega_o)D_{cl}(j\omega_o)}\right|=|R|\,|S(j\omega_o)| .
\tag{4.26}
$$

To hold the error to 1%, $|1+GD_{cl}|\ge100$, which is effectively $|GD_{cl}|\gtrsim100$. For a high-fidelity audio amplifier, the book asks for this over the whole audible band, $2\pi\cdot60\le\omega\le2\pi\cdot15{,}000$ rad/s.

> **Teaching check [beyond the book]:** $|L|\ge101$ guarantees $|1+L|\ge100$ by the triangle inequality, so "effectively" is justified. If the loop gain falls off like an integrator, $L=\omega_c/s$, then $|L(j\omega)|=\omega_c/\omega\ge100$ at $\omega=2\pi\cdot15{,}000$ requires $\omega_c\ge2\pi\cdot1.5\times10^6$ rad/s: a loop that is still at unity gain at **1.5 MHz**, for an audio amplifier. This is why op-amps are specified by their gain–bandwidth product. **Qualification:** the usual statement of the audible range is about 20 Hz to 20 kHz; the book's 60–15,000 Hz is a narrower working band.

**The filtered case.** With a prefilter $F(s)$ on the reference and sensor dynamics $H(s)$, the equations must be re-derived; the book defers this to online Appendix W4.1.4.1. L3 uses the sensor-dynamics version (Fig. 4.5).

### 10.3 The cost of feedback [beyond the book; AM §12.1, OWN §11.2]

The book's Review Questions 4.1 and 4.2 ask for three advantages and two disadvantages of feedback. Collect them on the board as a ledger:

| Feedback buys | Feedback costs |
|---|---|
| Stabilisation of an unstable plant (§6.3) | A **sensor**, and the output is only as good as the sensor (§9) |
| Disturbance rejection by $GS$ (§8) | **Noise injection**: $V$ reaches $Y$ through $\mathcal T$ and the actuator through $D_{cl}S$ (Demo 3) |
| Insensitivity to the plant by $S$ (§9) | **Control effort**: large loop gain means large $u$, and saturation (Demos 2, 4) |
| Tracking without an exact plant model | **Possible instability**: a stable plant can be destabilised by too much gain (§6.4) |

The control-signal entry deserves emphasis because it is invisible in an output plot. In Demo 3 at $K=100$ the output looks merely a little noisy. The motor, meanwhile, is being driven with a 4.4-amplitude sinusoid at 50 rad/s that does nothing useful and heats the windings. Åström and Murray call $D_{cl}S$ the **noise sensitivity** for this reason. At high frequency, where $L\to0$, $D_{cl}S\to D_{cl}$: whatever the controller's high-frequency gain is, the sensor noise gets multiplied by it. That is why the derivative term in L2 must be filtered.

---

## 11. Closing

### Instructor script

> Here is the bill.
>
> Open loop can track if you know the plant exactly, and it can't do anything about disturbances or instability. Feedback can do all three. But every benefit is measured by the same function, $S=1/(1+L)$, and making $S$ small at some frequency makes $\mathcal T$ nearly one there, which means the sensor noise goes straight through, and the controller hands it to the actuator multiplied by its own gain.
>
> Next lecture: the controller that almost every loop in industry actually uses. PID has three terms. The P makes $L$ big. The I makes $L$ infinite at zero frequency, which is the integrator we just saw kill the bias error in §8.3. The D adds damping, and we will have to filter it because of what we saw in Demo 3.

---

# Part II — Materials

## 12. One-board summary

```text
   THE LOOP (Fig. 4.2)          U = Dcl [R - (Y + V)],   Y = G (U + W)

     L = G Dcl     S = 1/(1+L)     T = L/(1+L)     S + T = 1

     Y = T R + G S W - T V
     U = Dcl S R - T W - Dcl S V
     E = S R - G S W + T V          (E = R - Y, the TRUE error)

   STABILITY
     open loop : poles of G stay poles.  Cannot stabilise.
     feedback  : a d + b c = 0.  Can -- but never cancel a RHP root.
     pendulum  : 1/(s^2-1), Dcl = 7(s+1)/(s+3)  ->  (s+1)(s^2+2s+4)

   TRACKING
     open loop : invert the plant -- proper? saturation? drift?
     exercise  : Dcl = 18(s^2+3s+9)/[s(s+9)]  cancels the plant poles
                 T = 18/[(s+3)(s+6)] perfect;  G S still rings at zeta 0.5

   REGULATION
     big Dcl  -> W rejected, V passed.   Resolve by FREQUENCY:
     L large at low w (bias), small at high w (sensor noise)
     integrator in Dcl -> zero error to a bias;  in G only -> -w0/Dcl(0)

   SENSITIVITY
     open loop  S = 1           feedback  S = 1/(1+L)
     1+L = 100 : 10% in G -> 0.1% in T        (exact: eps S / (1 + T eps))
     not insensitive to the SENSOR

   THE COST
     sensor, noise into u (Dcl S), control effort, possible instability
```

## 13. Discussion questions

1. The controller sees $R-Y-V$, but the book's error is $E=R-Y$. Which one do the specifications care about, and which one can the controller drive to zero?
2. In the pendulum design, the $(s+1)$ cancellation is called harmless. Under what physical change to the pendulum would it stop being harmless?
3. The pole-placement exercise *forced* a cancellation by specifying $s^2+3s+9$ as a closed-loop factor. Choose a different fourth-order target with no factor in common with $a(s)$, and predict what changes in $GS$.
4. Demo 3 shows that a pure gain cannot be large at DC and small at 50 rad/s. Sketch the magnitude of a controller that could, and say what kind of element it contains.
5. Feedback makes the output insensitive to the actuator but not to the sensor. What does that imply about where to spend money in a precision positioning stage?
6. The audio example needs loop gain 100 at 15 kHz. What would limit how far a real amplifier can push its crossover?
7. $S+\mathcal T=1$ holds at every frequency. Does that mean $|S|+|\mathcal T|=1$? Find a frequency in Demo 3 where both magnitudes are close to 1.

**Answer to 7 [beyond the book]:** No; the identity is complex. $|S|+|\mathcal T|\ge1$ by the triangle inequality, and near crossover both can exceed 0.7. In Demo 3 at $K=100$ and $\omega=100$ rad/s, $|S|=|1+100j|/|101+100j|=100.0/142.1=0.70$ and $|\mathcal T|=100/142.1=0.70$.

## 14. Homework and follow-up problems

| Problem | Topic | Why this one |
|---|---|---|
| 4.1 | Show $S+\mathcal T=1$ | The identity from first principles. |
| 4.2 | Sensitivity of three amplifier topologies (Fig. 4.30) | Part (c) shows that feedback shifts precision requirements onto the sensor. |
| 4.3 | Two structures compared for sensitivity to amplifier gain | Sensitivity as a logarithmic derivative. |
| 4.4 | Sensitivity of $A/[s(s+a)]$ to $A$, $a$ and a feedback gain $\beta$ | The frequency-dependent version; part (c) is the sensor result again. |
| 4.5 | System error with sensor dynamics (Fig. 4.5) | Bridge to the filtered case and to L3. |
| Exercises of §4.1.1–4.1.3 | Pendulum placement; pole placement; bias rejection | Worked in §6.3, §7.2–7.3 and §8.3; set the pendulum with $\zeta=0.7$, $\omega_n=3$ as a variation. |
| Review Questions 4.1, 4.2 | Advantages and disadvantages of feedback | Short answers; compare with the ledger in §10.3. |

**Suggested additional exercise [beyond the book]:** in `l1_demo3_regulation_tradeoff.py`, replace $D_{cl}=K$ with $D_{cl}=K\,a/(s+a)$ for $K=100$ and a few values of $a$. Find an $a$ that keeps the bias error near 1% while cutting the actuator noise by a factor of ten, and explain why it cannot also keep the closed-loop bandwidth at 101 rad/s.

## 15. Instructor cautions

1. **Two errors.** The book's $E$ is $R-Y$; the controller acts on $R-Y-V$. Say this when drawing Fig. 4.2, or students will be puzzled by the $+\mathcal T V$ term in Eq. (4.11).
2. **Sign conventions.** $V$ enters with a minus sign in $Y$ and $U$ and a plus sign in $E$. Derive them rather than memorising them.
3. **$\mathcal T$ versus $T$.** The book uses a script $\mathcal T$ for complementary sensitivity to avoid a clash with time constants and sampling periods. Students will write $T$; accept it, but keep $T_I$, $T_D$ (L2) visibly distinct.
4. **Cancellations again.** §6.2 and §7.2 are the second and third appearances of the cancellation lesson (after 3-L4 §6.3). The new point is that even a *stable* cancellation leaves the cancelled dynamics in $GS$.
5. **Sensitivity is not robustness to everything.** Emphasise the sensor caveat in §9; it is what Problem 4.2(c) is getting at.
6. **$|S|+|\mathcal T|\ne1$.** The identity is between complex numbers. Magnitude plots of $S$ and $\mathcal T$ do not add to one, and near crossover both can be of order one (§13, Q7).
7. **The first-order sensitivity formula underestimates large gain losses.** Demo 4's $-50\%$ row gives $-0.99\%$, not $-0.5\%$.

## 16. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l1_demo1_pendulum_stabilise.py` | §6.3 | Open-loop cancellation of the pendulum's unstable pole diverges under a 0.001 bias (11.0 at 10 s); feedback $7(s+1)/(s+3)$ holds it to 0.00075. | slide |
| 2 | `l1_demo2_hidden_poles.py` | §7.2 | The pole-placement answer cancels the plant; $\mathcal T$ is overdamped, $GS$ rings at $\zeta=0.5$, $u(0^+)=18$. | **live** |
| 3 | `l1_demo3_regulation_tradeoff.py` | §8.2, §10.3 | Raising $K$ from 1 to 100 cuts the bias error from 0.5 to 0.0099 and raises actuator noise from 0.10 to 4.44. | slide |
| 4 | `l1_demo4_gain_sensitivity.py` | §9 | A ±50% plant-gain error gives ±50% open loop and −0.99%/+0.33% with $1+L=100$; the exact formula matches. | **live** |

## 17. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| **This lecture (L1)** | **Ch. 4 intro, 4.1** | **Basic equations; stability, tracking, regulation, sensitivity; $S+\mathcal T=1$; the cost of feedback** |
| [L2](pid-control_instructor.md) | 4.3.1–4.3.5 | P, I, D, PI and PID actions |
| [L3](system-type_instructor.md) | 4.2 | Steady-state error, system type, error constants |
| [L4](pid-tuning_instructor.md) | 4.3.6, 4.4, 9.3.1 | Ziegler–Nichols tuning, feedforward, anti-windup, practical PID |
