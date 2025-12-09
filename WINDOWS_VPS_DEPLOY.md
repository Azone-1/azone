# 🪟 Windows VPS Deployment Guide (RDP)

Your VPS IP: **18.138.169.114** (Windows Server)

---

## ✅ Windows VPS မှာ Deploy လုပ်နည်း

### Step 1: RDP Connect လုပ်ပါ

1. **Windows မှာ Remote Desktop Connection** ဖွင့်ပါ
   - Start Menu → Search "Remote Desktop"
   - Or press `Win + R` → type `mstsc` → Enter

2. **VPS IP ထည့်ပါ**
   ```
   18.138.169.114
   ```

3. **Login** လုပ်ပါ
   - Username: `Administrator` (or your username)
   - Password: (your VPS password)

---

## 🚀 Quick Setup (Automated)

### Option 1: PowerShell Script (Recommended)

1. **RDP နဲ့ connect** လုပ်ပါ
2. **PowerShell as Administrator** ဖွင့်ပါ
   - Right-click Start → Windows PowerShell (Admin)

3. **Script download** လုပ်ပါ:
   ```powershell
   cd C:\
   git clone https://github.com/Apaing9611-arch/azone.git
   cd azone
   ```

4. **Setup script run** လုပ်ပါ:
   ```powershell
   .\WINDOWS_VPS_SETUP.ps1
   ```

**✅ Done!** Script က အကုန်လုပ်ပေးမယ်!

---

## 📋 Manual Setup (Step-by-Step)

### Step 1: Install Python

1. **Python Download** လုပ်ပါ:
   - https://www.python.org/downloads/
   - Download Python 3.11 or 3.12
   - **Important**: ✅ "Add Python to PATH" check လုပ်ပါ!

2. **Install** လုပ်ပါ:
   - Double-click installer
   - ✅ "Add Python to PATH"
   - Click "Install Now"

3. **Verify**:
   ```powershell
   python --version
   pip --version
   ```

### Step 2: Install Git (Optional but Recommended)

1. Download: https://git-scm.com/download/win
2. Install with default options
3. Verify:
   ```powershell
   git --version
   ```

### Step 3: Download Code

**Method 1: Git Clone (Recommended)**
```powershell
cd C:\
git clone https://github.com/Apaing9611-arch/azone.git
cd azone
```

**Method 2: Manual Upload**
- Download ZIP from GitHub
- Extract to `C:\azone`

### Step 4: Install Dependencies

```powershell
cd C:\azone
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Initialize Database

```powershell
python -c "import db_manager; db_manager.init_database()"
```

### Step 6: Create .env File

```powershell
# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Create .env file
notepad .env
```

Paste this (replace SECRET_KEY with generated key):
```
SECRET_KEY=your-generated-secret-key-here
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
HOST=0.0.0.0
PORT=5000
DOMAIN=18.138.169.114
```

### Step 7: Test Run

```powershell
python web_app.py
```

Browser မှာ open: `http://18.138.169.114:5000`

---

## 🔄 Keep Running (Background Service)

### Option 1: NSSM (Non-Sucking Service Manager) - Recommended

1. **Download NSSM**:
   - https://nssm.cc/download
   - Extract to `C:\nssm`

2. **Install Service**:
   ```powershell
   cd C:\nssm\win64
   .\nssm install AZoneBot "C:\Python311\python.exe" "C:\azone\web_app.py"
   .\nssm set AZoneBot AppDirectory "C:\azone"
   .\nssm set AZoneBot AppStdout "C:\azone\logs\output.log"
   .\nssm set AZoneBot AppStderr "C:\azone\logs\error.log"
   .\nssm start AZoneBot
   ```

3. **Service Commands**:
   ```powershell
   .\nssm start AZoneBot      # Start
   .\nssm stop AZoneBot       # Stop
   .\nssm restart AZoneBot    # Restart
   .\nssm status AZoneBot     # Status
   ```

### Option 2: Task Scheduler (Built-in Windows)

1. **Open Task Scheduler**:
   - Win + R → `taskschd.msc`

2. **Create Basic Task**:
   - Name: `AZone Bot`
   - Trigger: "When the computer starts"
   - Action: "Start a program"
   - Program: `C:\Python311\python.exe`
   - Arguments: `C:\azone\web_app.py`
   - Start in: `C:\azone`
   - ✅ "Run whether user is logged on or not"
   - ✅ "Run with highest privileges"

3. **Save** and test

### Option 3: PowerShell Background Job

```powershell
# Start job
Start-Job -ScriptBlock { cd C:\azone; python web_app.py }

# Check jobs
Get-Job

# View output
Receive-Job -Id 1
```

---

## 🌐 Configure Windows Firewall

### Allow Port 5000

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "AZone Flask" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

