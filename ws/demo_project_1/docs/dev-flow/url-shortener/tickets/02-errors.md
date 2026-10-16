Status: todo

# 02 Bad input and unknown codes

- **ACs:** AC-3, AC-4
- **Modules:** links, http
- **Blocked by:** 01

Validate URLs (`http`/`https`, host, ≤ 2048 chars, string), reject non-JSON bodies, and return JSON 400/404 errors.

**Done when** every bad input in AC-4 returns 400 and unknown codes return 404, all as `{"error": ...}`.
