from __future__ import annotations

import os
import re
import tempfile
import unittest

from shorty.links import LinkService


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


if __name__ == "__main__":
    unittest.main()
