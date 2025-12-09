# 🚀 VPS Deployment - Quick Guide

## ❓ မေးခွန်းများ

### 1. PC off ရပ်မှာလား?

**Local PC မှာ run လုပ်ထားရင်:**
- ❌ PC off ရင် server ရပ်သွားမယ်
- ❌ Phone က domain နဲ့ access လုပ်လို့မရဘူး (localhost only)

**VPS မှာ deploy လုပ်ထားရင်:**
- ✅ PC off ရင်လည်း server run လုပ်နေမယ် (24/7)
- ✅ Phone က domain နဲ့ access လုပ်လို့ရမယ်
- ✅ ဘယ်နေရာက ဖြစ်ဖြစ် access လုပ်လို့ရမယ်

---

### 2. Phone က domain နဲ့ ကြည့်မရသေးဘူးလား?

**Local PC မှာ run လုပ်ထားရင်:**
- ❌ Phone က `http://localhost:5000` access လုပ်လို့မရဘူး
- ❌ Domain နဲ့ access လုပ်လို့မရဘူး

**VPS မှာ deploy လုပ်ထားရင်:**
- ✅ Phone က `https://paing.xyz` access လုပ်လို့ရမယ်
- ✅ Domain နဲ့ access လုပ်လို့ရမယ်
- ✅ HTTPS (SSL) နဲ့ secure access လုပ်လို့ရမယ်

---

### 3. VPS ကို သွားလို့ရလား?

**ရပါတယ်!** ✅

VPS Info:
- **IP**: `18.138.169.114`
- **Domain**: `paing.xyz`
- **User**: `Administrator`
- **Status**: Ready to deploy

---

## 🚀 Quick Deploy (3 Steps)

### Step 1: Run Deployment Script

**PowerShell** မှာ:

```powershell
cd C:\Users\User\Desktop\Azone
.\DEPLOY_TO_VPS_NOW.ps1
```

**သို့မဟုတ်:**

```powershell
powershell -ExecutionPolicy Bypass -File DEPLOY_TO_VPS_NOW.ps1
```

### Step 2: Wait for Deployment

- ⏱️ 10-15 minutes စောင့်ပါ
- Password prompt ရင်: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`
- Script က automatically:
  - ✅ Files upload လုပ်မယ်
  - ✅ Dependencies install လုပ်မယ်
  - ✅ Domain configure လုပ်မယ်
  - ✅ Server start လုပ်မယ်

### Step 3: Test Access

**Phone/Computer** မှာ:

```
https://paing.xyz
http://18.138.169.114
```

---

## ✅ After Deployment

### PC Off ရင်လည်း:
- ✅ Server VPS မှာ run လုပ်နေမယ်
- ✅ Phone က domain နဲ့ access လုပ်လို့ရမယ်
- ✅ 24/7 available

### Phone Access:
- ✅ `https://paing.xyz` - Main app
- ✅ `https://paing.xyz/dashboard` - Dashboard
- ✅ `https://paing.xyz/webhook/facebook` - Webhook

---

## 🔧 Manual Deployment (If Script Fails)

### 1. Connect to VPS

```powershell
ssh Administrator@18.138.169.114
# Password: IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(
```

### 2. Upload Files

```powershell
# From local PC
scp -r C:\Users\User\Desktop\Azone\* Administrator@18.138.169.114:~/Azone/
```

### 3. Run Setup

```bash
# On VPS
cd ~/Azone
chmod +x QUICK_VPS_SETUP.sh
bash QUICK_VPS_SETUP.sh
```

### 4. Configure Domain

```bash
# On VPS
cd ~/Azone
echo "DOMAIN=paing.xyz" >> .env
echo "USE_HTTPS=True" >> .env
```

### 5. Start Server

```bash
# On VPS
pm2 start web_app.py --name azone-bot
pm2 save
pm2 startup
```

---

## 📊 Check Status

### On VPS:

```bash
# Check if server is running
pm2 list

# Check logs
pm2 logs azone-bot

# Check ports
netstat -tuln | grep -E ":(80|443|5000)"
```

### From Local PC:

```powershell
# Test connection
curl http://18.138.169.114
curl https://paing.xyz
```

---

## 🆘 Troubleshooting

### Connection Failed?

1. **Check VPN** (if required)
2. **Check VPS status** (AWS console)
3. **Check firewall** (port 22, 80, 443 open)

### Domain Not Working?

1. **Check DNS**:
   ```bash
   nslookup paing.xyz
   ```

2. **Check .env file**:
   ```bash
   cat ~/Azone/.env | grep DOMAIN
   ```

3. **Check Nginx**:
   ```bash
   sudo systemctl status nginx
   ```

### Server Not Starting?

1. **Check logs**:
   ```bash
   pm2 logs azone-bot
   ```

2. **Check Python**:
   ```bash
   python3 --version
   pip3 list
   ```

3. **Manual start**:
   ```bash
   cd ~/Azone
   python3 web_app.py
   ```

---

## ✅ Summary

| Question | Answer |
|----------|--------|
| PC off ရပ်မှာလား? | VPS deploy လုပ်ထားရင် PC off ရင်လည်း server run လုပ်နေမယ် ✅ |
| Phone က domain နဲ့ access လုပ်လို့ရလား? | VPS deploy လုပ်ထားရင် `https://paing.xyz` access လုပ်လို့ရမယ် ✅ |
| VPS ကို deploy လုပ်လို့ရလား? | ရပါတယ်! `DEPLOY_TO_VPS_NOW.ps1` run လုပ်ပါ ✅ |

---

## 🎉 Success!

Deploy လုပ်ပြီးရင်:
- ✅ PC off ရင်လည်း server run လုပ်နေမယ်
- ✅ Phone က domain နဲ့ access လုပ်လို့ရမယ်
- ✅ 24/7 available

**Next Step**: `DEPLOY_TO_VPS_NOW.ps1` run လုပ်ပါ! 🚀

