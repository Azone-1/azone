@echo off
echo =========================================
echo   Simple Deployment - Azone Project
echo =========================================
echo.
echo Password: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(
echo.
echo Using SINGLE SESSION - password asked ONLY ONCE!
echo Just copy and paste the password above when asked
echo IMPORTANT: Keep VPN ON during entire deployment!
echo.
pause

powershell.exe -ExecutionPolicy Bypass -NoProfile -File DEPLOY_SINGLE_SESSION.ps1

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
