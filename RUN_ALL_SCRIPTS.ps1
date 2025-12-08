# Run All Deployment Scripts
# This script runs all 3 steps sequentially

$ErrorActionPreference = "Continue"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Complete Deployment Workflow" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH Key
$SSH_KEY = "$env:USERPROFILE\.ssh\id_ed25519_azone"
if (Test-Path $SSH_KEY) {
    Write-Host "✅ SSH Key exists - Passwordless access available" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⚠️  SSH Key not found - Running setup..." -ForegroundColor Yellow
    Write-Host "   Password will be: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(" -ForegroundColor Cyan
    Write-Host ""
    
    # Step 1: SSH Key Setup
    Write-Host "Step 1: SSH Key Setup" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    & ".\SETUP_SSH_KEY.ps1"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  SSH key setup had issues" -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds 3
    Write-Host ""
}

# Step 2: Sync Files
Write-Host "Step 2: Syncing Files to VPS" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Cyan
& ".\SYNC_TO_VPS.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  File sync had issues" -ForegroundColor Yellow
}

Start-Sleep -Seconds 3
Write-Host ""

# Step 3: Deploy
Write-Host "Step 3: Deploying to VPS" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Cyan
& ".\SIMPLE_DEPLOY.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Deployment had issues" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ All Scripts Executed!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your application:" -ForegroundColor Green
Write-Host "   http://paing.xyz" -ForegroundColor White
Write-Host "   http://18.138.169.114" -ForegroundColor White
Write-Host ""
