// Page controller: state, sliders, presets, readouts and URL state.
//
// One plain `state` object holds everything the student can change. Every UI
// event edits it and calls schedule(); the scheduled recompute() rebuilds the
// closed loop, locus, simulation and metrics, then redraws both canvases.

import { DEFAULT_FILTER_N, LOCUS_SAMPLES, closedLoop, locusKind, sampleLocus, ultimateGain, unitDcGain, znGains } from './loop.js';
import { runLoop } from './sim.js';
import { PRESETS, clonePreset, presetById } from './presets.js';
import { SPlane } from './splane.js';
import { TimePlot } from './timeplot.js';

// --- Constants ---------------------------------------------------------------
const DEFAULT_PRESET = 'triple-lag';
const GAINS = {
  kP: { label: 'k_P', max: 50 },
  kI: { label: 'k_I', max: 50 },
  kD: { label: 'k_D', max: 200 },
};
const SLIDER_STEPS = 1000;     // slider positions 0..1000
const LINEAR_STEPS = 100;      // first 10% of travel is linear from 0 to LINEAR_TOP
const LINEAR_TOP = 0.01;       // gain at the end of the linear region
const NUMBER_MAX = 1e4;
const LOCUS_SAMPLES_DRAG = 60; // coarser locus while something is being dragged
const HASH_DEBOUNCE_MS = 200;
const MODIFIED_TOL = 1e-9;     // plant markers closer than this (relative) to the preset count as unmodified
const GAIN_DISPLAY_DIGITS = 5; // gain fields show this many digits; state keeps full precision
const URL_DIGITS = 10;         // enough to round-trip through the URL hash
const DARK_MDBOOK_THEMES = ['coal', 'navy', 'ayu'];
const LIGHT_MDBOOK_THEMES = ['light', 'rust'];

const $ = (id) => document.getElementById(id);
const el = { plane: $('plane'), time: $('time'), preset: $('preset'), status: $('status') };

// --- State -------------------------------------------------------------------
const state = {
  presetId: DEFAULT_PRESET, plant: null, gains: null,
  filter: false, N: DEFAULT_FILTER_N, input: 'ref', active: 'kP', horizon: null,
};
let model = { error: 'Loading...' };
let note = null; // transient status message {text, warn}
let pendingPhase = null;
let fitPending = false; // fit the s-plane after the next recompute, so it sees the new poles

function loadPreset(id) {
  const p = clonePreset(presetById(id) ?? presetById(DEFAULT_PRESET));
  Object.assign(state, {
    presetId: p.id, plant: p.plant, gains: { ...p.gains }, filter: p.filter, N: p.N,
    input: p.input, active: p.active, horizon: null,
  });
  note = null;
}

// --- Slider mapping: linear near zero, logarithmic above ----------------------
function positionToGain(name, pos) {
  const max = GAINS[name].max;
  if (pos <= LINEAR_STEPS) return (pos / LINEAR_STEPS) * LINEAR_TOP;
  const frac = (pos - LINEAR_STEPS) / (SLIDER_STEPS - LINEAR_STEPS);
  return LINEAR_TOP * Math.pow(max / LINEAR_TOP, frac);
}

function gainToPosition(name, g) {
  const max = GAINS[name].max;
  if (g <= LINEAR_TOP) return Math.round((g / LINEAR_TOP) * LINEAR_STEPS);
  const frac = Math.log(g / LINEAR_TOP) / Math.log(max / LINEAR_TOP);
  return Math.min(SLIDER_STEPS, Math.round(LINEAR_STEPS + frac * (SLIDER_STEPS - LINEAR_STEPS)));
}

const roundGain = (g, digits = 3) => Number(g.toPrecision(digits));

// --- Controls ----------------------------------------------------------------
const rows = {};

function buildSliders() {
  for (const [name, spec] of Object.entries(GAINS)) {
    const row = document.createElement('div');
    row.className = 'gain';
    row.innerHTML = `<label for="r-${name}">${spec.label}</label>
      <input type="range" id="r-${name}" min="0" max="${SLIDER_STEPS}" step="1" aria-label="${spec.label}">
      <input type="number" id="n-${name}" min="0" max="${NUMBER_MAX}" step="any" aria-label="${spec.label} value">`;
    $('sliders').append(row);
    const range = row.querySelector('input[type=range]');
    const number = row.querySelector('input[type=number]');
    rows[name] = { row, range, number };

    row.addEventListener('pointerdown', () => setActive(name));
    row.addEventListener('focusin', () => setActive(name));
    range.addEventListener('input', () => setGain(name, roundGain(positionToGain(name, Number(range.value))), 'drag', 'range'));
    range.addEventListener('change', () => schedule('release'));
    number.addEventListener('input', () => {
      const v = number.valueAsNumber;
      if (Number.isFinite(v)) setGain(name, Math.min(Math.max(v, 0), NUMBER_MAX), 'release', 'number');
    });
  }
}

