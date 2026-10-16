"""Links: shortening, following and stats, stored in SQLite."""

from __future__ import annotations

import secrets
import sqlite3
import string
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlsplit

ALPHABET = string.digits + string.ascii_letters
CODE_LENGTH = 7
MAX_URL_LENGTH = 2048
MAX_CODE_ATTEMPTS = 5

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
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


def validate_url(url: object) -> str:
    """Return `url` if it can be shortened, else raise InvalidURL."""
    if not isinstance(url, str) or not url:
        raise InvalidURL("url must be a non-empty string")
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL(f"url must be at most {MAX_URL_LENGTH} characters")
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise InvalidURL("url must be an http or https URL with a host")
    return url


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
        url = validate_url(url)
        with self._lock, self._db:
            if existing := self._by_url(url):
                return existing, False
            created_at = self._clock()
            for _ in range(MAX_CODE_ATTEMPTS):
                code = self._new_code()
                try:
                    self._db.execute(
                        "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                        (code, url, created_at),
                    )
                except sqlite3.IntegrityError:
                    # Another process may have stored this URL; otherwise the code was taken.
                    if existing := self._by_url(url):
                        return existing, False
                    continue
                return Link(code, url, created_at, 0), True
        raise RuntimeError(f"no free code after {MAX_CODE_ATTEMPTS} attempts")

    def follow(self, code: str) -> Link:
        """Record one hit and return the link."""
        with self._lock, self._db:
            row = self._db.execute(
                "UPDATE links SET hits = hits + 1 WHERE code = ? "
                "RETURNING code, url, created_at, hits",
                (code,),
            ).fetchone()
        if row is None:
            raise LinkNotFound(code)
        return Link(*row)

    def stats(self, code: str) -> Link:
        with self._lock:
            row = self._db.execute(
                "SELECT code, url, created_at, hits FROM links WHERE code = ?", (code,)
            ).fetchone()
        if row is None:
            raise LinkNotFound(code)
        return Link(*row)

    def _by_url(self, url: str) -> Link | None:
        row = self._db.execute(
            "SELECT code, url, created_at, hits FROM links WHERE url = ?", (url,)
        ).fetchone()
        return Link(*row) if row else None

    def close(self) -> None:
        self._db.close()
