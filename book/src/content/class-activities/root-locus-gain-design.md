# Root Locus: Read, Predict, and Check

**ME404 pair activity · November 10, 2026 · 105 minutes**

How much can one adjustable gain accomplish? Predict the closed-loop behavior by hand, compare reasoning with your partner, and use MATLAB to test your predictions after each round.

## How we will work

Use paper, a calculator, and this page. Keep MATLAB closed during each hand-work interval. One partner draws and records; the other checks signs, angles, and assumptions. Switch roles each round. Prepare one shared sketch or calculation and one sentence explaining what it means physically. Attempt the current round only; reconvene before moving on.

| Elapsed time | Task |
|---|---|
| 0–5 min | Form pairs; review the toolkit below |
| 5–20 min | 1. A zero changes the double-integrator locus |
| 20–35 min | 2. An added pole changes it again |
| 35–50 min | 3. Flexible modes and sensor location |
| 50–65 min | 4. Multiple roots away from the real axis |
| 65–80 min | 5. Can motor gain meet the target? |
| 80–95 min | 6. Select a cubic gain; check the whole design |
| 95–105 min | Synthesis and exit questions |

Each 15-minute round consists of **10 minutes working in pairs**, then **5 minutes comparing solutions and checking with MATLAB**. Finish the numbered tasks first. The labeled stretch tasks are optional; they are not needed to start the next round.

By the end, you should be able to predict how a zero, a pole, or a flexible mode changes a locus; find repeated roots; select a gain for a damping ratio; and distinguish pole placement from verified response and tracking performance.

## Common assumptions and hand-work toolkit

Use linear, continuous-time models, negative unity feedback, normalized signals, and zero initial conditions for forced responses. Time is in seconds, and pole coordinates are in $\mathrm{s}^{-1}$. For every locus, **$K\geq0$ varies and all other parameters stay fixed**. A controller parameter $p>0$ places its pole at $-p$. At $K=0$, inspect the characteristic polynomial before cancellation; zero gain is a locus endpoint, not an asymptotically stable operating choice for these integrator plants.

Write the loop as $L=KL_0=KB/A$, with gain excluded from $L_0$. Here $A$ and $B$ have no common factors, and the leading coefficient of $L_0$ is positive. Then

$$
P(s)=A(s)+KB(s)=0,\qquad
\mathcal T(s)=\frac{Y(s)}{R(s)}=\frac{KB(s)}{A(s)+KB(s)}.
$$

For a point away from poles and zeros, the positive-gain locus requires

$$
\arg L_0(s)=(2\ell+1)180^\circ,\qquad
K=\frac1{|L_0(s)|},\qquad \ell\in\mathbb Z.
$$

Use these construction rules:

1. There are $n$ branches starting at the $n$ open-loop poles, counted with multiplicity. They end at the $m$ finite zeros and at infinity. Real coefficients give conjugate symmetry.
2. A real point is on the locus when an odd number of real poles and zeros lies to its right, counting multiplicity.
3. When $n>m$, the $n-m$ asymptotes have centroid and angles
   $$
   \sigma_a=\frac{\sum p_i-\sum z_i}{n-m},\qquad
   \theta_\ell=\frac{(2\ell+1)180^\circ}{n-m},\quad \ell=0,\ldots,n-m-1.
   $$
4. At a **simple** pole $p_i$, the departure angle is
   $$
   \phi_{\rm dep}=180^\circ+\sum_j\arg(p_i-z_j)
   -\sum_{k\ne i}\arg(p_i-p_k)\pmod{360^\circ}.
   $$
   Measure each vector from the other pole or zero **to** $p_i$. Use the correct quadrant: $\arg(x+jy)=\operatorname{atan2}(y,x)$. At a repeated open-loop pole, use the local characteristic equation instead of the simple-pole formula.
5. A closed-loop multiple root satisfies $P=0$ and $\partial P/\partial s=0$. Where $B(s)\ne0$, equivalently solve $dK(s)/ds=0$ for $K(s)=-A/B$, then retain only points with real, nonnegative gain on the locus. Substitute back into $P$ to check the gain and multiplicity. A generic double-root event at $K>0$ has perpendicular arrival and departure directions; a triple root needs its own local analysis.

For an upper left-half-plane pole $s=-\sigma+j\omega_d$, with $\sigma>0$,

$$
\omega_n=\sqrt{\sigma^2+\omega_d^2},\qquad
\zeta=\frac{\sigma}{\omega_n}.
$$

