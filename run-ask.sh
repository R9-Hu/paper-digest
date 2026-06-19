#!/usr/bin/env bash
# Launch the local Ask-Claude bridge: (re)build the site, then serve it with an
# /ask endpoint backed by `claude -p` (your Claude subscription). Self-use only —
# do not expose this port publicly.
#
#   ./run-ask.sh                 # rebuild from the DB, serve on :8765
#   ./run-ask.sh --port 9000     # custom port (skips DB rebuild; just builds HTML)
#
# Then open the printed http://localhost:<port>/ and click '✦ Ask Claude' on a paper.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Load local secrets (e.g. SEMANTIC_SCHOLAR_API_KEY) if present.
if [[ -f "$PROJECT_DIR/.env" ]]; then
  set -a; source "$PROJECT_DIR/.env"; set +a
fi

# Ensure the claude CLI (and node) are on PATH.
export PATH="$HOME/.nvm/versions/node/v20.19.6/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

mkdir -p logs
# No args → refresh the site from the DB so the newest digests show.
if [[ $# -eq 0 ]]; then set -- --rebuild; fi

exec ./.venv/bin/python -m harness.ask_server "$@"
