# paing.xyz Quick Setup (အလွယ်ဆုံး)

## 🚀 3 Steps Only!

### Step 1: DNS Configuration

Domain provider (Namecheap/GoDaddy/etc.) မှာ:

**A Record:**
```
Type: A
Name: @
Value: 18.138.169.114 (or your VPS IP)
TTL: 3600
```

---

### Step 2: Environment Variable

VPS မှာ `.env` file (သို့မဟုတ် Railway environment variables):

```
DOMAIN=paing.xyz
USE_HTTPS=True
```

---

### Step 3: SSL Certificate (HTTPS)

**AWS VPS:**
```bash
sudo certbot certonly --standalone -d paing.xyz -d www.paing.xyz
```

**Railway.app:**
- Automatic (no setup needed) ✅

---

## ✅ Done!

Webhook URL: `https://paing.xyz/webhook/facebook`

---

## 🎯 Which VPS to Use?

### Option 1: Current AWS VPS (18.138.169.114)
- ✅ Already have
- ❌ Cost: ~15,000 MMK/month
- ❌ Setup: Manual

### Option 2: Railway.app (Recommended)
- ✅ Easy setup
- ✅ Free tier ($5 credit/month)
- ✅ Automatic HTTPS
- ✅ Auto-deploy

### Option 3: Oracle Cloud Free Tier
- ✅ Forever free
- ✅ Powerful (4 cores, 24GB RAM)
- ❌ Setup: Medium difficulty

---

## 💡 Recommendation

**Railway.app** ကို သုံးပါ:
1. Easy setup (10 minutes)
2. Automatic HTTPS
3. Free tier available
4. GitHub auto-deploy

**Cost**: Free tier နဲ့ လုံလောက်ပါတယ် ($5 credit/month)
