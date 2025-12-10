# Windows Service Setup for AZone

Windows VPS မှာ Flask app ကို Windows Service အဖြစ် run လုပ်နည်း

---

## 📋 Method 1: NSSM (Non-Sucking Service Manager)

### Step 1: Download NSSM
- Download: https://nssm.cc/download
- Extract to: `C:\nssm`

### Step 2: Install Service
```powershell
cd C:\nssm\win64

# Install service
.\nssm.exe install AZoneFlask "C:\Python\python.exe" "C:\Azone\web_app.py"

# Set working directory
.\nssm.exe set AZoneFlask AppDirectory "C:\Azone"

# Set environment variables (if needed)
.\nssm.exe set AZoneFlask AppEnvironmentExtra "PORT=5000"
```

### Step 3: Start Service
```powershell
.\nssm.exe start AZoneFlask
```

### Step 4: Check Status
```powershell
Get-Service AZoneFlask
```

---

## 📋 Method 2: Task Scheduler (Built-in)

### Step 1: Create Task
1. Open **Task Scheduler**
2. Create **Basic Task**
3. Name: `AZone Flask Server`
4. Trigger: **When the computer starts**
5. Action: **Start a program**
   - Program: `C:\Python\python.exe`
   - Arguments: `C:\Azone\web_app.py`
   - Start in: `C:\Azone`

### Step 2: Run Task
- Right-click task → **Run**

---

## 📋 Method 3: PowerShell Script (24/7)

Use existing `RUN_24_7.ps1` script:

```powershell
cd C:\Azone
.\RUN_24_7.ps1
```

---

## ✅ Verify Service

```powershell
# Check if running
Get-Process python

# Check port
netstat -ano | findstr :5000

# Test in browser
Start-Process "http://localhost:5000"
```

---

## 🔄 Service Management

### NSSM Commands
```powershell
cd C:\nssm\win64

# Start
.\nssm.exe start AZoneFlask

# Stop
.\nssm.exe stop AZoneFlask

# Restart
.\nssm.exe restart AZoneFlask

# Remove
.\nssm.exe remove AZoneFlask confirm
```

### Task Scheduler
- Open Task Scheduler → Find task → Right-click → Run/End

---

## 📝 Service File Equivalent (Windows)

Linux systemd service file ကို Windows equivalent:

**Linux:**
```ini
[Unit]
Description=Paing Azone Python App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/azone
ExecStart=/usr/bin/python3 /var/www/azone/run_server.py
Restart=on-failure
```

**Windows (NSSM):**
```powershell
.\nssm.exe install AZoneFlask "C:\Python\python.exe" "C:\Azone\web_app.py"
.\nssm.exe set AZoneFlask AppDirectory "C:\Azone"
.\nssm.exe set AZoneFlask AppRestartDelay 5000
.\nssm.exe set AZoneFlask AppExit Default Restart
```

---

**Recommended:** NSSM သုံးပါ (Linux systemd နဲ့ similar)
