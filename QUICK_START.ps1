# Quick Start - Fixed Version
# Copy and paste this entire block into PowerShell

cd C:\Users\User\Desktop\Azone
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Azone Deployment - Quick Start" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: SSH Key
Write-Host "Step 1: SSH Key Setup" -ForegroundColor Yellow
Write-Host "Password: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(" -ForegroundColor Cyan
Write-Host ""
& ".\SETUP_SSH_KEY.ps1"

Start-Sleep -Seconds 3

# Step 2: Sync
Write-Host ""
Write-Host "Step 2: Syncing Files" -ForegroundColor Yellow
& ".\SYNC_TO_VPS.ps1"

Start-Sleep -Seconds 3

# Step 3: Deploy
Write-Host ""
Write-Host "Step 3: Deploying" -ForegroundColor Yellow
& ".\SIMPLE_DEPLOY.ps1"

Write-Host ""
Write-Host "✅ Complete!" -ForegroundColor Green
