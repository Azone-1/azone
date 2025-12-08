# 🚀 Azone Project Deployment Guide
## Local PowerShell vs VPS Commands

---

## 📍 **LOCAL POWERSHELL (Windows) - လုပ်ရမယ့် အဆင့်တွေ**

### Step 1: SSH Key Setup (တစ်ကြိမ်သာ လုပ်ရမယ်)
```powershell
cd C:\Users\User\Desktop\Azone
powershell -ExecutionPolicy Bypass -File SETUP_SSH_KEY.ps1
```
**လုပ်ရမယ့်အရာ:**
- Password တစ်ကြိမ် ထည့်ရမယ်: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`
- SSH key generate လုပ်ပေးတယ်
- VPS ကို passwordless access setup လုပ်ပေးတယ်
- **ပြီးရင် password ထည့်စရာ မလိုတော့ဘူး!**

---

### Step 2: Files Upload (Sync to VPS)
```powershell
cd C:\Users\User\Desktop\Azone
powershell -ExecutionPolicy Bypass -File SYNC_TO_VPS.ps1
```
**လုပ်ရမယ့်အရာ:**
- Local files အားလုံးကို VPS ကို upload လုပ်တယ်
- Python files, templates, static files အားလုံး
- Progress ကို step-by-step ပြပေးတယ်

---

### Step 3: Run Deployment (VPS မှာ deployment လုပ်ခိုင်းတယ်)
```powershell
cd C:\Users\User\Desktop\Azone
powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1
```
**လုပ်ရမယ့်အရာ:**
- VPS ကို connect လုပ်တယ်
- MASTER_DEPLOY.sh ကို VPS မှာ run လုပ်ခိုင်းတယ်
- Status check လုပ်ပေးတယ်

---

## 🖥️ **VPS (Linux Server) - လုပ်ရမယ့် အဆင့်တွေ**

### Option A: Local PowerShell ကနေ Auto Run (အလွယ်ဆုံး)
Local PowerShell မှာ `SIMPLE_DEPLOY.ps1` run လုပ်ရင် VPS မှာ automatically run လုပ်ပေးတယ်။

---

### Option B: VPS ကို Manual Connect လုပ်ပြီး Run
```bash
# VPS ကို connect လုပ်တယ်
ssh Administrator@18.138.169.114
# သို့မဟုတ် (SSH key setup လုပ်ထားရင်)
ssh azone-vps

# Project folder ကို သွားတယ်
cd ~/Azone

# Deployment script ကို run လုပ်တယ်
chmod +x MASTER_DEPLOY.sh
bash MASTER_DEPLOY.sh
```

**VPS မှာ MASTER_DEPLOY.sh က လုပ်ပေးတာတွေ:**
1. ✅ System updates (apt update, upgrade)
2. ✅ Python dependencies install (requirements.txt)
3. ✅ Node.js & PM2 install
4. ✅ Flask app ကို PM2 နဲ့ start လုပ်တယ်
5. ✅ Nginx install & configure
6. ✅ Firewall setup
7. ✅ SSL certificate install (Let's Encrypt)

---

## 📋 **Complete Workflow (အဆင့်ဆင့်)**

### **Local PowerShell မှာ:**

#### 1️⃣ First Time Setup (တစ်ကြိမ်သာ)
```powershell
cd C:\Users\User\Desktop\Azone

# SSH key setup (password တစ်ကြိမ် ထည့်ရမယ်)
powershell -ExecutionPolicy Bypass -File SETUP_SSH_KEY.ps1
```

#### 2️⃣ Upload Files (ပြောင်းလဲထားတဲ့ files တွေ upload လုပ်တဲ့အခါ)
```powershell
cd C:\Users\User\Desktop\Azone

# Files အားလုံး sync လုပ်တယ်
powershell -ExecutionPolicy Bypass -File SYNC_TO_VPS.ps1
```

#### 3️⃣ Deploy (VPS မှာ deployment လုပ်တယ်)
```powershell
cd C:\Users\User\Desktop\Azone

# VPS မှာ deployment run လုပ်တယ်
powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1
```

---

### **VPS မှာ (Manual လုပ်ချင်ရင်):**

```bash
# Connect to VPS
ssh Administrator@18.138.169.114

# Go to project folder
cd ~/Azone

# Check files
ls -la

# Run deployment
bash MASTER_DEPLOY.sh

# Check status
pm2 status
pm2 logs azone-bot
sudo systemctl status nginx
```

---

## 🔍 **Useful Commands**

### **Local PowerShell:**
```powershell
# Check SSH key exists
Test-Path "$env:USERPROFILE\.ssh\id_ed25519_azone"

# Test VPS connection
ssh Administrator@18.138.169.114 "echo 'Connected!'"

# Quick file upload
scp web_app.py Administrator@18.138.169.114:~/Azone/
```

### **VPS (SSH ကနေ):**
```bash
# Check PM2 status
pm2 status
pm2 logs azone-bot
pm2 restart azone-bot

# Check Nginx
sudo systemctl status nginx
sudo nginx -t
sudo systemctl restart nginx

# Check ports
netstat -tuln | grep -E ":(80|443|8000)"

# View logs
tail -f ~/Azone/logs/pm2.log
sudo tail -f /var/log/nginx/paing.xyz.error.log
```

---

## 🌐 **Access Your Application**

After deployment, access at:
- **http://paing.xyz**
- **http://18.138.169.114**
- **https://paing.xyz** (if SSL installed)

---

## ⚠️ **Important Notes**

1. **First Time:** SETUP_SSH_KEY.ps1 ကို run လုပ်ပြီး password တစ်ကြိမ် ထည့်ရမယ်
2. **After Changes:** SYNC_TO_VPS.ps1 run လုပ်ပြီး files upload လုပ်ရမယ်
3. **Deploy:** SIMPLE_DEPLOY.ps1 run လုပ်ပြီး VPS မှာ deployment လုပ်ရမယ်
4. **VPS Manual:** VPS ကို SSH နဲ့ connect လုပ်ပြီး `bash MASTER_DEPLOY.sh` run လုပ်လို့ရတယ်

---

## 🎯 **Quick Start (အလွယ်ဆုံး)**

```powershell
# Local PowerShell မှာ - တစ်ခုပြီး တစ်ခု run လုပ်ပါ
cd C:\Users\User\Desktop\Azone

# 1. SSH setup (တစ်ကြိမ်သာ)
.\SETUP_SSH_KEY.ps1

# 2. Upload files
.\SYNC_TO_VPS.ps1

# 3. Deploy
.\SIMPLE_DEPLOY.ps1
```

**ဒါဆိုရင် အားလုံး အဆင်ပြေသွားပါပြီ! 🎉**