function setGain(name, value, phase, source) {
  state.gains[name] = value;
  note = null;
  syncGains(source === 'range' ? name : null, source === 'number' ? name : null);
  schedule(phase);
}

function setActive(name) {
  if (state.active === name) return;
  state.active = name;
  syncActive();
  schedule('release');
}

/** Push state to the gain widgets, skipping the one the user is currently typing in or dragging. */
function syncGains(skipRange = null, skipNumber = null) {
  for (const name of Object.keys(GAINS)) {
    const g = state.gains[name];
    if (name !== skipRange) rows[name].range.value = gainToPosition(name, g);
    if (name !== skipNumber) rows[name].number.value = String(roundGain(g, GAIN_DISPLAY_DIGITS));
  }
}

function syncActive() {
  for (const [name, r] of Object.entries(rows)) r.row.classList.toggle('active', name === state.active);
  $('locusName').textContent = GAINS[state.active].label;
  $('locusWord').textContent = locusKind({ filter: state.filter }, state.active) === 'path' ? 'pole path' : 'locus';
}

function syncControls() {
  syncGains();
  syncActive();
  $('filter').checked = state.filter;
  $('filterN').value = String(state.N);
  $('plantK').value = String(roundGain(state.plant.K, 6));
  $('horizon').value = state.horizon ? String(state.horizon) : '';
  $('preset').value = state.presetId;
  document.querySelector(`input[name=input][value=${state.input}]`).checked = true;
  renderCaption();
}

const close = (a, b) => Math.abs(a - b) <= MODIFIED_TOL * Math.max(1, Math.abs(b));

function plantModified() {
  const base = presetById(state.presetId)?.plant;
  if (!base || !close(state.plant.K, base.K)) return true;
  return ['poles', 'zeros'].some((list) => state.plant[list].length !== base[list].length
    || state.plant[list].some((m, i) => !close(m.re, base[list][i].re) || !close(m.im, base[list][i].im)));
}

function renderCaption() {
  const text = presetById(state.presetId)?.caption ?? '';
  $('caption').textContent = plantModified() ? `${text} (modified)` : text;
}

function buildPresetMenu() {
  for (const p of PRESETS) el.preset.add(new Option(p.name, p.id));
  el.preset.addEventListener('change', () => {
    loadPreset(el.preset.value);
    syncControls();
    requestFit();
  });
}

function wireToolbar() {
  $('reset').addEventListener('click', () => { loadPreset(state.presetId); syncControls(); requestFit(); });
  $('zn').addEventListener('click', applyZieglerNichols);
  for (const radio of document.querySelectorAll('input[name=input]')) {
    radio.addEventListener('change', () => { state.input = radio.value; note = null; schedule('release'); });
  }
  $('filter').addEventListener('change', () => { state.filter = $('filter').checked; note = null; syncActive(); schedule('release'); });
  $('filterN').addEventListener('input', () => {
    const v = $('filterN').valueAsNumber;
    if (v > 0) { state.N = v; schedule('release'); }
  });
  $('plantK').addEventListener('input', () => {
    const v = $('plantK').valueAsNumber;
    if (Number.isFinite(v)) { state.plant.K = v; schedule('release'); }
  });
  $('unitK').addEventListener('click', () => {
    const k = unitDcGain(state.plant);
    if (k === null) { note = { text: 'G(0) is undefined or zero (a pole or zero at the origin), so K cannot normalise it.', warn: true }; render(); return; }
    state.plant.K = k;
    syncControls();
    schedule('release');
  });
  $('horizon').addEventListener('input', () => {
    const v = $('horizon').valueAsNumber;
    state.horizon = v > 0 ? v : null;
    schedule('release');
  });
  $('addPole').addEventListener('click', () => toggleAdd('poles'));
  $('addZero').addEventListener('click', () => toggleAdd('zeros'));
  $('delete').addEventListener('click', () => plane.deleteSelected());
  $('fit').addEventListener('click', () => plane.fit());
}

