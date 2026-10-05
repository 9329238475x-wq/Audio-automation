@echo off
setlocal enabledelayedexpansion
title Pocket FM Studio - YouTube Automation Hub
cd /d "%~dp0"

echo ========================================================
echo   🎙️ Starting Pocket FM Studio YouTube Hub Server
echo ========================================================
echo.
echo [1/2] Opening browser at http://localhost:8000/ ...
start "Studio Browser" cmd /c "timeout /t 2 >nul & start http://localhost:8000/"

echo [2/2] Starting local authentication & upload server...
python -m uvicorn web_server:app --host 127.0.0.1 --port 8000

pause
