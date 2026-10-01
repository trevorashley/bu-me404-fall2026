#!/usr/bin/env python3
"""Serve the time-domain specifications explorer on localhost.

Usage (from anywhere in the repository):

    python3 apps/time-domain-specs/serve.py        # macOS / Linux
    py apps\\time-domain-specs\\serve.py            # Windows

Only the Python standard library is used. The page opens in your default
browser; press Ctrl-C in this terminal to stop the server.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import pathlib
import socketserver
import sys
import threading
import webbrowser

STATIC = pathlib.Path(__file__).resolve().parent / "static"
DEFAULT_PORT = 8404


class Handler(http.server.SimpleHTTPRequestHandler):
    # Make sure ES modules are served with a JavaScript MIME type on every platform
    # (some Windows registries map .js to text/plain).
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".css": "text/css",
        ".html": "text/html",
        ".svg": "image/svg+xml",
    }

    def end_headers(self) -> None:
        # Always serve the latest files: students may pull updates mid-lecture.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        pass  # keep the terminal quiet


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = False
    daemon_threads = True


def bind(port: int, tries: int = 20) -> Server:
    handler = functools.partial(Handler, directory=str(STATIC))
    for p in range(port, port + tries):
        try:
            return Server(("127.0.0.1", p), handler)
        except OSError:
            continue
    sys.exit(f"No free port found in {port}-{port + tries - 1}.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"first port to try (default {DEFAULT_PORT})")
    parser.add_argument("--no-browser", action="store_true", help="do not open a browser window")
    args = parser.parse_args()

    server = bind(args.port)
    url = f"http://localhost:{server.server_address[1]}/"
    print(f"Time-domain specifications explorer running at {url}")
    print("Press Ctrl-C to stop.")
    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
