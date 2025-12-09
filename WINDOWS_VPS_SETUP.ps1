# Windows VPS Setup Script for AZone
# Run as Administrator: .\WINDOWS_VPS_SETUP.ps1

Write-Host "=========================================" -ForegroundColor Green
Write-Host "🚀 AZone Windows VPS Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Please run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell → Run as Administrator" -ForegroundColor Yellow
    exit 1
}

# Project directory
$PROJECT_DIR = "C:\azone"
$LOGS_DIR = "$PROJECT_DIR\logs"

Write-Host "📋 Step 1: Checking Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📋 Step 2: Checking Git..." -ForegroundColor Cyan
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Git not found (optional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 3: Downloading/Updating Code..." -ForegroundColor Cyan
if (Test-Path $PROJECT_DIR) {
    Write-Host "📁 Project directory exists: $PROJECT_DIR" -ForegroundColor Yellow
    Set-Location $PROJECT_DIR
    if (Test-Path ".git") {
        Write-Host "🔄 Updating code from Git..." -ForegroundColor Yellow
        git pull 2>&1 | Out-Null
        Write-Host "✅ Code updated" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Not a Git repository, using existing files" -ForegroundColor Yellow
    }
} else {
    Write-Host "📥 Cloning repository..." -ForegroundColor Yellow
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git clone https://github.com/Apaing9611-arch/azone.git $PROJECT_DIR
        Write-Host "✅ Code downloaded" -ForegroundColor Green
    } else {
        Write-Host "❌ Git not found. Please download code manually to $PROJECT_DIR" -ForegroundColor Red
        exit 1
    }
}

Set-Location $PROJECT_DIR

Write-Host ""
Write-Host "📋 Step 4: Installing Python Dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  requirements.txt not found, installing basic packages..." -ForegroundColor Yellow
    pip install flask flask-login werkzeug requests google-generativeai python-dotenv
    Write-Host "✅ Basic packages installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Step 5: Creating Logs Directory..." -ForegroundColor Cyan
if (-not (Test-Path $LOGS_DIR)) {
    New-Item -ItemType Directory -Path $LOGS_DIR -Force | Out-Null
}
Write-Host "✅ Logs directory created" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Step 6: Initializing Database..." -ForegroundColor Cyan
try {
    python -c "import db_manager; db_manager.init_database()" 2>&1 | Out-Null
    Write-Host "✅ Database initialized" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database initialization failed (may already exist)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 7: Creating .env File..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    $secretKey = python -c "import secrets; print(secrets.token_hex(32))" 2>&1
    $envContent = @"
SECRET_KEY=$secretKey
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
HOST=0.0.0.0
PORT=5000
DOMAIN=18.138.169.114
"@
    Set-Content -Path ".env" -Value $envContent
    Write-Host "✅ .env file created" -ForegroundColor Green
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Step 8: Configuring Windows Firewall..." -ForegroundColor Cyan
try {
    $existingRule = Get-NetFirewallRule -DisplayName "AZone Flask" -ErrorAction SilentlyContinue
    if (-not $existingRule) {
        New-NetFirewallRule -DisplayName "AZone Flask" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow | Out-Null
        Write-Host "✅ Firewall rule created" -ForegroundColor Green
    } else {
        Write-Host "✅ Firewall rule already exists" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Firewall configuration failed (may need manual setup)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 9: Testing Flask App..." -ForegroundColor Cyan
Write-Host "Starting Flask app for testing (will run for 5 seconds)..." -ForegroundColor Yellow

$job = Start-Job -ScriptBlock {
    Set-Location $using:PROJECT_DIR
    python web_app.py 2>&1
}

Start-Sleep -Seconds 5

$running = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($running) {
    Write-Host "✅ Flask app is running on port 5000" -ForegroundColor Green
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -ErrorAction SilentlyContinue
} else {
    Write-Host "⚠️  Flask app test failed (check manually)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your app:" -ForegroundColor Cyan
Write-Host "  ✅ http://18.138.169.114:5000" -ForegroundColor Green
Write-Host "  ✅ http://18.138.169.114:5000/dashboard" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test manually: python web_app.py" -ForegroundColor Yellow
Write-Host "  2. Setup service (NSSM or Task Scheduler)" -ForegroundColor Yellow
Write-Host "  3. See WINDOWS_VPS_DEPLOY.md for service setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Useful Commands:" -ForegroundColor Cyan
Write-Host "  python web_app.py                    # Run Flask" -ForegroundColor White
Write-Host "  netstat -ano | findstr :5000         # Check if running" -ForegroundColor White
Write-Host "  Get-Process python                  # View Python processes" -ForegroundColor White
Write-Host ""
