// Interactive s-plane: constant-ζ rays and constant-ωn arcs, draggable pole (×)
// and zero (○) markers with automatic conjugate mirroring, and a hook for
// tab-specific overlays (specification regions, reference lines).
//
// The widget does not own the system. Each root passed to setRoots() is
//   {id, kind: "pole"|"zero", re, im, pair, draggable, color, muted, label}
// and dragging reports onDrag(id, re, im, phase) with im >= 0; the tab decides
// what the drag means and calls setRoots() again.

import { cssVar, uiScale, niceTicks, fmtTick, drawMarker, fmtNum } from "./plot.js";

export class SPlane {
  constructor(wrap, { onDrag = () => {}, onSelect = () => {}, overlay = null, snapAxisPx = 9, snap = 0, zetaRays = [0.1, 0.3, 0.5, 0.7, 0.9] } = {}) {
    this.wrap = wrap;
    this.canvas = document.createElement("canvas");
    wrap.append(this.canvas);
    this.ctx = this.canvas.getContext("2d");
    this.onDrag = onDrag;
    this.onSelect = onSelect;
    this.overlay = overlay;
    this.snapAxisPx = snapAxisPx;
    this.snap = snap;
    this.zetaRays = zetaRays;
    this.roots = [];
    this.selected = null;
    this.drag = null;
    this.hover = null;
    this.view = { xmin: -4, xmax: 1, ymax: 3 };
    new ResizeObserver(() => this.render()).observe(wrap);
    const c = this.canvas;
    c.addEventListener("pointerdown", (e) => this.#down(e));
    c.addEventListener("pointermove", (e) => this.#move(e));
    c.addEventListener("pointerup", (e) => this.#up(e));
    c.addEventListener("pointercancel", (e) => this.#up(e));
    c.addEventListener("pointerleave", () => { if (!this.drag) { this.hover = null; this.render(); } });
  }

  setRoots(roots) {
    this.roots = roots;
    this.render();
  }

  // Fit a view around the given points (plus the origin) with equal aspect.
  fit(points = this.roots, { margin = 0.3, minSpan = 2, includeRhp = 0.15 } = {}) {
    let xmin = 0, xmax = 0, ymax = 0;
    for (const p of points) {
      xmin = Math.min(xmin, p.re);
      xmax = Math.max(xmax, p.re);
      ymax = Math.max(ymax, Math.abs(p.im));
    }
    let span = Math.max(xmax - xmin, 2 * ymax, minSpan);
    const m = span * margin;
    xmin -= m;
    xmax = Math.max(xmax + m, span * includeRhp);
    ymax = Math.max(ymax + m, (xmax - xmin) / 2);
    this.view = { xmin, xmax, ymax };
    this.render();
  }

  setView(view) {
    this.view = view;
    this.render();
  }

  // Equal-aspect mapping that shows at least the requested view.
  #geom() {
    const { xmin, xmax, ymax } = this.view;
    const k = Math.min(this.w / (xmax - xmin), this.h / (2 * ymax));
    const cx = this.w / 2 - ((xmin + xmax) / 2) * k;
    const cy = this.h / 2;
    return { k, cx, cy };
  }

  toPx(re, im) {
    const { k, cx, cy } = this.#geom();
    return [cx + re * k, cy - im * k];
  }

  toS(px, py) {
    const { k, cx, cy } = this.#geom();
    return { re: (px - cx) / k, im: (cy - py) / k };
  }

  get bounds() {
    const a = this.toS(0, 0), b = this.toS(this.w, this.h);
    return { re0: a.re, re1: b.re, im0: b.im, im1: a.im };
  }

  #hit(px, py) {
    const R = 16 * uiScale();
    let best = null, bd = R;
    for (const r of this.roots) {
      if (r.draggable === false) continue;
      const pts = [this.toPx(r.re, r.im)];
      if (r.pair || r.im > 0) pts.push(this.toPx(r.re, -r.im));
      for (const [x, y] of pts) {
        const d = Math.hypot(x - px, y - py);
        if (d < bd) { bd = d; best = r; }
      }
    }
    return best;
  }

  #toRoot(e) {
    let { re, im } = this.toS(e.offsetX, e.offsetY);
    im = Math.abs(im);
    const { k } = this.#geom();
    if (this.snap > 0) {
      re = Math.round(re / this.snap) * this.snap;
      im = Math.round(im / this.snap) * this.snap;
    }
    if (im * k < this.snapAxisPx * uiScale()) im = 0;
    return { re, im };
  }

  #down(e) {
    const r = this.#hit(e.offsetX, e.offsetY);
    this.selected = r ? r.id : null;
    this.onSelect(this.selected);
    if (r) {
      this.drag = { id: r.id, moved: false };
      this.canvas.setPointerCapture(e.pointerId);
    }
    this.render();
  }

