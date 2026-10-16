"""Run every user journey in the spec against a deployed shorty.

    python3 e2e/run_e2e.py --base-url http://127.0.0.1:8081 --restart-cmd "scripts/restart.sh staging"
"""

from __future__ import annotations

import argparse
import http.client
import json
import subprocess
import sys
import time
import uuid
from collections.abc import Callable
from typing import Any
from urllib.parse import urlsplit


class Client:
    def __init__(self, base_url: str) -> None:
        parts = urlsplit(base_url)
        self.host, self.port = parts.hostname or "127.0.0.1", parts.port or 80

    def call(self, method: str, path: str, body: Any = None) -> tuple[int, dict[str, str], Any]:
        conn = http.client.HTTPConnection(self.host, self.port, timeout=5)
        data = None if body is None else json.dumps(body).encode()
        conn.request(method, path, body=data, headers={"Content-Type": "application/json"} if data else {})
        resp = conn.getresponse()
        text = resp.read().decode()
        conn.close()
        return resp.status, {k.lower(): v for k, v in resp.getheaders()}, json.loads(text) if text else None


class JourneyFailed(AssertionError):
    pass


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise JourneyFailed(msg)


def unique_url(tag: str) -> str:
    return f"https://example.com/e2e/{tag}/{uuid.uuid4().hex[:8]}"


def uj1_shorten_and_follow(c: Client, _: argparse.Namespace) -> str:
    url = unique_url("uj1")
    status, _, body = c.call("POST", "/links", {"url": url})
    expect(status == 201, f"POST /links → {status}, want 201")
    path = urlsplit(body["short_url"]).path
    status, headers, _ = c.call("GET", path)
    expect(status == 302 and headers.get("location") == url, f"GET {path} → {status} {headers.get('location')}")
    return f"{body['short_url']} → 302 {url}"


def uj2_measure(c: Client, _: argparse.Namespace) -> str:
    url = unique_url("uj2")
    code = c.call("POST", "/links", {"url": url})[2]["code"]
    c.call("GET", "/" + code)
    c.call("GET", "/" + code)
    again = c.call("POST", "/links", {"url": url})
    expect(again[0] == 200 and again[2]["code"] == code, f"re-shorten → {again[0]} {again[2]}")
    stats = c.call("GET", "/links/" + code)[2]
    expect(stats["hits"] == 2, f"hits = {stats['hits']}, want 2")
    return f"code {code}, re-shorten 200, hits 2"


def uj3_mistakes(c: Client, _: argparse.Namespace) -> str:
    bad = c.call("POST", "/links", {"url": "javascript:alert(1)"})
    expect(bad[0] == 400 and "error" in bad[2], f"javascript URL → {bad[0]}")
    missing = c.call("GET", "/zzzzzzz")
    expect(missing[0] == 404 and "error" in missing[2], f"unknown code → {missing[0]}")
    return f"javascript: → 400 ({bad[2]['error']}); unknown → 404"


def uj4_restart(c: Client, args: argparse.Namespace) -> str:
    if not args.restart_cmd:
        return "SKIP: no --restart-cmd"
    url = unique_url("uj4")
    code = c.call("POST", "/links", {"url": url})[2]["code"]
    c.call("GET", "/" + code)
    subprocess.run(args.restart_cmd, shell=True, check=True, capture_output=True)
    for _ in range(50):
        try:
            if c.call("GET", "/healthz")[0] == 200:
                break
        except OSError:
            time.sleep(0.1)
    status, headers, _ = c.call("GET", "/" + code)
    expect(status == 302 and headers.get("location") == url, f"after restart GET → {status}")
    hits = c.call("GET", "/links/" + code)[2]["hits"]
    expect(hits == 2, f"hits after restart = {hits}, want 2")
    return f"code {code} still redirects after restart, hits 2"


def uj5_health(c: Client, _: argparse.Namespace) -> str:
    status, _, body = c.call("GET", "/healthz")
    expect((status, body) == (200, {"status": "ok"}), f"/healthz → {status} {body}")
    return "200 {\"status\": \"ok\"}"


JOURNEYS: list[tuple[str, str, Callable[[Client, argparse.Namespace], str]]] = [
    ("UJ-1", "Shorten and follow", uj1_shorten_and_follow),
    ("UJ-2", "Measure", uj2_measure),
    ("UJ-3", "Mistakes", uj3_mistakes),
    ("UJ-4", "Restart", uj4_restart),
    ("UJ-5", "Health", uj5_health),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--restart-cmd", help="shell command that restarts the service under test")
    args = parser.parse_args()
    client = Client(args.base_url)

    failed = 0
    print(f"| Journey | Result | Evidence |\n| --- | --- | --- |")
    for jid, name, run in JOURNEYS:
        try:
            evidence = run(client, args)
            result = "skip" if evidence.startswith("SKIP") else "pass"
        except (JourneyFailed, OSError, KeyError, TypeError) as exc:
            evidence, result = f"{type(exc).__name__}: {exc}", "FAIL"
            failed += 1
        print(f"| {jid} {name} | {result} | {evidence} |")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
