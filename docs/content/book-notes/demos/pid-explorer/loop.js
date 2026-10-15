// Plant / controller / closed-loop assembly, root-locus sampling and the
// Ziegler-Nichols ultimate-gain search. No DOM dependencies (runs under Node).
//
// Notation follows the course notes: plant G = K N(s)/D(s), controller
// Dc = Nc/Dden, reference R, disturbance W at the plant input, output Y, control U.
//
//   a(s) = Dden D + Nc K N
//   Y/R = Nc K N / a     U/R = Nc D / a
//   Y/W = Dden K N / a   U/W = -Nc K N / a
//
// A plant marker is {re, im, fixed?}. A marker with im > 0 stands for the
// conjugate pair re +/- j im; im === 0 is a real pole or zero.

import {
  add, degree, fromRoots, maxRealPart, mul, roots, scale, strip,
} from './poly.js';

// --- Tolerances and limits ---------------------------------------------------
export const STABILITY_TOL = 1e-6;        // |Re| below this counts as marginal
export const DEFAULT_FILTER_N = 10;       // T_f = T_D / N, matching the tuning note
export const LOCUS_SAMPLES = 200;         // geometric gain samples (plus k = 0)
export const LOCUS_SPAN = 10;             // sweep out to this multiple of the slider value
export const LOCUS_FALLBACK_TOP = 1;      // sweep limit when the active gain is 0
export const LOCUS_MIN_FRACTION = 1e-4;   // smallest nonzero k, as a fraction of the top
export const ZN_K_MIN = 1e-4;
export const ZN_SCAN_POINTS = 600;
export const ZN_BISECT_ITER = 200;
export const ZN_BISECT_REL_TOL = 1e-14;
export const ZN_OMEGA_MIN = 1e-6;         // crossing frequency below this is a real-axis crossing

export const GAIN_NAMES = ['kP', 'kI', 'kD'];

// --- Plant -------------------------------------------------------------------

/**
 * Expand the plant markers into polynomials.
 * Returns {ok, N, D, K, num, den, relDegree} or {ok: false, error}.
 */
export function plantPolys(plant) {
  const N = fromRoots(plant.zeros);
  const D = fromRoots(plant.poles);
  if (degree(N) > degree(D)) {
    return { ok: false, error: 'The plant has more zeros than poles; add a pole or remove a zero.' };
  }
  return {
    ok: true, N, D, K: plant.K,
    num: scale(N, plant.K), den: D,
    relDegree: degree(D) - degree(N),
  };
}

/** K that makes G(0) = 1, or null when G has a pole or zero at the origin. */
export function unitDcGain(plant) {
  const N0 = fromRoots(plant.zeros).at(-1);
  const D0 = fromRoots(plant.poles).at(-1);
  return Math.abs(N0) > 0 && Math.abs(D0) > 0 ? D0 / N0 : null;
}

// --- Controller --------------------------------------------------------------

/**
 * Fixed polynomials of the controller, with Dc = (kP nP + kI nI + kD nD) / den.
 *
 * Ideal:    den = s,          nP = s,          nI = 1,         nD = s^2
 * Filtered: den = s(Tf s+1),  nP = s(Tf s+1),  nI = Tf s+1,    nD = s^2
 * with Tf = kD / (N kP). If dropIntegrator is set (kI = 0), the common factor s
 * is cancelled so PD does not carry a spurious pole at the origin.
 */
export function controllerParts({ filter, N, kP, kD }, dropIntegrator) {
  const filterRequested = Boolean(filter);
  const Tf = filterRequested && kP > 0 && kD > 0 ? kD / (N * kP) : 0;
  const lag = Tf > 0 ? [Tf, 1] : [1];
  const parts = dropIntegrator
    ? { den: lag, nP: lag, nI: [0], nD: [1, 0] }
    : { den: mul([1, 0], lag), nP: mul([1, 0], lag), nI: lag, nD: [1, 0, 0] };
  return { ...parts, Tf, filterRequested, filtered: Tf > 0 };
}

const numeratorOf = (parts, g) => strip(
  add(add(scale(parts.nP, g.kP), scale(parts.nI, g.kI)), scale(parts.nD, g.kD)),
);

// --- Closed loop -------------------------------------------------------------

/**
 * Assemble everything the app needs for one set of gains.
 * options = {filter, N}. Returns {ok: false, error} for an invalid plant.
 */
export function closedLoop(plant, gains, options = {}) {
  const asm = assemble(plant, gains, options, gains.kI === 0);
  if (!asm.ok) return asm;
  const { pp, parts } = asm;
  const Nc = numeratorOf(parts, gains);
  const a = strip(add(mul(parts.den, pp.den), mul(Nc, pp.num)));
  const poles = roots(a);
  return {
    ok: true,
    plant: pp, parts, Nc, a, poles,
    plantPoles: roots(pp.den),
    ctrlZeros: roots(Nc),
    ctrlPoles: roots(parts.den),
    tf: {
      YR: mul(Nc, pp.num),
      UR: mul(Nc, pp.den),
      YW: mul(parts.den, pp.num),
      UW: scale(mul(Nc, pp.num), -1),
    },
    stability: classifyStability(poles),
  };
}

/** Plant polynomials and controller parts for one set of gains; shared by closedLoop and locusSplit. */
function assemble(plant, gains, options, dropIntegrator) {
  const pp = plantPolys(plant);
  if (!pp.ok) return pp;
  const parts = controllerParts(
    { filter: options.filter, N: options.N ?? DEFAULT_FILTER_N, kP: gains.kP, kD: gains.kD },
    dropIntegrator,
  );
  return { ok: true, pp, parts };
}

