#!/usr/bin/env bash
# Deploy the working tree as a new release: copy src, switch "current", restart, health-check.
source "$(dirname "$0")/_env.sh"
BASE="$(date +%Y%m%d%H%M%S)-$(git -C "$ROOT" rev-parse --short HEAD)"
ID="$BASE"; n=1
while [ -e "$DIR/releases/$ID" ]; do ID="$BASE.$n"; n=$((n + 1)); done
mkdir -p "$DIR/releases/$ID"
cp -R "$ROOT/src" "$DIR/releases/$ID/src"
ln -sfn "$DIR/releases/$ID" "$DIR/current"
echo "$ID" >>"$DIR/history"
stop_server
start_server
