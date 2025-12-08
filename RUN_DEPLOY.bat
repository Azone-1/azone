@echo off
echo =========================================
echo   Azone Project - Full Deployment
echo =========================================
echo.
echo This will:
echo   1. Upload files to VPS
echo   2. Run deployment script
echo   3. Start PM2 and Nginx
echo.
echo Password will be needed: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(
echo.
pause

powershell.exe -ExecutionPolicy Bypass -NoProfile -File FIX_AND_DEPLOY.ps1

echo.
echo =========================================
echo   Deployment Complete!
echo =========================================
echo.
echo Access your application:
echo   http://paing.xyz
echo   http://18.138.169.114
echo.
pause
