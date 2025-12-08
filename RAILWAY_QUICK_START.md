# Railway.app Quick Start (5 Minutes) 🚀

## 🎯 Goal
VPS UI မသွားဘဲ, command line မသုံးဘဲ, **One Click Deploy**

---

## ✅ Step-by-Step (မြန်မာလို)

### Step 1: GitHub Repository (2 minutes)

1. **GitHub.com** → Login
2. **New Repository** button
3. Repository name: `azone`
4. **Public** or **Private** (your choice)
5. **Create repository**

---

### Step 2: Push Local Project to GitHub (2 minutes)

**PowerShell မှာ:**

```powershell
cd C:\Users\User\Desktop\Azone

# Initialize git (if not already)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit - Azone Bot Builder"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/azone.git

# Push to GitHub
git push -u origin main
```

**Note:** `YOUR_USERNAME` ကို သင့်ရဲ့ GitHub username နဲ့ replace လုပ်ပါ

---

### Step 3: Railway.app Deploy (1 minute)

1. **https://railway.app/** → "Start a New Project"
2. **"Deploy from GitHub repo"** → GitHub login
3. **Your `azone` repository** select
4. **Wait 2-3 minutes** → Automatic deploy!

---

### Step 4: Environment Variables (1 minute)

Railway dashboard → Your project → **Variables** tab:

**Add these:**
```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

---

### Step 5: Custom Domain (2 minutes)

1. Railway dashboard → **Settings** → **Domains**
2. **"Add Custom Domain"** → `paing.xyz`
3. Railway က DNS records ပေးပါမယ်
4. Domain provider မှာ **CNAME record** ထည့်ပါ
5. **Wait 5-10 minutes** → Done! ✅

---

## 🎉 Done!

**Now you have:**
- ✅ 24/7 running (automatic)
- ✅ Auto-deploy (Git push = deploy)
- ✅ HTTPS (automatic SSL)
- ✅ Custom domain: `https://paing.xyz`
- ✅ Webhook: `https://paing.xyz/webhook/facebook`

---

## 📋 Daily Usage (After Setup)

### Code Update:

1. **Local code edit**
2. **Git push:**
   ```powershell
   git add .
   git commit -m "Update"
   git push
   ```
3. **Done!** Railway auto-deploy (2-3 minutes)

**No VPS access needed!** ✅

---

## 💰 Cost

- **Free tier**: $5 credit/month
- **Your app**: ~$0-2/month (free tier နဲ့ လုံလောက်ပါတယ်)

---

## ✅ Advantages

- ✅ **No VPS Management** - Server management မလိုဘူး
- ✅ **No SSH/Commands** - Web UI only
- ✅ **24/7 Running** - Automatic
- ✅ **Auto-Deploy** - Git push = deploy
- ✅ **Automatic HTTPS** - SSL automatic
- ✅ **Free Tier** - $5 credit/month

---

## 🎯 Perfect for Your Needs!

**Railway.app = No VPS UI, No Commands, Just Deploy!** 🚀
