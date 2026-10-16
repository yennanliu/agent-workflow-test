"""HTTP API over a LinkService."""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from shorty.links import InvalidURL, Link, LinkNotFound, LinkService

MAX_BODY_BYTES = 8 * 1024
SOCKET_TIMEOUT_SECONDS = 10
CODE_PATH = re.compile(r"^/([0-9A-Za-z]+)$")
STATS_PATH = re.compile(r"^/links/([0-9A-Za-z]+)$")

log = logging.getLogger("shorty")


class BadRequest(Exception):
    pass


class NotFound(Exception):
    pass


def make_server(
    service: LinkService, host: str, port: int, base_url: str | None = None
) -> ThreadingHTTPServer:
    """Serve POST /links, GET /{code}, GET /links/{code} and GET /healthz."""

    class Handler(BaseHTTPRequestHandler):
        timeout = SOCKET_TIMEOUT_SECONDS

        def do_GET(self) -> None:
            self._handle(self._get)

        def do_POST(self) -> None:
            self._handle(self._post)

        def _get(self) -> None:
            path = self.path.split("?", 1)[0]
            if path == "/healthz":
                return self._json(200, {"status": "ok"})
            if match := STATS_PATH.match(path):
                link = service.stats(match.group(1))
                return self._json(200, _stats(link))
            if match := CODE_PATH.match(path):
                link = service.follow(match.group(1))
                self.send_response(302)
                self.send_header("Location", link.url)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            raise NotFound("no such route")

        def _post(self) -> None:
            if self.path.split("?", 1)[0] != "/links":
                raise NotFound("no such route")
            body = self._read_json()
            if not isinstance(body, dict) or "url" not in body:
                raise BadRequest('body must be a JSON object with a "url" field')
            link, created = service.shorten(body["url"])
            self._json(201 if created else 200, {"code": link.code, "short_url": f"{root()}/{link.code}", "url": link.url})

        def _read_json(self) -> Any:
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                raise BadRequest("invalid Content-Length") from None
            if length < 0:
                raise BadRequest("invalid Content-Length")
            if length > MAX_BODY_BYTES:
                raise BadRequest(f"body must be at most {MAX_BODY_BYTES} bytes")
            try:
                return json.loads(self.rfile.read(length) or b"null")
            except (UnicodeDecodeError, json.JSONDecodeError):
                raise BadRequest("body must be valid JSON") from None

        def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
            """JSON for the stdlib's own errors too (bad request line, unsupported method, …)."""
            if self.request_version == "HTTP/0.9":
                self.request_version = "HTTP/1.0"
            self.close_connection = True
            self._json(code, {"error": message or HTTPStatus(code).phrase})

        def _handle(self, route: Callable[[], None]) -> None:
            try:
                route()
            except (BadRequest, InvalidURL) as exc:
                self._json(400, {"error": str(exc)})
            except (NotFound, LinkNotFound):
                self._json(404, {"error": "not found"})
            except Exception:
                log.exception("unhandled error on %s %s", self.command, self.path)
                self._json(500, {"error": "internal error"})

        def _json(self, status: int, payload: Any) -> None:
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: Any) -> None:
            log.info("%s %s", self.address_string(), format % args)

    server = ThreadingHTTPServer((host, port), Handler)

    def root() -> str:
        if base_url:
            return base_url.rstrip("/")
        bound_host, bound_port = server.server_address[:2]
        return f"http://{bound_host}:{bound_port}"

    return server


def _stats(link: Link) -> dict[str, Any]:
    return {"code": link.code, "url": link.url, "created_at": link.created_at, "hits": link.hits}
