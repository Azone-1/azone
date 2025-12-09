# 🚀 VPS Deployment - One-Click Deploy
# This script will deploy to VPS and configure domain

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$DOMAIN = "paing.xyz"
$LOCAL_FOLDER = "C:\Users\User\Desktop\Azone"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 AZone VPS Deployment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS IP: $VPS_IP" -ForegroundColor White
Write-Host "Domain: $DOMAIN" -ForegroundColor White
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Upload code to VPS" -ForegroundColor White
Write-Host "  2. Install dependencies" -ForegroundColor White
Write-Host "  3. Configure domain" -ForegroundColor White
Write-Host "  4. Start server 24/7" -ForegroundColor White
Write-Host ""
Write-Host "Password: $VPS_PASSWORD" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting in 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Step 1: Test VPS connection
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 1: Testing VPS Connection..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$testCmd = "echo 'Connection test successful'"
Write-Host "Connecting to VPS..." -ForegroundColor White
Write-Host "⚠️  Type password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

$testResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $testCmd 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ VPS connection successful!" -ForegroundColor Green
} else {
    Write-Host "❌ VPS connection failed!" -ForegroundColor Red
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. VPN is connected (if required)" -ForegroundColor White
    Write-Host "  2. VPS is running" -ForegroundColor White
    Write-Host "  3. Internet connection is stable" -ForegroundColor White
    exit 1
}

# Step 2: Upload files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Uploading Files to VPS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  This may take a few minutes..." -ForegroundColor Yellow
Write-Host "⚠️  Type password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

# Create remote directory
$createDirCmd = "mkdir -p ~/Azone"
ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $createDirCmd 2>&1 | Out-Null

# Upload files using SCP
Write-Host "Uploading files..." -ForegroundColor White
$excludePatterns = @("__pycache__", "*.pyc", ".git", "node_modules", "_TRASH_BACKUP")
$excludeArgs = $excludePatterns | ForEach-Object { "-x $_" }
$excludeArgs = $excludeArgs -join " "

# Use rsync if available, otherwise use scp
$uploadCmd = "scp -r -o StrictHostKeyChecking=accept-new `"${LOCAL_FOLDER}\*`" ${VPS_USER}@${VPS_IP}:~/Azone/"
Write-Host "Running: $uploadCmd" -ForegroundColor Gray
Invoke-Expression $uploadCmd 2>&1 | Out-Host

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Files uploaded successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Upload may have issues, but continuing..." -ForegroundColor Yellow
}

# Step 3: Run deployment on VPS
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Running Deployment on VPS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  This will take 10-15 minutes" -ForegroundColor Yellow
Write-Host "⚠️  Type password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

$deployCmd = @"
cd ~/Azone
chmod +x MASTER_DEPLOY.sh 2>/dev/null || true
chmod +x QUICK_VPS_SETUP.sh 2>/dev/null || true

# Check which deployment script exists
if [ -f MASTER_DEPLOY.sh ]; then
    echo "Using MASTER_DEPLOY.sh..."
    bash MASTER_DEPLOY.sh
elif [ -f QUICK_VPS_SETUP.sh ]; then
    echo "Using QUICK_VPS_SETUP.sh..."
    bash QUICK_VPS_SETUP.sh
else
    echo "No deployment script found. Setting up manually..."
    # Basic setup
    python3 -m pip install --upgrade pip
    pip3 install -r requirements.txt
    echo "Basic setup complete. Please run deployment script manually."
fi
"@

Write-Host "Executing deployment..." -ForegroundColor Cyan
ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $deployCmd 2>&1 | Out-Host

# Step 4: Configure domain
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 4: Configuring Domain..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$domainCmd = @"
cd ~/Azone

# Set domain in .env file
if [ ! -f .env ]; then
    touch .env
fi

# Add or update DOMAIN
if grep -q "DOMAIN=" .env; then
    sed -i 's|DOMAIN=.*|DOMAIN=$DOMAIN|' .env
else
    echo "DOMAIN=$DOMAIN" >> .env
fi

# Add USE_HTTPS
if grep -q "USE_HTTPS=" .env; then
    sed -i 's|USE_HTTPS=.*|USE_HTTPS=True|' .env
else
    echo "USE_HTTPS=True" >> .env
fi

echo "✅ Domain configured: $DOMAIN"
cat .env | grep DOMAIN
"@

Write-Host "Configuring domain..." -ForegroundColor White
ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $domainCmd 2>&1 | Out-Host

# Step 5: Check status
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 5: Checking Deployment Status..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$statusCmd = @"
echo "===SERVER_STATUS==="
if pm2 list 2>/dev/null | grep -q azone; then
    echo "✅ PM2: Server is running"
    pm2 list | grep azone
else
    echo "⚠️  PM2: Server not found in PM2"
fi

echo ""
echo "===PORTS==="
if command -v netstat >/dev/null 2>&1; then
    netstat -tuln 2>/dev/null | grep -E ":(80|443|5000|8000)" || echo "No ports found"
elif command -v ss >/dev/null 2>&1; then
    ss -tuln 2>/dev/null | grep -E ":(80|443|5000|8000)" || echo "No ports found"
else
    echo "Cannot check ports"
fi

echo ""
echo "===NGINX==="
if systemctl is-active --quiet nginx 2>/dev/null; then
    echo "✅ Nginx: Running"
else
    echo "⚠️  Nginx: Not running"
fi
"@

Write-Host "Checking status..." -ForegroundColor White
ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $statusCmd 2>&1 | Out-Host

# Final summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your app:" -ForegroundColor Green
Write-Host "  http://$DOMAIN" -ForegroundColor White
Write-Host "  http://$VPS_IP" -ForegroundColor White
Write-Host ""
Write-Host "📱 Phone က domain နဲ့ access လုပ်လို့ရပါပြီ!" -ForegroundColor Green
Write-Host "  https://$DOMAIN" -ForegroundColor White
Write-Host ""
Write-Host "📝 Check logs:" -ForegroundColor Yellow
Write-Host "  ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor White
Write-Host "  pm2 logs azone-bot" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Restart server:" -ForegroundColor Yellow
Write-Host "  ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor White
Write-Host "  pm2 restart azone-bot" -ForegroundColor White
Write-Host ""

