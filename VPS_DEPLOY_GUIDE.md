# 🚀 VPS Deployment Guide - Myanmar Users (Parpid Card Friendly)

Railway က Parpid card လက်မခံတဲ့အတွက် VPS သုံးပြီး deploy လုပ်ရန် guide ပါ။

---

## 🎯 VPS Provider Options (Parpid Card နဲ့ ရနိုင်တဲ့)

### 1. **DigitalOcean** (Recommended) ⭐
- **Price**: $6/month (1GB RAM, 1 vCPU)
- **Payment**: Credit Card, PayPal
- **Free Trial**: $200 credit (60 days)
- **Link**: https://www.digitalocean.com
- **Myanmar Card**: ❌ (PayPal နဲ့ ရနိုင်တယ်)

### 2. **Vultr** (Best for Myanmar) ⭐⭐⭐
- **Price**: $6/month (1GB RAM, 1 vCPU)
- **Payment**: Credit Card, PayPal, Crypto
- **Free Trial**: $100 credit
- **Link**: https://www.vultr.com
- **Myanmar Card**: ✅ (Some cards work)

### 3. **Linode** (Now Akamai)
- **Price**: $5/month (1GB RAM, 1 vCPU)
- **Payment**: Credit Card, PayPal
- **Link**: https://www.linode.com
- **Myanmar Card**: ❌ (PayPal နဲ့ ရနိုင်တယ်)

### 4. **Contabo** (Cheapest) 💰
- **Price**: €4.99/month (~$5.50)
- **Payment**: Credit Card, PayPal, Bank Transfer
- **Link**: https://www.contabo.com
- **Myanmar Card**: ✅ (Most Myanmar cards work!)

### 5. **Hetzner** (Best Value)
- **Price**: €4.15/month (~$4.50)
- **Payment**: Credit Card, PayPal, SEPA
- **Link**: https://www.hetzner.com
- **Myanmar Card**: ❌ (PayPal နဲ့ ရနိုင်တယ်)

### 6. **Free Options** (For Testing)
- **Oracle Cloud**: Free tier (Always Free)
- **Google Cloud**: $300 free credit
- **AWS**: Free tier (12 months)

---

## 📋 Step-by-Step VPS Deployment

### **Option A: Automated Script (Recommended)** ⚡

#### Step 1: VPS ဝယ်ပါ
1. Contabo သို့မဟုတ် Vultr မှာ account ဖွင့်ပါ
2. Ubuntu 22.04 LTS VPS create လုပ်ပါ
3. SSH key သို့မဟုတ် password သိမ်းထားပါ

#### Step 2: VPS ကို Connect လုပ်ပါ
```bash
# Windows PowerShell မှာ
ssh root@YOUR_VPS_IP

# သို့မဟုတ်
ssh -i your-key.pem root@YOUR_VPS_IP
```

#### Step 3: Code Upload လုပ်ပါ
```bash
# Method 1: Git Clone (Recommended)
cd ~
git clone https://github.com/Apaing9611-arch/azone.git
cd azone

# Method 2: SCP Upload (Windows)
# PowerShell မှာ:
scp -r C:\Users\User\Desktop\Azone root@YOUR_VPS_IP:/root/Azone
```

#### Step 4: Automated Deploy Script Run လုပ်ပါ
```bash
cd ~/Azone  # or /root/Azone
chmod +x MASTER_DEPLOY.sh
bash MASTER_DEPLOY.sh
```

**✅ Done!** Script က အကုန်လုပ်ပေးမယ်:
- Python & dependencies install
- PM2 setup
- Nginx configuration
- SSL certificate
- Firewall setup

---

### **Option B: Manual Setup** (Step-by-Step)

#### Step 1: System Update
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Python & Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv git
cd ~/Azone
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 3: Install PM2 (Process Manager)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
```

#### Step 4: Start Flask App with PM2
```bash
cd ~/Azone
pm2 start web_app.py --name "azone-bot" --interpreter python3
pm2 save
pm2 startup  # Follow instructions shown
```

#### Step 5: Install & Configure Nginx
```bash
sudo apt install -y nginx
```

Create Nginx config:
```bash
sudo nano /etc/nginx/sites-available/azone
```

Paste this (replace `YOUR_DOMAIN` with your domain or IP):
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /root/Azone/static;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/azone /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 6: Setup SSL (Optional but Recommended)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d YOUR_DOMAIN
```

