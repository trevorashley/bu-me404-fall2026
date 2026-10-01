// Tab 3 — a zero or an extra real pole added to the standard pair at s = −ασ
// (FPE Eqs. 3.80–3.82). Shows the derivative decomposition y = y0 + ẏ0/(ασ),
// the RHP-zero undershoot, and how M_p (zero) or t_r (pole) varies with α.

import { Plot, fmtNum, cssVar } from "../plot.js";
import { SPlane } from "../splane.js";
import { pairFromZetaWn, simulate } from "../lti.js";
import { analyze, secondOrderEstimates } from "../metrics.js";
import { el, $, slider, specLayers, fitView, pct, secs, dragPair, pairRoots } from "../ui.js";

const DEFAULT = { mode: "zero", zeta: 0.5, wn: 1, alpha: 2, norm: true, decomp: true, eps: 0.01 };
const ALPHA_MIN = 0.2;

function clampAlpha(a, mode) {
  if (mode === "pole") return Math.max(ALPHA_MIN, Math.min(10, a));
  a = Math.max(-6, Math.min(10, a));
  if (Math.abs(a) < ALPHA_MIN) a = a < 0 ? -ALPHA_MIN : ALPHA_MIN;
  return a;
}

// Sweep over α for a given ζ with ωn = 1 (M_p is independent of ωn; t_r scales as 1/ωn).
const sweepCache = new Map();
function sweep(mode, zeta) {
  const key = `${mode}:${zeta.toFixed(3)}`;
  if (sweepCache.has(key)) return sweepCache.get(key);
  const pair = pairFromZetaWn(zeta, 1);
  const out = { lhp: { a: [], v: [] }, rhp: { a: [], v: [], u: [] } };
  const sigma = zeta;
  const alphas = [];
  for (let a = 0.2; a <= 10.0001; a *= 1.04) alphas.push(a);
  for (const a of alphas) {
    const sys = mode === "zero"
      ? { poles: pair, zeros: [{ re: -a * sigma, im: 0 }], gain: null }
      : { poles: [...pair, { re: -a * sigma, im: 0 }], zeros: [], gain: null };
    const m = analyze(sys).metrics;
    out.lhp.a.push(a);
    out.lhp.v.push(mode === "zero" ? m.Mp * 100 : m.rise);
  }
  if (mode === "zero") {
    for (const a of alphas.filter((x) => x <= 6)) {
      const m = analyze({ poles: pair, zeros: [{ re: a * sigma, im: 0 }], gain: null }).metrics;
      out.rhp.a.unshift(-a);
      out.rhp.v.unshift(m.Mp * 100);
      out.rhp.u.unshift(m.undershoot !== null ? -m.undershoot * 100 : 0);
    }
  }
  const base = analyze({ poles: pair, zeros: [], gain: null }).metrics;
  out.base = mode === "zero" ? base.Mp * 100 : base.rise;
  if (sweepCache.size > 60) sweepCache.clear();
  sweepCache.set(key, out);
  return out;
}

