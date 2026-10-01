#!/usr/bin/env sh
# Pull the latest code from GitHub and (re)build/restart only this project's container.
set -e
cd "$(dirname "$0")"
[ -f .env ] || cp .env.example .env
PORT=$(grep -E '^OMR_HOST_PORT=' .env | cut -d= -f2)
PORT=${PORT:-8510}

git pull --ff-only

# refuse to start if the port is taken by something other than this project
if ! docker ps --filter name=^institute-omr$ --format '{{.Ports}}' | grep -q ":$PORT->"; then
  if ss -ltn 2>/dev/null | awk '{print $4}' | grep -qE "[:.]$PORT$"; then
    echo "Port $PORT is already in use. Set another OMR_HOST_PORT in .env" >&2
    exit 1
  fi
fi

docker compose up -d --build
docker compose ps
echo "OMR is running on http://$(hostname -I 2>/dev/null | awk '{print $1}'):$PORT"
