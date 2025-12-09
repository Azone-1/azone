# 🪟 Windows VPS Deployment via RDP

VPS က **Windows Server** ဖြစ်နေတာကြောင့် RDP နဲ့ manually deploy လုပ်ရမယ်။

---

## 🚀 Quick Deploy (RDP Method)

### Step 1: RDP Connect လုပ်ပါ

1. **Remote Desktop Connection** ဖွင့်ပါ
   - `Win + R` → `mstsc` → Enter
   - Or Start Menu → Search "Remote Desktop"

2. **VPS IP ထည့်ပါ**
   ```
   18.138.169.114
   ```

3. **Login** လုပ်ပါ
   - Username: `Administrator`
   - Password: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`

---

### Step 2: VPS မှာ PowerShell ဖွင့်ပါ

1. **PowerShell as Administrator** ဖွင့်ပါ
   - Right-click Start → Windows PowerShell (Admin)

2. **Project folder** create လုပ်ပါ
   ```powershell
   cd C:\
   mkdir Azone
   cd Azone
   ```

---

### Step 3: Code Upload လုပ်ပါ

**Method 1: Copy-Paste (အလွယ်ဆုံး)**

1. **Local PC** မှာ:
   - `C:\Users\User\Desktop\Azone` folder ကို ZIP လုပ်ပါ
   - RDP session မှာ paste လုပ်ပါ
   - Extract လုပ်ပါ `C:\Azone`

**Method 2: Git Clone (If Git installed)**

```powershell
cd C:\Azone
git clone https://github.com/Apaing9611-arch/azone.git .
```

**Method 3: Network Share**

Local PC မှာ share folder လုပ်ပြီး VPS က network drive နဲ့ access လုပ်ပါ။

---

### Step 4: Install Python (If not installed)

1. **Download Python**:
   - https://www.python.org/downloads/
   - Download Python 3.11 or 3.12

2. **Install**:
   - ✅ **"Add Python to PATH"** check လုပ်ပါ!
   - Click "Install Now"

3. **Verify**:
   ```powershell
   python --version
   pip --version
   ```

---

### Step 5: Install Dependencies

```powershell
cd C:\Azone
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 6: Configure Domain

```powershell
cd C:\Azone

# Create .env file
@"
DOMAIN=paing.xyz
USE_HTTPS=True
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
"@ | Out-File -FilePath .env -Encoding utf8
```

---

### Step 7: Start Server

```powershell
cd C:\Azone
python web_app.py
```

**Server start ဖြစ်ရင်:**
- ✅ `http://localhost:5000` access လုပ်လို့ရမယ်
- ✅ `http://18.138.169.114:5000` access လုပ်လို့ရမယ်

---

### Step 8: Configure Windows Firewall

**PowerShell as Administrator** မှာ:

```powershell
# Allow port 5000
New-NetFirewallRule -DisplayName "AZone Flask 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Allow port 80 (if using HTTP)
New-NetFirewallRule -DisplayName "AZone Flask 80" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# Allow port 443 (if using HTTPS)
New-NetFirewallRule -DisplayName "AZone Flask 443" -Direction Inbound -LocalPort 443 -Protocol TCP -Action Allow
```

---

### Step 9: 24/7 Service Setup (Optional)

**Windows Service** အဖြစ် run လုပ်ရန်:

1. **NSSM Download**:
   - https://nssm.cc/download
   - Extract to `C:\nssm`

2. **Install Service**:
   ```powershell
   cd C:\nssm\win64
   .\nssm install AZoneBot "C:\Python311\python.exe" "C:\Azone\web_app.py"
   .\nssm set AZoneBot AppDirectory "C:\Azone"
   .\nssm set AZoneBot AppStdout "C:\Azone\logs\output.log"
   .\nssm set AZoneBot AppStderr "C:\Azone\logs\error.log"
   .\nssm start AZoneBot
   ```

**Or use Task Scheduler** (Built-in):

1. Open **Task Scheduler** (`taskschd.msc`)
2. Create Task:
   - **General**: Run whether user is logged on or not
   - **Triggers**: At startup
   - **Actions**: Start program
     - Program: `C:\Python311\python.exe`
     - Arguments: `C:\Azone\web_app.py`
     - Start in: `C:\Azone`
   - **Settings**: Restart on failure

---

## ✅ Test Access

### From Local PC:

```powershell
# Test connection
curl http://18.138.169.114:5000

# Or browser
# http://18.138.169.114:5000
```

### From Phone:

```
http://18.138.169.114:5000
```

---

## 🔧 Troubleshooting

### Server Not Starting?

1. **Check Python**:
   ```powershell
   python --version
   ```

2. **Check dependencies**:
   ```powershell
   pip list
   ```

3. **Check errors**:
   ```powershell
   cd C:\Azone
   python web_app.py
   # Check error messages
   ```

### Port Not Accessible?

1. **Check firewall**:
   ```powershell
   Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*AZone*"}
   ```

2. **Check if port is listening**:
   ```powershell
   netstat -ano | findstr :5000
   ```

3. **Check AWS Security Group**:
   - AWS Console → EC2 → Security Groups
   - Allow inbound: Port 5000, 80, 443

### Domain Not Working?

1. **Check .env file**:
   ```powershell
   Get-Content C:\Azone\.env
   ```

2. **Check DNS**:
   ```powershell
   nslookup paing.xyz
   ```

3. **Check IIS/Nginx** (if using reverse proxy):
   - Configure to proxy to `localhost:5000`

---

## 📝 Summary

| Step | Action | Status |
|------|--------|--------|
| 1 | RDP Connect | ✅ |
| 2 | Upload Code | ✅ |
| 3 | Install Python | ✅ |
| 4 | Install Dependencies | ✅ |
| 5 | Configure Domain | ✅ |
| 6 | Start Server | ✅ |
| 7 | Configure Firewall | ✅ |
| 8 | Test Access | ✅ |

---

## 🎉 Success!

Deploy လုပ်ပြီးရင်:
- ✅ PC off ရင်လည်း server run လုပ်နေမယ်
- ✅ Phone က `http://18.138.169.114:5000` access လုပ်လို့ရမယ်
- ✅ 24/7 available

**Next**: Configure domain DNS to point to `18.138.169.114` for `paing.xyz`! 🚀

