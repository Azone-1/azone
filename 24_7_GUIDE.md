# 🕐 AZone 24/7 Server Guide

Server ကို 24/7 (24 hours, 7 days) ဆက်တိုက် run လုပ်ရန် guide ပါ။

---

## 🚀 အလွယ်ဆုံး နည်းလမ်း

### Option 1: Batch File သုံးပြီး Start လုပ်ပါ (အလွယ်ဆုံး)

1. `START_24_7.bat` file ကို double-click လုပ်ပါ
2. Server က automatically start ဖြစ်ပြီး 24/7 run လုပ်နေပါမယ်
3. Server crash ဖြစ်ရင် automatically restart ဖြစ်ပါမယ်

**အသုံးပြုပုံ:**
```
START_24_7.bat ကို double-click
```

---

### Option 2: PowerShell Script သုံးပြီး Start လုပ်ပါ

**PowerShell** မှာ run လုပ်ပါ:

```powershell
cd C:\Users\User\Desktop\Azone
.\RUN_24_7.ps1
```

---

## 📋 Features

✅ **Auto-Restart**: Server crash ဖြစ်ရင် automatically restart ဖြစ်ပါမယ်  
✅ **Health Check**: Every 10 seconds မှာ server health check လုပ်ပါမယ်  
✅ **Logging**: All events ကို `server_24_7.log` file မှာ log လုပ်ပါမယ်  
✅ **Error Handling**: Errors ဖြစ်ရင်လည်း server က continue run လုပ်နေပါမယ်  

---

## 📊 Monitoring

### Server Status Check

```powershell
# Check if server is running
python test_system.py

# Check logs
Get-Content server_24_7.log -Tail 50 -Wait

# Check process
Get-Process python
```

### View Logs

```powershell
# View recent logs
Get-Content server_24_7.log -Tail 20

# Watch logs in real-time
Get-Content server_24_7.log -Wait
```

---

## 🛑 Server ကို Stop လုပ်ရန်

### Method 1: Script Window မှာ
- Script run လုပ်ထားတဲ့ window မှာ `Ctrl+C` နှိပ်ပါ

### Method 2: PowerShell မှာ
```powershell
# Find and stop Python processes
Get-Process python | Stop-Process -Force
```

---

## ⚙️ Configuration

### Check Interval ပြောင်းရန်

`RUN_24_7.ps1` file မှာ:
```powershell
$script:CheckInterval = 10  # seconds (default: 10)
```

### Max Restarts ပြောင်းရန်

`RUN_24_7.ps1` file မှာ:
```powershell
$script:MaxRestarts = 1000  # maximum restart attempts
```

---

## 🔧 Troubleshooting

### Server က Start မဖြစ်ဘူး?

1. **Check Python installation:**
   ```powershell
   python --version
   ```

2. **Check if port 5000 is available:**
   ```powershell
   netstat -ano | findstr :5000
   ```

3. **Check logs:**
   ```powershell
   Get-Content server_24_7.log -Tail 50
   ```

### Server က Restart ဖြစ်နေတယ်?

1. **Check error logs:**
   ```powershell
   Get-Content server_24_7.log | Select-String "error" -Context 5
   ```

2. **Test server manually:**
   ```powershell
   python web_app.py
   ```

3. **Check dependencies:**
   ```powershell
   python test_system.py
   ```

---

## 📝 Log File Location

Logs ကို `server_24_7.log` file မှာ save လုပ်ပါမယ်:
```
C:\Users\User\Desktop\Azone\server_24_7.log
```

---

## ✅ Checklist

- [ ] `START_24_7.bat` file exists
- [ ] `RUN_24_7.ps1` file exists
- [ ] Python installed and working
- [ ] Port 5000 is available
- [ ] Server starts successfully
- [ ] Auto-restart works when server crashes
- [ ] Logs are being written

---

## 🎉 Success!

Server က 24/7 run လုပ်နေပါပြီ:
- ✅ Auto-start on script launch
- ✅ Auto-restart on crash
- ✅ Health monitoring
- ✅ Logging enabled
- ✅ Accessible at http://localhost:5000

**Tip**: Script ကို Windows startup မှာ add လုပ်ထားရင် computer restart ဖြစ်ရင်လည်း automatically start ဖြစ်ပါမယ်!

---

## 🔄 Windows Startup မှာ Auto-Start လုပ်ရန်

1. Press `Win + R`
2. Type: `shell:startup`
3. Press Enter
4. `START_24_7.bat` file ကို shortcut create လုပ်ပြီး startup folder ထဲကို copy လုပ်ပါ

ဒါဆိုရင် computer start ဖြစ်တိုင်း server က automatically run လုပ်ပါမယ်!

