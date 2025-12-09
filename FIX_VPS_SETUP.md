# 🔧 Fix: WINDOWS_VPS_SETUP.ps1 Run မရတာ

## ❌ Error: Script Run မရတာ

**ပြဿနာ:**
- `.\WINDOWS_VPS_SETUP.ps1` run လုပ်လို့မရဘူး
- Execution policy error ဖြစ်နိုင်တယ်
- Script file မရှိတာဖြစ်နိုင်တယ်

---

## ✅ Solutions

### Solution 1: Execution Policy Fix (အလွယ်ဆုံး)

**PowerShell as Administrator** မှာ:

```powershell
# Check current policy
Get-ExecutionPolicy

# Set to Bypass for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Now run script
.\WINDOWS_VPS_SETUP.ps1
```

**Or run directly with bypass:**

```powershell
powershell -ExecutionPolicy Bypass -File .\WINDOWS_VPS_SETUP.ps1
```

---

### Solution 2: Check if Script Exists

```powershell
# Check if file exists
Test-Path .\WINDOWS_VPS_SETUP.ps1

# List files
dir *.ps1

# If not found, check current directory
pwd
cd C:\Azone
dir
```

---

### Solution 3: Manual Setup (Script မရှိရင်)

Script file မရှိရင် manually setup လုပ်ပါ:

```powershell
cd C:\Azone

# Step 1: Check Python
python --version

# Step 2: Upgrade pip
python -m pip install --upgrade pip

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Create .env file
@"
SECRET_KEY=your-secret-key-here-change-in-production
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
HOST=0.0.0.0
PORT=5000
DOMAIN=paing.xyz
USE_HTTPS=True
"@ | Out-File -FilePath .env -Encoding utf8

# Step 5: Initialize database
python -c "import db_manager; db_manager.init_database()"
python -c "import bot_db_manager; bot_db_manager.init_bot_database()"
python -c "import auth_manager; auth_manager.init_auth_database()"

# Step 6: Configure firewall
New-NetFirewallRule -DisplayName "AZone Flask 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Step 7: Start server
python web_app.py
```

---

### Solution 4: Download Script from Local PC

**Local PC** မှာ script file ကို VPS ကို copy လုပ်ပါ:

1. **RDP** နဲ့ connect လုပ်ပါ
2. **Local PC** မှာ `WINDOWS_VPS_SETUP.ps1` file ကို copy လုပ်ပါ
3. **VPS** မှာ `C:\Azone` folder ထဲကို paste လုပ်ပါ
4. **PowerShell** မှာ run လုပ်ပါ:

```powershell
cd C:\Azone
powershell -ExecutionPolicy Bypass -File .\WINDOWS_VPS_SETUP.ps1
```

---

## 🚀 Quick Fix Commands

**Copy-paste လုပ်ပြီး run လုပ်ပါ:**

```powershell
# Fix execution policy
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Check if script exists
if (Test-Path .\WINDOWS_VPS_SETUP.ps1) {
    Write-Host "✅ Script found!" -ForegroundColor Green
    .\WINDOWS_VPS_SETUP.ps1
} else {
    Write-Host "❌ Script not found!" -ForegroundColor Red
    Write-Host "Run manual setup instead" -ForegroundColor Yellow
}
```

---

## 📋 Step-by-Step Fix

### Step 1: Check Current Directory

```powershell
pwd
# Should show: C:\Azone
```

### Step 2: Check if Script Exists

```powershell
dir WINDOWS_VPS_SETUP.ps1
```

### Step 3: Fix Execution Policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

### Step 4: Run Script

```powershell
.\WINDOWS_VPS_SETUP.ps1
```

---

## ✅ Alternative: Run Without Script

Script run မရရင် manual commands run လုပ်ပါ:

```powershell
cd C:\Azone

# Install dependencies
pip install -r requirements.txt

# Create .env
echo "DOMAIN=paing.xyz" > .env
echo "USE_HTTPS=True" >> .env
echo "PORT=5000" >> .env
echo "HOST=0.0.0.0" >> .env

# Start server
python web_app.py
```

---

## 🎯 Most Likely Solution

**99% က execution policy ပြဿနာပါ:**

```powershell
# Run this first:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Then run script:
.\WINDOWS_VPS_SETUP.ps1
```

**ဒါက အလုပ်လုပ်မယ်!** ✅

