# ⚡ Quick Start - မနက်ဖြန် (5 Minutes)

## 🎯 Payment ထည့်ပြီးရင် ဒီ 5 ချက်လုပ်ပါ

---

### 1️⃣ Railway Deploy (2 minutes)

1. **https://railway.app** → "Start a New Project"
2. **"Deploy from GitHub repo"** → Login
3. **Select:** `Apaing9611-arch/azone`
4. **Wait 2-3 minutes** → Done!

---

### 2️⃣ Payment Add (1 minute)

1. Railway → **Settings** → **Billing**
2. **Add payment method**
3. **$5 credit** added automatically

---

### 3️⃣ Environment Variables (1 minute)

Railway → **Variables** tab → **Add these:**

```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=change-this-random-string-32-chars-minimum
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

**Important:** `SECRET_KEY` ကို random string နဲ့ replace လုပ်ပါ

---

### 4️⃣ Custom Domain (1 minute)

1. Railway → **Settings** → **Domains**
2. **"Add Custom Domain"** → `paing.xyz`
3. Copy **CNAME value** from Railway

---

### 5️⃣ DNS Configuration (1 minute)

**Domain provider** (Namecheap/GoDaddy) → DNS Management:

**CNAME Record:**
- Name: `@` (or blank)
- Value: Railway's CNAME value
- TTL: 3600

**WWW Subdomain:**
- Name: `www`
- Value: Same Railway CNAME value
- TTL: 3600

**Wait 5-10 minutes** → Done! ✅

---

## ✅ Done!

**Visit:** `https://paing.xyz` → Your app is running! 🚀

---

## 📋 What's Already Done:

- ✅ GitHub push completed
- ✅ All files ready
- ✅ Configuration ready
- ✅ Just need Railway payment!

**Everything is saved and ready!** ✅
