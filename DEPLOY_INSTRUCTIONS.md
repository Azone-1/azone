# 🚀 VPS Deployment Instructions

## Problem: Password ရိုက်ရတာ အဆင်မပြေဘူး

## Solution: 2 Steps

---

## Step 1: Setup SSH Key (One Time Only)

**Run this ONCE to avoid passwords forever:**

```powershell
powershell -ExecutionPolicy Bypass -File SETUP_SSH_KEY.ps1
```

**What it does:**
- ✅ Generates SSH key
- ✅ Copies to VPS (password ရိုက်ပေးရမယ် - 1 ခါပဲ)
- ✅ Setup SSH config
- ✅ Test passwordless connection

**Password:** `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(` (Type manually - 1 time only)

**After this:** No more passwords needed! 🎉

---

## Step 2: Deploy to VPS

**Run this to deploy:**

```powershell
powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1
```

**What it does:**
1. ✅ Checks VPS folder
2. ✅ Uploads MASTER_DEPLOY.sh (if needed)
3. ✅ Runs MASTER_DEPLOY.sh
4. ✅ Sets up PM2, Nginx, SSL
5. ✅ Shows status

**If SSH key setup worked:** No password needed!  
**If SSH key didn't work:** Type password when asked

---

## Alternative: Manual Deployment

**If scripts don't work, do it manually:**

### 1. Connect to VPS:
```powershell
ssh Administrator@18.138.169.114
```
Password: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`

### 2. On VPS, run:
```bash
cd ~/Azone
chmod +x MASTER_DEPLOY.sh
bash MASTER_DEPLOY.sh
```

### 3. Wait 10-15 minutes for deployment

### 4. Check status:
```bash
pm2 status
sudo systemctl status nginx
```

---

## After Deployment:

**Access your bot:**
- 🌐 http://paing.xyz (No port 8000!)
- 🌐 http://18.138.169.114
- 🔒 https://paing.xyz (After SSL)

**Check logs:**
```bash
pm2 logs azone-bot
sudo tail -f /var/log/nginx/paing.xyz.error.log
```

---

## Troubleshooting:

### SSH Connection Reset:
```powershell
# Test connection
Test-NetConnection -ComputerName 18.138.169.114 -Port 22
```

### Password Still Asked:
- Run `SETUP_SSH_KEY.ps1` again
- Check SSH key exists: `ls ~/.ssh/id_ed25519_azone*`
- Check SSH config: `cat ~/.ssh/config`

### MASTER_DEPLOY.sh Not Found:
```powershell
# Upload manually
scp MASTER_DEPLOY.sh Administrator@18.138.169.114:~/Azone/
```

---

## Quick Commands:

| Task | Command |
|------|---------|
| Setup SSH Key | `powershell -ExecutionPolicy Bypass -File SETUP_SSH_KEY.ps1` |
| Deploy | `powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1` |
| Connect VPS | `ssh azone-vps` |
| Check Status | `ssh azone-vps "pm2 status"` |
| View Logs | `ssh azone-vps "pm2 logs azone-bot"` |

---

**Recommended:** Run Step 1 first (SSH key setup), then Step 2 (deployment) 🚀

