#!/usr/bin/env sh
set -eu

REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
NAME="bronto"
WRAPPER="$REPO_ROOT/scripts/bronto-mcp"

ensure_env() {
  if [ ! -f "$REPO_ROOT/.env" ]; then
    echo "Missing $REPO_ROOT/.env"
    echo ""
    echo "Create it from the template:"
    echo "  cp .env.example .env"
    echo "  \${EDITOR:-nano} .env"
    exit 1
  fi

  if grep -q "<YOUR_API_KEY>" "$REPO_ROOT/.env"; then
    echo ".env still contains template values."
    echo "Open .env and set BRONTO_API_KEY before running install."
    exit 1
  fi

  if grep -q '^BRONTO_API_KEY=$' "$REPO_ROOT/.env"; then
    echo "BRONTO_API_KEY is empty in .env"
    exit 1
  fi

  if grep -q '^BRONTO_API_ENDPOINT=$' "$REPO_ROOT/.env"; then
    echo "BRONTO_API_ENDPOINT is empty in .env"
    exit 1
  fi
}

ensure_deps() {
  if command -v uv >/dev/null 2>&1; then
    (cd "$REPO_ROOT" && uv sync)
    return
  fi

  if [ ! -d "$REPO_ROOT/.venv" ]; then
    python3 -m venv "$REPO_ROOT/.venv"
  fi

  "$REPO_ROOT/.venv/bin/python" -m pip install -r "$REPO_ROOT/requirements.txt"
  "$REPO_ROOT/.venv/bin/python" -m pip install -e "$REPO_ROOT"
}

install_claude() {
  if ! command -v claude >/dev/null 2>&1; then
    echo "claude CLI not found. Install Claude Code first."
    exit 1
  fi

  claude mcp remove "$NAME" >/dev/null 2>&1 || true
  claude mcp add --transport stdio "$NAME" -- "$WRAPPER"
  echo "Added MCP server '$NAME' to Claude Code."
}

install_codex() {
  if ! command -v codex >/dev/null 2>&1; then
    echo "codex CLI not found. Install Codex first."
    exit 1
  fi

  CFG_DIR="$HOME/.codex"
  CFG="$CFG_DIR/config.toml"
  mkdir -p "$CFG_DIR"
  touch "$CFG"

  tmp="$(mktemp)"
  awk -v name="$NAME" '
    BEGIN { skip=0 }
    $0 ~ "^\\[mcp_servers\\." name "\\]$" { skip=1; next }
    skip && $0 ~ "^\\[mcp_servers\\." { skip=0 }
    !skip { print }
  ' "$CFG" > "$tmp"
  mv "$tmp" "$CFG"

  cat >> "$CFG" <<EOF

[mcp_servers.$NAME]
command = "$WRAPPER"
args = []
EOF

  echo "Added MCP server '$NAME' to Codex config at $CFG."
}

usage() {
  echo "Usage:"
  echo "  ./install.sh claude   # install deps + add to Claude Code"
  echo "  ./install.sh codex    # install deps + add to Codex"
  echo "  ./install.sh all      # both"
  echo ""
  echo "Setup:"
  echo "  cp .env.example .env"
  echo "  \${EDITOR:-nano} .env"
  echo "  Set BRONTO_API_KEY and BRONTO_API_ENDPOINT"
}

main() {
  if [ ! -x "$WRAPPER" ]; then
    echo "Wrapper not executable: $WRAPPER"
    echo "Run: chmod +x scripts/bronto-mcp"
    exit 1
  fi

  case "${1:-}" in
    claude)
      ensure_env
      ensure_deps
      install_claude
      ;;
    codex)
      ensure_env
      ensure_deps
      install_codex
      ;;
    all)
      ensure_env
      ensure_deps
      install_claude
      install_codex
      ;;
    *)
      usage
      exit 2
      ;;
  esac
}

main "$@"
