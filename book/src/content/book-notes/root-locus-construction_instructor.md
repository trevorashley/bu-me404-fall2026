# The Root-Locus Design Method I — From a Gain to a Family of Poles

<!--hidden-->

**Audience:** Fourth-year mechanical engineering, ME404.

**Duration:** One 105-minute scheduled meeting: about 75 minutes of core development plus 30 minutes of guided problem work or extensions. This follows the syllabus meeting length; the topic map's hours are a planning guide. Four such meetings cover this series.

# Teaching plan

**Theme:** Construction and geometric reasoning.

Follow FPE §§5.1–5.2 in the book's order: Definitions I and II, the Fig. 5.4 trial point, Rules 1–5 on the Eq. (5.20) running example, the §5.2.2 summary list, then gain selection (§5.2.3). Derive the phase condition on the board before stating any rule, and state each rule in FPE's words before giving its reason. The full asymptote derivation is available below; use it if students ask why the center formula works. Treat §8 and the arrival-angle formula as “if time permits” or follow-up reading; protect Rules 1–3, the departure calculation at $-4+4j$, and the complete cubic sketch during class.

The numbered lecture sections below match the student version, including the examples, assumptions, and numerical values. Complete instructor derivations and review answers follow the lecture. Keep this file outside the public chapter list.

| Time | Activity |
|---|---|
| 0–10 min | Motor roots by the quadratic formula (FPE §5.1) |
| 10–25 min | Definitions I and II; the Fig. 5.4 trial point; the motor passes |
| 25–50 min | Rules 1–5 on FPE's Eq. (5.20), rule by rule; summary list |
| 50–60 min | Magnitude condition; $K=64$ for $\zeta=0.5$ and the third root |
| 60–75 min | Cubic sketch by the rules; breakaway and Routh boundary; demos |
| 75–105 min | Guided sketching practice and discussion |

**Preparation:** Open the lecture's figures and runnable scripts in `demos/ch5/`. Use `--show` for an interactive figure; run without it to regenerate SVG and PNG. The demo guide includes MATLAB and Python instructions. Symbolic and independent numerical checks are in `verify_designs.py`.

---

**Instructor lecture notes — FPE 8th ed., Sections 5.1–5.2; selected examples from §5.3**

A gain changes every closed-loop pole at once. The root locus puts those changes on one picture, so that we can ask which responses feedback can produce before choosing a gain.

