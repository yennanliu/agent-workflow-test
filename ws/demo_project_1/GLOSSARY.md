# Glossary

## Link
A stored pair of a target URL and the short code that points at it, plus its creation time and hit count.
Avoid: entry, record, mapping

## Code
The 7-character base62 string that identifies a link in a short URL.
Avoid: slug, key, token, id

## Short URL
The service's base URL followed by a code, e.g. `http://127.0.0.1:8081/aZ3kQ9x`.
Avoid: tiny URL, alias

## Follow
Requesting a short URL and being redirected to the link's target. Each follow adds one hit.
Avoid: visit, click, open

## Hit
One recorded follow of a link.
Avoid: view, click
