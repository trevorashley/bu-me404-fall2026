# Chapter 5 lecture demonstrations

Seven runnable demonstrations accompany the four Part IV note pairs. Each prints
the relevant calculations and generates SVG and PNG figures in `figures/`.
The plotting palette and `--show` / `--no-save` options reuse `../ch2/demokit.py`.
Models are normalized, time is in seconds, and feedback is negative and unity
unless the notes explicitly introduce an inner velocity loop.

## Running with Python

From the repository root, the existing course environment can run the seven
demonstrations:

```bash
book/src/content/book-notes/demos/.venv/bin/python book/src/content/book-notes/demos/ch5/run_all.py
```

That environment does not currently include SymPy or pip, so it cannot run
`verify_designs.py` as-is. For verification, or for a fresh checkout, create a
separate Chapter 5 environment with all dependencies using the recipe below.
This leaves the shared course environment intact. The commands assume Python
3.11 or later is installed; `python3 -m venv` supplies pip in the new environment.

```bash
cd book/src/content/book-notes/demos
python3 -m venv ch5/.venv
ch5/.venv/bin/python -m pip install numpy scipy matplotlib sympy
ch5/.venv/bin/python ch5/run_all.py
ch5/.venv/bin/python ch5/l3_demo1_pd_lead.py --show
ch5/.venv/bin/python ch5/verify_designs.py
```

On Windows, the new environment's Python is `ch5\.venv\Scripts\python.exe`. SymPy is
needed only for the instructor verification script. The figures are already
included with the notes, so reading the notes does not require Python.

`--show` opens a figure window and does not save files, matching the earlier
course demos. With neither option, a script writes SVG and PNG; `--no-save`
computes and prints results without saving. Run `run_all.py` to regenerate all
eight figures. It stops with a failing exit status if any demo fails.

## MATLAB alternative

Run [run_ch5.m](run_ch5.m) in MATLAB with Control System Toolbox. It covers the
motor/cubic loci, gain selection, PD/lead and Franklin comparisons, long-horizon
lag/PI responses, and notch attenuation. It opens figures without writing files.
The notes also give shorter MATLAB examples beside the worked designs.

## What the Python means

| Python expression | MATLAB connection / purpose |
|---|---|
| `np.array([1, 6, 8, K])` | `[1 6 8 K]`: polynomial coefficients in descending powers |
| `np.roots(coefficients)` | `roots(coefficients)`: all polynomial roots |
| `np.polyadd(a, b)` | Adds polynomial coefficients, padding leading zeros as needed |
| `np.polymul(a, b)` | `conv(a,b)`: multiplies polynomials |
| `signal.TransferFunction(num, den)` | `tf(num,den)`: numerator/denominator model |
| `signal.step(system, T=t)` | `step(system,t)`, but Python returns `(time, output)` |
| `signal.lsim(system, U=u, T=t)` | `lsim(system,u,t)`, returning time, output, and states |
| `1j` | MATLAB's `1j`: the imaginary unit |
| `np.linspace(0, 20, 20001)` | `linspace(0,20,20001)`: a uniform time grid |
| `**` | MATLAB's scalar power `^`; NumPy arrays apply it element by element |

NumPy handles arrays and polynomial arithmetic, SciPy simulates linear systems,
and Matplotlib draws the figures. `kit.py` provides shared plotting and
closed-loop helpers. Its `closed_loop(num,den,K)` explicitly forms
`den + K*num` without cancelling factors. Dense root samples are plotted as
dots rather than connecting possibly mismatched roots at breakaway points.

## Demonstration index

| Lecture | Script | Purpose / source |
|---|---|---|
| I | [l1_demo1_motor_cubic.py](l1_demo1_motor_cubic.py) | FPE Example 5.1 motor; course cubic with breakaway and Routh crossing |
| I | [l1_demo2_departure.py](l1_demo2_departure.py) | Complex and repeated-pole departures; signed RHP-zero model |
| II | [l2_demo1_gain_design.py](l2_demo1_gain_design.py) | Exact damping-ray gain and full cubic response |
| III | [l3_demo1_pd_lead.py](l3_demo1_pd_lead.py) | Exact PD/lead design for −2 ± 2j; numerator effects |
| III | [l3_demo2_franklin.py](l3_demo2_franklin.py) | FPE 7th/8th ed. Example 5.11 and initial control effort |
| IV | [l4_demo1_lag_pi.py](l4_demo1_lag_pi.py) | Full lag and PI designs; reference, ramp, and disturbance paths, plus near-origin locus closeups |
| IV extension | [l4_demo2_extensions.py](l4_demo2_extensions.py) | FPE §5.4.2 lead–lag; illustrative notch; rate feedback |

## Numerical conventions and verification

Overshoot is relative to the true final value; rise is 10–90%; settling is the
last entry into a ±1% band on the sampled time grid, matching FPE and the earlier
course notes. MATLAB calls explicitly set `'SettlingTimeThreshold',0.01` because
`stepinfo` otherwise uses 2%. Short-response demos use
0.00025–0.001 s grids. The lag/PI demo uses 0.01 s steps over 1000 s to resolve
both its early response and slow tail. Values are rounded; changing a grid may
change the last printed digit. A run ending outside the settling band raises an
error. Simulation horizons also exceed several time constants of the slowest
closed-loop mode, rather than relying on that final-sample test alone.

[verify_designs.py](verify_designs.py) checks exact polynomial and partial-fraction
identities with SymPy, compares analytic responses with independently simulated
responses, verifies the Franklin performance specifications, and checks lag/PI
ramp limits and full-system stability. It prints the slow reference-step residues.
The notebook-style derivations are in the paired instructor Markdown notes;
students do not need SymPy to follow the lecture calculations.

No demo treats ideal PD's step-command impulse as a finite plotted spike. No
notch demonstration claims closed-loop robustness for an unspecified flexible
plant. The lead and lead–lag examples use the textbook parameters; the other
numerical designs are course examples identified in the notes.
