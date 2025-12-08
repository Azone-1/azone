@echo off
echo =========================================
echo   Quick Fix - Restart Services
echo =========================================
echo.
echo This will restart PM2 and Nginx on VPS
echo NO PASSWORD - uses SSH key only
echo.
pause

powershell.exe -ExecutionPolicy Bypass -NoProfile -File QUICK_FIX.ps1

pause
