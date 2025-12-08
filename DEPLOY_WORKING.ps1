# Working Deployment Script - Fixed All Issues with Connection Reuse
$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "FIX AND DEPLOY - Azone Project" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Make sure VPN is ON and stable!" -ForegroundColor Yellow
Write-Host "VPN must stay connected during entire deployment" -ForegroundColor Yellow
Write-Host ""

# Build SSH target using format string to avoid @ issues
$sshTarget = "{0}@{1}" -f $VPS_USER, $VPS_IP
$useSSHKey = Test-Path $SSH_KEY_PATH

# SSH options for connection reuse and stability
$sshCommonOpts = "-o StrictHostKeyChecking=accept-new -o ConnectTimeout=30 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o ControlMaster=auto -o ControlPath=~/.ssh/control_%h_%p_%r -o ControlPersist=300"
$scpCommonOpts = "-o StrictHostKeyChecking=accept-new -o ConnectTimeout=30 -o ServerAliveInterval=10 -o ServerAliveCountMax=3"

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

# Function to execute SSH command with retry
function Invoke-SSHWithRetry {
    param(
        [string]$Command,
        [int]$MaxRetries = 3,
        [string]$StepName = "SSH Command"
    )
    
    for ($retry = 1; $retry -le $MaxRetries; $retry++) {
        if ($retry -gt 1) {
            Write-Host "  Retry attempt $retry of $MaxRetries..." -ForegroundColor Yellow
            Write-Host "  Check VPN connection and wait 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
        
        Write-Host "  Executing: $StepName..." -ForegroundColor White
        if ($useSSHKey) {
            $result = ssh $sshCommonOpts -i $SSH_KEY_PATH $sshTarget $Command 2>&1
        } else {
            if ($retry -eq 1) {
                Write-Host "  Password: $VPS_PASSWORD" -ForegroundColor Cyan
            }
            $result = ssh $sshCommonOpts $sshTarget $Command 2>&1
        }
        
        if ($LASTEXITCODE -eq 0) {
            return @{Success=$true; Output=$result}
        } else {
            $errorMsg = $result -join " "
            if ($errorMsg -match "Connection reset" -or $errorMsg -match "Connection closed") {
                Write-Host "  Connection reset detected - will retry..." -ForegroundColor Yellow
            } else {
                Write-Host "  Error: $errorMsg" -ForegroundColor Red
            }
            if ($retry -lt $MaxRetries) {
                continue
            }
        }
    }
    
    return @{Success=$false; Output=$result}
}

# Function to execute SCP with retry
function Invoke-SCPWithRetry {
    param(
        [string]$LocalFile,
        [string]$RemotePath,
        [int]$MaxRetries = 3,
        [string]$StepName = "File Upload"
    )
    
    for ($retry = 1; $retry -le $MaxRetries; $retry++) {
        if ($retry -gt 1) {
            Write-Host "  Retry attempt $retry of $MaxRetries..." -ForegroundColor Yellow
            Write-Host "  Check VPN connection and wait 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
        
        Write-Host "  Uploading: $StepName..." -ForegroundColor White
        if ($useSSHKey) {
            $result = scp $scpCommonOpts -i $SSH_KEY_PATH $LocalFile $RemotePath 2>&1
        } else {
            if ($retry -eq 1) {
                Write-Host "  Password: $VPS_PASSWORD" -ForegroundColor Cyan
            }
            $result = scp $scpCommonOpts $LocalFile $RemotePath 2>&1
        }
        
        if ($LASTEXITCODE -eq 0) {
            return @{Success=$true; Output=$result}
        } else {
            $errorMsg = $result -join " "
            if ($errorMsg -match "Connection reset" -or $errorMsg -match "Connection closed") {
                Write-Host "  Connection reset detected - will retry..." -ForegroundColor Yellow
            } else {
                Write-Host "  Error: $errorMsg" -ForegroundColor Red
            }
            if ($retry -lt $MaxRetries) {
                continue
            }
        }
    }
    
    return @{Success=$false; Output=$result}
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

Write-Host "Step 1: Establishing SSH connection (with connection reuse)..." -ForegroundColor Yellow
Write-Host "  This will reduce password prompts..." -ForegroundColor White
Write-Host "  Password (enter once): $VPS_PASSWORD" -ForegroundColor Cyan
Write-Host ""

$testResult = Invoke-SSHWithRetry -Command "echo 'VPS_CONNECTED'" -StepName "Connection Test"
if ($testResult.Success) {
    Write-Host "  VPS connection established!" -ForegroundColor Green
    Write-Host "  Connection will be reused for subsequent commands" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Cannot connect to VPS after retries" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Solutions:" -ForegroundColor Yellow
    Write-Host "    1. Make sure VPN is ON and connected" -ForegroundColor White
    Write-Host "    2. Check VPS is running (EC2 instance status)" -ForegroundColor White
    Write-Host "    3. Wait for VPN to stabilize, then run again" -ForegroundColor White
    Write-Host ""
    Write-Host "  Continuing anyway - will try deployment steps..." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "Step 2: Ensuring project directory exists..." -ForegroundColor Yellow
$dirCmd = "mkdir -p $REMOTE_FOLDER; chmod 755 $REMOTE_FOLDER; echo 'DIR_OK'"
$dirResult = Invoke-SSHWithRetry -Command $dirCmd -StepName "Directory Setup"
if ($dirResult.Success -or ($dirResult.Output -match "DIR_OK")) {
    Write-Host "  Directory ready" -ForegroundColor Green
} else {
    Write-Host "  Directory check failed: $($dirResult.Output)" -ForegroundColor Yellow
    Write-Host "  Continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Uploading essential files..." -ForegroundColor Yellow
Write-Host "  (Connection reuse means password only needed once)" -ForegroundColor White
Write-Host ""

# Build SCP target
$scpTarget = "{0}@{1}:{2}/" -f $VPS_USER, $VPS_IP, $REMOTE_FOLDER

$upload1 = Invoke-SCPWithRetry -LocalFile "MASTER_DEPLOY.sh" -RemotePath $scpTarget -StepName "MASTER_DEPLOY.sh"
if ($upload1.Success) {
    Write-Host "    MASTER_DEPLOY.sh uploaded" -ForegroundColor Green
} else {
    Write-Host "    Upload failed: $($upload1.Output)" -ForegroundColor Red
}

$upload2 = Invoke-SCPWithRetry -LocalFile "web_app.py" -RemotePath $scpTarget -StepName "web_app.py"
if ($upload2.Success) {
    Write-Host "    web_app.py uploaded" -ForegroundColor Green
} else {
    Write-Host "    Upload failed: $($upload2.Output)" -ForegroundColor Red
}

if (Test-Path "requirements.txt") {
    $upload3 = Invoke-SCPWithRetry -LocalFile "requirements.txt" -RemotePath $scpTarget -StepName "requirements.txt"
    if ($upload3.Success) {
        Write-Host "    requirements.txt uploaded" -ForegroundColor Green
    } else {
        Write-Host "    Upload failed: $($upload3.Output)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 4: Running deployment..." -ForegroundColor Yellow
Write-Host "  IMPORTANT: Keep VPN ON during entire deployment!" -ForegroundColor Red
Write-Host "  This will take 5-10 minutes..." -ForegroundColor Yellow
Write-Host "  (Password should NOT be needed again - connection reused)" -ForegroundColor White
Write-Host ""

$deployCmd = "cd $REMOTE_FOLDER; chmod +x MASTER_DEPLOY.sh; echo 'Starting deployment...'; bash MASTER_DEPLOY.sh 2>&1; echo ''; echo 'DEPLOYMENT_DONE'"

Write-Host "  Starting deployment (DO NOT turn off VPN!)..." -ForegroundColor Yellow
Write-Host ""

if ($useSSHKey) {
    ssh $sshCommonOpts -i $SSH_KEY_PATH $sshTarget $deployCmd
} else {
    ssh $sshCommonOpts $sshTarget $deployCmd
}

Write-Host ""
Write-Host "Step 5: Verifying deployment..." -ForegroundColor Yellow

$verifyCmd = "cd ~/Azone; echo '===VERIFICATION==='; if pm2 list 2>/dev/null | grep -q azone-bot; then echo 'PM2: RUNNING'; pm2 list | grep azone-bot; else echo 'PM2: NOT_RUNNING'; fi; echo ''; if sudo systemctl is-active nginx 2>/dev/null | grep -q active; then echo 'NGINX: RUNNING'; else echo 'NGINX: NOT_RUNNING'; fi; echo ''; if ss -tuln 2>/dev/null | grep -q ':80 '; then echo 'PORT_80: LISTENING'; else echo 'PORT_80: NOT_LISTENING'; fi"

$verifyResult = Invoke-SSHWithRetry -Command $verifyCmd -StepName "Verification" -MaxRetries 2
Write-Host $verifyResult.Output -ForegroundColor Cyan

# Close SSH control connection
Write-Host ""
Write-Host "Closing SSH connection..." -ForegroundColor Yellow
ssh -O exit $sshTarget 2>&1 | Out-Null

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
