# Full Deployment Script - Complete VPS Setup
# This will sync files and deploy everything

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 FULL DEPLOYMENT - Azone Project" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH key
$useSSHKey = $false
if (Test-Path $SSH_KEY_PATH) {
    Write-Host "✅ SSH key found" -ForegroundColor Green
    $useSSHKey = $true
} else {
    Write-Host "⚠️  SSH key not found, will use password" -ForegroundColor Yellow
    Write-Host "   Password: $VPS_PASSWORD" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Step 1: Uploading files to VPS..." -ForegroundColor Yellow

# Upload key files
$filesToUpload = @(
    "web_app.py",
    "MASTER_DEPLOY.sh",
    "requirements.txt",
    "config.py",
    "db_manager.py",
    "bot_db_manager.py",
    "bot_logic_engine.py",
    "bot_templates.py",
    "gemini_service.py",
    "telegram_service.py",
    "facebook_service.py",
    "auth_manager.py",
    "auth_routes.py",
    "session_middleware.py"
)

$uploadSuccess = $true
foreach ($file in $filesToUpload) {
    if (Test-Path $file) {
        Write-Host "  Uploading $file..." -ForegroundColor White
        if ($useSSHKey) {
            scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "$file" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        } else {
            scp -o StrictHostKeyChecking=accept-new "$file" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        }
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✅ $file" -ForegroundColor Green
        } else {
            Write-Host "    ❌ $file failed" -ForegroundColor Red
            $uploadSuccess = $false
        }
    }
}

# Upload directories
Write-Host "  Uploading templates/..." -ForegroundColor White
if ($useSSHKey) {
    scp -r -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "templates" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
} else {
    scp -r -o StrictHostKeyChecking=accept-new "templates" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
}

Write-Host "  Uploading static/..." -ForegroundColor White
if ($useSSHKey) {
    scp -r -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "static" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
} else {
    scp -r -o StrictHostKeyChecking=accept-new "static" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
}

Write-Host ""
Write-Host "Step 2: Running deployment on VPS..." -ForegroundColor Yellow
Write-Host "  This will take 5-10 minutes..." -ForegroundColor White

$deployCmd = @"
cd $REMOTE_FOLDER
chmod +x MASTER_DEPLOY.sh
bash MASTER_DEPLOY.sh
"@

if ($useSSHKey) {
    Write-Host "  Executing MASTER_DEPLOY.sh..." -ForegroundColor Cyan
    ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $deployCmd
} else {
    Write-Host "  ⚠️  Password needed: $VPS_PASSWORD" -ForegroundColor Yellow
    Write-Host "  Executing MASTER_DEPLOY.sh..." -ForegroundColor Cyan
    ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $deployCmd
}

Write-Host ""
Write-Host "Step 3: Checking deployment status..." -ForegroundColor Yellow

$statusCmd = @'
cd ~/Azone
echo "===PM2_STATUS==="
pm2 list 2>/dev/null | grep azone-bot || echo "PM2_NOT_RUNNING"
echo ""
echo "===NGINX_STATUS==="
sudo systemctl is-active nginx 2>/dev/null || echo "NGINX_NOT_RUNNING"
echo ""
echo "===PORTS==="
ss -tuln 2>/dev/null | grep -E ":(80|443|8000)" || netstat -tuln 2>/dev/null | grep -E ":(80|443|8000)" || echo "NO_PORTS"
'@

if ($useSSHKey) {
    $status = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $statusCmd 2>&1
} else {
    $status = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $statusCmd 2>&1
}

Write-Host $status -ForegroundColor Cyan

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your application:" -ForegroundColor Green
Write-Host "  http://paing.xyz" -ForegroundColor White
Write-Host "  http://18.138.169.114" -ForegroundColor White
Write-Host "  https://paing.xyz (if SSL installed)" -ForegroundColor White
Write-Host ""