A damping-ratio ray makes angle $\cos^{-1}\zeta$ with the **negative** real axis. For the standard second-order transfer function **without finite zeros**,

$$
\mathcal T_2(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_ns+\omega_n^2},\qquad
M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}},\quad 0<\zeta<1.
$$

$M_p$ is fractional overshoot; multiply by 100 for percent overshoot. Useful design estimates are

$$
t_s\approx\frac{4.6}{\sigma}\quad\text{(1\% band)},\qquad
t_r\approx\frac{1.8}{\omega_n}\quad\text{(10–90\% rise, moderate damping)}.
$$

These are estimates, not guarantees for a complete system with other poles or zeros. Settling means the **last entry into a $\pm1\%$ band about the final value**. MATLAB's default settling band is 2%, so explicitly request 1%.

For a stable Type 1 unity-feedback loop (one uncanceled integrator),

$$
K_v=\lim_{s\to0}sL(s),\qquad
e_{ss,\rm step}=0,\qquad e_{ss,\rm ramp}=\frac1{K_v}
$$

for a unit step and a unit-slope ramp. Check stability before applying final-value formulas. For a cubic $s^3+a_2s^2+a_1s+a_0$, the Routh first column is

$$
1,\quad a_2,\quad\frac{a_2a_1-a_0}{a_2},\quad a_0.
$$

All entries must be positive for asymptotic stability.

## 1. Can a controller zero supply damping?

A normalized rigid satellite or frictionless joint has $G(s)=1/s^2$. Compare proportional control $D_c=K$ with PD control $D_c=K(s+1)$. The proportional and derivative coefficients have the same numerical value in this normalized model; their physical units differ. Both terms act on the tracking error $e=r-y$, so $u=K e+K\dot e$. This placement matters for the reference-step response. Treat ideal differentiation as a model; Round 2 adds a pole to make the controller proper.

1. Write both characteristic polynomials. Find the proportional-control poles and sketch their locus. Does any $K>0$ make errors decay?
2. For PD control, identify the starts, endpoints, real-axis portion, and departure directions from the double pole at zero. Find where two roots meet on the real axis and the corresponding gain. Complete a qualitative sketch with arrows for increasing $K$.
3. Match the PD denominator to the second-order form. Find a gain giving $\zeta=1/2$, and report both poles. Would the standard second-order overshoot formula necessarily give the actual PD overshoot? Explain before simulating.

**Stretch:** For a complex pole $s=x+jy$, separate real and imaginary parts of the PD polynomial. Prove that its curved locus is a circle, and find its center and radius.

**During the MATLAB check:** Plot both loci. At your PD gain, compare the complete step response with the standard second-order model having the same denominator and unit DC gain. What changed even though the poles did not?

## 2. What does an added controller pole cost?

Replace ideal PD with a lead controller:

$$
G(s)=\frac1{s^2},\qquad
D_c(s)=K\frac{s+1}{s+p},\qquad p\in\{12,9,4\}.
$$

1. Write $P(s)$ and $K(s)$. For a fixed $p>1$, identify the branch starts, finite endpoint, real-axis segment, and asymptote centroid and angles.
2. Find the real-axis multiple-root candidates for $p=12$, $9$, and $4$. If needed, use the scaffold: apart from the starting point $s=0$, the stationary-gain equation reduces to
   $$
   2s^2+(p+3)s+2p=0.
   $$
   For $p=12$, calculate the two candidate gains and decide which event is break-in and which is breakaway.
3. At $p=9$, find the gain at the repeated point and factor the entire characteristic polynomial. How many roots coincide? Contrast the three qualitative locus shapes.

**Stretch:** Use the discriminant of the stationary-gain equation to explain why the transition occurs at $p=9$ for $p>1$. Use the cubic Routh column to determine whether the three controllers are stable for all $K>0$.

**During the MATLAB check:** Compare all three loci on equal axis scales. Follow the roots as $p$ changes from 12 through 9 to 4. This repeats the comparison in FPE Example 5.7 without requiring an interactive controller-design tool. Why can moving a controller pole closer to the zero reduce the damping that was available with PD?

Compare locus **shapes** first. For $|s|\ll p$, $D_c(s)\approx(K/p)(s+1)$, so the same numerical $K$ in Rounds 1 and 2 does not give the same effective PD gain.

## 3. Can sensor location change the stability risk?

Flexibility adds a lightly damped mode. Compare these two supplied plants, each with $D_c=K(s+1)/(s+12)$:

