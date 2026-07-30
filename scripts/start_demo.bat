@echo off
echo ============================================================
echo   GeoSlide-JK v1.0.0 — Automated Demonstration Startup
echo ============================================================
echo.

echo 1. Starting FastAPI backend on http://127.0.0.1:8000 ...
start /B "GeoSlide FastAPI" "C:\Program Files\Python311\python.exe" -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000

ping 127.0.0.1 -n 4 > NUL

echo 2. Verifying backend health endpoint ...
powershell -Command "try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/health' -TimeoutSec 5; if ($res.status -eq 'healthy') { exit 0 } else { exit 1 } } catch { exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] FastAPI backend failed to start or health check failed.
    exit /b 1
)
echo [SUCCESS] FastAPI backend is online and healthy.
echo.

echo 3. Checking Next.js production build status ...
if not exist "apps\web\.next" (
    echo Production build not found. Compiling Next.js production bundle...
    cd apps\web
    call npm run build
    cd ..\..
)

echo 4. Starting Next.js Production Web Server on http://127.0.0.1:3000 ...
cd apps\web
start /B "GeoSlide Web UI Production" npm run start -- -p 3000 -H 127.0.0.1
cd ..\..

ping 127.0.0.1 -n 5 > NUL

echo 5. Verifying Next.js frontend health ...
powershell -Command "try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:3000' -UseBasicParsing -TimeoutSec 5; if ($res.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Next.js frontend is starting up.
)

echo.
echo ============================================================
echo   GeoSlide-JK v1.0.0 Demonstration Application Active!
echo   Frontend:    http://127.0.0.1:3000
echo   Backend API: http://127.0.0.1:8000
echo ============================================================
