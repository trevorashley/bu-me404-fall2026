// Small canvas helpers shared by the s-plane and time-response plots.
// (An addition to the file list in the plan: avoids duplicating tick and
// colour code in splane.js and timeplot.js.)

/** Read the page's colour tokens (CSS custom properties) so canvases follow the theme. */
export function readColors() {
  const style = getComputedStyle(document.documentElement);
  const get = (name) => style.getPropertyValue(name).trim();
  return {
    bg: get('--plot-bg'), fg: get('--fg'), muted: get('--muted'),
    grid: get('--grid'), axis: get('--axis'), rhp: get('--rhp'),
    plant: get('--plant'), ctrl: get('--ctrl'), closed: get('--closed'),
    locus: get('--locus'), y: get('--trace-y'), u: get('--trace-u'),
    band: get('--band'), bad: get('--bad'),
  };
}

/** Match the canvas backing store to its CSS size and device pixel ratio. Returns {ctx, w, h}. */
export function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const w = Math.max(1, Math.round(canvas.clientWidth));
  const h = Math.max(1, Math.round(canvas.clientHeight));
  if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
  }
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, w, h };
}

/** "Nice" tick values (1, 2, 5 x 10^n) covering [lo, hi] with roughly `target` ticks. */
export function niceTicks(lo, hi, target = 6) {
  const span = hi - lo;
  if (!(span > 0)) return [lo];
  const raw = span / target;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 5, 10].map((m) => m * mag).find((s) => s >= raw);
  const ticks = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) {
    ticks.push(Math.abs(v) < step * 1e-9 ? 0 : v);
  }
  return ticks;
}

/** Compact tick label: at most 3 significant digits, no trailing zeros. */
export const tickLabel = (v) => String(Number(v.toPrecision(3)));
