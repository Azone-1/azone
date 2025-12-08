# Free VPS Setup Guide - Domain & Webhook Configuration

## 🎯 ရည်ရွယ်ချက်
Free VPS ယူပြီး Domain နဲ့ Webhook URL ချိတ်ဆက်ရန်

---

## ✅ Best Free VPS Options (မြန်မာလို)

### Option 1: Oracle Cloud Free Tier (အကြံပြုထားသော) ⭐⭐⭐⭐⭐

**အကျိုးကျေးဇူးများ:**
- ✅ **Always Free** - ထာဝရ free (credit card လိုတယ်)
- ✅ **Powerful**: 2 VMs, 4 ARM cores, 24GB RAM
- ✅ **Domain support**: Custom domain ချိတ်ဆက်နိုင်တယ်
- ✅ **Webhook support**: HTTPS webhook URL လုပ်နိုင်တယ်
- ✅ **No time limit**: Forever free

**အားနည်းချက်:**
- ❌ Credit card လိုတယ် (ဒါပေမယ့် charge မလုပ်ဘူး)
- ❌ Setup က နည်းနည်း ရှုပ်တယ်

**Registration:**
1. https://www.oracle.com/cloud/free/ သို့ သွားပါ
2. "Start for Free" button ကို နှိပ်ပါ
3. Account ဖန်တီးပါ (credit card လိုတယ်)
4. Always Free resources ကို create လုပ်ပါ

---

### Option 2: Railway.app ⭐⭐⭐⭐

**အကျိုးကျေးဇူးများ:**
- ✅ **Easy deployment**: GitHub နဲ့ auto-deploy
- ✅ **Free tier**: $5 credit/month
- ✅ **Custom domain**: Free subdomain + custom domain support
- ✅ **HTTPS**: Automatic SSL certificate
- ✅ **Webhook support**: Perfect for webhooks

**အားနည်းချက်:**
- ❌ Free tier က limited (500 hours/month)
- ❌ Credit card လိုတယ်

**Registration:**
1. https://railway.app/ သို့ သွားပါ
2. GitHub account နဲ့ login လုပ်ပါ
3. "New Project" → "Deploy from GitHub repo"
4. Your Azone project ကို select လုပ်ပါ

---

### Option 3: Render.com ⭐⭐⭐⭐

**အကျိုးကျေးဇူးများ:**
- ✅ **Free tier**: 750 hours/month
- ✅ **Custom domain**: Free subdomain + custom domain
- ✅ **HTTPS**: Automatic SSL
- ✅ **Easy setup**: GitHub integration

**အားနည်းချက်:**
- ❌ Free tier က sleep mode (15 minutes inactive ဆိုရင် sleep)
- ❌ Credit card လိုတယ်

**Registration:**
1. https://render.com/ သို့ သွားပါ
2. GitHub account နဲ့ sign up လုပ်ပါ
3. "New Web Service" → "Public Git repository"
4. Your Azone repo ကို connect လုပ်ပါ

---

### Option 4: Fly.io ⭐⭐⭐

**အကျိုးကျေးဇူးများ:**
- ✅ **Free tier**: 3 shared VMs
- ✅ **Global**: Multiple regions
- ✅ **Custom domain**: Free subdomain + custom domain

**အားနည်းချက်:**
- ❌ Setup က နည်းနည်း ရှုပ်တယ်
- ❌ Credit card လိုတယ်

---

## 🎯 အကြံပြုထားသော Option

### **Oracle Cloud Free Tier** (အဆင့်မြင့် users အတွက်)
- Powerful resources
- Always free
- Full control

### **Railway.app** (အလွယ်ဆုံး)
- Easy deployment
- GitHub integration
- Automatic HTTPS

---

## 📋 Domain & Webhook Setup (အကုန် တစ်ခုထဲ)

### Step 1: Free Domain ယူရန်

