# 🎯 AZone - စတင်ရန် Guide (မြန်မာလို)

## ✅ အကုန်လုံး Ready ဖြစ်ပြီးသား!

---

## 📋 သင်လုပ်ရမဲ့ ၅ ချက်:

### 1️⃣ Setup Script Run လုပ်ပါ (1 မိနစ်)

**PowerShell မှာ:**

```powershell
cd C:\Users\User\Desktop\Azone
.\SETUP_RAILWAY.ps1
```

---

### 2️⃣ GitHub ကို Push လုပ်ပါ ✅ DONE!

**✅ Already Completed!**
- Repository: `https://github.com/Apaing9611-arch/azone.git`
- Branch: `main`
- Status: All files pushed successfully

**Note:** If you need to update code later:
```powershell
git add .
git commit -m "Update"
git push
```

---

### 3️⃣ Railway.app မှာ Deploy လုပ်ပါ (1 မိနစ်)

1. **https://railway.app** → "Start a New Project"
2. **"Deploy from GitHub repo"** → GitHub login
3. **Your `azone` repository** select
4. **2-3 မိနစ် စောင့်ပါ** → Automatic deploy!

---

### 4️⃣ Environment Variables ထည့်ပါ (1 မိနစ်)

Railway dashboard → Your project → **Variables** tab:

**ဒီ variables တွေ add လုပ်ပါ:**

```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-random-secret-key-change-this
GEMINI_API_KEY=your-gemini-api-key-here
DEBUG=False
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

**Important:** `SECRET_KEY` ကို strong random string နဲ့ replace လုပ်ပါ

---

### 5️⃣ Domain Setup လုပ်ပါ (2 မိနစ်)

1. **Railway dashboard** → **Settings** → **Domains**
2. **"Add Custom Domain"** → `paing.xyz` ရိုက်ပါ
3. Railway က CNAME value ပေးပါမယ် (e.g., `xyz.up.railway.app`)
4. **Domain provider** (Namecheap, GoDaddy, etc.) မှာ:
   - DNS Management → CNAME record add လုပ်ပါ
   - Name: `@` (သို့မဟုတ် blank)
   - Value: Railway က ပေးတဲ့ CNAME value
   - TTL: 3600
5. **5-10 မိနစ် စောင့်ပါ** → DNS propagation

---

## ✅ ပြီးရင်:

- ✅ **VPS Deployment** - Railway.app (24/7 running)
- ✅ **Domain** - `https://paing.xyz` (SSL automatic)
- ✅ **24/7 Running** - Automatic (Railway handles)
- ✅ **Webhook** - `https://paing.xyz/webhook/facebook`

---

## 🔗 Important URLs:

- **Main App**: `https://paing.xyz`
- **Dashboard**: `https://paing.xyz/dashboard`
- **Webhook**: `https://paing.xyz/webhook/facebook`

---

## 📖 Detailed Guides:

- **Quick Deploy**: `QUICK_DEPLOY.md` (5 minutes)
- **Complete Guide**: `DEPLOY_COMPLETE.md` (detailed)
- **Final Guide**: `FINAL_SETUP_GUIDE.md` (comprehensive)

---

## 🎉 Done!

**အကုန်လုံး ready ဖြစ်ပြီးသား!** 

**Next:** Railway မှာ deploy လုပ်ပြီး `https://paing.xyz` ကို visit လုပ်ပါ! 🚀
