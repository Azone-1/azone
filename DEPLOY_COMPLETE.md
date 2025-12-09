# 🚀 AZone Complete Deployment Guide (4 Steps)

## ✅ အကုန်လုံး Setup လုပ်ရန် Guide

---

## 📋 Step 1: VPS Deployment (Railway.app)

### 1.1 GitHub Repository Setup

**PowerShell မှာ run ပါ:**

```powershell
cd C:\Users\User\Desktop\Azone

# Git initialize (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AZone Bot Builder"

# Add GitHub remote (YOUR_USERNAME ကို replace လုပ်ပါ)
git remote add origin https://github.com/YOUR_USERNAME/azone.git

# Push to GitHub
git push -u origin main
```

**Note:** GitHub account မရှိရင် https://github.com မှာ account ဖွင့်ပါ

---

### 1.2 Railway.app Deploy

1. **https://railway.app/** → "Start a New Project"
2. **"Deploy from GitHub repo"** → GitHub login
3. **Your `azone` repository** select
4. **Wait 2-3 minutes** → Automatic deploy!

---

### 1.3 Environment Variables Setup

Railway dashboard → Your project → **Variables** tab:

**Add these variables:**

```
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key-here
DEBUG=False
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

**Important:** `SECRET_KEY` ကို strong random string နဲ့ replace လုပ်ပါ

---

## 📋 Step 2: Domain Setup (paing.xyz)

### 2.1 Railway Custom Domain

1. Railway dashboard → **Settings** → **Domains**
2. **"Add Custom Domain"** → `paing.xyz`
3. Railway က DNS records ပေးပါမယ် (CNAME record)

---

### 2.2 Domain Provider DNS Configuration

Domain provider (Namecheap, GoDaddy, etc.) မှာ:

**CNAME Record:**
```
Type: CNAME
Name: @ (or leave blank for root domain)
Value: your-project.up.railway.app
TTL: 3600
```

**WWW Subdomain:**
```
Type: CNAME
Name: www
Value: your-project.up.railway.app
TTL: 3600
```

**Note:** Railway dashboard မှာ exact CNAME value ကို copy လုပ်ပါ

---

### 2.3 Wait for DNS Propagation

- **5-10 minutes** စောင့်ပါ
- DNS propagation check: https://dnschecker.org
- `paing.xyz` ကို search လုပ်ပြီး CNAME record ပေါ်ရင် ready

---

## 📋 Step 3: 24/7 Running Setup

### 3.1 Railway Auto-Restart (Automatic)

Railway.app က **automatic** အားဖြင့်:
- ✅ Auto-restart on failure
- ✅ Health checks
- ✅ 24/7 running
- ✅ Zero downtime

**No additional setup needed!** Railway handles everything.

---

### 3.2 Monitoring (Optional)

Railway dashboard မှာ:
- **Metrics** tab → CPU, Memory, Network usage
- **Logs** tab → Real-time logs
- **Deployments** tab → Deployment history

---

## 📋 Step 4: Complete Configuration & Testing

### 4.1 Verify Domain

**Browser မှာ test လုပ်ပါ:**
- `https://paing.xyz` → Dashboard ပေါ်ရင် ✅
- `https://www.paing.xyz` → Same dashboard ✅

---

### 4.2 Test Webhook URL

**Facebook Webhook:**
```
https://paing.xyz/webhook/facebook
```

**Test command:**
```bash
curl "https://paing.xyz/webhook/facebook?hub.mode=subscribe&hub.verify_token=azone_bot_verify_token&hub.challenge=test123"
```

**Expected:** `test123` response

---

### 4.3 Facebook Webhook Configuration

1. **Facebook Developer Console** → Your App
2. **Messenger** → **Settings** → **Webhooks**
3. **Add Callback URL:**
   ```
   https://paing.xyz/webhook/facebook
   ```
4. **Verify Token:**
   ```
   azone_bot_verify_token
   ```
5. **Subscribe to events:**
   - `messages`
   - `messaging_postbacks`
   - `messaging_optins`

---

## 🎉 Done! All 4 Steps Complete

### ✅ What You Have Now:

1. ✅ **VPS Deployment** - Railway.app (24/7 running)
2. ✅ **Domain Setup** - `https://paing.xyz` (with SSL)
3. ✅ **24/7 Running** - Automatic (Railway handles it)
4. ✅ **Complete Configuration** - Webhooks, SSL, Environment variables

---

## 📱 Daily Usage

### Code Updates:

```powershell
cd C:\Users\User\Desktop\Azone

# Edit your code...

# Commit and push
git add .
git commit -m "Your update message"
git push
```

**Railway auto-deploys in 2-3 minutes!** ✅

---

## 🔗 Important URLs

- **Main App**: `https://paing.xyz`
- **Dashboard**: `https://paing.xyz/dashboard`
- **Facebook Webhook**: `https://paing.xyz/webhook/facebook`
- **Railway Dashboard**: https://railway.app

---

## 💰 Cost

- **Railway Free Tier**: $5 credit/month
- **Your App**: ~$0-2/month (usually free!)
- **Domain**: Already purchased ✅

---

## ✅ Checklist

- [ ] GitHub repository created and pushed
- [ ] Railway.app project deployed
- [ ] Environment variables configured
- [ ] Custom domain added in Railway
- [ ] DNS CNAME records configured
- [ ] Domain working (`https://paing.xyz`)
- [ ] Webhook URL tested
- [ ] Facebook webhook configured
- [ ] All features working

---

## 🆘 Troubleshooting

### Domain Not Working?
- Check DNS propagation: https://dnschecker.org
- Wait 10-15 minutes for DNS propagation
- Verify CNAME record in domain provider

### Server Not Running?
- Check Railway dashboard → Logs
- Verify environment variables
- Check Railway status page

### Webhook Not Working?
- Verify `DOMAIN=paing.xyz` in Railway variables
- Check webhook URL: `https://paing.xyz/webhook/facebook`
- Test with curl command above

---

## 🎯 Next Steps

After setup complete:
1. ✅ Test all features
2. ✅ Configure Facebook Messenger bot
3. ✅ Set up Telegram bot (optional)
4. ✅ Start using your bot!

**Everything is ready!** 🚀
