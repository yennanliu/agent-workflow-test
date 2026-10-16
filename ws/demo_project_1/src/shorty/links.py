"""Links: shortening, following and stats, stored in SQLite."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


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


class LinkService:
    def __init__(
        self,
        db_path: str,
        *,
        clock: Callable[[], str] | None = None,
        new_code: Callable[[], str] | None = None,
    ) -> None:
        raise NotImplementedError

    def shorten(self, url: str) -> tuple[Link, bool]:
        """Return the link for `url` and whether it was just created."""
        raise NotImplementedError

    def follow(self, code: str) -> Link:
        """Record one hit and return the link."""
        raise NotImplementedError

    def stats(self, code: str) -> Link:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