#### Step 7: Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 🔧 Configuration Files

### Environment Variables (.env file)
Create `.env` file in project root:
```bash
nano ~/Azone/.env
```

Add:
```
SECRET_KEY=your-random-secret-key-here-min-32-chars
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
HOST=0.0.0.0
PORT=5000
DOMAIN=your-domain.com
```

### Generate Secret Key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📊 Useful Commands

### PM2 Commands
```bash
pm2 status              # Check status
pm2 logs azone-bot      # View logs
pm2 restart azone-bot   # Restart app
pm2 stop azone-bot      # Stop app
pm2 monit               # Monitor dashboard
```

### Nginx Commands
```bash
sudo systemctl status nginx    # Check status
sudo nginx -t                  # Test config
sudo systemctl restart nginx   # Restart
sudo tail -f /var/log/nginx/error.log  # View errors
```

### Database Commands
```bash
cd ~/Azone
python3 -c "import db_manager; db_manager.init_database()"
python3 create_sample_data.py  # Add sample data
```

---

## 🌐 Domain Setup (Optional)

### Step 1: Domain ဝယ်ပါ
- Namecheap, GoDaddy, Cloudflare စတာတွေမှာ domain ဝယ်ပါ

### Step 2: DNS Configuration
Domain provider မှာ A Record ထည့်ပါ:
```
Type: A
Name: @ (or blank)
Value: YOUR_VPS_IP
TTL: 3600
```

WWW subdomain:
```
Type: A
Name: www
Value: YOUR_VPS_IP
TTL: 3600
```

### Step 3: SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## ✅ Testing Checklist

- [ ] VPS created and accessible via SSH
- [ ] Code uploaded to VPS
- [ ] Python dependencies installed
- [ ] PM2 running (`pm2 status`)
- [ ] Flask app accessible on port 5000
- [ ] Nginx configured and running
- [ ] Domain pointing to VPS (if using domain)
- [ ] SSL certificate installed (if using domain)
- [ ] Firewall configured
- [ ] Database initialized
- [ ] Admin user created

---

## 🆘 Troubleshooting

### App Not Starting?
```bash
pm2 logs azone-bot  # Check logs
cd ~/Azone
python3 web_app.py  # Run directly to see errors
```

### Port Already in Use?
```bash
sudo lsof -i :5000  # Check what's using port 5000
pm2 stop azone-bot
pm2 start azone-bot
```

### Nginx 502 Bad Gateway?
```bash
# Check if Flask app is running
pm2 status

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify proxy_pass port matches Flask port
sudo nano /etc/nginx/sites-available/azone
```

### Database Errors?
```bash
cd ~/Azone
python3 -c "import db_manager; db_manager.init_database()"
ls -la *.db  # Check database files exist
```

---

## 💰 Cost Comparison

| Provider | Monthly Cost | Myanmar Card | Best For |
|----------|--------------|--------------|----------|
| **Contabo** | €4.99 (~$5.50) | ✅ Yes | Budget users |
| **Vultr** | $6 | ✅ Sometimes | Myanmar users |
| **DigitalOcean** | $6 | ❌ (PayPal OK) | Beginners |
| **Hetzner** | €4.15 (~$4.50) | ❌ (PayPal OK) | Best value |
| **Oracle Cloud** | FREE | ✅ Yes | Testing |

---

## 🎉 Success!

Deploy လုပ်ပြီးရင်:
- ✅ Your app: `http://YOUR_VPS_IP:5000` or `http://yourdomain.com`
- ✅ Dashboard: `http://YOUR_VPS_IP/dashboard`
- ✅ 24/7 running with PM2
- ✅ Auto-restart on crash
- ✅ SSL/HTTPS ready

---

## 📞 Need Help?

1. Check PM2 logs: `pm2 logs azone-bot`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Test Flask directly: `cd ~/Azone && python3 web_app.py`

**Good luck! 🚀**
