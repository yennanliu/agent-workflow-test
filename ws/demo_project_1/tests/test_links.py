from __future__ import annotations

import os
import re
import tempfile
import unittest

from shorty.links import InvalidURL, LinkNotFound, LinkService


class LinkServiceCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "shorty.db")
        self.svc = LinkService(self.db, clock=lambda: "2026-10-16T00:00:00Z")

    def tearDown(self) -> None:
        self.svc.close()
        self.tmp.cleanup()


class ShortenAndFollow(LinkServiceCase):
    def test_shorten_creates_link_with_7_char_base62_code(self) -> None:
        link, created = self.svc.shorten("https://example.com/x")
        self.assertTrue(created)
        self.assertRegex(link.code, re.compile(r"^[0-9A-Za-z]{7}$"))
        self.assertEqual(link.url, "https://example.com/x")
        self.assertEqual(link.created_at, "2026-10-16T00:00:00Z")
        self.assertEqual(link.hits, 0)

    def test_follow_returns_target(self) -> None:
        link, _ = self.svc.shorten("https://example.com/y")
        self.assertEqual(self.svc.follow(link.code).url, "https://example.com/y")


class Idempotent(LinkServiceCase):
    def test_same_url_returns_same_link(self) -> None:
        first, created_first = self.svc.shorten("https://example.com/same")
        second, created_second = self.svc.shorten("https://example.com/same")
        self.assertEqual((created_first, created_second), (True, False))
        self.assertEqual(first.code, second.code)

    def test_code_collision_retries_with_new_code(self) -> None:
        codes = iter(["AAAAAAA", "AAAAAAA", "BBBBBBB"])
        svc = LinkService(self.db, new_code=lambda: next(codes))
        self.addCleanup(svc.close)
        self.assertEqual(svc.shorten("https://example.com/1")[0].code, "AAAAAAA")
        self.assertEqual(svc.shorten("https://example.com/2")[0].code, "BBBBBBB")

    def test_gives_up_after_five_collisions(self) -> None:
        svc = LinkService(self.db, new_code=lambda: "CCCCCCC")
        self.addCleanup(svc.close)
        svc.shorten("https://example.com/first")
        with self.assertRaises(RuntimeError):
            svc.shorten("https://example.com/second")


class Hits(LinkServiceCase):
    def test_each_follow_adds_one_hit(self) -> None:
        link, _ = self.svc.shorten("https://example.com/h")
        self.assertEqual(self.svc.follow(link.code).hits, 1)
        self.assertEqual(self.svc.follow(link.code).hits, 2)
        self.assertEqual(self.svc.stats(link.code).hits, 2)

    def test_stats_does_not_add_a_hit(self) -> None:
        link, _ = self.svc.shorten("https://example.com/s")
        self.svc.stats(link.code)
        self.assertEqual(self.svc.stats(link.code).hits, 0)

    def test_concurrent_follows_lose_no_hits(self) -> None:
        import threading

        link, _ = self.svc.shorten("https://example.com/c")
        threads = [threading.Thread(target=self.svc.follow, args=(link.code,)) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(self.svc.stats(link.code).hits, 50)


class Errors(LinkServiceCase):
    def test_rejects_bad_urls(self) -> None:
        for url in ["", "javascript:alert(1)", "ftp://example.com", "https://", "example.com",
                    "https://example.com/" + "a" * 2048, 42, None]:
            with self.subTest(url=url), self.assertRaises(InvalidURL):
                self.svc.shorten(url)  # type: ignore[arg-type]

    def test_accepts_url_at_2048_chars(self) -> None:
        url = "https://example.com/" + "a" * (2048 - len("https://example.com/"))
        self.assertEqual(self.svc.shorten(url)[0].url, url)

    def test_unknown_code_raises_not_found(self) -> None:
        with self.assertRaises(LinkNotFound):
            self.svc.follow("zzzzzzz")


if __name__ == "__main__":
    unittest.main()
