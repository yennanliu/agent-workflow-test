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


class ErrorsOverHttp(HttpCase):
    def test_bad_url_is_400_json(self) -> None:
        status, _, body = self.s.request("POST", "/links", {"url": "javascript:alert(1)"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_missing_url_and_non_json_are_400(self) -> None:
        for kwargs in ({"body": {}}, {"raw": b"{not json"}, {"body": ["https://example.com"]}):
            with self.subTest(**{k: str(v) for k, v in kwargs.items()}):
                status, _, body = self.s.request("POST", "/links", **kwargs)
                self.assertEqual(status, 400)
                self.assertIn("error", body)

    def test_oversized_body_is_400(self) -> None:
        status, _, body = self.s.request("POST", "/links", raw=b"x" * 9000)
        self.assertEqual(status, 400)

    def test_unknown_code_and_route_are_404_json(self) -> None:
        for method, path in (("GET", "/zzzzzzz"), ("GET", "/links/zzzzzzz"), ("POST", "/nope")):
            with self.subTest(path=path):
                status, _, body = self.s.request(method, path, {} if method == "POST" else None)
                self.assertEqual(status, 404)
                self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