$$
G_c(s)=\frac{(s+0.1)^2+6^2}{s^2[(s+0.1)^2+6.6^2]},\qquad
G_n(s)=\frac1{s^2[(s+0.1)^2+6.6^2]}.
$$

Here $c$ denotes a **collocated** sensor and actuator on the same rigid body; $n$ denotes a **noncollocated** sensor across the flexibility. These illustrative models show the effect of nearby zeros; they are not a universal model of every sensor placement. Their low-frequency gains also differ: $G_c/G_n\to36.01$ as $s\to0$. Equal numerical controller gains therefore do not give equal low-frequency loop gains. A positive constant rescaling changes the gain labels on a locus, but not its shape or departure directions.

Both loops have poles $0,0,-12,-0.1\pm6.6j$. The collocated loop has zeros $-1,-0.1\pm6j$; the noncollocated loop has only the zero at $-1$.

1. Find the branch count, number of infinite endpoints, real-axis portion, and asymptotes for each loop.
2. Calculate the departure direction from $p_f=-0.1+6.6j$ in each case. Share the arithmetic: one partner adds the zero angles and the other adds the other-pole angles. Count the origin twice. State whether each branch initially moves left or right.
3. Draw a small local sketch around $p_f$ and its conjugate. Does a departure toward the right prove instability for every $K>0$? What must MATLAB check before a gain is accepted?

**During the MATLAB check:** Plot both loci, zoom near the flexible poles, and inspect **all five** closed-loop poles at $K=100$ and $200$. Compare the noncollocated case's change in stability. A rigid-body model would omit which evidence?

## 4. Can two roots meet off the real axis?

Consider

$$
L_0(s)=\frac1{s(s+2)[(s+1)^2+4]},\qquad L=KL_0.
$$

1. Mark the starting poles and real-axis segment; find the asymptotes. Calculate the departure angle from $-1+2j$.
2. Set $q=(s+1)^2$. Show that the characteristic equation becomes $q^2+3q-4+K=0$. Find all positive-gain repeated-root events using $P=0$ and
   $$
   \frac{\partial P}{\partial s}=2(s+1)(2q+3)=0.
   $$
   At each event, report the gain, root locations, and multiplicities.
3. Use the quadratic formula in $q$ to explain the sequence: roots meet on the real axis, move vertically, meet the branches from the original complex poles, and then depart horizontally before curving toward the asymptotes. Sketch that sequence with increasing-gain arrows. Horizontal departure is a local tangent, not an entire straight branch.

**Stretch:** At the complex repeated-root gain, factor $P(s)$ into a squared quadratic. Does a complex repeated root have to be a triple root?

**During the MATLAB check:** Plot the locus and mark all roots at each gain you found. Small numerical splitting of a repeated root is expected; use your exact factorization to interpret it.

## 5. Can motor gain meet the target?

A normalized motor-position plant is $G(s)=1/[s(s+1)]$, with proportional controller $D_c=K$.

1. Derive $\mathcal T(s)$, its poles, $\omega_n$, and $\zeta$. Sketch the locus, including the breakaway gain. What is the real part of every underdamped pole?
2. A design request is **at most 10% overshoot and a 1% settling time of at most 2 s**. Convert these into a damping wedge and an approximate settling line. Does the locus reach their intersection? Explain what your graphical test does and does not guarantee about an exact time-response specification. Consider the real-pole portion too.
3. Find the gain for $\zeta=1/2$. Calculate the standard overshoot and settling estimate. Separately, test the requested pole $s_d=-2+2j$ by computing the candidate $K=-s_d(s_d+1)$. Can a real positive gain place a pole there?

**During the MATLAB check:** Check the $\zeta=1/2$ gain and compare with $K=5$. Did larger gain move the complex poles farther left? Did it improve overshoot? Propose the kind of controller change that could move the locus.

## 6. A gain meets damping: does it meet everything else?

Now use $G(s)=1/[s(s+2)(s+4)]$, $D_c=K$, and require a complex pair with $\zeta=1/2$.

1. Form $P(s)$. Write the candidate upper pole as $s=-\alpha+j\sqrt3\alpha$, $\alpha>0$. Find $\alpha$ by setting the imaginary part of $P$ to zero, then obtain $K$ from the real part. If needed, use
   $$
   s^2=-2\alpha^2-2j\sqrt3\alpha^2,\qquad s^3=8\alpha^3.
   $$
