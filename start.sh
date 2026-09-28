#!/usr/bin/env bash
set -e

echo "========================================================="
echo "  FraudShield AI - Starting FastAPI Backend on Render"
echo "========================================================="

# 1. Initialize and seed database if not already seeded
echo "[1/2] Checking database initialization..."
python scripts/seed_database.py || echo "DB initialization skipped or already present."

# 2. Launch FastAPI on Render's assigned public PORT
#    Render sets $PORT automatically (default 10000).
#    This makes the API reachable at https://<service>.onrender.com/api/v1/...
RENDER_PORT="${PORT:-8000}"
echo "[2/2] Launching FastAPI Backend on port ${RENDER_PORT}..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${RENDER_PORT}" \
    --workers 1
