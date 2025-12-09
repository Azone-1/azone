# 🚀 VPS Deployment - Complete Guide (Myanmar Users)

Railway က Parpid card လက်မခံတဲ့အတွက် VPS သုံးပြီး deploy လုပ်ရန် guide ပါ။

---

## ⚡ Quick Start (5 Minutes)

### Step 1: VPS ဝယ်ပါ
**Recommended**: Contabo (€4.99/month) - Myanmar cards work!
- Link: https://www.contabo.com
- Choose: VPS S (€4.99/month)
- OS: Ubuntu 22.04 LTS

### Step 2: Code Upload လုပ်ပါ
```bash
# VPS မှာ run လုပ်ပါ
cd ~
git clone https://github.com/Apaing9611-arch/azone.git
cd azone
```

### Step 3: Automated Setup Run လုပ်ပါ
```bash
chmod +x QUICK_VPS_SETUP.sh
bash QUICK_VPS_SETUP.sh
```

**✅ Done!** Your app will be running at `http://YOUR_VPS_IP`

---

## 📋 Detailed Steps

### 1. VPS Provider ရွေးချယ်ပါ

**Best Options:**
- **Contabo** (€4.99) - Myanmar cards ✅
- **Vultr** ($6) - Some Myanmar cards ✅
- **Oracle Cloud** (FREE) - Myanmar cards ✅

See `VPS_PROVIDERS_COMPARISON.md` for details.

### 2. VPS Create လုပ်ပါ

#### Contabo:
1. https://www.contabo.com → Sign up
2. VPS → VPS S → Ubuntu 22.04
3. Payment (Myanmar card should work!)
4. Wait 5 minutes

#### Vultr:
1. https://www.vultr.com → Sign up ($100 free credit!)
2. Deploy → Server → Ubuntu 22.04
3. $6/month plan
4. Deploy

#### Oracle Cloud (FREE):
1. https://www.oracle.com/cloud/free → Sign up
2. Create Always Free VM
3. Ubuntu 22.04
4. Free forever!

### 3. SSH Connect လုပ်ပါ

```bash
# Windows PowerShell
ssh root@YOUR_VPS_IP

# Password သို့မဟုတ် key file သုံးပါ
ssh -i your-key.pem root@YOUR_VPS_IP
```

### 4. Code Upload လုပ်ပါ

**Method 1: Git Clone (Recommended)**
```bash
cd ~
git clone https://github.com/Apaing9611-arch/azone.git
cd azone
```

**Method 2: SCP Upload (Windows)**
```powershell
# PowerShell မှာ
scp -r C:\Users\User\Desktop\Azone root@YOUR_VPS_IP:/root/Azone
```

### 5. Automated Setup Run လုပ်ပါ

```bash
cd ~/Azone
chmod +x QUICK_VPS_SETUP.sh
bash QUICK_VPS_SETUP.sh
```

Script က အကုန်လုပ်ပေးမယ်:
- ✅ Python & dependencies install
- ✅ PM2 process manager setup
- ✅ Nginx web server configuration
- ✅ Firewall setup
- ✅ Database initialization
- ✅ Environment variables setup

### 6. Verify Installation

```bash
# Check PM2 status
pm2 status

# Check Nginx status
sudo systemctl status nginx

# View logs
pm2 logs azone-bot
```

### 7. Access Your App

- **HTTP**: `http://YOUR_VPS_IP`
- **Direct Flask**: `http://YOUR_VPS_IP:5000`
- **Dashboard**: `http://YOUR_VPS_IP/dashboard`

---

## 🔧 Manual Setup (If Script Fails)

### Install Python & Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
cd ~/Azone
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install PM2
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
```

### Start Flask App
```bash
cd ~/Azone
pm2 start web_app.py --name "azone-bot" --interpreter python3
pm2 save
pm2 startup  # Follow instructions
```

### Install Nginx
```bash
sudo apt install -y nginx
sudo nano /etc/nginx/sites-available/azone
```

Paste this config:
```nginx
server {
    listen 80;
    server_name YOUR_VPS_IP_OR_DOMAIN;

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

---

## 🔒 SSL Setup (Optional but Recommended)

### Using Let's Encrypt (Free SSL)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Auto-renewal
```bash
sudo certbot renew --dry-run
```

---

## 📊 Useful Commands

### PM2 Commands
```bash
pm2 status              # Check status
pm2 logs azone-bot      # View logs
pm2 restart azone-bot   # Restart
pm2 stop azone-bot      # Stop
pm2 monit               # Monitor dashboard
```

### Nginx Commands
```bash
sudo systemctl status nginx    # Status
sudo nginx -t                  # Test config
sudo systemctl restart nginx   # Restart
sudo tail -f /var/log/nginx/error.log  # View errors
```

### Database Commands
```bash
cd ~/Azone
python3 -c "import db_manager; db_manager.init_database()"
python3 create_sample_data.py
```

---

## 🆘 Troubleshooting

### App Not Starting?
```bash
pm2 logs azone-bot
cd ~/Azone
python3 web_app.py  # Run directly to see errors
```

### Port Already in Use?
```bash
sudo lsof -i :5000
pm2 stop azone-bot
pm2 start azone-bot
```

### Nginx 502 Bad Gateway?
```bash
# Check Flask is running
pm2 status

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Verify port in Nginx config
sudo nano /etc/nginx/sites-available/azone
```

### Database Errors?
```bash
cd ~/Azone
python3 -c "import db_manager; db_manager.init_database()"
ls -la *.db
```

---

## 🌐 Domain Setup (Optional)

### Step 1: Domain ဝယ်ပါ
- Namecheap, GoDaddy, Cloudflare

### Step 2: DNS Configuration
Add A Record:
```
Type: A
Name: @
Value: YOUR_VPS_IP
TTL: 3600
```

### Step 3: Update Nginx Config
```bash
sudo nano /etc/nginx/sites-available/azone
# Change server_name to your domain
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## ✅ Checklist

- [ ] VPS created
- [ ] SSH access working
- [ ] Code uploaded
- [ ] Dependencies installed
- [ ] PM2 running
- [ ] Nginx configured
- [ ] App accessible
- [ ] Domain configured (optional)
- [ ] SSL installed (optional)

---

## 🎉 Success!

Your app is now running on VPS:
- ✅ 24/7 uptime with PM2
- ✅ Auto-restart on crash
- ✅ Web server (Nginx)
- ✅ SSL/HTTPS ready
- ✅ Production ready!

**Access**: `http://YOUR_VPS_IP` or `http://yourdomain.com`

---

## 📚 More Resources

- **VPS Providers**: See `VPS_PROVIDERS_COMPARISON.md`
- **Detailed Guide**: See `VPS_DEPLOY_GUIDE.md`
- **Scripts**: `QUICK_VPS_SETUP.sh`, `MASTER_DEPLOY.sh`

**Good luck! 🚀**
