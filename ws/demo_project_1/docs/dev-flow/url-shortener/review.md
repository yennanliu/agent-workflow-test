# Review: url-shortener

Run by `/dev-flow:validate` in a fresh subagent over the diff since `6e8fb60`, against `spec.md` and `docs/standards.md`. 30/30 tests passing at review time.

## Standards
| # | File:line | Finding | Blocking | Outcome |
| --- | --- | --- | --- | --- |
| 1 | links.py:55, http.py:50 | `urlsplit` strips CR/LF/tab, so a target with `\r\nSet-Cookie: …` was accepted and injected a response header on redirect (reproduced) | yes | fixed in ticket 06 |
| 2 | http.py:48 | Non-ASCII target crashed after the 302 status line was sent; double response, hit still counted (reproduced) | yes | fixed in ticket 06 |
| 3 | http.py:67 | Negative `Content-Length` blocked a handler thread forever; no socket timeout (reproduced) | yes | fixed in ticket 06 |
| 4 | http.py:33 | PUT/DELETE/HEAD and stdlib 400/414 errors returned HTML, not JSON | yes | fixed in ticket 06 |
| 5 | `__pycache__/*.pyc` | Bytecode committed before `.gitignore` existed | no | fixed |
| 6 | links.py:82 | Idempotency compares raw strings (`https://x.com` vs `https://x.com/` vs upper-case host) | no | open: spec doesn't require normalisation |
| 7 | __main__.py:37 | SIGTERM handler installed after the "listening" line | no | fixed |
| 8 | __main__.py:43 | `service.close()` may race in-flight daemon handler threads at shutdown | no | open |
| 9 | http.py:77 | `route: Any` should be `Callable[[], None]` | no | fixed |
| 10 | links.py:102 | `UPDATE … RETURNING` needs SQLite ≥ 3.35, undocumented | no | documented in design.md |
| 11 | test_http.py:61 | Oversized-body test doesn't assert the `error` key; findings 1–4 untested | no | fixed in ticket 06 |
| 12 | http.py:50 | *Re-check:* findings 1–2 were only validated on write; rows stored before 06 still injected headers on follow, and deploys keep the database (reproduced) | yes | fixed in ticket 07 (410 Gone, no hit) |
| 13 | http.py:73 | *Re-check:* body shorter than `Content-Length` timed out into a 500 | no | fixed in ticket 07 (400) |
| 14 | http.py:send_error | *Re-check:* error replies to HEAD carried a body | no | fixed in ticket 07 |

Re-check after ticket 06 (same reviewer): findings 1–4 fixed for new links; finding 12 raised. After ticket 07: 42/42 tests passing, no blocking finding open.

## Spec
| AC | Verdict at review | Evidence |
| --- | --- | --- |
| AC-1 | met | `ShortenContract`, `ShortenAndFollowOverHttp.test_post_then_get_redirects` |
| AC-2 | partly → met after 06 | `FollowContract`; failed for non-ASCII and CR/LF targets (findings 1, 2) |
| AC-3 | met | `NotFoundContract`, `ErrorsOverHttp.test_unknown_code_and_route_are_404_json` |
| AC-4 | partly → met after 06 | `InvalidURLContract`; control characters and HTML errors (findings 1, 4) |
| AC-5 | met | `IdempotentContract`, `test_links.Idempotent` |
| AC-6 | met | `StatsContract`, `test_concurrent_follows_lose_no_hits` |
| AC-7 | met | `HealthContract` |
| AC-8 | met | `RestartTest.test_links_and_hits_survive_restart` |
