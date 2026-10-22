#!/bin/bash
# CoSight — stop backend and frontend

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$SCRIPT_DIR/.pids"

stop_pid() {
  local name=$1 file=$2
  if [ -f "$PID_DIR/$file" ]; then
    pid=$(cat "$PID_DIR/$file")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      echo "Stopped $name (PID $pid)"
    fi
    rm -f "$PID_DIR/$file"
  fi
}

stop_pid "backend" "backend.pid"
stop_pid "frontend" "frontend.pid"
