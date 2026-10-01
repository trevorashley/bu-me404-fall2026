// Tab 2 — specifications become a region of the s-plane (FPE §3.4, Example 3.27).
// Formula checks (ωn, ζ, σ bounds) are shown separately from checks on the
// measured response, so a pair can pass one and fail the other.

import { Plot, fmtNum, cssVar } from "../plot.js";
import { SPlane } from "../splane.js";
import { pairFromZetaWn } from "../lti.js";
import { analyze, zetaFromMp, BAND_CONST } from "../metrics.js";
import { el, $, slider, specLayers, fitView, displayT, pct, secs, badge, dragPair, pairRoots } from "../ui.js";

const DEFAULT = { tr: 0.6, Mp: 0.1, ts: 3, eps: 0.01, zeta: 0.7, wn: 3.0 };

const PRESETS = [
  { label: "Ex. 3.27: boundary pair (ζ=0.7, ωn=3)", state: { ...DEFAULT }, note: "Meets every formula bound, yet the actual rise time is 0.709 s > 0.6 s: 1.8/ωn is a fit, and ωn·t_r = 2.13 at ζ = 0.7." },
  { label: "Corner of the region (ζ=0.591, ωn=3)", state: { ...DEFAULT, zeta: 0.5912, wn: 3 }, note: "Exactly on both the ζ and ωn boundaries. Overshoot is exactly 10% here because the ζ bound is exact for the standard pair." },
  { label: "Comfortable design (ζ=0.7, ωn=4)", state: { ...DEFAULT, zeta: 0.7, wn: 4 }, note: "Moving outward from the ωn circle buys margin against the rise-time fit." },
  { label: "Too little damping (ζ=0.45, ωn=4)", state: { ...DEFAULT, zeta: 0.45, wn: 4 }, note: "Outside the ζ wedge: overshoot fails, measured and predicted alike." },
];

