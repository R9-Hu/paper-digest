#!/usr/bin/env bash
# Daily entry point for the paper digest meta-harness (invoked by cron at 08:00).
# Runs the full pipeline: fetch -> digest -> trends -> publish.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Load local secrets (e.g. SEMANTIC_SCHOLAR_API_KEY) if present. Gitignored;
# covers manual runs as well as systemd (which also reads it via EnvironmentFile).
if [[ -f "$PROJECT_DIR/.env" ]]; then
  set -a; source "$PROJECT_DIR/.env"; set +a
fi

# Ensure CLIs used by sub-stages are on PATH under cron's minimal env.
export PATH="$HOME/.nvm/versions/node/v20.19.6/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

mkdir -p logs
echo "=== $(date -Iseconds) starting paper digest ==="
exec ./.venv/bin/python -m harness.orchestrate "$@"
