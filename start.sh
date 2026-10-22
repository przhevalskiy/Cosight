#!/bin/bash
# CoSight — start backend (8000) and frontend (5173)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
PID_DIR="$SCRIPT_DIR/.pids"
LOG_DIR="$SCRIPT_DIR/logs"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

mkdir -p "$PID_DIR" "$LOG_DIR"

if [ ! -f "$BACKEND_DIR/.env" ]; then
  echo "Copy backend/.env.example to backend/.env and configure credentials."
  exit 1
fi

if [ ! -f "$FRONTEND_DIR/.env" ]; then
  echo "VITE_API_URL=http://localhost:8000" > "$FRONTEND_DIR/.env"
fi

echo -e "${BLUE}Starting CoSight backend...${NC}"
cd "$BACKEND_DIR"
if [ ! -d venv ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi
nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 >> "$LOG_DIR/backend.log" 2>&1 &
echo $! > "$PID_DIR/backend.pid"

echo -e "${BLUE}Starting CoSight frontend...${NC}"
cd "$FRONTEND_DIR"
[ -d node_modules ] || npm install
nohup npm run dev -- --host 127.0.0.1 >> "$LOG_DIR/frontend.log" 2>&1 &
echo $! > "$PID_DIR/frontend.pid"

sleep 2
echo -e "${GREEN}CoSight backend:  http://localhost:8000${NC}"
echo -e "${GREEN}CoSight frontend: http://localhost:5173${NC}"
echo "Logs: $LOG_DIR/"
