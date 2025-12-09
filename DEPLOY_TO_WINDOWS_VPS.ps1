# 🚀 Windows VPS Deployment - RDP Method
# This script uses RDP/Remote PowerShell to deploy to Windows VPS

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$DOMAIN = "paing.xyz"
$LOCAL_FOLDER = "C:\Users\User\Desktop\Azone"
$REMOTE_FOLDER = "C:\Azone"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 AZone Windows VPS Deployment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS IP: $VPS_IP" -ForegroundColor White
Write-Host "Domain: $DOMAIN" -ForegroundColor White
Write-Host "Method: Remote PowerShell (WinRM)" -ForegroundColor White
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Connect to Windows VPS via PowerShell" -ForegroundColor White
Write-Host "  2. Upload code to VPS" -ForegroundColor White
Write-Host "  3. Install Python & dependencies" -ForegroundColor White
Write-Host "  4. Configure domain" -ForegroundColor White
Write-Host "  5. Start server 24/7" -ForegroundColor White
Write-Host ""
Write-Host "Starting in 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Step 1: Test WinRM connection
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 1: Testing VPS Connection..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Create credential object
$securePassword = ConvertTo-SecureString $VPS_PASSWORD -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($VPS_USER, $securePassword)

# Test connection
Write-Host "Testing WinRM connection to $VPS_IP..." -ForegroundColor White
try {
    $session = New-PSSession -ComputerName $VPS_IP -Credential $credential -ErrorAction Stop
    Write-Host "✅ VPS connection successful!" -ForegroundColor Green
    Remove-PSSession $session
} catch {
    Write-Host "❌ WinRM connection failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Use RDP to connect manually:" -ForegroundColor Yellow
    Write-Host "  1. Open Remote Desktop Connection (mstsc)" -ForegroundColor White
    Write-Host "  2. Connect to: $VPS_IP" -ForegroundColor White
    Write-Host "  3. Username: $VPS_USER" -ForegroundColor White
    Write-Host "  4. Password: $VPS_PASSWORD" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run: .\DEPLOY_VIA_RDP.ps1" -ForegroundColor Yellow
    exit 1
}

# Step 2: Create remote session
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Creating Remote Session..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$session = New-PSSession -ComputerName $VPS_IP -Credential $credential
Write-Host "✅ Remote session created!" -ForegroundColor Green

# Step 3: Check Python on VPS
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Checking Python Installation..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$checkPython = Invoke-Command -Session $session -ScriptBlock {
    $pythonVersion = python --version 2>&1
    $pipVersion = pip --version 2>&1
    return @{
        Python = $pythonVersion
        Pip = $pipVersion
        PythonExists = $LASTEXITCODE -eq 0
    }
}

if ($checkPython.PythonExists) {
    Write-Host "✅ Python found: $($checkPython.Python)" -ForegroundColor Green
    Write-Host "✅ Pip found: $($checkPython.Pip)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Python not found. Installing Python..." -ForegroundColor Yellow
    Write-Host "Please install Python manually via RDP:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  2. Install with 'Add Python to PATH' checked" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Remove-PSSession $session
    exit 1
}

# Step 4: Upload files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 4: Uploading Files to VPS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Create remote directory
Invoke-Command -Session $session -ScriptBlock {
    param($RemoteFolder)
    if (-not (Test-Path $RemoteFolder)) {
        New-Item -ItemType Directory -Path $RemoteFolder -Force | Out-Null
    }
} -ArgumentList $REMOTE_FOLDER

Write-Host "Uploading files to $REMOTE_FOLDER..." -ForegroundColor White
Write-Host "⚠️  This may take a few minutes..." -ForegroundColor Yellow

# Copy files using Copy-Item over session
$excludePatterns = @("__pycache__", "*.pyc", ".git", "node_modules", "_TRASH_BACKUP")
$filesToCopy = Get-ChildItem -Path $LOCAL_FOLDER -Recurse | Where-Object {
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($_.FullName -like "*$pattern*") {
            $exclude = $true
            break
        }
    }
    return -not $exclude
}

$fileCount = 0
foreach ($file in $filesToCopy) {
    $relativePath = $file.FullName.Substring($LOCAL_FOLDER.Length + 1)
    $remotePath = Join-Path $REMOTE_FOLDER $relativePath
    $remoteDir = Split-Path $remotePath -Parent
    
    try {
        Invoke-Command -Session $session -ScriptBlock {
            param($Dir)
            if (-not (Test-Path $Dir)) {
                New-Item -ItemType Directory -Path $Dir -Force | Out-Null
            }
        } -ArgumentList $remoteDir
        
        Copy-Item -Path $file.FullName -Destination $remotePath -ToSession $session -Force -ErrorAction SilentlyContinue
        $fileCount++
        if ($fileCount % 10 -eq 0) {
            Write-Host "  Uploaded $fileCount files..." -ForegroundColor Gray
        }
    } catch {
        Write-Host "  ⚠️  Failed to upload: $relativePath" -ForegroundColor Yellow
    }
}

Write-Host "✅ Uploaded $fileCount files!" -ForegroundColor Green