  #move(e) {
    this.hover = this.toS(e.offsetX, e.offsetY);
    if (this.drag) {
      const { re, im } = this.#toRoot(e);
      this.drag.moved = true;
      this.onDrag(this.drag.id, re, im, "move");
    } else {
      this.canvas.style.cursor = this.#hit(e.offsetX, e.offsetY) ? "grab" : "crosshair";
      this.render();
    }
  }

  #up(e) {
    if (this.drag) {
      const { re, im } = this.#toRoot(e);
      if (this.drag.moved) this.onDrag(this.drag.id, re, im, "end");
      this.drag = null;
    }
  }

  render() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.wrap.getBoundingClientRect();
    this.w = rect.width;
    this.h = rect.height;
    if (!this.w || !this.h) return;
    this.canvas.width = Math.round(this.w * dpr);
    this.canvas.height = Math.round(this.h * dpr);
    const ctx = this.ctx;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, this.w, this.h);
    const s = uiScale();
    const font = `${11.5 * s}px system-ui, -apple-system, "Segoe UI", sans-serif`;
    ctx.font = font;
    const B = this.bounds;
    const [ox, oy] = this.toPx(0, 0);

    // RHP tint
    ctx.fillStyle = cssVar("--shade");
    ctx.fillRect(ox, 0, this.w - ox, this.h);

    // ωn arcs (left half plane) and axis ticks
    const reach = Math.max(-B.re0, B.im1);
    const ticks = niceTicks(0, reach, 5).filter((v) => v > 0);
    const step = ticks.length > 1 ? ticks[1] - ticks[0] : ticks[0] || 1;
    ctx.strokeStyle = cssVar("--grid");
    ctx.lineWidth = 1;
    const { k } = this.#geom();
    for (const r of ticks) {
      ctx.beginPath();
      ctx.arc(ox, oy, r * k, Math.PI / 2, (3 * Math.PI) / 2);
      ctx.stroke();
    }
    // ζ rays
    ctx.fillStyle = cssVar("--muted");
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const L = Math.hypot(this.w, this.h) * 2;
    for (const z of this.zetaRays) {
      const th = Math.asin(z); // angle from the imaginary axis
      const dx = -Math.sin(th), dy = Math.cos(th);
      ctx.beginPath();
      ctx.moveTo(ox, oy);
      ctx.lineTo(ox + dx * L, oy - dy * L);
      ctx.moveTo(ox, oy);
      ctx.lineTo(ox + dx * L, oy + dy * L);
      ctx.stroke();
      // label near the top edge of the view
      const tEdge = Math.min(oy / Math.max(dy, 1e-6), ox / Math.max(-dx, 1e-6)) * 0.88;
      const lx = ox + dx * tEdge, ly = oy - dy * tEdge;
      if (lx > 12 && ly > 8) ctx.fillText(`ζ=${z}`, lx, ly);
    }

    // axes
    ctx.strokeStyle = cssVar("--axis");
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, oy); ctx.lineTo(this.w, oy);
    ctx.moveTo(ox, 0); ctx.lineTo(ox, this.h);
    ctx.stroke();
    ctx.fillStyle = cssVar("--muted");
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    for (const v of niceTicks(B.re0, B.re1, 7)) {
      if (Math.abs(v) < 1e-12) continue;
      const [px] = this.toPx(v, 0);
      ctx.fillRect(px - 0.5, oy - 3, 1, 6);
      ctx.fillText(fmtTick(v, step), px, oy + 5 * s);
    }
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    for (const v of niceTicks(B.im0, B.im1, 7)) {
      if (Math.abs(v) < 1e-12) continue;
      const [, py] = this.toPx(0, v);
      ctx.fillRect(ox - 3, py - 0.5, 6, 1);
      ctx.fillText(fmtTick(v, step) + "j", ox + 6 * s, py);
    }
    ctx.fillStyle = cssVar("--ink-2");
    ctx.textAlign = "right";
    ctx.textBaseline = "bottom";
    ctx.fillText("Re(s)", this.w - 6, oy - 4);
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText("Im(s)", ox + 6, 6);

    if (this.overlay) {
      ctx.save();
      this.overlay(ctx, { toPx: (a, b) => this.toPx(a, b), toS: (a, b) => this.toS(a, b), w: this.w, h: this.h, k, ox, oy, s, bounds: B });
      ctx.restore();
    }

    // roots
    const ring = cssVar("--surface");
    for (const r of this.roots) {
      const color = cssVar(r.color || (r.muted ? "--muted" : "--ink"));
      const size = (r.kind === "pole" ? 7 : 7) * s;
      const pts = [[r.re, r.im]];
      if (r.pair || r.im > 0) pts.push([r.re, -r.im]);
      for (const [a, b] of pts) {
        const [px, py] = this.toPx(a, b);
        if (r.id === this.selected && r.draggable !== false) {
          ctx.fillStyle = cssVar("--band");
          ctx.beginPath(); ctx.arc(px, py, 15 * s, 0, 2 * Math.PI); ctx.fill();
          ctx.strokeStyle = cssVar("--accent"); ctx.lineWidth = 1.5;
          ctx.stroke();
        }
        if (r.kind === "zero") {
          ctx.fillStyle = ring;
          ctx.beginPath(); ctx.arc(px, py, size, 0, 2 * Math.PI); ctx.fill();
        }
        drawMarker(ctx, r.kind === "pole" ? "x" : "o", px, py, size, color, ring);
      }
      if ((r.pair || r.im > 0) && r.im === 0) {
        const [px, py] = this.toPx(r.re, 0);
        ctx.fillStyle = cssVar("--ink-2");
        ctx.textAlign = "left";
        ctx.textBaseline = "bottom";
        ctx.font = font;
        ctx.fillText("×2", px + 8 * s, py - 6 * s);
      }
      if (r.label) {
        const [px, py] = this.toPx(r.re, r.im);
        ctx.fillStyle = cssVar("--ink-2");
        ctx.textAlign = "left";
        ctx.textBaseline = "bottom";
        ctx.font = font;
        ctx.fillText(r.label, px + 9 * s, py - 8 * s);
      }
    }

    // hover readout
    if (this.hover) {
      const { re, im } = this.hover;
      const wn = Math.hypot(re, im);
      const z = wn > 0 ? -re / wn : 0;
      const txt = `s = ${fmtNum(re)} ${im < 0 ? "−" : "+"} ${fmtNum(Math.abs(im))}j   ζ ${fmtNum(z, 2)}   ωn ${fmtNum(wn)}   σ ${fmtNum(-re)}`;
      ctx.font = font;
      const tw = ctx.measureText(txt).width;
      ctx.fillStyle = cssVar("--surface");
      ctx.globalAlpha = 0.85;
      ctx.fillRect(4, this.h - 22 * s, tw + 12, 18 * s);
      ctx.globalAlpha = 1;
      ctx.fillStyle = cssVar("--ink-2");
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(txt, 10, this.h - 13 * s);
    }
  }
}
