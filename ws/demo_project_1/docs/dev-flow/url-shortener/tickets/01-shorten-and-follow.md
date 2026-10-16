Status: todo

# 01 Shorten and follow (tracer bullet)

- **ACs:** AC-1, AC-2, AC-7
- **Modules:** links, http
- **Blocked by:** none

`POST /links` stores a link in SQLite with a random code and returns 201; `GET /{code}` redirects 302; `GET /healthz` is ok.

**Done when** a URL posted to a running server redirects from its short URL, and `/healthz` returns ok.
