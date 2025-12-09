@echo off
chcp 65001 >nul
title Push to GitHub - AZone
color 0B
echo ========================================
echo   Push AZone Files to GitHub
echo ========================================
echo.
cd /d "%~dp0"

echo [1/3] Adding all files...
git add .
echo.

echo [2/3] Committing changes...
git commit -m "Update AZone files - %date% %time%"
echo.

echo [3/3] Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo   Done! Railway will auto-deploy
echo ========================================
pause
