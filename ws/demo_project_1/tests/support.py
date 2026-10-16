"""A real server on an ephemeral port, for HTTP-level tests."""

from __future__ import annotations

import http.client
import json
import os
import tempfile
import threading
from typing import Any

from shorty.http import make_server
from shorty.links import LinkService


class RunningServer:
    def __init__(self, db_path: str | None = None) -> None:
        self._tmp = None
        if db_path is None:
            self._tmp = tempfile.TemporaryDirectory()
            db_path = os.path.join(self._tmp.name, "shorty.db")
        self.db_path = db_path
        self.service = LinkService(db_path)
        self.server = make_server(self.service, "127.0.0.1", 0)
        self.port = self.server.server_address[1]
        self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self._thread.start()

    def request(
        self, method: str, path: str, body: Any = None, raw: bytes | None = None
    ) -> tuple[int, dict[str, str], Any]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
        headers = {"Content-Type": "application/json"} if data is not None else {}
        conn.request(method, path, body=data, headers=headers)
        resp = conn.getresponse()
        text = resp.read().decode()
        conn.close()
        payload = json.loads(text) if text else None
        return resp.status, {k.lower(): v for k, v in resp.getheaders()}, payload

    def stop(self, keep_db: bool = False) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.service.close()
        if self._tmp is not None and not keep_db:
            self._tmp.cleanup()
