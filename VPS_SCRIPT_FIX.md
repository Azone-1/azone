# 🔧 Fix: Script Run မရတာ

## ❌ Problem: `.\WINDOWS_VPS_SETUP.ps1` Run မရတာ

**ပြဿနာ:**
- Execution policy fix လုပ်ပြီးတောင် script run လုပ်လို့မရဘူး
- Script file မရှိတာဖြစ်နိုင်တယ်
- Path မှားနေတာဖြစ်နိုင်တယ်

---

## ✅ Solution 1: Check if Script Exists

```powershell
# Check current directory
pwd
# Should show: C:\Azone

# Check if script file exists
Test-Path .\WINDOWS_VPS_SETUP.ps1

# List all .ps1 files
dir *.ps1

# List all files
dir
```

**If script not found:**
- Script file က VPS မှာ မရှိဘူး
- Local PC က copy လုပ်ရမယ်

---

## ✅ Solution 2: Manual Setup (Script မရှိရင်)

**သတင်းကောင်း:** Server က run လုပ်နေပြီးသားဖြစ်နေတယ်! ✅

Script run မရရင်လည်း manual setup လုပ်ပြီးသားဖြစ်နေတယ်။

### Check Server Status:

```powershell
# Check if server is running
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue

# Check Python processes
Get-Process python -ErrorAction SilentlyContinue
```

---

## ✅ Solution 3: Create .env File (Access Denied Fix)

**Error:** `Access to the path 'C:\Azone\.env' is denied`

**Fix:**

```powershell
# Method 1: Run PowerShell as Administrator
# Right-click PowerShell → Run as Administrator

# Method 2: Use different location
cd C:\Azone
New-Item -ItemType File -Path .env -Force

# Then edit manually or use:
Set-Content -Path .env -Value "DOMAIN=paing.xyz`nUSE_HTTPS=True`nPORT=5000`nHOST=0.0.0.0"
```

**Or create manually:**
1. Open Notepad
2. Save as `C:\Azone\.env`
3. Add content:
```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
```

---

## ✅ Solution 4: Download Script from Local PC

**Local PC** မှာ script file ကို VPS ကို copy လုပ်ပါ:

1. **RDP** connect လုပ်ပါ
2. **Local PC** မှာ `WINDOWS_VPS_SETUP.ps1` file ကို copy လုပ်ပါ
3. **VPS** မှာ `C:\Azone` folder ထဲကို paste လုပ်ပါ
4. **PowerShell as Administrator** မှာ:

```powershell
cd C:\Azone
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\WINDOWS_VPS_SETUP.ps1
```

---

## 🎯 Current Status Check

**Server က run လုပ်နေပြီးသားဖြစ်နေတယ်!** ✅

### Verify:

```powershell
# Check port 5000
netstat -ano | findstr :5000

# Check Python process
Get-Process python

# Test server
curl http://localhost:5000
```

---

## ✅ Complete Manual Setup (Script မရှိရင်)

Script run မရရင်လည်း manual setup လုပ်ပြီးသားဖြစ်နေတယ်:

```powershell
cd C:\Azone

# ✅ Dependencies installed (already done)
# ✅ Firewall configured (already done)
# ✅ Server running (already done)

# Only missing: .env file
# Create manually via Notepad or:
New-Item -ItemType File -Path .env -Force
# Then edit with Notepad
```

---

## 🚀 Next Steps

### 1. Create .env File (If missing)

**Notepad** နဲ့ create လုပ်ပါ:
- File → New
- Save as: `C:\Azone\.env`
- Content:
```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
```

### 2. Test Server Access

**From VPS:**
```powershell
curl http://localhost:5000
```

**From Local PC/Phone:**
```
http://18.138.169.114:5000
```

### 3. Configure AWS Security Group

**AWS Console** → EC2 → Security Groups:
- Allow inbound: Port 5000 (TCP)
- Allow inbound: Port 80 (HTTP)
- Allow inbound: Port 443 (HTTPS)

---

## 📋 Summary

| Item | Status |
|------|--------|
| Python installed | ✅ |
| Dependencies installed | ✅ |
| Firewall configured | ✅ |
| Server running | ✅ |
| .env file | ⚠️ Need to create |
| Script file | ⚠️ May not exist |

---

## 🎉 Good News!

**Server က run လုပ်နေပြီးသားဖြစ်နေတယ်!** ✅

Script run မရရင်လည်း:
- ✅ Server already running
- ✅ Firewall configured
- ✅ Just need .env file

**Next:** Create .env file manually, then test access from phone! 🚀

