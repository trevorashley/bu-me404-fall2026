"""Shared helpers for the lecture demonstrations.

Everything here exists to keep the individual demos short and readable, so that
what a student sees on screen is the physics, not the plumbing.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import matplotlib
import numpy as np

FIGDIR = pathlib.Path(__file__).parent / "figures"

# Colour-blind-safe palette (Okabe-Ito), used consistently across every demo.
C = {
    "blue":   "#0072B2",
    "orange": "#E69F00",
    "green":  "#009E73",
    "red":    "#D55E00",
    "purple": "#CC79A7",
    "sky":    "#56B4E9",
    "yellow": "#F0E442",
    "grey":   "#666666",
}


def parse_args(description: str) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--show", action="store_true",
                   help="open an interactive window instead of writing files")
    p.add_argument("--no-save", action="store_true",
                   help="skip writing PNG/SVG output")
    return p.parse_args()


def setup(args: argparse.Namespace):
    """Pick a backend and apply lecture-hall-friendly styling."""
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.figsize": (11, 6),
        "figure.dpi": 110,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.labelsize": 13,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "lines.linewidth": 2.2,
        "legend.frameon": False,
    })
    return plt


def finish(plt, fig, stem: str, args: argparse.Namespace) -> None:
    """Show or save a finished figure."""
    if args.show:
        plt.show()
        return
    if args.no_save:
        return
    FIGDIR.mkdir(exist_ok=True)
    for ext in ("png", "svg"):
        path = FIGDIR / f"{stem}.{ext}"
        fig.savefig(path)
    print(f"\n  wrote figures/{stem}.png and figures/{stem}.svg")


# ---------------------------------------------------------------- narration

def title(text: str) -> None:
    print()
    print("=" * 78)
    print(text)
    print("=" * 78)


def section(text: str) -> None:
    print(f"\n--- {text} " + "-" * max(0, 73 - len(text)))


def note(text: str) -> None:
    """Wrap a paragraph of explanation to the terminal width."""
    import textwrap
    print()
    for line in textwrap.wrap(text, width=78):
        print(line)


def fmt_root(z: complex, places: int = 4) -> str:
    """Format a complex root the way it would be written on the board."""
    if abs(z.imag) < 1e-9:
        return f"{z.real:+.{places}f}"
    return f"{z.real:+.{places}f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.{places}f}j"


def table(headers: list[str], rows: list[list[str]], indent: str = "  ") -> None:
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) if rows else len(str(h))
              for i, h in enumerate(headers)]
    line = indent + "  ".join(str(h).rjust(w) for h, w in zip(headers, widths))
    print(line)
    print(indent + "  ".join("-" * w for w in widths))
    for r in rows:
        print(indent + "  ".join(str(c).rjust(w) for c, w in zip(r, widths)))


# ------------------------------------------------------------- s-plane plot

def splane(ax, poles=(), zeros=(), *, xlim=None, ylim=None,
           pole_color=C["blue"], zero_color=C["red"], label_poles=None,
           label_zeros=None, title_text=None):
    """Draw a pole-zero map with the LHP shaded and the axes marked."""
    poles = np.atleast_1d(np.asarray(poles, dtype=complex)) if len(poles) else np.array([])
    zeros = np.atleast_1d(np.asarray(zeros, dtype=complex)) if len(zeros) else np.array([])

    allpts = np.concatenate([poles, zeros]) if len(poles) + len(zeros) else np.array([0j])
    if xlim is None:
        m = max(1.0, float(np.max(np.abs(allpts.real))) * 1.35)
        xlim = (-m, m)
    if ylim is None:
        m = max(1.0, float(np.max(np.abs(allpts.imag))) * 1.35)
        ylim = (-m, m)

    ax.axvspan(xlim[0], 0, color=C["green"], alpha=0.06, zorder=0)
    ax.axhline(0, color="k", lw=1.0, zorder=1)
    ax.axvline(0, color="k", lw=1.6, zorder=1)

    if len(poles):
        ax.plot(poles.real, poles.imag, "x", ms=13, mew=3.0,
                color=pole_color, label=label_poles, zorder=3)
    if len(zeros):
        ax.plot(zeros.real, zeros.imag, "o", ms=12, mfc="none", mew=2.6,
                color=zero_color, label=label_zeros, zorder=3)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(r"$\Re(s)$   [1/s]")
    ax.set_ylabel(r"$\omega = \Im(s)$   [rad/s]")
    if title_text:
        ax.set_title(title_text)
    ax.text(0.02, 0.975, "LHP: decay", transform=ax.transAxes, ha="left",
            va="top", fontsize=10.5, color=C["grey"])
    ax.text(0.98, 0.975, "RHP: growth", transform=ax.transAxes, ha="right",
            va="top", fontsize=10.5, color=C["grey"])
    return ax


def require_venv() -> None:
    """Fail loudly if the demo was launched with the wrong interpreter."""
    try:
        import numpy  # noqa: F401
        import scipy  # noqa: F401
        import matplotlib  # noqa: F401
    except ImportError:  # pragma: no cover
        sys.exit(
            "\nMissing dependencies. Run the demos with the project environment:\n"
            "    uv run python <script>.py\n"
            "or activate it first:\n"
            "    source .venv/bin/activate\n"
        )
