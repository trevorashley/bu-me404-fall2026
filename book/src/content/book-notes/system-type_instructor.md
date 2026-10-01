# A First Analysis of Feedback III — Steady-State Error and System Type
## FPE 8th ed., Section 4.2

**Audience:** Fourth-year undergraduate mechanical engineering (ME 404)

**Source:** Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., §4.2 (4.2.1 and 4.2.2, with the pointer to Truxal's formula). Worked examples and figure numbers are the book's. Additions of my own are marked **[beyond the book]**.

**Prerequisites:** [The Basic Equations of Control](feedback-properties_instructor.md) (§4.1: $S$, $\mathcal T$, Eq. (4.8)) and [PID Control](pid-control_instructor.md) (§§4.3.1–4.3.5). From Chapter 3: the Final Value Theorem ([Convolution and transfer functions §11](convolution-impulse-response_instructor.md#section-11)) and Routh's criterion ([Stability and Routh’s criterion §§7–9](stability_instructor.md#section-7)).

**Course order:** this course teaches PID (FPE §4.3) *before* system type (FPE §4.2). This lecture therefore re-reads the [PID control](pid-control_instructor.md) examples in the language of type rather than previewing them.

**Duration:** two 75-minute sessions ("System Type" and "System Type (cont.)"). The split is marked in §3.

**Book figures:** figure numbers refer to the source chapter at

```text
references/documents/Franklin, Powell, Emami-Naeimi - 8th Ed./4 - A First Analysis of Feedback.pdf
```

Page cues below use the PDF viewer's 1-based page numbers (120 pages). Extracted figures are embedded from `book-figures/`. **[beyond the book]** Classroom checks and teaching prompts are instructor additions. Demo paths are relative to `demos/`; the demonstration index lists the scripts.

**Notation:**

| Symbol | Meaning |
|---|---|
| $G,\ D_c,\ H$ | plant, controller, sensor. The book writes $D_{cl}$ for the controller in §4.2.1 and $D_c$ from Eq. (4.39) on; they are the same block |
| $R,\ W,\ V$ | reference, plant disturbance, sensor noise |
| $E=R-Y$ | **system error**: reference minus output, *not* the signal entering the controller |
| $S=\dfrac{1}{1+GD_c},\ \mathcal T=\dfrac{GD_c}{1+GD_c}$ | sensitivity and complementary sensitivity ([Feedback properties](feedback-properties_instructor.md)) |
| $n$ | system type: the number of poles of the loop at $s=0$ (unity feedback), or more generally the degree read off Eq. (4.45) or (4.48) |
| $k$ | degree of the polynomial input $r(t)=t^k/k!$ |
| $K_n$ | $\lim_{s\to0}s^nGD_c(s)$; $K_p=K_0$, $K_v=K_1$, $K_a=K_2$ |
| $T_w,\ K_{n,w}$ | disturbance-to-error transfer function and its error constant |
| $k_P,\ k_I,\ k_D,\ k_t$ | proportional, integral, derivative, tachometer gains |

---

# Part 0 — Planning

## 1. Teaching strategy

[PID control](pid-control_instructor.md) showed, with pictures, that integral action removes the steady error to a step and to a constant disturbance. This lecture turns that observation into bookkeeping: **count the integrators, and you know the answer before you simulate.**

The section is algebraically light. The Final Value Theorem does all the work, and the only new objects are an integer (the type) and one constant per type. What students get wrong is not the algebra. It is the *scope* of each statement:

| Statement | True when |
|---|---|
| "Type = number of integrators in $GD_c$" | unity feedback, reference input |
| "Type 1 or higher $\Rightarrow$ zero step error" | the closed loop is stable, and (with a sensor) $H(0)=1$ |
| "Type is robust to parameter changes" | unity feedback; integrators are structural |
| "Error constants are robust" | never: $K_v$ moves with every gain in the loop |
| "The plant's integrator rejects a constant disturbance" | **false** when the disturbance enters upstream of that integrator |

So the lecture is organised around three questions: *what is being tracked or rejected, where does it enter, and what does the error actually measure?*

The framing line:

> **Steady-state error is not a matter of how hard the controller pushes. It is a matter of how many integrators stand between the error and the place the signal enters.**

Three moments to protect:

1. **§6** — Table 4.1 filled in live by Demo 1. The diagonal is the error constants; below it is zero; above it is growth.
2. **§11** — Example 4.3: the tachometer triples the damping ratio and triples the ramp error. A trade-off with numbers on it.
3. **§13** — Example 4.4: the *same* loop is Type 1 to the reference and Type 0 to a load torque. The plant's integrator does not help against a disturbance that enters before it.

---

## 2. Learning objectives

By the end of the two sessions students should be able to:

1. Explain why polynomial inputs (step, ramp, parabola) are the right test signals for steady-state accuracy, and name the "position, velocity, acceleration" convention.
2. Derive the steady-state error of a stable unity-feedback loop to $t^k/k!$ from the Final Value Theorem, Eqs. (4.28)–(4.35).
3. Define system type and the error constants $K_p$, $K_v$, $K_a$, and reproduce Table 4.1 from the single formula $e_{ss}=\lim_{s\to0}s^n/(s^n+K_n)\cdot1/s^k$.
4. Determine type and error constant for the P and PI speed-control loops (Examples 4.1, 4.2) and for the P and I loops of [PID control](pid-control_instructor.md).
5. Explain why type is robust to parameter changes in unity feedback while error constants are not.
6. Compute steady-state error with sensor dynamics from $1-\mathcal T(s)$, Eqs. (4.39)–(4.45), and explain why $H(0)=1$ matters (Example 4.3).
7. Classify a loop by type with respect to a disturbance, Eqs. (4.46)–(4.48), and identify which integrators count (Example 4.4).
8. Compute $K_v$ from closed-loop poles and zeros (Truxal's formula), and interpret $1/K_v$ as the area under the step error. **[beyond the book]**
9. Explain the cost of raising type: each added integrator makes stability harder, and must usually come with a zero.

---

## 3. Suggested lecture flow (2 × 75 minutes)

### Session 1 — System Type

| Time | Topic | Section |
|---:|---|---|
| 0–6 min | Opening: satellite tracking, elevators, and why polynomials | §4 |
| 6–20 min | The error to $t^k/k!$ by the Final Value Theorem | §5 |
| 20–40 min | Type, error constants, Table 4.1; Demo 1 live | §6 |
| 40–52 min | Examples 4.1 and 4.2: speed control with P and PI | §7 |
| 52–68 min | The PID examples re-read; robustness of type; Demo 2 | §8 |
| 68–75 min | Summary of session 1; what a sensor will break | §9 |

### Session 2 — System Type (cont.)

| Time | Topic | Section |
|---:|---|---|
| 0–5 min | Recap: one formula, one table | §10 |
| 5–25 min | Sensor dynamics, Eqs. (4.39)–(4.45); Example 4.3; Demo 3 | §11 |
| 25–40 min | Type for regulation, Eqs. (4.46)–(4.48); which integrators count | §12 |
| 40–52 min | Example 4.4: the DC motor with a load torque; Demo 4 live | §13 |
| 52–64 min | $K_v$ from the closed loop: error area and Truxal's formula; Demo 5 | §14 |
| 64–72 min | The price of type: integrators and stability | §15 |
| 72–75 min | Closing | §16 |

**Prepare as slides:** Fig. 4.3, Fig. 4.4, the reconstructed Table 4.1, Fig. 4.5, Fig. 4.6 and the Demo 1 grid. The Final Value Theorem derivation in §5 and the rule in §12.3 belong on the board.

**If you are short of time,** compress §14 to the boxed Truxal formula and the one-line area argument, and set §15 as reading. Do not compress §13: it is the one result in the section that surprises students.

### Runnable demonstrations

```
cd demos
uv run python ch4/l3_demo1_type_table.py --show
uv run python ch4/l3_demo4_disturbance_type.py --show
```

**Run Demo 1 and Demo 4 live.** Demo 1 is Table 4.1 filled in by simulation; Demo 4 is the same motor loop measured against a reference and against a load torque. Demos 2, 3 and 5 work as slides.

### Teaching scope

Use the demos for the protected examples; the accompanying checks also work on the board. Assign Truxal's formula and the Type 2 overshoot argument (§14) as follow-up reading if Session 2 runs long. Do not try to present every derivation live.

---

# Part I — Session 1: System Type

## 4. Opening: why polynomials

### Instructor script

> In [Feedback properties](feedback-properties_instructor.md) we wrote the error of a feedback loop as a sum of three terms: reference, disturbance, noise. In [PID control](pid-control_instructor.md) we watched integral action drive one of those terms to zero. Today we ask the question an engineer asks at a design review: *which signals will this loop follow with zero error, which with a fixed error, and which will it lose altogether?* And we want to answer it without running a simulation.
>
> The trick is to pick the right test signals. Real references are not steps. But over the time scale on which a loop responds, most of them look like a low-degree polynomial.

![Fig. 4.3 — Signal for satellite tracking](./book-figures/4-3.png)

> **[ FIG 4.3 ]** — PDF p. 21 *(slide)*

An antenna tracking a satellite sees an elevation angle shaped like an S. Over a stretch of a few loop time constants the middle of that S is nearly a straight line: a **ramp**. An elevator moving between floors is commanded at constant speed, again a ramp. A thermostat setpoint or a constant load is a **step**. A constant-acceleration command, a **parabola**, is rarer but real.

The book writes the family as

$$
r(t)=\frac{t^k}{k!}\,1(t)
\qquad\Longleftrightarrow\qquad
R(s)=\frac{1}{s^{k+1}},
$$

and borrows mechanical names regardless of the physical units:

| $k$ | $r(t)$ | $R(s)$ | name |
|---:|---|---|---|
| 0 | $1(t)$ | $1/s$ | position (step) |
| 1 | $t$ | $1/s^2$ | velocity (ramp) |
| 2 | $t^2/2$ | $1/s^3$ | acceleration (parabola) |

The $1/k!$ is there so that every transform is exactly $1/s^{k+1}$. The Laplace pair is $\mathcal L\{t^k\}=k!/s^{k+1}$, so dividing by $k!$ removes the factorial.

**The one assumption, stated once and enforced throughout:** the closed loop is stable. Everything below uses the Final Value Theorem. An unstable loop has no steady state, so asking about its steady-state error makes no sense. The book says this in one sentence on PDF p. 22; say it louder.

---

## 5. The error to a polynomial input (§4.2.1, Eqs. 4.27–4.35)

### 5.1 Unity feedback, reference only

![Fig. 4.2 — Closed-loop system with reference, disturbance and noise](./book-figures/4-2.png)

> **[ FIG 4.2 ]** — PDF p. 4 *(recall from [Feedback properties](feedback-properties_instructor.md))*

Set $W=V=0$ in Eq. (4.8) in [Feedback properties](feedback-properties_instructor.md). What remains is

$$
E=\frac{1}{1+GD_c}R=SR .
\tag{4.27}
$$

Apply the Final Value Theorem ([Convolution and transfer functions §11](convolution-impulse-response_instructor.md#section-11)) with $R=1/s^{k+1}$:

$$
e_{ss}=\lim_{s\to0}sE(s)=\lim_{s\to0}s\,\frac{1}{1+GD_c}\,\frac{1}{s^{k+1}} .
\tag{4.28–4.30}
$$

### 5.2 Separate the integrators from everything else

The limit depends on how $GD_c$ behaves as $s\to0$, and that is decided by how many poles it has at the origin. Pull them out:

$$
GD_c(s)=\frac{GD_{co}(s)}{s^n},
\qquad
GD_{co}(0)=K_n\ \text{finite and nonzero}.
\tag{4.33}
$$

Substitute and multiply the numerator and denominator by $s^n$:

$$
e_{ss}
=\lim_{s\to0}\frac{s}{1+GD_{co}(s)/s^n}\cdot\frac{1}{s^{k+1}}
=\lim_{s\to0}\frac{s^n}{s^n+K_n}\cdot\frac{1}{s^k}.
\tag{4.35}
$$

$$
\boxed{
e_{ss}=\lim_{s\to0}\frac{s^n}{s^n+K_n}\,\frac{1}{s^k}
=\begin{cases}
0, & n>k\\[2pt]
\dfrac{1}{1+K_0}, & n=k=0\\[6pt]
\dfrac{1}{K_n}, & n=k\ge1\\[6pt]
\infty, & n<k
\end{cases}}
$$

**Read the cases on the board, one at a time.**

- $n>k$: the numerator carries $s^{n-k}\to0$, and the denominator tends to $K_n$. Zero.
- $n=k=0$: the $s^0$ terms are 1, so the expression is $1/(1+K_0)$.
- $n=k\ge1$: the $s^n$ cancel, and the denominator $s^n+K_n\to K_n$. The error is $1/K_n$.
- $n<k$: a factor $1/s^{k-n}$ is left over. The error grows without bound.

**Qualification [beyond the book]:** in the last case the Final Value Theorem's hypothesis fails, because $sE(s)$ keeps a pole at the origin. The statement "$e_{ss}=\infty$" is shorthand for "the error grows like $t^{k-n}$". Partial fractions confirm it: the leftover $1/s^{k-n+1}$ term inverts to a polynomial of degree $k-n$ in $t$. Demo 1 shows the growth directly.

### Instructor script

> Look at what decided the answer. Not the gain. Not the time constants. One integer, $n$, compared with another integer, $k$. The gain only enters on the diagonal, where $n=k$, and there it sets the size of a constant error.
>
> That is the whole of system type. Everything else in this section is applying it carefully.

---

## 6. System type and the error constants

### 6.1 Definitions

The integer $n$ is the **type** of the system. For a unity-feedback loop and a reference input it is simply the number of poles of $GD_c$ at $s=0$, counting the controller's and the plant's together. The book defines type by what it can track: a Type $k$ system follows a polynomial of degree $k$ with a nonzero constant error.

The constants on the diagonal get names:

$$
\boxed{
K_p=\lim_{s\to0}GD_c(s),\qquad
K_v=\lim_{s\to0}sGD_c(s),\qquad
K_a=\lim_{s\to0}s^2GD_c(s)
}
\tag{4.36–4.38}
$$

the **position**, **velocity** and **acceleration** error constants. Each is finite and nonzero only for the type it belongs to. A Type 1 system has $K_p=\infty$ and $K_a=0$, which is another way of writing the first and last cases above.

**Units [beyond the book].** $K_p$ is dimensionless. $K_v$ has units of 1/s, because $1/K_v$ is the error, in output units, per unit of ramp rate (output units per second). $K_a$ has units of 1/s². Review Question 4.4 asks exactly this.

### 6.2 Table 4.1

**Source note [beyond the book]:** in the 8th-edition PDF the body of Table 4.1 on PDF p. 26 is missing; only the caption is printed. The table below follows from Eq. (4.35) and from the definitions above.

| Type | step ($k=0$) | ramp ($k=1$) | parabola ($k=2$) |
|---|:---:|:---:|:---:|
| **Type 0** | $\dfrac{1}{1+K_p}$ | $\infty$ | $\infty$ |
| **Type 1** | $0$ | $\dfrac{1}{K_v}$ | $\infty$ |
| **Type 2** | $0$ | $0$ | $\dfrac{1}{K_a}$ |

**Source correction [beyond the book]:** on PDF p. 24 the book says that for Type 0, "if the input should be a polynomial of degree higher than 1, the resulting error would grow without bound." A Type 0 loop already loses a degree-1 input, a ramp. Read "degree 1 or higher", which is what the book's own next sentence ("degree 0 is the highest degree a system of Type 0 can track at all") says.

### 6.3 Demo 1: the table, measured

Three unity-feedback loops, one of each type:

| Loop | $GD_c$ | constant | closed-loop characteristic polynomial |
|---|---|---|---|
| Type 0 | $\dfrac{4}{(s+1)(0.5s+1)}$ | $K_p=4$ | $0.5s^2+1.5s+5$, i.e. $s^2+3s+10$ |
| Type 1 | $\dfrac{2}{s(0.5s+1)}$ | $K_v=2$ | $0.5s^2+s+2$, i.e. $s^2+2s+4$ |
| Type 2 | $\dfrac{2(s+1)}{s^2(0.2s+1)}$ | $K_a=2$ | $0.2s^3+s^2+2s+2$, i.e. $s^3+5s^2+10s+10$ |

> **[ DEMO 1 ]** — `ch4/l3_demo1_type_table.py` *(live, ~5 s)*
>
> **Teaching check [beyond the book]:** Predict all nine entries before running the demo. The diagonal gives $1/(1+4)=0.2$, $1/2=0.5$ and $1/2=0.5$. Below the diagonal every entry is 0; above it every entry grows. The simulation at $t=30$ s gives exactly 0.2000, 0.5000 and 0.5000 on the diagonal. Above the diagonal it gives 6.24 for the Type 0 ramp error, which is about $t/(1+K_p)=30/5=6$ plus a constant, and 15.0 for the Type 1 parabola error, which is about $t/K_v=15$.
>
> *Stability first.* The Type 2 cubic is the only one that needs checking: Routh's $s^1$ entry is $(5\cdot10-1\cdot10)/5=8>0$, so all three loops are stable (roots $-2.651,\ -1.175\pm1.547j$). Without the zero at $-1$ the Type 2 loop would be $s^2(0.2s+1)+2=0.2s^3+s^2+2$, with no $s$ term. That polynomial is not stable for any gain; §15 comes back to this.

![Table 4.1 by simulation: error histories for Type 0, 1 and 2 loops driven by a step, a ramp and a parabola](demos/ch4/figures/l3_demo1_type_table.svg)

![Fig. 4.4 — Relationship between ramp response and K_v](./book-figures/4-4.png)

> **[ FIG 4.4 ]** — PDF p. 25 *(slide)*
>
> **Say:** "This is the Type 1 box of the table as a picture. The output runs parallel to the ramp at the same slope, a fixed distance $1/K_v$ behind. Same speed, constant lag. Reading the book's plot at $t=10$ s, $y\approx9.55$, so this system has $K_v\approx2.2$."

#### Ask the class

> A Type 1 system follows a ramp with a constant error. Why does it follow at *the same speed*?

If the output fell behind in speed, the error would grow, and the loop's integrator would respond until the speeds matched. In steady state the integrator's *input* must be constant, so that its output ramps. Distinguish the two places it can sit:

- **Plant integrator, P control** (motor position): constant error → constant $u=k_Pe$ → constant output speed. The error is $1/K_v$ per unit ramp rate, just enough for $k_Pe$ to command that speed.
- **Controller integrator** (PI on a Type 0 plant): $\dot u=k_Ie$, so a constant error makes $u$ *ramp* at a constant rate. The error is just large enough to ramp the control at the rate the plant needs.

A common student error is to say the constant error "holds the integrator's output". It holds the integrator's *input*.

---

## 7. Examples 4.1 and 4.2: speed control with P and PI

The speed-control plant of §4.1 ([Feedback properties](feedback-properties_instructor.md)) is first order,

$$
G(s)=\frac{A}{\tau s+1}.
$$

### 7.1 Example 4.1: proportional control

With $D_c=k_P$,

$$
GD_c=\frac{k_PA}{\tau s+1},
$$

which has no pole at $s=0$. So $n=0$: **Type 0**, with

$$
\boxed{K_p=\lim_{s\to0}\frac{k_PA}{\tau s+1}=k_PA}
\qquad
e_{ss,\text{step}}=\frac{1}{1+k_PA}.
$$

### 7.2 Example 4.2: proportional plus integral

With $D_c=k_P+k_I/s=(k_Ps+k_I)/s$,

$$
GD_c=\frac{A(k_Ps+k_I)}{s(\tau s+1)},
$$

with one pole at the origin: **Type 1**, and

$$
\boxed{K_v=\lim_{s\to0}s\cdot\frac{A(k_Ps+k_I)}{s(\tau s+1)}=Ak_I .}
$$

The velocity constant depends on $k_I$ only, not on $k_P$. At $s=0$ the proportional term is swamped by the integral term. **[beyond the book]**

> **Teaching check [beyond the book]:** Take a cruise-control loop with $A=1$, $\tau=10$ s. With P control, what $k_P$ gives a 2% step error? $1/(1+k_P)=0.02$ gives $k_P=49$. With PI and $k_I=0.5$, a unit-ramp speed command (constant acceleration) leaves a speed error $1/K_v=1/(Ak_I)=2$. Stability of the PI loop: the characteristic polynomial is $s(\tau s+1)+A(k_Ps+k_I)=10s^2+(1+k_P)s+k_I$. A second-order polynomial is stable when all coefficients are positive, so this loop is stable for any $k_P>-1$ and $k_I>0$.

---

## 8. The PID examples, re-read — and the robustness of type

### 8.1 Proportional control of the second-order plant

In [PID control](pid-control_instructor.md) we closed a proportional loop around FPE Eq. (4.58),

$$
G(s)=\frac{A}{s^2+a_1s+a_2},\qquad a_1=1.4,\ a_2=1,\ A=1 ,
$$

and saw in Fig. 4.7 an offset that shrank as $k_P$ rose but never vanished. In today's language: $GD_c=k_PG$ has no pole at the origin, so the loop is **Type 0** with $K_p=k_PG(0)=k_PA/a_2=k_P$:

| $k_P$ | $K_p$ | $e_{ss,\text{step}}=1/(1+K_p)$ | $y_{ss}$ |
|---:|---:|---:|---:|
| 1.5 | 1.5 | 0.4000 | 0.600 |
| 6 | 6 | 0.1429 | 0.857 |

These are the two final values in Fig. 4.7.

![Fig. 4.7 — Steady-state tracking error under proportional control](./book-figures/4-7.png)

> **[ FIG 4.7 ]** — PDF p. 38 *(recall from [PID control](pid-control_instructor.md))*

### 8.2 Integral control of the same plant

With $D_c=k_I/s$ and $k_I=0.5$ (Fig. 4.9 in [PID control](pid-control_instructor.md)), $GD_c=k_IG/s$ has one integrator: **Type 1**, with

$$
K_v=\lim_{s\to0}s\cdot\frac{k_I}{s}G(s)=k_IG(0)=0.5 .
$$

Zero step error, as Eq. (4.66) in [PID control](pid-control_instructor.md) found. The new information is the next column of the table: a unit ramp leaves an error $1/K_v=2$.

### 8.3 Type is robust; error constants are not

Now let the plant gain $A$ drift. In Demo 2, $A\in\{0.5,\ 1,\ 2\}$ with $k_P=6$ for P control and $k_I=0.5$ for I control:

| $A$ | P: $e_{ss,\text{step}}=1/(1+6A)$ | I: $e_{ss,\text{step}}$ | I: $e_{ss,\text{ramp}}=1/(k_IA)$ |
|---:|---:|---:|---:|
| 0.5 | 0.2500 | 0 | 4 |
| 1 | 0.1429 | 0 | 2 |
| 2 | 0.0769 | 0 | 1 |

> **[ DEMO 2 ]** — `ch4/l3_demo2_pid_type.py` *(slide)*
>
> **Teaching check [beyond the book]:** The zero in the middle column survives every change of $A$, because it comes from the pole of $D_c$ at $s=0$, and changing $A$ cannot move that pole. The P-control error and the I-control ramp error both move with $A$, because they are set by an error constant, and every error constant is a product of loop gains. The I loop is not stable for every $A$: its characteristic polynomial is $s^3+1.4s^2+s+k_IA$, and Routh's $s^1$ entry $(1.4\cdot1-k_IA)/1.4$ requires $k_IA<1.4$, i.e. $A<2.8$. At $A=2$ the slowest pair has real part $-0.079$, and the step response rings for tens of seconds.

![P and I control of the plant from the PID-control lecture as its gain A varies: the step error under I control stays zero, while the ramp error scales as 1/(k_I A)](demos/ch4/figures/l3_demo2_pid_type.svg)

This is what the book means on PDF p. 27:

$$
\boxed{
\begin{array}{c}
\text{In unity feedback, system type is a robust property:}\\
\text{it survives any parameter change that keeps the loop stable}\\
\text{and does not remove the integrators.}
\end{array}}
$$

Robustness of type is, in the book's words, "a major reason for preferring unity feedback over other kinds of control structure." §11 shows how a sensor can break it.

### Instructor script

> Here is the practical version. If your plant gain is uncertain by a factor of two, and it usually is, then a spec written as "zero error to a constant setpoint" is one you can *guarantee* with an integrator. A spec written as "ramp error less than 0.5" is one you can only guarantee by designing for the worst-case gain.

---

## 9. End of Session 1

### Say out loud

> Two things to take away. First, one formula: $e_{ss}=\lim s^n/(s^n+K_n)\cdot1/s^k$. The table is that formula evaluated nine times. Second, the zeros in the table come from integrators, and integrators do not care about parameter values.
>
> Next time we break both results. We put a sensor in the feedback path, and we move the input from the reference to a disturbance. The formula survives, but "count the integrators" needs more care.

**Exit question [beyond the book]:** a loop has $GD_c=\dfrac{50(s+2)}{s(s+5)(s+10)}$ and is stable. What is its error to a unit ramp? *Answer:* Type 1, $K_v=50\cdot2/(5\cdot10)=2$, so $e_{ss}=0.5$. Stability check: $s(s+5)(s+10)+50(s+2)=s^3+15s^2+100s+100$, and Routh gives $(15\cdot100-100)/15=93.3>0$.

---

# Part II — Session 2: System Type (cont.)

## 10. Recap

Write the formula and the table on the board again; they are the only things needed from Session 1. Then add the question for today:

> What if the error the controller sees is not the error we care about? And what if the signal is a disturbance rather than a reference?

---

## 11. A sensor in the loop (§4.2.1, Eqs. 4.39–4.45) {#section-11}

### 11.1 The system error is not the actuating error

![Fig. 4.5 — Closed-loop system with sensor dynamics](./book-figures/4-5.png)

> **[ FIG 4.5 ]** — PDF p. 28 *(slide)*

With a sensor $H(s)$ in the feedback path, the controller acts on $R-H(Y+V)$. That is the **actuating error**. What we care about is still the **system error** $E=R-Y$, and the two are different signals. With $W=V=0$,

$$
\frac{Y}{R}=\mathcal T(s)=\frac{GD_c}{1+GD_cH},
\tag{4.39}
$$

$$
E=R-Y=\bigl[1-\mathcal T(s)\bigr]R .
\tag{4.40–4.42}
$$

Now apply the Final Value Theorem, assuming every pole of $sE(s)$ is in the LHP, with $R=1/s^{k+1}$:

$$
\boxed{
e_{ss}=\lim_{s\to0}\frac{1-\mathcal T(s)}{s^k}
}
\tag{4.45}
$$

The loop is **Type $k$** if this limit is a nonzero constant. This definition needs no integrator counting. It works for any structure, and it reduces to Eq. (4.35) when $H=1$, because then $1-\mathcal T=S$.

**Corollary (book, PDF p. 29).** Setting $k=0$: the step error is $1-\mathcal T(0)$. So a system of Type 1 or higher has **closed-loop DC gain exactly 1**, $\mathcal T(0)=1$, and conversely. That is a useful check on any simulation.

### 11.2 Example 4.3: tachometer feedback

$$
G(s)=\frac{1}{s(\tau s+1)},\qquad D_c=k_P,\qquad H(s)=1+k_ts .
$$

The sensor adds a speed signal to the position signal, as a tachometer on the motor shaft does. First the error:

$$
E=R-\frac{D_cG}{1+HD_cG}R=\frac{1+(H-1)D_cG}{1+HD_cG}\,R .
$$

Substitute $G$, $D_c$, $H$, and multiply the numerator and denominator by $s(\tau s+1)$. Since $H-1=k_ts$,

$$
1-\mathcal T(s)=\frac{s(\tau s+1)+k_tk_Ps}{s(\tau s+1)+(1+k_ts)k_P}.
$$

Now Eq. (4.45). For $k=0$ the numerator vanishes at $s=0$ while the denominator tends to $k_P$, so $e_{ss}=0$. For $k=1$, divide the numerator by $s$:

$$
e_{ss}=\lim_{s\to0}\frac{(\tau s+1)+k_tk_P}{s(\tau s+1)+(1+k_ts)k_P}=\frac{1+k_tk_P}{k_P}.
$$

$$
\boxed{\text{Type 1},\qquad K_v=\frac{k_P}{1+k_tk_P}}
$$

With $k_t=0$ this is the unity-feedback value $K_v=k_P$. **Any positive $k_t$ lowers $K_v$.**

### 11.3 Why use a tachometer, then? Put numbers on it [beyond the book]

The closed-loop characteristic polynomial is $s(\tau s+1)+k_P(1+k_ts)=\tau s^2+(1+k_tk_P)s+k_P$. The tachometer adds to the damping term and to nothing else. With $\tau=1$ and $k_P=10$:

| $k_t$ | characteristic polynomial | $\zeta$ | overshoot | $K_v$ | ramp error |
|---:|---|---:|---:|---:|---:|
| 0 | $s^2+s+10$ | 0.158 | 60.5% | 10 | 0.1 |
| 0.2 | $s^2+3s+10$ | 0.474 | 18.4% | 3.33 | 0.3 |

Here $\omega_n=\sqrt{10}=3.162$, and $\zeta=(1+k_tk_P)/(2\omega_n)$: $1/6.325=0.158$ and $3/6.325=0.474$. The transfer function $\mathcal T=10/(s^2+(1+10k_t)s+10)$ has no zero, because $H$ sits in the feedback path. So the standard overshoot formula from [Time-domain specifications](time-domain-specs_instructor.md) applies exactly: $e^{-\pi\zeta/\sqrt{1-\zeta^2}}=0.605$ and $0.184$.

> **[ DEMO 3 ]** — `ch4/l3_demo3_tachometer.py` *(slide)*
>
> **Teaching check [beyond the book]:** Tripling $1+k_tk_P$ (from 1 to 3) triples $\zeta$ *and* triples $1/K_v$. That is the book's conclusion on PDF p. 31 — "there is a trade-off between improving stability and reducing steady-state error" — with the exchange rate written down.

**The book's closing remark, sharpened [beyond the book]: $H(0)$ must equal 1.** The tachometer term vanishes at $s=0$, so $H(0)=1$ and Type 1 survives. Now suppose the *position* sensor is miscalibrated by 2%: $H(s)=0.98(1+k_ts)$. The loop still contains the plant's integrator, but

$$
\mathcal T(0)=\frac{1}{H(0)}=\frac{1}{0.98}=1.0204,
\qquad
e_{ss,\text{step}}=1-\frac{1}{0.98}=-\frac{1}{49}=-0.0204 .
$$

The output settles 2% *above* the reference, and the ramp error drifts at $-0.0204$ per unit of ramp. By Eq. (4.45) the loop is now **Type 0**, integrator or not. Demo 3's third trace shows this.

$$
\boxed{
\text{With a sensor in the loop, the output follows }R/H(0)\text{, and the loop can only be as accurate as the sensor.}
}
$$

![Tachometer feedback: step responses and ramp errors for k_t = 0 and 0.2, and with a 2% sensor calibration error](demos/ch4/figures/l3_demo3_tachometer.svg)

#### Ask the class

> The book says type is robust "in the unity feedback structure". What did we just see that is not robust?

Type now depends on $H(0)=1$ holding exactly. That equality is a calibration, not a structural fact. An integrator in the controller guarantees that the *measured* output matches the reference; it cannot know that the measurement is wrong.

---

## 12. Type for regulation and disturbance rejection (§4.2.2)

### 12.1 The disturbance-to-error transfer function

Set $R=0$. The system error is then $E=-Y$, and

$$
\frac{E(s)}{W(s)}=-\frac{Y(s)}{W(s)}=T_w(s).
\tag{4.46}
$$

The classification copies the reference case. Pull out the zeros of $T_w$ at the origin,

$$
T_w(s)=s^nT_{o,w}(s),\qquad T_{o,w}(0)=\frac{1}{K_{n,w}},
\tag{4.47}
$$

and apply the Final Value Theorem to a disturbance $w=t^k/k!$:

$$
e_{ss}=\lim_{s\to0}\left[sT_w(s)\frac{1}{s^{k+1}}\right]=\lim_{s\to0}\left[T_{o,w}(s)\frac{s^n}{s^k}\right].
\tag{4.48}
$$

If $n>k$ the error is zero, if $n<k$ it is unbounded, and if $n=k$ the loop is **Type $k$ with respect to $W$**, with $e_{ss}=1/K_{n,w}$.

**Source correction [beyond the book]:** Eq. (4.48) on PDF p. 32 labels the left-hand side $y_{ss}$, and the sentence before Eq. (4.47) says that with zero reference "the output is the error". Since $T_w=E/W$, the limit is $e_{ss}$, and with $R=0$ the error is the *negative* of the output. The book's own Example 4.4 uses $e_{ss}$ and gets the sign right.

### 12.2 Where the type comes from [beyond the book]

For the disturbance at the plant input in Fig. 4.2,

$$
T_w=-\frac{G}{1+GD_c}.
$$

Write $G=G_o/s^{n_G}$ and $D_c=D_o/s^{n_D}$, with $G_o(0)$ and $D_o(0)$ finite and nonzero. Multiply the numerator and denominator by $s^{n_G+n_D}$:

$$
T_w=-\frac{G_o\,s^{n_D}}{s^{n_G+n_D}+G_oD_o}
\qquad\Longrightarrow\qquad
T_w\approx-\frac{s^{n_D}}{D_o(0)}\quad\text{as }s\to0\quad(n_G+n_D>0) .
$$

The approximation needs at least one integrator in the loop, so that $s^{n_G+n_D}\to0$ in the denominator. If neither block has an integrator, the $1$ survives and

$$
T_w(0)=-\frac{G_o(0)}{1+G_o(0)D_o(0)} .
$$

The loop is still Type 0 with respect to $W$. In magnitude $|T_w(0)|\,/\,|1/D_o(0)|=|L(0)/(1+L(0))|$, so for a positive DC loop gain the error is smaller than $1/D_o(0)$ suggests. It need not be otherwise: the unstable plant $G=1/(s-1)$ stabilised by $D_c=2$ gives $T_w=-1/(s+1)$ and an error of $-1$, twice $1/D_o(0)$. For $G=1/(s+1)$ and $D_c=1$, a unit-step disturbance leaves $e_{ss}=-1/2$, not $-1$.

### 12.3 The rule

$$
\boxed{
\begin{array}{c}
\text{Type with respect to the reference} = n_G+n_D \quad(\text{unity feedback})\\[4pt]
\text{Type with respect to a disturbance at the plant input} = n_D
\end{array}}
$$

and when $n_D\ge1$ the disturbance error constant is $K_{n,w}=-D_o(0)$, a property of the controller alone. The general statement: **only integrators between the error signal and the point where the disturbance enters count.** Integrators downstream of the disturbance see the disturbance as just another input to integrate.

This is the answer to the exercise on PDF p. 14 discussed in [Feedback properties](feedback-properties_instructor.md) ("if $w$ is a constant bias and $D_c$ has a pole at $s=0$, the error due to this bias will be zero; ... if $G$ has a pole at zero, the error due to this bias will not be zero"), and to Review Question 4.7.

---

## 13. Example 4.4: a DC motor with a load torque

![Fig. 4.6 — DC motor with unity feedback](./book-figures/4-6.png)

> **[ FIG 4.6 ]** — PDF p. 33 *(slide)*

The motor is $A/[s(\tau s+1)]$. The load torque enters at the plant input through $B/A$. The feedback is drawn as a $-1.0$ block into a $(+,+)$ summer, which is ordinary negative unity feedback.

Close the loop with $R=0$: the plant input is $D_c(-Y)+(B/A)W$, so

$$
Y=\frac{A}{s(\tau s+1)}\Bigl[-D_cY+\tfrac{B}{A}W\Bigr]
\quad\Longrightarrow\quad
\frac{Y}{W}=\frac{B}{s(\tau s+1)+AD_c},
\qquad
T_w=-\frac{B}{s(\tau s+1)+AD_c}.
$$

### 13.1 (a) Proportional control, $D_c=k_P$

$$
T_w=-\frac{B}{s(\tau s+1)+Ak_P}=s^0T_{o,w},
\qquad
K_{0,w}=-\frac{Ak_P}{B}.
$$

**Type 0 to the disturbance.** A unit-step torque leaves

$$
\boxed{e_{ss}=-\frac{B}{Ak_P}}
$$

Yet the *same loop* is Type 1 to the reference, since $GD_c=Ak_P/[s(\tau s+1)]$ has the motor's integrator, with $K_v=Ak_P$. **System type depends on which input you ask about.**

### 13.2 (b) PI control, $D_c=k_P+k_I/s$

Multiply the denominator through by $s$:

$$
T_w=-\frac{Bs}{s^2(\tau s+1)+(k_Ps+k_I)A},
\qquad n=1,
\qquad K_{1,w}=-\frac{Ak_I}{B}.
\tag{4.51–4.53}
$$

**Type 1 to the disturbance.** A step torque leaves no error, and a unit-ramp torque leaves

$$
\boxed{e_{ss}=-\frac{B}{Ak_I}}
\tag{4.54}
$$

Both constants agree with §12.3. For (a), $n_D=0$; for (b), $n_D=1$ and $K_{1,w}=-(B/A)^{-1}k_I$, where the $B/A$ is the gain of the disturbance path.

### 13.3 Numbers [beyond the book]

Take $A=2$, $B=1$, $\tau=0.5$, $k_P=2$, $k_I=1$.

| | (a) P | (b) PI |
|---|---|---|
| characteristic polynomial | $0.5s^2+s+4$ | $0.5s^3+s^2+4s+2$ |
| closed-loop poles | $-1\pm2.646j$ | $-0.556,\ -0.722\pm2.584j$ |
| type to $R$ | 1, $K_v=Ak_P=4$ | 2, $K_a=Ak_I=2$ |
| type to $W$ | 0 | 1 |
| unit-step torque | $e_{ss}=-B/(Ak_P)=-0.25$ | $0$ |
| unit-ramp torque | grows | $e_{ss}=-B/(Ak_I)=-0.5$ |

Stability of (b) by Routh: $s^3$ row $0.5,\ 4$; $s^2$ row $1,\ 2$; $s^1$ entry $(1\cdot4-0.5\cdot2)/1=3>0$; $s^0$ entry $2$. No sign changes.

> **[ DEMO 4 ]** — `ch4/l3_demo4_disturbance_type.py` *(live, ~5 s)*
>
> **Teaching check [beyond the book]:** Ask for the step-torque error before running it: $-1/(2\cdot2)=-0.25$ under P control, and zero under PI. The simulation gives $-0.2500$ and $0.0000$. Physically, under P control the shaft must be displaced by 0.25 so that the proportional term $k_P\cdot0.25=0.5$ produces a control that cancels the torque's contribution $(B/A)\cdot1=0.5$ at the plant input. Under PI control the integrator builds up that 0.5 by itself, and the error can return to zero.

![Example 4.4: a step and a ramp load torque on the DC motor under P and PI control](demos/ch4/figures/l3_demo4_disturbance_type.svg)

### Instructor script

> This is the example I want you to remember from this section. The motor has an integrator: shaft angle is the integral of speed. So the position loop tracks a step reference perfectly with nothing but a proportional gain. Then someone leans on the shaft, and it stays leaned on.
>
> The motor's integrator integrates the *torque*, disturbance included. It sits on the wrong side of the disturbance to reject it. To reject a constant torque, the integrator has to be in the controller.

---

## 14. $K_v$ from the closed loop: error area and Truxal's formula [beyond the book]

The book mentions Truxal's formula (PDF p. 35) and sends readers to Appendix W4.2.2.1. Both results below follow in a few lines from Eq. (4.45), and both are worth having.

### 14.1 $1/K_v$ is the area under the step error

For a stable loop with $\mathcal T(0)=1$, the step error has transform $E(s)=[1-\mathcal T(s)]/s$. The total area under a decaying signal equals its transform at $s=0$, since $\int_0^\infty e\,dt=\lim_{s\to0}\int_0^\infty e(t)e^{-st}\,dt$. So

$$
\boxed{
\int_0^\infty e_{\text{step}}(t)\,dt=\lim_{s\to0}\frac{1-\mathcal T(s)}{s}=\frac{1}{K_v}
}
$$

This is Eq. (4.45) with $k=1$. For a Type 1 loop, the area between the reference step and the response equals the error to a unit ramp. Fig. 4.4 and the step response are two views of the same number.

**For Type 2, $1/K_v=0$, so the net area is zero.** The step error starts at $e(0^+)=1$ for any strictly proper loop, so it must go *negative* somewhere to cancel that positive area. That is, **the step response of a stable Type 2 system always overshoots.** This is FPE Problem 4.28, proved in two lines.

### 14.2 Truxal's formula

Near $s=0$ a Type 1 loop has $1-\mathcal T(s)\approx s/K_v$, so $\mathcal T'(0)=-1/K_v$ and $\mathcal T(0)=1$. Take the logarithmic derivative of $\mathcal T(s)=K\prod(s-z_j)/\prod(s-p_i)$ at $s=0$:

$$
\frac{\mathcal T'(0)}{\mathcal T(0)}=\sum_j\frac{1}{0-z_j}-\sum_i\frac{1}{0-p_i}
\quad\Longrightarrow\quad
\boxed{
\frac{1}{K_v}=\sum_i\frac{1}{-p_i}-\sum_j\frac{1}{-z_j}
}
$$

Here $p_i$ and $z_j$ are the **closed-loop** poles and zeros. Two consequences:

- $\sum_i 1/(-p_i)=a_{n-1}/a_n$, the ratio of the last two coefficients of the closed-loop denominator. You never need the poles themselves.
- A slow closed-loop pole contributes a large term. A closed-loop zero close to it nearly cancels that term, but not exactly.

> **[ DEMO 5 ]** — `ch4/l3_demo5_error_area.py` *(slide)*
>
> **Teaching check [beyond the book]:** Take the PI loop of Ch. 3 Example 3.34 at $K=10$, $K_I=5$ ([Stability and Routh’s criterion §9](stability_instructor.md#section-9)). Directly, $K_v=\lim_{s\to0}s\cdot\dfrac{10s+5}{s(s+1)(s+2)}=5/2=2.5$. By Truxal, the closed-loop denominator $s^3+3s^2+12s+5$ gives $\sum1/(-p_i)=12/5=2.4$, and the zero at $-0.5$ gives $1/0.5=2$. So $1/K_v=2.4-2.0=0.4$ and $K_v=2.5$ ✓. Individually, the slow pole at $-0.462$ contributes $2.166$, and it sits next to the zero. This near-cancelling pair barely shows in the step response, yet it carries $0.166$ of the $0.400$. For the Type 1 loop of Demo 1, $s^2+2s+4$ gives $2/4=0.5=1/K_v$ ✓. For the Type 2 loop, $s^3+5s^2+10s+10$ gives $10/10=1$ and the zero at $-1$ gives 1, so $1/K_v=0$ ✓. Its measured step-error area is $0.0000$, with a minimum error of $-0.375$: 37.5% overshoot.

![Step-error area equals 1/K_v; the Type 2 error must cross zero; Truxal's pole-zero contributions for the Example 3.34 PI loop](demos/ch4/figures/l3_demo5_error_area.svg)

**Why this matters later.** The closed-loop dipole near the origin is the mechanism behind lag compensation in Chapter 5: a slow pole-zero pair that changes the low-frequency gain, and hence the error constant, while leaving the transient nearly unchanged.

---

## 15. The price of type [beyond the book]

Each integrator raises the type by one. It also adds a pole at the origin to the loop, and Routh's criterion shows the cost.

**Pure integral control on a plant that already has an integrator.** With $G=1/[s(s+1)]$ and $D_c=k_I/s$, the characteristic polynomial is

$$
s^2(s+1)+k_I=s^3+s^2+0\cdot s+k_I .
$$

The coefficient of $s$ is missing, so the loop is unstable for **every** $k_I>0$, by the necessary condition of [Stability and Routh’s criterion §7.1](stability_instructor.md#section-7-1). At $k_I=1$ the roots are $-1.466$ and $+0.233\pm0.793j$.

**Add a zero: PI control.** With $D_c=(k_Ps+k_I)/s$,

$$
s^3+s^2+k_Ps+k_I=0,
\qquad
s^1\text{ entry: }\frac{1\cdot k_P-1\cdot k_I}{1}=k_P-k_I ,
$$

so the loop is stable iff $k_P>k_I>0$. It is then Type 2 with $K_a=k_I$. At the boundary $k_P=k_I=1$ the polynomial factors as $(s+1)(s^2+1)$, a neutral pair at $\pm j$. At $k_P=2$, $k_I=1$ the roots are $-0.570$ and $-0.215\pm1.307j$: stable, but only lightly damped.

$$
\boxed{
\text{Each integrator adds an order of accuracy and takes away stability margin.
The zero that comes with it in PI (or with the }(s+1)\text{ in Demo 1's Type 2 loop) buys the margin back.}
}
$$

This is the same trade as Example 4.3, from the other side: there damping cost accuracy; here accuracy costs damping.

---

## 16. Closing

### Closing script

> Here is what the section gave us.
>
> One formula: the Final Value Theorem applied to $E=[1-\mathcal T]R$. For unity feedback it reduces to counting integrators, and the table falls out of it.
>
> One robustness result: integrators are structural, so type survives parameter changes. Error constants do not.
>
> Two warnings. With a sensor in the loop, type depends on $H(0)=1$, which is a calibration. And for a disturbance, only the integrators upstream of where it enters count, which is why a motor position loop needs integral action in the controller even though the motor already integrates.
>
> And a price: every integrator makes stability harder, and needs a zero to pay for it.
>
> In [PID tuning and implementation](pid-tuning_instructor.md) we put numbers on the three PID gains using tuning rules, and deal with what happens to an integrator when the actuator saturates.

---

# Part III — Materials

## 17. One-board summary

```text
   THE FORMULA  (stable loop, input t^k/k!, R = 1/s^(k+1))

     unity feedback:    e_ss = lim  s^n / (s^n + K_n) * 1/s^k      n = integrators in G D_c
     any structure:     e_ss = lim  [1 - T(s)] / s^k               E = R - Y (system error)
     disturbance:       e_ss = lim  T_w(s) / s^k,   T_w = E/W       type = zeros of T_w at 0

   THE TABLE                step        ramp        parabola
     Type 0              1/(1+K_p)      inf          inf
     Type 1                  0          1/K_v        inf
     Type 2                  0           0          1/K_a

     K_p = lim G D_c     K_v = lim s G D_c     K_a = lim s^2 G D_c

   ROBUST?
     type             yes (unity feedback): integrators are structural
     error constants  no: products of loop gains
     with sensor H    only if H(0) = 1 exactly  -> output follows R/H(0)

   WHICH INTEGRATORS COUNT
     reference                      n_G + n_D
     disturbance at plant input     n_D only (upstream of the entry point)
     DC motor, P control:  Type 1 to R, Type 0 to a load torque

   EXAMPLES
     4.1  P,  A/(tau s+1)          Type 0, K_p = k_P A
     4.2  PI, A/(tau s+1)          Type 1, K_v = A k_I
     4.3  tach H = 1 + k_t s       Type 1, K_v = k_P/(1 + k_t k_P)   damping up, K_v down
     4.4  motor, load torque       P: e_ss = -B/(A k_P)   PI: ramp e_ss = -B/(A k_I)

   BEYOND THE BOOK
     area under step error = 1/K_v ;  Type 2 => net area 0 => must overshoot
     Truxal:  1/K_v = sum 1/(-p_i) - sum 1/(-z_j),   sum 1/(-p_i) = a_(n-1)/a_n
     each integrator costs stability; the PI zero buys it back
```

## 18. Discussion questions

1. A temperature controller has zero steady-state error to a constant setpoint (Review Question 4.3). What does that tell you about its type, and what does it *not* tell you about its response to a slowly rising setpoint?
2. Fig. 4.3 is an S-curve, not a ramp. Over what time window is a ramp model of it justified, and what does the loop do near the ends of the S?
3. Why is it acceptable to say "$e_{ss}=\infty$" for a Type 0 loop tracking a ramp, when the Final Value Theorem's hypothesis fails? What is the precise statement?
4. The tachometer in Example 4.3 improves damping at the cost of $K_v$. Propose a controller that improves damping *without* lowering $K_v$, and say what it costs instead.
5. Your position sensor has a 0.5% gain error. An integrator in the controller does not remove the resulting output error. Why not, and what would?
6. In Example 4.4, where would you have to put an integrator to reject a ramp load torque, and what does §15 say that would cost?
7. Truxal's formula says a slow closed-loop pole contributes heavily to $1/K_v$. Why, physically, does a slow mode make the ramp error large?
8. Give a mechanical system in which a disturbance enters *downstream* of the controller's integrator but upstream of the plant's. Which type does it see?

## 19. Homework and follow-up problems

| Problem | Topic | Why this one |
|---|---|---|
| Review Questions 4.4–4.7 | Units of error constants; type for reference and for disturbance | Short answers; check vocabulary. |
| 4.6 | DC motor with tachometer feedback | Example 4.3 in a different block-diagram arrangement. |
| 4.8 | Fig. 4.5 with numbers: tracking error, type, error coefficient | Eq. (4.45) with a sensor. |
| 4.9 | Non-unity feedback: what must $H$ satisfy to keep Type 1? | The $H(0)=1$ condition, derived in general. |
| 4.12, 4.13 | Type and constants from a closed-loop transfer function; stable *and* Type 1 | Links type to Routh. |
| 4.15 | Satellite attitude: type to reference and to disturbance torque | The Example 4.4 lesson on a double integrator. |
| 4.17 | Three disturbance entry points, three types | The rule of §12.3 in general form. |
| 4.19, 4.21 | Type obtained by parameter matching is not robust | The counterpoint to §8.3. |
| 4.28 | A Type 2 step response must overshoot | Two lines with the area argument of §14.1. |

**Suggested additional exercise [beyond the book]:** extend `l3_demo5_error_area.py` to a Type 1 loop with a slow closed-loop dipole whose zero lies *closer* to the origin than its pole. Predict from Truxal's formula whether $K_v$ rises or falls, then check.

## 20. Instructor cautions

1. **Stability before type.** Every error formula assumes a stable closed loop. Make students state the stability check before every error calculation, even when it is one line of Routh.
2. **System error versus actuating error.** With a sensor, the controller's input $R-HY$ is not $E=R-Y$. Students who compute error constants from $GD_cH$ get Example 4.3 wrong.
3. **"Count the integrators" is a unity-feedback, reference-input rule.** For disturbances, only controller integrators upstream of the entry point count. Example 4.4 is the counterexample; use it.
4. **$K_v$ depends on $k_I$, not $k_P$, in a PI loop around a Type 0 plant.** Students often multiply in $k_P$ as well.
5. **Table 4.1 is missing from the PDF.** Students reading the e-text will find an empty table; give them the reconstructed one (§6.2).
6. **Sign of the disturbance error.** With $R=0$, $E=-Y$. The book's Eq. (4.48) labels the result $y_{ss}$; the worked example correctly gets $e_{ss}=-B/(Ak_P)$.
7. **Type is robust, but only to changes that keep the loop stable.** §8.3's Demo 2 shows the I loop approaching instability at $A=2$, and failing beyond $A=2.8$.

## 21. Demonstration index

| # | Script | Section | What it settles | Use |
|---|---|---|---|---|
| 1 | `l3_demo1_type_table.py` | §6.3 | Table 4.1 measured: nine error histories against the formula; the diagonal matches to four decimals. | **live** |
| 2 | `l3_demo2_pid_type.py` | §8 | The plant from [PID control](pid-control_instructor.md) under P and I control as its gain varies by 4×: the I-control step error stays zero while every error constant moves. | slide |
| 3 | `l3_demo3_tachometer.py` | §11 | Example 4.3: $\zeta$ from 0.158 to 0.474 and $1/K_v$ from 0.1 to 0.3; a 2% sensor gain error turns the loop Type 0. | slide |
| 4 | `l3_demo4_disturbance_type.py` | §13 | Example 4.4: step and ramp load torque under P and PI; Type 1 to the reference, Type 0 to the torque. | **live** |
| 5 | `l3_demo5_error_area.py` | §14 | $1/K_v$ three ways: $\lim sGD_c$, Truxal, and step-error area; the Type 2 error crosses zero. | slide |

## 22. Where this lecture sits

| Lecture | Book sections | Content |
|---|---|---|
| [Feedback properties](feedback-properties_instructor.md) | 4.1 | The basic equations of control: stability, tracking, regulation, sensitivity; $S$ and $\mathcal T$ |
| [PID control](pid-control_instructor.md) | 4.3.1–4.3.5 | P, I, D, PI and PID actions and their effect on response |
| **This lecture** | **4.2** | **Steady-state error to polynomial inputs; system type for tracking and for disturbance rejection** |
| [PID tuning and implementation](pid-tuning_instructor.md) | 4.3.6, 4.4, 9.3.1 | Ziegler–Nichols tuning, feedforward, integrator anti-windup, physical realisation |
| Next | Chapter 5 | Root locus: moving the poles with a gain, and lag compensation for error constants |
