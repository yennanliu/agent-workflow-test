# Retro: url-shortener

| # | What went wrong | Fix | Kind | Status |
| --- | --- | --- | --- | --- |
| 1 | Header injection (CR/LF in a target URL) got through grill, spec and five tickets; only the review caught it. | `/dev-flow:spec`: for every input that reaches an HTTP header, a shell, SQL or HTML, add an acceptance criterion for hostile input. | skill edit | proposed |
| 2 | Input was validated only on write, so rows stored before the fix were still unsafe. | Standard: "Validate untrusted data where it is used, not only where it is stored." | coding standard | applied |
| 3 | The per-ticket `code-review` in `/dev-flow:implement` was skipped in this demo and batched into `/dev-flow:validate`, so four blocking findings surfaced late, after five tickets. | Keep the per-ticket review; the skill already says so. | process | dropped (the skill was right; the demo cut a corner) |
| 4 | `.pyc` files were committed before `.gitignore` existed. | `/dev-flow:setup`: make sure `.gitignore` covers the stack's build and cache output before the first commit. | skill edit | proposed |
| 5 | Two deploys in the same second shared a release ID. | Fixed in `scripts/deploy.sh`; the staging rollback drill in `/dev-flow:deploy` is what caught it, so keep it. | deterministic check | applied |
| 6 | Idempotency compares raw URL strings (`https://x.com` vs `https://x.com/`), from review finding 6. | Needs a spec decision first: should URLs be normalised? | spec question | open |

Proposed skill edits (1 and 4) are left for the plugin owner to approve.
