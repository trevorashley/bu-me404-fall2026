// Polynomial arithmetic and root finding. No DOM dependencies (runs under Node).
//
// A polynomial is an array of real coefficients in DESCENDING powers of s:
// [1, 3, 2] is s^2 + 3s + 2. A complex number is a plain object {re, im}.

// --- Tolerances and limits (plan Section 6) ---------------------------------
export const LEADING_ZERO_REL = 1e-13;   // leading coeff below this fraction of the largest is dropped
export const ABERTH_TOL = 1e-14;         // converged when every correction < ABERTH_TOL * max(1, |z|)
export const ABERTH_MAX_ITER = 500;
export const NEWTON_MAX_STEPS = 10;      // polish stops earlier once the residual stops decreasing
export const REAL_SNAP_TOL = 1e-9;       // |Im| below this (scaled by max(1,|z|)) is snapped to the real axis
const START_ANGLE_OFFSET = 0.4;          // radians; keeps initial guesses off the real axis

// --- Real polynomial arithmetic ---------------------------------------------

/** Drop leading (highest-power) coefficients that are zero or negligible. */
export function strip(p) {
  const scale = Math.max(0, ...p.map(Math.abs));
  let i = 0;
  while (i < p.length && Math.abs(p[i]) <= LEADING_ZERO_REL * scale) i++;
  return p.slice(i);
}

export const degree = (p) => strip(p).length - 1;

export function add(p, q) {
  const n = Math.max(p.length, q.length);
  const out = new Array(n).fill(0);
  for (let i = 0; i < p.length; i++) out[n - p.length + i] += p[i];
  for (let i = 0; i < q.length; i++) out[n - q.length + i] += q[i];
  return out;
}

export const scale = (p, c) => p.map((x) => x * c);

export function mul(p, q) {
  if (p.length === 0 || q.length === 0) return [];
  const out = new Array(p.length + q.length - 1).fill(0);
  for (let i = 0; i < p.length; i++) {
    for (let j = 0; j < q.length; j++) out[i + j] += p[i] * q[j];
  }
  return out;
}

/** Multiply by s^k (append k zero coefficients). */
export const shift = (p, k) => p.concat(new Array(k).fill(0));

/** Value of p at a real or complex point (Horner). Returns {re, im}. */
export function evalComplex(p, z) {
  let re = 0;
  let im = 0;
  for (const c of p) {
    const nr = re * z.re - im * z.im + c;
    im = re * z.im + im * z.re;
    re = nr;
  }
  return { re, im };
}

export function derivative(p) {
  const n = p.length - 1;
  return p.slice(0, n).map((c, i) => c * (n - i));
}

/**
 * Polynomial division p = q*d + r, with deg r < deg d.
 * Returns {quot, rem}; both are stripped of leading zeros (possibly empty).
 */
export function divide(p, d) {
  const dd = strip(d);
  let rem = strip(p).slice();
  if (dd.length === 0) throw new Error('division by the zero polynomial');
  const quot = [];
  while (rem.length >= dd.length) {
    const c = rem[0] / dd[0];
    quot.push(c);
    for (let i = 0; i < dd.length; i++) rem[i] -= c * dd[i];
    rem.shift();
  }
  return { quot, rem: strip(rem) };
}

/**
 * Real polynomial with the given roots. Each root is {re, im}; a root with
 * im > 0 stands for the conjugate pair, so the result is always real.
 */
export function fromRoots(roots) {
  let p = [1];
  for (const r of roots) {
    p = r.im === 0
      ? mul(p, [1, -r.re])
      : mul(p, [1, -2 * r.re, r.re * r.re + r.im * r.im]);
  }
  return p;
}

// --- Root finding -----------------------------------------------------------

/**
 * Roots of a real polynomial as [{re, im}], sorted by real part then by
 * imaginary part (upper half first). Complex roots come in exact conjugate
 * pairs. The zero polynomial and constants have no roots.
 */
export function roots(coeffs) {
  const p = strip(coeffs);
  // Exact zero constant terms are roots at the origin: deflate them exactly.
  let zeros = 0;
  while (p.length > 1 && p[p.length - 1] === 0) {
    p.pop();
    zeros++;
  }
  const found = solveNonzero(p);
  for (let i = 0; i < zeros; i++) found.push({ re: 0, im: 0 });
  return sortRoots(found);
}

function solveNonzero(p) {
  const n = p.length - 1;
  if (n < 1) return [];
  if (n === 1) return [{ re: -p[1] / p[0], im: 0 }];
  if (n === 2) return solveQuadratic(p);
  return pairConjugates(polish(p, aberth(p)));
}

