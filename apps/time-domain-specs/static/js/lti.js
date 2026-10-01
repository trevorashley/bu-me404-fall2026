// Linear time-invariant systems described by poles, zeros and a gain.
//
// A system is { poles, zeros, gain } where poles and zeros are lists of
// {re, im, pair?} with im >= 0; an entry with pair: true (or im > 0) stands
// for the conjugate pair re ± j·im, which is a double real root when im = 0. gain === null means "choose K so that H(0) = 1" whenever no pole or
// zero sits at the origin.
//
// Responses are computed by exact zero-order-hold discretisation of a
// controllable-canonical state-space realisation, so they are exact at the
// sample instants (no integration error) and repeated poles need no special case.

import { C, sub, mul, div, abs, scale } from "./complex.js";
import { fromRoots, polyval, polyvalC } from "./poly.js";

export const ORIGIN_TOL = 1e-9;

export const isPair = (r) => Boolean(r.pair) || r.im > 0;
export const order = (list) => list.reduce((n, r) => n + (isPair(r) ? 2 : 1), 0);

export function expand(list) {
  const out = [];
  for (const r of list) {
    if (isPair(r)) out.push(C(r.re, r.im), C(r.re, -r.im));
    else out.push(C(r.re, 0));
  }
  return out;
}

const atOrigin = (r) => Math.abs(r.re) < ORIGIN_TOL && Math.abs(r.im) < ORIGIN_TOL;

// Numerator and denominator polynomials and the gain actually used.
export function tf(sys) {
  const P = expand(sys.poles);
  const Z = expand(sys.zeros);
  const den = fromRoots(P);
  const monicNum = fromRoots(Z);
  let K = sys.gain;
  let normalized = false;
  if (K === null || K === undefined) {
    const n0 = polyval(monicNum, 0);
    const d0 = polyval(den, 0);
    if (Math.abs(n0) > 1e-14 && Math.abs(d0) > 1e-14) {
      K = d0 / n0;
      normalized = true;
    } else {
      K = 1;
    }
  }
  const num = monicNum.map((c) => c * K);
  return { num, den, K, normalized, P, Z };
}

// Evaluate H(s) at a complex point.
export function evalH(sys, s) {
  const { num, den } = tf(sys);
  return div(polyvalC(num, s), polyvalC(den, s));
}

// ---------------------------------------------------------------- state space

export function stateSpace(num, den) {
  const n = den.length - 1;
  if (num.length - 1 > n) throw new Error("improper: more zeros than poles");
  const a0 = den[0];
  const a = den.map((c) => c / a0);
  const b = new Array(n + 1 - num.length).fill(0).concat(num.map((c) => c / a0));
  const D = b[0];
  const A = zeros(n, n);
  for (let j = 0; j < n; j++) A[0][j] = -a[j + 1];
  for (let i = 1; i < n; i++) A[i][i - 1] = 1;
  const B = new Array(n).fill(0);
  if (n > 0) B[0] = 1;
  const Cv = new Array(n);
  for (let j = 0; j < n; j++) Cv[j] = b[j + 1] - D * a[j + 1];
  return { A, B, C: Cv, D, n };
}

function zeros(r, c) {
  return Array.from({ length: r }, () => new Array(c).fill(0));
}

function matmul(X, Y) {
  const r = X.length, m = Y.length, c = Y[0].length;
  const Z = zeros(r, c);
  for (let i = 0; i < r; i++)
    for (let k = 0; k < m; k++) {
      const x = X[i][k];
      if (x === 0) continue;
      for (let j = 0; j < c; j++) Z[i][j] += x * Y[k][j];
    }
  return Z;
}

// Solve P X = Q by Gaussian elimination with partial pivoting.
function solve(P, Q) {
  const n = P.length, c = Q[0].length;
  const M = P.map((row, i) => row.concat(Q[i]));
  for (let k = 0; k < n; k++) {
    let piv = k;
    for (let i = k + 1; i < n; i++) if (Math.abs(M[i][k]) > Math.abs(M[piv][k])) piv = i;
    [M[k], M[piv]] = [M[piv], M[k]];
    const d = M[k][k];
    for (let i = k + 1; i < n; i++) {
      const f = M[i][k] / d;
      if (f === 0) continue;
      for (let j = k; j < n + c; j++) M[i][j] -= f * M[k][j];
    }
  }
  const X = zeros(n, c);
  for (let i = n - 1; i >= 0; i--)
    for (let j = 0; j < c; j++) {
      let s = M[i][n + j];
      for (let k = i + 1; k < n; k++) s -= M[i][k] * X[k][j];
      X[i][j] = s / M[i][i];
    }
  return X;
}

