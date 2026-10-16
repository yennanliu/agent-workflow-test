"""Contract tests: one class per interface call in the spec's Trace table."""

from __future__ import annotations

import re
import unittest

from tests.support import RunningServer

CODE = re.compile(r"^[0-9A-Za-z]{7}$")


class ServerCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = RunningServer()

    def tearDown(self) -> None:
        self.s.stop()

    def shorten(self, url: str) -> dict:
        status, _, body = self.s.request("POST", "/links", {"url": url})
        self.assertIn(status, (200, 201))
        return body


class ShortenContract(ServerCase):
    """AC-1"""

    def test_returns_201_with_code_short_url_and_url(self) -> None:
        status, _, body = self.s.request("POST", "/links", {"url": "https://example.com/a"})
        self.assertEqual(status, 201)
        self.assertRegex(body["code"], CODE)
        self.assertEqual(body["url"], "https://example.com/a")
        self.assertTrue(body["short_url"].endswith("/" + body["code"]))


class FollowContract(ServerCase):
    """AC-2"""

    def test_redirects_302_to_target(self) -> None:
        code = self.shorten("https://example.com/b")["code"]
        status, headers, _ = self.s.request("GET", "/" + code)
        self.assertEqual(status, 302)
        self.assertEqual(headers["location"], "https://example.com/b")


class NotFoundContract(ServerCase):
    """AC-3"""

    def test_unknown_code_is_404_json(self) -> None:
        for path in ("/zzzzzzz", "/links/zzzzzzz"):
            with self.subTest(path=path):
                status, _, body = self.s.request("GET", path)
                self.assertEqual(status, 404)
                self.assertIn("error", body)


class InvalidURLContract(ServerCase):
    """AC-4"""

    def test_bad_input_is_400_json(self) -> None:
        cases = {
            "missing url": {"other": 1},
            "javascript": {"url": "javascript:alert(1)"},
            "ftp": {"url": "ftp://example.com/f"},
            "no host": {"url": "https://"},
            "too long": {"url": "https://example.com/" + "a" * 2048},
            "not a string": {"url": 42},
        }
        for name, body in cases.items():
            with self.subTest(name):
                status, _, payload = self.s.request("POST", "/links", body)
                self.assertEqual(status, 400)
                self.assertIn("error", payload)

    def test_non_json_body_is_400(self) -> None:
        status, _, payload = self.s.request("POST", "/links", raw=b"not json")
        self.assertEqual(status, 400)
        self.assertIn("error", payload)


class IdempotentContract(ServerCase):
    """AC-5"""

    def test_same_url_same_code_201_then_200(self) -> None:
        first = self.s.request("POST", "/links", {"url": "https://example.com/c"})
        second = self.s.request("POST", "/links", {"url": "https://example.com/c"})
        self.assertEqual((first[0], second[0]), (201, 200))
        self.assertEqual(first[2]["code"], second[2]["code"])


class StatsContract(ServerCase):
    """AC-6"""

    def test_each_follow_adds_one_hit(self) -> None:
        code = self.shorten("https://example.com/d")["code"]
        self.s.request("GET", "/" + code)
        self.s.request("GET", "/" + code)
        status, _, body = self.s.request("GET", "/links/" + code)
        self.assertEqual(status, 200)
        self.assertEqual(body["hits"], 2)
        self.assertEqual(body["url"], "https://example.com/d")
        self.assertEqual(body["code"], code)
        self.assertIn("created_at", body)


class HealthContract(ServerCase):
    """AC-7"""

    def test_healthz_ok(self) -> None:
        status, _, body = self.s.request("GET", "/healthz")
        self.assertEqual((status, body), (200, {"status": "ok"}))


if __name__ == "__main__":
    unittest.main()
