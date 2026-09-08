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

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    printf '%s\n' python3
  elif command -v python >/dev/null 2>&1; then
    printf '%s\n' python
  else
    printf '%s\n' "potetos: Python 3 is required." >&2
    exit 1
  fi
}

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

PYTHON="$(find_python)"
if [ ! -f "$SOURCE/bin/potetos" ]; then
  printf '%s\n' "potetos: invalid source directory: $SOURCE" >&2
  exit 1
fi

if [ "$ACTION" = "auto" ]; then
  if [ -f "$TARGET/.potetos/install.json" ]; then ACTION="update"; else ACTION="install"; fi
fi

case "$ACTION" in
  install)
    "$PYTHON" "$SOURCE/bin/potetos" install --target "$TARGET" --agent "$AGENT" "$@"
    ;;
  update)
    UPDATE_MODE=""
    if [ "$EPHEMERAL_SOURCE" = "1" ]; then UPDATE_MODE="--copy"; fi
    if [ "${POTETOS_FORCE:-0}" = "1" ]; then
      "$PYTHON" "$SOURCE/bin/potetos" update --target "$TARGET" ${UPDATE_MODE:+$UPDATE_MODE} --force "$@"
    else
      "$PYTHON" "$SOURCE/bin/potetos" update --target "$TARGET" ${UPDATE_MODE:+$UPDATE_MODE} "$@"
    fi
    ;;
  uninstall|status|doctor)
    "$PYTHON" "$SOURCE/bin/potetos" "$ACTION" --target "$TARGET" "$@"
    ;;
  *)
    printf '%s\n' "potetos: unknown bootstrap action: $ACTION" >&2
    exit 2
    ;;
esac
