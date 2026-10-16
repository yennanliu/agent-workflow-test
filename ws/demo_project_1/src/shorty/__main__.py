"""Run the shorty server: python -m shorty --port 8080 --db shorty.db"""

from __future__ import annotations

import argparse
import logging
import signal
import sqlite3
import sys
from types import FrameType

from shorty.http import make_server
from shorty.links import LinkService


def _stop(signum: int, frame: FrameType | None) -> None:
    raise KeyboardInterrupt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="shorty", description="A small self-hosted URL shortener.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--db", default="shorty.db", help="SQLite file; created if missing")
    parser.add_argument("--base-url", help="public base URL for short URLs, e.g. https://sho.rt")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    try:
        service = LinkService(args.db)
        server = make_server(service, args.host, args.port, args.base_url)
    except (OSError, sqlite3.Error) as exc:
        print(f"shorty: {exc}", file=sys.stderr)
        return 1

    host, port = server.server_address[:2]
    print(f"shorty listening on http://{host}:{port}", flush=True)
    signal.signal(signal.SIGTERM, _stop)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        service.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
