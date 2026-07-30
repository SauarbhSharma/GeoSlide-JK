#!/bin/bash
set -e

PORT="${PORT:-10000}"

echo "=== GeoSlide-JK Production Startup ==="
echo "PORT=$PORT"

# Start FastAPI backend on internal port 8000
cd /app
python -m uvicorn apps.api.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --workers 1 \
  --log-level warning &

FASTAPI_PID=$!
echo "FastAPI started (PID=$FASTAPI_PID) on 127.0.0.1:8000"

# Wait for FastAPI to be ready (up to 30 seconds)
for i in $(seq 1 30); do
  if curl -sf http://127.0.0.1:8000/api/v1/health > /dev/null 2>&1; then
    echo "FastAPI is ready"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "WARNING: FastAPI health check timed out, starting Next.js anyway"
  fi
  sleep 1
done

# Graceful shutdown handler
cleanup() {
  echo "Shutting down..."
  kill $FASTAPI_PID 2>/dev/null || true
  wait $FASTAPI_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGTERM SIGINT

# Start Next.js standalone server on the public PORT
cd /app/apps/web
HOSTNAME="0.0.0.0" PORT="$PORT" exec node server.js
