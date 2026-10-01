// Tab 4 — Sandbox: place any poles and zeros, compare the full response with
// the dominant-pair formulas, and see how zeros reweight the modes (FPE §3.5).

import { Plot, fmtNum, cssVar, uiScale } from "../plot.js";
import { SPlane } from "../splane.js";
import { tf, order, isPair, dominant, factorFlags, modes, modeCurve, simulate, ORIGIN_TOL } from "../lti.js";
import { analyze, secondOrderEstimates, firstOrderExact } from "../metrics.js";
import { polyString } from "../poly.js";
import { el, $, specLayers, fitView, displayT, pct, secs, toast } from "../ui.js";

const R = (re) => ({ re, im: 0 });
const P2 = (re, im) => ({ re, im, pair: true });

const PRESETS = [
  { id: "pair", label: "Standard pair (ζ = 0.5, ωn = 2)", poles: [P2(-1, Math.sqrt(3))], zeros: [],
    note: "Start here: add a zero or an extra pole and watch the response leave the dominant-pair ghost." },
  { id: "eq378", label: "Eq. 3.78: 2/((s+1)(s+2))", poles: [R(-1), R(-2)], zeros: [],
    note: "Cover-up residues: the impulse coefficients are +2 on e^{−t} and −2 on e^{−2t}. Switch the input to impulse to see them." },
  { id: "eq379", label: "Eq. 3.79: zero at −1.1", poles: [R(-1), R(-2)], zeros: [R(-1.1)],
    note: "The zero at −1.1 nearly cancels the pole at −1: that mode's impulse coefficient drops from 2 to 2/11. Drag the zero onto −1 to remove it." },
  { id: "ex328", label: "Ex. 3.28: zero at −z (drag, snaps to integers)", poles: [R(-4), R(-6)], zeros: [R(-2)], snap: 1,
    note: "Overshoot is 108%, 25%, 3.7% for z = 1, 2, 3, and none for z = 4…6. At z = 4 or 6 a mode is cancelled exactly; at z = 5 both coefficients are negative." },
  { id: "ex329a", label: "Ex. 3.29: zeros −0.1 ± j (exact cancellation)", poles: [R(-1), P2(-0.1, 1)], zeros: [P2(-0.1, 1)],
    note: "The zeros sit exactly on the lightly damped poles, so the oscillatory mode vanishes from this transfer function. Shown as H/H(0)." },
  { id: "ex329b", label: "Ex. 3.29: zeros −0.25 ± j", poles: [R(-1), P2(-0.1, 1)], zeros: [P2(-0.25, 1)],
    note: "Slightly misplaced zeros leave a small, slowly decaying oscillation. The pole locations are never known exactly, so exact cancellation is fragile." },
  { id: "ex329c", label: "Ex. 3.29: zeros −0.5 ± j", poles: [R(-1), P2(-0.1, 1)], zeros: [P2(-0.5, 1)],
    note: "Further from the poles, the zeros barely attenuate the resonance. Shown as H/H(0) so the three cases share a final value." },
  { id: "b747", label: "Ex. 3.30: Boeing 747 altitude (impulse)", poles: [R(0), P2(-2, 3)], zeros: [R(6)], normalize: false, K: 30, input: "impulse", amp: -1,
    note: "Negative unit elevator impulse. The zero at +6 makes the aircraft sink first (to ≈ −1.68) before climbing to 180/13 ≈ 13.85. The integrator turns the impulse into a step-like response." },
  { id: "nmp", label: "(1 − s)/(s + 1)²: stable, non-minimum phase", poles: [P2(-1, 0)], zeros: [R(1)],
    note: "Both poles are stable; the RHP zero alone causes the initial reversal. Nonminimum phase is not instability." },
];

const DEFAULT = { preset: "pair", poles: PRESETS[0].poles, zeros: [], normalize: true, K: 1, input: "step", amp: 1, snap: 0, eps: 0.01, ghost: true, showModes: false };

