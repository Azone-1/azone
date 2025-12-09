# ⚡ Quick Deploy - 5 Minutes Setup

## 🎯 Goal: Deploy AZone to Railway.app with paing.xyz domain

---

## Step 1: Run Setup Script (1 minute)

**PowerShell မှာ:**

```powershell
cd C:\Users\User\Desktop\Azone
.\SETUP_RAILWAY.ps1
```

---

## Step 2: GitHub Push (2 minutes)

```powershell
# If git not initialized
git init

# Add files
git add .

# Commit
git commit -m "AZone Bot Builder - Ready for Railway"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/azone.git

# Push
git push -u origin main
```

---

## Step 3: Railway Deploy (1 minute)

1. **https://railway.app** → "Start a New Project"
2. **"Deploy from GitHub repo"** → Select `azone`
3. **Wait 2-3 minutes** → Done!

---

## Step 4: Environment Variables (1 minute)

Railway dashboard → **Variables** tab:

```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=change-this-to-random-string
GEMINI_API_KEY=your-key-here
DEBUG=False
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

---

## Step 5: Custom Domain (1 minute)

1. Railway → **Settings** → **Domains**
2. **"Add Custom Domain"** → `paing.xyz`
3. Copy CNAME value from Railway
4. Domain provider → Add CNAME record
5. Wait 5-10 minutes

---

## ✅ Done!

**Your app is now:**
- ✅ Running 24/7 on Railway
- ✅ Available at `https://paing.xyz`
- ✅ Auto-deploy on git push
- ✅ HTTPS enabled automatically

**Webhook URL:** `https://paing.xyz/webhook/facebook`

---

## 📝 Next: Configure Facebook Webhook

1. Facebook Developer → Your App
2. Messenger → Webhooks
3. Callback URL: `https://paing.xyz/webhook/facebook`
4. Verify Token: `azone_bot_verify_token`

**Done!** 🎉
