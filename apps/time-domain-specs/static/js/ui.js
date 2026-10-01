// Shared UI helpers: DOM construction, sliders, response annotations, tables.

import { fmtNum } from "./plot.js";

export function el(html) {
  const t = document.createElement("template");
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}

export const $ = (root, sel) => root.querySelector(sel);

// Range slider with a numeric readout. Optional log scale for positive ranges.
export function slider({ name, min, max, step = 0.01, value, log = false, digits = 3, onInput }) {
  const node = el(`<label class="slider"><span class="name">${name}</span><input type="range"><output></output></label>`);
  const input = node.querySelector("input");
  const out = node.querySelector("output");
  const toPos = (v) => (log ? Math.log(v / min) / Math.log(max / min) : (v - min) / (max - min));
  const fromPos = (p) => (log ? min * (max / min) ** p : min + p * (max - min));
  input.min = 0;
  input.max = 1000;
  input.step = 1;
  let current = value;
  const quant = (v) => (step ? Math.round(v / step) * step : v);
  const show = () => { out.textContent = fmtNum(current, digits); };
  const api = {
    node,
    get value() { return current; },
    set(v) {
      current = v;
      input.value = Math.round(Math.max(0, Math.min(1, toPos(v))) * 1000);
      show();
    },
  };
  input.addEventListener("input", () => {
    current = quant(fromPos(input.value / 1000));
    show();
    onInput?.(current);
  });
  api.set(value);
  return api;
}

export function pct(v, digits = 3) {
  return v === null || v === undefined ? "—" : `${fmtNum(v * 100, digits)}%`;
}

export function secs(v, digits = 3) {
  return v === null || v === undefined ? "—" : `${fmtNum(v, digits)} s`;
}

// Annotation layers for a measured response. k scales time (ωn for normalised axes).
export function specLayers(m, { k = 1, eps = 0.01, showBand = true, color = "--ink-2" } = {}) {
  const L = [];
  if (m.yf === null || m.reason) return L;
  const yf = m.yf;
  if (showBand) L.push({ type: "hband", y0: yf * (1 - eps), y1: yf * (1 + eps), fill: "--band", keep: true });
  L.push({ type: "hline", y: yf, color: "--axis", width: 1, keep: true });
  if (m.t10 !== null && m.t90 !== null) {
    const y0 = 0.1 * yf, y1 = 0.9 * yf;
    L.push({ type: "segment", x0: m.t10 * k, y0: 0, x1: m.t10 * k, y1: y0, color, dash: [2, 3], width: 1 });
    L.push({ type: "segment", x0: m.t90 * k, y0: 0, x1: m.t90 * k, y1: y1, color, dash: [2, 3], width: 1 });
    L.push({ type: "marker", x: m.t10 * k, y: y0, shape: "dot", color, size: 3.5 });
    L.push({ type: "marker", x: m.t90 * k, y: y1, shape: "dot", color, size: 3.5 });
    L.push({ type: "segment", x0: m.t10 * k, y0: 0.03 * yf, x1: m.t90 * k, y1: 0.03 * yf, color, arrows: true, width: 1.2,
      label: `t_r = ${fmtNum(m.rise)} s` });
  }
  if (m.tp !== null) {
    L.push({ type: "segment", x0: m.tp * k, y0: yf, x1: m.tp * k, y1: m.peak, color, arrows: true, width: 1.2 });
    L.push({ type: "marker", x: m.tp * k, y: m.peak, shape: "diamond", color: "--series-1", size: 6,
      label: `M_p = ${pct(m.Mp)} at t_p = ${fmtNum(m.tp)} s`, labelDir: "ne" });
  }
  if (m.undershoot !== null) {
    L.push({ type: "marker", x: m.tMin * k, y: m.undershoot * yf, shape: "diamond", color: "--series-1", size: 6,
      label: `undershoot ${pct(m.undershoot)}`, labelDir: "se" });
  }
  if (m.ts !== null && m.ts > 0) {
    L.push({ type: "vline", x: m.ts * k, color, dash: [5, 4], width: 1.2, label: `t_s = ${fmtNum(m.ts)} s (${eps * 100}%)` });
  }
  return L;
}

// Axis limits that show a response and its annotations.
export function fitView(t, ys, { k = 1, T = null, yf = 1 } = {}) {
  let lo = 0, hi = Math.max(yf ?? 0, 0);
  for (const y of ys) for (let i = 0; i < y.length; i++) { if (y[i] < lo) lo = y[i]; if (y[i] > hi) hi = y[i]; }
  const span = hi - lo || 1;
  return { x0: 0, x1: (T ?? t[t.length - 1]) * k, y0: lo - 0.08 * span, y1: hi + 0.12 * span };
}

// Display window: long enough to show settling, not the whole analysis horizon.
export function displayT(res) {
  const m = res.metrics;
  if (!m || m.reason || !m.settled) return res.T;
  const cands = [m.ts * 1.35, (m.tp ?? 0) * 3, (m.t90 ?? 0) * 3];
  return Math.min(res.T, Math.max(...cands, res.T * 0.05));
}

export function badge(state, text) {
  const cls = state === true ? "pass" : state === false ? "fail" : "na";
  const icon = state === true ? "✓" : state === false ? "✗" : "–";
  return `<span class="badge ${cls}">${icon} ${text}</span>`;
}

export function toast(msg) {
  let t = document.querySelector(".toast");
  if (!t) { t = el(`<div class="toast"></div>`); document.body.append(t); }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove("show"), 1600);
}

// Interpret a drag of a second-order pair (roots from pairFromZetaWn) as new
// (ζ, ωn). id "p0" is the complex pole or the first real pole, "p1" the second.
export function dragPair({ zeta, wn }, id, re, im, { zetaMin = 0.02, zetaMax = 3, wnMin = 0.05, wnMax = 50 } = {}) {
  let z = zeta, w = wn;
  if (im > 0) {
    const r = Math.hypot(re, im);
    w = r;
    z = re < 0 ? -re / r : zetaMin;
  } else if (zeta < 1) {
    // a complex pair dragged onto the axis: critical damping at that radius
    w = Math.abs(re);
    z = 1;
  } else {
    // two real poles: move the one nearest the pointer, keep the other
    // (ids swap when the poles cross, so they cannot identify the dragged pole)
    const d = wn * Math.sqrt(zeta * zeta - 1);
    const p = [-zeta * wn + d, -zeta * wn - d];
    const i = Math.abs(p[1] - re) < Math.abs(p[0] - re) ? 1 : 0;
    p[i] = Math.min(re, -wnMin);
    w = Math.sqrt(p[0] * p[1]);
    z = -(p[0] + p[1]) / (2 * w);
  }
  z = Math.max(zetaMin, Math.min(zetaMax, z));
  w = Math.max(wnMin, Math.min(wnMax, w));
  return { zeta: z, wn: w };
}

export function pairRoots(poles, extra = {}) {
  return poles.map((p, i) => ({ id: `p${i}`, kind: "pole", ...p, ...extra }));
}