const MODE_COLORS = ["--series-3", "--series-4", "--series-5", "--series-7"];

const STYLE = `
.tab-panel[data-id="sandbox"] .sb-tools { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.4rem 0; align-items: center; }
.tab-panel[data-id="sandbox"] .sb-flags { margin: 0.4rem 0 0; padding-left: 1.1rem; color: var(--ink-2); font-size: 0.9rem; }
.tab-panel[data-id="sandbox"] .sb-flags li.near { color: var(--ink); }
.tab-panel[data-id="sandbox"] .sb-flags li.near::marker { content: "⚠ "; }
.tab-panel[data-id="sandbox"] select.preset { max-width: 100%; }
.tab-panel[data-id="sandbox"] .sb-sel { color: var(--ink-2); font-size: 0.9rem; font-variant-numeric: tabular-nums; }
`;

let nextId = 1;
const withIds = (list, kind) => list.map((r) => ({ id: `${kind}${nextId++}`, re: r.re, im: r.im ?? 0, pair: Boolean(r.pair || r.im > 0) }));
const strip = (list) => list.map((r) => (r.pair ? { re: r.re, im: r.im, pair: true } : { re: r.re, im: 0 }));

// ---------------------------------------------------------------- formatting

function rootText(r) {
  if (r.pair && r.im > 0) return `${fmtNum(r.re)} ± ${fmtNum(r.im)}j`;
  return `${fmtNum(r.re)}${r.pair ? " (double)" : ""}`;
}

function factorText(r) {
  if (r.pair && r.im > 0) {
    const b = -2 * r.re, c = r.re * r.re + r.im * r.im;
    return `(s² ${b < 0 ? "−" : "+"} ${fmtNum(Math.abs(b))}s + ${fmtNum(c)})`;
  }
  const lin = Math.abs(r.re) < ORIGIN_TOL ? "s" : `(s ${r.re > 0 ? "−" : "+"} ${fmtNum(Math.abs(r.re))})`;
  return r.pair ? `${lin}²` : lin;
}

// Remove pole-zero pairs that cancel exactly (same location and multiplicity),
// so the dominant pole is chosen from the modes that actually appear in H(s).
function cancelled(poles, zeros) {
  const tol = 1e-6 * Math.max(1, ...poles.map((r) => Math.hypot(r.re, r.im)));
  const same = (a, b) => isPair(a) === isPair(b) && Math.abs(a.re - b.re) < tol && Math.abs(a.im - b.im) < tol;
  const left = [...zeros];
  const keep = [], gone = [];
  for (const p of poles) {
    const i = left.findIndex((z) => same(p, z));
    if (i >= 0) { gone.push(p); left.splice(i, 1); } else keep.push(p);
  }
  return { keep, gone, zerosLeft: left };
}

// ---------------------------------------------------------------- bar chart

class Bars {
  constructor(wrap) {
    this.wrap = wrap;
    this.canvas = document.createElement("canvas");
    wrap.append(this.canvas);
    this.items = [];
    this.message = "";
    new ResizeObserver(() => this.render()).observe(wrap);
  }

  set(items, message = "") {
    this.items = items;
    this.message = message;
    this.render();
  }

