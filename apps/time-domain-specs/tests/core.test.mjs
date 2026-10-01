// Numerical core checked against values stated in the L3 notes
// (book/src/content/book-notes/time-domain-specs_*.md).
// Run from the repository root:  node --test apps/time-domain-specs/tests/

import test from "node:test";
import assert from "node:assert/strict";
import { simulate, pairFromZetaWn, modes, finalValue, dominant, factorFlags } from "../static/js/lti.js";
import { analyze, secondOrderEstimates, zetaFromMp, firstOrderExact } from "../static/js/metrics.js";

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ""} got ${a}, expected ${b} ± ${tol}`);

const pair = (zeta, wn, extra = {}) => ({ poles: pairFromZetaWn(zeta, wn), zeros: [], gain: null, ...extra });
const withZero = (alpha, zeta = 0.5, wn = 1) => ({ ...pair(zeta, wn), zeros: [{ re: -alpha * zeta * wn, im: 0 }] });
const withPole = (alpha, zeta = 0.5, wn = 1) => ({
  ...pair(zeta, wn),
  poles: [...pairFromZetaWn(zeta, wn), { re: -alpha * zeta * wn, im: 0 }],
});

test("normalised rise time of the standard pair (§2.2)", () => {
  for (const [zeta, want] of [[0.1, 1.10], [0.5, 1.64], [0.7, 2.13], [1.0, 3.36]]) {
    const { metrics } = analyze(pair(zeta, 1));
    close(metrics.rise, want, 0.006, `ζ=${zeta}`);
  }
});

test("overshoot of the standard pair matches Eq. 3.72 (§2.3)", () => {
  for (const [zeta, want] of [[0.3, 0.3723], [0.5, 0.163], [0.7, 0.046]]) {
    const { metrics } = analyze(pair(zeta, 2.5));
    close(metrics.Mp, want, 0.0006, `ζ=${zeta}`);
    close(metrics.Mp, secondOrderEstimates(zeta, 2.5).Mp, 1e-6, `formula ζ=${zeta}`);
    close(metrics.tp, secondOrderEstimates(zeta, 2.5).tp, 1e-4, `t_p ζ=${zeta}`);
  }
});

test("settling time at ζ=0.7, ωn=4 and the envelope bound (§2.4)", () => {
  const { metrics } = analyze(pair(0.7, 4));
  close(metrics.ts, 1.644, 0.001);
  const est = secondOrderEstimates(0.7, 4);
  close(est.ts, 1.643, 0.001);
  close(est.tsEnvelope, 1.765, 0.001);
});

test("critically damped settling time ωn·t_s ≈ 6.64 (§2.4)", () => {
  const { metrics } = analyze(pair(1, 1));
  close(metrics.ts, 6.64, 0.005);
});

test("first-order exact results (§2.5)", () => {
  const sigma = 3;
  const { metrics } = analyze({ poles: [{ re: -sigma, im: 0 }], zeros: [], gain: null });
  const ex = firstOrderExact(sigma);
  close(metrics.rise, ex.rise, 1e-5);
  close(metrics.ts, ex.ts, 1e-5);
  assert.equal(metrics.Mp, 0);
});

test("Example 3.27: boundary pair fails rise time; exact ζ bound", () => {
  const { metrics } = analyze(pair(0.7, 3));
  close(metrics.rise, 0.709, 0.001);
  close(zetaFromMp(0.1), 0.591155, 1e-6);
});

test("LHP zero overshoot family, ζ=0.5 (§5)", () => {
  for (const [alpha, want] of [[4, 0.191], [2, 0.298], [1, 0.699], [0.5, 1.71]]) {
    const { metrics } = analyze(withZero(alpha));
    close(metrics.Mp, want, want * 0.005 + 0.0006, `α=${alpha}`);
  }
  close(analyze(withZero(-2)).metrics.Mp, 0.209, 0.0006, "α=-2");
});

test("RHP zero undershoot minima (§7)", () => {
  for (const [alpha, want] of [[-1, -0.752], [-2, -0.280], [-4, -0.091]]) {
    const { metrics } = analyze(withZero(alpha));
    close(metrics.undershoot, want, 0.001, `α=${alpha}`);
  }
});

test("derivative decomposition y = y0 + ẏ0/(ασ) (§6)", () => {
  const zeta = 0.5, wn = 2, alpha = 1.5, sigma = zeta * wn, T = 10, N = 3000;
  const y = simulate(withZero(alpha, zeta, wn), { input: "step", T, N }).y;
  const y0 = simulate(pair(zeta, wn), { input: "step", T, N }).y;
  const h0 = simulate(pair(zeta, wn), { input: "impulse", T, N }).y;
  let err = 0;
  for (let k = 0; k < N; k++) err = Math.max(err, Math.abs(y[k] - (y0[k] + h0[k] / (alpha * sigma))));
  assert.ok(err < 1e-9, `max error ${err}`);
});

test("extra-pole rise times, ζ=0.5 (§9)", () => {
  for (const [alpha, want] of [[4, 1.87], [2, 2.29], [1, 3.46], [0.5, 8.49]]) {
    const { metrics } = analyze(withPole(alpha));
    close(metrics.rise, want, 0.006, `α=${alpha}`);
  }
});

test("Example 3.28: overshoot and modal coefficients", () => {
  for (const [z, want] of [[1, 1.08], [2, 0.25], [3, 0.037], [4, 0], [5, 0], [6, 0]]) {
    const sys = { poles: [{ re: -4, im: 0 }, { re: -6, im: 0 }], zeros: [{ re: -z, im: 0 }], gain: 24 / z };
    const { metrics } = analyze(sys);
    close(metrics.Mp, want, 0.0015, `z=${z}`);
    const m = modes(sys);
    close(m.c0, 1, 1e-12);
    close(m.modes[0].coef.re, 12 / z - 3, 1e-12, `C4 z=${z}`);
    close(m.modes[1].coef.re, 2 - 12 / z, 1e-12, `C6 z=${z}`);
  }
});

test("Eqs. 3.78–3.79 residues by cover-up", () => {
  const m1 = modes({ poles: [{ re: -1, im: 0 }, { re: -2, im: 0 }], zeros: [], gain: 2 }, "impulse");
  close(m1.modes[0].coef.re, 2, 1e-12);
  close(m1.modes[1].coef.re, -2, 1e-12);
  const m2 = modes({ poles: [{ re: -1, im: 0 }, { re: -2, im: 0 }], zeros: [{ re: -1.1, im: 0 }], gain: null }, "impulse");
  close(m2.modes[0].coef.re, 2 / 11, 1e-12);
  close(m2.modes[1].coef.re, 18 / 11, 1e-12);
});

test("Example 3.30: Boeing 747 altitude after a negative unit elevator impulse", () => {
  const sys = { poles: [{ re: 0, im: 0 }, { re: -2, im: 3 }], zeros: [{ re: 6, im: 0 }], gain: 30 };
  const opts = { input: "impulse", amp: -1 };
  close(finalValue(sys, "impulse", -1), 180 / 13, 1e-12);
  const { metrics } = analyze(sys, opts);
  close(metrics.undershoot * metrics.yf, -1.68, 0.01, "minimum");
  close(metrics.rise, 0.43, 0.006, "t_r");
  close(metrics.Mp, 0.138, 0.0015, "M_p");
  close(metrics.ts, 2.54, 0.006, "t_s");
  assert.equal(finalValue(sys, "step", 1), null, "a step drives the integrator forever");
});

test("dominant pole and factor-of-four flags", () => {
  const sys = withPole(3, 0.5, 2);
  const d = dominant(sys);
  close(d.zeta, 0.5, 1e-12);
  close(d.wn, 2, 1e-12);
  const flags = factorFlags(sys);
  assert.equal(flags.length, 1);
  close(flags[0].ratio, 3, 1e-12);
  assert.ok(flags[0].near);
});

test("repeated poles are flagged, and ζ=1 still simulates exactly", () => {
  const sys = pair(1, 2);
  assert.ok(modes(sys).repeated);
  const { t, y } = simulate(sys, { input: "step", T: 5, N: 501 });
  let err = 0;
  for (let k = 0; k < t.length; k++) err = Math.max(err, Math.abs(y[k] - (1 - (1 + 2 * t[k]) * Math.exp(-2 * t[k]))));
  assert.ok(err < 1e-12, `max error ${err}`);
});

test("dragging one of two real poles past the other keeps moving the same pole", async () => {
  const { dragPair } = await import("../static/js/ui.js");
  let st = { zeta: 1, wn: 1.5 };
  for (const re of [-1.6, -2, -2.5, -3]) st = dragPair(st, "p0", re, 0);
  // poles at −3 and −1.5
  close(st.wn, Math.sqrt(4.5), 1e-9);
  close(st.zeta, 4.5 / (2 * Math.sqrt(4.5)), 1e-9);
});
