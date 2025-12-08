@echo off
echo =========================================
echo Azone Project Deployment
echo =========================================
echo.

cd /d "%~dp0"

echo Step 1: SSH Key Setup...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SETUP_SSH_KEY.ps1"
echo.

timeout /t 3 /nobreak >nul

echo Step 2: Syncing Files...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SYNC_TO_VPS.ps1"
echo.

timeout /t 3 /nobreak >nul

echo Step 3: Deploying...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SIMPLE_DEPLOY.ps1"
echo.

echo =========================================
echo Deployment Complete!
echo =========================================
pause
