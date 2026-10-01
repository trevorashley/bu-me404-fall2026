// Minimal complex arithmetic on plain {re, im} objects.

export const C = (re, im = 0) => ({ re, im });
export const add = (a, b) => C(a.re + b.re, a.im + b.im);
export const sub = (a, b) => C(a.re - b.re, a.im - b.im);
export const mul = (a, b) => C(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
export const scale = (a, k) => C(a.re * k, a.im * k);
export const abs = (a) => Math.hypot(a.re, a.im);
export const arg = (a) => Math.atan2(a.im, a.re);
export const conj = (a) => C(a.re, -a.im);

export function div(a, b) {
  const d = b.re * b.re + b.im * b.im;
  return C((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
}

export function exp(a) {
  const m = Math.exp(a.re);
  return C(m * Math.cos(a.im), m * Math.sin(a.im));
}
