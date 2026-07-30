#!/bin/bash
set -e

PORT="${PORT:-10000}"
FASTAPI_LOG="/tmp/fastapi.log"

echo "=== GeoSlide-JK Production Startup Supervisor ==="
echo "PORT=$PORT"

# 1. Start FastAPI background process on internal 127.0.0.1:8000
cd /app
python -u -m uvicorn apps.api.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --log-level info > "$FASTAPI_LOG" 2>&1 &

FASTAPI_PID=$!
echo "FastAPI started (PID=$FASTAPI_PID) on 127.0.0.1:8000"

NEXTJS_PID=""

# Signal trapping for clean two-process shutdown
cleanup() {
  echo "Received termination signal. Shutting down processes..."
  if [ -n "$FASTAPI_PID" ] && kill -0 "$FASTAPI_PID" 2>/dev/null; then
    echo "Stopping FastAPI (PID $FASTAPI_PID)..."
    kill -TERM "$FASTAPI_PID" 2>/dev/null || true
  fi
  if [ -n "$NEXTJS_PID" ] && kill -0 "$NEXTJS_PID" 2>/dev/null; then
    echo "Stopping Next.js (PID $NEXTJS_PID)..."
    kill -TERM "$NEXTJS_PID" 2>/dev/null || true
  fi
  wait "$FASTAPI_PID" 2>/dev/null || true
  wait "$NEXTJS_PID" 2>/dev/null || true
  exit 0
}
trap cleanup SIGTERM SIGINT

# 2. Poll FastAPI readiness (up to 90 seconds)
echo "Polling FastAPI readiness at http://127.0.0.1:8000/api/v1/health..."
FASTAPI_READY=0

for i in $(seq 1 90); do
  # Verify FastAPI process hasn't crashed
  if ! kill -0 "$FASTAPI_PID" 2>/dev/null; then
    echo "ERROR: FastAPI process (PID $FASTAPI_PID) exited prematurely!"
    echo "=== FastAPI Startup Error Logs ==="
    cat "$FASTAPI_LOG"
    exit 1
  fi

  # Check health endpoint
  if curl -sf http://127.0.0.1:8000/api/v1/health > /dev/null 2>&1; then
    echo "FastAPI health check PASSED (HTTP 200) after ${i}s"
    FASTAPI_READY=1
    break
  fi

  sleep 1
done

if [ "$FASTAPI_READY" -ne 1 ]; then
  echo "ERROR: FastAPI health check timed out after 90 seconds!"
  echo "=== FastAPI Log Output ==="
  cat "$FASTAPI_LOG"
  kill -9 "$FASTAPI_PID" 2>/dev/null || true
  exit 1
fi

echo "=== FastAPI Initial Startup Output ==="
cat "$FASTAPI_LOG"

# 3. Start Next.js standalone server on public PORT
echo "Starting Next.js standalone server on HOSTNAME=0.0.0.0 PORT=$PORT..."
cd /app/apps/web
HOSTNAME="0.0.0.0" PORT="$PORT" node server.js &
NEXTJS_PID=$!

echo "Next.js standalone server running with PID $NEXTJS_PID"

# Tail FastAPI logs in background so container stdout captures ongoing API logs
tail -f "$FASTAPI_LOG" &
TAIL_PID=$!

# Wait for Next.js process to complete
wait "$NEXTJS_PID"
