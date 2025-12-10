# VPS Manual Update Guide

VPS မှာ script file မရှိရင် manual commands သုံးပါ

---

## 🚀 Quick Update Commands (VPS PowerShell)

VPS PowerShell (Admin) မှာ run လုပ်ပါ:

```powershell
cd C:\Azone

# Stop Flask server if running
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Pull latest code from GitHub
git pull origin main

# If main branch doesn't exist, try master
# git pull origin master

# Update dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start server
python web_app.py
```

---

## 📋 Step-by-Step

### Step 1: Stop Server
```powershell
cd C:\Azone
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Step 2: Pull Code
```powershell
git pull origin main
```

**If error occurs:**
```powershell
# Check current branch
git branch

# Pull from correct branch
git pull origin master
# or
git pull origin <your-branch-name>
```

### Step 3: Update Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Start Server
```powershell
python web_app.py
```

---

## 🔄 Alternative: Copy Script File

**Local PC မှာ:**
1. `VPS_PULL_UPDATE.ps1` file ကို copy လုပ်ပါ
2. RDP session မှာ paste လုပ်ပါ `C:\Azone\`

**VPS မှာ:**
```powershell
cd C:\Azone
.\VPS_PULL_UPDATE.ps1
```

---

## ✅ Verify Update

Browser မှာ check လုပ်ပါ:
- `http://18.138.169.114:5000/bot-builder`
- Bot Builder page ပေါ်ရင် update successful!

---

## ⚠️ Troubleshooting

### Git Not Found
```powershell
# Install Git from: https://git-scm.com/downloads
# Or use manual copy method
```

### Not a Git Repository
```powershell
cd C:\Azone
git init
git remote add origin https://github.com/Apaing9611-arch/azone.git
git pull origin main
```

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

**Quick Update:** Just run these 3 commands:
```powershell
cd C:\Azone
git pull origin main
python web_app.py
```

