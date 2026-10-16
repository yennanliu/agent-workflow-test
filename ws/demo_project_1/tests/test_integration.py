"""Integration tests through the real CLI process and SQLite file."""

from __future__ import annotations

import http.client
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SRC = str(Path(__file__).resolve().parent.parent / "src")


class Process:
    def __init__(self, db: str, *extra: str) -> None:
        env = {**os.environ, "PYTHONPATH": SRC}
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "shorty", "--host", "127.0.0.1", "--port", "0", "--db", db, *extra],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        line = self.proc.stdout.readline()
        if not line.startswith("shorty listening on "):
            self.stop()
            raise AssertionError(f"unexpected startup line: {line!r}; stderr: {self.proc.stderr.read()}")
        self.base_url = line.split("listening on ", 1)[1].strip()
        self.port = int(self.base_url.rsplit(":", 1)[1])

    def request(self, method: str, path: str, body: object = None) -> tuple[int, dict, object]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        data = None if body is None else json.dumps(body).encode()
        conn.request(method, path, body=data, headers={"Content-Type": "application/json"} if data else {})
        resp = conn.getresponse()
        text = resp.read().decode()
        conn.close()
        return resp.status, {k.lower(): v for k, v in resp.getheaders()}, json.loads(text) if text else None

    def stop(self) -> int:
        self.proc.terminate()
        code = self.proc.wait(timeout=5)
        self.proc.stdout.close()
        self.proc.stderr.close()
        return code


class RestartTest(unittest.TestCase):
    """AC-8"""

    def test_links_and_hits_survive_restart(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = os.path.join(tmp, "shorty.db")
            first = Process(db)
            code = first.request("POST", "/links", {"url": "https://example.com/keep"})[2]["code"]
            first.request("GET", "/" + code)
            self.assertEqual(first.stop(), 0)

            second = Process(db)
            try:
                status, headers, _ = second.request("GET", "/" + code)
                self.assertEqual((status, headers["location"]), (302, "https://example.com/keep"))
                self.assertEqual(second.request("GET", "/links/" + code)[2]["hits"], 2)
            finally:
                second.stop()


class CliTest(unittest.TestCase):
    def test_base_url_flag_sets_short_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Process(os.path.join(tmp, "shorty.db"), "--base-url", "https://sho.rt/")
            try:
                body = p.request("POST", "/links", {"url": "https://example.com/b"})[2]
                self.assertEqual(body["short_url"], "https://sho.rt/" + body["code"])
            finally:
                p.stop()

    def test_unwritable_db_exits_non_zero(self) -> None:
        env = {**os.environ, "PYTHONPATH": SRC}
        result = subprocess.run(
            [sys.executable, "-m", "shorty", "--port", "0", "--db", "/nonexistent/dir/shorty.db"],
            capture_output=True, text=True, env=env, timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shorty:", result.stderr)


if __name__ == "__main__":
    unittest.main()