export function classifyStability(poles) {
  const m = maxRealPart(poles);
  if (m > STABILITY_TOL) return 'unstable';
  if (m > -STABILITY_TOL) return 'marginal';
  return 'stable';
}

/** Natural frequency, damping ratio, etc. for the tooltip on a closed-loop pole. */
export function poleInfo(p) {
  const wn = Math.hypot(p.re, p.im);
  return { sigma: p.re, wd: Math.abs(p.im), wn, zeta: wn > 0 ? -p.re / wn : NaN };
}

// --- Root locus of one gain --------------------------------------------------

/**
 * Affine split a(s) = a0(s) + k b(s) for the active gain, other gains held
 * fixed (and T_f held fixed when the filter is on).
 */
export function locusSplit(plant, gains, options, active) {
  const asm = assemble(plant, gains, options, gains.kI === 0 && active !== 'kI');
  if (!asm.ok) return asm;
  const { pp, parts } = asm;
  const terms = { kP: parts.nP, kI: parts.nI, kD: parts.nD };
  const others = { kP: 0, kI: 0, kD: 0 };
  for (const g of GAIN_NAMES) if (g !== active) others[g] = gains[g];
  const a0 = strip(add(mul(parts.den, pp.den), mul(numeratorOf(parts, others), pp.num)));
  const b = strip(mul(terms[active], pp.num));
  return { ok: true, a0, b };
}

/**
 * 'path' when the filter is on and the active gain is kP or kD: T_f = kD/(N kP)
 * moves with those gains, so the affine locus would not be where the poles go.
 * Otherwise 'locus' (the standard root locus, T_f fixed or irrelevant).
 */
export const locusKind = (options, active) => (options.filter && active !== 'kI' ? 'path' : 'locus');

/**
 * Closed-loop roots for k on {0} plus a geometric grid up to LOCUS_SPAN x the slider value.
 * Follows the true pole path (re-assembling the loop at every k) when locusKind is 'path'.
 */
export function sampleLocus(plant, gains, options, active, samples = LOCUS_SAMPLES) {
  const split = locusSplit(plant, gains, options, active);
  if (!split.ok) return [];
  const rootsAt = locusKind(options, active) === 'path'
    ? (k) => closedLoop(plant, { ...gains, [active]: k }, options).poles
    : (k) => roots(strip(add(split.a0, scale(split.b, k))));
  const top = LOCUS_SPAN * (gains[active] > 0 ? gains[active] : LOCUS_FALLBACK_TOP);
  const ratio = Math.pow(LOCUS_MIN_FRACTION, -1);
  const out = [];
  const path = locusKind(options, active) === 'path';
  // In path mode k = 0 is a different controller (T_f = 0) from k -> 0+ (T_f -> infinity): start at the first grid point.
  for (let i = path ? 1 : 0; i <= samples; i++) {
    const k = i === 0 ? 0 : top * Math.pow(ratio, (i - samples) / (samples - 1));
    out.push({ k, roots: rootsAt(k) });
  }
  return out;
}

// --- Ziegler-Nichols ultimate sensitivity -----------------------------------

/**
 * Sweep a P-only gain upward and find the first imaginary-axis crossing of the
 * closed-loop poles. Returns {found: true, Ku, Pu, omegaU} or {found: false, reason}.
 */
export function ultimateGain(plant, kMax) {
  const pp = plantPolys(plant);
  if (!pp.ok) return { found: false, reason: pp.error };
  const worstRoot = (k) => {
    const z = roots(strip(add(pp.den, scale(pp.num, k))));
    return z.length ? z.reduce((w, r) => (r.re > w.re ? r : w)) : { re: -Infinity, im: 0 };
  };
  const ratio = Math.pow(kMax / ZN_K_MIN, 1 / (ZN_SCAN_POINTS - 1));
  if (worstRoot(ZN_K_MIN).re >= -STABILITY_TOL) {
    return { found: false, reason: 'The P-only loop is already marginal or unstable at small gain, so there is no stable-to-unstable boundary to find.' };
  }
  let lo = ZN_K_MIN;
  for (let i = 1; i < ZN_SCAN_POINTS; i++) {
    const hi = ZN_K_MIN * Math.pow(ratio, i);
    if (worstRoot(hi).re >= 0) return refineCrossing(worstRoot, lo, hi);
    lo = hi;
  }
  return { found: false, reason: `The P-only loop stays stable for every k_P up to ${kMax}, so there is no ultimate gain.` };
}

function refineCrossing(worstRoot, lo, hi) {
  for (let i = 0; i < ZN_BISECT_ITER && hi - lo > ZN_BISECT_REL_TOL * hi; i++) {
    const mid = 0.5 * (lo + hi);
    if (worstRoot(mid).re < 0) lo = mid; else hi = mid;
  }
  const omegaU = Math.abs(worstRoot(hi).im);
  if (omegaU < ZN_OMEGA_MIN) {
    return { found: false, reason: 'The loop goes unstable through the origin (a real root), so it never oscillates and has no ultimate period.' };
  }
  return { found: true, Ku: hi, omegaU, Pu: (2 * Math.PI) / omegaU };
}

/** Table 4.3 PID row: kP = 0.6 Ku, TI = Pu/2, TD = Pu/8; kI = kP/TI, kD = kP TD. */
export function znGains(Ku, Pu) {
  const kP = 0.6 * Ku;
  const TI = Pu / 2;
  const TD = Pu / 8;
  return { kP, kI: kP / TI, kD: kP * TD, TI, TD };
}
