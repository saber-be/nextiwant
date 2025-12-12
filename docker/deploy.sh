#!/usr/bin/env bash
set -e

# Determine project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

cd "${PROJECT_ROOT}"

echo "[deploy] Pulling latest code..."
git pull

echo "[deploy] Applying docker compose (prod overlay)..."
cd "${SCRIPT_DIR}"

docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

echo "[deploy] Done. Current services:"
docker compose ps
