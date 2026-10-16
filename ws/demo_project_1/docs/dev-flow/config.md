# dev-flow config

## Commands
- install: `none` (standard library only, Python 3.10+)
- typecheck: `python3 -m compileall -q src tests e2e`
- lint: `none`
- test, one file: `PYTHONPATH=src python3 -m unittest tests/{file}`
- test, full suite: `PYTHONPATH=src python3 -m unittest discover -s tests -t .`
- build: `none`
- e2e: `python3 e2e/run_e2e.py --base-url {url}`

## Environments
- staging deploy: `scripts/deploy.sh staging`
- staging health check: `curl -fsS http://127.0.0.1:8081/healthz`
- production deploy: `none` (demo project: staging is the last environment)
- production health check: `none`
- rollback: `scripts/rollback.sh staging`

## Tickets
- tracker: `local` (docs/dev-flow/<feature>/tickets/)

## Standards
- coding standards: `docs/standards.md`
- commit style: `demo_project_1: <ticket title>`
