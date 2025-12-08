# paing.xyz Domain Setup Guide

## 🎯 Domain Information
- **Domain**: `paing.xyz`
- **Status**: Already purchased ✅
- **Webhook URL**: `https://paing.xyz/webhook/facebook`

---

## 📋 Step-by-Step Setup (အကုန် တစ်ခုထဲ)

### Step 1: Domain DNS Configuration

Domain provider (Namecheap, GoDaddy, etc.) မှာ DNS records ထည့်ရန်:

#### Option A: VPS IP Address (Direct)

**A Record:**
```
Type: A
Name: @ (or leave blank)
Value: Your VPS IP address (e.g., 18.138.169.114)
TTL: 3600 (or Auto)
```

**WWW Subdomain:**
```
Type: A
Name: www
Value: Your VPS IP address
TTL: 3600
```

#### Option B: Railway.app (CNAME)

**CNAME Record:**
```
Type: CNAME
Name: @
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

---

### Step 2: Project Configuration

#### Local Machine (.env file):

`.env` file ဖန်တီးရန် (သို့မဟုတ် update):

```env
# Domain Configuration
DOMAIN=paing.xyz
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# Database Paths
BOT_DB_PATH=bots.db
SCHEDULED_POSTS_DB_PATH=web_scheduled_posts.db

# Facebook Messenger Configuration
FACEBOOK_VERIFY_TOKEN=azone_bot_verify_token
```

#### VPS/Server (.env file):

VPS မှာ deploy လုပ်ရင် same `.env` file ကို upload လုပ်ပါ (သို့မဟုတ် environment variables သတ်မှတ်ပါ)

---

### Step 3: VPS Deployment Options

#### Option A: Current AWS VPS (18.138.169.114)

**DNS Configuration:**
1. Domain provider မှာ A record ထည့်ပါ:
   ```
   Type: A
   Name: @
   Value: 18.138.169.114
   ```

2. VPS မှာ `.env` file update လုပ်ပါ:
   ```bash
   nano .env
   # DOMAIN=paing.xyz ထည့်ပါ
   ```

3. SSL Certificate install လုပ်ပါ:
   ```bash
   sudo certbot certonly --standalone -d paing.xyz -d www.paing.xyz
   ```

4. Project restart လုပ်ပါ

---

#### Option B: Railway.app (Recommended - အလွယ်ဆုံး)

**Setup:**
1. Railway.app → New Project → Deploy from GitHub
2. Environment Variables ထည့်ပါ:
   ```
   DOMAIN=paing.xyz
   USE_HTTPS=True
   PORT=5000
   ```
3. Settings → Domains → Add Custom Domain
4. `paing.xyz` ထည့်ပါ
5. Railway က DNS records ပေးပါမယ်
6. Domain provider မှာ CNAME record ထည့်ပါ

**Advantages:**
- ✅ Automatic HTTPS (SSL)
- ✅ Auto-deploy from GitHub
- ✅ No server management
- ✅ Free tier available

---

#### Option C: Oracle Cloud Free Tier

**Setup:**
1. Oracle Cloud → Create Always Free VM
2. Project deploy လုပ်ပါ
3. DNS A record ထည့်ပါ (VPS IP)
4. SSL certificate install လုပ်ပါ
5. `.env` file မှာ `DOMAIN=paing.xyz` ထည့်ပါ

---

### Step 4: SSL Certificate (HTTPS)

#### Current AWS VPS:

```bash
# Install Certbot
sudo yum install certbot -y

# Get SSL certificate
sudo certbot certonly --standalone -d paing.xyz -d www.paing.xyz

# Auto-renewal
sudo certbot renew --dry-run
```

#### Railway.app:
- Automatic SSL (no setup needed)

#### Oracle Cloud:
```bash
sudo yum install certbot -y
sudo certbot certonly --standalone -d paing.xyz -d www.paing.xyz
```

---

### Step 5: Verify Domain & Webhook

#### Test Domain:
```bash
# Check DNS propagation
nslookup paing.xyz

# Test HTTP
curl http://paing.xyz

# Test HTTPS
curl https://paing.xyz
```

#### Test Webhook URL:
```bash
# Facebook webhook verification
curl "https://paing.xyz/webhook/facebook?hub.mode=subscribe&hub.verify_token=azone_bot_verify_token&hub.challenge=test123"
```

**Expected Response:** `test123`

---

### Step 6: Facebook Webhook Configuration

1. Facebook Developer Console → Your App
2. Messenger → Settings → Webhooks
3. Add Callback URL:
   ```
   https://paing.xyz/webhook/facebook
   ```
4. Verify Token:
   ```
   azone_bot_verify_token
   ```
5. Subscribe to events:
   - `messages`
   - `messaging_postbacks`
   - `messaging_optins`

---

## 🎯 Quick Setup Summary

### Current AWS VPS:
1. Domain provider → A record → `18.138.169.114`
2. VPS `.env` file → `DOMAIN=paing.xyz`
3. SSL certificate install
4. Project restart
5. Done! ✅

### Railway.app (Recommended):
1. Railway → Deploy from GitHub
2. Environment Variables → `DOMAIN=paing.xyz`
3. Custom Domain → `paing.xyz`
4. DNS CNAME record ထည့်ပါ
5. Done! ✅ (Automatic HTTPS)

---

## 📝 Project Files Status

✅ **Ready**: Project configuration က ready ဖြစ်ပြီးသား
- `config.py` - Domain support ✅
- `web_app.py` - Webhook URL generation ✅
- `env.example` - `DOMAIN=paing.xyz` ✅

**Update လုပ်စရာ:**
- `.env` file မှာ `DOMAIN=paing.xyz` ထည့်ရုံပါပဲ

---

## 🔗 Webhook URLs

After setup, these URLs will be available:

- **Facebook Webhook**: `https://paing.xyz/webhook/facebook`
- **Main App**: `https://paing.xyz`
- **Dashboard**: `https://paing.xyz/dashboard`

---

## ✅ Checklist

- [ ] Domain DNS A record (or CNAME) configured
- [ ] `.env` file မှာ `DOMAIN=paing.xyz` ထည့်ပြီး
- [ ] SSL certificate installed (HTTPS)
- [ ] Project deployed and running
- [ ] Webhook URL tested
- [ ] Facebook webhook configured

---

## 🎉 Done!

After completing these steps:
- ✅ Domain: `paing.xyz` working
- ✅ HTTPS: `https://paing.xyz` working
- ✅ Webhook: `https://paing.xyz/webhook/facebook` ready
- ✅ Facebook integration: Ready to use