function solveQuadratic([a, b, c]) {
  const disc = b * b - 4 * a * c;
  if (disc >= 0) {
    // Avoid cancellation: compute the larger-magnitude root first.
    const q = -0.5 * (b + Math.sign(b || 1) * Math.sqrt(disc));
    return q === 0
      ? [{ re: 0, im: 0 }, { re: 0, im: 0 }]
      : [{ re: q / a, im: 0 }, { re: c / q, im: 0 }];
  }
  const re = -b / (2 * a);
  const im = Math.sqrt(-disc) / (2 * Math.abs(a));
  return [{ re, im }, { re, im: -im }];
}

/** Aberth-Ehrlich simultaneous iteration on the monic form of p. */
function aberth(p) {
  const n = p.length - 1;
  const monic = p.map((c) => c / p[0]);
  const bound = 1 + Math.max(...monic.slice(1).map(Math.abs)); // Cauchy bound
  const dp = derivative(monic);
  const z = [];
  for (let k = 0; k < n; k++) {
    const ang = (2 * Math.PI * k) / n + START_ANGLE_OFFSET;
    z.push({ re: bound * Math.cos(ang), im: bound * Math.sin(ang) });
  }
  for (let iter = 0; iter < ABERTH_MAX_ITER; iter++) {
    let converged = true;
    const next = z.map((zi, i) => {
      const w = newtonRatio(monic, dp, zi);
      if (w === null) return zi;
      // Sum of 1/(z_i - z_j) over the other approximations.
      let sr = 0;
      let si = 0;
      for (let j = 0; j < n; j++) {
        if (j === i) continue;
        const dr = zi.re - z[j].re;
        const di = zi.im - z[j].im;
        const d2 = dr * dr + di * di || Number.EPSILON;
        sr += dr / d2;
        si += -di / d2;
      }
      // delta = w / (1 - w*S)
      const dr = 1 - (w.re * sr - w.im * si);
      const di = -(w.re * si + w.im * sr);
      const den = dr * dr + di * di || Number.EPSILON;
      const delta = {
        re: (w.re * dr + w.im * di) / den,
        im: (w.im * dr - w.re * di) / den,
      };
      if (Math.hypot(delta.re, delta.im) > ABERTH_TOL * Math.max(1, Math.hypot(zi.re, zi.im))) converged = false;
      return { re: zi.re - delta.re, im: zi.im - delta.im };
    });
    for (let i = 0; i < n; i++) z[i] = next[i];
    if (converged) break;
  }
  return z;
}

/** p(z)/p'(z), or null when p(z) is exactly zero or p'(z) vanishes. */
function newtonRatio(p, dp, z) {
  const f = evalComplex(p, z);
  if (f.re === 0 && f.im === 0) return null;
  const g = evalComplex(dp, z);
  const den = g.re * g.re + g.im * g.im;
  if (den === 0) return null;
  return {
    re: (f.re * g.re + f.im * g.im) / den,
    im: (f.im * g.re - f.re * g.im) / den,
  };
}

/** Newton steps on the original (unnormalised) polynomial, kept only while |p(z)| decreases. */
function polish(p, z) {
  const dp = derivative(p);
  const residual = (w) => Math.hypot(evalComplex(p, w).re, evalComplex(p, w).im);
  return z.map((zi) => {
    let cur = zi;
    let res = residual(cur);
    for (let k = 0; k < NEWTON_MAX_STEPS; k++) {
      const w = newtonRatio(p, dp, cur);
      if (w === null) break;
      const next = { re: cur.re - w.re, im: cur.im - w.im };
      const nextRes = residual(next);
      if (!(nextRes < res)) break;
      cur = next;
      res = nextRes;
    }
    return cur;
  });
}

/**
 * Snap near-real roots to the real axis, then pair the rest into conjugates
 * (nearest match) and average each pair so the two are exact mirror images.
 */
function pairConjugates(z) {
  const out = [];
  const upper = [];
  let lower = [];
  for (const r of z) {
    if (Math.abs(r.im) < REAL_SNAP_TOL * Math.max(1, Math.hypot(r.re, r.im))) {
      out.push({ re: r.re, im: 0 });
    } else if (r.im > 0) upper.push(r);
    else lower.push(r);
  }
  for (const u of upper) {
    let best = -1;
    let bestDist = Infinity;
    lower.forEach((l, k) => {
      const d = Math.hypot(u.re - l.re, u.im + l.im);
      if (d < bestDist) { bestDist = d; best = k; }
    });
    if (best < 0) { out.push({ re: u.re, im: 0 }); continue; } // unmatched: treat as real
    const l = lower[best];
    lower = lower.filter((_, k) => k !== best);
    const re = (u.re + l.re) / 2;
    const im = (u.im - l.im) / 2;
    out.push({ re, im }, { re, im: -im });
  }
  for (const l of lower) out.push({ re: l.re, im: 0 }); // unmatched leftovers
  return out;
}

function sortRoots(z) {
  return z.sort((a, b) => a.re - b.re || b.im - a.im);
}

/** Largest real part among the roots (-Infinity when there are none). */
export const maxRealPart = (z) => z.reduce((m, r) => Math.max(m, r.re), -Infinity);
