#!/usr/bin/env sh
set -eu

REPOSITORY="${POTETOS_REPO:-TheOnlyFusionCube/potetos-for-everyone}"
REF="${POTETOS_REF:-main}"
TARGET="${POTETOS_TARGET:-$PWD}"
AGENT="${POTETOS_AGENT:-all}"
ACTION="${POTETOS_ACTION:-auto}"
if [ "$#" -gt 0 ]; then
  case "$1" in
    install|update|uninstall|status|doctor) ACTION="$1"; shift ;;
  esac
fi
SOURCE="${POTETOS_SOURCE_DIR:-}"
TMP=""
EPHEMERAL_SOURCE=0

cleanup() {
  if [ -n "$TMP" ] && [ -d "$TMP" ]; then
    rm -rf "$TMP"
  fi
}
trap cleanup 0 INT TERM

fetch_source() {
  EPHEMERAL_SOURCE=1
  TMP="$(mktemp -d 2>/dev/null || mktemp -d -t potetos)"
  ARCHIVE="$TMP/source.tar.gz"
  URL="https://github.com/$REPOSITORY/archive/$REF.tar.gz"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$URL" -o "$ARCHIVE"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$ARCHIVE" "$URL"
  else
    printf '%s\n' "potetos: curl or wget is required for the one-line installer." >&2
    exit 1
  fi
  mkdir -p "$TMP/src"
  tar -xzf "$ARCHIVE" -C "$TMP/src" --strip-components=1
  SOURCE="$TMP/src"
}

if [ -z "$SOURCE" ]; then
  # When run from a clone, avoid a network round trip.
  SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" 2>/dev/null && pwd || true)"
  if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/bin/potetos" ]; then
    SOURCE="$SCRIPT_DIR"
  else
    fetch_source
  fi
fi

if [ "$ACTION" = "auto" ]; then
  if [ -f "$TARGET/.potetos/install.json" ]; then ACTION="update"; else ACTION="install"; fi
fi

# Prefer Python or Node runner for full feature parity
if command -v python3 >/dev/null 2>&1; then
  RUNNER="python3"
elif command -v python >/dev/null 2>&1; then
  RUNNER="python"
elif command -v node >/dev/null 2>&1; then
  RUNNER="node"
elif command -v bun >/dev/null 2>&1; then
  RUNNER="bun"
else
  RUNNER="sh"
fi

if [ "$RUNNER" = "python3" ] || [ "$RUNNER" = "python" ]; then
  CLI="$SOURCE/bin/potetos"
  case "$ACTION" in
    install)
      "$RUNNER" "$CLI" install --target "$TARGET" --agent "$AGENT" "$@"
      ;;
    update)
      UPDATE_MODE=""
      if [ "$EPHEMERAL_SOURCE" = "1" ]; then UPDATE_MODE="--copy"; fi
      if [ "${POTETOS_FORCE:-0}" = "1" ]; then
        "$RUNNER" "$CLI" update --target "$TARGET" ${UPDATE_MODE:+$UPDATE_MODE} --force "$@"
      else
        "$RUNNER" "$CLI" update --target "$TARGET" ${UPDATE_MODE:+$UPDATE_MODE} "$@"
      fi
      ;;
    uninstall|status|doctor)
      "$RUNNER" "$CLI" "$ACTION" --target "$TARGET" "$@"
      ;;
    *)
      printf '%s\n' "potetos: unknown action: $ACTION" >&2
      exit 2
      ;;
  esac
elif [ "$RUNNER" = "node" ] || [ "$RUNNER" = "bun" ]; then
  CLI="$SOURCE/npm/potetos.mjs"
  case "$ACTION" in
    install)
      "$RUNNER" "$CLI" install --target "$TARGET" --agent "$AGENT" "$@"
      ;;
    update)
      if [ "${POTETOS_FORCE:-0}" = "1" ]; then
        "$RUNNER" "$CLI" update --target "$TARGET" --force "$@"
      else
        "$RUNNER" "$CLI" update --target "$TARGET" "$@"
      fi
      ;;
    uninstall|status|doctor)
      "$RUNNER" "$CLI" "$ACTION" --target "$TARGET" "$@"
      ;;
    *)
      printf '%s\n' "potetos: unknown action: $ACTION" >&2
      exit 2
      ;;
  esac
else
  # Minimal POSIX shell fallback (zero external runtimes required)
  case "$ACTION" in
    install)
      mkdir -p "$TARGET/.agents/skills"
      cp -R "$SOURCE/skills/"* "$TARGET/.agents/skills/"
      mkdir -p "$TARGET/.potetos"
      printf '{\n  "mode": "copy",\n  "skills": ".agents/skills",\n  "installer": "shell"\n}\n' > "$TARGET/.potetos/install.json"
      printf '\n<!-- potetos-for-everyone:begin -->\n## potetos-for-everyone\n\nFor non-trivial engineering work, use the Agent Skill at `.agents/skills/poteto-mode/SKILL.md`.\n<!-- potetos-for-everyone:end -->\n' >> "$TARGET/AGENTS.md"
      printf '%s\n' "installed skills in $TARGET"
      printf '%s\n' "ready: ask your agent to use poteto-mode"
      ;;
    uninstall)
      rm -rf "$TARGET/.agents/skills" "$TARGET/.potetos"
      printf '%s\n' "uninstalled potetos-for-everyone from $TARGET"
      ;;
    *)
      printf '%s\n' "potetos: $ACTION requires Node.js or Python." >&2
      exit 1
      ;;
  esac
fi
