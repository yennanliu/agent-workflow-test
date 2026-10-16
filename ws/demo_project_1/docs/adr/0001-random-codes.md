# 1. Codes are random, not sequential

**Status:** accepted · 2026-10-16

## Context
Short URLs get shared publicly, so a code can never change once issued. Sequential codes (base62 of the row id) are shorter and collision-free, but they reveal how many links exist and let anyone enumerate every link.

## Decision
Codes are 7 random base62 characters from `secrets`. On the rare collision, generate a new code and retry, up to 5 times.

## Consequences
- 62^7 ≈ 3.5 × 10^12 codes, so collisions stay rare at demo scale.
- Codes are not guessable from each other.
- Switching schemes later would only affect new links; issued codes stay valid.
