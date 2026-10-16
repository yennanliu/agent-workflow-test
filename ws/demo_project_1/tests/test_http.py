from __future__ import annotations

import socket
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


class IdempotentOverHttp(HttpCase):
    def test_second_post_is_200_with_same_code(self) -> None:
        first = self.s.request("POST", "/links", {"url": "https://example.com/again"})
        second = self.s.request("POST", "/links", {"url": "https://example.com/again"})
        self.assertEqual((first[0], second[0]), (201, 200))
        self.assertEqual(first[2], second[2])


class StatsOverHttp(HttpCase):
    def test_stats_show_hits_after_follows(self) -> None:
        code = self.s.request("POST", "/links", {"url": "https://example.com/st"})[2]["code"]
        self.s.request("GET", "/" + code)
        self.s.request("GET", "/" + code)
        status, _, body = self.s.request("GET", "/links/" + code)
        self.assertEqual(status, 200)
        self.assertEqual(body["hits"], 2)
        self.assertEqual(set(body), {"code", "url", "created_at", "hits"})


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
        self.assertIn("error", body)

    def test_unknown_code_and_route_are_404_json(self) -> None:
        for method, path in (("GET", "/zzzzzzz"), ("GET", "/links/zzzzzzz"), ("POST", "/nope")):
            with self.subTest(path=path):
                status, _, body = self.s.request(method, path, {} if method == "POST" else None)
                self.assertEqual(status, 404)
                self.assertIn("error", body)


class ReviewFixes(HttpCase):
    def raw(self, request: bytes) -> bytes:
        with socket.create_connection(("127.0.0.1", self.s.port), timeout=3) as sock:
            sock.sendall(request)
            chunks = []
            while chunk := sock.recv(4096):
                chunks.append(chunk)
        return b"".join(chunks)

    def test_crlf_target_cannot_inject_headers(self) -> None:
        status, _, _ = self.s.request("POST", "/links", {"url": "https://example.com/a\r\nSet-Cookie: pwn=1"})
        self.assertEqual(status, 400)

    def test_non_ascii_target_redirects_percent_encoded(self) -> None:
        body = self.s.request("POST", "/links", {"url": "https://example.com/日本"})[2]
        status, headers, _ = self.s.request("GET", "/" + body["code"])
        self.assertEqual((status, headers["location"]), (302, "https://example.com/%E6%97%A5%E6%9C%AC"))

    def test_negative_content_length_is_400(self) -> None:
        reply = self.raw(b"POST /links HTTP/1.1\r\nHost: x\r\nContent-Length: -1\r\n\r\n")
        self.assertTrue(reply.startswith(b"HTTP/1.0 400"), reply[:40])
        self.assertIn(b'"error"', reply)

    def test_unsupported_method_is_json(self) -> None:
        for method in ("PUT", "DELETE", "PATCH"):
            with self.subTest(method=method):
                status, headers, body = self.s.request(method, "/links")
                self.assertEqual(headers["content-type"], "application/json")
                self.assertIn("error", body)
                self.assertGreaterEqual(status, 400)

    def test_unsafe_stored_target_is_410_without_location(self) -> None:
        import sqlite3

        with sqlite3.connect(self.s.db_path) as db:
            db.execute("INSERT INTO links (code, url, created_at) VALUES ('LEGACY2', ?, 'old')",
                       ("https://example.com/a\r\nSet-Cookie: pwn=1",))
        reply = self.raw(b"GET /LEGACY2 HTTP/1.1\r\nHost: x\r\n\r\n")
        self.assertTrue(reply.startswith(b"HTTP/1.0 410"), reply[:40])
        self.assertNotIn(b"Set-Cookie", reply)
        self.assertNotIn(b"Location", reply)

    def test_short_body_is_400(self) -> None:
        reply = self.raw(b'POST /links HTTP/1.1\r\nHost: x\r\nContent-Length: 50\r\n\r\n{"url"')
        self.assertTrue(reply.startswith(b"HTTP/1.0 400"), reply[:40])

    def test_head_error_has_no_body(self) -> None:
        reply = self.raw(b"HEAD /links HTTP/1.1\r\nHost: x\r\n\r\n")
        head, _, body = reply.partition(b"\r\n\r\n")
        self.assertTrue(head.startswith(b"HTTP/1.0 501"), head[:40])
        self.assertEqual(body, b"")

    def test_malformed_request_line_is_json(self) -> None:
        reply = self.raw(b"GARBAGE\r\n\r\n")
        self.assertTrue(reply.startswith(b"HTTP/1.0 400"), reply[:40])
        self.assertIn(b"application/json", reply)


if __name__ == "__main__":
    unittest.main()
