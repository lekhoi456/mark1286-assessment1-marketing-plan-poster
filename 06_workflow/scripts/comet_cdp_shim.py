#!/usr/bin/env python3
"""HTTP discovery shim for Comet's remote-debugging session.

When remote debugging is enabled from chrome://inspect/#remote-debugging, Comet
(Chromium) exposes only a WebSocket endpoint, written to `DevToolsActivePort` in its
profile folder; its HTTP discovery endpoints (/json/version) return 404. CDP clients
that need an HTTP endpoint (e.g. Puppeteer's browserURL) can point at this shim: it
answers /json/version with Comet's WebSocket URL, and the client then connects to
Comet directly. Comet asks the student to "Allow remote debugging?" on each new
connection.

Usage (from the workspace root):
  python3 -B 06_workflow/scripts/comet_cdp_shim.py [--port 9333]
Then attach with cdp_url http://127.0.0.1:9333
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ACTIVE_PORT_FILE = Path.home() / "Library/Application Support/Comet/DevToolsActivePort"


def websocket_url() -> str:
    port, path = ACTIVE_PORT_FILE.read_text(encoding="utf-8").split()[:2]
    return f"ws://127.0.0.1:{port}{path}"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (http.server naming)
        route = self.path.split("?")[0].rstrip("/")
        if route == "/json/version":
            try:
                body: object = {"Browser": "Comet", "Protocol-Version": "1.3", "webSocketDebuggerUrl": websocket_url()}
            except (OSError, ValueError):
                self.send_error(503, "Comet remote debugging is not enabled (DevToolsActivePort missing)")
                return
        elif route in ("/json", "/json/list"):
            body = []
        else:
            self.send_error(404)
            return
        data = json.dumps(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=9333)
    args = parser.parse_args()
    print(f"Comet CDP shim on http://127.0.0.1:{args.port} -> {websocket_url()}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