  render() {
    const dpr = window.devicePixelRatio || 1;
    const { width: w, height: h } = this.wrap.getBoundingClientRect();
    if (!w || !h) return;
    this.canvas.width = Math.round(w * dpr);
    this.canvas.height = Math.round(h * dpr);
    const ctx = this.canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    const s = uiScale();
    ctx.font = `${11.5 * s}px system-ui, -apple-system, "Segoe UI", sans-serif`;
    if (this.message || !this.items.length) {
      ctx.fillStyle = cssVar("--ink-2");
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(this.message || "No modes", w / 2, h / 2, w - 20);
      return;
    }
    // Positive bars above the baseline, negative below; leave room for the value
    // labels under negative bars so they never meet the category labels.
    const top = 20 * s, bottom = h - 36 * s;
    const vpos = Math.max(0, ...this.items.map((it) => it.value));
    const vneg = Math.max(0, ...this.items.map((it) => -it.value));
    const room = vneg > 0 ? 18 * s : 0;
    const scale = (bottom - top - room) / Math.max(1e-12, vpos + vneg);
    const y0 = top + vpos * scale;
    const n = this.items.length;
    const slot = (w - 20) / n;
    const bw = Math.min(46 * s, slot * 0.55);
    ctx.strokeStyle = cssVar("--axis");
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(10, y0);
    ctx.lineTo(w - 10, y0);
    ctx.stroke();
    this.items.forEach((it, i) => {
      const cx = 10 + slot * (i + 0.5);
      const hgt = it.value * scale;
      const yTop = Math.min(y0, y0 - hgt), bh = Math.max(1, Math.abs(hgt));
      ctx.fillStyle = cssVar(it.color);
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(cx - bw / 2, yTop, bw, bh, 3);
      else ctx.rect(cx - bw / 2, yTop, bw, bh);
      ctx.fill();
      ctx.fillStyle = cssVar("--ink");
      ctx.textAlign = "center";
      ctx.textBaseline = it.value >= 0 ? "bottom" : "top";
      ctx.fillText(it.text, cx, it.value >= 0 ? yTop - 3 : yTop + bh + 3, slot - 4);
      ctx.fillStyle = cssVar("--ink-2");
      ctx.textBaseline = "top";
      ctx.fillText(it.label, cx, bottom + 6 * s, slot - 4);
      if (it.sub) ctx.fillText(it.sub, cx, bottom + 20 * s, slot - 4);
    });
  }
}

// ---------------------------------------------------------------- tab