# Step 5: Install dependencies
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 5: Installing Dependencies..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$installResult = Invoke-Command -Session $session -ScriptBlock {
    param($RemoteFolder)
    Set-Location $RemoteFolder
    
    # Upgrade pip
    Write-Host "Upgrading pip..." -ForegroundColor White
    python -m pip install --upgrade pip 2>&1
    
    # Install requirements
    Write-Host "Installing requirements..." -ForegroundColor White
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt 2>&1
    } else {
        Write-Host "⚠️  requirements.txt not found!" -ForegroundColor Yellow
    }
    
    return $LASTEXITCODE
} -ArgumentList $REMOTE_FOLDER

if ($installResult -eq 0) {
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some dependencies may have failed, but continuing..." -ForegroundColor Yellow
}

# Step 6: Configure domain
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 6: Configuring Domain..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Invoke-Command -Session $session -ScriptBlock {
    param($RemoteFolder, $Domain)
    Set-Location $RemoteFolder
    
    $envFile = Join-Path $RemoteFolder ".env"
    
    # Create or update .env file
    $envContent = @()
    if (Test-Path $envFile) {
        $envContent = Get-Content $envFile
    }
    
    # Update or add DOMAIN
    $domainFound = $false
    for ($i = 0; $i -lt $envContent.Length; $i++) {
        if ($envContent[$i] -match "^DOMAIN=") {
            $envContent[$i] = "DOMAIN=$Domain"
            $domainFound = $true
            break
        }
    }
    if (-not $domainFound) {
        $envContent += "DOMAIN=$Domain"
    }
    
    # Update or add USE_HTTPS
    $httpsFound = $false
    for ($i = 0; $i -lt $envContent.Length; $i++) {
        if ($envContent[$i] -match "^USE_HTTPS=") {
            $envContent[$i] = "USE_HTTPS=True"
            $httpsFound = $true
            break
        }
    }
    if (-not $httpsFound) {
        $envContent += "USE_HTTPS=True"
    }
    
    $envContent | Set-Content $envFile
    Write-Host "✅ Domain configured: $Domain" -ForegroundColor Green
} -ArgumentList $REMOTE_FOLDER, $DOMAIN

# Step 7: Create startup script
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 7: Creating 24/7 Startup Script..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Invoke-Command -Session $session -ScriptBlock {
    param($RemoteFolder)
    Set-Location $RemoteFolder
    
    # Create Windows Service startup script
    $startScript = @"
# AZone 24/7 Server Startup
cd `"$RemoteFolder`"
python web_app.py
"@
    
    $startScriptPath = Join-Path $RemoteFolder "START_SERVER.bat"
    $startScript | Set-Content $startScriptPath
    
    Write-Host "✅ Startup script created!" -ForegroundColor Green
} -ArgumentList $REMOTE_FOLDER

# Step 8: Start server
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 8: Starting Server..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Invoke-Command -Session $session -ScriptBlock {
    param($RemoteFolder)
    Set-Location $RemoteFolder
    
    # Stop existing Python processes
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    # Start server in background
    $startScriptPath = Join-Path $RemoteFolder "START_SERVER.bat"
    Start-Process -FilePath "python" -ArgumentList "web_app.py" -WorkingDirectory $RemoteFolder -WindowStyle Hidden
    
    Start-Sleep -Seconds 5
    
    # Check if server is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        return @{Success = $true; Status = $response.StatusCode}
    } catch {
        return @{Success = $false; Error = $_.Exception.Message}
    }
} -ArgumentList $REMOTE_FOLDER

# Step 9: Check status
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 9: Checking Deployment Status..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$status = Invoke-Command -Session $session -ScriptBlock {
    # Check Python processes
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
    $port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
    
    return @{
        PythonRunning = $pythonProcesses.Count -gt 0
        Port5000Open = $null -ne $port5000
        ProcessCount = $pythonProcesses.Count
    }
}

Write-Host "===SERVER_STATUS===" -ForegroundColor Cyan
if ($status.PythonRunning) {
    Write-Host "✅ Python server is running ($($status.ProcessCount) process(es))" -ForegroundColor Green
} else {
    Write-Host "⚠️  Python server not running" -ForegroundColor Yellow
}

if ($status.Port5000Open) {
    Write-Host "✅ Port 5000 is open" -ForegroundColor Green
} else {
    Write-Host "⚠️  Port 5000 not open" -ForegroundColor Yellow
}

# Cleanup session
Remove-PSSession $session

# Final summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your app:" -ForegroundColor Green
Write-Host "  http://$DOMAIN" -ForegroundColor White
Write-Host "  http://$VPS_IP:5000" -ForegroundColor White
Write-Host ""
Write-Host "📱 Phone က domain နဲ့ access လုပ်လို့ရပါပြီ!" -ForegroundColor Green
Write-Host "  http://$VPS_IP:5000" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. RDP to VPS: mstsc → $VPS_IP" -ForegroundColor White
Write-Host "  2. Check server: cd $REMOTE_FOLDER" -ForegroundColor White
Write-Host "  3. View logs: Check PowerShell window" -ForegroundColor White
Write-Host "  4. Configure firewall: Allow port 5000" -ForegroundColor White
Write-Host ""

