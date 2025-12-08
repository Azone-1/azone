# Check Deployment Status
# Run this to see what's already done and what needs to be done

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "📊 Deployment Status Check" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH Key
$SSH_KEY = "$env:USERPROFILE\.ssh\id_ed25519_azone"
Write-Host "1. SSH Key:" -ForegroundColor Yellow
if (Test-Path $SSH_KEY) {
    Write-Host "   ✅ SSH Key exists" -ForegroundColor Green
    Write-Host "   ✅ SETUP_SSH_KEY.ps1 - ALREADY DONE!" -ForegroundColor Green
    Write-Host "   → You can SKIP Step 1" -ForegroundColor Cyan
} else {
    Write-Host "   ❌ SSH Key not found" -ForegroundColor Red
    Write-Host "   → Need to run: .\SETUP_SSH_KEY.ps1" -ForegroundColor Yellow
}
Write-Host ""

# Check SSH Config
Write-Host "2. SSH Config:" -ForegroundColor Yellow
$SSH_CONFIG = "$env:USERPROFILE\.ssh\config"
if (Test-Path $SSH_CONFIG) {
    $config = Get-Content $SSH_CONFIG -Raw
    if ($config -match "azone-vps") {
        Write-Host "   ✅ SSH config configured" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  SSH config exists but incomplete" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  SSH config not found" -ForegroundColor Yellow
}
Write-Host ""

# Test Passwordless Connection
Write-Host "3. Passwordless Connection Test:" -ForegroundColor Yellow
if (Test-Path $SSH_KEY) {
    Write-Host "   Testing connection..." -ForegroundColor White
    $test = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY -o ConnectTimeout=5 Administrator@18.138.169.114 "echo TEST_OK" 2>&1
    if ($test -match "TEST_OK") {
        Write-Host "   ✅ Passwordless connection WORKS!" -ForegroundColor Green
        Write-Host "   → You can SKIP password entry for SYNC and DEPLOY" -ForegroundColor Cyan
    } else {
        Write-Host "   ⚠️  Passwordless connection not working" -ForegroundColor Yellow
        Write-Host "   → May need to re-run SETUP_SSH_KEY.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Cannot test - SSH key not found" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "📋 What to Do Next:" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $SSH_KEY) {
    Write-Host "✅ Step 1 (SSH Key) - ALREADY DONE" -ForegroundColor Green
    Write-Host "   → Skip SETUP_SSH_KEY.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "   1. .\SYNC_TO_VPS.ps1  (Upload files)" -ForegroundColor White
    Write-Host "   2. .\SIMPLE_DEPLOY.ps1  (Deploy)" -ForegroundColor White
} else {
    Write-Host "❌ Step 1 (SSH Key) - NEED TO DO" -ForegroundColor Red
    Write-Host "   → Run: .\SETUP_SSH_KEY.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Then:" -ForegroundColor Yellow
    Write-Host "   1. .\SYNC_TO_VPS.ps1  (Upload files)" -ForegroundColor White
    Write-Host "   2. .\SIMPLE_DEPLOY.ps1  (Deploy)" -ForegroundColor White
}
Write-Host ""
