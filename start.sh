#!/usr/bin/env bash
set -e

echo "========================================================="
echo "  ??? FraudShield AI - Starting Services on Render"
echo "========================================================="

# 1. Initialize and seed database if not already seeded
echo "[1/3] Checking database initialization..."
python scripts/seed_database.py || echo "DB initialization skipped or already present."

# 2. Launch FastAPI Backend in background on internal port 8000
echo "[2/3] Launching FastAPI Backend on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait briefly for FastAPI to start
sleep 3

# Trap exit signals to ensure background processes are killed on stop
trap 'kill $BACKEND_PID' EXIT

# 3. Launch Streamlit UI on Render assigned PORT (defaults to 10000 on Render or 8501 locally)
RENDER_PORT="${PORT:-8501}"
echo "[3/3] Launching Streamlit Frontend on port ${RENDER_PORT}..."
streamlit run frontend/app.py \
    --server.port "${RENDER_PORT}" \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false