**Free Domain Providers:**
1. **Freenom** (https://www.freenom.com/)
   - Free .tk, .ml, .ga, .cf domains
   - Registration လွယ်တယ်

2. **No-IP** (https://www.noip.com/)
   - Free subdomain
   - Dynamic DNS

3. **Cloudflare** (https://www.cloudflare.com/)
   - Free domain (limited)
   - Best DNS service

**အကြံပြုထားသော**: Freenom ကို သုံးပါ (.tk domain free)

---

### Step 2: VPS မှာ Project Deploy လုပ်ရန်

#### Oracle Cloud အတွက်:

```bash
# SSH connection
ssh opc@your-vps-ip

# Update system
sudo yum update -y

# Install Python 3.11
sudo yum install python3.11 python3.11-pip -y

# Install Git
sudo yum install git -y

# Clone your project
git clone https://github.com/yourusername/azone.git
cd azone

# Install dependencies
pip3.11 install -r requirements.txt

# Create .env file
nano .env
```

`.env` file ထဲမှာ:
```
DOMAIN=yourdomain.tk
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
```

#### Railway.app အတွက်:

1. Railway dashboard → "New Project"
2. "Deploy from GitHub repo"
3. Your Azone repo ကို select
4. Environment variables ထည့်ပါ:
   - `DOMAIN=yourdomain.tk`
   - `USE_HTTPS=True`
   - `PORT=5000`

---

### Step 3: Domain ကို VPS နဲ့ ချိတ်ဆက်ရန်

#### DNS Configuration:

1. **Freenom Domain Manager** မှာ:
   - Login → My Domains → Manage Domain
   - "Manage Freenom DNS" → Add Record

2. **DNS Records ထည့်ရန်:**
   ```
   Type: A
   Name: @ (or www)
   Target: Your VPS IP address
   TTL: 3600
   ```

3. **Subdomain အတွက်:**
   ```
   Type: A
   Name: bot
   Target: Your VPS IP address
   TTL: 3600
   ```

---

### Step 4: SSL Certificate (HTTPS) Setup

#### Oracle Cloud (Let's Encrypt):

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.tk -d www.yourdomain.tk

# Auto-renewal setup
sudo certbot renew --dry-run
```

#### Railway/Render:
- Automatic SSL (no setup needed)
- Just add domain in dashboard

---

### Step 5: Project Configuration Update

`config.py` file ကို update လုပ်ရန်:

```python
# Domain configuration
DOMAIN = os.getenv('DOMAIN', 'yourdomain.tk')
USE_HTTPS = os.getenv('USE_HTTPS', 'True')
```

`.env` file:
```
DOMAIN=yourdomain.tk
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
```

---

### Step 6: Webhook URL Test

Project run လုပ်ပြီးရင်:

```bash
# Test webhook URL
curl https://yourdomain.tk/webhook/facebook

# Facebook webhook verification
curl "https://yourdomain.tk/webhook/facebook?hub.mode=subscribe&hub.verify_token=azone_bot_verify_token&hub.challenge=test123"
```

---

## 🎯 Complete Setup Guide (တစ်ခုထဲ)

### Oracle Cloud Free Tier Setup:

1. **Register Oracle Cloud:**
   - https://www.oracle.com/cloud/free/
   - Credit card ထည့်ပါ (charge မလုပ်ဘူး)

2. **Create Always Free VM:**
   - Compute → Instances → Create Instance
   - Image: Oracle Linux 8
   - Shape: VM.Standard.A1.Flex (Always Free)
   - 4 OCPUs, 24GB RAM
   - Create

3. **SSH Connection:**
   ```bash
   ssh opc@your-vps-ip
   ```

4. **Install Dependencies:**
   ```bash
   sudo yum update -y
   sudo yum install python3.11 python3.11-pip git -y
   ```

5. **Deploy Project:**
   ```bash
   git clone https://github.com/yourusername/azone.git
   cd azone
   pip3.11 install -r requirements.txt
   ```

6. **Configure Domain:**
   - Freenom မှာ domain ယူပါ
   - DNS A record ထည့်ပါ (VPS IP)
   - `.env` file မှာ `DOMAIN=yourdomain.tk`

7. **Setup SSL:**
   ```bash
   sudo yum install certbot -y
   sudo certbot certonly --standalone -d yourdomain.tk
   ```

8. **Run Project:**
   ```bash
   python3.11 web_app.py
   ```

---

### Railway.app Setup (အလွယ်ဆုံး):

1. **Register Railway:**
   - https://railway.app/
   - GitHub account နဲ့ login

2. **Deploy:**
   - "New Project" → "Deploy from GitHub repo"
   - Your Azone repo select

3. **Configure Domain:**
   - Settings → Domains → Add Custom Domain
   - `yourdomain.tk` ထည့်ပါ
   - DNS records ကို Railway က ပေးတဲ့ values နဲ့ update လုပ်ပါ

4. **Environment Variables:**
   - Variables tab → Add:
     - `DOMAIN=yourdomain.tk`
     - `USE_HTTPS=True`

5. **Done!** Automatic deployment

---

## 💰 Cost Comparison

| Option | Cost | Setup Difficulty | Best For |
|--------|------|------------------|----------|
| Oracle Cloud | Free Forever | Medium | Full control |
| Railway | $5/month free | Easy | Quick deployment |
| Render | Free tier | Easy | Simple apps |
| Current AWS | ~15,000 MMK/month | Hard | Already have |

---

## 🎯 Recommendation

**အကြံပြုထားသော:**
- **Oracle Cloud Free Tier** - Powerful & forever free
- **Railway.app** - Easiest deployment

**Project update လုပ်ရန်:**
- Domain configuration က `config.py` နဲ့ `.env` file မှာ ရှိပြီးသား
- Webhook URL က automatically `DOMAIN` variable ကို သုံးပါတယ်
- Update လုပ်ရန် `.env` file ကို edit လုပ်ရုံပါပဲ

---

## ✅ Quick Start (Railway.app - အလွယ်ဆုံး)

1. Railway.app မှာ account ဖန်တီးပါ
2. GitHub repo ကို connect လုပ်ပါ
3. Environment variables ထည့်ပါ:
   ```
   DOMAIN=yourdomain.tk
   USE_HTTPS=True
   ```
4. Custom domain ထည့်ပါ
5. Done! Webhook URL: `https://yourdomain.tk/webhook/facebook`

---

## 📝 Project Files Update လုပ်စရာ

Project မှာ update လုပ်စရာ မရှိပါဘူး! 

`config.py` နဲ့ `web_app.py` မှာ domain configuration က ရှိပြီးသား:
- `DOMAIN` environment variable ကို သုံးပါတယ်
- Webhook URL automatically generate လုပ်ပါတယ်
- `.env` file မှာ `DOMAIN=yourdomain.tk` ထည့်ရုံပါပဲ
