Status: todo

# 03 Idempotent shorten

- **ACs:** AC-5
- **Modules:** links, http
- **Blocked by:** 01

The same URL returns the same code: 201 when created, 200 after. Code collisions retry with a new code.

**Done when** two POSTs of one URL return one code with 201 then 200, and a forced collision still creates the link.
