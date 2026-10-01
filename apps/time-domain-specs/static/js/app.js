// Tab router and cross-cutting features: predict-then-reveal, theme, UI scale,
// keyboard shortcuts and shareable URL state.

import { el, toast } from "./ui.js";

const TABS = [
  { id: "specs", title: "Specifications", module: "./tabs/specs.js" },
  { id: "region", title: "Design region", module: "./tabs/region.js" },
  { id: "alpha", title: "Zeros & extra poles", module: "./tabs/alpha.js" },
  { id: "sandbox", title: "Sandbox", module: "./tabs/sandbox.js" },
];

const store = {
  get(k, d) { try { return localStorage.getItem(k) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};

const app = {
  tabs: {},
  active: null,
  predictOn: false,
  hidden: false,
  plots: new Set(),

  isHidden() { return this.hidden; },

  // Response plots that participate in predict-then-reveal.
  registerPlot(plot) {
    this.plots.add(plot);
    plot.onGuess = () => {};
    plot.setHidden(this.hidden);
  },

  // Called by tabs after any user change.
  edited() {
    if (this.predictOn && !this.hidden) this._setHidden(true, true);
    this.save();
  },

  _setHidden(h, clearGuesses = false) {
    this.hidden = h;
    document.body.classList.toggle("predict-hidden", h);
    for (const p of this.plots) {
      if (clearGuesses) p.guess = null;
      p.setHidden(h);
    }
  },

  setPredict(on) {
    this.predictOn = on;
    document.body.classList.toggle("predict-on", on);
    document.getElementById("predict").setAttribute("aria-pressed", String(on));
    document.getElementById("reveal").hidden = !on;
    this._setHidden(on, true);
  },

  reveal() {
    if (this.predictOn) this._setHidden(!this.hidden);
  },

  save() {
    clearTimeout(this._saveT);
    this._saveT = setTimeout(() => {
      const tab = this.tabs[this.active];
      if (!tab?.getState) return;
      const s = encodeURIComponent(JSON.stringify(tab.getState()));
      history.replaceState(null, "", `#${this.active}=${s}`);
    }, 250);
  },

  async select(id, state = null) {
    if (!TABS.some((t) => t.id === id)) id = "specs";
    this.active = id;
    document.querySelectorAll("nav.tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.id === id)));
    document.querySelectorAll(".tab-panel").forEach((p) => (p.hidden = p.dataset.id !== id));
    const tab = await this.load(id);
    if (state && tab?.setState) tab.setState(state);
    tab?.activate?.();
    this.save();
  },

  async load(id) {
    if (this.tabs[id]) return this.tabs[id];
    const def = TABS.find((t) => t.id === id);
    const panel = document.querySelector(`.tab-panel[data-id="${id}"]`);
    try {
      const mod = await import(def.module);
      this.tabs[id] = mod.create(panel, this);
    } catch (err) {
      console.error(err);
      panel.append(el(`<p class="warn-text">This tab failed to load: ${err.message}</p>`));
      this.tabs[id] = null;
    }
    return this.tabs[id];
  },
};

function applyScale(s) {
  s = Math.max(0.75, Math.min(1.8, s));
  document.documentElement.style.setProperty("--ui-scale", String(s));
  store.set("tds-scale", String(s));
  window.dispatchEvent(new Event("resize"));
  for (const t of Object.values(app.tabs)) t?.redraw?.();
}

function applyTheme(mode) {
  if (mode === "auto") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", mode);
  document.getElementById("theme").textContent = `Theme: ${mode}`;
  store.set("tds-theme", mode);
  for (const t of Object.values(app.tabs)) t?.redraw?.();
}

function init() {
  const nav = document.querySelector("nav.tabs");
  const panels = document.getElementById("panels");
  TABS.forEach((t, i) => {
    const b = el(`<button role="tab" data-id="${t.id}"><kbd>${i + 1}</kbd>${t.title}</button>`);
    b.addEventListener("click", () => app.select(t.id));
    nav.append(b);
    panels.append(el(`<section class="tab-panel" data-id="${t.id}" hidden></section>`));
  });

  // Optional query overrides, e.g. ?theme=dark&scale=1.3&predict=1 (handy for a projector).
  const q = new URLSearchParams(location.search);
  let theme = ["auto", "light", "dark"].includes(q.get("theme")) ? q.get("theme") : store.get("tds-theme", "auto");
  applyTheme(theme);
  document.getElementById("theme").addEventListener("click", () => {
    theme = { auto: "light", light: "dark", dark: "auto" }[theme];
    applyTheme(theme);
  });
  let scale = parseFloat(q.get("scale") ?? store.get("tds-scale", "1")) || 1;
  applyScale(scale);
  document.getElementById("smaller").addEventListener("click", () => applyScale((scale = Math.max(0.75, scale - 0.1))));
  document.getElementById("larger").addEventListener("click", () => applyScale((scale = Math.min(1.8, scale + 0.1))));
  document.getElementById("predict").addEventListener("click", () => app.setPredict(!app.predictOn));
  document.getElementById("reveal").addEventListener("click", () => app.reveal());
  document.getElementById("share").addEventListener("click", async () => {
    app.save();
    await new Promise((r) => setTimeout(r, 300));
    try {
      await navigator.clipboard.writeText(location.href);
      toast("Link copied");
    } catch {
      prompt("Copy this link:", location.href);
    }
  });

  document.addEventListener("keydown", (e) => {
    const tag = e.target.tagName;
    if ((tag === "INPUT" && e.target.type !== "range" && e.target.type !== "checkbox") || tag === "SELECT" || tag === "TEXTAREA") return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const n = parseInt(e.key, 10);
    if (n >= 1 && n <= TABS.length) app.select(TABS[n - 1].id);
    else if (e.key === "r" || e.key === "R") app.reveal();
    else if (e.key === "p" || e.key === "P") app.tabs[app.active]?.pin?.();
    else if (e.key === "+" || e.key === "=") applyScale((scale = Math.min(1.8, scale + 0.1)));
    else if (e.key === "-" || e.key === "_") applyScale((scale = Math.max(0.75, scale - 0.1)));
    else if (e.key === "Delete" || e.key === "Backspace") app.tabs[app.active]?.deleteSelected?.();
    else return;
    e.preventDefault();
  });

  // Restore from the URL: #tab=<json>
  const m = location.hash.match(/^#([a-z]+)(?:=(.*))?$/);
  let state = null;
  if (m?.[2]) {
    try { state = JSON.parse(decodeURIComponent(m[2])); } catch { state = null; }
  }
  app.select(m?.[1] ?? "specs", state).then(() => { if (q.get("predict") === "1") app.setPredict(true); });
}

window.tdsApp = app; // for automated UI checks
init();
