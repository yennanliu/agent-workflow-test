---
name: tdd
description: Build behaviour test-first in a red-green-refactor loop, one vertical slice at a time. Use when implementing a feature or fixing a bug, or when the user says TDD or test-first.
---

Build in a **tight** loop of **red**, **green**, **refactor**, one vertical slice at a time.

1. **Red.** Write one test for the next smallest behaviour, through the public interface. Run it. Done when it fails for the reason you expect; a test that passes or fails for another reason is fixed before going on.
2. **Green.** Write the least code that makes it pass. Run it. Done when it and every earlier test pass.
3. **Refactor.** With the suite green, remove duplication and sharpen names. Done when the suite is still green.

Then pick the next slice. For a bug, the first red test reproduces the bug.

Tests describe behaviour a user or caller can observe, so they survive a rewrite of the internals. Reach for a fake only at a boundary you don't own (network, clock, payment provider), and keep it at that boundary.
