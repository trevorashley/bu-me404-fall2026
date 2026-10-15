// The time-response canvas: y(t) above u(t), with the final value, the 1% band,
// the settling time, and badges for unstable / marginal / truncated runs.

import { niceTicks, readColors, setupCanvas, tickLabel } from './plotutil.js';

const UNSTABLE_CLIP = 5;        // unstable loops: y axis clipped to +/- 5 x the unit reference
const PAD = { left: 46, right: 12, top: 10, bottom: 26, gap: 22 };
const Y_FRACTION = 0.62;        // share of the plot height given to y(t)
const RANGE_MARGIN = 0.08;
const EARLY_FRACTION = 0.25;    // u clip uses the peak over this leading part of an unstable run
const MIN_SPAN = 1e-9;

export class TimePlot {
  constructor(canvas) {
    this.canvas = canvas;
    this.model = null;
  }

  /** model = {trace, metrics, stability, input, error} or null to clear. */
  setModel(model) {
    this.model = model;
    this.draw();
  }

  draw() {
    const { ctx, w, h } = setupCanvas(this.canvas);
    const c = readColors();
    ctx.fillStyle = c.bg;
    ctx.fillRect(0, 0, w, h);
    const m = this.model;
    if (!m || !m.trace) {
      this.message(ctx, c, w, h, m?.error ?? 'No response to show.');
      return;
    }
    const innerH = h - PAD.top - PAD.bottom - PAD.gap;
    const yBox = { x: PAD.left, y: PAD.top, w: w - PAD.left - PAD.right, h: innerH * Y_FRACTION };
    const uBox = { x: yBox.x, y: yBox.y + yBox.h + PAD.gap, w: yBox.w, h: innerH * (1 - Y_FRACTION) };
    const unstable = m.stability === 'unstable';
    const yRange = unstable ? [-UNSTABLE_CLIP, UNSTABLE_CLIP] : this.range(m.trace.y, m.metrics.yInf, m.input === 'ref' ? 1 : 0);
    const uRange = unstable ? this.earlyRange(m.trace.u) : this.range(m.trace.u, 0);
    const T = m.trace.T;
    this.panel(ctx, c, yBox, yRange, T, 'y', false);
    this.panel(ctx, c, uBox, uRange, T, 'u', true);
    this.bandAndReference(ctx, c, yBox, yRange, T, m);
    this.trace(ctx, c.y, yBox, yRange, m.trace.t, m.trace.y, T);
    this.trace(ctx, c.u, uBox, uRange, m.trace.t, m.trace.u, T);
    this.badges(ctx, c, yBox, m);
  }

  message(ctx, c, w, h, text) {
    ctx.fillStyle = c.muted;
    ctx.font = '14px system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(text, w / 2, h / 2);
  }

  /** Value range covering the data and the given anchors, with a margin. */
  range(series, ...anchors) {
    let lo = Math.min(0, ...anchors.filter((a) => a !== null));
    let hi = Math.max(0, ...anchors.filter((a) => a !== null));
    for (const v of series) { if (v < lo) lo = v; if (v > hi) hi = v; }
    const pad = Math.max(hi - lo, MIN_SPAN) * RANGE_MARGIN;
    return [lo - pad, hi + pad];
  }