export function create(panel, app) {
  let st = { ...DEFAULT };
  let view = null;
  let note = PRESETS[0].note;

  panel.append(el(`<p class="intro">Enter specifications. Inverting the formulas gives <b>ω<sub>n</sub> ≥ 1.8/t<sub>r</sub></b> (outside a circle), <b>ζ ≥ ζ(M<sub>p</sub>)</b> (inside a wedge) and <b>σ ≥ 4.6/t<sub>s</sub></b> (left of a line). Shading marks the <b>allowable</b> region (the book's Fig. 3.26 shades the excluded one). Then check the actual response.</p>`));
  const layout = el(`<div class="layout">
    <div class="col">
      <div class="card"><h2>Specifications</h2>
        <div class="controls">
          <label><span>t<sub>r</sub> ≤</span><input type="number" step="0.05" min="0.01" data-k="tr"> s</label>
          <label><span>M<sub>p</sub> ≤</span><input type="number" step="1" min="0.1" max="99" data-k="Mp"> %</label>
          <label><span>t<sub>s</sub> ≤</span><input type="number" step="0.1" min="0.05" data-k="ts"> s</label>
          <label>band <select data-k="eps"><option value="0.01">1%</option><option value="0.02">2%</option><option value="0.05">5%</option></select></label>
        </div>
        <div class="readout bounds" style="margin-top:.5rem"></div>
      </div>
      <div class="card"><h2>s-plane <button class="tool" data-act="fitS">Fit view</button></h2>
        <div class="canvas-wrap splane-wrap"></div>
        <div class="sliders"></div>
        <div class="btn-row presets" style="margin-top:.5rem"></div>
      </div>
    </div>
    <div class="col">
      <div class="card"><h2>Verdict <span class="badge-row verdict reveal-sensitive"></span></h2>
        <div class="table"></div>
        <p class="hint preset-note reveal-sensitive"></p>
      </div>
      <div class="card"><h2>Step response against the specifications <button class="tool" data-act="fit">Fit axes</button></h2>
        <div class="canvas-wrap plot-wrap"></div>
        <div class="legend"><span><i style="border-color:var(--series-1)"></i>y(t)</span><span><i class="dash" style="border-color:var(--bad)"></i>limits: overshoot ceiling, t<sub>r</sub> (from the 10% crossing), t<sub>s</sub></span></div>
      </div>
    </div>
  </div>`);
  panel.append(layout);

  const bounds = () => {
    const wnMin = 1.8 / st.tr;
    const zMin = zetaFromMp(st.Mp);
    const sMin = (BAND_CONST[st.eps] ?? -Math.log(st.eps)) / st.ts;
    return { wnMin, zMin, sMin };
  };

  const splane = new SPlane($(layout, ".splane-wrap"), {
    onDrag: (id, re, im) => {
      Object.assign(st, dragPair(st, id, re, im, { zetaMax: 2, wnMax: 30 }));
      note = "";
      sync();
      update();
    },
    overlay: (ctx, g) => drawRegion(ctx, g, bounds()),
  });
  const plot = new Plot($(layout, ".plot-wrap"), { xlabel: "t (s)", ylabel: "y(t)" });
  app.registerPlot(plot);

  const sZeta = slider({ name: "ζ", min: 0.05, max: 2, step: 0.001, value: st.zeta, onInput: (v) => { st.zeta = v; note = ""; update(); } });
  const sWn = slider({ name: "ωn", min: 0.3, max: 30, step: 0.01, value: st.wn, log: true, onInput: (v) => { st.wn = v; note = ""; update(); } });
  $(layout, ".sliders").append(sZeta.node, sWn.node);

  const presetRow = $(layout, ".presets");
  for (const p of PRESETS) {
    const b = el(`<button class="tool">${p.label}</button>`);
    b.addEventListener("click", () => { st = { ...p.state }; note = p.note; view = null; sync(); fitS(); update(); });
    presetRow.append(b);
  }

  layout.querySelectorAll("[data-k]").forEach((inp) => {
    inp.addEventListener("change", () => {
      const v = parseFloat(inp.value);
      if (!(v > 0)) { sync(); return; }
      st[inp.dataset.k] = inp.dataset.k === "Mp" ? Math.min(0.99, v / 100) : v;
      view = null;
      note = "";
      fitS();
      update();
    });
  });
  $(layout, '[data-act="fit"]').addEventListener("click", () => { view = null; render(); });
  $(layout, '[data-act="fitS"]').addEventListener("click", () => fitS());

  function fitS() {
    const { wnMin } = bounds();
    const r = Math.max(wnMin * 1.6, st.wn * 1.25);
    splane.setView({ xmin: -r, xmax: r * 0.25, ymax: r * 0.85 });
  }

  function sync() {
    sZeta.set(st.zeta);
    sWn.set(st.wn);
    layout.querySelectorAll("[data-k]").forEach((inp) => {
      const k = inp.dataset.k;
      inp.value = k === "Mp" ? String(+(st.Mp * 100).toFixed(3)) : String(st[k]);
    });
  }

  function update() {
    app.edited();
    render();
  }

  function render() {
    const { wnMin, zMin, sMin } = bounds();
    const poles = pairFromZetaWn(st.zeta, st.wn);
    const sys = { poles, zeros: [], gain: null };
    const res = analyze(sys, { eps: st.eps, minT: st.ts * 1.3 });
    const m = res.metrics;
    const sigma = st.zeta * st.wn;
    const k = BAND_CONST[st.eps] ?? -Math.log(st.eps);

    const bRow = $(layout, ".bounds");
    const redundant = zMin * wnMin >= sMin;
    bRow.innerHTML = `<span>ω<sub>n</sub> ≥ 1.8/t<sub>r</sub> = <b>${fmtNum(wnMin)}</b> rad/s</span><span>ζ ≥ <b>${fmtNum(zMin, 4)}</b> (θ ≥ ${fmtNum((Math.asin(zMin) * 180) / Math.PI)}°)</span><span>σ ≥ ${fmtNum(k, 2)}/t<sub>s</sub> = <b>${fmtNum(sMin)}</b> s⁻¹</span>` +
      (redundant ? `<span class="hint">At the corner σ = ζω<sub>n</sub> ≥ ${fmtNum(zMin * wnMin)} > ${fmtNum(sMin)}: the settling constraint is redundant.</span>` : "");

    splane.setRoots(pairRoots(poles));

    const fChecks = { tr: st.wn >= wnMin - 1e-9, Mp: st.zeta >= zMin - 1e-9, ts: sigma >= sMin - 1e-9 };
    const mChecks = {
      tr: m.rise !== null ? m.rise <= st.tr + 1e-9 : false,
      Mp: m.Mp !== null ? m.Mp <= st.Mp + 1e-9 : false,
      ts: m.ts !== null ? m.ts <= st.ts + 1e-9 : false,
    };
    const all = (c) => c.tr && c.Mp && c.ts;
    $(layout, ".verdict").innerHTML = badge(all(fChecks), "formula region") + badge(all(mChecks), "actual response");
    const row = (name, spec, fTxt, fOk, mTxt, mOk) =>
      `<tr><td>${name}</td><td>${spec}</td><td>${fTxt}</td><td>${badge(fOk, fOk ? "in" : "out")}</td><td class="reveal-sensitive">${mTxt}</td><td class="reveal-sensitive">${badge(mOk, mOk ? "meets" : "fails")}</td></tr>`;
    $(layout, ".table").innerHTML = `<table class="metrics"><thead><tr><th></th><th>Spec</th><th>Formula quantity</th><th>Region</th><th>Measured</th><th>Response</th></tr></thead><tbody>
      ${row("Rise time", `≤ ${secs(st.tr)}`, `ω<sub>n</sub> = ${fmtNum(st.wn)}`, fChecks.tr, secs(m.rise), mChecks.tr)}
      ${row("Overshoot", `≤ ${pct(st.Mp)}`, `ζ = ${fmtNum(st.zeta, 4)}`, fChecks.Mp, pct(m.Mp), mChecks.Mp)}
      ${row(`Settling (${st.eps * 100}%)`, `≤ ${secs(st.ts)}`, `σ = ${fmtNum(sigma)}`, fChecks.ts, secs(m.ts), mChecks.ts)}
    </tbody></table>`;
    let n = note;
    if (!n && all(fChecks) && !all(mChecks)) n = "Inside the formula region but failing a measured specification: the rise-time and settling formulas are approximations, so check the response near the boundary.";
    if (!n && !all(fChecks) && all(mChecks)) n = "Outside the formula region but the response meets the specifications: the formulas are approximate in both directions.";
    $(layout, ".preset-note").innerHTML = n;

    // response with spec limits
    const T = Math.max(displayT(res), st.ts * 1.25);
    if (!view) view = fitView(res.t, [res.y], { T, yf: 1 });
    view.y1 = Math.max(view.y1, 1 + st.Mp + 0.08);
    const layers = [
      ...specLayers(m, { eps: st.eps }),
      { type: "hline", y: 1 + st.Mp, color: "--bad", dash: [6, 4], width: 1.5, label: `M_p limit ${pct(st.Mp)}`, textColor: "--ink-2", keep: true },
      { type: "vline", x: st.ts, color: "--bad", dash: [6, 4], width: 1.5, label: `t_s limit ${fmtNum(st.ts)} s`, textColor: "--ink-2", keep: true },
    ];
    if (m.t10 !== null) layers.push({ type: "segment", x0: m.t10, y0: 0.9, x1: m.t10 + st.tr, y1: 0.9, color: "--bad", dash: [6, 4], width: 1.5, arrows: true, label: `t_r limit ${fmtNum(st.tr)} s`, textColor: "--ink-2" });
    layers.push({ type: "line", x: res.t, y: res.y, color: "--series-1", width: 2.25, label: "y" });
    plot.set(layers, view);
  }

  sync();
  fitS();
  render();

  return {
    debug: { splane, plot },
    activate() { render(); },
    redraw() { splane.render(); render(); },
    getState() { return st; },
    setState(s) { st = { ...DEFAULT, ...s }; note = ""; view = null; sync(); fitS(); render(); },
  };
}

