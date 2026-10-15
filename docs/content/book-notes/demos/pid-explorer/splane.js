// The s-plane canvas: drawing, hit testing, dragging with conjugate mirroring.
//
// The plant is edited in place (state.plant.poles / zeros hold markers with
// im >= 0). `host.changed(phase)` is called after every edit; phase is 'drag'
// while a marker is moving and 'release' when it settles.

import { niceTicks, readColors, setupCanvas, tickLabel } from './plotutil.js';
import { poleInfo } from './loop.js';

const HIT_PX = 14;            // pick radius for mouse
const HIT_PX_TOUCH = 24;      // larger for fingers
const SNAP_PX = 8;            // a complex marker dragged this close to the real axis becomes two real ones
const ADD_REAL_PX = 12;       // adding this close to the real axis creates a real marker
const MARKER_R = 6;
const CLOSED_R = 4.5;
const NUDGE_PX = 4;           // arrow-key step, in pixels at the current zoom
const NUDGE_FAST = 5;         // shift multiplies the step
const ZOOM_STEP = 1.15;
const FIT_MARGIN = 1.35;
const MIN_FIT_SPAN = 2;
const CLICK_SLOP_PX = 4;      // movement below this counts as a click
const LOCUS_DOT_R = 1.7;

export class SPlane {
  constructor(canvas, host) {
    this.canvas = canvas;
    this.host = host;
    this.model = null;
    this.sel = null;          // {list: 'poles'|'zeros', index}
    this.addMode = null;      // 'poles' | 'zeros' | null
    this.tipIndex = null;     // index into model.cl.poles
    this.x0 = -5;             // real part at the left edge
    this.scale = 40;          // pixels per unit
    this.w = 1;
    this.h = 1;
    this.drag = null;
    this.bind();
  }

  get plant() { return this.host.state.plant; }

  // --- Coordinates -----------------------------------------------------------
  toPx(re, im) { return [(re - this.x0) * this.scale, this.h / 2 - im * this.scale]; }
  toWorld(px, py) { return [px / this.scale + this.x0, (this.h / 2 - py) / this.scale]; }

  /** Choose a view that contains the origin, every marker and every closed-loop pole. */
  fit() {
    const { w, h } = setupCanvas(this.canvas);
    const pts = [{ re: 0, im: 0 }];
    for (const m of [...this.plant.poles, ...this.plant.zeros]) pts.push(m);
    const cl = this.model?.cl;
    if (cl) pts.push(...cl.poles, ...cl.ctrlZeros); // the filter pole is far out and would squash the view
    const res = pts.map((p) => p.re);
    const reMin = Math.min(...res);
    const reMax = Math.max(...res);
    const imMax = Math.max(...pts.map((p) => Math.abs(p.im)));
    const spanX = Math.max(reMax - reMin, MIN_FIT_SPAN);
    const spanY = Math.max(2 * imMax, MIN_FIT_SPAN);
    this.scale = Math.min(w / (spanX * FIT_MARGIN), h / (spanY * FIT_MARGIN));
    this.x0 = (reMin + reMax) / 2 - w / (2 * this.scale);
    this.draw();
  }

  setModel(model) {
    this.model = model;
    const n = model?.cl?.poles.length ?? 0;
    if (this.tipIndex !== null && this.tipIndex >= n) this.tipIndex = null;
    this.draw();
  }

  setAddMode(mode) {
    this.addMode = mode;
    this.canvas.style.cursor = mode ? 'crosshair' : '';
  }

  // --- Drawing ---------------------------------------------------------------
  draw() {
    const { ctx, w, h } = setupCanvas(this.canvas);
    this.w = w;
    this.h = h;
    const c = readColors();
    ctx.fillStyle = c.bg;
    ctx.fillRect(0, 0, w, h);
    this.drawGrid(ctx, c);
    if (this.model?.locus) this.drawLocus(ctx, c);
    this.drawPlant(ctx, c);
    if (this.model?.cl) this.drawLoop(ctx, c);
    this.drawTip(ctx, c);
  }

