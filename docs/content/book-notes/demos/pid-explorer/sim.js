// Time-domain simulation and step-response metrics. No DOM dependencies.
//
// All four closed-loop transfer functions share the denominator a(s), so one
// controllable canonical realisation of 1/a(s) carries every response; each
// numerator only adds its own output row c and feedthrough d.

import { divide, strip } from './poly.js';

// --- Limits (plan Section 3.5 and 3.6) --------------------------------------
export const SAMPLES = 4000;             // output samples per horizon; each is one exact step
export const EXPM_THETA = 5.37;         // scale M so its norm estimate is below this (Pade-13 accuracy limit)
export const EXPM_POWER_ORDER = 5;       // norm estimate uses ||M^k||^(1/k) for k = 4, 5 (Al-Mohy and Higham)
export const PADE_DEGREE = 13;
export const HORIZON_REF_RADIANS = 200;  // horizon <= 200 / (slowest nonzero closed-loop |pole|)
export const HORIZON_DECAY_TAUS = 8;     // horizon <= 8 / (slowest stable decay rate)
export const PLANT_CLIP_MIN_TAUS = 1;    // horizon >= 1 slowest-plant-pole time constants
export const PLANT_CLIP_MAX_TAUS = 50;   // horizon <= 50 slowest-plant-pole time constants
export const HORIZON_PERIODS = 5;        // marginal/unstable: periods of the rightmost complex pair shown
export const HORIZON_E_FOLDS = 3;        // ... stretched to this many e-foldings of growth when that is longer
export const HORIZON_MAX_PERIODS = 15;   // ... but never beyond this many periods (keeps cycles legible near K_u)
export const DIVERGENCE_MAX_GROWTH = 1e3; // ... and never more than this growth factor (no overflow)
export const DEFAULT_HORIZON = 10;       // used when the loop has no dynamics at all
export const RISE_LOW = 0.1;
export const RISE_HIGH = 0.9;
export const SETTLING_BAND = 0.01;       // the 1% band used in the course notes
export const MIN_FINAL_VALUE = 1e-9;     // |y_inf| below this makes relative metrics undefined
const RATE_FLOOR = 1e-6;                 // decay rates below this are not "stable poles"

// --- Horizon ---------------------------------------------------

/**
 * Pick the simulation horizon.
 *
 * Stable loop: T = min(200 / omega_ref, 8 / sigma_min), clipped to a range set
 * by the slowest plant pole. omega_ref is the slowest nonzero closed-loop
 * |lambda| (so a lightly damped slow pair gets 200 radians of oscillation) and
 * sigma_min the slowest decay rate among stable poles.
 *
 * Marginal or unstable loop: the rightmost pole decides what the student must
 * see. For a complex pair T covers HORIZON_PERIODS periods, stretched towards
 * HORIZON_E_FOLDS e-foldings of growth but never past HORIZON_MAX_PERIODS, so a
 * loop just above K_u shows a slowly growing oscillation rather than thousands
 * of aliased cycles. For a real pole T is HORIZON_PERIODS / sigma, clipped by
 * the slowest stable plant time constant like the stable rule. Either way T is capped
 * so that exp(sigma T) stays below DIVERGENCE_MAX_GROWTH (visible, finite).
 * A real pole exactly at the origin (type-1 loop at zero gain) is not treated
 * as unstable: it falls through to the stable rule.
 *
 * A positive `override` replaces either rule.
 */
export function chooseHorizon(cl, override = null) {
  if (override > 0) return override;
  const rightmost = cl.poles.reduce((w, p) => (p.re > w.re + RATE_FLOOR || (Math.abs(p.re - w.re) <= RATE_FLOOR && p.im > w.im) ? p : w), cl.poles[0] ?? { re: -Infinity, im: 0 });
  if (rightmost.re > -RATE_FLOOR && (rightmost.im > RATE_FLOOR || rightmost.re > RATE_FLOOR)) {
    return unstableHorizon(cl, rightmost);
  }
  return stableHorizon(cl);
}

