@echo off
chcp 65001 >nul
title AZone Flask Server
color 0A
echo ========================================
echo   AZone Flask Server Starting...
echo ========================================
echo.
cd /d "%~dp0"
echo Current Directory: %CD%
echo.
echo Checking Python...
python --version
echo.
echo Starting Flask server...
echo.
echo ========================================
echo   Server will start at: http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ========================================
echo.
python web_app.py
pause
