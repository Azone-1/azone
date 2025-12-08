# Complete System Check - All Scripts + VPS
# Run this to check everything at once

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔍 Complete System Check" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 1. SSH Key Check
Write-Host "1. SSH Key Status:" -ForegroundColor Yellow
$SSH_KEY = "$env:USERPROFILE\.ssh\id_ed25519_azone"
if (Test-Path $SSH_KEY) {
    $keyInfo = Get-Item $SSH_KEY
    Write-Host "   ✅ SSH Key exists" -ForegroundColor Green
    Write-Host "   Created: $($keyInfo.CreationTime)" -ForegroundColor White
    Write-Host "   Size: $([math]::Round($keyInfo.Length/1KB, 2)) KB" -ForegroundColor White
} else {
    Write-Host "   ❌ SSH Key NOT found" -ForegroundColor Red
    Write-Host "   -> Run: .\SETUP_SSH_KEY.ps1" -ForegroundColor Yellow
}
Write-Host ""

# 2. SSH Config Check
Write-Host "2. SSH Config:" -ForegroundColor Yellow
$SSH_CONFIG = "$env:USERPROFILE\.ssh\config"
if (Test-Path $SSH_CONFIG) {
    $config = Get-Content $SSH_CONFIG -Raw
    if ($config -match "azone-vps") {
        Write-Host "   ✅ SSH config has azone-vps entry" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  SSH config exists but no azone-vps" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  SSH config not found" -ForegroundColor Yellow
}
Write-Host ""

# 3. Script Syntax Check
Write-Host "3. Script Syntax Check:" -ForegroundColor Yellow
$scripts = @("SETUP_SSH_KEY.ps1", "SYNC_TO_VPS.ps1", "SIMPLE_DEPLOY.ps1", "CHECK_STATUS.ps1", "AUTO_DEPLOY.ps1", "RUN_ALL_SCRIPTS.ps1")
$allOK = $true
foreach ($script in $scripts) {
    if (Test-Path $script) {
        $errors = $null
        try {
            [System.Management.Automation.PSParser]::Tokenize((Get-Content $script -Raw), [ref]$errors)
            if ($errors.Count -eq 0) {
                Write-Host "   ✅ $script" -ForegroundColor Green
            } else {
                Write-Host "   ❌ $script - ERRORS" -ForegroundColor Red
                $allOK = $false
            }
        } catch {
            Write-Host "   ⚠️  $script - Check failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ⚠️  $script - NOT FOUND" -ForegroundColor Yellow
    }
}
Write-Host ""

# 4. VPS Connection Test
Write-Host "4. VPS Connection Test:" -ForegroundColor Yellow
if (Test-Path $SSH_KEY) {
    Write-Host "   Testing passwordless connection..." -ForegroundColor White
    $testCmd = 'echo VPS_OK; pwd'
    $test = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY -o ConnectTimeout=10 Administrator@18.138.169.114 $testCmd 2>&1
    if ($test -match "VPS_OK") {
        Write-Host "   ✅ Passwordless connection WORKS!" -ForegroundColor Green
        $vpsConnected = $true
    } else {
        Write-Host "   ⚠️  Connection issue: $test" -ForegroundColor Yellow
        $vpsConnected = $false
    }
} else {
    Write-Host "   ⚠️  Cannot test - SSH key not found" -ForegroundColor Yellow
    $vpsConnected = $false
}
Write-Host ""

# 5. VPS Files Check
Write-Host "5. VPS Files Status:" -ForegroundColor Yellow
if ($vpsConnected) {
    $vpsFilesCmd = @'
cd ~/Azone 2>/dev/null; echo '===FILES==='; if [ -f web_app.py ]; then echo '✅ web_app.py'; else echo '❌ web_app.py'; fi; if [ -f MASTER_DEPLOY.sh ]; then echo '✅ MASTER_DEPLOY.sh'; else echo '❌ MASTER_DEPLOY.sh'; fi; if [ -d templates ]; then echo '✅ templates/'; else echo '❌ templates/'; fi; if [ -d static ]; then echo '✅ static/'; else echo '❌ static/'; fi
'@
    $vpsFiles = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY -o ConnectTimeout=10 Administrator@18.138.169.114 $vpsFilesCmd 2>&1
    Write-Host $vpsFiles -ForegroundColor Cyan
} else {
    Write-Host "   ⚠️  Cannot check - VPS not connected" -ForegroundColor Yellow
}
Write-Host ""

# 6. VPS Deployment Status
Write-Host "6. VPS Deployment Status:" -ForegroundColor Yellow
if ($vpsConnected) {
    $vpsDeployCmd = @'
if pm2 list 2>/dev/null | head -3; then true; else echo 'PM2 not running'; fi; echo ''; if sudo systemctl status nginx --no-pager 2>/dev/null | head -2; then true; else echo 'Nginx not running'; fi
'@
    $vpsDeploy = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY -o ConnectTimeout=10 Administrator@18.138.169.114 $vpsDeployCmd 2>&1
    Write-Host $vpsDeploy -ForegroundColor Cyan
} else {
    Write-Host "   ⚠️  Cannot check - VPS not connected" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "📋 Summary & Next Steps" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Re-check SSH_KEY for summary (ensure variable is set)
$SSH_KEY_CHECK = "$env:USERPROFILE\.ssh\id_ed25519_azone"
if (Test-Path $SSH_KEY_CHECK) {
    Write-Host "✅ SSH Key: EXISTS" -ForegroundColor Green
    Write-Host "   -> SETUP_SSH_KEY.ps1 - SKIP" -ForegroundColor Cyan
} else {
    Write-Host "❌ SSH Key: NOT FOUND" -ForegroundColor Red
    Write-Host "   -> Run: .\SETUP_SSH_KEY.ps1" -ForegroundColor Yellow
}

if ($vpsConnected) {
    Write-Host "✅ VPS Connection: WORKING" -ForegroundColor Green
    Write-Host "   -> Can run SYNC and DEPLOY without password" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  VPS Connection: NEEDS PASSWORD" -ForegroundColor Yellow
    Write-Host "   -> Will need password for SYNC and DEPLOY" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
if (Test-Path $SSH_KEY_CHECK) {
    Write-Host "   1. .\SYNC_TO_VPS.ps1  (Upload files)" -ForegroundColor White
    Write-Host "   2. .\SIMPLE_DEPLOY.ps1  (Deploy)" -ForegroundColor White
} else {
    Write-Host "   1. .\SETUP_SSH_KEY.ps1  (Setup SSH key first)" -ForegroundColor White
    Write-Host "   2. .\SYNC_TO_VPS.ps1  (Upload files)" -ForegroundColor White
    Write-Host "   3. .\SIMPLE_DEPLOY.ps1  (Deploy)" -ForegroundColor White
}
Write-Host ""