/**
 * Time constant of the slowest plant pole with a nonzero real part, or null.
 * With `stableOnly`, right-half-plane plant poles are ignored, so an unstable
 * plant pole cannot set its own clip.
 */
function slowestPlantTau(cl, stableOnly = false) {
  const rates = cl.plantPoles
    .filter((p) => (stableOnly ? p.re < -RATE_FLOOR : Math.abs(p.re) > RATE_FLOOR))
    .map((p) => Math.abs(p.re));
  return rates.length ? 1 / Math.min(...rates) : null;
}

function unstableHorizon(cl, p) {
  const sigma = Math.max(p.re, 0);
  const growing = sigma > RATE_FLOOR;
  let horizon;
  if (p.im > RATE_FLOOR) {
    const period = (2 * Math.PI) / p.im;
    horizon = HORIZON_PERIODS * period;
    if (growing) horizon = Math.max(horizon, Math.min(HORIZON_E_FOLDS / sigma, HORIZON_MAX_PERIODS * period));
  } else {
    horizon = HORIZON_PERIODS / sigma;
    const tau = slowestPlantTau(cl, true);
    if (tau !== null) horizon = Math.min(horizon, PLANT_CLIP_MAX_TAUS * tau);
  }
  if (growing) horizon = Math.min(horizon, Math.log(DIVERGENCE_MAX_GROWTH) / sigma);
  return horizon;
}

function stableHorizon(cl) {
  const magnitudes = cl.poles.map((p) => Math.hypot(p.re, p.im)).filter((m) => m > RATE_FLOOR);
  if (magnitudes.length === 0) return DEFAULT_HORIZON;
  let horizon = HORIZON_REF_RADIANS / Math.min(...magnitudes);
  const decay = cl.poles.filter((p) => p.re < -RATE_FLOOR).map((p) => -p.re);
  if (decay.length) horizon = Math.min(horizon, HORIZON_DECAY_TAUS / Math.min(...decay));
  const tau = slowestPlantTau(cl);
  if (tau !== null) {
    horizon = Math.min(Math.max(horizon, PLANT_CLIP_MIN_TAUS * tau), PLANT_CLIP_MAX_TAUS * tau);
  }
  return horizon;
}

// --- State-space realisation -------------------------------------------------

/**
 * Output row for numerator q over monic a of degree n:
 * y = c . x + d u, with d the constant part of the quotient q / a.
 * `impulse` is true when q has higher degree than a (the quotient contains s
 * terms, i.e. Dirac impulses, which a state-space model cannot represent).
 */
function outputRow(q, aMonic) {
  const n = aMonic.length - 1;
  const { quot, rem } = divide(q.length ? q : [0], aMonic);
  const padded = new Array(n - rem.length).fill(0).concat(rem); // s^(n-1) ... s^0
  return {
    c: Float64Array.from(padded.reverse()),                      // c[k] multiplies x_(k+1)
    d: quot.length ? quot[quot.length - 1] : 0,
    impulse: quot.length > 1,
  };
}

// --- Exact zero-order-hold stepping ------------------------------------------
//
// With a constant (unit step) input, x' = A x + b has the exact one-step map
// x_next = Phi x + Gamma, where [Phi Gamma; 0 1] = expm([A b; 0 0] dt). Unlike a
// fixed-step Runge-Kutta rule this is stable for any stable loop, however stiff.

const identity = (n) => Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));

function matMul(X, Y) {
  const n = X.length;
  return X.map((row) => Array.from({ length: n }, (_, j) => row.reduce((acc, v, k) => acc + v * Y[k][j], 0)));
}

const matAdd = (X, Y, c = 1) => X.map((row, i) => row.map((v, j) => v + c * Y[i][j]));
const norm1 = (X) => Math.max(...X[0].map((_, j) => X.reduce((acc, row) => acc + Math.abs(row[j]), 0)));

