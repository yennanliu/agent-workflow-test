# Grill log: url-shortener

Demo run of `/dev-flow:grill`. For this demo the agent accepted its own recommended answer to every question in place of the user. In a real run, each answer below is the user's.

## Round 1

**Q1. What is the product?** A self-hosted URL shortener with an HTTP JSON API, no UI.
→ Recommended: yes. An API keeps the demo small and every behaviour testable over HTTP.

**Q2. Which stack?** Python standard library only (`http.server`, `sqlite3`, `secrets`), no frameworks.
→ Recommended: yes. Nothing to install, so the demo runs anywhere Python 3.10+ runs.

**Q3. Where do links live?** One SQLite file, path set by a `--db` flag.
→ Recommended: yes. Links survive restarts with no server to run.

**Q4. Who can create links?** Anyone who can reach the service; no auth in this version.
→ Recommended: yes, and auth goes in Out of scope.

## Round 2 (unblocked by Q1–Q3)

**Q5. How are codes made?** 7 random base62 characters, retry on collision.
→ Recommended: yes. Sequential codes leak volume and allow enumeration, and codes can never change once shared. Recorded as ADR 0001.

**Q6. Same URL twice?** Return the existing link instead of making a new code.
→ Recommended: yes. Shortening is idempotent, so callers can retry safely.

**Q7. Which URLs are valid?** `http` or `https`, with a host, at most 2048 characters.
→ Recommended: yes. That rejects `javascript:` and `file:` URLs and keeps rows bounded.

**Q8. What does following a link return?** `302 Found` with `Location` set to the target, and one hit recorded.
→ Recommended: yes. 302 rather than 301, so browsers don't cache the redirect and every follow is counted.

**Q9. Stats?** `GET /links/{code}` returns the target, creation time and hit count.
→ Recommended: yes.

**Q10. Operations?** `GET /healthz` returns `{"status": "ok"}` for deploy health checks.
→ Recommended: yes.

Frontier empty. Terms recorded in `GLOSSARY.md`; one ADR recorded.
