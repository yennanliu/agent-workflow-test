"""Links: shortening, following and stats, stored in SQLite."""

from __future__ import annotations

import secrets
import sqlite3
import string
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

ALPHABET = string.digits + string.ascii_letters
CODE_LENGTH = 7

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    created_at TEXT NOT NULL,
    hits INTEGER NOT NULL DEFAULT 0
)
"""


@dataclass(frozen=True)
class Link:
    code: str
    url: str
    created_at: str
    hits: int


class InvalidURL(ValueError):
    """The URL can't be shortened."""


class LinkNotFound(LookupError):
    """No link has this code."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _random_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


class LinkService:
    def __init__(
        self,
        db_path: str,
        *,
        clock: Callable[[], str] | None = None,
        new_code: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or _utc_now
        self._new_code = new_code or _random_code
        self._lock = threading.Lock()
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self._db.execute(SCHEMA)
        self._db.commit()

    def shorten(self, url: str) -> tuple[Link, bool]:
        """Return the link for `url` and whether it was just created."""
        link = Link(self._new_code(), url, self._clock(), 0)
        with self._lock, self._db:
            self._db.execute(
                "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                (link.code, link.url, link.created_at),
            )
        return link, True

    def follow(self, code: str) -> Link:
        """Record one hit and return the link."""
        with self._lock:
            row = self._db.execute(
                "SELECT code, url, created_at, hits FROM links WHERE code = ?", (code,)
            ).fetchone()
        return Link(*row)

    def stats(self, code: str) -> Link:
        raise NotImplementedError

    def close(self) -> None:
        self._db.close()