function toggleAdd(list) {
  plane.setAddMode(plane.addMode === list ? null : list);
  syncAddButtons();
}

function syncAddButtons() {
  $('addPole').setAttribute('aria-pressed', String(plane.addMode === 'poles'));
  $('addZero').setAttribute('aria-pressed', String(plane.addMode === 'zeros'));
}

function applyZieglerNichols() {
  const result = ultimateGain(state.plant, GAINS.kP.max);
  if (!result.found) {
    note = { text: `No Ziegler-Nichols tuning: ${result.reason}`, warn: true };
  } else {
    const z = znGains(result.Ku, result.Pu);
    state.gains = { kP: z.kP, kI: z.kI, kD: z.kD }; // full precision: rounding would split the double zero
    state.active = 'kP';
    note = {
      text: `K_u = ${roundGain(result.Ku, 5)}, P_u = ${roundGain(result.Pu, 4)} s  ->  k_P = ${roundGain(z.kP, 4)}, `
        + `T_I = ${roundGain(z.TI, 4)} s, T_D = ${roundGain(z.TD, 4)} s (k_I = ${roundGain(z.kI, 4)}, k_D = ${roundGain(z.kD, 4)}).`,
      warn: false,
    };
  }
  syncControls();
  requestFit();
}

// --- Compute and render --------------------------------------------------------
function requestFit() {
  fitPending = true;
  schedule('release');
}

function schedule(phase) {
  if (pendingPhase === null) requestAnimationFrame(() => { const p = pendingPhase; pendingPhase = null; recompute(p); });
  pendingPhase = pendingPhase === 'release' ? 'release' : phase;
}

function recompute(phase) {
  try {
    const options = { filter: state.filter, N: state.N };
    const cl = closedLoop(state.plant, state.gains, options);
    if (!cl.ok) {
      model = { error: cl.error };
    } else {
      const samples = phase === 'drag' ? LOCUS_SAMPLES_DRAG : LOCUS_SAMPLES;
      const locus = sampleLocus(state.plant, state.gains, options, state.active, samples);
      const { trace, metrics } = runLoop(cl, state.input, state.horizon);
      model = { cl, locus, trace, metrics, stability: cl.stability, input: state.input };
    }
  } catch (err) {
    model = { error: `Internal error: ${err.message}` };
  }
  render();
  if (fitPending) { fitPending = false; plane.fit(); }
  if (phase === 'release') scheduleHashWrite();
}

function render() {
  plane.setModel(model.cl ? { cl: model.cl, locus: model.locus } : null);
  time.setModel(model);
  renderMetrics();
  renderReadout();
  renderStatus();
  renderCaption();
  syncAddButtons();
}

const fmt = (x) => String(Number(x.toPrecision(4)));

function renderMetrics() {
  const m = model.metrics;
  const ref = state.input === 'ref';
  const tiles = [
    ['t_r (s)', m?.tr], ['M_p (%)', m?.Mp], ['t_s (s)', m?.ts],
    [ref ? 'e_ss' : 'y(inf)', ref ? m?.ess : m?.yInf], ['max |u|', m?.umax],
  ];
  $('metrics').innerHTML = tiles
    .map(([k, v]) => `<div class="tile"><div class="k">${k}</div><div class="v">${v === null || v === undefined ? '&ndash;' : fmt(v)}</div></div>`)
    .join('');
}

/** "2.5 s^2 + s - 3" for descending coefficients; coefficients negligible next to the largest are omitted. */
function polyString(coeffs, v = 's') {
  const top = Math.max(0, ...coeffs.map(Math.abs));
  const terms = [];
  coeffs.forEach((c, i) => {
    if (Math.abs(c) <= 1e-12 * top) return;
    const p = coeffs.length - 1 - i;
    const mag = Math.abs(c);
    const body = p === 0 ? fmt(mag) : `${mag === 1 ? '' : `${fmt(mag)} `}${v}${p > 1 ? `^${p}` : ''}`;
    terms.push({ neg: c < 0, body });
  });
  if (!terms.length) return '0';
  return terms.map((t, i) => (i === 0 ? (t.neg ? '-' : '') : (t.neg ? ' - ' : ' + ')) + t.body).join('');
}

