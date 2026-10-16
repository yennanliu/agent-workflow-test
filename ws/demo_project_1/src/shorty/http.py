"""HTTP API over a LinkService."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from shorty.links import LinkService


def make_server(
    service: LinkService, host: str, port: int, base_url: str | None = None
) -> ThreadingHTTPServer:
    """Serve POST /links, GET /{code}, GET /links/{code} and GET /healthz."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/healthz":
                return self._json(200, {"status": "ok"})
            link = service.follow(self.path[1:])
            self.send_response(302)
            self.send_header("Location", link.url)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length))
            link, _ = service.shorten(body["url"])
            self._json(201, {"code": link.code, "short_url": f"{root()}/{link.code}", "url": link.url})

        def _json(self, status: int, payload: Any) -> None:
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer((host, port), Handler)

    def root() -> str:
        if base_url:
            return base_url.rstrip("/")
        bound_host, bound_port = server.server_address[:2]
        return f"http://{bound_host}:{bound_port}"

    return server
