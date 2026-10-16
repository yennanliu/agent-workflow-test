from __future__ import annotations

import unittest

from tests.support import RunningServer


class HttpCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = RunningServer()

    def tearDown(self) -> None:
        self.s.stop()


class ShortenAndFollowOverHttp(HttpCase):
    def test_post_then_get_redirects(self) -> None:
        status, _, body = self.s.request("POST", "/links", {"url": "https://example.com/z"})
        self.assertEqual(status, 201)
        self.assertEqual(body["short_url"], f"http://127.0.0.1:{self.s.port}/{body['code']}")
        status, headers, _ = self.s.request("GET", "/" + body["code"])
        self.assertEqual(status, 302)
        self.assertEqual(headers["location"], "https://example.com/z")

    def test_healthz(self) -> None:
        self.assertEqual(self.s.request("GET", "/healthz")[::2], (200, {"status": "ok"}))


if __name__ == "__main__":
    unittest.main()
