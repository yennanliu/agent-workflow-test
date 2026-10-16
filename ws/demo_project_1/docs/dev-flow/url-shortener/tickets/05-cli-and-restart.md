Status: done

# 05 CLI and restart persistence

- **ACs:** AC-8
- **Modules:** cli, links
- **Blocked by:** 01, 04

`python -m shorty --host --port --db --base-url` runs the server; links and hits survive a restart on the same db file.

**Done when** a link followed before a restart still redirects afterwards with its hit count kept.