// Shade { |s| ≥ ωn_min } ∩ { ζ ≥ ζ_min } ∩ { Re s ≤ −σ_min } and draw its edges.
function drawRegion(ctx, g, { wnMin, zMin, sMin }) {
  const { toPx, w, h, ox, oy, k, s } = g;
  const th = Math.asin(Math.min(1, zMin));
  const L = (w + h) * 4 / k; // far away, in s units
  const dx = -Math.sin(th), dy = Math.cos(th);
  ctx.save();
  // wedge about the negative real axis
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  const [ax, ay] = toPx(dx * L, dy * L);
  const [bx, by] = toPx(dx * L, -dy * L);
  ctx.lineTo(ax, ay);
  ctx.lineTo(Math.min(ax, 0) - w, ay);
  ctx.lineTo(Math.min(bx, 0) - w, by);
  ctx.lineTo(bx, by);
  ctx.closePath();
  ctx.clip();
  // left of −σ_min
  const [lx] = toPx(-sMin, 0);
  ctx.beginPath();
  ctx.rect(-10, -10, lx + 10, h + 20);
  ctx.clip();
  // outside the ωn circle (even-odd)
  ctx.beginPath();
  ctx.rect(-10, -10, w + 20, h + 20);
  ctx.moveTo(ox + wnMin * k, oy);
  ctx.arc(ox, oy, wnMin * k, 0, 2 * Math.PI);
  ctx.fillStyle = cssVar("--region");
  ctx.fill("evenodd");
  ctx.restore();

  // edges
  ctx.save();
  ctx.strokeStyle = cssVar("--region-edge");
  ctx.lineWidth = 1.75 * s;
  ctx.setLineDash([6 * s, 4 * s]);
  ctx.beginPath();
  ctx.arc(ox, oy, wnMin * k, Math.PI / 2, (3 * Math.PI) / 2);
  ctx.moveTo(ox, oy); ctx.lineTo(ax, ay);
  ctx.moveTo(ox, oy); ctx.lineTo(bx, by);
  ctx.moveTo(lx, 0); ctx.lineTo(lx, h);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = cssVar("--ink-2");
  ctx.font = `${11.5 * s}px system-ui, sans-serif`;
  ctx.textAlign = "right";
  ctx.textBaseline = "bottom";
  ctx.fillText(`ωn = ${fmtNum(wnMin)}`, ox - wnMin * k * 0.72 - 4, oy - wnMin * k * 0.7 - 4);
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  ctx.fillText(`σ = ${fmtNum(sMin)}`, lx + 4, h * 0.3);
  const t = Math.min(oy / Math.max(dy, 1e-6), ox / Math.max(-dx, 1e-6)) * 0.62;
  ctx.textAlign = "right";
  ctx.fillText(`ζ = ${fmtNum(zMin, 3)}`, ox + dx * t - 6, oy + dy * t + 4);
  ctx.restore();
}
