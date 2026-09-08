# 6. Verify and ship

Completion means proof against the requested surface, not merely a plausible diff. Unit tests prove unit behavior; a compile proves compilation; neither automatically proves UI, service, device, or workflow behavior.

Use `interrogate` for adversarial review, `blast-radius` to prove what else can be affected, and `shipping` when a verified PR/stack is meant to land. Freeze the exact revision being judged and report the actual commands, artifacts, and unavailable verification surfaces.
