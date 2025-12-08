# Simple Deployment - Step by Step
# This will work even with password prompts

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$LOCAL_FOLDER = "C:\Users\User\Desktop\Azone"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Simple VPS Deployment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will guide you step by step" -ForegroundColor Yellow
Write-Host "You will type password when asked" -ForegroundColor Yellow
Write-Host ""
Write-Host "Password: $VPS_PASSWORD" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting in 2 seconds..." -ForegroundColor White
Start-Sleep -Seconds 2

# Step 1: Check VPS folder
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 1: Checking VPS folder..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$checkCmd = @'
cd ~/Azone 2>/dev/null
if [ $? -eq 0 ]; then pwd; else echo "FOLDER_NOT_FOUND"; fi
echo ""
echo "===FILES==="
ls -la | head -10
echo ""
echo "===KEY_FILES==="
if [ -f MASTER_DEPLOY.sh ]; then echo "✅ MASTER_DEPLOY.sh"; else echo "❌ MASTER_DEPLOY.sh"; fi
if [ -f web_app.py ]; then echo "✅ web_app.py"; else echo "❌ web_app.py"; fi
echo "CHECK_DONE"
'@

Write-Host "Connecting to VPS..." -ForegroundColor White
Write-Host "⚠️  Type password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

$checkResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $checkCmd 2>&1

Write-Host $checkResult
Write-Host ""

if ($checkResult -match "FOLDER_NOT_FOUND") {
    Write-Host "❌ Folder not found on VPS!" -ForegroundColor Red
    Write-Host "Upload folder first:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File DELETE_AND_UPLOAD_FRESH.ps1" -ForegroundColor White
    exit 1
}

if ($checkResult -match "❌ MASTER_DEPLOY.sh") {
    Write-Host "⚠️  MASTER_DEPLOY.sh not found!" -ForegroundColor Yellow
    Write-Host "Uploading MASTER_DEPLOY.sh..." -ForegroundColor White
    Write-Host "⚠️  Type password again: $VPS_PASSWORD" -ForegroundColor Yellow
    Write-Host ""
    
    scp -o StrictHostKeyChecking=accept-new "MASTER_DEPLOY.sh" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Host
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ MASTER_DEPLOY.sh uploaded!" -ForegroundColor Green
    } else {
        Write-Host "❌ Upload failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Running deployment..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  This will take 10-15 minutes" -ForegroundColor Yellow
Write-Host "⚠️  Type password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""
Write-Host "Continuing in 2 seconds..." -ForegroundColor White
Start-Sleep -Seconds 2

$deployCmd = @"
cd $REMOTE_FOLDER
chmod +x MASTER_DEPLOY.sh
echo "Starting deployment..."
bash MASTER_DEPLOY.sh
"@

Write-Host "Executing MASTER_DEPLOY.sh..." -ForegroundColor Cyan
Write-Host ""

# Run deployment - output will show in real-time
$deployExitCode = 0
ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $deployCmd
$deployExitCode = $LASTEXITCODE

if ($deployExitCode -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Deployment may have encountered errors (Exit code: $deployExitCode)" -ForegroundColor Yellow
    Write-Host "   Check the output above for details" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Checking status..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$statusCmd = @'
echo "===PM2_STATUS==="
if pm2 list 2>/dev/null; then true; else echo "PM2 not running"; fi
echo ""
echo "===NGINX_STATUS==="
if sudo systemctl status nginx --no-pager 2>/dev/null | head -5; then true; else echo "Nginx not installed"; fi
echo ""
echo "===PORTS==="
if netstat -tuln 2>/dev/null | grep -E ":(80|443|8000)"; then true; elif ss -tuln 2>/dev/null | grep -E ":(80|443|8000)"; then true; else echo "No ports found"; fi
echo "STATUS_DONE"
'@

Write-Host "Checking status (type password if needed)..." -ForegroundColor White
$statusResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $statusCmd 2>&1
$statusExitCode = $LASTEXITCODE

Write-Host $statusResult
Write-Host ""

if ($statusExitCode -ne 0) {
    Write-Host "⚠️  Status check had issues (Exit code: $statusExitCode)" -ForegroundColor Yellow
    Write-Host "   But deployment may still be running..." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Process Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your bot:" -ForegroundColor Green
Write-Host "  http://paing.xyz" -ForegroundColor White
Write-Host "  http://18.138.169.114" -ForegroundColor White
Write-Host ""
Write-Host "📝 Check logs:" -ForegroundColor Yellow
Write-Host "  ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor White
Write-Host '  pm2 logs azone-bot' -ForegroundColor White
Write-Host ""

