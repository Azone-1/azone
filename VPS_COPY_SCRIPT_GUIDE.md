# VPS Script Copy Guide

## Method 1: RDP Copy-Paste (အလွယ်ဆုံး)

### Step 1: Local PC မှာ
1. File Explorer ဖွင့်ပါ
2. `C:\Users\User\Desktop\VPS_PULL_UPDATE.ps1` file ကို **Copy** လုပ်ပါ (Ctrl+C)

### Step 2: VPS RDP Session မှာ
1. RDP session ဖွင့်ပါ
2. File Explorer ဖွင့်ပါ
3. `C:\Azone` folder ထဲ သွားပါ
4. **Paste** လုပ်ပါ (Ctrl+V)

### Step 3: VPS PowerShell မှာ Run လုပ်ပါ
```powershell
cd C:\Azone
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\VPS_PULL_UPDATE.ps1
```

---

## Method 2: PowerShell နဲ့ Create လုပ်ပါ

VPS PowerShell မှာ file content ကို create လုပ်ပါ:

```powershell
cd C:\Azone

# Create script file
@"
# VPS Code Update Script
# Run this on VPS to pull latest code from GitHub
# Run as Administrator: .\VPS_PULL_UPDATE.ps1

Write-Host "=========================================" -ForegroundColor Green
Write-Host "🔄 AZone VPS Code Update" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Project directory
`$PROJECT_DIR = "C:\Azone"

# Check if running as Administrator
`$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not `$isAdmin) {
    Write-Host "⚠️  Not running as Administrator (some steps may fail)" -ForegroundColor Yellow
}

# Check if Git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git not found!" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if project directory exists
if (-not (Test-Path `$PROJECT_DIR)) {
    Write-Host "❌ Project directory not found: `$PROJECT_DIR" -ForegroundColor Red
    Write-Host "Please run WINDOWS_VPS_SETUP.ps1 first" -ForegroundColor Yellow
    exit 1
}

Set-Location `$PROJECT_DIR

# Check if this is a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not a Git repository!" -ForegroundColor Red
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    
    git init
    Write-Host "Enter GitHub repository URL:" -ForegroundColor Yellow
    `$repoUrl = Read-Host "Repository URL"
    git remote add origin `$repoUrl
    Write-Host "✅ Git initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Step 1: Stopping Flask server (if running)..." -ForegroundColor Cyan
`$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if (`$pythonProcesses) {
    Write-Host "Found Python processes, stopping..." -ForegroundColor Yellow
    `$pythonProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Flask server stopped" -ForegroundColor Green
} else {
    Write-Host "✅ No Flask server running" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Step 2: Checking current branch..." -ForegroundColor Cyan
`$currentBranch = git branch --show-current
if ([string]::IsNullOrWhiteSpace(`$currentBranch)) {
    `$currentBranch = "main"
    Write-Host "No branch found, using 'main'" -ForegroundColor Yellow
} else {
    Write-Host "Current branch: `$currentBranch" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 3: Fetching latest code from GitHub..." -ForegroundColor Cyan
try {
    git fetch origin
    Write-Host "✅ Fetched latest code" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Fetch failed: `$_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 4: Pulling latest changes..." -ForegroundColor Cyan
try {
    git pull origin `$currentBranch
    Write-Host "✅ Code updated successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Pull failed: `$_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying to reset and pull..." -ForegroundColor Yellow
    git reset --hard origin/`$currentBranch
    git pull origin `$currentBranch
}

Write-Host ""
Write-Host "📋 Step 5: Installing/Updating dependencies..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    Write-Host "✅ Dependencies updated" -ForegroundColor Green
} else {
    Write-Host "⚠️  requirements.txt not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Step 6: Testing Flask app..." -ForegroundColor Cyan
Write-Host "Starting Flask app for 5 seconds to test..." -ForegroundColor Yellow

`$job = Start-Job -ScriptBlock {
    Set-Location `$using:PROJECT_DIR
    python web_app.py 2>&1
}

Start-Sleep -Seconds 5

`$running = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if (`$running) {
    Write-Host "✅ Flask app is working!" -ForegroundColor Green
    Stop-Job `$job -ErrorAction SilentlyContinue
    Remove-Job `$job -ErrorAction SilentlyContinue
} else {
    Write-Host "⚠️  Flask app test failed (check manually)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ UPDATE COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Start server:" -ForegroundColor Cyan
Write-Host "   python web_app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Access Bot Builder:" -ForegroundColor Cyan
Write-Host "   http://18.138.169.114:5000/bot-builder" -ForegroundColor Green
Write-Host "   http://18.138.169.114:5000/login" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Login Credentials:" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White
Write-Host ""
"@ | Out-File -FilePath "VPS_PULL_UPDATE.ps1" -Encoding UTF8

# Run script
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\VPS_PULL_UPDATE.ps1
```

---

## Method 3: Manual Git Commands (Script မလိုဘူး)

Script file copy လုပ်ဖို့ အခက်အခဲရှိရင် manual commands သုံးပါ:

```powershell
cd C:\Azone
git pull origin main
python web_app.py
```

---

## ⚠️ Execution Policy Error ရှိရင်

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\VPS_PULL_UPDATE.ps1
```

---

## ✅ Verify

Script run လုပ်ပြီးရင်:
- Browser မှာ `http://18.138.169.114:5000/bot-builder` ဖွင့်ပါ
- Bot Builder page ပေါ်ရင် successful!

