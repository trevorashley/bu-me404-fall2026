# Time-Domain Specifications Explorer

An interactive companion to the L3 notes on time-domain specifications and the effects of zeros and extra poles (FPE 8th ed., §3.4–3.5). Drag poles and zeros in the s-plane and watch rise time, overshoot, peak time and settling time change in the step response.

## Running it

You need Python 3 (any recent version; no packages to install). From the repository root:

```bash
python3 apps/time-domain-specs/serve.py      # macOS / Linux
py apps\time-domain-specs\serve.py           # Windows
```

The page opens in your browser at `http://localhost:8404/`; if that port is busy the next free one is used and printed in the terminal. Press **Ctrl-C** in the terminal to stop. Everything runs locally and works offline.

Use a current Chrome, Edge, Firefox or Safari. If the browser does not open automatically, copy the printed address into it.

## The four tabs

1. **Specifications.** A standard second-order pair with unit DC gain. The measured 10–90% rise time, peak, overshoot and settling time are marked on the step response and compared with the textbook formulas t_r ≈ 1.8/ωn, M_p = e^(−πζ/√(1−ζ²)) and t_s ≈ 4.6/σ, plus the guaranteed envelope bound. The insets show why 1.8 is only a fit and why M_p depends on ζ alone. **First order** switches to a single real pole with its exact results.
2. **Design region.** Enter limits for t_r, M_p and t_s. The allowable region of the s-plane is shaded (the book shades the excluded region). Drag a candidate pair and compare the *formula* check with the *measured* check. The Ex. 3.27 preset passes every formula bound and still fails the rise-time requirement.
3. **Zeros & extra poles.** Add a zero or an extra real pole at s = −ασ. For a zero, the plot shows the exact decomposition y = y₀ + ẏ₀/(ασ). Push α below zero to see the right-half-plane zero's undershoot. The inset sweeps α so you can see where the factor-of-four rule comes from.
4. **Sandbox.** Place any poles and zeros. The Sandbox shows modal coefficients (residues), the dominant-pair approximation, factor-of-four flags and pinned comparison responses. Presets reproduce Eqs. 3.78–3.79 and Examples 3.28–3.30 (including the Boeing 747), plus the stable non-minimum-phase system (1−s)/(s+1)².

## Controls

| Key / button | Action |
|---|---|
| `1`–`4` | switch tabs |
| drag × or ○ | move a pole or zero; conjugate partners follow |
| **Predict mode**, then `R` | hide responses and measured values; click the plot to mark your guess for the peak, then reveal |
| `P` | pin the current response (Sandbox) |
| `Delete` | delete the selected root (Sandbox) |
| `+` / `−` | larger / smaller text (useful on a projector) |
| **Copy link** | the URL stores the whole configuration, so a link reproduces exactly what you see |
| **Fit axes** / **Fit view** | re-scale the plots (axes stay fixed while you drag, so changes are visible) |

## Conventions

These match the L3 notes and the Chapter 3 demo scripts:

- **Rise time t_r:** from the first 10% crossing to the first 90% crossing of the final value.
- **Overshoot M_p:** the maximum excess over the final value, as a fraction of the final value.
- **Settling time t_s:** the last time the response is outside the band. The band is 1% by default; 2% and 5% are available.
- **Normalisation:** unless a preset sets a gain, the DC gain is normalised to H(0) = 1.

Responses are computed by exact discretisation of a state-space model, so they are exact at the sample points. Crossing times are interpolated between samples.

## Tests (instructor)

From the repository root:

```bash
node --test apps/time-domain-specs/tests/*.test.mjs
book/src/content/book-notes/demos/.venv/bin/python apps/time-domain-specs/tests/reference.py
```

- **`core.test.mjs`** checks the numerical core against the values stated in the L3 notes.
- **`reference.py`** compares the simulator with `scipy.signal` on random systems.