/** Solve X Z = B for Z by Gaussian elimination with partial pivoting. */
function solve(X, B) {
  const n = X.length;
  const A = X.map((row, i) => [...row, ...B[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
    [A[c], A[p]] = [A[p], A[c]];
    for (let r = c + 1; r < n; r++) {
      const f = A[r][c] / A[c][c];
      for (let k = c; k < 2 * n; k++) A[r][k] -= f * A[c][k];
    }
  }
  const Z = Array.from({ length: n }, () => new Array(n).fill(0));
  for (let col = 0; col < n; col++) {
    for (let r = n - 1; r >= 0; r--) {
      let acc = A[r][n + col];
      for (let k = r + 1; k < n; k++) acc -= A[r][k] * Z[k][col];
      Z[r][col] = acc / A[r][r];
    }
  }
  return Z;
}

/**
 * Scale factor exponent for expm: ||M^k||^(1/k) for k = 4, 5 is a much tighter
 * size estimate than ||M|| for the non-normal companion matrices used here, so
 * far fewer squarings (each of which amplifies rounding error) are needed.
 */
function squaringsFor(M) {
  let power = M;
  let estimate = 0;
  for (let k = 2; k <= EXPM_POWER_ORDER; k++) {
    power = matMul(power, M);
    if (k >= EXPM_POWER_ORDER - 1) estimate = Math.max(estimate, norm1(power) ** (1 / k));
  }
  return Math.max(0, Math.ceil(Math.log2(estimate / EXPM_THETA)));
}

/** Matrix exponential: scaling and squaring around a degree-13 Pade approximant. */
export function expm(M) {
  const n = M.length;
  const squarings = squaringsFor(M);
  const scaled = M.map((row) => row.map((v) => v / 2 ** squarings));
  let term = identity(n);
  let num = identity(n);
  let den = identity(n);
  let coeff = 1;
  for (let k = 1; k <= PADE_DEGREE; k++) {
    coeff *= (PADE_DEGREE - k + 1) / (k * (2 * PADE_DEGREE - k + 1));
    term = matMul(term, scaled);
    num = matAdd(num, term, coeff);
    den = matAdd(den, term, k % 2 ? -coeff : coeff);
  }
  let result = solve(den, num);
  for (let i = 0; i < squarings; i++) result = matMul(result, result);
  return result;
}

/**
 * Exact one-step map for the companion form of 1/a (x_k' = x_(k+1),
 * x_n' = -a . x + u) under a constant input over dt. aLow lists a_0 ... a_(n-1)
 * of the monic polynomial. Returns {Phi, Gamma}.
 */
export function zohMatrices(aLow, dt) {
  const n = aLow.length;
  const M = Array.from({ length: n + 1 }, () => new Array(n + 1).fill(0));
  for (let k = 0; k < n - 1; k++) M[k][k + 1] = dt;
  for (let k = 0; k < n; k++) M[n - 1][k] = -aLow[k] * dt;
  if (n > 0) M[n - 1][n] = dt;
  const E = expm(M);
  return { Phi: E.slice(0, n).map((r) => r.slice(0, n)), Gamma: E.slice(0, n).map((r) => r[n]) };
}

const dot = (c, x) => c.reduce((s, ck, k) => s + ck * x[k], 0);

/**
 * Unit-step response of the chosen input ('ref' or 'dist').
 * Returns {t, y, u, T, dt, impulseU, impulseY, valid} with t, y, u as Float64Arrays.
 * `valid` is false if any sample is non-finite.
 */
export function simulate(cl, input, horizonOverride = null) {
  const [yNum, uNum] = input === 'dist' ? [cl.tf.YW, cl.tf.UW] : [cl.tf.YR, cl.tf.UR];
  const lead = cl.a[0];
  const aMonic = cl.a.map((c) => c / lead);
  const rowY = outputRow(strip(yNum).map((c) => c / lead), aMonic);
  const rowU = outputRow(strip(uNum).map((c) => c / lead), aMonic);
  const n = aMonic.length - 1;
  const aLow = aMonic.slice(1).reverse(); // a_0 ... a_(n-1)

  const T = chooseHorizon(cl, horizonOverride);
  const dt = T / SAMPLES;
  const { Phi, Gamma } = zohMatrices(aLow, dt);
  const count = SAMPLES + 1;
  const t = new Float64Array(count);
  const y = new Float64Array(count);
  const u = new Float64Array(count);
  let x = new Array(n).fill(0);
  for (let i = 0; i < count; i++) {
    t[i] = i * dt;
    y[i] = dot(rowY.c, x) + rowY.d;
    u[i] = dot(rowU.c, x) + rowU.d;
    x = Phi.map((row, r) => dot(row, x) + Gamma[r]);
  }
  const valid = [t, y, u].every((series) => series.every(Number.isFinite));
  return { t, y, u, T, dt, impulseU: rowU.impulse, impulseY: rowY.impulse, valid };
}

// --- Metrics -----------------------------------------------------------------

/** y(infinity) by the Final Value Theorem, or null unless the loop is stable. */
export function finalValue(cl, input) {
  if (cl.stability !== 'stable') return null;
  const num = strip(input === 'dist' ? cl.tf.YW : cl.tf.YR);
  return num.length ? num[num.length - 1] / cl.a[cl.a.length - 1] : 0;
}

/** First time the series crosses `level` upward, by linear interpolation, or null. */
function firstCrossing(t, y, level) {
  for (let i = 1; i < y.length; i++) {
    if (y[i - 1] < level && y[i] >= level) {
      return t[i - 1] + ((level - y[i - 1]) / (y[i] - y[i - 1])) * (t[i] - t[i - 1]);
    }
  }
  return y[0] >= level ? t[0] : null;
}

/** Last time |y - yInf| exceeds the band (interpolated), 0 if never, null if still outside at the end. */
function settlingTime(t, y, yInf, band) {
  let last = -1;
  for (let i = 0; i < y.length; i++) if (Math.abs(y[i] - yInf) > band) last = i;
  if (last < 0) return 0;
  if (last === y.length - 1) return null;
  const e0 = Math.abs(y[last] - yInf);
  const e1 = Math.abs(y[last + 1] - yInf);
  return t[last] + ((e0 - band) / (e0 - e1)) * (t[last + 1] - t[last]);
}

/**
 * Step-response metrics. Every entry is null when undefined (unstable or
 * marginal loop, y_inf = 0, horizon too short, non-finite or improper
 * simulation), never zero by default.
 * Returns {yInf, ess, tr, Mp, ts, umax, band}; Mp is a percentage and `band`
 * is the half-width of the settling band around y_inf.
 */
export function computeMetrics(cl, trace, input) {
  const empty = { yInf: null, ess: null, tr: null, Mp: null, ts: null, umax: null, band: null };
  const yInf = finalValue(cl, input);
  if (yInf === null || !trace.valid || trace.impulseY) return empty;
  const umax = trace.impulseU ? null : trace.u.reduce((m, v) => Math.max(m, Math.abs(v)), 0);
  const { t, y } = trace;

  if (input === 'dist') {
    const peak = y.reduce((m, v) => Math.max(m, Math.abs(v)), 0);
    const band = SETTLING_BAND * peak;
    const ts = peak > MIN_FINAL_VALUE ? settlingTime(t, y, yInf, band) : null;
    return { ...empty, yInf, ess: yInf, ts, umax, band };
  }
  const band = SETTLING_BAND * Math.abs(yInf);
  const out = { ...empty, yInf, ess: 1 - yInf, umax, band };
  if (Math.abs(yInf) < MIN_FINAL_VALUE) return out;

  const yn = y.map((v) => v / yInf); // normalised so the target is +1 for either sign of y_inf
  const t10 = firstCrossing(t, yn, RISE_LOW);
  const t90 = firstCrossing(t, yn, RISE_HIGH);
  const overshoot = 100 * (yn.reduce((m, v) => Math.max(m, v), -Infinity) - 1);
  return {
    ...out,
    tr: t10 !== null && t90 !== null ? t90 - t10 : null,
    Mp: overshoot > 0 ? overshoot : null,
    ts: settlingTime(t, yn, 1, SETTLING_BAND),
  };
}

/** Convenience: simulate and compute metrics in one call. */
export function runLoop(cl, input, horizonOverride = null) {
  const trace = simulate(cl, input, horizonOverride);
  return { trace, metrics: computeMetrics(cl, trace, input) };
}