2. Find the **third** pole at the same gain using the sum of the roots, then factor $P$. Check stability with Routh. Is a dominant-pair approximation plausible?
3. Compute $\omega_n$, the pair's predicted overshoot, and the approximate rise and 1% settling times. Write both the complete $\mathcal T$ and a unit-DC-gain second-order approximation. Which response must be checked before accepting the design?
4. Find $K_v$ and the unit-ramp steady-state error. A second requirement is $e_{ss,\rm ramp}\leq0.2$. What gain would meet the accuracy bound? Does your selected damping gain meet it? Check the poles at the accuracy-bound gain during the discussion.

**Stretch:** Determine the full stable gain interval. Could the unit-ramp error be reduced to 0.1 with proportional control while retaining stability?

**During the MATLAB check:** Compare the complete response with the pair approximation using a common dense time vector and a 1% band. Check all roots at the accuracy-bound gain. Name the conflict a lag or PI controller might address, and one added-mode effect that would need checking.

## MATLAB checks after each hand attempt

Download [root_locus_check.m](root_locus_check.m) into your MATLAB working folder. It requires **Control System Toolbox**. It contains the supplied models and plotting commands; you enter the gains you found by hand.

Use `root_locus_check(1,K)` with your Round 1 gain, `root_locus_check(5,K)` with your Round 5 gain, and `root_locus_check(6,K)` with your Round 6 gain. For the model comparisons in Rounds 2 and 3 and the full locus in Round 4, call `root_locus_check(2)`, `root_locus_check(3)`, and `root_locus_check(4)`. To mark a Round 4 event, call `root_locus_check(4,K)` with its gain. The helper returns the model and pole data when an output is requested: `result = root_locus_check(6,K)`.

For Round 6's accuracy check, first save `result = root_locus_check(6,K)` at your damping gain. Set `Kaccuracy` to the gain you calculated from the ramp-error bound, then run `pole(feedback(Kaccuracy*result.L0,1))`.

The helper simulates 30 seconds by default. If it warns that a response has not settled, it reports `NaN` (unverified) for that response's metrics. Extend the duration with a third argument, for example `root_locus_check(6,Kaccuracy,120)`. Inspect the full response and extend again if needed; a finite simulation is a numerical check, not a proof that no later excursion occurs.

The essential commands, also usable without the helper, are:

```matlab
s = tf('s');
% Define L0 from the current problem, excluding the varied gain.
% Set K to your hand-calculated positive gain.
rlocus(L0); grid on
T = feedback(K*L0,1);            % Negative unity feedback
pole(T)                         % All closed-loop poles
zero(T)                         % Retain relevant zeros in the response
t = (0:0.001:30)';
y = step(T,t);
plot(t,y); grid on
info = stepinfo(y,t,dcgain(T), ...
    'RiseTimeLimits',[0.1 0.9],'SettlingTimeThreshold',0.01)
```

Only calculate settling metrics for stable cases, and extend the time vector if the response has not settled. In Round 3, inspect the poles of unstable cases rather than assigning them a settling time. To keep the plotted gain equal to the $K$ in your characteristic equation, use `rlocus(L0)`, then apply the selected gain once in `feedback(K*L0,1)`. Using `rlocus(K*L0)` would sweep an additional multiplier and relabel the gains.

## Synthesis and exit questions

With your partner, prepare brief answers:

1. Give one example today in which a zero changed the conclusion.
2. Explain why a magnitude calculation alone cannot place a pole off the locus.
3. Why must a selected gain be accompanied by **all** poles and the complete response?
4. Which conflict motivates PD or lead, and which motivates lag or PI? What would you verify after adding either controller?

## Sources and continuation

Rounds 1–4 adapt FPE, *Feedback Control of Dynamic Systems*, **8th edition, §5.3, Examples 5.3–5.10**, checked against the **7th edition, §5.3, pp. 252–264**. Round 2's MATLAB comparison serves Example 5.7. The normalized motor continues FPE Example 5.1; the cubic calculations are course examples. Nise, *Control Systems Engineering*, **7th edition, §§8.6–8.7**, supports gain selection and verification of the higher-order response. Prompts and scaffolding are adapted for this activity.

This page includes the formulas and models needed today. For further explanation, see [Root Locus I](../book-notes/root-locus-construction_student.md), [Root Locus II](../book-notes/root-locus-gain-design_student.md), [Root Locus III: PD and Lead](../book-notes/root-locus-lead-pd_student.md), and [Root Locus IV: Lag and PI](../book-notes/root-locus-lag-pi_student.md). The later notes develop the controller changes motivated by Rounds 5–6.
