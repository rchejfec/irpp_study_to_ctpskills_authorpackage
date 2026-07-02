#!/usr/bin/env bash
# Serve the wired figures over HTTP for local review.
# The figures fetch() their JSON, which browsers block over file:// — so open
# them via this server, not by double-clicking the .html.
#
#   ./figure_data/serve.sh          # serves on :8000
#   ./figure_data/serve.sh 8080     # custom port
#
# Then open  http://localhost:<port>/   (the review index).
set -euo pipefail
PORT="${1:-8000}"
DIST="$(cd "$(dirname "$0")/dist" && pwd)"
echo "Serving $DIST at http://localhost:${PORT}/"
exec python3 -m http.server "$PORT" --directory "$DIST"
