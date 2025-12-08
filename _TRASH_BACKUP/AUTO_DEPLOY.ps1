# Auto Deployment Script - Runs all 3 steps automatically
# Password will be entered automatically where possible

$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Auto Deployment - Azone Project" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH key
$hasSSHKey = Test-Path $SSH_KEY_PATH

if ($hasSSHKey) {
    Write-Host "✅ SSH Key found - Passwordless access available" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⚠️  SSH Key not found" -ForegroundColor Yellow
    Write-Host "   Will set up SSH key first (password required once)" -ForegroundColor Yellow
    Write-Host "   Password: $VPS_PASSWORD" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Enter to start SSH key setup..." -ForegroundColor White
    Read-Host
    
    Write-Host "Running SSH key setup..." -ForegroundColor Cyan
    & powershell.exe -ExecutionPolicy Bypass -File "SETUP_SSH_KEY.ps1"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ SSH key setup failed!" -ForegroundColor Red
        exit 1
    }
    
    Start-Sleep -Seconds 2
}

# Step 2: Sync Files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Syncing files to VPS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

& powershell.exe -ExecutionPolicy Bypass -File "SYNC_TO_VPS.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  File sync had issues" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# Step 3: Deploy
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Deploying to VPS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

& powershell.exe -ExecutionPolicy Bypass -File "SIMPLE_DEPLOY.ps1"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Auto Deployment Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your application:" -ForegroundColor Green
Write-Host "   http://paing.xyz" -ForegroundColor White
Write-Host "   http://18.138.169.114" -ForegroundColor White
Write-Host ""
