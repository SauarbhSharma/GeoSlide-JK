@echo off
echo ============================================================
echo   GeoSlide-JK v1.0.0 — Stopping Demo Services
echo ============================================================
echo.

taskkill /F /IM node.exe /T 2>NUL
taskkill /F /FI "WINDOWTITLE eq GeoSlide*" 2>NUL
powershell -Command "Get-Process -Name python,uvicorn -ErrorAction SilentlyContinue | Stop-Process -Force"

echo [SUCCESS] Demo services stopped.
