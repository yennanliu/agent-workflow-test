Status: done

# 04 Stats and hit counting

- **ACs:** AC-6
- **Modules:** links, http
- **Blocked by:** 01

Each follow adds one hit; `GET /links/{code}` returns code, url, created_at and hits.

**Done when** following a link twice makes its stats show 2 hits.
