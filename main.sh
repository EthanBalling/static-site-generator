#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"
python3 src/main.py
cd docs
exec python3 -m http.server 8888
