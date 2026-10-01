// Real polynomials, coefficients highest power first (MATLAB / NumPy convention).

import { C, mul, sub, add } from "./complex.js";

// Monic polynomial with the given complex roots; imaginary parts of the
// coefficients cancel for conjugate-symmetric root sets and are dropped.
export function fromRoots(roots) {
  let p = [C(1)];
  for (const r of roots) {
    const q = new Array(p.length + 1).fill(null).map(() => C(0));
    for (let i = 0; i < p.length; i++) {
      q[i] = add(q[i], p[i]);
      q[i + 1] = sub(q[i + 1], mul(p[i], r));
    }
    p = q;
  }
  return p.map((c) => c.re);
}

export function polyval(p, x) {
  let y = 0;
  for (const c of p) y = y * x + c;
  return y;
}

export function polyvalC(p, s) {
  let y = C(0);
  for (const c of p) y = add(mul(y, s), C(c));
  return y;
}

// Human-readable polynomial in s, e.g. "s² + 2s + 13".
export function polyString(p, digits = 3) {
  const sup = ["", "", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"];
  const n = p.length - 1;
  const fmt = (x) => {
    const r = Number(x.toPrecision(digits));
    return String(r);
  };
  let out = "";
  p.forEach((c, i) => {
    const k = n - i;
    if (Math.abs(c) < 1e-12 && n > 0) return;
    const neg = c < 0;
    const m = Math.abs(c);
    const coef = k > 0 && Math.abs(m - 1) < 1e-12 ? "" : fmt(m);
    const term = k === 0 ? fmt(m) : `${coef}s${sup[k] ?? "^" + k}`;
    if (!out) out = (neg ? "−" : "") + term;
    else out += (neg ? " − " : " + ") + term;
  });
  return out || "0";
}
