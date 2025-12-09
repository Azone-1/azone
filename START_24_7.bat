@echo off
chcp 65001 >nul
title AZone 24/7 Server
color 0B
echo ========================================
echo   AZone 24/7 Keep-Alive Server
echo ========================================
echo.
echo This script will keep the server running 24/7
echo It will automatically restart if the server crashes
echo.
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "RUN_24_7.ps1"

pause

