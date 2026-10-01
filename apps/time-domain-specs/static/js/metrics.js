// Step-response specifications, measured and estimated.
//
// Conventions follow the L3 notes and demos (demos/ch3/l3_demo1_step_specs.py):
//   t_r  first time y ≥ 0.9·yf minus first time y ≥ 0.1·yf
//   t_p  time of the global maximum; M_p = max(0, (y_max − yf)/|yf|)
//   t_s  last time |y − yf| > ε·|yf|  (ε = 0.01 by default)
// Crossings are linearly interpolated; the peak is refined with a parabola.

import { simulate, finalValue, autoHorizon, samplesFor } from "./lti.js";

function firstUp(t, z, level) {
  for (let k = 0; k < z.length; k++) {
    if (z[k] >= level) {
      if (k === 0) return t[0];
      const f = (level - z[k - 1]) / (z[k] - z[k - 1]);
      return t[k - 1] + f * (t[k] - t[k - 1]);
    }
  }
  return null;
}

export function measure(t, y, yf, eps = 0.01) {
  const out = { yf, rise: null, t10: null, t90: null, peak: null, tp: null, Mp: null,
    ts: null, settled: false, undershoot: null, tMin: null, reason: null };
  if (yf === null) { out.reason = "no final value"; return out; }
  if (Math.abs(yf) < 1e-12) { out.reason = "final value is 0"; return out; }
  const N = y.length;
  const z = new Float64Array(N);
  for (let k = 0; k < N; k++) z[k] = y[k] / yf;

  out.t10 = firstUp(t, z, 0.1);
  out.t90 = firstUp(t, z, 0.9);
  if (out.t10 !== null && out.t90 !== null) out.rise = out.t90 - out.t10;

  let kmax = 0, kmin = 0;
  for (let k = 1; k < N; k++) {
    if (z[k] > z[kmax]) kmax = k;
    if (z[k] < z[kmin]) kmin = k;
  }
  let zmax = z[kmax], tmax = t[kmax];
  if (kmax > 0 && kmax < N - 1) {
    const [a, b, c] = [z[kmax - 1], z[kmax], z[kmax + 1]];
    const den = a - 2 * b + c;
    if (den < 0) {
      const d = (0.5 * (a - c)) / den;
      zmax = b - 0.25 * (a - c) * d;
      tmax = t[kmax] + d * (t[1] - t[0]);
    }
  }
  if (zmax > 1 + 1e-9) {
    out.Mp = zmax - 1;
    out.tp = tmax;
    out.peak = zmax * yf;
  } else out.Mp = 0;
  if (z[kmin] < -1e-9) {
    out.undershoot = z[kmin];
    out.tMin = t[kmin];
  }

  let last = -1;
  for (let k = N - 1; k >= 0; k--) {
    if (Math.abs(z[k] - 1) > eps) { last = k; break; }
  }
  if (last === -1) { out.ts = 0; out.settled = true; }
  else if (last === N - 1) { out.ts = null; out.settled = false; }
  else {
    const e0 = Math.abs(z[last] - 1), e1 = Math.abs(z[last + 1] - 1);
    const f = (e0 - eps) / (e0 - e1);
    out.ts = t[last] + f * (t[last + 1] - t[last]);
    out.settled = true;
  }
  return out;
}

// Simulate on an automatic horizon, extending it until the response settles.
// Returns the response, its final value and the measured specifications.
export function analyze(sys, { input = "step", amp = 1, eps = 0.01, minT = 0 } = {}) {
  const yf = finalValue(sys, input, amp);
  let T = Math.max(autoHorizon(sys), minT);
  let res, m;
  for (let tries = 0; tries < 4; tries++) {
    res = simulate(sys, { input, amp, T, N: samplesFor(sys, T) });
    m = measure(res.t, res.y, yf, eps);
    if (m.settled || yf === null || Math.abs(yf) < 1e-12) break;
    T *= 2;
  }
  return { ...res, T, yf, metrics: m };
}

// ---------------------------------------------------------------- formulas

export const BAND_CONST = { 0.01: 4.6, 0.02: 3.9, 0.05: 3.0 };

export function zetaFromMp(Mp) {
  if (Mp <= 0) return 1;
  if (Mp >= 1) return 0;
  const L = -Math.log(Mp);
  return L / Math.sqrt(Math.PI ** 2 + L * L);
}

export function mpFromZeta(zeta) {
  if (zeta >= 1) return 0;
  if (zeta <= 0) return 1;
  return Math.exp((-Math.PI * zeta) / Math.sqrt(1 - zeta * zeta));
}

// Textbook estimates for a standard second-order pair with no zeros.
export function secondOrderEstimates(zeta, wn, eps = 0.01) {
  const sigma = zeta * wn;
  const wd = zeta < 1 ? wn * Math.sqrt(1 - zeta * zeta) : 0;
  const k = BAND_CONST[eps] ?? -Math.log(eps);
  return {
    sigma, wd,
    rise: 1.8 / wn,
    Mp: mpFromZeta(zeta),
    tp: zeta < 1 ? Math.PI / wd : null,
    ts: k / sigma,
    tsEnvelope: zeta < 1 ? -Math.log(eps * Math.sqrt(1 - zeta * zeta)) / sigma : null,
    theta: Math.asin(Math.min(1, zeta)),
  };
}

// Exact first-order results for σ/(s + σ).
export function firstOrderExact(sigma, eps = 0.01) {
  return { rise: Math.log(9) / sigma, Mp: 0, tp: null, ts: -Math.log(eps) / sigma, tau: 1 / sigma };
}
