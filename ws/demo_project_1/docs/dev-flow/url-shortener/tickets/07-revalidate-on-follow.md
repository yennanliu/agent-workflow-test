Status: done

# 07 Re-validate stored targets on follow

- **ACs:** AC-2
- **Modules:** links, http
- **Blocked by:** 06
- **Source:** review.md re-check, new blocking finding 12; non-blocking 13, 14

Rows written before ticket 06 can still hold unsafe targets, and deploys keep the database. `follow` re-checks the stored target; an unsafe one returns `410 Gone` (JSON, no `Location`) and records no hit. Also: a body shorter than its `Content-Length` returns 400, not 500, and error replies to HEAD carry no body.

**Done when** a raw-inserted CRLF row can't inject a header, and the full suite is green.
