#!/usr/bin/env bash
# Point "current" back at the previous release and restart. The SQLite file is kept.
source "$(dirname "$0")/_env.sh"
[ "$(wc -l <"$DIR/history" 2>/dev/null || echo 0)" -ge 2 ] || { echo "no previous release to roll back to" >&2; exit 1; }
sed -i.bak '$d' "$DIR/history" && rm -f "$DIR/history.bak"
ln -sfn "$DIR/releases/$(tail -n 1 "$DIR/history")" "$DIR/current"
stop_server
start_server
