# 🔄 Windows Service Setup - Keep Flask Running 24/7

Windows VPS မှာ Flask app ကို background service အဖြစ် run လုပ်ရန် guide ပါ။

---

## 🎯 Option 1: NSSM (Recommended) ⭐

NSSM (Non-Sucking Service Manager) က Windows service အတွက် အလွယ်ဆုံး method ပါ။

### Step 1: Download NSSM

1. Go to: https://nssm.cc/download
2. Download latest release (nssm-2.24.zip)
3. Extract to `C:\nssm`

### Step 2: Install Service

**PowerShell as Administrator** မှာ run လုပ်ပါ:

```powershell
cd C:\nssm\win64

# Install service
.\nssm install AZoneBot "C:\Python311\python.exe" "C:\azone\web_app.py"

# Set working directory
.\nssm set AZoneBot AppDirectory "C:\azone"

# Set environment variables (if needed)
.\nssm set AZoneBot AppEnvironmentExtra "PATH=C:\Python311;C:\Python311\Scripts"

# Set log files
.\nssm set AZoneBot AppStdout "C:\azone\logs\output.log"
.\nssm set AZoneBot AppStderr "C:\azone\logs\error.log"

# Set auto-restart on failure
.\nssm set AZoneBot AppRestartDelay 5000
.\nssm set AZoneBot AppThrottle 1500

# Start service
.\nssm start AZoneBot
```

### Step 3: Verify Service

```powershell
# Check status
.\nssm status AZoneBot

# Or use Windows Services
services.msc
# Look for "AZoneBot"
```

### Step 4: Service Commands

```powershell
cd C:\nssm\win64

.\nssm start AZoneBot      # Start
.\nssm stop AZoneBot       # Stop
.\nssm restart AZoneBot    # Restart
.\nssm status AZoneBot     # Status
.\nssm edit AZoneBot       # Edit configuration
.\nssm remove AZoneBot     # Remove service
```

### Step 5: View Logs

```powershell
# Output logs
Get-Content C:\azone\logs\output.log -Tail 50 -Wait

# Error logs
Get-Content C:\azone\logs\error.log -Tail 50 -Wait
```

---

## 🎯 Option 2: Task Scheduler (Built-in Windows)

Windows built-in Task Scheduler သုံးပြီး service လုပ်နိုင်တယ်။

### Step 1: Open Task Scheduler

- Press `Win + R`
- Type: `taskschd.msc`
- Press Enter

### Step 2: Create Task

1. **Right-click** "Task Scheduler Library" → **Create Task**

2. **General Tab**:
   - Name: `AZone Bot`
   - ✅ "Run whether user is logged on or not"
   - ✅ "Run with highest privileges"
   - Configure for: **Windows 10/11**

3. **Triggers Tab**:
   - Click **New**
   - Begin the task: **At startup**
   - ✅ "Enabled"
   - OK

4. **Actions Tab**:
   - Click **New**
   - Action: **Start a program**
   - Program/script: `C:\Python311\python.exe`
   - Add arguments: `C:\azone\web_app.py`
   - Start in: `C:\azone`
   - OK

5. **Conditions Tab**:
   - ✅ "Start the task only if the computer is on AC power" (uncheck if needed)
   - ✅ "Wake the computer to run this task" (optional)

6. **Settings Tab**:
   - ✅ "Allow task to be run on demand"
   - ✅ "Run task as soon as possible after a scheduled start is missed"
   - ✅ "If the task fails, restart every: **1 minute**"
   - Attempt to restart up to: **3 times**

7. **OK** to save

### Step 3: Test Task

1. Right-click task → **Run**
2. Check if Flask starts
3. View logs in Task Scheduler → Task History

---

## 🎯 Option 3: PowerShell Background Job

Simple method for testing, but less reliable for production.

### Start Background Job

```powershell
cd C:\azone
Start-Job -ScriptBlock { 
    Set-Location C:\azone
    python web_app.py 
} -Name "AZoneBot"
```

### Check Job Status

```powershell
Get-Job
Receive-Job -Name "AZoneBot"
```

### Stop Job

```powershell
Stop-Job -Name "AZoneBot"
Remove-Job -Name "AZoneBot"
```

---

## 🔧 Advanced Configuration

### Multiple Environment Variables

If using NSSM:

```powershell
.\nssm set AZoneBot AppEnvironmentExtra "PATH=C:\Python311;C:\Python311\Scripts;SECRET_KEY=your-key;GEMINI_API_KEY=your-key"
```

### Custom Port

Edit `web_app.py` or `.env`:
```
PORT=8000
```

Update firewall:
```powershell
New-NetFirewallRule -DisplayName "AZone Flask 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Auto-restart on Crash

**NSSM** (already configured):
```powershell
.\nssm set AZoneBot AppRestartDelay 5000
.\nssm set AZoneBot AppThrottle 1500
```

**Task Scheduler**:
- Settings tab → "If the task fails, restart every: 1 minute"

---

## 📊 Monitoring

### Check if Service is Running

```powershell
# Check port
netstat -ano | findstr :5000

# Check process
Get-Process python

# Check service (NSSM)
Get-Service AZoneBot
```

### View Real-time Logs

```powershell
# NSSM logs
Get-Content C:\azone\logs\output.log -Tail 50 -Wait

# Task Scheduler logs
# Task Scheduler → Task History
```

### Performance Monitoring

```powershell
# CPU and Memory usage
Get-Process python | Select-Object CPU, WorkingSet, ProcessName
```

---

## 🆘 Troubleshooting

### Service Won't Start?

1. **Check logs**:
   ```powershell
   Get-Content C:\azone\logs\error.log -Tail 50
   ```

2. **Test manually**:
   ```powershell
   cd C:\azone
   python web_app.py
   ```

3. **Check Python path**:
   ```powershell
   where.exe python
   ```

4. **Check permissions**:
   - Run PowerShell as Administrator
   - Check file permissions on C:\azone

### Service Starts but Stops Immediately?

1. **Check error logs**
2. **Verify Python path** in service config
3. **Check environment variables**
4. **Test with manual run first**

### Port Already in Use?

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Can't Access from Outside?

1. **Check Windows Firewall**:
   ```powershell
   Get-NetFirewallRule -DisplayName "AZone Flask"
   ```

2. **Check VPS firewall** (if any)
3. **Verify HOST=0.0.0.0** in .env

---

## ✅ Checklist

- [ ] NSSM installed or Task Scheduler configured
- [ ] Service created and configured
- [ ] Service starts successfully
- [ ] Logs directory created
- [ ] Firewall port 5000 opened
- [ ] Service auto-starts on boot
- [ ] Service auto-restarts on crash
- [ ] App accessible at http://18.138.169.114:5000

---

## 🎉 Success!

Your Flask app is now running as a Windows service:
- ✅ 24/7 uptime
- ✅ Auto-start on boot
- ✅ Auto-restart on crash
- ✅ Background running
- ✅ Accessible at http://18.138.169.114:5000

**Recommended**: Use **NSSM** for best results! 🚀
