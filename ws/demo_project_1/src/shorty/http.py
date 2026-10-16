"""HTTP API over a LinkService."""

from __future__ import annotations

from http.server import ThreadingHTTPServer

from shorty.links import LinkService


def make_server(
    service: LinkService, host: str, port: int, base_url: str | None = None
) -> ThreadingHTTPServer:
    """Serve POST /links, GET /{code}, GET /links/{code} and GET /healthz."""
    raise NotImplementedError
