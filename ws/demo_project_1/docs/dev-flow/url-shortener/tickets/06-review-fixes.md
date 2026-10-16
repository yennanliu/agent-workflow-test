Status: done

# 06 Fix blocking review findings

- **ACs:** AC-2, AC-4
- **Modules:** links, http, cli
- **Blocked by:** 05
- **Source:** review.md findings 1–4, 5, 7, 9, 11

Reject control characters and spaces in URLs; percent-encode non-ASCII path/query characters and reject non-ASCII hosts; reject negative `Content-Length` and time out idle sockets; return JSON for every error, including the stdlib's own.

**Done when** each of findings 1–4 has a test that failed before the fix and passes after, and the full suite is green.