const VECTOR_DIGITS = 10; // enough that pasted coefficients keep ZN's double zero and K = 1/600
const vector = (c) => `[${c.map((x) => Number(x.toPrecision(VECTOR_DIGITS))).join(' ')}]`;

function poleList(poles) {
  const parts = [];
  for (const p of poles) {
    if (p.im < 0) continue;
    parts.push(p.im === 0 ? fmt(p.re) : `${fmt(p.re)} +/- ${fmt(p.im)}j`);
  }
  return parts.join(',  ') || '(none)';
}

function renderReadout() {
  if (!model.cl) { $('readout').textContent = model.error ?? ''; return; }
  const { cl } = model;
  const g = state.gains;
  $('tf').textContent = cl.parts.filtered ? `T_f = k_D/(N k_P) = ${fmt(cl.parts.Tf)} s` : '';
  const cNum = cl.Nc.length ? cl.Nc : [0];
  $('readout').textContent = [
    `G(s)  = ( ${polyString(cl.plant.num)} ) / ( ${polyString(cl.plant.den)} )`,
    `Dc(s) = ( ${polyString(cNum)} ) / ( ${polyString(cl.parts.den)} )     [k_P = ${fmt(g.kP)}, k_I = ${fmt(g.kI)}, k_D = ${fmt(g.kD)}]`,
    `a(s)  = ${polyString(cl.a)}     (closed-loop characteristic polynomial)`,
    `closed-loop poles: ${poleList(cl.poles)}`,
    `controller zeros:  ${poleList(cl.ctrlZeros)}`,
    `MATLAB: G = tf(${vector(cl.plant.num)}, ${vector(cl.plant.den)}); Dc = tf(${vector(cNum)}, ${vector(cl.parts.den)});`,
  ].join('\n');
}

function renderStatus() {
  const msgs = [];
  let warn = false;
  if (model.error) { msgs.push(model.error); warn = true; }
  if (note) { msgs.push(note.text); warn = warn || note.warn; }
  if (model.cl) {
    const g = state.gains;
    if (state.filter && g.kP <= 0 && g.kD > 0) {
      msgs.push('The derivative filter needs k_P > 0 (T_f = k_D/(N k_P)); showing the ideal derivative.');
    }
    if (model.stability === 'unstable') { msgs.push('The closed loop is unstable: metrics are blank and the y axis is clipped.'); warn = true; }
    if (model.stability === 'marginal') msgs.push('The closed loop is marginally stable (a pole on the imaginary axis): metrics are blank.');
    if (model.trace.impulseY) msgs.push(`The response ${state.input === 'dist' ? 'Y/W' : 'Y/R'} is improper here (a(s) lost degree), so it has an impulse that is not drawn; metrics are blank.`);
    if (!model.trace.valid) { msgs.push('The simulation produced non-finite values; metrics are blank.'); warn = true; }
    if (model.trace.impulseU) {
      msgs.push('An ideal derivative acting on a reference step puts an impulse in u. It is not drawn and max|u| is blank; turn on the filter to see it as a finite spike.');
    }
  }
  el.status.textContent = msgs.join(' ');
  el.status.classList.toggle('warn', warn);
}

// --- URL state ----------------------------------------------------------------
const encodeNumber = (x) => String(Number(x.toPrecision(URL_DIGITS)));

function encodeMarkers(list) {
  return list.map((m) => `${encodeNumber(m.re)}${m.im ? `:${encodeNumber(m.im)}` : ''}${m.fixed ? '!' : ''}`).join(',');
}

function decodeMarkers(text) {
  return text.split(',').filter((tok) => tok !== '').map((tok) => {
    const fixed = tok.endsWith('!');
    const [re, im = 0] = tok.replace('!', '').split(':').map(Number);
    if (!Number.isFinite(re) || !Number.isFinite(im)) throw new Error(`bad marker "${tok}"`);
    return fixed ? { re, im: Math.abs(im), fixed: true } : { re, im: Math.abs(im) };
  });
}

