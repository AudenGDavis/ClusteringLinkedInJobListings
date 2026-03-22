#!/usr/bin/env bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

command="${1:-}"
shift || true

case "$command" in
  format)
    exec "$PYTHON_BIN" src/format.py "$@"
    ;;
  wordset)
    exec "$PYTHON_BIN" src/wordset.py "$@"
    ;;
  trimwordset)
    exec "$PYTHON_BIN" src/trimwordset.py "$@"
    ;;
  vectorize)
    exec "$PYTHON_BIN" src/vectorize.py "$@"
    ;;
  cluster)
    exec "$PYTHON_BIN" src/cluster.py "$@"
    ;;
  "")
    echo "Usage: ./manager.sh {format|wordset|trimwordset|vectorize|cluster} [args...]" >&2
    exit 1
    ;;
  *)
    echo "Unknown command: $command" >&2
    echo "Usage: ./manager.sh {format|wordset|trimwordset|vectorize|cluster} [args...]" >&2
    exit 1
    ;;
esac
