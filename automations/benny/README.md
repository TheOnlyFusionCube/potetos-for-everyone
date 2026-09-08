# Benny, portable pack

Benny is an optional issue-report automation pattern adapted from the Benny pack in Lauren Tan's pstack. Upstream wires it to Cursor automations and Slack. This version keeps the two-stage workflow but does not assume either product:

1. `triage-issue-reports` classifies and validates incoming reports.
2. `reproduce-and-fix-issues` reproduces confirmed defects and may prepare a small draft fix.

A host may trigger these from Slack, GitHub Issues, Linear, email, a webhook queue, or a human prompt. Keep source credentials and routing outside this pack. Always reply in the originating thread/ticket when the host exposes one.

This pack is dormant by default and is not installed with the main 47 skills.
