@echo off
echo =========================================
echo Complete System Check
echo =========================================
echo.

cd /d "%~dp0"

powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "& { Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; . '.\COMPLETE_CHECK.ps1' }"

pause
