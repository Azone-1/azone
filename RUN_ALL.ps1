# Run All Deployment Scripts - Bypass Execution Policy
# This script runs all 3 steps with proper execution policy

$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Complete Deployment Workflow" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: SSH Key Setup
Write-Host "Step 1: Setting up SSH key..." -ForegroundColor Yellow
& powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SETUP_SSH_KEY.ps1"

if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
    Write-Host "⚠️  SSH key setup had issues, but continuing..." -ForegroundColor Yellow
}

Start-Sleep -Seconds 3

# Step 2: Sync Files
Write-Host ""
Write-Host "Step 2: Syncing files to VPS..." -ForegroundColor Yellow
& powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SYNC_TO_VPS.ps1"

Start-Sleep -Seconds 3

# Step 3: Deploy
Write-Host ""
Write-Host "Step 3: Deploying to VPS..." -ForegroundColor Yellow
& powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SIMPLE_DEPLOY.ps1"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ All Steps Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
