# Single SSH Session Deployment - Password Only Once
$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SINGLE SESSION DEPLOYMENT - Azone" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Make sure VPN is ON and stable!" -ForegroundColor Yellow
Write-Host "VPN must stay connected during entire deployment" -ForegroundColor Yellow
Write-Host ""

# Build SSH target
$sshTarget = "{0}@{1}" -f $VPS_USER, $VPS_IP
$useSSHKey = Test-Path $SSH_KEY_PATH

# Function to test VPN/Network connectivity
function Test-VPNConnection {
    Write-Host "Checking VPN/Network connection..." -ForegroundColor Yellow
    $ping = Test-Connection -ComputerName $VPS_IP -Count 2 -Quiet -ErrorAction SilentlyContinue
    if ($ping) {
        Write-Host "  Network connection OK" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  Network connection FAILED" -ForegroundColor Red
        Write-Host "  Please check:" -ForegroundColor Yellow
        Write-Host "    1. VPN is ON and connected" -ForegroundColor White
        Write-Host "    2. VPS is running (EC2 instance)" -ForegroundColor White
        Write-Host "    3. Internet connection is stable" -ForegroundColor White
        return $false
    }
}

# Function to encode file to base64
function Encode-FileToBase64 {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        $bytes = [System.IO.File]::ReadAllBytes($FilePath)
        return [Convert]::ToBase64String($bytes)
    }
    return $null
}

# Check VPN first
if (-not (Test-VPNConnection)) {
    Write-Host ""
    Write-Host "Waiting 5 seconds for VPN to stabilize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    if (-not (Test-VPNConnection)) {
        Write-Host ""
        Write-Host "ERROR: Cannot connect to VPS. Please:" -ForegroundColor Red
        Write-Host "  1. Turn ON VPN" -ForegroundColor Yellow
        Write-Host "  2. Wait for VPN to fully connect" -ForegroundColor Yellow
        Write-Host "  3. Run this script again" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
}
Write-Host ""

Write-Host "Step 1: Preparing files for upload..." -ForegroundColor Yellow

# Encode files to base64
$masterDeployBase64 = $null
$webAppBase64 = $null
$requirementsBase64 = $null

if (Test-Path "MASTER_DEPLOY.sh") {
    Write-Host "  Encoding MASTER_DEPLOY.sh..." -ForegroundColor White
    $masterDeployBase64 = Encode-FileToBase64 -FilePath "MASTER_DEPLOY.sh"
    if ($masterDeployBase64) {
        Write-Host "    MASTER_DEPLOY.sh encoded" -ForegroundColor Green
    }
}

if (Test-Path "web_app.py") {
    Write-Host "  Encoding web_app.py..." -ForegroundColor White
    $webAppBase64 = Encode-FileToBase64 -FilePath "web_app.py"
    if ($webAppBase64) {
        Write-Host "    web_app.py encoded" -ForegroundColor Green
    }
}

if (Test-Path "requirements.txt") {
    Write-Host "  Encoding requirements.txt..." -ForegroundColor White
    $requirementsBase64 = Encode-FileToBase64 -FilePath "requirements.txt"
    if ($requirementsBase64) {
        Write-Host "    requirements.txt encoded" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 2: Creating deployment script..." -ForegroundColor Yellow

# Create a single bash script that does everything
$deploymentScript = @"
#!/bin/bash
set -e

REMOTE_FOLDER="$REMOTE_FOLDER"

echo "=== Starting Single Session Deployment ==="
echo ""

# Create directory
echo "Creating project directory..."
mkdir -p `$REMOTE_FOLDER
chmod 755 `$REMOTE_FOLDER
cd `$REMOTE_FOLDER

# Decode and write files
echo "Uploading files via base64..."

if [ -n "$masterDeployBase64" ]; then
    echo "  Writing MASTER_DEPLOY.sh..."
    echo "$masterDeployBase64" | base64 -d > MASTER_DEPLOY.sh
    chmod +x MASTER_DEPLOY.sh
    echo "    MASTER_DEPLOY.sh uploaded"
fi

if [ -n "$webAppBase64" ]; then
    echo "  Writing web_app.py..."
    echo "$webAppBase64" | base64 -d > web_app.py
    echo "    web_app.py uploaded"
fi

if [ -n "$requirementsBase64" ]; then
    echo "  Writing requirements.txt..."
    echo "$requirementsBase64" | base64 -d > requirements.txt
    echo "    requirements.txt uploaded"
fi

echo ""
echo "=== Files uploaded successfully ==="
echo ""
echo "Starting deployment..."
echo ""

# Run deployment
cd `$REMOTE_FOLDER
bash MASTER_DEPLOY.sh 2>&1

echo ""
echo "=== Deployment completed ==="
echo ""

# Verification
echo "=== Verification ==="
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

if ss -tuln 2>/dev/null | grep -q ':80 '; then
    echo "PORT_80: LISTENING"
else
    echo "PORT_80: NOT_LISTENING"
fi
"@

# Save deployment script to temp file
$tempScript = [System.IO.Path]::GetTempFileName()
$deploymentScript | Out-File -FilePath $tempScript -Encoding UTF8 -NoNewline

Write-Host "  Deployment script created" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Executing deployment in SINGLE SSH session..." -ForegroundColor Yellow
Write-Host "  Password will be asked ONCE: $VPS_PASSWORD" -ForegroundColor Cyan
Write-Host "  IMPORTANT: Keep VPN ON during entire deployment!" -ForegroundColor Red
Write-Host "  This will take 5-10 minutes..." -ForegroundColor Yellow
Write-Host ""

# Read the script content
$scriptContent = Get-Content $tempScript -Raw

Write-Host "  Connecting to VPS..." -ForegroundColor White
Write-Host "  Enter password ONCE when prompted: $VPS_PASSWORD" -ForegroundColor Cyan
Write-Host ""

# Build SSH command arguments as array
$sshArgs = @(
    "-o", "StrictHostKeyChecking=accept-new",
    "-o", "ConnectTimeout=30",
    "-o", "ServerAliveInterval=10",
    "-o", "ServerAliveCountMax=3"
)

if ($useSSHKey) {
    $sshArgs += "-i", $SSH_KEY_PATH
}

$sshArgs += $sshTarget
$sshArgs += "bash"
$sshArgs += "-s"

# Use direct SSH invocation - this allows interactive password prompt
# Pipe script content directly to SSH
Write-Host "  Executing SSH command..." -ForegroundColor White
$scriptContent | & ssh.exe $sshArgs

# Cleanup
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT PROCESS COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access your application:" -ForegroundColor Green
Write-Host "  http://paing.xyz" -ForegroundColor White
Write-Host "  http://18.138.169.114" -ForegroundColor White
Write-Host ""
Write-Host "If the site doesn't load, wait 1-2 minutes for services to start" -ForegroundColor Yellow
Write-Host ""
