# Shared settings for deploy, rollback and restart. Only "staging" exists in this demo.
set -euo pipefail
ENV_NAME="${1:-}"
[ "$ENV_NAME" = "staging" ] || { echo "usage: $0 staging" >&2; exit 2; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/.deploy/$ENV_NAME"
PORT=8081
HEALTH="http://127.0.0.1:$PORT/healthz"
mkdir -p "$DIR/releases"

stop_server() {
  if [ -f "$DIR/pid" ] && kill -0 "$(cat "$DIR/pid")" 2>/dev/null; then
    kill "$(cat "$DIR/pid")"
    for _ in $(seq 50); do kill -0 "$(cat "$DIR/pid")" 2>/dev/null || break; sleep 0.1; done
  fi
  rm -f "$DIR/pid"
}

start_server() {
  PYTHONPATH="$DIR/current/src" nohup python3 -m shorty --host 127.0.0.1 --port "$PORT" \
    --db "$DIR/shorty.db" --base-url "http://127.0.0.1:$PORT" >>"$DIR/server.log" 2>&1 &
  echo $! >"$DIR/pid"
  for _ in $(seq 50); do curl -fsS "$HEALTH" >/dev/null 2>&1 && { echo "healthy: $(readlink "$DIR/current")"; return 0; }; sleep 0.1; done
  echo "health check failed; see $DIR/server.log" >&2
  return 1
}
