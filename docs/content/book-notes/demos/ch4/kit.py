"""Shared plumbing for the Chapter 4 demos.

These scripts reuse the helpers written for the first lecture (`../ch2/demokit.py`)
so that the terminal narration, the colour palette and the s-plane drawing all
look the same from one lecture to the next. The only change is where figures
land: `ch4/figures/` rather than `figures/`.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ch2"))

import demokit  # noqa: E402

demokit.FIGDIR = pathlib.Path(__file__).parent / "figures"

from demokit import *  # noqa: E402,F401,F403
