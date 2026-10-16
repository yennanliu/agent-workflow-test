---
name: codebase-design
description: Shape modules and interfaces as deep modules with small interfaces. Use when designing an API, a module boundary or an interface, or when restructuring code.
---

Design **deep modules**: a small interface over a large amount of hidden work. A caller should need to know little to use a module well.

- **Interface size.** Prefer fewer, more general calls. A call that only forwards to another call is a shallow layer; fold it in.
- **Information hiding.** Each design decision (storage format, retry policy, third-party SDK) lives inside one module. Changing it touches that module alone.
- **Seams.** Put module boundaries where you want to test or swap an implementation: the database, the network, the clock, a vendor. Each seam is one interface with one real and one test implementation.
- **Errors.** Define them out of existence where you can (idempotent writes, defaults for absent values). Report the rest in the caller's terms, not the dependency's.
- **Names.** Use the terms from `GLOSSARY.md`. A module name that needs "and" is two modules.

Done when every interface call has one owning module, each hidden decision lives in exactly one module, and each external dependency sits behind a seam.