export function create(panel, app) {
  panel.append(el(`<style>${STYLE}</style>`));
  let st = { ...DEFAULT };
  let poles = withIds(st.poles, "p");
  let zeros = withIds(st.zeros, "z");
  let selected = null;
  let view = null;
  let pins = [];
  let last = null; // last computed response, for pinning

  panel.append(el(`<p class="intro">Place any poles (×) and zeros (○). Drag them, add or delete them, or load an example from the notes. The <b>dominant-pair ghost</b> is what the second-order formulas assume; the gap between it and the full response is the effect of the zeros and extra poles.</p>`));
  const layout = el(`<div class="layout">
    <div class="col">
      <div class="card"><h2>Example</h2>
        <select class="preset"></select>
        <p class="hint preset-note" style="margin:.45rem 0 0"></p>
      </div>
      <div class="card"><h2>s-plane <button class="tool" data-act="fitS">Fit view</button></h2>
        <div class="sb-tools">
          <button class="tool" data-add="pole-real">+ real pole</button>
          <button class="tool" data-add="pole-pair">+ complex poles</button>
          <button class="tool" data-add="zero-real">+ real zero</button>
          <button class="tool" data-add="zero-pair">+ complex zeros</button>
          <button class="tool" data-act="delete" disabled>Delete selected</button>
          <label class="hint">snap <select data-k="snap"><option value="0">off</option><option value="0.1">0.1</option><option value="0.5">0.5</option><option value="1">1</option></select></label>
        </div>
        <div class="canvas-wrap splane-wrap"></div>
        <div class="sb-sel hint">Click a root to select it; drag to move. Real roots stay on the real axis; a complex pair dropped on the axis becomes a double root.</div>
      </div>
      <div class="card"><h2>Transfer function</h2>
        <div class="tf tf-fact"></div>
        <div class="tf tf-exp" style="margin-top:.3rem"></div>
        <p class="hint gain-note" style="margin:.3rem 0 0"></p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h2>Response <span class="controls">
          <label>input <select data-k="input"><option value="step">step</option><option value="impulse">impulse</option></select></label>
          <label>amplitude <input type="number" step="1" data-k="amp"></label>
          <label><input type="checkbox" data-k="normalize"> H(0) = 1</label>
          <label class="k-wrap">K <input type="number" step="0.1" data-k="K"></label>
        </span></h2>
        <div class="controls" style="margin-bottom:.4rem">
          <label>band <select data-k="eps"><option value="0.01">1%</option><option value="0.02">2%</option><option value="0.05">5%</option></select></label>
          <label><input type="checkbox" data-k="ghost"> dominant-pair ghost</label>
          <label><input type="checkbox" data-k="showModes"> show modes</label>
          <button class="tool" data-act="pin">Pin (P)</button>
          <button class="tool" data-act="clear">Clear pins</button>
          <button class="tool" data-act="fit">Fit axes</button>
        </div>
        <div class="canvas-wrap plot-wrap"></div>
        <div class="legend"></div>
        <p class="warn-text sim-error" hidden></p>
      </div>
      <div class="card"><h2>Measured versus dominant-pair formulas <span class="sub dom-text"></span></h2>
        <div class="table reveal-sensitive"></div>
        <ul class="sb-flags reveal-sensitive"></ul>
      </div>
      <div class="card"><h2>Modal coefficients <span class="sub modes-sub"></span></h2>
        <div class="canvas-wrap bars-wrap reveal-sensitive"></div>
        <p class="hint">y(t) = ${"c<sub>0</sub>"} + Σ C<sub>i</sub>e<sup>p<sub>i</sub>t</sup> (cover-up residues of Y(s)). A zero near a pole shrinks that pole's bar; exact cancellation removes it. Complex pairs show the amplitude 2|C| and phase.</p>
      </div>
    </div>
  </div>`);
  panel.append(layout);

  // presets
  const presetSel = $(layout, ".preset");
  presetSel.append(el(`<option value="">— custom —</option>`));
  for (const p of PRESETS) presetSel.append(el(`<option value="${p.id}">${p.label}</option>`));
  presetSel.addEventListener("change", () => { if (presetSel.value) loadPreset(presetSel.value); });

  const splane = new SPlane($(layout, ".splane-wrap"), {
    onDrag: (id, re, im) => {
      const r = find(id);
      if (!r) return;
      r.re = Math.max(-1e3, Math.min(1e3, re));
      if (r.pair) r.im = Math.min(1e3, im);
      showSelection();
      update();
    },
    onSelect: (id) => {
      selected = id;
      showSelection();
    },
  });
  const plot = new Plot($(layout, ".plot-wrap"), { xlabel: "t (s)", ylabel: "y(t)" });
  app.registerPlot(plot);
  const bars = new Bars($(layout, ".bars-wrap"));

  function find(id) {
    return poles.find((r) => r.id === id) || zeros.find((r) => r.id === id);
  }

  function sys() {
    return { poles, zeros, gain: st.normalize ? null : st.K };
  }

  function custom() {
    st.preset = "";
    presetSel.value = "";
    $(layout, ".preset-note").textContent = "";
  }

  function showSelection() {
    const r = selected ? find(selected) : null;
    $(layout, '[data-act="delete"]').disabled = !r;
    $(layout, ".sb-sel").textContent = r
      ? `Selected ${poles.includes(r) ? "pole" : "zero"}: s = ${rootText(r)}. Press Delete or the button to remove it.`
      : "Click a root to select it; drag to move. Real roots stay on the real axis; a complex pair dropped on the axis becomes a double root.";
  }

  function loadPreset(id) {
    const p = PRESETS.find((q) => q.id === id);
    if (!p) return;
    st = { ...DEFAULT, preset: id, normalize: p.normalize ?? true, K: p.K ?? 1, input: p.input ?? "step", amp: p.amp ?? 1, snap: p.snap ?? 0,
      eps: st.eps, ghost: st.ghost, showModes: st.showModes };
    poles = withIds(p.poles, "p");
    zeros = withIds(p.zeros, "z");
    selected = null;
    view = null;
    pins = [];
    sync();
    fitS();
    update();
  }

  function fitS() {
    const pts = [...poles, ...zeros];
    splane.fit(pts.length ? pts : [R(-1)], { margin: 0.35, minSpan: 2 });
  }

  function addRoot(kind, type) {
    const list = kind === "pole" ? poles : zeros;
    const k = type === "pair" ? 2 : 1;
    if (kind === "zero" && order(zeros) + k > order(poles)) {
      toast("A proper transfer function needs at least as many poles as zeros");
      return;
    }
    const v = splane.view;
    const span = v.xmax - v.xmin;
    const re = +(v.xmin + span * (kind === "pole" ? 0.3 : 0.4)).toFixed(2);
    const r = type === "pair" ? { re, im: +(v.ymax * 0.45).toFixed(2), pair: true } : { re: kind === "pole" ? re : +(re * 0.6).toFixed(2), im: 0 };
    const [nr] = withIds([r], kind === "pole" ? "p" : "z");
    list.push(nr);
    selected = nr.id;
    splane.selected = nr.id;
    custom();
    showSelection();
    update();
  }

  function deleteSelected() {
    if (!selected) return;
    const r = find(selected);
    if (!r) return;
    if (poles.includes(r)) {
      const k = isPair(r) ? 2 : 1;
      if (poles.length === 1) { toast("Keep at least one pole"); return; }
      if (order(zeros) > order(poles) - k) { toast("Delete a zero first: zeros cannot outnumber poles"); return; }
      poles = poles.filter((q) => q !== r);
    } else zeros = zeros.filter((q) => q !== r);
    selected = null;
    splane.selected = null;
    custom();
    showSelection();
    update();
  }

  layout.querySelectorAll("[data-add]").forEach((b) =>
    b.addEventListener("click", () => {
      const [kind, type] = b.dataset.add.split("-");
      addRoot(kind, type);
    }));
  $(layout, '[data-act="delete"]').addEventListener("click", deleteSelected);
  $(layout, '[data-act="fitS"]').addEventListener("click", fitS);
  $(layout, '[data-act="fit"]').addEventListener("click", () => { view = null; render(); });
  $(layout, '[data-act="pin"]').addEventListener("click", () => pin());
  $(layout, '[data-act="clear"]').addEventListener("click", () => { pins = []; render(); });

  layout.querySelectorAll("[data-k]").forEach((inp) => {
    inp.addEventListener("change", () => {
      const k = inp.dataset.k;
      if (inp.type === "checkbox") st[k] = inp.checked;
      else if (k === "input") st[k] = inp.value;
      else {
        const v = parseFloat(inp.value);
        if (!isFinite(v) || (k === "amp" && v === 0)) { sync(); return; }
        st[k] = v;
      }
      if (k === "snap") splane.snap = st.snap;
      if (["input", "amp", "normalize", "K"].includes(k)) { view = null; custom(); }
      sync();
      update();
    });
  });

  function sync() {
    layout.querySelectorAll("[data-k]").forEach((inp) => {
      const k = inp.dataset.k;
      if (inp.type === "checkbox") inp.checked = Boolean(st[k]);
      else inp.value = String(st[k]);
    });
    $(layout, ".k-wrap").hidden = st.normalize;
    splane.snap = st.snap;
    presetSel.value = st.preset || "";
    const p = PRESETS.find((q) => q.id === st.preset);
    $(layout, ".preset-note").textContent = p ? p.note : "";
  }

  function pin() {
    if (!last) return;
    pins.push({ t: last.t, y: last.y });
    if (pins.length > 3) pins.shift();
    toast(`Pinned (${pins.length}/3)`);
    render();
  }

  function update() {
    app.edited();
    render();
  }

  function render() {
    const S = sys();
    const { num, den, K, normalized } = tf(S);
    const input = st.input, amp = st.amp, eps = st.eps;

    splane.setRoots([
      ...poles.map((r) => ({ ...r, kind: "pole" })),
      ...zeros.map((r) => ({ ...r, kind: "zero" })),
    ]);

    // transfer function text
    const numF = zeros.map(factorText).join("");
    const denF = poles.map(factorText).join("");
    $(layout, ".tf-fact").textContent = `H(s) = ${fmtNum(K, 4)}${numF ? ` · ${numF}` : ""} / ${denF}`;
    $(layout, ".tf-exp").textContent = `H(s) = (${polyString(num, 4)}) / (${polyString(den, 4)})`;
    let gainNote = st.normalize && !normalized ? "A pole or zero at the origin: H(0) cannot be set to 1, so K = 1." : st.normalize ? "K chosen so that H(0) = 1." : "";
    $(layout, ".gain-note").textContent = gainNote;

    // response
    const errEl = $(layout, ".sim-error");
    let res;
    try {
      res = analyze(S, { input, amp, eps, minT: view ? view.x1 : 0 });
      errEl.hidden = true;
    } catch (e) {
      errEl.hidden = false;
      errEl.textContent = `Cannot simulate: ${e.message}.`;
      plot.set([], view ?? { x0: 0, x1: 1, y0: 0, y1: 1 });
      $(layout, ".table").innerHTML = "";
      $(layout, ".sb-flags").innerHTML = "";
      $(layout, ".legend").innerHTML = "";
      $(layout, ".dom-text").textContent = "";
      $(layout, ".modes-sub").textContent = "";
      bars.set([], "—");
      last = null;
      return;
    }
    const m = res.metrics;
    const yf = res.yf;
    const t = res.t, y = res.y;
    last = { t, y };

    const unstable = poles.some((p) => p.re > ORIGIN_TOL || (Math.abs(p.re) <= ORIGIN_TOL && p.im > 0));
    const cx = cancelled(poles, zeros);
    const Sred = { poles: cx.keep, zeros: cx.zerosLeft, gain: S.gain };
    const dom = unstable || !cx.keep.length ? null : dominant(Sred);
    const layers = [];
    const legend = [`<span><i style="border-color:var(--series-1)"></i>y(t)</span>`];

    pins.forEach((p, i) => {
      layers.push({ type: "line", x: p.t, y: p.y, color: "--pin", width: 1.5, dash: [4, 3], label: `Pin ${i + 1}` });
    });
    if (pins.length) legend.push(`<span><i class="dash" style="border-color:var(--pin)"></i>pinned (${pins.length})</span>`);

    // dominant-pair ghost: zero-free, unit-DC-gain dominant pole(s), scaled to the actual final value
    let est = null;
    if (dom) {
      est = dom.complex || isPair(dom.pole) ? secondOrderEstimates(Math.min(dom.zeta, 1), dom.wn, eps) : { ...firstOrderExact(dom.sigma, eps), tsEnvelope: null };
      if (!(dom.complex || isPair(dom.pole))) est.tp = null;
    }
    if (st.ghost && dom && yf !== null && Math.abs(yf) > 1e-12) {
      const g = simulate({ poles: [{ re: dom.pole.re, im: dom.pole.im, pair: isPair(dom.pole) }], zeros: [], gain: null }, { input: "step", T: res.T, N: t.length }).y;
      layers.push({ type: "line", x: t, y: Array.from(g, (v) => v * yf), color: "--series-2", width: 1.75, dash: [7, 4], label: "dominant pair only" });
      legend.push(`<span><i class="dash" style="border-color:var(--series-2)"></i>dominant pair only${input === "impulse" ? " (step shape × final value)" : ""}</span>`);
    }

    // modes
    const md = modes(S, input, amp);
    if (st.showModes && !md.repeated) {
      md.modes.forEach((mo, i) => {
        const c = MODE_COLORS[i] ?? "--muted";
        layers.push({ type: "line", x: t, y: modeCurve(mo, t), color: c, width: 1.25, dash: [2, 3], label: `mode ${rootText(mo.pole)}` });
      });
      legend.push(`<span><i class="dot" style="border-color:var(--series-3)"></i>individual modes${input === "step" ? " (plus c₀)" : ""}</span>`);
    }

    layers.push(...specLayers(m, { eps }));
    layers.push({ type: "line", x: t, y: Array.from(y), color: "--series-1", width: 2.25, label: "y" });
    if (!view) {
      const T = displayT(res);
      view = fitView(t, [y], { T, yf: yf ?? 0 });
      if (!isFinite(view.y0) || !isFinite(view.y1) || view.y1 - view.y0 > 1e8) view = { ...view, y0: -1, y1: 1 };
    }
    plot.set(layers, view);
    if (m.reason) legend.push(`<span class="warn-text">${m.reason === "no final value" ? "No final value: an unstable pole, or an integrator driven by a step. Specifications do not apply." : "Final value is 0: rise, overshoot and settling are not defined."}</span>`);
    $(layout, ".legend").innerHTML = legend.join("");

    // metrics table
    $(layout, ".dom-text").innerHTML = dom
      ? `dominant ${dom.complex ? "pair" : "pole"} ${rootText(dom.pole)}${dom.complex ? ` · ζ ${fmtNum(dom.zeta)} · ω<sub>n</sub> ${fmtNum(dom.wn)}` : ""} · σ ${fmtNum(dom.sigma)}`
      : unstable ? "unstable: the formulas do not apply" : "no stable pole";
    const fmtFinal = yf === null ? "none" : fmtNum(yf, 4);
    const under = m.undershoot !== null ? `${pct(m.undershoot)} (y = ${fmtNum(m.undershoot * yf)})` : m.reason ? "—" : "none";
    if (m.reason) est = null; // no final value, or zero: the specifications are undefined
    const e = est || {};
    const rows = [
      ["Final value", fmtFinal, "", ""],
      ["Rise time t<sub>r</sub>", secs(m.rise), est ? secs(e.rise) : "—", est ? (dom.complex || isPair(dom.pole) ? "1.8/ω<sub>n</sub>" : "ln 9/σ") : ""],
      ["Overshoot M<sub>p</sub>", m.reason ? "—" : pct(m.Mp), est ? pct(e.Mp) : "—", est && dom.complex ? "e<sup>−πζ/√(1−ζ²)</sup>" : ""],
      ["Peak time t<sub>p</sub>", secs(m.tp), est && e.tp ? secs(e.tp) : "—", est && dom.complex ? "π/ω<sub>d</sub>" : ""],
      [`Settling t<sub>s</sub> (${eps * 100}%)`, m.reason ? "—" : m.settled ? secs(m.ts) : `> ${fmtNum(res.T)} s`, est ? secs(e.ts) : "—", est ? `${fmtNum(e.ts * dom.sigma, 2)}/σ` : ""],
      ["Undershoot", under, "", ""],
    ];
    $(layout, ".table").innerHTML = `<table class="metrics"><thead><tr><th></th><th>Measured (full model)</th><th>Dominant-pair formula</th><th style="text-align:left">Formula</th></tr></thead><tbody>${rows
      .map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td class="note">${r[3]}</td></tr>`)
      .join("")}</tbody></table>`;

    // factor-of-four and first-motion flags
    const items = [];
    for (const p of cx.gone)
      items.push(`<li class="near">Pole at ${rootText(p)} is cancelled exactly by a zero: that mode is absent from this transfer function (it may still exist inside the physical system). The formulas use the remaining poles.</li>`);
    for (const f of dom ? factorFlags(Sred) : []) {
      const what = `${f.kind} at ${rootText(f.root)}`;
      if (f.kind === "pole" && Math.abs(f.root.re) <= ORIGIN_TOL && !(f.root.im > 0)) { items.push(`<li>Pole at s = 0: an integrator. It sets the final value of an impulse response; a step drives it without bound.</li>`); continue; }
      if (f.kind === "zero" && f.rhp) items.push(`<li class="near">RHP ${what}: nonminimum phase (ratio ${fmtNum(f.ratio, 2)}).</li>`);
      else if (f.near) items.push(`<li class="near">${what}: |Re| / σ<sub>dom</sub> = ${fmtNum(f.ratio, 2)} &lt; 4. Check its effect; the dominant-pair formulas may be off.</li>`);
      else items.push(`<li>${what}: ratio ${fmtNum(f.ratio, 2)} ≥ 4. A candidate for neglect, but check the response.</li>`);
    }
    // First motion: the first nonzero derivative at 0⁺ has the sign of amp·K (monic factors).
    if (yf !== null && Math.abs(yf) > 1e-12 && Math.sign(amp * K) !== Math.sign(yf))
      items.push(`<li class="near">The response starts in the opposite direction to its final value (initial undershoot).</li>`);
    if (unstable)
      items.push(`<li class="near">A pole on or right of the imaginary axis: the response does not settle.</li>`);
    if (!items.length && dom) items.push(`<li>Only the dominant ${dom.complex ? "pair" : "pole"}: the formulas apply as in the Specifications tab.</li>`);
    $(layout, ".sb-flags").innerHTML = items.join("");

    // modal coefficient bars
    if (md.repeated) {
      bars.set([], md.reason === "origin"
        ? "Pole at s = 0 with a step input: Y(s) has a double pole at 0 (a ramp term), so there are no simple residues"
        : "Repeated poles: coefficients are not defined as simple residues");
      $(layout, ".modes-sub").textContent = "";
    } else {
      const bItems = [];
      if (input === "step" && md.c0 !== null) bItems.push({ label: "c₀ (s = 0)", value: md.c0, color: "--axis", text: fmtNum(md.c0) });
      md.modes.forEach((mo, i) => {
        const c = MODE_COLORS[i] ?? "--muted";
        if (mo.pole.im > 0) {
          const A = 2 * Math.hypot(mo.coef.re, mo.coef.im);
          const ph = (Math.atan2(mo.coef.im, mo.coef.re) * 180) / Math.PI;
          bItems.push({ label: `${rootText(mo.pole)}`, sub: "2|C|", value: A, color: c, text: `${fmtNum(A)} ∠${fmtNum(ph, 3)}°` });
        } else bItems.push({ label: rootText(mo.pole), value: mo.coef.re, color: c, text: fmtNum(mo.coef.re) });
      });
      bars.set(bItems);
      $(layout, ".modes-sub").textContent = `${input === "step" ? "step" : "impulse"} response${amp !== 1 ? `, amplitude ${fmtNum(amp)}` : ""}`;
    }
  }

  sync();
  $(layout, ".preset-note").textContent = PRESETS[0].note;
  fitS();
  render();

  return {
    debug: { splane, plot },
    activate() { render(); },
    redraw() { splane.render(); render(); bars.render(); },
    pin,
    deleteSelected,
    getState() { return { ...st, poles: strip(poles), zeros: strip(zeros) }; },
    setState(s) {
      st = { ...DEFAULT, ...s };
      if (st.preset && !s.poles) {
        loadPreset(st.preset);
        // display options in the link override the preset's defaults
        for (const k of ["input", "amp", "eps", "ghost", "showModes", "snap"]) if (k in s) st[k] = s[k];
        view = null;
        sync();
        render();
        return;
      }
      st.preset = s.preset ?? "";
      poles = withIds(st.poles ?? DEFAULT.poles, "p");
      zeros = withIds(st.zeros ?? [], "z");
      if (!poles.length) poles = withIds(DEFAULT.poles, "p");
      while (order(zeros) > order(poles)) zeros.pop();
      selected = null;
      view = null;
      pins = [];
      sync();
      fitS();
      render();
    },
  };
}
