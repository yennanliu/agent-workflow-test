# shorty (demo_project_1)

A small self-hosted URL shortener: an HTTP JSON API on the Python standard library, with links stored in SQLite.

It was built end to end with the [`dev-flow`](../../README.md) plugin, as a worked example of every stage. Each stage's output is in [`docs/dev-flow/url-shortener/`](docs/dev-flow/url-shortener/):

| Stage | Artifact |
| --- | --- |
| setup | [`docs/dev-flow/config.md`](docs/dev-flow/config.md) |
| grill | [`grill-log.md`](docs/dev-flow/url-shortener/grill-log.md), [`GLOSSARY.md`](GLOSSARY.md), [ADR 0001](docs/adr/0001-random-codes.md) |
| spec | [`spec.md`](docs/dev-flow/url-shortener/spec.md): 8 acceptance criteria, 5 user journeys, a trace table |
| interface | [`src/shorty/links.py`](src/shorty/links.py), [`src/shorty/http.py`](src/shorty/http.py), [`tests/test_contract.py`](tests/test_contract.py) |
| design | [`design.md`](docs/dev-flow/url-shortener/design.md) |
| tickets | [`tickets/`](docs/dev-flow/url-shortener/tickets/): 5 planned, plus 2 that came out of review |
| implement | one commit per ticket (`git log -- ws/demo_project_1`) |
| harden | contract tests enabled, integration tests through the real CLI process |
| validate | [`review.md`](docs/dev-flow/url-shortener/review.md): a two-axis subagent review that found 4 blocking issues, then 1 more on re-check |
| deploy | [`release.md`](docs/dev-flow/url-shortener/release.md): staging plus a rollback drill, which caught a bug in the deploy script |
| e2e | [`e2e.md`](docs/dev-flow/url-shortener/e2e.md): all 5 journeys pass on staging |
| retro | [`retro.md`](docs/dev-flow/url-shortener/retro.md) |

In this demo the agent answered its own grill questions and approved its own spec. In a real run, those two decisions are yours.

## Run it

```bash
PYTHONPATH=src python3 -m shorty --port 8080 --db shorty.db
curl -s -X POST localhost:8080/links -d '{"url": "https://example.com/some/long/path"}'
curl -si localhost:8080/<code>            # 302 to the target
curl -s localhost:8080/links/<code>       # {"code", "url", "created_at", "hits"}
```

## API

| Request | Response |
| --- | --- |
| `POST /links` `{"url": "https://…"}` | `201` new link, `200` existing link: `{"code", "short_url", "url"}`; `400` bad URL |
| `GET /{code}` | `302` to the target; `404` unknown code; `410` stored target no longer allowed |
| `GET /links/{code}` | `200` `{"code", "url", "created_at", "hits"}`; `404` |
| `GET /healthz` | `200` `{"status": "ok"}` |

Every error is JSON: `{"error": "…"}`.

## Develop

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -t .     # 42 tests
scripts/deploy.sh staging                                       # local staging on :8081
python3 e2e/run_e2e.py --base-url http://127.0.0.1:8081 --restart-cmd "scripts/restart.sh staging"
scripts/rollback.sh staging
scripts/stop.sh staging
```

Requires Python 3.10+ with SQLite 3.35+ (bundled on most platforms). No packages to install.
