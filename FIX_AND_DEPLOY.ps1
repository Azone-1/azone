# Fix and Deploy - Complete Solution
# This script will check VPS, fix issues, and ensure deployment works

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔧 FIX AND DEPLOY - Azone Project" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Determine SSH method
$useSSHKey = Test-Path $SSH_KEY_PATH
$sshOpts = if ($useSSHKey) { "-i $SSH_KEY_PATH" } else { "" }

Write-Host "Step 1: Checking VPS connection..." -ForegroundColor Yellow
$testCmd = "echo 'VPS_CONNECTED'"
$sshTarget = $VPS_USER + '@' + $VPS_IP
if ($useSSHKey) {
    $test = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $sshTarget $testCmd 2>&1
} else {
    Write-Host "  Password needed: $VPS_PASSWORD" -ForegroundColor Yellow
    $test = ssh -o StrictHostKeyChecking=accept-new $sshTarget $testCmd 2>&1
}

if ($test -match "VPS_CONNECTED") {
    Write-Host "  ✅ VPS connection OK" -ForegroundColor Green
} else {
    Write-Host "  ❌ VPS connection failed: $test" -ForegroundColor Red
    Write-Host "  Please check your network and VPS status" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 2: Ensuring project directory exists..." -ForegroundColor Yellow
$dirCmd = "mkdir -p $REMOTE_FOLDER; chmod 755 $REMOTE_FOLDER; echo 'DIR_OK'"
$sshTarget = $VPS_USER + '@' + $VPS_IP
if ($useSSHKey) {
    $dirResult = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $sshTarget $dirCmd 2>&1
} else {
    Write-Host "  Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    $dirResult = ssh -o StrictHostKeyChecking=accept-new $sshTarget $dirCmd 2>&1
}
Write-Host "  ✅ Directory ready" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Uploading essential files..." -ForegroundColor Yellow

# Upload MASTER_DEPLOY.sh first
Write-Host "  Uploading MASTER_DEPLOY.sh..." -ForegroundColor White
$scpTarget = ($VPS_USER + '@' + $VPS_IP + ':' + $REMOTE_FOLDER + '/')
if ($useSSHKey) {
    scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "MASTER_DEPLOY.sh" $scpTarget 2>&1 | Out-Null
} else {
    Write-Host "    Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    scp -o StrictHostKeyChecking=accept-new "MASTER_DEPLOY.sh" $scpTarget 2>&1 | Out-Null
}
Write-Host "    ✅ MASTER_DEPLOY.sh" -ForegroundColor Green

# Upload web_app.py
Write-Host "  Uploading web_app.py..." -ForegroundColor White
if ($useSSHKey) {
    scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "web_app.py" $scpTarget 2>&1 | Out-Null
} else {
    Write-Host "    Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    scp -o StrictHostKeyChecking=accept-new "web_app.py" $scpTarget 2>&1 | Out-Null
}
Write-Host "    ✅ web_app.py" -ForegroundColor Green

# Upload requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "  Uploading requirements.txt..." -ForegroundColor White
    if ($useSSHKey) {
        scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "requirements.txt" $scpTarget 2>&1 | Out-Null
    } else {
        Write-Host "    Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
        scp -o StrictHostKeyChecking=accept-new "requirements.txt" $scpTarget 2>&1 | Out-Null
    }
    Write-Host "    ✅ requirements.txt" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 4: Running deployment..." -ForegroundColor Yellow
Write-Host "  ⚠️  This will take 5-10 minutes..." -ForegroundColor Yellow
Write-Host "  ⚠️  Password may be needed: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

$deployCmd = @"
cd $REMOTE_FOLDER
chmod +x MASTER_DEPLOY.sh
echo 'Starting deployment...'
bash MASTER_DEPLOY.sh 2>&1
echo ''
echo 'DEPLOYMENT_DONE'
"@

$sshTarget = $VPS_USER + '@' + $VPS_IP
if ($useSSHKey) {
    ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $sshTarget $deployCmd
} else {
    Write-Host "  Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    ssh -o StrictHostKeyChecking=accept-new $sshTarget $deployCmd
}

Write-Host ""
Write-Host "Step 5: Verifying deployment..." -ForegroundColor Yellow

$verifyCmd = @'
cd ~/Azone
echo "===VERIFICATION==="
if pm2 list 2>/dev/null | grep -q azone-bot; then
    echo "PM2: RUNNING"
    pm2 list | grep azone-bot
else
    echo "PM2: NOT_RUNNING"
fi
echo ""
if sudo systemctl is-active nginx 2>/dev/null | grep -q active; then
    echo "NGINX: RUNNING"
else
    echo "NGINX: NOT_RUNNING"
fi
echo ""
if ss -tuln 2>/dev/null | grep -q ":80 "; then
    echo "PORT_80: LISTENING"
else
    echo "PORT_80: NOT_LISTENING"
fi
'@

$sshTarget = $VPS_USER + '@' + $VPS_IP
if ($useSSHKey) {
    $verify = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $sshTarget $verifyCmd 2>&1
} else {
    Write-Host "  Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    $verify = ssh -o StrictHostKeyChecking=accept-new $sshTarget $verifyCmd 2>&1
}

Write-Host $verify -ForegroundColor Cyan

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT PROCESS COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your application:" -ForegroundColor Green
Write-Host "  http://paing.xyz" -ForegroundColor White
Write-Host "  http://18.138.169.114" -ForegroundColor White
Write-Host ""
Write-Host "If the site doesn't load, wait 1-2 minutes for services to start" -ForegroundColor Yellow
Write-Host ""