Or manually:
1. Windows Defender Firewall → Advanced Settings
2. Inbound Rules → New Rule
3. Port → TCP → Specific port: `5000`
4. Allow connection
5. Apply to all profiles
6. Name: "AZone Flask"

---

## 🔒 Setup IIS Reverse Proxy (Optional)

If you want to use port 80 instead of 5000:

### Install IIS

```powershell
# Run as Administrator
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationInit
```

### Install URL Rewrite & ARR

1. Download URL Rewrite: https://www.iis.net/downloads/microsoft/url-rewrite
2. Download ARR: https://www.iis.net/downloads/microsoft/application-request-routing
3. Install both

### Configure IIS

1. Open IIS Manager
2. Add Website:
   - Site name: `AZone`
   - Physical path: `C:\azone`
   - Binding: Port 80, IP: All Unassigned

3. Configure Reverse Proxy:
   - Select site → URL Rewrite → Add Rule
   - Reverse Proxy
   - Inbound: `(.*)`
   - Rewrite URL: `http://localhost:5000/{R:1}`

---

## 📊 Useful Commands

### Check if Flask is Running
```powershell
netstat -ano | findstr :5000
```

### View Logs
```powershell
# If using NSSM
Get-Content C:\azone\logs\output.log -Tail 50
Get-Content C:\azone\logs\error.log -Tail 50
```

### Restart Service (NSSM)
```powershell
cd C:\nssm\win64
.\nssm restart AZoneBot
```

### Check Python Processes
```powershell
Get-Process python
```

---

## 🆘 Troubleshooting

### ❌ Account Locked - "Too many logon attempts"

**Problem**: Administrator account locked due to failed login attempts.

**Solutions**:

#### Option 1: Wait for Auto-Unlock (15-30 minutes)
- Windows usually auto-unlocks after 15-30 minutes
- Wait and try again later

#### Option 2: Unlock via VPS Provider Console (AWS EC2)
If this is AWS EC2:
1. Go to AWS Console → EC2
2. Select instance → **Connect** → **EC2 Instance Connect** or **Session Manager**
3. Open PowerShell/Command Prompt
4. Run unlock command:
   ```powershell
   net user Administrator /active:yes
   net user Administrator /unlock
   ```

#### Option 3: Reset Password via VPS Provider
1. **AWS EC2**: EC2 Console → Instance → Actions → **Get Windows Password**
2. **Other Providers**: Check provider's console for password reset option

#### Option 4: Use Different User Account
If you have another admin account:
```powershell
# Create new admin user (if you can access via console)
net user NewAdmin Password123 /add
net localgroup administrators NewAdmin /add
```

#### Option 5: Disable Account Lockout Policy (After Unlocking)
Once you're logged in:
```powershell
# Run as Administrator
gpedit.msc
# Computer Configuration → Windows Settings → Security Settings → Account Policies → Account Lockout Policy
# Set "Account lockout threshold" to 0 (disabled)
```

### Port Already in Use?
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Python Not Found?
```powershell
# Add Python to PATH manually
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Python311;C:\Python311\Scripts", "Machine")
```

### Permission Denied?
- Run PowerShell as Administrator
- Check firewall rules
- Check Windows Defender exclusions

### Service Won't Start?
```powershell
# Check NSSM logs
cd C:\nssm\win64
.\nssm status AZoneBot
.\nssm edit AZoneBot  # Check configuration
```

### RDP Connection Issues?

**"The user account has been locked"**:
- See "Account Locked" section above
- Wait 15-30 minutes or unlock via provider console

**"CredSSP encryption oracle remediation"**:
```powershell
# On your local Windows PC, run:
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\CredSSP\Parameters" /v AllowEncryptionOracle /t REG_DWORD /d 2 /f
```

**"This computer can't connect to the remote computer"**:
- Check VPS firewall allows RDP (port 3389)
- Verify VPS is running
- Check network security groups (AWS)

---

## ✅ Checklist

- [ ] RDP connected to 18.138.169.114
- [ ] Python installed and in PATH
- [ ] Code downloaded to C:\azone
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Database initialized
- [ ] .env file created
- [ ] Flask app tested (python web_app.py)
- [ ] Firewall port 5000 opened
- [ ] Service configured (NSSM or Task Scheduler)
- [ ] App accessible at http://18.138.169.114:5000

---

## 🎉 Success!

Your app should now be running at:
- ✅ **http://18.138.169.114:5000**
- ✅ **http://18.138.169.114:5000/dashboard**

**24/7 running** with Windows Service! 🚀

---

## 📝 Quick Reference

**VPS IP**: 18.138.169.114  
**RDP**: `mstsc` → 18.138.169.114  
**App URL**: http://18.138.169.114:5000  
**Code Location**: C:\azone  
**Service Name**: AZoneBot (if using NSSM)

**Good luck! 🚀**