function readParams() {
  const merged = new URLSearchParams(location.search);
  for (const [k, v] of new URLSearchParams(location.hash.replace(/^#/, ''))) merged.set(k, v);
  return merged;
}

/** Load the preset named in the URL, then apply any explicit overrides. */
function applyParams(params) {
  loadPreset(params.get('preset') ?? DEFAULT_PRESET);
  const number = (key) => (params.has(key) && Number.isFinite(Number(params.get(key))) ? Number(params.get(key)) : null);
  for (const name of Object.keys(GAINS)) if (number(name) !== null) state.gains[name] = Math.max(0, number(name));
  if (number('K') !== null) state.plant.K = number('K');
  if (params.has('poles')) state.plant.poles = decodeMarkers(params.get('poles'));
  if (params.has('zeros')) state.plant.zeros = decodeMarkers(params.get('zeros'));
  if (params.has('filter')) state.filter = params.get('filter') === '1';
  if (number('N') > 0) state.N = number('N');
  if (['ref', 'dist'].includes(params.get('input'))) state.input = params.get('input');
  if (params.get('active') in GAINS) state.active = params.get('active');
  if (number('T') > 0) state.horizon = number('T');
}

/** Remove one query-string parameter (leaving the hash alone) so it does not re-run on reload. */
function dropQueryParam(name) {
  const url = new URL(location.href);
  url.searchParams.delete(name);
  try { history.replaceState(null, '', url); } catch { /* sandboxed frame: skip */ }
}

let hashTimer = null;
function scheduleHashWrite() {
  clearTimeout(hashTimer);
  hashTimer = setTimeout(() => {
    const p = new URLSearchParams();
    p.set('preset', state.presetId);
    for (const name of Object.keys(GAINS)) p.set(name, encodeNumber(state.gains[name]));
    p.set('filter', state.filter ? '1' : '0');
    p.set('N', String(state.N));
    p.set('input', state.input);
    p.set('active', state.active);
    p.set('K', encodeNumber(state.plant.K));
    p.set('poles', encodeMarkers(state.plant.poles));
    p.set('zeros', encodeMarkers(state.plant.zeros));
    if (state.horizon) p.set('T', String(state.horizon));
    const theme = readParams().get('theme');
    if (theme) p.set('theme', theme);
    try { history.replaceState(null, '', `#${p.toString()}`); } catch { /* sandboxed frame: skip */ }
  }, HASH_DEBOUNCE_MS);
}

// --- Theme --------------------------------------------------------------------

/** ?theme=dark|light wins; then the surrounding mdBook theme (same-origin parent); then the OS. */
function detectTheme() {
  const forced = readParams().get('theme');
  if (forced === 'dark' || forced === 'light') return forced;
  try {
    const classes = window.parent !== window ? window.parent.document.documentElement.classList : null;
    if (classes) {
      if (DARK_MDBOOK_THEMES.some((t) => classes.contains(t))) return 'dark';
      if (LIGHT_MDBOOK_THEMES.some((t) => classes.contains(t))) return 'light';
    }
  } catch { /* cross-origin parent: fall through */ }
  return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme() {
  document.documentElement.dataset.theme = detectTheme();
  plane.draw();
  time.draw();
}

function watchTheme() {
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
  try {
    if (window.parent !== window) {
      new MutationObserver(applyTheme).observe(window.parent.document.documentElement, { attributes: true, attributeFilter: ['class'] });
    }
  } catch { /* cross-origin parent */ }
}

// --- Embedding ------------------------------------------------------------------
let lastHeight = 0;

/** Tell a same-origin parent page how tall the content is, so it can size the iframe. */
function postHeight() {
  const height = document.body.offsetHeight;
  if (window.parent === window || height === lastHeight) return;
  lastHeight = height;
  window.parent.postMessage({ type: 'pid-explorer-height', height }, '*');
}

// --- Start up -----------------------------------------------------------------
const plane = new SPlane(el.plane, {
  state,
  changed(phase) { note = null; schedule(phase); },
});
const time = new TimePlot(el.time);

function start() {
  buildPresetMenu();
  buildSliders();
  wireToolbar();
  try { applyParams(readParams()); } catch (err) { loadPreset(DEFAULT_PRESET); note = { text: `Ignoring the URL state: ${err.message}`, warn: true }; }
  syncControls();
  applyTheme();
  watchTheme();
  fitPending = true;
  recompute('release');
  if (readParams().get('zn') === '1') { dropQueryParam('zn'); applyZieglerNichols(); }
  new ResizeObserver(() => { plane.draw(); time.draw(); postHeight(); }).observe(document.body);
  window.addEventListener('hashchange', () => {
    try { applyParams(readParams()); syncControls(); requestFit(); } catch { /* keep current state */ }
  });
}

start();
