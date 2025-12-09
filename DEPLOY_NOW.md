# 🚀 Deploy Now - Payment ထည့်ပြီးရင် (5 Minutes)

## ✅ အကုန်လုံး Ready! ဒီ 5 ချက်လုပ်ပါ:

---

### 1️⃣ Railway Deploy (1 minute)

1. **https://railway.app** → "Start a New Project"
2. **"Deploy from GitHub repo"** → GitHub login
3. **Select:** `Apaing9611-arch/azone` repository
4. **Click Deploy** → Wait 2-3 minutes

**✅ Code automatically deploys from GitHub!**

---

### 2️⃣ Add Payment (1 minute)

1. Railway dashboard → **Settings** → **Billing**
2. **"Add Payment Method"**
3. Enter credit card/PayPal
4. **$5 free credit** added automatically

**✅ Payment done!**

---

### 3️⃣ Environment Variables (1 minute)

Railway → Your project → **Variables** tab → **Add New Variable**

**Copy from `RAILWAY_ENV_VARS.txt` or copy these:**

```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-random-secret-key-min-32-chars
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

**Important:** 
- `SECRET_KEY` ကို random string နဲ့ replace လုပ်ပါ
- Example: `openssl rand -hex 32` (PowerShell: `[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))`)

**✅ Variables added!**

---

### 4️⃣ Custom Domain (1 minute)

1. Railway → **Settings** → **Domains**
2. **"Add Custom Domain"**
3. Type: `paing.xyz`
4. Railway shows **CNAME value** (copy this!)

**✅ Domain added!**

---

### 5️⃣ DNS Configuration (1 minute)

**Domain Provider** (Namecheap/GoDaddy/etc.) → DNS Management:

**Add CNAME Record:**
```
Type: CNAME
Name: @ (or blank for root domain)
Value: [Railway's CNAME value - paste here]
TTL: 3600
```

**Add WWW Subdomain:**
```
Type: CNAME
Name: www
Value: [Same Railway CNAME value]
TTL: 3600
```

**Save** → Wait 5-10 minutes for DNS propagation

**✅ DNS configured!**

---

## 🎉 Done!

**Visit:** `https://paing.xyz` → Your app is running! 🚀

---

## ✅ What You Get:

- ✅ **24/7 Running** - Automatic
- ✅ **Auto-Deploy** - Git push = auto deploy
- ✅ **HTTPS/SSL** - Automatic
- ✅ **Webhook Ready** - `https://paing.xyz/webhook/facebook`
- ✅ **Dashboard** - `https://paing.xyz/dashboard`

---

## 📋 Quick Reference:

- **GitHub Repo**: https://github.com/Apaing9611-arch/azone
- **Railway Dashboard**: https://railway.app
- **Environment Vars**: See `RAILWAY_ENV_VARS.txt`
- **Detailed Guide**: See `STATUS_READY.md`

---

## 🆘 Troubleshooting:

### App Not Deploying?
- Check Railway → Logs tab
- Verify environment variables are correct
- Check `PORT` variable is set to `5000`

### Domain Not Working?
- Check DNS propagation: https://dnschecker.org
- Verify CNAME record in domain provider
- Wait 10-15 minutes for DNS

### Webhook Not Working?
- Verify `DOMAIN=paing.xyz` in Railway variables
- Check webhook URL: `https://paing.xyz/webhook/facebook`
- Test with curl command

---

## ✅ Everything is Ready!

**မနက်ဖြန် payment ထည့်ပြီးရင် 5 မိနစ်အတွင်း deploy လုပ်လို့ရပါတယ်!** 🚀

**All your code is saved on GitHub and ready to deploy!** ✅