// Matrix exponential: diagonal Padé(6) approximant with scaling and squaring.
export function expm(Min) {
  const n = Min.length;
  let norm = 0;
  for (let j = 0; j < n; j++) {
    let s = 0;
    for (let i = 0; i < n; i++) s += Math.abs(Min[i][j]);
    norm = Math.max(norm, s);
  }
  const sq = Math.max(0, Math.ceil(Math.log2(norm / 0.5)) + 1);
  const f = 2 ** -sq;
  const M = Min.map((r) => r.map((x) => x * f));
  const q = 6;
  let c = 1;
  let X = M;
  const I = zeros(n, n).map((r, i) => (r[i] = 1, r));
  const N = I.map((r) => r.slice());
  const Dn = I.map((r) => r.slice());
  for (let k = 1; k <= q; k++) {
    c = (c * (q - k + 1)) / (k * (2 * q - k + 1));
    if (k > 1) X = matmul(M, X);
    const sgn = k % 2 === 0 ? 1 : -1;
    for (let i = 0; i < n; i++)
      for (let j = 0; j < n; j++) {
        N[i][j] += c * X[i][j];
        Dn[i][j] += sgn * c * X[i][j];
      }
  }
  let E = solve(Dn, N);
  for (let k = 0; k < sq; k++) E = matmul(E, E);
  return E;
}

// ---------------------------------------------------------------- responses

// input: "step" or "impulse"; amp scales the input (e.g. -1 for the 747).
export function simulate(sys, { input = "step", amp = 1, T, N = 2000 }) {
  const { num, den } = tf(sys);
  const ss = stateSpace(num, den);
  const t = new Float64Array(N);
  const y = new Float64Array(N);
  const h = T / (N - 1);
  for (let k = 0; k < N; k++) t[k] = k * h;
  const n = ss.n;
  if (n === 0) {
    y.fill(input === "step" ? amp * ss.D : 0);
    return { t, y };
  }
  if (input === "impulse" && Math.abs(ss.D) > 1e-12)
    throw new Error("impulse response contains a delta: add a pole or remove a zero");
  const Maug = zeros(n + 1, n + 1);
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) Maug[i][j] = ss.A[i][j] * h;
    Maug[i][n] = ss.B[i] * h;
  }
  const E = expm(Maug);
  const Phi = E.slice(0, n).map((r) => r.slice(0, n));
  const Gam = E.slice(0, n).map((r) => r[n]);
  let x = input === "impulse" ? ss.B.map((b) => b * amp) : new Array(n).fill(0);
  const u = input === "step" ? amp : 0;
  const xn = new Array(n);
  for (let k = 0; k < N; k++) {
    let s = ss.D * u;
    for (let j = 0; j < n; j++) s += ss.C[j] * x[j];
    y[k] = s;
    for (let i = 0; i < n; i++) {
      let v = Gam[i] * u;
      const row = Phi[i];
      for (let j = 0; j < n; j++) v += row[j] * x[j];
      xn[i] = v;
    }
    x = xn.slice();
  }
  return { t, y };
}

// Final value by the final-value theorem, or null when it does not exist.
export function finalValue(sys, input = "step", amp = 1) {
  const { P, Z, K } = tf(sys);
  for (const p of P) {
    if (atOrigin(p)) continue;
    if (p.re > -ORIGIN_TOL) return null; // RHP or imaginary-axis pole
  }
  let n0 = P.filter(atOrigin).length + (input === "step" ? 1 : 0);
  let z0 = Z.filter(atOrigin).length;
  const cancel = Math.min(n0, z0);
  n0 -= cancel;
  z0 -= cancel;
  if (n0 === 0) return 0;
  if (n0 > 1) return null;
  if (z0 > 0) return 0;
  // Y(s) = amp·K·N(s) / (s·∏(s − p_j)) after cancellation, so s·Y(0) is
  // amp·K·∏(−z_i)/∏(−p_j); both products are real for conjugate-symmetric roots.
  let numP = C(1), denP = C(1);
  for (const z of Z) if (!atOrigin(z)) numP = mul(numP, scale(z, -1));
  for (const p of P) if (!atOrigin(p)) denP = mul(denP, scale(p, -1));
  return (amp * K * numP.re) / denP.re;
}

export function isStable(sys) {
  return expand(sys.poles).every((p) => p.re < -ORIGIN_TOL);
}

