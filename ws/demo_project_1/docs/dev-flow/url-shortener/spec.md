# URL shortener (shorty)

**Approved:** 2026-10-16 (demo run: approved by the agent on the user's behalf)

## Problem
Long URLs are hard to share in chat and print. Teams want a self-hosted service that turns a URL into a short URL and counts how often it is followed, without sending links to a third party. It is fixed when a link can be shortened, followed and measured over HTTP, and survives a restart.

## Acceptance criteria
- **AC-1** `POST /links` with `{"url": "<target>"}` returns `201` and `{"code", "short_url", "url"}`, where `code` is 7 base62 characters. Check: contract test on the response shape.
- **AC-2** `GET /{code}` returns `302` with `Location` equal to the link's target. Check: HTTP test without following redirects.
- **AC-3** `GET /{code}` and `GET /links/{code}` for an unknown code return `404` and `{"error": ...}`. Check: HTTP test.
- **AC-4** `POST /links` with a missing, non-`http(s)`, hostless or over-2048-character URL, or a body that isn't JSON, returns `400` and `{"error": ...}`. Check: table of bad inputs.
- **AC-5** Shortening the same URL twice returns the same code, with `201` the first time and `200` after. Check: two POSTs compared.
- **AC-6** `GET /links/{code}` returns `{"code", "url", "created_at", "hits"}`; each follow adds exactly one hit. Check: follow twice, then hits == 2.
- **AC-7** `GET /healthz` returns `200` and `{"status": "ok"}`. Check: HTTP test.
- **AC-8** Links and hit counts survive a restart that keeps the same `--db` file. Check: restart test.

## User journeys
- **UJ-1** Shorten and follow: POST a URL → GET the short URL → land on the target. Covers AC-1, AC-2.
- **UJ-2** Measure: shorten → follow twice → shorten the same URL again → read stats showing 2 hits and the same code. Covers AC-5, AC-6.
- **UJ-3** Mistakes: POST a `javascript:` URL → 400; GET an unknown code → 404. Covers AC-3, AC-4.
- **UJ-4** Restart: shorten and follow → restart the service → the short URL still redirects and the hit count is kept. Covers AC-8.
- **UJ-5** Health: GET `/healthz` → ok. Covers AC-7.

## Out of scope
- Authentication, rate limiting and abuse detection
- Custom codes and link expiry
- A web UI

## Trace
| AC | Interface | Module | Ticket | Test |
| --- | --- | --- | --- | --- |
| AC-1 | `POST /links`; `LinkService.shorten` | `links`, `http` | 01 | `test_contract.ShortenContract` |
| AC-2 | `GET /{code}`; `LinkService.follow` | `links`, `http` | 01 | `test_contract.FollowContract` |
| AC-3 | `GET /{code}`, `GET /links/{code}`; `LinkNotFound` | `links`, `http` | 02 | `test_contract.NotFoundContract` |
| AC-4 | `POST /links`; `InvalidURL` | `links`, `http` | 02 | `test_contract.InvalidURLContract` |
| AC-5 | `LinkService.shorten` → `(link, created)` | `links` | 03 | `test_contract.IdempotentContract` |
| AC-6 | `GET /links/{code}`; `LinkService.stats` | `links`, `http` | 04 | `test_contract.StatsContract` |
| AC-7 | `GET /healthz` | `http` | 01 | `test_contract.HealthContract` |
| AC-8 | `python -m shorty --db`; `LinkService(db_path)` | `links`, `cli` | 05 | `test_integration.RestartTest` |
