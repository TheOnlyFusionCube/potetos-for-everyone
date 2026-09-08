# 7. Long autonomous runs

Use `autonomous-run` for a bounded long task and `orchestrate` for a standing multi-slice project. Define the completion predicate, irreversible-action boundary, and proof for every work unit before starting.

Maintain a durable decision trail with `show-me-your-work`. Recompute the queue after evidence changes. A host without background execution cannot literally continue after the session ends; the playbook still produces resumable checkpoints and a precise `session-pickup` handoff instead of claiming otherwise.