// A horizon long enough for the slowest stable mode to decay by ~e^-7.
export function autoHorizon(sys) {
  const P = expand(sys.poles);
  const stable = P.filter((p) => p.re < -ORIGIN_TOL);
  if (stable.length === 0) {
    const m = Math.max(0.5, ...P.map((p) => abs(p)));
    return 10 / m;
  }
  const sigmaMin = Math.min(...stable.map((p) => -p.re));
  let T = 7 / sigmaMin;
  const unstable = P.filter((p) => p.re >= -ORIGIN_TOL && !atOrigin(p));
  if (unstable.length) T = Math.min(T, 8 / Math.max(...unstable.map((p) => abs(p))));
  return Math.min(T, 2000);
}

export function samplesFor(sys, T) {
  const wmax = Math.max(1e-6, ...expand(sys.poles).map((p) => abs(p)), ...expand(sys.zeros).map((z) => abs(z)));
  return Math.min(20000, Math.max(2000, Math.ceil(((T * wmax) / (2 * Math.PI)) * 60)));
}

// ---------------------------------------------------------------- modes

// Modal coefficients of the response: y(t) = c0 + Σ C_i e^{p_i t} (step), or
// Σ C_i e^{p_i t} (impulse). Returns one entry per stored pole (pairs merged,
// with the coefficient of the upper-half-plane pole) or {repeated: true}.
export function modes(sys, input = "step", amp = 1) {
  const { P, K } = tf(sys);
  const Z = expand(sys.zeros);
  const scale_ = 1e-6 * Math.max(1, ...P.map(abs));
  for (let i = 0; i < P.length; i++)
    for (let j = i + 1; j < P.length; j++)
      if (abs(sub(P[i], P[j])) < scale_) return { repeated: true };
  // A pole at the origin driven by a step is a double pole of Y(s) at 0 (a ramp term).
  if (input === "step" && P.some(atOrigin)) return { repeated: true, reason: "origin" };
  const out = [];
  for (const r of sys.poles) {
    const p = C(r.re, r.im);
    let v = C(amp * K);
    for (const z of Z) v = mul(v, sub(p, z));
    let d = input === "step" ? p : C(1);
    for (const q of P) if (abs(sub(p, q)) >= scale_) d = mul(d, sub(p, q));
    out.push({ pole: r, coef: div(v, d) });
  }
  const c0 = input === "step" ? finalValue(sys, "step", amp) : 0;
  return { repeated: false, c0, modes: out };
}

// Evaluate one mode's contribution on a time grid.
export function modeCurve(mode, t) {
  const { pole, coef } = mode;
  const y = new Float64Array(t.length);
  for (let k = 0; k < t.length; k++) {
    const e = Math.exp(pole.re * t[k]);
    if (pole.im > 0) {
      const w = pole.im * t[k];
      y[k] = 2 * e * (coef.re * Math.cos(w) - coef.im * Math.sin(w));
    } else y[k] = coef.re * e;
  }
  return y;
}

// ---------------------------------------------------------------- dominant pole(s)

export function dominant(sys) {
  const stable = sys.poles.filter((p) => p.re < -ORIGIN_TOL);
  if (!stable.length) return null;
  let best = stable[0];
  for (const p of stable) if (-p.re < -best.re - 1e-12 || (Math.abs(p.re - best.re) < 1e-12 && p.im > best.im)) best = p;
  const sigma = -best.re;
  const wn = Math.hypot(best.re, best.im);
  return { pole: best, sigma, wn, zeta: sigma / wn, complex: best.im > 0 };
}

// Roots (other than the dominant pole) closer than `factor` times the dominant
// decay rate to the imaginary axis.
export function factorFlags(sys, factor = 4) {
  const dom = dominant(sys);
  if (!dom) return [];
  const flags = [];
  const check = (list, kind) =>
    list.forEach((r, i) => {
      if (kind === "pole" && r === dom.pole) return;
      const ratio = Math.abs(r.re) / dom.sigma;
      flags.push({ kind, index: i, root: r, ratio, near: ratio < factor, rhp: r.re > ORIGIN_TOL });
    });
  check(sys.poles, "pole");
  check(sys.zeros, "zero");
  return flags;
}

// Second-order pole pair from ζ and ωn (ζ < 1 complex pair; ζ ≥ 1 two real poles).
export function pairFromZetaWn(zeta, wn) {
  if (zeta < 1) return [{ re: -zeta * wn, im: wn * Math.sqrt(1 - zeta * zeta), pair: true }];
  const d = wn * Math.sqrt(zeta * zeta - 1);
  return [{ re: -zeta * wn + d, im: 0 }, { re: -zeta * wn - d, im: 0 }];
}
