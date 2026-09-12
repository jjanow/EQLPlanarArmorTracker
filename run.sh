#!/usr/bin/env bash
# Launcher for Linux/macOS. Finds a working Python 3 interpreter and runs
# the tracker, forwarding any arguments (e.g. ./run.sh -o report.txt).
set -euo pipefail
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "error: no python3/python found on PATH. Install Python 3.9+ and try again." >&2
    exit 1
fi

exec "$PYTHON" eq_planar_armor.py "$@"
