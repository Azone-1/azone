# Simple Deployment Starter
# Copy and paste this entire block into PowerShell

$ErrorActionPreference = "Continue"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Azone Deployment - Starting..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1
Write-Host "Step 1: SSH Key Setup" -ForegroundColor Yellow
Write-Host "Password will be: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(" -ForegroundColor Cyan
Write-Host ""
& "$PSScriptRoot\SETUP_SSH_KEY.ps1"

Start-Sleep -Seconds 3

# Step 2
Write-Host ""
Write-Host "Step 2: Syncing Files" -ForegroundColor Yellow
& "$PSScriptRoot\SYNC_TO_VPS.ps1"

Start-Sleep -Seconds 3

# Step 3
Write-Host ""
Write-Host "Step 3: Deploying" -ForegroundColor Yellow
& "$PSScriptRoot\SIMPLE_DEPLOY.ps1"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
