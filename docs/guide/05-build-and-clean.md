# 5. Build and clean

Build the smallest end-to-end slice that produces the requested outcome. Prefer deletion, direct data shapes, and migration of callers over compatibility scaffolding that becomes permanent by accident.

Use `tdd` when a cheap behavior-level failing test exists. Use `no-comments` before review to remove comments that only narrate syntax; encode durable constraints in types, tests, assertions, lints, or structure when possible.