  drawGrid(ctx, c) {
    const [x0px] = this.toPx(0, 0);
    ctx.fillStyle = c.rhp;
    ctx.fillRect(Math.max(0, x0px), 0, Math.max(0, this.w - x0px), this.h);
    ctx.font = '11px system-ui, sans-serif';
    ctx.fillStyle = c.muted;
    const [reLo] = this.toWorld(0, 0);
    const [reHi] = this.toWorld(this.w, 0);
    const imHi = this.h / 2 / this.scale;
    ctx.lineWidth = 1;
    ctx.textAlign = 'center';
    for (const v of niceTicks(reLo, reHi, Math.max(3, this.w / 80))) {
      const [x] = this.toPx(v, 0);
      this.line(ctx, x, 0, x, this.h, c.grid);
      ctx.fillStyle = c.muted;
      ctx.fillText(tickLabel(v), x, this.h - 4);
    }
    ctx.textAlign = 'left';
    for (const v of niceTicks(-imHi, imHi, Math.max(3, this.h / 60))) {
      const [, y] = this.toPx(0, v);
      this.line(ctx, 0, y, this.w, y, c.grid);
      if (v !== 0) ctx.fillText(`${tickLabel(v)}j`, 4, y - 3);
    }
    this.line(ctx, x0px, 0, x0px, this.h, c.axis, 1.5);       // imaginary axis
    this.line(ctx, 0, this.h / 2, this.w, this.h / 2, c.axis, 1.5); // real axis
  }

  line(ctx, x1, y1, x2, y2, color, width = 1) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  drawLocus(ctx, c) {
    const { locus } = this.model;
    ctx.fillStyle = c.locus;
    locus.forEach((sample, i) => {
      ctx.globalAlpha = 0.12 + 0.6 * (i / locus.length); // light to dark with increasing k
      for (const r of sample.roots) {
        const [x, y] = this.toPx(r.re, r.im);
        ctx.beginPath();
        ctx.arc(x, y, LOCUS_DOT_R, 0, 2 * Math.PI);
        ctx.fill();
      }
    });
    ctx.globalAlpha = 1;
  }

  drawPlant(ctx, c) {
    for (const list of ['poles', 'zeros']) {
      this.plant[list].forEach((m, index) => {
        const selected = this.sel?.list === list && this.sel.index === index;
        for (const im of m.im === 0 ? [0] : [m.im, -m.im]) {
          const [x, y] = this.toPx(m.re, im);
          const color = m.fixed ? c.muted : c.plant;
          if (selected) this.ring(ctx, x, y, MARKER_R + 6, c.fg);
          if (list === 'poles') this.cross(ctx, x, y, MARKER_R, color, m.fixed);
          else this.circle(ctx, x, y, MARKER_R, color, m.fixed);
        }
      });
    }
  }

  drawLoop(ctx, c) {
    const { cl } = this.model;
    for (const z of cl.ctrlZeros) this.plus(ctx, ...this.toPx(z.re, z.im), MARKER_R, c.ctrl);
    for (const p of cl.ctrlPoles) this.plus(ctx, ...this.toPx(p.re, p.im), MARKER_R, c.ctrl);
    cl.poles.forEach((p, i) => {
      const [x, y] = this.toPx(p.re, p.im);
      ctx.fillStyle = p.re > 0 ? c.bad : c.closed;
      ctx.beginPath();
      ctx.arc(x, y, CLOSED_R, 0, 2 * Math.PI);
      ctx.fill();
      if (i === this.tipIndex) this.ring(ctx, x, y, CLOSED_R + 4, c.fg);
    });
  }

  drawTip(ctx, c) {
    const p = this.model?.cl?.poles[this.tipIndex];
    if (!p) return;
    const info = poleInfo(p);
    const lines = [
      `pole ${tickLabel(p.re)} ${p.im < 0 ? '-' : '+'} ${tickLabel(Math.abs(p.im))}j`,
      `sigma = ${tickLabel(info.sigma)}, wd = ${tickLabel(info.wd)}`,
      `wn = ${tickLabel(info.wn)}, zeta = ${Number.isNaN(info.zeta) ? '-' : tickLabel(info.zeta)}`,
    ];
    ctx.font = '12px system-ui, sans-serif';
    const width = Math.max(...lines.map((l) => ctx.measureText(l).width)) + 12;
    const boxH = lines.length * 16 + 8;
    const [px, py] = this.toPx(p.re, p.im);
    const bx = Math.min(Math.max(4, px + 10), this.w - width - 4);
    const by = Math.min(Math.max(4, py - boxH - 10), this.h - boxH - 4);
    ctx.fillStyle = c.bg;
    ctx.strokeStyle = c.fg;
    ctx.lineWidth = 1;
    ctx.fillRect(bx, by, width, boxH);
    ctx.strokeRect(bx, by, width, boxH);
    ctx.fillStyle = c.fg;
    ctx.textAlign = 'left';
    lines.forEach((l, i) => ctx.fillText(l, bx + 6, by + 16 + i * 16));
  }

