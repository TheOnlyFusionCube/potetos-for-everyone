#!/usr/bin/env sh
set -eu

# Keep skills and commands available without adding automatic session context.
if [ "${POTETOS_AUTO_ACTIVATE:-1}" = "0" ]; then
  exit 0
fi

cat "${CLAUDE_PLUGIN_ROOT}/hooks/session-start-context.md"
