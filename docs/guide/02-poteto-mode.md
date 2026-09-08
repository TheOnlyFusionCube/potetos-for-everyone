# 2. Poteto Mode

`poteto-mode` is the front door. It classifies a task into a playbook, copies that playbook's steps into whatever task-tracking mechanism exists, and progressively loads supporting skills.

A useful prompt is outcome-first:

```text
Use poteto-mode. Reproduce the idle scroll drift, fix the root cause with the smallest change, and prove the real UI no longer moves while idle.
```

Do not manually invoke every principle. The router loads a principle only when it changes a concrete decision. This protects context and keeps rigor from becoming ceremony.
