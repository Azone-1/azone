@echo off
echo =========================================
echo   Setup SSH Key First - NO MORE PASSWORDS!
echo =========================================
echo.
echo This will setup SSH key so you don't need
echo to type password every time!
echo.
echo Password (enter ONCE): IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(
echo.
pause

powershell.exe -ExecutionPolicy Bypass -NoProfile -File SETUP_SSH_KEY.ps1

echo.
echo =========================================
echo   SSH Key Setup Complete!
echo =========================================
echo.
echo Now run: .\DEPLOY_SIMPLE.bat
echo (NO password needed anymore!)
echo.
pause