  // --- Marker glyphs ---------------------------------------------------------
  cross(ctx, x, y, r, color, dashed) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.setLineDash(dashed ? [3, 2] : []);
    ctx.beginPath();
    ctx.moveTo(x - r, y - r); ctx.lineTo(x + r, y + r);
    ctx.moveTo(x - r, y + r); ctx.lineTo(x + r, y - r);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  circle(ctx, x, y, r, color, dashed) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.setLineDash(dashed ? [3, 2] : []);
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  plus(ctx, x, y, r, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(x - r, y); ctx.lineTo(x + r, y);
    ctx.moveTo(x, y - r); ctx.lineTo(x, y + r);
    ctx.stroke();
  }

  ring(ctx, x, y, r, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.stroke();
  }

  // --- Hit testing -----------------------------------------------------------

  /** Nearest draggable plant marker within `radius` pixels, as {list, index}, or null. */
  hitMarker(px, py, radius) {
    let best = null;
    let bestDist = radius;
    for (const list of ['poles', 'zeros']) {
      this.plant[list].forEach((m, index) => {
        if (m.fixed) return;
        for (const im of m.im === 0 ? [0] : [m.im, -m.im]) {
          const [x, y] = this.toPx(m.re, im);
          const d = Math.hypot(px - x, py - y);
          if (d < bestDist) { bestDist = d; best = { list, index }; }
        }
      });
    }
    return best;
  }

  hitClosedPole(px, py, radius) {
    const poles = this.model?.cl?.poles ?? [];
    let best = null;
    let bestDist = radius;
    poles.forEach((p, i) => {
      const [x, y] = this.toPx(p.re, p.im);
      const d = Math.hypot(px - x, py - y);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    return best;
  }

  localPoint(e) {
    const r = this.canvas.getBoundingClientRect();
    return [e.clientX - r.left, e.clientY - r.top];
  }

  // --- Editing ---------------------------------------------------------------

  /** Move a marker to world (re, im). A complex marker dragged onto the axis splits into two real ones. */
  moveMarker(list, index, re, im) {
    const markers = this.plant[list];
    const m = markers[index];
    if (m.fixed) return;
    if (m.im === 0) { m.re = re; return; }
    if (Math.abs(im) * this.scale < SNAP_PX) {
      markers.splice(index, 1, { re, im: 0 }, { re, im: 0 });
      this.sel = { list, index };
    } else {
      m.re = re;
      m.im = Math.abs(im);
    }
  }

  addMarker(list, re, im) {
    const real = Math.abs(im) * this.scale < ADD_REAL_PX;
    this.plant[list].push({ re, im: real ? 0 : Math.abs(im) });
    this.sel = { list, index: this.plant[list].length - 1 };
    this.setAddMode(null);
    this.host.changed('release');
  }

  deleteSelected() {
    if (!this.sel) return;
    this.plant[this.sel.list].splice(this.sel.index, 1);
    this.sel = null;
    this.host.changed('release');
  }

  selectableMarkers() {
    const out = [];
    for (const list of ['poles', 'zeros']) {
      this.plant[list].forEach((m, index) => { if (!m.fixed) out.push({ list, index }); });
    }
    return out;
  }

  cycleSelection(step) {
    const all = this.selectableMarkers();
    if (!all.length) return;
    const cur = all.findIndex((s) => this.sel && s.list === this.sel.list && s.index === this.sel.index);
    this.sel = all[(cur + step + all.length) % all.length];
    this.draw();
  }

  nudge(dx, dy, fast) {
    if (!this.sel) return;
    const m = this.plant[this.sel.list][this.sel.index];
    const step = (NUDGE_PX * (fast ? NUDGE_FAST : 1)) / this.scale;
    this.moveMarker(this.sel.list, this.sel.index, m.re + dx * step, m.im + dy * step);
    this.host.changed('release');
  }

  zoom(factor, anchorPx = this.w / 2) {
    const [anchor] = this.toWorld(anchorPx, 0);
    this.scale *= factor;
    this.x0 = anchor - anchorPx / this.scale;
    this.draw();
  }

  // --- Events ----------------------------------------------------------------
  bind() {
    const cv = this.canvas;
    cv.addEventListener('pointerdown', (e) => this.onDown(e));
    cv.addEventListener('pointermove', (e) => this.onMove(e));
    cv.addEventListener('pointerup', (e) => this.onUp(e));
    cv.addEventListener('pointercancel', (e) => this.onUp(e));
    cv.addEventListener('keydown', (e) => this.onKey(e));
    cv.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.zoom(e.deltaY < 0 ? ZOOM_STEP : 1 / ZOOM_STEP, this.localPoint(e)[0]);
    }, { passive: false });
    // Stop the page from scrolling when a finger lands on a marker (touch-action alone cannot decide this).
    cv.addEventListener('touchstart', (e) => {
      const t = e.touches[0];
      const r = cv.getBoundingClientRect();
      if (this.addMode || this.hitMarker(t.clientX - r.left, t.clientY - r.top, HIT_PX_TOUCH)) e.preventDefault();
    }, { passive: false });
  }

