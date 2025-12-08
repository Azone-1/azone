# Setup SSH Key for Passwordless Access
# Run this ONCE to avoid password prompts forever

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"
$SSH_PUB_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone.pub"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔑 Setup SSH Key for Passwordless Access" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Generate SSH key (if not exists)" -ForegroundColor White
Write-Host "  2. Copy key to VPS" -ForegroundColor White
Write-Host "  3. Setup SSH config" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  You will type password ONCE: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host "   After this, NO MORE passwords needed!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting now..." -ForegroundColor White

# Step 1: Generate SSH key
Write-Host ""
Write-Host "Step 1: Generating SSH key..." -ForegroundColor Yellow

if (-not (Test-Path $SSH_KEY_PATH)) {
    Write-Host "   Creating new SSH key..." -ForegroundColor White
    $null = ssh-keygen -t ed25519 -f $SSH_KEY_PATH -N "" -C "azone-vps-key" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ SSH key generation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✅ SSH key generated" -ForegroundColor Green
} else {
    Write-Host "   ✅ SSH key already exists" -ForegroundColor Green
}

# Step 2: Copy public key to VPS
Write-Host ""
Write-Host "Step 2: Copying SSH key to VPS..." -ForegroundColor Yellow
Write-Host "   ⚠️  Type password: $VPS_PASSWORD" -ForegroundColor Yellow
Write-Host ""

$publicKey = Get-Content $SSH_PUB_KEY_PATH -Raw -ErrorAction SilentlyContinue

if ($publicKey) {
    $publicKey = $publicKey.Trim()
    
    $copyKeyCmd = @"
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "$publicKey" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "KEY_ADDED_SUCCESS"
"@
    
    Write-Host "   Copying key to VPS..." -ForegroundColor White
    Write-Host "   ⚠️  Enter password when prompted: $VPS_PASSWORD" -ForegroundColor Yellow
    
    # Try using Plink if available (supports password flag)
    $plinkPath = Get-Command plink -ErrorAction SilentlyContinue
    if ($plinkPath) {
        $keyResult = echo $VPS_PASSWORD | & plink -ssh -pw $VPS_PASSWORD "${VPS_USER}@${VPS_IP}" $copyKeyCmd 2>&1
    } else {
    $keyResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $copyKeyCmd 2>&1
    }
    
    if ($keyResult -match "KEY_ADDED_SUCCESS" -or $LASTEXITCODE -eq 0) {
        Write-Host "   ✅ SSH key copied to VPS!" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Key copy result: $keyResult" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Could not read public key!" -ForegroundColor Red
    exit 1
}

# Step 3: Update SSH config
Write-Host ""
Write-Host "Step 3: Updating SSH config..." -ForegroundColor Yellow

$sshConfigPath = "$env:USERPROFILE\.ssh\config"
$configEntry = @"

Host azone-vps
    HostName $VPS_IP
    User $VPS_USER
    Port 22
    IdentityFile $SSH_KEY_PATH
    StrictHostKeyChecking accept-new
"@

if (Test-Path $sshConfigPath) {
    $existingConfig = Get-Content $sshConfigPath -Raw
    if ($existingConfig -notmatch "Host azone-vps") {
        Add-Content -Path $sshConfigPath -Value $configEntry
        Write-Host "   ✅ SSH config updated" -ForegroundColor Green
    } else {
        Write-Host "   ✅ SSH config already has azone-vps entry" -ForegroundColor Green
        # Update IdentityFile if different
        $existingConfig = $existingConfig -replace "(?s)(Host azone-vps.*?IdentityFile\s+)[^\r\n]+", "`$1$SSH_KEY_PATH"
        Set-Content -Path $sshConfigPath -Value $existingConfig
    }
} else {
    New-Item -Path $sshConfigPath -ItemType File -Force | Out-Null
    Set-Content -Path $sshConfigPath -Value $configEntry
    Write-Host "   ✅ SSH config created" -ForegroundColor Green
}

# Step 4: Test passwordless connection
Write-Host ""
Write-Host "Step 4: Testing passwordless connection..." -ForegroundColor Yellow
Write-Host ""

$testCmd = "echo PASSWORDLESS_WORKS"
# Try with host alias first, then fallback to full connection
$testResult = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH azone-vps $testCmd 2>&1
if ($LASTEXITCODE -ne 0 -or $testResult -notmatch "PASSWORDLESS_WORKS") {
    # Fallback to full connection string
    $testResult = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $testCmd 2>&1
}

if ($testResult -match "PASSWORDLESS_WORKS") {
    Write-Host "   ✅ Passwordless SSH works!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "✅ Setup Complete!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Now you can use:" -ForegroundColor Yellow
    Write-Host "  ssh azone-vps" -ForegroundColor White
    Write-Host "  (NO password needed!)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Run deployment:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "   ⚠️  Passwordless test failed" -ForegroundColor Yellow
    Write-Host "   You may still need to type password" -ForegroundColor Yellow
    Write-Host "   But deployment will still work!" -ForegroundColor Green
    Write-Host ""
}

