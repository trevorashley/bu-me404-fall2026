// Preset plants from the course notes (plan Section 4). Pure data, no DOM.
//
// plant.poles / plant.zeros hold markers {re, im, fixed?}: im > 0 stands for the
// conjugate pair re +/- j im; `fixed` markers (the Pade approximation) cannot be dragged.

import { DEFAULT_FILTER_N } from './loop.js';

// Second-order Pade approximation of e^{-Ls} with L = 5 s:
//   (1 - Ls/2 + (Ls)^2/12) / (1 + Ls/2 + (Ls)^2/12)
// has zeros at (3 +/- j sqrt 3)/L and poles at (-3 +/- j sqrt 3)/L. Both quadratics
// share the same leading coefficient, so the Pade factor contributes no extra gain.
const DELAY = 5;
const PADE_RE = 3 / DELAY;
const PADE_IM = Math.sqrt(3) / DELAY;

/** Ultimate gain of the Pade heat exchanger, from verify/verify.py (check 4). */
export const PADE_KU = 15.30;

const base = { filter: false, N: DEFAULT_FILTER_N, input: 'ref', active: 'kP' };

export const PRESETS = [
  {
    ...base,
    id: 'second-order',
    name: 'Second-order, no ultimate gain',
    plant: { K: 1, poles: [{ re: -0.7, im: Math.sqrt(1 - 0.49) }], zeros: [] },
    gains: { kP: 1, kI: 0, kD: 0 },
    caption: 'G = 1/(s^2 + 1.4s + 1). P alone cannot destabilise it: k_P moves the natural frequency but the real part stays at -0.7, so there is no K_u.',
  },
  {
    ...base,
    id: 'two-lag',
    name: 'Two-lag thermal system',
    plant: { K: 100, poles: [{ re: -1, im: 0 }, { re: -0.1, im: 0 }], zeros: [] },
    gains: { kP: 0.03, kI: 0.003, kD: 0 },
    active: 'kI',
    caption: 'G = 100/[(s+1)(s+0.1)] (DC gain 1000). With k_P = 0.03, k_I = 0.003 the PI zero cancels the slow pole, as in Example 4.5. Raise k_I and watch the slow tail.',
  },
  {
    ...base,
    id: 'triple-lag',
    name: 'Triple lag',
    plant: { K: 1, poles: [{ re: -1, im: 0 }, { re: -1, im: 0 }, { re: -1, im: 0 }], zeros: [] },
    gains: { kP: 1, kI: 0, kD: 0 },
    caption: 'G = 1/(s+1)^3. K_u = 8 and P_u = 2 pi/sqrt(3) = 3.628 s. Press ZN tune for k_P = 4.8, T_I = 1.814 s, T_D = 0.453 s.',
  },
  {
    ...base,
    id: 'double-integrator',
    name: 'Double integrator',
    plant: { K: 1, poles: [{ re: 0, im: 0 }, { re: 0, im: 0 }], zeros: [] },
    gains: { kP: 1, kI: 0, kD: 1.4 },
    active: 'kD',
    caption: 'G = 1/s^2. P or PI alone leaves poles on the imaginary axis or in the right half-plane; PD supplies the damping. Set k_D = 0 to see it.',
  },
  {
    ...base,
    id: 'heat-exchanger',
    name: 'Heat exchanger (Pade)',
    plant: {
      K: 1 / 600,
      poles: [
        { re: -0.1, im: 0 }, { re: -1 / 60, im: 0 },
        { re: -PADE_RE, im: PADE_IM, fixed: true },
      ],
      zeros: [{ re: PADE_RE, im: PADE_IM, fixed: true }],
    },
    gains: { kP: 7.65, kI: 0, kD: 0 },
    caption: `G = e^{-5s}/[(10s+1)(60s+1)] with a 2nd-order Pade delay (fixed markers; note the right-half-plane zeros). The textbook measures K_u = 15.3; the exact-delay model gives 15.29 and this Pade model gives ${PADE_KU.toFixed(2)}, so the approximation costs almost nothing here.`,
  },
  {
    ...base,
    id: 'blank',
    name: 'Blank',
    plant: { K: 1, poles: [{ re: 0, im: 0 }], zeros: [] },
    gains: { kP: 1, kI: 0, kD: 0 },
    caption: 'G = 1/s with one pole. Drag it, add poles and zeros, and experiment.',
  },
];

export const presetById = (id) => PRESETS.find((p) => p.id === id) ?? null;

/** Deep copy, so the UI can edit a preset's plant without changing the table. */
export const clonePreset = (preset) => JSON.parse(JSON.stringify(preset));