  onDown(e) {
    this.canvas.focus({ preventScroll: true });
    const [px, py] = this.localPoint(e);
    const [re, im] = this.toWorld(px, py);
    if (this.addMode) { this.addMarker(this.addMode, re, im); return; }
    const radius = e.pointerType === 'touch' ? HIT_PX_TOUCH : HIT_PX;
    const hit = this.hitMarker(px, py, radius);
    this.canvas.setPointerCapture(e.pointerId);
    this.drag = { hit, startPx: px, startPy: py, startX0: this.x0, moved: false, clickPole: this.hitClosedPole(px, py, radius) };
    this.sel = hit;
    this.tipIndex = null;
    this.draw();
  }

  onMove(e) {
    const [px, py] = this.localPoint(e);
    if (!this.drag) {
      const over = this.hitMarker(px, py, HIT_PX) || this.hitClosedPole(px, py, HIT_PX) !== null;
      this.canvas.style.cursor = this.addMode ? 'crosshair' : over ? 'pointer' : '';
      return;
    }
    const d = this.drag;
    if (!d.moved && Math.hypot(px - d.startPx, py - d.startPy) < CLICK_SLOP_PX) return;
    d.moved = true;
    if (d.hit) {
      const [re, im] = this.toWorld(px, py);
      this.moveMarker(d.hit.list, this.sel.index, re, im);
      this.host.changed('drag');
    } else {
      this.x0 = d.startX0 - (px - d.startPx) / this.scale;
      this.draw();
    }
  }

  onUp(e) {
    const d = this.drag;
    this.drag = null;
    if (!d) return;
    if (d.hit && d.moved) this.host.changed('release');
    if (!d.moved && d.clickPole !== null) { this.tipIndex = d.clickPole; this.draw(); }
    if (this.canvas.hasPointerCapture(e.pointerId)) this.canvas.releasePointerCapture(e.pointerId);
  }

  onKey(e) {
    const arrows = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] };
    if (arrows[e.key]) { this.nudge(...arrows[e.key], e.shiftKey); }
    else if (e.key === '[') this.cycleSelection(-1);
    else if (e.key === ']') this.cycleSelection(1);
    else if (e.key === 'Delete' || e.key === 'Backspace') this.deleteSelected();
    else if (e.key === 'p' || e.key === 'z') this.addAtViewCentre(e.key === 'p' ? 'poles' : 'zeros');
    else if (e.key === '+' || e.key === '=') this.zoom(ZOOM_STEP);
    else if (e.key === '-') this.zoom(1 / ZOOM_STEP);
    else if (e.key === '0') this.fit();
    else if (e.key === 'Escape') { this.setAddMode(null); this.sel = null; this.draw(); }
    else return;
    e.preventDefault();
  }

  /** Keyboard path for adding a real marker: place it a third of the way in from the left. */
  addAtViewCentre(list) {
    const [re] = this.toWorld(this.w / 3, 0);
    this.addMarker(list, re, 0);
  }
}