export function create(panel, app) {
  let st = { ...DEFAULT };
  let view = null;

  panel.append(el(`<p class="intro">Add a real <b>zero</b> or an extra real <b>pole</b> at <b>s = −ασ</b>, where σ = ζω<sub>n</sub> is the pair's distance from the imaginary axis (FPE Eqs. 3.80–3.82). Unit DC gain throughout. For a zero, the response splits exactly as <b>y = y<sub>0</sub> + ẏ<sub>0</sub>/(ασ)</b>: the zero-free response plus a scaled copy of its derivative. α &lt; 0 puts the zero in the right half-plane.</p>`));
  const layout = el(`<div class="layout">
    <div class="col">
      <div class="card"><h2>s-plane <span class="btn-row"><span class="seg"><button class="tool" data-mode="zero">Zero</button><button class="tool" data-mode="pole">Extra pole</button></span><button class="tool" data-act="fitS">Fit view</button></span></h2>
        <div class="canvas-wrap splane-wrap"></div>
        <div class="sliders"></div>
        <div class="btn-row quick" style="margin-top:.4rem"></div>
        <div class="readout" style="margin-top:.4rem"></div>
      </div>
      <div class="card"><h2 class="sweep-title"></h2>
        <div class="canvas-wrap inset-wrap sweep reveal-sensitive"></div>
        <p class="hint sweep-hint"></p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h2>Step response <span class="controls">
          <label class="decomp-ctl"><input type="checkbox" data-k="decomp"> decomposition</label>
          <label><input type="checkbox" data-k="norm"><span>normalised time ω<sub>n</sub>t</span></label>
          <button class="tool" data-act="fit">Fit axes</button></span></h2>
        <div class="canvas-wrap plot-wrap"></div>
        <div class="legend"></div>
      </div>
      <div class="card"><h2><span>Effect of the added <span class="what">zero</span></span></h2><div class="table reveal-sensitive"></div><p class="hint tab-note reveal-sensitive"></p></div>
    </div>
  </div>`);
  panel.append(layout);

  const splane = new SPlane($(layout, ".splane-wrap"), {
    onDrag: (id, re, im) => {
      const sigma = st.zeta * st.wn;
      if (id === "extra") st.alpha = clampAlpha(-re / sigma, st.mode);
      else Object.assign(st, dragPair(st, id, re, im, { zetaMax: 0.98, zetaMin: 0.05, wnMax: 20 }));
      sync();
      update();
    },
    overlay: (ctx, g) => {
      const sigma = st.zeta * st.wn;
      const { toPx, h, s } = g;
      const [x4] = toPx(-4 * sigma, 0), [x1] = toPx(-sigma, 0), [xr] = toPx(4 * sigma, 0);
      // |α| < 4 marked as a strip along the real axis
      const oy = toPx(0, 0)[1];
      ctx.fillStyle = cssVar("--region");
      const left = x4, right = st.mode === "zero" ? xr : toPx(0, 0)[0];
      ctx.fillRect(left, oy - 10 * s, right - left, 20 * s);
      ctx.strokeStyle = cssVar("--muted");
      ctx.setLineDash([4 * s, 4 * s]);
      ctx.lineWidth = 1;
      for (const x of st.mode === "zero" ? [x4, x1, xr] : [x4, x1]) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
      ctx.setLineDash([]);
      ctx.fillStyle = cssVar("--ink-2");
      ctx.font = `${11.5 * s}px system-ui, sans-serif`;
      ctx.textBaseline = "bottom";
      ctx.textAlign = "left";
      ctx.fillText("α = 4", x4 + 4, h - 26 * s);
      ctx.fillText("α = 1", x1 + 4, h - 26 * s);
      if (st.mode === "zero") ctx.fillText("α = −4", xr + 4, h - 26 * s);
    },
  });
  const plot = new Plot($(layout, ".plot-wrap"), { xlabel: "ωn·t", ylabel: "y" });
  app.registerPlot(plot);
  const inset = new Plot($(layout, ".sweep"), { xlabel: "α", ylabel: "" });

  const sAlpha = slider({ name: "α", min: -6, max: 10, step: 0.05, value: st.alpha, digits: 3, onInput: (v) => { st.alpha = clampAlpha(v, st.mode); update(); } });
  const sZeta = slider({ name: "ζ", min: 0.05, max: 0.98, step: 0.01, value: st.zeta, onInput: (v) => { st.zeta = v; update(); } });
  const sWn = slider({ name: "ωn", min: 0.2, max: 20, step: 0.01, log: true, value: st.wn, onInput: (v) => { st.wn = v; update(); } });
  $(layout, ".sliders").append(sAlpha.node, sZeta.node, sWn.node);

  const quick = $(layout, ".quick");
  function buildQuick() {
    quick.innerHTML = "";
    const list = st.mode === "zero" ? [10, 4, 2, 1, 0.5, -1, -2, -4] : [10, 4, 2, 1, 0.5];
    quick.append(el(`<span class="hint">α =</span>`));
    for (const a of list) {
      const b = el(`<button class="tool">${a < 0 ? "−" + -a : a}</button>`);
      b.addEventListener("click", () => { st.alpha = a; sync(); update(); });
      quick.append(b);
    }
  }

  layout.querySelectorAll("[data-mode]").forEach((b) =>
    b.addEventListener("click", () => {
      st.mode = b.dataset.mode;
      st.alpha = clampAlpha(st.alpha, st.mode);
      view = null;
      sync();
      update();
    }));
  layout.querySelectorAll("[data-k]").forEach((inp) =>
    inp.addEventListener("change", () => { st[inp.dataset.k] = inp.checked; if (inp.dataset.k === "norm") view = null; update(); }));
  $(layout, '[data-act="fit"]').addEventListener("click", () => { view = null; render(); });
  $(layout, '[data-act="fitS"]').addEventListener("click", () => fitS());

  function roots() {
    const sigma = st.zeta * st.wn;
    return {
      pair: pairFromZetaWn(st.zeta, st.wn),
      extra: { re: -st.alpha * sigma, im: 0 },
    };
  }

  function fitS() {
    const { pair, extra } = roots();
    splane.fit([...pair, extra, { re: -4.5 * st.zeta * st.wn, im: 0 }, ...(st.mode === "zero" ? [{ re: 4.5 * st.zeta * st.wn, im: 0 }] : [])], { margin: 0.12, includeRhp: 0.1 });
  }

  function sync() {
    sAlpha.set(st.alpha);
    sZeta.set(st.zeta);
    sWn.set(st.wn);
    layout.querySelectorAll("[data-mode]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mode === st.mode)));
    layout.querySelectorAll("[data-k]").forEach((inp) => (inp.checked = st[inp.dataset.k]));
    $(layout, ".decomp-ctl").hidden = st.mode !== "zero";
    $(layout, ".what").textContent = st.mode === "zero" ? (st.alpha < 0 ? "RHP zero" : "zero") : "pole";
    buildQuick();
  }

  function update() {
    app.edited();
    render();
  }

  function render() {
    const { pair, extra } = roots();
    const sigma = st.zeta * st.wn;
    const zero = st.mode === "zero";
    const sys = zero ? { poles: pair, zeros: [extra], gain: null } : { poles: [...pair, extra], zeros: [], gain: null };
    const sys0 = { poles: pair, zeros: [], gain: null };

    splane.setRoots([
      ...pairRoots(pair),
      { id: "extra", kind: zero ? "zero" : "pole", ...extra, color: "--series-1", label: `α = ${fmtNum(st.alpha)}` },
    ]);

    const res = analyze(sys, { eps: st.eps });
    const res0 = analyze(sys0, { eps: st.eps });
    const T = Math.max(res.metrics.ts ?? res.T, res0.metrics.ts ?? res0.T) * 1.3;
    const N = 2400;
    const y = simulate(sys, { input: "step", T, N }).y;
    const y0 = simulate(sys0, { input: "step", T, N }).y;
    const k = st.norm ? st.wn : 1;
    const t = Array.from({ length: N }, (_, i) => (i * T) / (N - 1));
    const tk = t.map((v) => v * k);

    const layers = [...specLayers(res.metrics, { k, eps: st.eps })];
    const legend = [`<span><i style="border-color:var(--series-1)"></i>y (with ${zero ? "zero" : "extra pole"})</span>`, `<span><i class="dash" style="border-color:var(--series-2)"></i>y<sub>0</sub> (zero-free pair)</span>`];
    layers.push({ type: "line", x: tk, y: Array.from(y0), color: "--series-2", dash: [6, 4], width: 1.75, label: "y0" });
    let term = null;
    if (zero && st.decomp) {
      const h0 = simulate(sys0, { input: "impulse", T, N }).y;
      term = Array.from(h0, (v) => v / (st.alpha * sigma));
      layers.push({ type: "line", x: tk, y: term, color: "--series-3", dash: [2, 3], width: 2, label: "ẏ0/(ασ)" });
      legend.push(`<span><i class="dot" style="border-color:var(--series-3)"></i>ẏ<sub>0</sub>/(ασ) — the derivative term</span>`);
    }
    layers.push({ type: "line", x: tk, y: Array.from(y), color: "--series-1", width: 2.5, label: "y" });
    if (!view) {
      view = fitView(t, term ? [y, y0, term] : [y, y0], { k, T, yf: 1 });
    }
    plot.xlabel = st.norm ? "ωn·t (rad)" : "t (s)";
    plot.set(layers, view);
    $(layout, ".legend").innerHTML = legend.join("");

    // readout
    const coef = 1 / (st.alpha * sigma);
    $(layout, ".readout").innerHTML = `<span>${zero ? "zero" : "pole"} at <b>s = ${fmtNum(extra.re)}</b></span><span>σ = <b>${fmtNum(sigma)}</b></span>` +
      (zero ? `<span>1/(ασ) = <b>${fmtNum(coef)}</b></span>` : "") +
      `<span class="${Math.abs(st.alpha) < 4 ? "warn-text" : ""}">|α| ${Math.abs(st.alpha) < 4 ? "< 4: check explicitly" : "≥ 4: candidate for neglect"}</span>`;

    // comparison table
    const m = res.metrics, m0 = res0.metrics;
    const ch = (a, b) => (a === null || b === null || b === 0 ? "" : `${a >= b ? "+" : ""}${fmtNum(((a - b) / b) * 100, 2)}%`);
    const rows = [
      ["Rise time t<sub>r</sub>", secs(m0.rise), secs(m.rise), ch(m.rise, m0.rise)],
      ["Overshoot M<sub>p</sub>", pct(m0.Mp), pct(m.Mp), m0.Mp > 0 && m.Mp !== null ? `${m.Mp >= m0.Mp ? "+" : ""}${fmtNum((m.Mp - m0.Mp) * 100, 3)} pts` : ""],
      ["Peak time t<sub>p</sub>", secs(m0.tp), secs(m.tp), ch(m.tp, m0.tp)],
      [`Settling t<sub>s</sub> (${st.eps * 100}%)`, secs(m0.ts), secs(m.ts), ch(m.ts, m0.ts)],
      ["Undershoot", "none", m.undershoot !== null ? pct(m.undershoot) : "none", ""],
    ];
    $(layout, ".table").innerHTML = `<table class="metrics"><thead><tr><th></th><th>Zero-free pair</th><th>With ${zero ? "zero" : "pole"}</th><th>Change</th></tr></thead><tbody>${rows
      .map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join("")}</tbody></table>`;
    const est = secondOrderEstimates(st.zeta, st.wn, st.eps);
    let note;
    if (zero && st.alpha < 0) note = `RHP zero: y = y<sub>0</sub> − ẏ<sub>0</sub>/(|α|σ). Early on ẏ<sub>0</sub> is largest, so the response starts the wrong way (initial slope ω<sub>n</sub>²/(ασ) &lt; 0). Compare overshoot with care: against the same-distance LHP zero it is lower; against no zero it can be higher.`;
    else if (zero) note = `LHP zero: adding the positive hump ẏ<sub>0</sub>/(ασ) speeds the rise and raises the peak. The formulas for the pair alone predict t<sub>r</sub> ≈ ${secs(est.rise)} and M<sub>p</sub> = ${pct(est.Mp)}.`;
    else note = `Extra pole: the response is filtered by a first-order lag, so the rise slows and the overshoot is usually reduced. Factor of four is a heuristic: even α = 4 changes t<sub>r</sub> by roughly 14% at ζ = 0.5.`;
    $(layout, ".tab-note").innerHTML = note;

    // sweep inset
    const sw = sweep(st.mode, Math.round(st.zeta * 200) / 200);
    if (zero) {
      $(layout, ".sweep-title").textContent = "Overshoot versus zero location";
      $(layout, ".sweep-hint").innerHTML = `M<sub>p</sub> (blue) against α, with the zero-free value dashed. For α &lt; 0 the aqua curve is the initial undershoot. Shaded: |α| &lt; 4 (also marked along the real axis of the s-plane).`;
      const cur = m.Mp * 100;
      inset.set([
        { type: "vspan", x0: -4, x1: 4, fill: "--shade" },
        { type: "hline", y: sw.base, color: "--series-2", dash: [6, 4], width: 1.5, label: `no zero: ${fmtNum(sw.base)}%`, textColor: "--ink-2" },
        { type: "line", x: sw.lhp.a, y: sw.lhp.v, color: "--series-1", width: 2, label: "M_p %" },
        { type: "line", x: sw.rhp.a, y: sw.rhp.v, color: "--series-1", width: 2, label: "M_p %" },
        { type: "line", x: sw.rhp.a, y: sw.rhp.u, color: "--series-3", width: 2, dash: [2, 3], label: "undershoot %" },
        { type: "marker", x: st.alpha, y: Math.min(cur, 199), shape: "diamond", color: "--series-1", size: 6, label: `${fmtNum(cur)}%`, labelDir: st.alpha > 6 ? "nw" : "ne" },
      ], { x0: -6, x1: 10, y0: -5, y1: Math.min(200, Math.max(60, cur * 1.2)) });
    } else {
      $(layout, ".sweep-title").textContent = "Rise time versus extra-pole location";
      $(layout, ".sweep-hint").innerHTML = `Normalised rise time ω<sub>n</sub>t<sub>r</sub> against α, with the zero-free value dashed. Shaded: α &lt; 4.`;
      const cur = m.rise * st.wn;
      inset.set([
        { type: "vspan", x0: 0, x1: 4, fill: "--shade" },
        { type: "hline", y: sw.base, color: "--series-2", dash: [6, 4], width: 1.5, label: `no extra pole: ${fmtNum(sw.base)}`, textColor: "--ink-2" },
        { type: "line", x: sw.lhp.a, y: sw.lhp.v, color: "--series-1", width: 2, label: "ωn·t_r" },
        { type: "marker", x: st.alpha, y: cur, shape: "diamond", color: "--series-1", size: 6, label: fmtNum(cur), labelDir: "ne" },
      ], { x0: 0, x1: 10, y0: 0, y1: Math.min(Math.max(...sw.lhp.v) * 1.05, sw.base * 5) });
    }
  }

  sync();
  fitS();
  render();

  return {
    debug: { splane, plot },
    activate() { render(); },
    redraw() { splane.render(); render(); },
    getState() { return st; },
    setState(s) { st = { ...DEFAULT, ...s }; st.alpha = clampAlpha(st.alpha, st.mode); view = null; sync(); fitS(); render(); },
  };
}
