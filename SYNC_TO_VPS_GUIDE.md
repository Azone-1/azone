# 🚀 Local to VPS Sync Guide

Bot Builder code ကို Local PC ကနေ VPS ကို sync လုပ်နည်း

---

## 📋 Method 1: Git Sync (Recommended)

### Step 1: Local PC မှာ Code Push လုပ်ပါ

```powershell
# Local PC PowerShell မှာ
cd C:\Users\User\Desktop\Azone

# Sync script run လုပ်ပါ
.\SYNC_TO_VPS.ps1
```

Script က:
- ✅ Git status check လုပ်မယ်
- ✅ Changes commit လုပ်မယ်
- ✅ GitHub ကို push လုပ်မယ်

### Step 2: VPS မှာ Code Pull လုပ်ပါ

**RDP Connect လုပ်ပါ:**
- IP: `18.138.169.114`
- Username: `Administrator`
- Password: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`

**VPS PowerShell (Admin) မှာ:**

```powershell
cd C:\Azone

# Update script run လုပ်ပါ
.\VPS_PULL_UPDATE.ps1
```

Script က:
- ✅ Flask server stop လုပ်မယ်
- ✅ GitHub ကနေ latest code pull လုပ်မယ်
- ✅ Dependencies update လုပ်မယ်
- ✅ Server test လုပ်မယ်

### Step 3: Server Start လုပ်ပါ

```powershell
cd C:\Azone
python web_app.py
```

---

## 📋 Method 2: Manual Copy (Git မရှိရင်)

### Step 1: Local PC မှာ ZIP လုပ်ပါ

1. `C:\Users\User\Desktop\Azone` folder ကို right-click
2. **Send to → Compressed (zipped) folder**
3. `Azone.zip` file ကို create လုပ်ပါ

### Step 2: RDP နဲ့ VPS ကို Connect လုပ်ပါ

1. **Remote Desktop Connection** ဖွင့်ပါ
   - `Win + R` → `mstsc` → Enter
2. **VPS IP** ထည့်ပါ: `18.138.169.114`
3. **Login** လုပ်ပါ

### Step 3: ZIP File Copy လုပ်ပါ

1. Local PC က `Azone.zip` ကို **Copy** လုပ်ပါ
2. RDP session မှာ **Paste** လုပ်ပါ (သို့မဟုတ် drag & drop)
3. `C:\Azone` folder ထဲကို copy လုပ်ပါ

### Step 4: Extract လုပ်ပါ

```powershell
# VPS PowerShell (Admin) မှာ
cd C:\Azone
Expand-Archive -Path Azone.zip -DestinationPath . -Force
```

### Step 5: Setup Run လုပ်ပါ

```powershell
cd C:\Azone
.\WINDOWS_VPS_SETUP.ps1
```

---

## 🌐 Access Bot Builder

Sync လုပ်ပြီးရင်:

1. **Server Start:**
   ```powershell
   cd C:\Azone
   python web_app.py
   ```

2. **Browser မှာ ဖွင့်ပါ:**
   - Bot Builder: `http://18.138.169.114:5000/bot-builder`
   - Login: `http://18.138.169.114:5000/login`
   - Username: `admin`
   - Password: `admin123`

---

## 🔄 Quick Sync (Next Time)

**Local PC:**
```powershell
cd C:\Users\User\Desktop\Azone
.\SYNC_TO_VPS.ps1
```

**VPS:**
```powershell
cd C:\Azone
.\VPS_PULL_UPDATE.ps1
python web_app.py
```

---

## ⚠️ Troubleshooting

### Git Push Failed
- GitHub repository URL check လုပ်ပါ
- Internet connection check လုပ်ပါ
- Git credentials check လုပ်ပါ

### VPS Pull Failed
- Git installed ဖြစ်ရဲ့လား check လုပ်ပါ
- `.git` folder ရှိရဲ့လား check လုပ်ပါ
- Manual copy method သုံးပါ

### Server Not Starting
- Python installed ဖြစ်ရဲ့လား check လုပ်ပါ
- Port 5000 available ဖြစ်ရဲ့လား check လုပ်ပါ
- `.env` file ရှိရဲ့လား check လုပ်ပါ

---

## ✅ Success Checklist

- [ ] Local code pushed to GitHub
- [ ] VPS code pulled successfully
- [ ] Dependencies installed/updated
- [ ] Server starts without errors
- [ ] Bot Builder accessible at `/bot-builder`
- [ ] Test Chat widget appears in Bot Builder

---

**Bot Builder ကို VPS မှာ access လုပ်နိုင်ပါပြီ!** 🎉

