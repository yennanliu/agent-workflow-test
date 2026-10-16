# E2E: url-shortener

Run by `/dev-flow:e2e` on 2026-10-16 against staging (`http://127.0.0.1:8081`, release `20261016192643-da9ad36`):

```
python3 e2e/run_e2e.py --base-url http://127.0.0.1:8081 --restart-cmd "scripts/restart.sh staging"
```

| Journey | Environment | Result | Evidence |
| --- | --- | --- | --- |
| UJ-1 Shorten and follow | staging | pass | `http://127.0.0.1:8081/F5d00Tk` → 302 `https://example.com/e2e/uj1/c529926a` |
| UJ-2 Measure | staging | pass | code `nZqQ5XA`, re-shorten 200, hits 2 |
| UJ-3 Mistakes | staging | pass | `javascript:` → 400; unknown code → 404 |
| UJ-4 Restart | staging | pass | code `sLUfQW2` still redirects after a real process restart, hits 2 |
| UJ-5 Health | staging | pass | 200 `{"status": "ok"}` |

There is no production smoke run, because this demo has no production environment. No failures, so no new tickets.
