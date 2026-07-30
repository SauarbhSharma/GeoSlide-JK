@echo off
echo ============================================================
echo   GeoSlide-JK v1.0.0 — Automated Demo Startup Script
echo ============================================================
echo.

echo 1. Starting FastAPI backend on http://127.0.0.1:8000 ...
start /B "GeoSlide FastAPI" "C:\Program Files\Python311\python.exe" -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000

timeout /t 3 /nobreak > NUL

echo 2. Testing backend health endpoint ...
curl -s http://127.0.0.1:8000/api/v1/health
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] FastAPI backend failed to start.
    exit /b 1
)

echo.
echo [SUCCESS] FastAPI backend is online and healthy.
echo.

echo 3. Starting Next.js Web UI on http://127.0.0.1:3000 ...
cd apps\web
start /B "GeoSlide Web UI" npm run dev

echo.
echo ============================================================
echo   GeoSlide-JK v1.0.0 is running!
echo   Frontend: http://127.0.0.1:3000
echo   Backend API: http://127.0.0.1:8000
echo ============================================================
