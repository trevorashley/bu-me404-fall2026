// Tab 1 — the four specifications for a standard second-order pair (FPE §3.4),
// measured from the response and compared with the textbook formulas.

import { Plot, fmtNum } from "../plot.js";
import { SPlane } from "../splane.js";
import { pairFromZetaWn } from "../lti.js";
import { analyze, secondOrderEstimates, firstOrderExact, mpFromZeta } from "../metrics.js";
import { el, $, slider, specLayers, fitView, displayT, pct, secs, dragPair, pairRoots } from "../ui.js";

const DEFAULT = { mode: "second", zeta: 0.5, wn: 2, sigma: 1, eps: 0.01, envelope: true, estimates: true, norm: false };

// ωn·t_r versus ζ for the standard pair, computed once.
let riseCurve = null;
function getRiseCurve() {
  if (riseCurve) return riseCurve;
  const z = [], r = [];
  for (let zeta = 0.05; zeta <= 1.5001; zeta += 0.01) {
    const { metrics } = analyze({ poles: pairFromZetaWn(zeta, 1), zeros: [], gain: null });
    z.push(zeta);
    r.push(metrics.rise);
  }
  return (riseCurve = { z, r });
}

export function create(panel, app) {
  let st = { ...DEFAULT };
  let view = null;

  panel.append(el(`<p class="intro">Drag the pole (or use the sliders). The step response is measured directly — 10–90% rise time, peak, and settling band — and compared with the formulas <b>t<sub>r</sub> ≈ 1.8/ω<sub>n</sub></b>, <b>M<sub>p</sub> = e<sup>−πζ/√(1−ζ²)</sup></b>, <b>t<sub>s</sub> ≈ 4.6/σ</b>. Unit DC gain throughout.</p>`));
  const layout = el(`<div class="layout">
    <div class="col">
      <div class="card"><h2>s-plane <span class="btn-row"><button class="tool" data-act="first">First order</button><button class="tool" data-act="fitS">Fit view</button></span></h2>
        <div class="canvas-wrap splane-wrap"></div>
        <div class="sliders"></div>
        <div class="readout"></div>
      </div>
      <div class="card insets"><h2>Why the formulas work — and where they don't</h2>
        <div class="canvas-wrap inset-wrap rise-inset reveal-sensitive"></div>
        <p class="hint">ω<sub>n</sub>t<sub>r</sub> measured for the standard pair versus ζ. The textbook's 1.8 is a fit that is only met near ζ ≈ 0.58.</p>
        <div class="canvas-wrap inset-wrap mp-inset"></div>
        <p class="hint">M<sub>p</sub> depends on ζ alone: ω<sub>n</sub> only rescales time.</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h2>Step response <span class="controls">
          <label>Band <select data-k="eps"><option value="0.01">1%</option><option value="0.02">2%</option><option value="0.05">5%</option></select></label>
          <label><input type="checkbox" data-k="envelope"> envelope</label>
          <label><input type="checkbox" data-k="estimates"> formula marks</label>
          <label><input type="checkbox" data-k="norm"> normalised time</label>
          <button class="tool" data-act="fit">Fit axes</button></span></h2>
        <div class="canvas-wrap plot-wrap"></div>
        <div class="legend"><span><i style="border-color:var(--series-1)"></i>y(t)</span><span class="lg-env"><i class="dot" style="border-color:var(--muted)"></i>envelope 1 ± e<sup>−σt</sup>/√(1−ζ²)</span><span class="lg-est"><i class="dash" style="border-color:var(--series-2)"></i>formula estimates</span><span><i style="border-color:var(--band);border-top-width:8px"></i>settling band</span></div>
      </div>
      <div class="card"><h2>Measured versus formula</h2><div class="table reveal-sensitive"></div><p class="hint tab-note reveal-sensitive"></p></div>
    </div>
  </div>`);
  panel.append(layout);

  const splane = new SPlane($(layout, ".splane-wrap"), {
    onDrag: (id, re, im) => {
      if (st.mode === "first") st.sigma = Math.max(0.05, Math.min(50, -re));
      else Object.assign(st, dragPair(st, id, re, im, { zetaMax: 2, wnMax: 20 }));
      sync();
      update();
    },
  });
  const plot = new Plot($(layout, ".plot-wrap"), { xlabel: "t (s)", ylabel: "y(t)" });
  app.registerPlot(plot);
  const riseInset = new Plot($(layout, ".rise-inset"), { xlabel: "ζ", ylabel: "ωn·t_r" });
  const mpInset = new Plot($(layout, ".mp-inset"), { xlabel: "ζ", ylabel: "M_p (%)" });

  const sliders = $(layout, ".sliders");
  const sZeta = slider({ name: "ζ", min: 0.02, max: 2, step: 0.005, value: st.zeta, onInput: (v) => { st.zeta = v; update(); } });
  const sWn = slider({ name: "ωn", min: 0.2, max: 20, step: 0.01, value: st.wn, log: true, onInput: (v) => { st.wn = v; update(); } });
  const sSig = slider({ name: "σ", min: 0.05, max: 20, step: 0.01, value: st.sigma, log: true, onInput: (v) => { st.sigma = v; update(); } });
  sliders.append(sZeta.node, sWn.node, sSig.node);

  layout.querySelectorAll("[data-k]").forEach((inp) => {
    inp.addEventListener("change", () => {
      const k = inp.dataset.k;
      st[k] = inp.type === "checkbox" ? inp.checked : parseFloat(inp.value);
      if (k === "norm") view = null;
      update();
    });
  });
  $(layout, '[data-act="fit"]').addEventListener("click", () => { view = null; update(); });
  $(layout, '[data-act="fitS"]').addEventListener("click", () => fitS());
  $(layout, '[data-act="first"]').addEventListener("click", () => {
    st.mode = st.mode === "first" ? "second" : "first";
    if (st.mode === "first") st.sigma = st.zeta * st.wn;
    view = null;
    sync();
    fitS();
    update();
  });

  function poles() {
    return st.mode === "first" ? [{ re: -st.sigma, im: 0 }] : pairFromZetaWn(st.zeta, st.wn);
  }

  function fitS() {
    splane.fit(poles(), { margin: 0.6, minSpan: 1 });
  }

  function sync() {
    sZeta.set(st.zeta);
    sWn.set(st.wn);
    sSig.set(st.sigma);
    const first = st.mode === "first";
    sZeta.node.hidden = first;
    sWn.node.hidden = first;
    sSig.node.hidden = !first;
    $(layout, '[data-act="first"]').setAttribute("aria-pressed", String(first));
    $(layout, ".insets").hidden = first;
    layout.querySelectorAll("[data-k]").forEach((inp) => {
      if (inp.type === "checkbox") inp.checked = st[inp.dataset.k];
      else inp.value = String(st[inp.dataset.k]);
    });
  }

  function update() {
    app.edited();
    render();
  }

  function render() {
    const first = st.mode === "first";
    const sys = { poles: poles(), zeros: [], gain: null };
    const k = st.norm ? (first ? st.sigma : st.wn) : 1;
    const res = analyze(sys, { eps: st.eps, minT: view ? view.x1 / k : 0 });
    const m = res.metrics;
    const est = first ? null : secondOrderEstimates(st.zeta, st.wn, st.eps);
    // For ζ > 1 the slow real pole, not ζωn, sets the decay; use it for the settling estimate.
    const over = !first && st.zeta > 1;
    const sigmaSlow = over ? st.wn * (st.zeta - Math.sqrt(st.zeta ** 2 - 1)) : null;
    if (over) est.ts = (est.ts * est.sigma) / sigmaSlow;
    const ex = first ? firstOrderExact(st.sigma, st.eps) : null;
    const sigma = first ? st.sigma : st.zeta * st.wn;

    splane.setRoots(pairRoots(sys.poles));

    // readout
    const ro = $(layout, ".readout");
    if (first) ro.innerHTML = `<span>pole <b>s = −${fmtNum(sigma)}</b></span><span>τ = 1/σ = <b>${fmtNum(1 / sigma)} s</b></span>`;
    else {
      const wd = st.zeta < 1 ? st.wn * Math.sqrt(1 - st.zeta ** 2) : 0;
      ro.innerHTML = `<span>ζ <b>${fmtNum(st.zeta)}</b></span><span>ω<sub>n</sub> <b>${fmtNum(st.wn)}</b> rad/s</span>${over ? `<span>slow pole σ = <b>${fmtNum(sigmaSlow)}</b> s⁻¹</span>` : `<span>σ = ζω<sub>n</sub> <b>${fmtNum(sigma)}</b> s⁻¹</span>`}<span>ω<sub>d</sub> <b>${st.zeta < 1 ? fmtNum(wd) : "—"}</b> rad/s</span><span>θ = sin⁻¹ζ <b>${st.zeta < 1 ? fmtNum((Math.asin(st.zeta) * 180) / Math.PI) + "°" : "—"}</b></span>`;
    }

    // response plot
    const t = Array.from(res.t, (v) => v * k);
    const layers = [];
    if (st.envelope && !first && st.zeta < 1) {
      const c = 1 / Math.sqrt(1 - st.zeta ** 2);
      const up = Array.from(res.t, (v) => 1 + c * Math.exp(-sigma * v));
      const dn = Array.from(res.t, (v) => 1 - c * Math.exp(-sigma * v));
      layers.push({ type: "line", x: t, y: up, color: "--muted", width: 1.2, dash: [2, 3] }, { type: "line", x: t, y: dn, color: "--muted", width: 1.2, dash: [2, 3] });
    }
    layers.push(...specLayers(m, { k, eps: st.eps }));
    if (st.estimates) {
      if (!first) {
        layers.push({ type: "vline", x: est.ts * k, color: "--series-2", dash: [6, 4], width: 1.5, label: `${fmtNum(est.ts * (over ? sigmaSlow : sigma), 2)}/σ${over ? "_slow" : ""} = ${fmtNum(est.ts)} s`, textColor: "--ink-2", keep: true, row: 1 });
        if (est.tsEnvelope) layers.push({ type: "vline", x: est.tsEnvelope * k, color: "--muted", dash: [2, 3], width: 1.2, label: "envelope bound", keep: true, row: 2 });
        if (est.Mp > 0) layers.push({ type: "hline", y: 1 + est.Mp, color: "--series-2", dash: [6, 4], width: 1.5, label: `e^(−πζ/√(1−ζ²)) → ${pct(est.Mp)}`, textColor: "--ink-2", keep: true, labelAlign: "left" });
        if (m.t10 !== null) layers.push({ type: "segment", x0: m.t10 * k, y0: 0.5, x1: (m.t10 + est.rise) * k, y1: 0.5, color: "--series-2", width: 1.5, dash: [6, 4], arrows: true, label: `1.8/ωn = ${fmtNum(est.rise)} s`, textColor: "--ink-2" });
      } else {
        layers.push({ type: "vline", x: ex.tau * k, color: "--series-2", dash: [6, 4], width: 1.5, label: `τ = 1/σ (63%)`, textColor: "--ink-2", keep: true });
      }
    }
    layers.push({ type: "line", x: t, y: Array.from(res.y), color: "--series-1", width: 2.25, label: "y" });
    const T = displayT(res);
    if (!view) view = fitView(res.t, [res.y], { k, T, yf: 1 });
    plot.xlabel = st.norm ? (first ? "σt" : "ωn·t (rad)") : "t (s)";
    plot.set(layers, view);
    $(layout, ".lg-env").hidden = first || !st.envelope;
    $(layout, ".lg-est").hidden = !st.estimates;

    // table
    const err = (meas, f) => {
      if (meas === null || f === null || meas === 0) return "";
      const e = (f - meas) / meas;
      if (Math.abs(e) < 5e-4) return `<span class="err-ok">≈ 0</span>`;
      return `<span class="${Math.abs(e) > 0.1 ? "err-pos" : "err-ok"}">${e >= 0 ? "+" : ""}${fmtNum(e * 100, 2)}%</span>`;
    };
    const bandTxt = `${st.eps * 100}%`;
    let rows;
    if (first) {
      rows = [
        ["Rise time t<sub>r</sub>", secs(m.rise), secs(ex.rise), "ln 9 / σ (exact)", err(m.rise, ex.rise)],
        ["Overshoot M<sub>p</sub>", pct(m.Mp), "0%", "monotone", ""],
        [`Settling t<sub>s</sub> (${bandTxt})`, secs(m.ts), secs(ex.ts), `ln(1/${st.eps}) / σ (exact)`, err(m.ts, ex.ts)],
        ["Time constant τ", "", secs(ex.tau), "1/σ: 63% of final value", ""],
      ];
    } else {
      rows = [
        ["Rise time t<sub>r</sub>", secs(m.rise), secs(est.rise), "1.8/ω<sub>n</sub> (fit)", err(m.rise, est.rise)],
        ["Overshoot M<sub>p</sub>", pct(m.Mp), pct(est.Mp), st.zeta < 1 ? "e<sup>−πζ/√(1−ζ²)</sup> (exact)" : "ζ ≥ 1: none", ""],
        ["Peak time t<sub>p</sub>", secs(m.tp), secs(est.tp), st.zeta < 1 ? "π/ω<sub>d</sub> (exact)" : "no peak", st.zeta < 1 ? err(m.tp, est.tp) : ""],
        [`Settling t<sub>s</sub> (${bandTxt})`, secs(m.ts), secs(est.ts), over ? `${fmtNum(est.ts * sigmaSlow, 2)}/σ<sub>slow</sub> (slowest pole)` : `${fmtNum(est.ts * sigma, 2)}/σ (decay rate only)`, err(m.ts, est.ts)],
        ["Envelope bound", "", secs(est.tsEnvelope), st.zeta < 1 ? "−ln(ε√(1−ζ²))/σ (guaranteed)" : "not defined for ζ ≥ 1", ""],
      ];
    }
    $(layout, ".table").innerHTML = `<table class="metrics"><thead><tr><th></th><th>Measured</th><th>Formula</th><th style="text-align:left">Formula used</th><th>Error</th></tr></thead><tbody>${rows
      .map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td class="note">${r[3]}</td><td>${r[4]}</td></tr>`)
      .join("")}</tbody></table>`;
    let note = "";
    if (!first) {
      if (over) note = "Overdamped: two real poles. The slower one, at −(ζ − √(ζ²−1))ω<sub>n</sub>, dominates settling, so σ = ζω<sub>n</sub> no longer describes the decay; its residue also exceeds 1, so ln(1/ε)/σ<sub>slow</sub> is still optimistic.";
      else if (st.zeta >= 0.95) note = "Near critical damping the decay-rate rule underestimates settling: the response is (1 + ω<sub>n</sub>t)e<sup>−ω<sub>n</sub>t</sup> at ζ = 1, and ω<sub>n</sub>t<sub>s</sub> ≈ 6.64 for 1%.";
      else if (m.ts !== null && m.ts > est.ts) note = "The measured settling time is later than the estimate: 4.6/σ drops the 1/√(1−ζ²) prefactor, so it is not a guaranteed bound.";
      else note = "Settling happens at the last band crossing, so it can be earlier than the envelope bound.";
    }
    $(layout, ".tab-note").innerHTML = note;

    // insets
    if (!first) {
      const rc = getRiseCurve();
      const cur = m.rise !== null ? m.rise * st.wn : null;
      riseInset.set([
        { type: "hline", y: 1.8, color: "--series-2", dash: [6, 4], width: 1.5, label: "1.8 (textbook)", textColor: "--ink-2" },
        { type: "line", x: rc.z, y: rc.r, color: "--series-1", width: 2, label: "ωn·t_r" },
        ...(cur !== null && st.zeta <= 1.5 ? [{ type: "marker", x: st.zeta, y: cur, shape: "diamond", color: "--series-1", size: 6, label: `ζ=${fmtNum(st.zeta, 3)}: ${fmtNum(cur)}` }] : []),
      ], { x0: 0, x1: 1.5, y0: 0.8, y1: Math.max(...rc.r) * 1.08 });
      const zz = [], mp = [];
      for (let z = 0.02; z < 1; z += 0.005) { zz.push(z); mp.push(mpFromZeta(z) * 100); }
      zz.push(1, 1.5); mp.push(0, 0);
      mpInset.set([
        { type: "line", x: zz, y: mp, color: "--series-1", width: 2, label: "M_p %" },
        { type: "marker", x: 0.5, y: 16.3, shape: "dot", color: "--muted", size: 3.5, label: "0.5 → 16%", labelDir: "ne" },
        { type: "marker", x: 0.7, y: 4.6, shape: "dot", color: "--muted", size: 3.5, label: "0.7 → 5%", labelDir: "ne" },
        ...(st.zeta <= 1.5 ? [{ type: "marker", x: st.zeta, y: mpFromZeta(st.zeta) * 100, shape: "diamond", color: "--series-1", size: 6, label: `ζ=${fmtNum(st.zeta, 3)}`, labelDir: "nw" }] : []),
      ], { x0: 0, x1: 1.5, y0: -4, y1: 100 });
    }
  }

  sync();
  fitS();
  render();

  return {
    debug: { splane, plot },
    activate() { render(); },
    redraw() { render(); },
    getState() { return st; },
    setState(s) { st = { ...DEFAULT, ...s }; view = null; sync(); fitS(); render(); },
  };
}