  /** For divergent runs, scale u by the early part of the record so the start stays readable. */
  earlyRange(u) {
    const n = Math.max(2, Math.floor(u.length * EARLY_FRACTION));
    let peak = 1;
    for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(u[i]));
    return [-UNSTABLE_CLIP * peak, UNSTABLE_CLIP * peak];
  }

  xOf(box, t, T) { return box.x + (t / T) * box.w; }
  yOf(box, v, range) { return box.y + box.h - ((v - range[0]) / (range[1] - range[0])) * box.h; }

  panel(ctx, c, box, range, T, label, showTime) {
    ctx.font = '11px system-ui, sans-serif';
    ctx.lineWidth = 1;
    ctx.strokeStyle = c.grid;
    ctx.fillStyle = c.muted;
    ctx.textAlign = 'right';
    for (const v of niceTicks(range[0], range[1], Math.max(2, box.h / 45))) {
      const y = this.yOf(box, v, range);
      ctx.beginPath(); ctx.moveTo(box.x, y); ctx.lineTo(box.x + box.w, y); ctx.stroke();
      ctx.fillText(tickLabel(v), box.x - 5, y + 4);
    }
    ctx.textAlign = 'center';
    for (const v of niceTicks(0, T, Math.max(3, box.w / 90))) {
      const x = this.xOf(box, v, T);
      ctx.beginPath(); ctx.moveTo(x, box.y); ctx.lineTo(x, box.y + box.h); ctx.stroke();
      if (showTime) ctx.fillText(tickLabel(v), x, box.y + box.h + 14);
    }
    if (showTime) ctx.fillText('t (s)', box.x + box.w / 2, box.y + box.h + 25);
    ctx.strokeStyle = c.axis;
    ctx.strokeRect(box.x, box.y, box.w, box.h);
    ctx.fillStyle = c.fg;
    ctx.textAlign = 'left';
    ctx.fillText(`${label}(t)`, box.x + 6, box.y + 14);
  }

  bandAndReference(ctx, c, box, range, T, m) {
    ctx.save();
    ctx.beginPath(); ctx.rect(box.x, box.y, box.w, box.h); ctx.clip();
    if (m.input === 'ref') this.hline(ctx, c.muted, box, range, 1, [6, 4]);
    const yInf = m.metrics.yInf;
    if (yInf !== null) {
      const half = m.metrics.band;
      const top = this.yOf(box, yInf + half, range);
      const bottom = this.yOf(box, yInf - half, range);
      ctx.fillStyle = c.band;
      ctx.fillRect(box.x, top, box.w, Math.max(1, bottom - top));
      this.hline(ctx, c.y, box, range, yInf, [2, 3]);
      if (m.metrics.ts !== null && m.metrics.ts > 0) {
        const x = this.xOf(box, m.metrics.ts, T);
        ctx.strokeStyle = c.muted;
        ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(x, box.y); ctx.lineTo(x, box.y + box.h); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = c.muted;
        ctx.textAlign = 'left';
        ctx.fillText('ts', x + 3, box.y + box.h - 5);
      }
    }
    ctx.restore();
  }

  hline(ctx, color, box, range, value, dash) {
    const y = this.yOf(box, value, range);
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.setLineDash(dash);
    ctx.beginPath(); ctx.moveTo(box.x, y); ctx.lineTo(box.x + box.w, y); ctx.stroke();
    ctx.setLineDash([]);
  }

  trace(ctx, color, box, range, t, v, T) {
    ctx.save();
    ctx.beginPath(); ctx.rect(box.x, box.y, box.w, box.h); ctx.clip();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    for (let i = 0; i < t.length; i++) {
      const x = this.xOf(box, t[i], T);
      const y = this.yOf(box, v[i], range);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.restore();
  }

  badges(ctx, c, box, m) {
    const items = [];
    if (m.stability === 'unstable') items.push(['UNSTABLE', c.bad]);
    else if (m.stability === 'marginal') items.push(['MARGINAL', c.ctrl]);
    if (m.trace.impulseU) items.push(['u: derivative impulse omitted', c.muted]);
    ctx.font = 'bold 11px system-ui, sans-serif';
    ctx.textAlign = 'right';
    let y = box.y + 16;
    for (const [text, color] of items) {
      const width = ctx.measureText(text).width + 12;
      const x = box.x + box.w - 6;
      ctx.fillStyle = c.bg;
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.fillRect(x - width, y - 12, width, 18);
      ctx.strokeRect(x - width, y - 12, width, 18);
      ctx.fillStyle = color;
      ctx.fillText(text, x - 6, y + 1);
      y += 22;
    }
  }
}
