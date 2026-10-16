#!/usr/bin/env bash
# Restart the current release without changing it (used by the e2e restart journey).
source "$(dirname "$0")/_env.sh"
stop_server
start_server