**Prerequisites:** [Pole locations and response](time-domain-specs_instructor.md), [Routh's criterion](stability_instructor.md), and [feedback equations](feedback-properties_instructor.md). We use complex numbers as vectors; no complex integration is needed.

**Sources:** Franklin, Powell & Emami-Naeini (FPE), *Feedback Control of Dynamic Systems*, 8th ed., §§5.1–5.3, checked against the corresponding sections of the 7th ed. The lecture follows the book's order: §5.1 (the motor, Example 5.1), §5.2 (Definitions I and II, the trial point of Eq. (5.18) and Fig. 5.4, Rules 1–5 on the running example of Eq. (5.20), the summary of §5.2.2, and gain selection in §5.2.3), and the satellite of §5.3. The damping-parameter locus in §8 is Example 5.2 of the 8th ed.; the 7th ed. presents it in §5.1 without an example number. Nise, *Control Systems Engineering*, 7th ed., §§8.2–8.5, supplements the construction procedure. Åström & Murray, *Feedback Systems*, 2nd ed., §12.5, supplies the repeated-root viewpoint. Examples labelled **[course example]** are our own, not numbered textbook examples. Figures are recomputed from the stated models.

## Learning objectives

1. Put a characteristic equation in root-locus form, $a(s)+Kb(s)=0$ or $1+KL_0(s)=0$.
2. State Definitions I and II of the root locus and test a trial point with the phase condition.
3. State and justify FPE's Rules 1–5, and apply them to sketch a locus.
4. Use the magnitude condition to select the gain that places a root at a chosen point on the locus.
5. Find imaginary-axis crossings and the stable gain interval.
6. Explain what a root-locus plot does and does not say about a closed loop.

## Notation and assumptions

| Symbol | Meaning |
|---|---|
| $G(s),D_c(s),H(s)$ | plant, controller, sensor |
| $L(s)=D_c(s)G(s)H(s)=K L_0(s)$ | full loop transfer function; $L_0$ excludes the varied gain |
| $L_0=b/a$ | fixed rational part of the loop |
| $p_i,z_i$ | signed open-loop pole and zero locations |
| $n,m$ | number of poles and zeros, including multiplicity |
| $K$ | real gain, varied from zero toward positive infinity unless stated otherwise |
| $\phi_i,\ \psi_i$ | angle of the vector from pole $p_i$, or from zero $z_i$, to a test point (FPE's notation) |
| $\sigma_a$ | center of the asymptotes on the real axis (FPE writes $\alpha$) |

Negative feedback gives $1+L=0$. In the core rules, $a$ and $b$ are real, monic polynomials with no common factor, $n>m$, and any **positive** fixed scale factor has been absorbed into $K$. Monic means that the highest-power coefficient is one. A negative scale factor must remain explicit (§8). Unity feedback means $H=1$. Signals and motor gains are normalized; time is in seconds and pole coordinates are in $\mathrm{s}^{-1}$.

**Notation bridge:** FPE writes $1+KL(s)=0$ with the gain omitted from its $L$. Our $L_0$ is FPE's $L$; our $L$ retains the meaning used in the earlier course notes. FPE's asymptote center $\alpha$ is our $\sigma_a$; we reserve $\alpha$ for the damping-ray parameter in Lecture II.

---

## Where we are, and where this lecture goes

In Chapter 4 we built proportional, PI, and PID controllers and watched the closed-loop poles move as we turned the gains. For a second-order loop we could follow them with the quadratic formula. For anything higher we had only Routh's criterion, which answers "stable or not?" for a given gain but says nothing about *where* the poles are or how fast the response will be. That gap is the subject of the next four lectures.

The idea is due to W. R. Evans, who in 1948 proposed plotting every root of the characteristic equation as the gain sweeps from zero to infinity, then reading the design off the picture. His rules let an engineer sketch the plot by hand, long before software could draw it. Today MATLAB draws it in one line, so the point of learning the rules is different: they tell you what the picture *means*, let you predict how adding a controller pole or zero will reshape it, and let you catch a plot that is wrong. FPE puts it bluntly: it is easy to get a constant wrong or leave out a term, and a rough hand sketch is how you notice.

The plan for this lecture follows FPE §§5.1–5.2:

1. Start with the motor, where the quadratic formula draws the whole picture (§1, FPE §5.1).
2. Define the root locus twice: once by the characteristic equation and once by a condition on phase, and test a trial point (§2, FPE §5.2).
3. State Evans's five rules, each justified from the phase condition and applied to FPE's running example (§3, FPE §5.2.1), then collect them in one list (§4, FPE §5.2.2).
4. Use the magnitude condition to select the gain that puts a root at a chosen point (§5, FPE §5.2.3).
5. Sketch the course cubic from start to finish by the rules and find the gain at which it goes unstable (§6), then summarize the procedure (§7).

Lecture II uses the finished picture to choose a gain against specifications. Lectures III and IV reshape the picture with controller dynamics.

## 1. Root locus of a basic feedback system {#section-1}

With $H=1$,

$$
\mathcal T(s)=\frac{Y}{R}=\frac{D_cG}{1+D_cG},\qquad
1+KL_0(s)=0\quad\Longleftrightarrow\quad a(s)+Kb(s)=0.
$$

FPE calls these the **root-locus form** (or Evans form) of the characteristic equation; a third version, $L_0(s)=-1/K$, is the one the next section builds on. The **root locus** is the set of roots of this polynomial for all permitted $K$. A plotted point is a possible closed-loop pole. A particular gain selects **all $n$ roots together**, not one independently chosen point on each branch.

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

Now put the table on the $s$-plane. The left panel of the figure below plots every root in the table as $K$ grows. At $K=0$ the two roots sit on the open-loop poles at $0$ and $-1$. As $K$ increases they move toward each other along the real axis, meet at $-1/2$ when $K=1/4$, and then leave the axis as a conjugate pair travelling straight up and down. The arrows show the direction of increasing gain. This picture **is** the root locus of the motor: every closed-loop pole the motor can have under proportional control lies on these two branches, and no gain can produce a pole anywhere else.

Read the design limitation directly from the geometry. The complex branches are a vertical line at $\Re s=-1/2$. Whatever gain we choose, the decay rate of the oscillatory response is fixed at $0.5\ \mathrm{s}^{-1}$; the gain only slides the poles up and down that line. Chapter 4 found this by algebra. The locus shows it at a glance, and it will show the analogous limitation for plants where the algebra is not available.

![Motor root locus and cubic root locus with breakaway and imaginary-axis crossings](demos/ch5/figures/l1_demo1_motor_cubic.svg)

The right panel previews §6: a third-order plant whose locus bends into the right half-plane. For a quadratic we can solve for the roots and plot them directly. For that plant, and for anything of higher order, there is no formula, so we need a way to find the branches without solving for the roots. That is the job of the next section.

## 2. Guidelines for determining a root locus: two definitions {#section-2}

FPE defines the locus twice. The first definition is the one we have been using.

> **Definition I.** The root locus is the set of values of $s$ for which $1+KL_0(s)=0$ is satisfied as the real parameter $K$ varies from $0$ to $+\infty$. Typically $1+KL_0(s)=0$ is the characteristic equation of the system, and in that case the roots on the locus are the closed-loop poles of that system.

Here is the reframing that makes the method work for any order. Instead of asking "where are the roots?", pick a trial point $s$ in the plane and ask "is this point a closed-loop pole for *some* positive gain?" Write the equation as $L_0(s)=-1/K$. If $K$ is real and positive, then $L_0(s)$ must be a **negative real number**: a complex number whose phase is $180^\circ$, or $180^\circ$ plus any multiple of $360^\circ$. Its magnitude can be anything, because $K$ is free to scale it. That gives the second definition.

> **Definition II.** The root locus of $L_0(s)$ is the set of points in the $s$-plane where the phase of $L_0(s)$ is $180^\circ$. If $\psi_i$ is the angle from zero $z_i$ to the test point and $\phi_i$ is the angle from pole $p_i$ to the test point, then the locus is the set of points where, for some integer $l$, the phase condition below holds.

$$
\boxed{\sum_i\psi_i-\sum_i\phi_i=180^\circ+360^\circ(l-1)}
$$

The immense merit of Definition II, in FPE's words, is that solving a high-order polynomial by hand is very difficult, while computing the phase of a transfer function is easy. Factoring $a$ and $b$,

$$
L_0(s)=\frac{\prod_{i=1}^m(s-z_i)}{\prod_{i=1}^n(s-p_i)},
\qquad
\arg L_0(s)=\sum_{i=1}^m\arg(s-z_i)-\sum_{i=1}^n\arg(s-p_i).
$$

Each factor $s-p_i$ or $s-z_i$ is itself a complex number with a simple picture. Stand at the trial point $s$ and draw an arrow to it from each open-loop pole and zero. The arrow from $p_i$ is the vector $s-p_i$: its length is $|s-p_i|$ and its angle, measured counterclockwise from the positive real direction, is $\phi_i$. The angle condition then says: add up the angles of the arrows from the zeros, subtract the angles of the arrows from the poles, and the total must be an odd multiple of $180^\circ$. Use a quadrant-aware angle: the vector $-1+j$ has angle $135^\circ$, not $-45^\circ$. Angles differing by $360^\circ$ represent the same direction.

The usual case, $K>0$, is called the **positive** or **$180^\circ$ locus**. When $K$ is real and negative, $L_0(s)$ must be real and positive, with phase $0^\circ$; that is the **negative** or **$0^\circ$ locus**, taken up in §8.

### Testing a trial point: FPE Eq. (5.18) and Fig. 5.4

FPE's first illustration is

$$
L_0(s)=\frac{s+1}{s(s+5)\left[(s+2)^2+4\right]},
$$

with poles at $0$, $-5$, and $-2\pm2j$ and a zero at $-1$. Is the test point $s_0=-1+2j$ on the locus for some $K$? Draw the five arrows (left panel of the figure below). The arrow from the zero at $-1$ is vertical, so $\psi_1=90^\circ$. From the pole at $0$ the arrow $-1+2j$ has $\phi_1=116.6^\circ$; from $-5$ the arrow $4+2j$ has $\phi_2=26.6^\circ$; from $-2+2j$ the arrow $1+0j$ has $\phi_3=0^\circ$; from $-2-2j$ the arrow $1+4j$ has $\phi_4=76.0^\circ$. Then

$$
\sum\psi_i-\sum\phi_i=90^\circ-116.6^\circ-26.6^\circ-0^\circ-76.0^\circ=-129.1^\circ.
$$

(FPE rounds the individual angles first and prints $-129.2^\circ$.) The phase is not $180^\circ$, so $s_0$ is not on the locus, and we would have to pick another point and try again. Measuring phase at one point is easy; measuring it at every point in the plane is hardly practical. That is why Evans's rules exist: they say where to look.

![FPE's trial-point phase test and the Eq. (5.20) locus built rule by rule](demos/ch5/figures/l1_demo3_fpe_rules.svg)

### A point that passes: the motor

For the motor at $s_d=-1/2+j\sqrt3/2$, the arrows from the poles at $0$ and $-1$ have angles $\phi_1=120^\circ$ and $\phi_2=60^\circ$. There are no zeros, so $\sum\psi_i-\sum\phi_i=-180^\circ$, and the point is on the locus. Direct substitution confirms it: $s_d(s_d+1)=-1$, so $K=1$ places a root exactly there. The gain is the subject of §5; for now the lesson is that the angle test, not the magnitude, decides membership. A magnitude calculation alone would assign a positive number to any trial point, even one that fails the angle test.

Notice what has changed. The angle test never asks us to solve a polynomial. It depends only on the *geometry* of the open-loop pole-zero pattern relative to the trial point. That is why the method scales to high order, and it is also why adding a controller pole or zero, which adds one more arrow, has a predictable effect on the picture. Lectures III and IV are built on exactly that observation.

## 3. Rules for determining a positive (180°) root locus {#section-3}

Evans's rules are the phase condition applied to special families of points, where the answer can be written down once and for all: points on the real axis, points very far away, and points very close to a pole or zero. FPE's advice: the first three rules are simple to remember and essential for any reasonable sketch; the last two are used occasionally. We state each rule as FPE does, give its one-paragraph reason, and apply it to FPE's running example,

$$
L_0(s)=\frac1{s\left[(s+4)^2+16\right]}=\frac1{s(s^2+8s+32)},
\qquad\text{poles }0,\ -4\pm4j,\qquad n=3,\ m=0.
$$

The right panel of the figure above is this locus, built up rule by rule.

**RULE 1.** *The $n$ branches of the locus start at the poles of $L_0(s)$, and $m$ of these branches end on the zeros of $L_0(s)$.*

From $a(s)+Kb(s)=0$: at $K=0$ the equation reduces to $a(s)=0$, whose roots are the poles. As $K\to\infty$, either $b(s)=0$ or $s\to\infty$. There are $m$ zeros where $b(s)=0$, so $m$ branches can end there; the case $s\to\infty$ is Rule 3. Because the coefficients are real, the locus is symmetric about the real axis.

*Example:* three branches start at $0$, $-4+4j$, and $-4-4j$. There are no finite zeros, so none of them ends at a finite point.

**RULE 2.** *The loci are on the real axis to the left of an odd number of poles and zeros.*

Take a test point on the real axis. The two angles from a complex-conjugate pair of poles cancel each other, as would the angles from a conjugate pair of zeros. The angle from a real pole or zero is $0^\circ$ if the test point is to its right and $180^\circ$ if the test point is to its left. For the total to be $180^\circ+360^\circ(l-1)$, the test point must be to the left of an odd number of real-axis poles plus zeros. Count multiplicity; for parity, subtracting a pole angle and adding a zero angle have the same effect.

*Example:* the only real pole is at $0$, so the locus occupies the entire negative real axis. For the motor, the segment $(-1,0)$ has exactly one pole to its right.

**RULE 3.** *For large $s$ and $K$, $n-m$ branches of the loci are asymptotic to lines at angles $\phi_l$ radiating out from the point $\sigma_a$ on the real axis, where*

$$
\phi_l=\frac{180^\circ+360^\circ(l-1)}{n-m},\quad l=1,2,\ldots,n-m,
\qquad
\sigma_a=\frac{\sum p_i-\sum z_i}{n-m}.
$$

As $K\to\infty$, $L_0(s)=-1/K$ can be satisfied only if $L_0(s)\to0$: either at the $m$ zeros (Rule 1) or as $s\to\infty$, since $n>m$. The asymptotes describe how the remaining $n-m$ roots go to infinity. Stand very far from the whole cluster of poles and zeros. Every arrow then has nearly the same angle, and the $m$ zero arrows cancel $m$ of the $n$ pole arrows, leaving $n-m$ pole arrows that all point the same way. From that vantage point the plant looks like

$$
1+\frac K{(s-\sigma_a)^{n-m}}=0,
$$

a stack of $n-m$ identical poles at a single point $\sigma_a$. The phase of that simple system is $180^\circ$ when its $n-m$ equal angles sum to $180^\circ+360^\circ(l-1)$, which is the formula for $\phi_l$. The center $\sigma_a$ comes from a property of polynomials: the coefficient of $s^{n-1}$ in a monic polynomial is the negative sum of its roots. If $m<n-1$, that coefficient of $a(s)+Kb(s)$ does not depend on $K$, so the sum of the closed-loop roots equals the sum of the open-loop poles at every gain. At large $K$, $m$ roots sit at the zeros and $n-m$ sit on the asymptotic system whose poles sum to $(n-m)\sigma_a$; equating the two sums gives $\sigma_a$. Imaginary parts cancel in both sums, so $\sigma_a$ is real: a center of mass of the poles, with the zeros counted negatively.

*Example:* $n-m=3$, so $\phi_l=60^\circ,180^\circ,300^\circ$ (that is, $\pm60^\circ$ and $180^\circ$), and

$$
\sigma_a=\frac{0+(-4+4j)+(-4-4j)}{3}=-\frac83=-2.67.
$$

The $\pm60^\circ$ asymptotes cross the imaginary axis at $\pm(8/3)\tan60^\circ=\pm4.62j$. The $180^\circ$ asymptote is the negative real axis already found by Rule 2. For the motor, $n-m=2$ gives $\pm90^\circ$ from $\sigma_a=(0-1)/2=-1/2$: the vertical line through $-1/2$, exactly where the quadratic formula put the complex branches.

Asymptotes describe the far-away branches, not necessarily the locus near the plant poles. They intersect at $\sigma_a$, which need not itself be a point on the locus.

**RULE 4.** *The angle of departure of a branch of the locus from a single pole is*

$$
\phi_{\mathrm{dep}}=\sum_i\psi_i-\sum_{i\ne\mathrm{dep}}\phi_i-180^\circ,
$$

*where $\sum\phi_i$ is the sum of the angles to the remaining poles and $\sum\psi_i$ the sum of the angles to all the zeros. For a pole of multiplicity $q$,*

$$
q\,\phi_{l,\mathrm{dep}}=\sum_i\psi_i-\sum_{i\ne\mathrm{dep}}\phi_i-180^\circ-360^\circ(l-1),\qquad l=1,2,\ldots,q,
$$

*and the angle(s) of arrival at a zero of multiplicity $q$ are*

$$
q\,\psi_{l,\mathrm{arr}}=\sum_i\phi_i-\sum_{i\ne\mathrm{arr}}\psi_i+180^\circ+360^\circ(l-1),\qquad l=1,2,\ldots,q.
$$

Take a test point a very small distance from the pole in question. The arrows from every *other* pole and zero are essentially the arrows to that pole itself, whose angles we can compute. Only the short arrow from the pole has an unknown angle, and transposing everything else in the phase condition to the right-hand side solves for it. For a multiple pole the unknown angle is counted $q$ times, which is why $l$ takes $q$ values and $q$ branches depart. The same argument at large $K$ gives the arrival angle at a zero. The arrival angle is the angle of the vector *from the zero* to nearby locus points; the direction of motion toward the zero is opposite that ray.

*Example:* at the pole $-4+4j$, the arrow from $-4-4j$ is vertical, $\phi_2=90^\circ$, and the arrow from $0$ is $-4+4j$, $\phi_3=135^\circ$. There are no zeros, so

$$
\phi_{\mathrm{dep}}=-90^\circ-135^\circ-180^\circ=-405^\circ=-45^\circ.
$$

By conjugate symmetry the branch from $-4-4j$ departs at $+45^\circ$. FPE notes that this rule is particularly useful when a pole lies near the imaginary axis, because it shows whether the branch starts off toward the stable left half-plane or toward the unstable right half-plane.

**[Course example]** For $L_0=1/[(s+4)(s^2+2s+5)]$, the upper pole is $-1+2j$. The arrows from the other poles have angles $90^\circ$ and $\tan^{-1}(2/3)=33.69^\circ$, so $\phi_{\mathrm{dep}}=-90^\circ-33.69^\circ-180^\circ=-303.69^\circ=56.31^\circ$. Its branch initially moves rightward: a lightly damped mechanical mode, such as a flexible link or a compliant gearbox, need not initially move deeper into the left half-plane under feedback.

*Repeated poles:* for the rigid satellite model $L_0=1/s^2$ of FPE §5.3, $q=2$ and there are no other poles or zeros, so $2\phi_{l,\mathrm{dep}}=-180^\circ-360^\circ(l-1)$ gives $\phi_{\mathrm{dep}}=\pm90^\circ$. Equivalently $s^2=-K$. Proportional control of a double integrator creates oscillation but no damping. The same local argument appears in Åström–Murray §12.5: near a pole of multiplicity $q$, $(s-p)^q\approx-Kb(p)/\widetilde a(p)$, and the $q$ rays are separated by $360^\circ/q$.

![Complex-pole departure, repeated origin poles, and a right-half-plane-zero example](demos/ch5/figures/l1_demo2_departure.svg)

**RULE 5.** *The locus can have multiple roots at points on the locus of multiplicity $q$. The branches will approach a point of $q$ roots at angles separated by*

$$
\frac{180^\circ+360^\circ(l-1)}{q}
$$

*and will depart at angles with the same separation, forming an array of $2q$ rays equally spaced. If the point is on the real axis, the orientation of this array is given by the real-axis rule. If the point is in the complex plane, the angle-of-departure rule must be applied.*

Watch the motor's two real roots again. One leaves the pole at $0$ moving left; the other leaves $-1$ moving right. They cannot pass through each other as distinct real roots: at the meeting point the characteristic polynomial has a double root, and beyond it the roots must become a complex-conjugate pair, because the coefficients are real. FPE's Fig. 5.2 shows exactly this: at $K=1/4$ there are two roots at $s=-1/2$, the horizontal branches come together, and the vertical branches break away. The locus arrives at $0^\circ$ and $180^\circ$ and departs at $+90^\circ$ and $-90^\circ$: four rays, $q=2$, separated by $90^\circ$. The meeting point is a **breakaway point**; the reverse event, a complex pair landing on the axis and splitting into two real roots, is a **break-in point**. FPE computes the departure angles from such a point with a *continuation locus*: restart the locus at the multiple root with $K=K_1+K_2$ and apply Rule 4 to the repeated pole.

To *find* the points, use the gain along the real axis,

$$
K(s)=-\frac{a(s)}{b(s)}.
$$

A multiple closed-loop root satisfies both $a+Kb=0$ and $a'+Kb'=0$. Eliminating $K$ gives

$$
\boxed{a'b-ab'=0}\qquad\text{or}\qquad \frac{dK}{ds}=0,
$$

provided $b(s)\ne0$. These are **candidates**. Keep only real candidates on an allowed real-axis segment with $K>0$. There is a useful picture behind the derivative. On the motor's segment $(-1,0)$, $K(s)$ is zero at each pole and positive in between, so it rises from one end, peaks, and falls to the other. Two roots moving inward from the ends reach the same gain only at the peak, so the breakaway is where $K(s)$ is maximum on the segment. On a segment between two zeros, $K$ is infinite at both ends and the break-in is at its minimum.

*Example:* for the motor, $K=-s^2-s$, so $dK/ds=-2s-1=0$ gives $s=-1/2$ at $K=1/4$. The FPE running example has no real-axis breakaway: its real-axis branch runs from the pole at $0$ out to $-\infty$ alone, and its complex branches never touch the axis.

**Which rules matter most.** FPE's closing remark on §5.2.1 is worth repeating. It is usually sufficient to draw the locus using only Rules 1 to 3, which should be memorized. Rule 4 is sometimes useful to understand how a branch departs, especially from a pole near the imaginary axis. Rule 5 helps interpret computer plots and, in later sections, explains how a locus changes qualitatively as a pole or zero is moved. The accurate curves come from MATLAB:

```matlab
s = tf('s');
sysL = 1/(s*((s+4)^2+16));      % FPE Eq. (5.20)
rlocus(sysL); grid on
```

## 4. Summary of the rules for determining a root locus {#section-4}

This is FPE §5.2.2, in our notation.

1. **RULE 1.** The $n$ branches of the locus start at the poles of $L_0(s)$, and $m$ branches end on the zeros of $L_0(s)$.
2. **RULE 2.** The loci are on the real axis to the left of an odd number of poles and zeros.
3. **RULE 3.** For large $s$ and $K$, $n-m$ branches of the loci are asymptotic to lines at angles $\phi_l$ radiating out from the center point $\sigma_a$ on the real axis, where
   $$
   \phi_l=\frac{180^\circ+360^\circ(l-1)}{n-m},\quad l=1,2,\ldots,n-m,
   \qquad
   \sigma_a=\frac{\sum p_i-\sum z_i}{n-m}.
   $$
4. **RULE 4.** The angle(s) of departure of a branch of the locus from a pole of multiplicity $q$ are given by
   $$
   q\,\phi_{l,\mathrm{dep}}=\sum\psi_i-\sum_{i\ne\mathrm{dep}}\phi_i-180^\circ-360^\circ(l-1),
   $$
   where $l=1,2,\ldots,q$, and the angle(s) of arrival of a branch at a zero of multiplicity $q$ are given by
   $$
   q\,\psi_{l,\mathrm{arr}}=\sum\phi_i-\sum_{i\ne\mathrm{arr}}\psi_i+180^\circ+360^\circ(l-1).
   $$
5. **RULE 5.** The locus can have multiple roots at points on the locus of multiplicity $q$. The branches approach a point of $q$ roots at angles separated by $[180^\circ+360^\circ(l-1)]/q$ and depart at angles with the same separation, forming an array of $2q$ rays equally spaced. If the point is on the real axis, the orientation of this array is given by the real-axis rule. If the point is in the complex plane, the angle-of-departure rule must be applied.

Two practical additions that the rules do not state: multiple roots on the real axis are found from $dK/ds=0$ on an allowed segment, and imaginary-axis crossings are found from Routh's criterion or by substituting $s=j\omega$ (§6).

## 5. Selecting the parameter value {#section-5}

The positive locus is a plot of all possible root locations for *some* positive $K$. Design means choosing a *particular* $K$. Definition II used only the phase of $L_0$; if a root is actually to sit at a chosen point on the locus, the **magnitude condition** must hold as well. From $L_0(s)=-1/K$,

$$
\boxed{K=\frac1{|L_0(s)|}
=\frac{\prod_i|s-p_i|}{\prod_i|s-z_i|}}.
$$

This has a graphical reading: on a plot with equal scales on the two axes, $K$ is the product of the lengths of the arrows from the poles divided by the product of the lengths of the arrows from the zeros. FPE remarks that nobody does this by hand to finish a design; MATLAB's `rlocfind` or `rltool` returns the gain at a clicked point. The value of the hand calculation is as a sanity check on the computer's answer.

### FPE's example: a damping ratio of 0.5 on the Eq. (5.20) locus

On the right panel of the §2 figure, the dotted rays make angle $\cos^{-1}0.5=60^\circ$ with the negative real axis, so every point on them has $\zeta=0.5$. Suppose we want the complex pair of closed-loop poles there. The locus crosses the upper ray at $s_0=-2+2\sqrt3\,j\approx-2+3.46j$. Reading lengths off the figure as FPE does, $|s_0|\approx4.0$, $|s_0-(-4+4j)|\approx2.1$, and $|s_0-(-4-4j)|\approx7.7$, so $K\approx4.0(2.1)(7.7)\approx65$. The exact lengths are $4$, $\sqrt{4+(2\sqrt3-4)^2}$, and $\sqrt{4+(2\sqrt3+4)^2}$, whose product is exactly $64$. The graphical estimate is good to about two percent.

Where is the third root? Rule 3's sum-of-roots property answers without searching: the roots sum to $-8$ at every gain, the pair sums to $-4$, so the third root is $-4$. Indeed

$$
s^3+8s^2+32s+64=(s+4)(s^2+4s+16).
$$

The design is not finished when the poles are placed. This loop has one integrator, so it is Type 1, and with $K=64$ its velocity constant is

$$
K_v=\lim_{s\to0}sKL_0(s)=\frac K{32}=2\ \mathrm{s}^{-1}.
$$

If the dynamic response implied by the root locations and the steady-state accuracy implied by $K_v$ are both acceptable, gain selection alone completes the design. If no value of $K$ satisfies all the constraints, which FPE notes is the typical case, the controller must be given dynamics. Lecture II makes the first check systematic; Lectures III and IV supply the dynamics.

For the motor, the magnitude condition at $s_d=-1/2+j\sqrt3/2$ gives $K=|s_d|\,|s_d+1|=1$, agreeing with the direct substitution in §2.

## 6. A complete sketch by the rules [course example] {#section-6}

Now apply the rules in order to the cubic that Lecture II will design against. Think of it as the motor with one more lag: an amplifier, a filtered velocity sensor, or a compliant coupling each add a pole, and here that pole sits at $-4$ with the other poles at $0$ and $-2$:

$$
L_0(s)=\frac1{s(s+2)(s+4)},\qquad
P(s,K)=s^3+6s^2+8s+K.
$$

**RULE 1.** The poles are $0,-2,-4$ and there are no finite zeros, so three branches start at the poles and all three go to infinity.

**RULE 2.** The real-axis segment $(-2,0)$ has one pole to its right and is on the locus; so is $(-\infty,-4)$, with three poles to its right. The segment $(-4,-2)$ has two poles to its right and is not on the locus.

**RULE 3.** With $n-m=3$,

$$
\sigma_a=\frac{0-2-4}{3}=-2,\qquad \phi_l=60^\circ,180^\circ,300^\circ.
$$

Already the sketch tells the main story. Two of the three far branches leave at $\pm60^\circ$ from the center $-2$, and a ray at $60^\circ$ from a point on the negative real axis must eventually cross into the right half-plane. So the closed loop becomes unstable at some large enough gain. The remaining questions are where the two roots from $0$ and $-2$ leave the axis, and at what gain the crossing happens.

**RULE 4.** All poles are real and simple; the branches leave the real poles along the real axis in the directions Rule 2 allows.

**RULE 5.** The two roots starting at $0$ and $-2$ move toward each other and must leave the axis between them. The stationary-gain equation is

$$
3s^2+12s+8=0
\quad\Longrightarrow\quad s=-2\pm\frac{2\sqrt3}{3}.
$$

Only $s=-0.8453$ lies on a positive-gain segment. It gives $K=16\sqrt3/9\approx3.0792$. The other candidate, $-3.155$, lies on $(-4,-2)$ and gives negative gain; it is rejected. Two branches arrive at $-0.8453$ along the axis and depart at $\pm90^\circ$.

**Crossing the imaginary axis.** The pair leaves the axis at $-0.845$ and curves outward toward the $\pm60^\circ$ asymptotes. To find the gain at which it reaches the imaginary axis we do not need the plot at all: that is precisely the stability boundary Routh's criterion locates.

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

Compare the two panels of the figure in §1 once more. The motor's branches turn vertical and never cross the axis. Adding one pole at $-4$ pulls the asymptotes from $\pm90^\circ$ to $\pm60^\circ$, and that is enough to bend the branches into the right half-plane. This is the lesson that generalizes. Each additional excess pole adds one more asymptote direction, and the outermost pair leans further toward the right half-plane: $\pm90^\circ$ for two excess poles, $\pm60^\circ$ for three, $\pm45^\circ$ for four. Extra lags push a locus toward instability, and the locus shows it before any gain is chosen.

## 7. Sketch first, compute second {#section-7}

Here is the whole procedure, in the order we used it on the cubic.

1. Derive the characteristic polynomial and identify the varied parameter; put it in root-locus form.
2. Mark poles and zeros; apply Rules 1–3 for endpoints, real-axis segments, and asymptotes.
3. Apply Rule 4 at any complex or repeated pole, and Rule 5 with $dK/ds=0$ for real-axis breakaway and break-in points.
4. Use Routh or $s=j\omega$ to locate crossings.
5. Compute roots at a few gains, including every root at each gain.
6. Add arrows for increasing gain. Select $K$ by the magnitude condition, then verify any proposed design in the time domain.

A numerical plot fills in the curves. It does not replace the sign, stability, or cancellation checks.

```matlab
s = tf('s');                      % Control System Toolbox
L0 = 1/(s*(s+2)*(s+4));
rlocus(L0); grid on
K = 48;
roots([1 6 8 K])                  % Characteristic roots at this gain
```

## 8. Extensions: another parameter or another sign {#section-8}

FPE's Example 5.2 (8th ed.; §5.1 of the 7th ed.) varies a plant pole rather than controller gain. For $s^2+cs+A=0$, fixed $A>0$ and variable $c\ge0$ give

$$
1+c\frac{s}{s^2+A}=0.
$$

That is a different locus, with starting poles $\pm j\sqrt A$ and a zero at zero. It describes increasing physical damping, not increasing motor gain. The root-locus method applies to any real parameter that enters the characteristic equation linearly.

For negative $K$, or positive feedback written $1-KL_0=0$, the angle condition is $0^\circ$ modulo $360^\circ$ (FPE §5.6.1). Re-derive the real-axis and asymptote rules for that sign: the locus lies to the left of an *even* number of poles and zeros, and the asymptote angles become $360^\circ(l-1)/(n-m)$.

**[Course example]** $L_0=(1-s)/[s(s+2)]$ has a positive DC-direction numerator but a **negative leading coefficient**. Do not replace $1-s$ by $s-1$ without retaining the minus sign. The closed-loop polynomial is

$$
s^2+(2-K)s+K,
$$

stable only for $0<K<2$. As $K\to\infty$, one root approaches the RHP zero at $+1$. Endpoint reasoning identifies a high-gain limitation before detailed design.

## What to take away

- The root locus is the set of all closed-loop poles for all gains (Definition I). A gain picks one point on *every* branch at once.
- A point is on the locus when the phase of $L_0$ there is $180^\circ$ (Definition II): the zero-arrow angles minus the pole-arrow angles. No polynomial is solved.
- Rules 1–5 are the phase condition applied to special points. Rules 1–3 (endpoints, real axis, asymptotes) draw almost everything and should be memorized; Rule 4 (departure) matters near the imaginary axis; Rule 5 (multiple roots) explains breakaway and break-in.
- The magnitude condition $K=1/|L_0(s)|$ selects the gain for a chosen point, and the sum of the roots locates the remaining ones.
- Extra poles spread the asymptotes and bend branches toward the right half-plane; the cubic became gain-limited at $K=48$, while FPE's running example is limited at $K=256$.
- The plot tells you where the poles *can* go, and the magnitude condition which gain puts them there. Whether that gain meets the specifications is Lecture II.

## Review questions

1. For the motor at $s=-1+j$, why does the magnitude condition alone give a misleading candidate gain?
2. Why does the cubic's breakaway equation have a real solution that is not on the positive-gain locus?
3. Does an asymptote at $60^\circ$ imply that the system is unstable at every gain?
4. For a double pole at the origin, why are departure angles not found by inserting the other coincident pole into the simple-pole formula?
5. Sketch the real-axis segments for poles $0,-1,-3$ and a zero at $-2$.
6. For FPE's running example $1/(s[(s+4)^2+16])$, at what gain does the locus cross the imaginary axis, and at what frequency?

## Optional practice and demonstrations

Work FPE §5.2's rules on one new pole-zero pattern, then check it numerically. Nise 7th ed. §8.5 provides additional breakaway and departure practice. Run `l1_demo1_motor_cubic.py`, `l1_demo2_departure.py`, and `l1_demo3_fpe_rules.py`; instructions and a MATLAB alternative are in the [demo guide](demos/ch5/guide.md).

**Next:** [II — Reading the locus and selecting gain](root-locus-gain-design_instructor.md).

# Instructor derivations and teaching material

## Board derivation A — Endpoints and asymptotes

Assume the monic, coprime $a,b$ of the lecture, $n>m$, with $r=n-m$. The polynomial $a+Kb$ has degree $n$ for every finite $K$, so there are $n$ roots counting multiplicity. As $K\to0$, coefficient continuity gives the roots of $a$. For a finite limiting root as $K\to\infty$, divide by $K$:

$$
\frac{a(s)}K+b(s)=0\quad\Longrightarrow\quad b(s)=0.
$$

There are $m$ finite endpoints; the remaining $r$ roots escape to infinity. Expand the products at large $s$:

$$
a(s)=s^n\left(1-\frac{\sum p_i}s+O(s^{-2})\right),\qquad
b(s)=s^m\left(1-\frac{\sum z_i}s+O(s^{-2})\right),
$$

$$
\frac ab=s^r\left[1+\frac{\sum z_i-\sum p_i}s+O(s^{-2})\right].
$$

Compare with

$$
(s-\sigma_a)^r=s^r\left[1-\frac{r\sigma_a}s+O(s^{-2})\right].
$$

Matching the next-to-leading coefficient gives $\sigma_a=(\sum p_i-\sum z_i)/r$. Then $a/b=-K$ becomes $(s-\sigma_a)^r\approx-K$. The $r$ roots of the negative real number $-K$ have angles $(2q+1)\pi/r$. Real coefficients make the pole and zero sums real, hence the intersection is on the real axis.

**Say:** “The asymptotes come from the polynomial's highest powers. The centroid uses the next coefficient.” No contour integration or residue theorem is required.

**Scope boundary:** $n=m$ has no such asymptotes and may have a special gain at which the leading coefficient vanishes. Do not apply these formulas to that case. Negative leading loop scale shifts the phase condition; preserve it explicitly.

## Board derivation B — Multiple roots and the gain derivative

At a multiple root $s_b$, $P(s_b,K_b)=0$ and $P_s(s_b,K_b)=0$. For $b(s_b)\ne0$,

$$
K_b=-a/b,\qquad P_s=a'+K_bb'=\frac{a'b-ab'}b=0.
$$

Also

$$
K'(s)=-\frac{a'b-ab'}{b^2}.
$$

This proves the stationary-gain test, but does not prove that each solution lies on the desired positive-gain locus. Near an ordinary double root, Taylor-expand the polynomial:

$$
0\approx b(s_b)\Delta K+\frac12P_{ss}(s_b,K_b)(\Delta s)^2,
\qquad
(\Delta s)^2\approx-\frac{2b(s_b)\Delta K}{P_{ss}(s_b,K_b)}.
$$

For real coefficients and a real double root the right side is real. On one side of $K_b$ the local roots separate horizontally; on the other they separate vertically. If $P_{ss}=0$, a higher-order expansion is required.

For the cubic, let $x=s+2$. Then $a=s(s+2)(s+4)=x^3-4x$ and $K=4x-x^3$. Stationarity gives $x=\pm2/\sqrt3$. The positive-gain candidate has $x=2/\sqrt3$ and

$$
K=\frac8{\sqrt3}-\frac8{3\sqrt3}=\frac{16\sqrt3}{9}.
$$

The other candidate gives its negative. At the selected candidate $P_{ss}=6s+12=4\sqrt3>0$, so increasing $K$ makes $(\Delta s)^2<0$ and the pair leaves vertically.

## Board derivation C — Departure and arrival, including multiplicity

For a pole of multiplicity $q$,

$$
(s-p)^q\widetilde a(s)+Kb(s)=0.
$$

At small $K$, evaluate the smooth factors at $p$:

$$
q\theta=180^\circ+\arg b(p)-\arg\widetilde a(p)+360^\circ\ell.
$$

There are $q$ distinct rays separated by $360^\circ/q$. For the complex-pole example, $a=(s+4)(s^2+2s+5)=s^3+6s^2+13s+20$. At $p=-1+2j$, the other-pole vectors are $4j$ and $3+2j$. Therefore $\arg\widetilde a(p)=90^\circ+33.69^\circ$, giving $56.31^\circ$. A numerical check uses $ds/dK=-b/P_s=-1/a'(p)$ at $K=0$; here $a'(p)=-8+12j$, so $ds/dK=(8+12j)/208$ has precisely that angle.

For FPE's running example $a=s^3+8s^2+32s$, at $p=-4+4j$ the other-pole vectors are $8j$ and $-4+4j$, so $\arg\widetilde a(p)=90^\circ+135^\circ$ and $\phi_{\mathrm{dep}}=-225^\circ-180^\circ=-405^\circ\equiv-45^\circ$. The numerical check: $a'(p)=3p^2+16p+32=-96j+(-64+64j)+32=-32-32j$, so $ds/dK=-1/a'(p)=(1-j)/64$, whose angle is $-45^\circ$.

**Sign conventions.** FPE writes the single-pole rule as $\sum\psi_i-\sum\phi_i-180^\circ$; the earlier course form $180^\circ+\sum\psi_i-\sum\phi_i\pmod{360^\circ}$ is the same set of directions. FPE's asymptote index $l=1,\ldots,n-m$ with $180^\circ+360^\circ(l-1)$ equals the $q=0,\ldots,n-m-1$ form with $(2q+1)180^\circ$.

For a zero of multiplicity $q$, divide by $K$ and write $b=(s-z)^q\widetilde b$. At large $K$,

$$
(s-z)^q\approx-\frac{a(z)}{K\widetilde b(z)},\qquad
q\theta=180^\circ+\arg a(z)-\arg\widetilde b(z)+360^\circ\ell.
$$

The vector used is $s-z$. Motion toward $z$ is the opposite direction. This resolves differing diagram conventions without memorizing two incompatible “arrival” angles.

## Worked classroom check — FPE's §5.2 numbers

*Trial point (Eq. 5.18, Fig. 5.4).* At $s_0=-1+2j$ the exact angles are $\psi_1=90^\circ$, $\phi_1=116.565^\circ$, $\phi_2=26.565^\circ$, $\phi_3=0^\circ$, $\phi_4=75.964^\circ$; the total is $-129.09^\circ$. FPE rounds each angle to one decimal before adding and prints $-129.2^\circ$. Either way the point fails.

*Rule 3 (Eq. 5.20).* $\sigma_a=-8/3$; the $\pm60^\circ$ asymptotes meet the imaginary axis at $\pm(8/3)\sqrt3\,j=\pm4.619j$.

*Section 5.2.3 gain.* Write $s=\alpha(-1+j\sqrt3)$ in $s^3+8s^2+32s+K$: $s^2=\alpha^2(-2-2j\sqrt3)$ and $s^3=8\alpha^3$, so $\Im P=\sqrt3\alpha(32-16\alpha)=0$ gives $\alpha=2$, and $\Re P=64-64-64+K=0$ gives $K=64$ exactly. FPE's graphical reading is 65. The roots sum to $-8$, so the third root is $-4$, and $(s+4)(s^2+4s+16)=s^3+8s^2+32s+64$. $K_v=64/32=2\ \mathrm{s}^{-1}$.

*Imaginary-axis crossing.* Routh: $s^1$ row $(256-K)/8$, so $K=256$, with auxiliary polynomial $8s^2+256$ giving $\pm j\sqrt{32}=\pm5.657j$ and the real root $-8$. This is the number behind review question 6. All of these are checked symbolically in `verify_designs.py` and printed by `l1_demo3_fpe_rules.py`.

## Worked classroom check — A Routh boundary is not a stable design

For the cubic, Routh's first column is $1,6,(48-K)/6,K$. For $K<0$ there is one RHP root; for $0<K<48$ there are none; for $K>48$ there are two. At $K=0$ there is an origin root. At $K=48$, the zero row requires the auxiliary polynomial $6s^2+48$ and its derivative $12s$. The factorization $(s+6)(s^2+8)$ confirms the boundary modes. A sinusoidal input at $\sqrt8$ can produce an unbounded resonant response, so do not call the boundary BIBO stable.

## Review-question answers

1. At $-1+j$, $s(s+1)=-1-j$, so $\arg L_0=135^\circ$ rather than $180^\circ$. Its magnitude suggests $K=\sqrt2$, but substitution gives $-1-j+\sqrt2\ne0$.
2. The root $-2-2\sqrt3/3$ lies between $-4$ and $-2$, with two real poles to its right. Its gain is negative.
3. No. An asymptote is a large-gain limit. The cubic is stable over $0<K<48$.
4. The coincident vector is zero, with undefined angle. Factor the repeated pole and solve for $q$ rays instead.
5. The ordered real locations are $-3$ (pole), $-2$ (zero), $-1$ (pole), $0$ (pole). The locus lies on $(-3,-2)$ and $(-1,0)$; the two asymptotes are vertical through $\sigma_a=(-4+2)/2=-1$.
6. $K=256$ at $\omega=\sqrt{32}\approx5.66$ rad/s, from the Routh $s^1$ row $(256-K)/8$ or by substituting $s=j\omega$: $-j\omega^3-8\omega^2+32j\omega+K=0$ gives $\omega^2=32$ from the imaginary part and $K=8\omega^2=256$ from the real part.

## Instructor cautions and source checks

- Use $L_0$ consistently. FPE's gain-excluded $L$ differs from Chapter 4's full-loop convention in these notes. FPE's asymptote center is $\alpha$; the notes write $\sigma_a$ because Lecture II uses $\alpha$ as the damping-ray parameter.
- The damping-parameter locus is Example 5.2 only in the 8th edition. The 7th edition presents the same $c$-locus in §5.1 (Fig. 5.3) without an example number.
- Rule 4's departure formula and Rule 5's multiple-root statement are quoted from §5.2.2 of both editions. The $dK/ds=0$ computation is the course's practical addition; FPE locates multiple roots from the plot and the continuation locus.
- Do not substitute the simple-pole formula at a multiple pole.
- Never connect unrelated roots by sorting only their real parts across a breakaway. The demos plot dense root samples without artificial branch connections.
- FPE 8th ed. chapter extract has 195 PDF pages; the corresponding 7th-edition extract `complete_258-331.pdf` has 74 pages and printed pp. 234–307. Section labels, not PDF offsets, anchor citations.
- The local 8th-edition extraction drops many displayed equations. The rules were checked against the 7th edition and independently derived here. Nise §8.5 and Åström–Murray §12.5 corroborate the construction and repeated-root arguments.

## Demonstration index

| Script | Lecture purpose | Pause and ask |
|---|---|---|
| `l1_demo1_motor_cubic.py` | Analytic motor versus gain-limited cubic | Which model can become unstable as gain increases? |
| `l1_demo2_departure.py` | Complex and repeated poles; signed RHP zero | Which open-loop mode initially moves rightward? |
| `l1_demo3_fpe_rules.py` | FPE Fig. 5.4 trial point; Eq. (5.20) locus with asymptotes, departure, $\zeta=0.5$ dots, crossing | Before revealing the dots: estimate $K$ from the three arrow lengths |

The figures are generated from the exact models and are not crops of textbook figures. Algebra checks are in `demos/ch5/verify_designs.py`.
