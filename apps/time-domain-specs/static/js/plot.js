// Small canvas line-plot widget: axes with nice ticks, layered marks, hover
// crosshair with a value tooltip, and a "hidden" mode for predict-then-reveal.
//
// Layers (drawn in order; colours may be CSS custom-property names like "--series-1"):
//   {type: "line", x, y, color, width, dash, label, alpha}
//   {type: "hline", y, color, dash, width, label}      {type: "vline", x, ...}
//   {type: "hband", y0, y1, fill}                       {type: "vspan", x0, x1, fill}
//   {type: "segment", x0, y0, x1, y1, color, dash, width, arrows}
//   {type: "marker", x, y, shape: "circle"|"x"|"diamond"|"star"|"dot", color, size, label, labelDir}
//   {type: "text", x, y, text, color, align, baseline}
// A layer with keep: true is still drawn while the plot is hidden.

export function cssVar(name) {
  if (!name) return name;
  if (!name.startsWith("--")) return name;
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export function uiScale() {
  return parseFloat(cssVar("--ui-scale")) || 1;
}

export function niceTicks(min, max, count = 6) {
  if (!(max > min)) return [min];
  const span = max - min;
  const raw = span / count;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const norm = raw / mag;
  const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
  const ticks = [];
  for (let v = Math.ceil(min / step - 1e-9) * step; v <= max + step * 1e-9; v += step) ticks.push(Math.abs(v) < step * 1e-9 ? 0 : v);
  return ticks;
}

export function fmtTick(v, step) {
  const d = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
  return v.toFixed(Math.min(d, 6));
}

export class Plot {
  constructor(wrap, { xlabel = "", ylabel = "", onGuess = null, tooltip = true, xfmt = null, yfmt = null } = {}) {
    this.wrap = wrap;
    this.canvas = document.createElement("canvas");
    this.tip = document.createElement("div");
    this.tip.className = "tooltip";
    wrap.append(this.canvas, this.tip);
    this.ctx = this.canvas.getContext("2d");
    this.xlabel = xlabel;
    this.ylabel = ylabel;
    this.layers = [];
    this.view = { x0: 0, x1: 1, y0: 0, y1: 1 };
    this.hidden = false;
    this.guess = null;
    this.onGuess = onGuess;
    this.tooltip = tooltip;
    this.hoverX = null;
    this.xfmt = xfmt;
    this.yfmt = yfmt;
    new ResizeObserver(() => this.render()).observe(wrap);
    this.canvas.addEventListener("pointermove", (e) => this.#hover(e));
    this.canvas.addEventListener("pointerleave", () => { this.hoverX = null; this.tip.style.display = "none"; this.render(); });
    this.canvas.addEventListener("click", (e) => {
      if (!this.hidden || !this.onGuess) return;
      const { x, y } = this.toData(e.offsetX, e.offsetY);
      this.guess = { x, y };
      this.onGuess(this.guess);
      this.render();
    });
  }

  set(layers, view) {
    this.layers = layers;
    if (view) this.view = view;
    this.render();
  }

  setHidden(hidden) {
    this.hidden = hidden;
    this.render();
  }

  get pad() {
    const s = uiScale();
    return { l: 56 * s, r: 14 * s, t: 12 * s, b: 42 * s };
  }

  toPx(x, y) {
    const { l, r, t, b } = this.pad;
    const W = this.w - l - r, H = this.h - t - b;
    const v = this.view;
    return [l + ((x - v.x0) / (v.x1 - v.x0)) * W, t + (1 - (y - v.y0) / (v.y1 - v.y0)) * H];
  }

  toData(px, py) {
    const { l, r, t, b } = this.pad;
    const W = this.w - l - r, H = this.h - t - b;
    const v = this.view;
    return { x: v.x0 + ((px - l) / W) * (v.x1 - v.x0), y: v.y0 + (1 - (py - t) / H) * (v.y1 - v.y0) };
  }

  #hover(e) {
    if (!this.tooltip) return;
    const { l, r } = this.pad;
    if (e.offsetX < l || e.offsetX > this.w - r) { this.hoverX = null; this.tip.style.display = "none"; this.render(); return; }
    this.hoverX = this.toData(e.offsetX, e.offsetY).x;
    this.render();
    if (this.hidden) { this.tip.style.display = "none"; return; }
    const rows = [];
    for (const L of this.layers) {
      if (L.type !== "line" || !L.label) continue;
      const v = interp(L.x, L.y, this.hoverX);
      if (v === null) continue;
      rows.push(`<div><span class="sw" style="background:${cssVar(L.color)}"></span>${L.label}: <b>${fmtNum(v)}</b></div>`);
    }
    if (!rows.length) { this.tip.style.display = "none"; return; }
    const xl = this.xlabel.split(" ")[0] || "x";
    this.tip.innerHTML = `<div>${xl} = <b>${fmtNum(this.hoverX)}</b></div>` + rows.join("");
    this.tip.style.display = "block";
    const tw = this.tip.offsetWidth;
    const left = e.offsetX + 14 + tw > this.w ? e.offsetX - tw - 14 : e.offsetX + 14;
    this.tip.style.left = `${left}px`;
    this.tip.style.top = `${Math.max(4, e.offsetY - 10)}px`;
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
    const font = `${12 * s}px system-ui, -apple-system, "Segoe UI", sans-serif`;
    ctx.font = font;
    const { l, r, t, b } = this.pad;
    const v = this.view;

    // grid and ticks
    const xt = niceTicks(v.x0, v.x1, Math.max(3, Math.floor((this.w - l - r) / (70 * s))));
    const yt = niceTicks(v.y0, v.y1, Math.max(3, Math.floor((this.h - t - b) / (45 * s))));
    const xstep = xt.length > 1 ? xt[1] - xt[0] : 1, ystep = yt.length > 1 ? yt[1] - yt[0] : 1;
    ctx.lineWidth = 1;
    ctx.strokeStyle = cssVar("--grid");
    ctx.fillStyle = cssVar("--muted");
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    for (const x of xt) {
      const [px] = this.toPx(x, 0);
      line(ctx, px, t, px, this.h - b);
      ctx.fillText(this.xfmt ? this.xfmt(x) : fmtTick(x, xstep), px, this.h - b + 5 * s);
    }
    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    for (const y of yt) {
      const [, py] = this.toPx(0, y);
      line(ctx, l, py, this.w - r, py);
      ctx.fillText(this.yfmt ? this.yfmt(y) : fmtTick(y, ystep), l - 6 * s, py);
    }
    ctx.strokeStyle = cssVar("--axis");
    if (v.y0 < 0 && v.y1 > 0) { const [, py] = this.toPx(0, 0); line(ctx, l, py, this.w - r, py); }
    line(ctx, l, this.h - b, this.w - r, this.h - b);
    line(ctx, l, t, l, this.h - b);
    ctx.fillStyle = cssVar("--ink-2");
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillText(this.xlabel, l + (this.w - l - r) / 2, this.h - 2);
    ctx.save();
    ctx.translate(12 * s, t + (this.h - t - b) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textBaseline = "top";
    ctx.fillText(this.ylabel, 0, -8 * s);
    ctx.restore();

    // data layers, clipped to the plot area
    ctx.save();
    ctx.beginPath();
    ctx.rect(l, t, this.w - l - r, this.h - t - b);
    ctx.clip();
    const labels = [];
    for (const L of this.layers) {
      if (this.hidden && !L.keep) continue;
      this.#drawLayer(ctx, L, s, labels);
    }
    if (this.guess) this.#drawLayer(ctx, { type: "marker", x: this.guess.x, y: this.guess.y, shape: "star", color: "--warn", size: 11, label: "your guess" }, s, labels);
    if (this.hoverX !== null && !this.hidden) {
      const [px] = this.toPx(this.hoverX, 0);
      ctx.strokeStyle = cssVar("--muted");
      ctx.setLineDash([3, 3]);
      line(ctx, px, t, px, this.h - b);
      ctx.setLineDash([]);
    }
    ctx.restore();
    // labels outside the clip so they are never cut off
    ctx.font = font;
    for (const lb of labels) {
      ctx.fillStyle = cssVar(lb.color || "--ink-2");
      ctx.textAlign = lb.align;
      ctx.textBaseline = lb.baseline;
      const x = Math.min(Math.max(lb.x, l + 2), this.w - 2);
      ctx.fillText(lb.text, x, lb.y);
    }
    if (this.hidden) {
      ctx.fillStyle = cssVar("--ink-2");
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.font = `${15 * s}px system-ui, sans-serif`;
      const msg = this.onGuess ? "Response hidden — click to mark where you predict the peak, then Reveal (R)" : "Response hidden — Reveal (R)";
      const mx = l + (this.w - l - r) / 2, my = t + (this.h - t - b) * 0.55;
      const mw = Math.min(ctx.measureText(msg).width, this.w - l - r - 10) + 24 * s;
      ctx.fillStyle = cssVar("--surface");
      ctx.globalAlpha = 0.92;
      ctx.fillRect(mx - mw / 2, my - 16 * s, mw, 32 * s);
      ctx.globalAlpha = 1;
      ctx.fillStyle = cssVar("--ink-2");
      ctx.fillText(msg, mx, my, this.w - l - r - 10);
    }
  }

  #drawLayer(ctx, L, s, labels) {
    const color = cssVar(L.color || "--ink");
    ctx.globalAlpha = L.alpha ?? 1;
    ctx.setLineDash((L.dash || []).map((d) => d * s));
    ctx.lineWidth = (L.width ?? 2) * s;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    const { l, r, t, b } = this.pad;
    switch (L.type) {
      case "line": {
        ctx.beginPath();
        const n = L.x.length;
        const stride = Math.max(1, Math.floor(n / (this.w * 2)));
        for (let k = 0; k < n; k += stride) {
          const [px, py] = this.toPx(L.x[k], L.y[k]);
          const cy = Math.max(-1e4, Math.min(1e4, py));
          if (k === 0) ctx.moveTo(px, cy); else ctx.lineTo(px, cy);
        }
        const [px, py] = this.toPx(L.x[n - 1], L.y[n - 1]);
        ctx.lineTo(px, Math.max(-1e4, Math.min(1e4, py)));
        ctx.lineJoin = "round";
        ctx.stroke();
        break;
      }
      case "hline": {
        const [, py] = this.toPx(0, L.y);
        ctx.lineWidth = (L.width ?? 1.25) * s;
        line(ctx, l, py, this.w - r, py);
        if (L.label) {
          const left = L.labelAlign === "left";
          labels.push({ text: L.label, x: left ? l + 4 : this.w - r - 4, y: py - 3, align: left ? "left" : "right", baseline: "bottom", color: L.textColor });
        }
        break;
      }
      case "vline": {
        const [px] = this.toPx(L.x, 0);
        ctx.lineWidth = (L.width ?? 1.25) * s;
        line(ctx, px, t, px, this.h - b);
        if (L.label) labels.push({ text: L.label, x: px + 4, y: t + 2 + (L.row ?? 0) * 16 * s, align: "left", baseline: "top", color: L.textColor });
        break;
      }
      case "hband": {
        const [, p0] = this.toPx(0, L.y0), [, p1] = this.toPx(0, L.y1);
        ctx.fillStyle = cssVar(L.fill || "--band");
        ctx.fillRect(l, Math.min(p0, p1), this.w - l - r, Math.abs(p1 - p0));
        break;
      }
      case "vspan": {
        const [p0] = this.toPx(L.x0, 0), [p1] = this.toPx(L.x1, 0);
        ctx.fillStyle = cssVar(L.fill || "--band");
        ctx.fillRect(Math.min(p0, p1), t, Math.abs(p1 - p0), this.h - t - b);
        break;
      }
      case "segment": {
        const [x0, y0] = this.toPx(L.x0, L.y0), [x1, y1] = this.toPx(L.x1, L.y1);
        ctx.lineWidth = (L.width ?? 1.5) * s;
        line(ctx, x0, y0, x1, y1);
        if (L.arrows) {
          ctx.setLineDash([]);
          arrowHead(ctx, x1, y1, x0, y0, 6 * s);
          arrowHead(ctx, x0, y0, x1, y1, 6 * s);
        }
        if (L.label) labels.push({ text: L.label, x: (x0 + x1) / 2, y: Math.min(y0, y1) - 4 * s, align: "center", baseline: "bottom", color: L.textColor });
        break;
      }
      case "marker": {
        const [px, py] = this.toPx(L.x, L.y);
        ctx.setLineDash([]);
        drawMarker(ctx, L.shape || "circle", px, py, (L.size ?? 5) * s, color, cssVar("--surface"));
        if (L.label) {
          const dir = L.labelDir || "ne";
          const dx = dir.includes("w") ? -8 * s : 8 * s;
          const dy = dir.includes("s") ? 8 * s : -8 * s;
          labels.push({ text: L.label, x: px + dx, y: py + dy, align: dx < 0 ? "right" : "left", baseline: dy < 0 ? "bottom" : "top", color: L.textColor });
        }
        break;
      }
      case "text": {
        const [px, py] = this.toPx(L.x, L.y);
        labels.push({ text: L.text, x: px, y: py, align: L.align || "left", baseline: L.baseline || "bottom", color: L.textColor || "--ink-2" });
        break;
      }
    }
    ctx.globalAlpha = 1;
    ctx.setLineDash([]);
  }
}

function line(ctx, x0, y0, x1, y1) {
  ctx.beginPath();
  ctx.moveTo(x0, y0);
  ctx.lineTo(x1, y1);
  ctx.stroke();
}

function arrowHead(ctx, xFrom, yFrom, xTo, yTo, size) {
  const a = Math.atan2(yTo - yFrom, xTo - xFrom);
  ctx.beginPath();
  ctx.moveTo(xTo, yTo);
  ctx.lineTo(xTo - size * Math.cos(a - 0.45), yTo - size * Math.sin(a - 0.45));
  ctx.lineTo(xTo - size * Math.cos(a + 0.45), yTo - size * Math.sin(a + 0.45));
  ctx.closePath();
  ctx.fill();
}

export function drawMarker(ctx, shape, x, y, r, color, ring) {
  ctx.save();
  ctx.lineWidth = Math.max(2, r * 0.45);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  switch (shape) {
    case "x":
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(x - r, y - r); ctx.lineTo(x + r, y + r);
      ctx.moveTo(x - r, y + r); ctx.lineTo(x + r, y - r);
      ctx.stroke();
      break;
    case "o":
      ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI); ctx.stroke();
      break;
    case "diamond":
      ctx.beginPath();
      ctx.moveTo(x, y - r); ctx.lineTo(x + r, y); ctx.lineTo(x, y + r); ctx.lineTo(x - r, y); ctx.closePath();
      ctx.lineWidth = 2; ctx.strokeStyle = ring; ctx.fill(); ctx.stroke();
      break;
    case "star": {
      ctx.beginPath();
      for (let i = 0; i < 10; i++) {
        const rr = i % 2 ? r * 0.45 : r;
        const a = -Math.PI / 2 + (i * Math.PI) / 5;
        ctx.lineTo(x + rr * Math.cos(a), y + rr * Math.sin(a));
      }
      ctx.closePath();
      ctx.lineWidth = 1.5; ctx.strokeStyle = ring; ctx.fill(); ctx.stroke();
      break;
    }
    default:
      ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
      ctx.lineWidth = 2; ctx.strokeStyle = ring; ctx.fill(); ctx.stroke();
  }
  ctx.restore();
}

export function interp(xs, ys, x) {
  const n = xs.length;
  if (!n || x < xs[0] || x > xs[n - 1]) return null;
  let lo = 0, hi = n - 1;
  while (hi - lo > 1) {
    const mid = (lo + hi) >> 1;
    if (xs[mid] <= x) lo = mid; else hi = mid;
  }
  const f = xs[hi] === xs[lo] ? 0 : (x - xs[lo]) / (xs[hi] - xs[lo]);
  return ys[lo] + f * (ys[hi] - ys[lo]);
}

export function fmtNum(v, digits = 3) {
  if (v === null || v === undefined || !isFinite(v)) return "—";
  if (v !== 0 && (Math.abs(v) >= 1e4 || Math.abs(v) < 1e-3)) return v.toExponential(2);
  return Number(v.toPrecision(digits)).toString();
}
